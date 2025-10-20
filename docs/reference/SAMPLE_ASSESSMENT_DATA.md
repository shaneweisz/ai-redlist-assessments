# IUCN Red List Assessment Data Structure

This document provides examples of the data structure used in IUCN Red List assessments, based on the official API.

## Overview

The IUCN Red List API returns comprehensive assessment data in JSON format. Each assessment contains:
- Taxonomic information
- Conservation status and criteria
- Population and distribution data
- Habitat and ecology information
- Threats
- Conservation actions
- Documentation and rationale

## Example 1: Atlantic Puffin (Fratercula arctica)

### Basic Assessment Response

```json
{
  "name": "Fratercula arctica",
  "result": [{
    "taxonid": 22694927,
    "scientific_name": "Fratercula arctica",
    "kingdom": "ANIMALIA",
    "phylum": "CHORDATA",
    "class": "AVES",
    "order": "CHARADRIIFORMES",
    "family": "ALCIDAE",
    "genus": "Fratercula",
    "main_common_name": "Atlantic Puffin",
    "authority": "(Linnaeus, 1758)",
    "published_year": 2017,
    "assessment_date": "2017-10-01",
    "category": "VU",
    "criteria": "A4abcde",
    "population_trend": "Decreasing",
    "marine_system": true,
    "freshwater_system": false,
    "terrestrial_system": true,
    "assessor": "BirdLife International",
    "reviewer": "Symes, A.",
    "aoo_km2": null,
    "eoo_km2": "20800000",
    "elevation_upper": null,
    "elevation_lower": null,
    "depth_upper": null,
    "depth_lower": null,
    "errata_flag": null,
    "errata_reason": null,
    "amended_flag": null,
    "amended_reason": null
  }]
}
```

## Complete Assessment Data Structure

### Core Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `taxonid` | integer | Unique IUCN taxon identifier | 22694927 |
| `scientific_name` | string | Full scientific name | "Fratercula arctica" |
| `kingdom` | string | Taxonomic kingdom | "ANIMALIA" |
| `phylum` | string | Taxonomic phylum | "CHORDATA" |
| `class` | string | Taxonomic class | "AVES" |
| `order` | string | Taxonomic order | "CHARADRIIFORMES" |
| `family` | string | Taxonomic family | "ALCIDAE" |
| `genus` | string | Genus name | "Fratercula" |
| `species_name` | string | Species epithet | "arctica" |
| `authority` | string | Taxonomic authority | "(Linnaeus, 1758)" |
| `main_common_name` | string | Primary common name | "Atlantic Puffin" |
| `published_year` | integer | Year published on Red List | 2017 |
| `assessment_date` | date | Date of assessment | "2017-10-01" |

### Assessment Status Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `category` | string | Red List category code | "VU" (Vulnerable) |
| `criteria` | string | IUCN criteria met | "A4abcde" |
| `population_trend` | string | Direction of population change | "Decreasing", "Increasing", "Stable", "Unknown" |

**Category Codes:**
- `EX` - Extinct
- `EW` - Extinct in the Wild
- `CR` - Critically Endangered
- `EN` - Endangered
- `VU` - Vulnerable
- `NT` - Near Threatened
- `LC` - Least Concern
- `DD` - Data Deficient
- `NE` - Not Evaluated

### Spatial and Ecological Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `aoo_km2` | float/null | Area of Occupancy (km²) | 5000 |
| `eoo_km2` | float/null | Extent of Occurrence (km²) | 20800000 |
| `elevation_upper` | integer/null | Maximum elevation (m) | 2000 |
| `elevation_lower` | integer/null | Minimum elevation (m) | 0 |
| `depth_upper` | integer/null | Maximum depth (m) | -50 |
| `depth_lower` | integer/null | Minimum depth (m) | 0 |
| `marine_system` | boolean | Occurs in marine systems | true |
| `freshwater_system` | boolean | Occurs in freshwater systems | false |
| `terrestrial_system` | boolean | Occurs in terrestrial systems | true |

### Quality Control Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `assessor` | string | Name(s) of assessor(s) | "BirdLife International" |
| `reviewer` | string | Name(s) of reviewer(s) | "Symes, A." |
| `errata_flag` | boolean/null | Has errata been issued | null |
| `errata_reason` | string/null | Reason for errata | null |
| `amended_flag` | boolean/null | Has been amended | null |
| `amended_reason` | string/null | Reason for amendment | null |

## Extended Assessment Data

A full assessment includes additional nested structures:

### Habitats

```json
{
  "habitats": [
    {
      "code": "1.5",
      "habitat": "Forest - Subtropical/Tropical Dry",
      "suitability": "Suitable",
      "season": "Resident",
      "majorimportance": "Yes"
    }
  ]
}
```

### Threats

```json
{
  "threats": [
    {
      "code": "2.1",
      "title": "Agriculture & aquaculture",
      "timing": "Ongoing",
      "scope": "Majority (50-90%)",
      "severity": "Rapid Declines",
      "score": "High Impact: 8"
    }
  ]
}
```

**Common Threat Codes:**
- `1.x` - Residential & commercial development
- `2.x` - Agriculture & aquaculture
- `3.x` - Energy production & mining
- `4.x` - Transportation & service corridors
- `5.x` - Biological resource use
- `6.x` - Human intrusions & disturbance
- `7.x` - Natural system modifications
- `8.x` - Invasive & other problematic species
- `9.x` - Pollution
- `10.x` - Geological events
- `11.x` - Climate change & severe weather

### Conservation Actions

```json
{
  "conservation_actions": [
    {
      "code": "1.1",
      "title": "Land/water protection - Site/area protection",
      "status": "On-going"
    }
  ]
}
```

### Documentation

```json
{
  "rationale": "This species has been classified as Vulnerable because...",
  "geographic_range": "This species occurs across...",
  "population": "The global population is estimated at...",
  "habitat_and_ecology": "This species inhabits...",
  "use_and_trade": "This species is used for...",
  "threats_narrative": "The major threats to this species include...",
  "conservation_actions_narrative": "Conservation measures include..."
}
```

## Criteria Interpretation

### Criterion A (Population Reduction)

**Format:** `A2abc` or `A4abcde`

- **Number** (1-4): Time period
  - `A1` - Past reduction (causes reversible/understood/ceased)
  - `A2` - Past reduction (causes may not have ceased)
  - `A3` - Future reduction
  - `A4` - Past + future reduction

- **Letters** (a-e): Evidence basis
  - `a` - Direct observation
  - `b` - Index of abundance
  - `c` - Decline in area/quality of habitat
  - `d` - Exploitation levels
  - `e` - Effects of introduced taxa, hybridization, pathogens, pollutants, competitors or parasites

**Thresholds:**
- CR: ≥90% reduction
- EN: ≥70% reduction
- VU: ≥50% reduction
- NT: ≥30% reduction

### Criterion B (Geographic Range)

**Format:** `B1ab(i,ii,iii)+2ab(i,ii,iii)`

- `B1` - Extent of Occurrence (EOO)
- `B2` - Area of Occupancy (AOO)

**Sub-criteria (a-c):**
- `a` - Severely fragmented or number of locations
- `b` - Continuing decline in:
  - `(i)` - extent of occurrence
  - `(ii)` - area of occupancy
  - `(iii)` - area/extent/quality of habitat
  - `(iv)` - number of locations/subpopulations
  - `(v)` - number of mature individuals
- `c` - Extreme fluctuations

**Thresholds:**
- CR: EOO <100 km² OR AOO <10 km²
- EN: EOO <5,000 km² OR AOO <500 km²
- VU: EOO <20,000 km² OR AOO <2,000 km²

### Criterion C (Small Population Size and Decline)

**Format:** `C2a(i)`

**Thresholds:**
- CR: <250 mature individuals
- EN: <2,500 mature individuals
- VU: <10,000 mature individuals

**Sub-criteria:**
- `C1` - Continuing decline
- `C2` - Continuing decline + population structure
  - `C2a` - Number in largest subpopulation
    - `(i)` - CR: <50, EN: <250, VU: <1,000
  - `C2b` - % in one subpopulation

### Criterion D (Very Small or Restricted Population)

**Thresholds:**
- CR: <50 mature individuals
- EN: <250 mature individuals
- VU: D1: <1,000 OR D2: AOO <20 km² or ≤5 locations

### Criterion E (Quantitative Analysis)

Extinction probability:
- CR: ≥50% in 10 years or 3 generations
- EN: ≥20% in 20 years or 5 generations
- VU: ≥10% in 100 years

## API Endpoints

### Base URL
```
https://apiv3.iucnredlist.org/api/v3
```

### Key Endpoints

1. **Get species by name**
   ```
   GET /species/{name}
   ```

2. **Get species by ID**
   ```
   GET /species/id/{id}
   ```

3. **Get assessment by ID**
   ```
   GET /assessment/{assessment_id}
   ```

4. **Get species narrative**
   ```
   GET /species/narrative/{name}
   ```

5. **Get habitats**
   ```
   GET /habitats/species/name/{name}
   ```

6. **Get threats**
   ```
   GET /threats/species/name/{name}
   ```

7. **Get conservation measures**
   ```
   GET /measures/species/name/{name}
   ```

8. **Search species**
   ```
   GET /species/find/{search_term}
   ```

All endpoints require authentication via API token:
```
?token=YOUR_API_TOKEN
```

## Data for AI Automation

### Most Automatable Fields

1. **Taxonomy** - Can be extracted from literature/databases
   - scientific_name, kingdom, phylum, class, order, family, genus
   - Confidence: High

2. **Distribution data** - Can be extracted from occurrence databases
   - eoo_km2, aoo_km2, elevation ranges
   - Confidence: Medium-High

3. **Habitat classification** - Can be inferred from literature
   - Habitat codes and descriptions
   - Confidence: Medium

4. **Population trend indicators** - Can be extracted from papers
   - Numeric population estimates
   - Time series data
   - Confidence: Medium

5. **Threat identification** - Text mining from literature
   - Threat categories and severity
   - Confidence: Medium

### Challenging for Automation

1. **Criteria application** - Requires expert judgment
   - Interpreting threshold boundaries
   - Selecting appropriate criteria
   - Confidence: Low-Medium

2. **Rationale text** - Requires synthesis and reasoning
   - Justifying category assignment
   - Weighing evidence quality
   - Confidence: Medium (with LLMs)

3. **Conservation actions** - Requires current knowledge
   - Identifying ongoing measures
   - Assessing effectiveness
   - Confidence: Low-Medium

4. **Data quality assessment** - Requires expertise
   - Determining data reliability
   - Identifying knowledge gaps
   - Confidence: Low

## Example Workflow for AI-Assisted Assessment

1. **Data Collection**
   - Extract species occurrence records (GBIF, iNaturalist)
   - Mine scientific literature for population data
   - Gather habitat information from field guides

2. **Preliminary Calculations**
   - Calculate EOO and AOO from occurrence data
   - Analyze population trend from time series
   - Identify habitat types from descriptions

3. **Threat Analysis**
   - Extract threats mentioned in literature
   - Classify threats using IUCN threat taxonomy
   - Score severity based on text analysis

4. **Draft Assessment**
   - Generate preliminary category based on calculations
   - Create rationale text using LLM
   - Flag uncertainties for expert review

5. **Expert Review**
   - Validate AI-generated category
   - Refine rationale text
   - Add expert knowledge
   - Submit via SIS

## Resources

- **API Documentation:** https://api.iucnredlist.org/api-docs
- **Categories & Criteria:** https://www.iucnredlist.org/resources/categories-and-criteria
- **Guidelines:** https://www.iucnredlist.org/resources/redlistguidelines
- **R Client:** https://github.com/ropensci/rredlist
- **Python Client:** https://pypi.org/project/IUCN-API/
- **Sign up for API token:** https://api.iucnredlist.org/users/sign_up
