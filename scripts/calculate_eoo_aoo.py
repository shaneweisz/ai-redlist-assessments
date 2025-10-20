#!/usr/bin/env python3
"""
Calculate Extent of Occurrence (EOO) and Area of Occupancy (AOO)
following IUCN Red List guidelines.

Usage:
    python scripts/calculate_eoo_aoo.py <species_name>

Example:
    python scripts/calculate_eoo_aoo.py "panthera_leo"
"""

import sys
import json
from pathlib import Path
import geopandas as gpd
from shapely.geometry import Point, MultiPoint
import numpy as np


def load_occurrence_data(species_name):
    """Load occurrence data from agent output"""
    data_file = Path(f"data/{species_name}/02_occurrence_data.json")

    if not data_file.exists():
        raise FileNotFoundError(f"Occurrence data not found: {data_file}")

    with open(data_file, 'r') as f:
        return json.load(f)


def calculate_eoo(points):
    """
    Calculate Extent of Occurrence as minimum convex polygon area

    Args:
        points: List of (lon, lat) tuples

    Returns:
        eoo_km2: Area in square kilometers
        convex_hull_coords: List of coordinates forming the convex hull
    """
    if len(points) < 3:
        return None, None

    # Create MultiPoint geometry
    multipoint = MultiPoint(points)

    # Calculate convex hull
    convex_hull = multipoint.convex_hull

    # Convert to geodataframe for area calculation in proper CRS
    gdf = gpd.GeoDataFrame([1], geometry=[convex_hull], crs="EPSG:4326")

    # Project to equal area projection (World Mollweide)
    gdf_projected = gdf.to_crs("ESRI:54009")

    # Calculate area in km²
    eoo_km2 = gdf_projected.geometry.area[0] / 1_000_000

    # Get convex hull coordinates for mapping
    hull_coords = list(convex_hull.exterior.coords)

    return eoo_km2, hull_coords


def calculate_aoo(points, cell_size_km=2):
    """
    Calculate Area of Occupancy using a grid-based approach

    Args:
        points: List of (lon, lat) tuples
        cell_size_km: Grid cell size in kilometers (default 2km per IUCN)

    Returns:
        aoo_km2: Area in square kilometers
        n_cells: Number of occupied cells
    """
    if len(points) < 1:
        return None, 0

    # Convert to geodataframe
    geometry = [Point(lon, lat) for lon, lat in points]
    gdf = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:4326")

    # Project to equal area projection
    gdf_projected = gdf.to_crs("ESRI:54009")

    # Create grid cells
    # Cell size is in meters (2km = 2000m)
    cell_size_m = cell_size_km * 1000

    # Get bounds
    minx, miny, maxx, maxy = gdf_projected.total_bounds

    # Create grid
    from shapely.geometry import box

    cols = int((maxx - minx) / cell_size_m) + 1
    rows = int((maxy - miny) / cell_size_m) + 1

    cells = set()

    # Assign each point to a grid cell
    for geom in gdf_projected.geometry:
        col = int((geom.x - minx) / cell_size_m)
        row = int((geom.y - miny) / cell_size_m)
        cells.add((col, row))

    # Number of occupied cells
    n_cells = len(cells)

    # AOO is number of cells × cell area
    aoo_km2 = n_cells * (cell_size_km ** 2)

    return aoo_km2, n_cells


def assess_criterion_b(eoo_km2, aoo_km2):
    """
    Assess IUCN Criterion B thresholds

    Returns:
        dict with b1_met, b2_met, b1_category, b2_category
    """
    result = {
        "b1_met": False,
        "b1_category": None,
        "b2_met": False,
        "b2_category": None
    }

    if eoo_km2 is None or aoo_km2 is None:
        return result

    # B1 (EOO) thresholds
    if eoo_km2 < 100:
        result["b1_met"] = True
        result["b1_category"] = "CR"
    elif eoo_km2 < 5000:
        result["b1_met"] = True
        result["b1_category"] = "EN"
    elif eoo_km2 < 20000:
        result["b1_met"] = True
        result["b1_category"] = "VU"

    # B2 (AOO) thresholds
    if aoo_km2 < 10:
        result["b2_met"] = True
        result["b2_category"] = "CR"
    elif aoo_km2 < 500:
        result["b2_met"] = True
        result["b2_category"] = "EN"
    elif aoo_km2 < 2000:
        result["b2_met"] = True
        result["b2_category"] = "VU"

    return result


def main(species_name):
    """Main execution function"""

    print(f"Calculating EOO and AOO for {species_name}...")

    # Load occurrence data
    try:
        occ_data = load_occurrence_data(species_name)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Extract coordinates
    points_data = occ_data.get("data", {}).get("occurrence_points", [])

    if not points_data:
        print("Error: No occurrence points found in data")
        sys.exit(1)

    # Convert to (lon, lat) tuples - handle both formats
    points = []
    for p in points_data:
        if "lon" in p and "lat" in p:
            points.append((p["lon"], p["lat"]))
        elif "longitude" in p and "latitude" in p:
            points.append((p["longitude"], p["latitude"]))

    print(f"Processing {len(points)} occurrence points...")

    # Calculate EOO
    eoo_km2, hull_coords = calculate_eoo(points)

    if eoo_km2 is None:
        print("Error: Not enough points to calculate EOO (need at least 3)")
        sys.exit(1)

    print(f"EOO: {eoo_km2:,.0f} km²")

    # Calculate AOO
    aoo_km2, n_cells = calculate_aoo(points, cell_size_km=2)

    print(f"AOO: {aoo_km2:,.0f} km² ({n_cells} grid cells)")

    # Assess Criterion B
    criterion_b = assess_criterion_b(eoo_km2, aoo_km2)

    # Validation check
    if eoo_km2 < aoo_km2:
        print(f"WARNING: EOO ({eoo_km2:.0f}) < AOO ({aoo_km2:.0f}), which is impossible!")

    # Calculate bounding box
    lons = [p[0] for p in points]
    lats = [p[1] for p in points]

    bounding_box = {
        "min_lat": min(lats),
        "max_lat": max(lats),
        "min_lon": min(lons),
        "max_lon": max(lons)
    }

    # Calculate centroid
    centroid = {
        "lat": np.mean(lats),
        "lon": np.mean(lons)
    }

    # Prepare output
    output = {
        "status": "success",
        "agent": "geographic",
        "species_name": species_name.replace("_", " ").title(),
        "confidence": 0.85 if len(points) > 100 else 0.6,
        "data": {
            "eoo_km2": round(eoo_km2, 2),
            "aoo_km2": round(aoo_km2, 2),
            "number_of_locations": "TBD - requires expert analysis",
            "severely_fragmented": "TBD - requires expert analysis",
            "criterion_b": {
                **criterion_b,
                "notes": f"EOO: {eoo_km2:,.0f} km². AOO: {aoo_km2:,.0f} km²."
            },
            "geographic_range": {
                "centroid": centroid,
                "bounding_box": bounding_box,
                "convex_hull_coords": hull_coords
            },
            "spatial_analysis": {
                "number_of_occurrences": len(points),
                "number_of_unique_cells": n_cells,
                "spatial_extent_km2": round(eoo_km2, 2)
            }
        },
        "metadata": {
            "method": "python_geopandas",
            "grid_size_km": 2,
            "crs": "EPSG:4326"
        },
        "warnings": [],
        "errors": []
    }

    # Save output
    output_file = Path(f"data/{species_name}/03_range_metrics.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n✓ Results saved to {output_file}")

    # Print Criterion B assessment
    if criterion_b["b1_met"] or criterion_b["b2_met"]:
        print("\n⚠️  Criterion B thresholds met:")
        if criterion_b["b1_met"]:
            print(f"   - B1 (EOO): {criterion_b['b1_category']}")
        if criterion_b["b2_met"]:
            print(f"   - B2 (AOO): {criterion_b['b2_category']}")
    else:
        print("\n✓ No Criterion B thresholds met")

    return output


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/calculate_eoo_aoo.py <species_name>")
        print('Example: python scripts/calculate_eoo_aoo.py "panthera_leo"')
        sys.exit(1)

    species = sys.argv[1].lower().replace(" ", "_")
    main(species)
