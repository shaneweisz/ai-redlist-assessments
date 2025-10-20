# Accelerate Red List Assessments

This repository explores the process of contributing IUCN Red List assessments and investigates opportunities for AI-assisted automation.

## Contents

1. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Multi-agent pipeline architecture and design
2. **[SAMPLE_ASSESSMENT_DATA.md](SAMPLE_ASSESSMENT_DATA.md)** - Comprehensive guide to IUCN Red List assessment data structures
3. **[example_assessment.json](example_assessment.json)** - Complete example assessment for Atlantic Puffin (*Fratercula arctica*)

## Quick Start

```bash
# 1. Run setup
./scripts/setup.sh

# 2. Add your IUCN API key to src/config/api_keys.env

# 3. Run assessment pipeline
/assess Panthera leo
```

## Overview

The IUCN Red List of Threatened Species is the world's most comprehensive information source on the global conservation status of species. However, maintaining current assessments for all species is a significant challenge:

- **160,000+ species** still need assessment
- **25% of existing assessments** are out of date
- **Manual assessment process** is time-consuming and resource-intensive
- **Expert knowledge required** for quality assessments

## Assessment Process Summary

### Categories (9 levels)
- **EX** - Extinct
- **EW** - Extinct in the Wild
- **CR** - Critically Endangered
- **EN** - Endangered
- **VU** - Vulnerable
- **NT** - Near Threatened
- **LC** - Least Concern
- **DD** - Data Deficient
- **NE** - Not Evaluated

### Five Assessment Criteria (A-E)

| Criterion | Measures | CR Threshold | EN Threshold | VU Threshold |
|-----------|----------|--------------|--------------|--------------|
| **A** | Population reduction | ≥80% | ≥50% | ≥30% |
| **B** | Geographic range | <100 km² (EOO) or <10 km² (AOO) | <5,000 km² (EOO) or <500 km² (AOO) | <20,000 km² (EOO) or <2,000 km² (AOO) |
| **C** | Small population + decline | <250 mature | <2,500 mature | <10,000 mature |
| **D** | Very small population | <50 mature | <250 mature | <1,000 mature or restricted |
| **E** | Quantitative analysis | ≥50% extinction risk in 10 years | ≥20% in 20 years | ≥10% in 100 years |

**Key:** Meeting ANY ONE criterion qualifies a species for that category.

### Required Components

Every assessment must include:

1. **Taxonomy** - Scientific name, authority, common names
2. **Category & Criteria** - Assigned category with justification
3. **Rationale** - Text explaining why the category was assigned
4. **Geographic Range** - Distribution, EOO, AOO
5. **Population** - Size, trend, structure
6. **Habitat & Ecology** - Habitat types, ecological requirements
7. **Threats** - Current and future threats with severity
8. **Conservation Actions** - Existing and needed measures
9. **Distribution Map** - Geographic representation
10. **Bibliography** - Supporting references

## Submission Process

1. **Obtain Access** - Contact IUCN Red List Unit or join SSC Specialist Group
2. **Prepare Assessment** - Use Species Information Service (SIS) platform
3. **Submit to Queue** - Assessment enters review queue
4. **Quality Check** - IUCN Red List Unit validates data
5. **Peer Review** - Relevant experts review assessment
6. **Publication** - If approved, published to IUCN Red List

## Agentic Pipeline Architecture

This project implements a **multi-agent workflow** using Claude Code's subagent system to automate IUCN Red List assessments.

### Pipeline Phases

1. **Phase 1: Data Collection** (Parallel)
   - Taxonomy Agent - Resolves scientific names and taxonomic hierarchy
   - Occurrence Agent - Collects distribution data from GBIF/iNaturalist

2. **Phase 2: Geographic Analysis** (Sequential)
   - Geographic Agent - Calculates EOO, AOO, and Criterion B assessment

3. **Phase 3: Literature Mining & Analysis** (Mixed)
   - Literature Agent - Mines scientific literature
   - Population, Habitat, Threat, Conservation Agents (parallel)

4. **Phase 4: Synthesis** (Sequential)
   - Criteria Agent - Evaluates all IUCN criteria
   - Rationale Agent - Generates assessment text

5. **Phase 5: Validation** (Sequential)
   - Validation Agent - Quality checks and final report

**Current Status:** ✅ Phases 1-2 implemented and functional

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete details on the agentic system design.

## AI Automation Potential

### High Automation Potential ✅

| Task | Approach | Confidence |
|------|----------|------------|
| Taxonomy extraction | Database lookup, literature mining | High |
| Occurrence data | GBIF, iNaturalist APIs | High |
| EOO/AOO calculation | Geographic algorithms | High |
| Habitat classification | Text mining, ML classification | Medium-High |
| Population trend extraction | Time series analysis, NLP | Medium |
| Threat identification | Text mining, classification | Medium |
| Draft rationale generation | Large Language Models | Medium |

### Challenging to Automate ⚠️

| Task | Challenge | Confidence |
|------|-----------|------------|
| Criteria application | Requires expert judgment on edge cases | Low-Medium |
| Data quality assessment | Understanding reliability and biases | Low |
| Conservation prioritization | Balancing multiple factors | Low |
| Final category decision | Legal/conservation implications | Low |
| Expert validation | Requires domain expertise | Human-only |

### Existing Tools & Research

- **sRedList** (2023) - R package for compiling assessments, SIS-compatible outputs
- **ML prediction models** - Identify species needing urgent reassessment
- **"Rapid Least Concern"** - Automated assessments for low-risk species
- **rredlist** - R client for IUCN Red List API
- **Various Python/Node.js clients** - Programmatic API access

## Proposed AI-Assisted Workflow

### Phase 1: Data Collection
```
Input: Species name
  ↓
[GBIF API] → Occurrence records
[Literature Mining] → Population data, threats
[Taxonomic Databases] → Classification, synonyms
[Climate/Land Use Data] → Environmental context
```

### Phase 2: Preliminary Analysis
```
Occurrence Data → Calculate EOO/AOO
Population Data → Analyze trends
Literature Text → Extract threats, habitats
Historical Assessments → Identify changes
```

### Phase 3: Draft Generation
```
Calculated Metrics → Suggest criteria met
Evidence Synthesis → Generate draft rationale
Threat Analysis → Classify and score threats
Conservation Info → Draft action needs
  ↓
Complete Draft Assessment
```

### Phase 4: Expert Review
```
Draft Assessment
  ↓
Expert Reviewer → Validate calculations
              → Refine category assignment
              → Add expert knowledge
              → Approve rationale
  ↓
Final Assessment → Submit via SIS
```

### Key Principles

1. **AI as Assistant, Not Replacement** - Experts make final decisions
2. **Transparency** - Clear provenance for all AI-generated content
3. **Conservative Approach** - Flag uncertainties for review
4. **Quality over Speed** - Maintain assessment standards
5. **Start with Low-Risk** - Begin with Least Concern species
6. **Continuous Learning** - Improve models with feedback

## Data Sources

### Species Occurrence
- **GBIF** (Global Biodiversity Information Facility) - gbif.org
- **iNaturalist** - inaturalist.org
- **eBird** (birds) - ebird.org
- **Ocean Biodiversity Information System** - obis.org

### Scientific Literature
- **Crossref** - crossref.org
- **PubMed** - ncbi.nlm.nih.gov/pubmed
- **Google Scholar** - scholar.google.com
- **Biodiversity Heritage Library** - biodiversitylibrary.org

### Taxonomic Information
- **Catalogue of Life** - catalogueoflife.org
- **WoRMS** (marine species) - marinespecies.org
- **ITIS** - itis.gov
- **GBIF Backbone Taxonomy** - gbif.org/dataset/d7dddbf4-2cf0-4f39-9b2a-bb099caae36c

### Environmental Data
- **WorldClim** - worldclim.org
- **CHELSA** - chelsa-climate.org
- **Copernicus Land Monitoring** - land.copernicus.eu
- **Protected Planet** (protected areas) - protectedplanet.net

## Getting Started with IUCN Red List API

### 1. Get API Token
Sign up at: https://api.iucnredlist.org/users/sign_up

### 2. Example API Call
```bash
curl "https://apiv3.iucnredlist.org/api/v3/species/Fratercula%20arctica?token=YOUR_TOKEN"
```

### 3. Python Example
```python
import requests

API_TOKEN = "your_token_here"
BASE_URL = "https://apiv3.iucnredlist.org/api/v3"

def get_species_info(species_name):
    url = f"{BASE_URL}/species/{species_name}"
    params = {"token": API_TOKEN}
    response = requests.get(url, params=params)
    return response.json()

# Get Atlantic Puffin assessment
puffin = get_species_info("Fratercula arctica")
print(puffin)
```

### 4. R Example
```r
library(rredlist)

# Set API key
rl_use_iucn()  # Follow prompts to set API key

# Get species assessment
puffin <- rl_search("Fratercula arctica")
print(puffin)

# Get narrative information
narrative <- rl_narrative("Fratercula arctica")
print(narrative)

# Get threats
threats <- rl_threats("Fratercula arctica")
print(threats)
```

## Next Steps for AI Development

### Immediate (Research Phase)
1. ✅ Understand assessment structure and requirements
2. ⬜ Analyze existing assessments for patterns
3. ⬜ Identify common data sources and extraction methods
4. ⬜ Prototype text extraction from literature
5. ⬜ Experiment with LLM-generated rationales

### Short-term (Prototype Phase)
1. ⬜ Build occurrence data fetcher (GBIF integration)
2. ⬜ Implement EOO/AOO calculator
3. ⬜ Develop threat classifier
4. ⬜ Create draft rationale generator
5. ⬜ Build expert review interface

### Medium-term (Pilot Phase)
1. ⬜ Test on Least Concern species
2. ⬜ Validate with expert assessors
3. ⬜ Measure time savings
4. ⬜ Assess accuracy vs manual assessments
5. ⬜ Refine based on feedback

### Long-term (Scale Phase)
1. ⬜ Expand to Data Deficient species
2. ⬜ Support reassessment of outdated assessments
3. ⬜ Integrate with SIS platform
4. ⬜ Develop continuous monitoring system
5. ⬜ Collaborate with IUCN for adoption

## Resources

### Official IUCN Resources
- **Red List Homepage:** https://www.iucnredlist.org
- **API Documentation:** https://api.iucnredlist.org/api-docs
- **Categories & Criteria (v3.1):** https://www.iucnredlist.org/resources/categories-and-criteria
- **Guidelines (v16, 2024):** https://www.iucnredlist.org/resources/redlistguidelines
- **SIS Platform:** https://www.iucnredlist.org/assessment/sis

### Research Papers
- **Accelerating assessments with sRedList** (2024): https://www.sciencedirect.com/science/article/pii/S0006320724003239
- **Rapid Least Concern automation** (2020): https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6992691/
- **Using AI to update Red List** (2024): https://www.rewild.org/blog/how-AI-can-help-update-IUCN-Red-List

### Development Tools
- **rredlist** (R): https://github.com/ropensci/rredlist
- **IUCN-API** (Python): https://pypi.org/project/IUCN-API/
- **IUCN-Red-List** (Node.js): https://github.com/AJFunk/IUCN-Red-List

### Training
- **IUCN Red List Assessor Training:** https://www.conservationtraining.org/course/index.php?categoryid=23

## Contributing

This is a research project exploring AI automation opportunities for IUCN Red List assessments. Contributions, ideas, and collaborations are welcome!

## Contact & Support

For questions about IUCN Red List assessments:
- Email: redlist@iucn.org
- Twitter: @IUCNRedList

## License

This repository is for educational and research purposes. IUCN Red List data is subject to IUCN's terms of use: https://www.iucnredlist.org/terms/terms-of-use

---

**Note:** This project is exploratory and not officially affiliated with IUCN. Any AI-assisted assessments would require proper validation by qualified experts before submission to the IUCN Red List.
