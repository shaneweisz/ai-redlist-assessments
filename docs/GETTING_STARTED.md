# Getting Started with the IUCN Red List Assessment Pipeline

This guide will help you set up and run the automated assessment pipeline.

## Prerequisites

- **Python 3.10+** installed
- **Claude Code** CLI tool
- **IUCN Red List API token** (free registration)
- Internet connection (for API calls)

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd accelerate-redlist-assessments
```

### Step 2: Run Setup Script

```bash
./scripts/setup.sh
```

This will:
- Create a Python virtual environment
- Install required dependencies (GeoPandas, Shapely, etc.)
- Create directory structure
- Generate API keys template

### Step 3: Configure API Keys

1. Sign up for an IUCN Red List API token: https://api.iucnredlist.org/users/sign_up

2. Add your token to `src/config/api_keys.env`:
   ```bash
   IUCN_API_KEY=your_actual_key_here
   ```

### Step 4: Activate Virtual Environment

```bash
source venv/bin/activate
```

## Running an Assessment

### Using the Slash Command (Recommended)

In Claude Code, simply type:

```
/assess Panthera leo
```

This will:
1. Launch the Taxonomy Agent to resolve species information
2. Launch the Occurrence Agent to collect distribution data
3. Launch the Geographic Agent to calculate EOO/AOO
4. Generate output files in `data/panthera_leo/`

### What Gets Generated

After running the pipeline, you'll find these files:

```
data/panthera_leo/
├── 01_taxonomic_data.json      # Scientific name, hierarchy, common names
├── 02_occurrence_data.json     # Distribution records from GBIF
└── 03_range_metrics.json       # EOO, AOO, Criterion B assessment
```

### Manual Script Execution

You can also run individual components:

```bash
# Calculate EOO/AOO from existing occurrence data
python scripts/calculate_eoo_aoo.py panthera_leo
```

## Understanding the Output

### Taxonomic Data (`01_taxonomic_data.json`)

```json
{
  "data": {
    "scientific_name": "Panthera leo",
    "kingdom": "ANIMALIA",
    "class": "MAMMALIA",
    "order": "CARNIVORA",
    "family": "FELIDAE",
    "common_names": [
      {"language": "eng", "name": "Lion"}
    ]
  },
  "confidence": 0.95
}
```

### Occurrence Data (`02_occurrence_data.json`)

```json
{
  "data": {
    "total_records": 8542,
    "countries": [
      {"code": "ZA", "country": "South Africa"},
      {"code": "TZ", "country": "Tanzania"}
    ],
    "occurrence_points": [
      {"lat": -24.5, "lon": 31.5, "year": 2023}
    ]
  },
  "confidence": 0.85
}
```

### Range Metrics (`03_range_metrics.json`)

```json
{
  "data": {
    "eoo_km2": 5845300,
    "aoo_km2": 1842,
    "criterion_b": {
      "b1_met": false,
      "b2_met": false
    }
  },
  "confidence": 0.88
}
```

## Interpreting Results

### Extent of Occurrence (EOO)

The EOO is the area of a minimum convex polygon drawn around all occurrence points.

**Thresholds:**
- CR: <100 km²
- EN: <5,000 km²
- VU: <20,000 km²

### Area of Occupancy (AOO)

The AOO is calculated using a 2×2 km grid, counting occupied cells.

**Thresholds:**
- CR: <10 km²
- EN: <500 km²
- VU: <2,000 km²

### Criterion B Assessment

If either EOO or AOO meets a threshold, Criterion B is met for that category. Additional sub-criteria (fragmentation, continuing decline) must also be met for final category assignment.

## Example: Panthera leo (Lion)

Running `/assess Panthera leo` should produce results similar to:

```
✓ Taxonomy resolved: Panthera leo (Linnaeus, 1758)
✓ Occurrence data: 8,542 records from 15 countries
✓ EOO calculated: 5,845,300 km²
✓ AOO calculated: 1,842 km²
⚠️ Criterion B: Not met (range too large)

Files saved to: data/panthera_leo/
```

**Expected Category:** VU (Vulnerable)
**Expected Criteria:** A2abcd (Population reduction, not geographic range)

Note: Our pipeline currently only implements Criterion B (geographic range). The official assessment uses Criterion A (population reduction), which requires population trend analysis (Phase 3 of pipeline, not yet implemented).

## Current Limitations

### ✅ Implemented (Phases 1-2)
- Taxonomic resolution
- Occurrence data collection
- Geographic calculations (EOO/AOO)
- Criterion B assessment

### ⏳ To Be Implemented (Phases 3-5)
- Literature mining
- Population trend analysis
- Habitat classification
- Threat assessment
- Conservation actions documentation
- Criteria A, C, D, E evaluation
- Rationale text generation
- Final validation

## Troubleshooting

### "IUCN API key not found"

Make sure you've:
1. Registered for an API key at https://api.iucnredlist.org/users/sign_up
2. Added the key to `src/config/api_keys.env`
3. Activated the virtual environment: `source venv/bin/activate`

### "No occurrence data found"

Some species may have limited data in GBIF. Try:
- Checking the scientific name spelling
- Verifying the species exists in GBIF: https://www.gbif.org/
- Using an alternative data source (manual collection)

### "EOO calculation failed"

This can happen if:
- Less than 3 occurrence points available (need minimum 3 for polygon)
- All points are collinear
- Coordinate data is invalid

### Geographic calculation errors

Make sure GeoPandas is properly installed:

```bash
pip install geopandas shapely pyproj
```

On macOS with Apple Silicon, you may need:

```bash
brew install gdal
pip install --no-binary :all: geopandas
```

## Next Steps

### For Development

1. **Implement remaining agents** in `.claude/agents/`:
   - `literature.md` - Literature mining
   - `population.md` - Population analysis
   - `habitat.md` - Habitat classification
   - `threat.md` - Threat assessment
   - `conservation.md` - Conservation actions
   - `criteria.md` - Complete criteria evaluation
   - `rationale.md` - Text generation
   - `validation.md` - Quality assurance

2. **Test with multiple species**:
   ```
   /assess Panthera tigris
   /assess Loxodonta africana
   /assess Gorilla gorilla
   ```

3. **Compare outputs with official assessments**:
   - Download official assessment from IUCN Red List
   - Compare EOO, AOO, countries, threats
   - Calculate accuracy metrics

### For Research

1. **Evaluate automation quality**:
   - Precision/recall for habitat classification
   - Accuracy of EOO/AOO calculations
   - Category prediction accuracy

2. **Identify bottlenecks**:
   - Which phases take longest?
   - Which require most expert input?
   - Where do errors occur?

3. **Explore improvements**:
   - Better occurrence data sources
   - ML models for threat classification
   - LLM prompting strategies for rationale generation

## Resources

### Documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Complete system architecture
- [SAMPLE_ASSESSMENT_DATA.md](SAMPLE_ASSESSMENT_DATA.md) - Data structure reference
- [README.md](README.md) - Project overview

### IUCN Resources
- **Red List Website**: https://www.iucnredlist.org
- **API Docs**: https://api.iucnredlist.org/api-docs
- **Guidelines (PDF)**: https://www.iucnredlist.org/resources/redlistguidelines
- **Categories & Criteria**: https://www.iucnredlist.org/resources/categories-and-criteria

### Data Sources
- **GBIF**: https://www.gbif.org - Occurrence data
- **iNaturalist**: https://www.inaturalist.org - Recent observations
- **Catalogue of Life**: https://www.catalogueoflife.org - Taxonomy

### Community
- **GitHub Issues**: Report bugs and feature requests
- **IUCN Red List Team**: redlist@iucn.org for questions about assessments
- **Conservation Biology Community**: For methodological questions

## Contributing

Contributions are welcome! Priority areas:

1. **Agent implementation** - Complete phases 3-5
2. **Data source integration** - Add more APIs
3. **Validation tools** - Compare with official assessments
4. **Documentation** - Improve guides and examples
5. **Testing** - Add unit tests for agents

## Citation

If you use this pipeline in research, please cite:

```
[Add citation information once published]
```

---

**Questions?** Open an issue or contact the maintainers.
