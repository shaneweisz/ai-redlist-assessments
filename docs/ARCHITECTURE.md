# IUCN Red List Assessment Pipeline - Agentic Architecture

## Overview

This document describes the multi-agent architecture for automating IUCN Red List assessments using Claude Code's subagents and skills system.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                        │
│              (Main coordinator & validator)                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬─────────────────┐
        │               │               │                 │
        ▼               ▼               ▼                 ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   PHASE 1    │ │   PHASE 2    │ │   PHASE 3    │ │   PHASE 4    │
│ Data         │ │  Analysis    │ │  Synthesis   │ │  Validation  │
│ Collection   │ │  & Metrics   │ │  & Draft     │ │  & Export    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

## Agent Roles & Responsibilities

### 1. **Orchestrator Agent** (Main Thread)
- **Purpose:** Coordinate all subagents and manage workflow
- **Responsibilities:**
  - Accept species name as input
  - Dispatch tasks to specialized subagents
  - Aggregate results from all phases
  - Perform final validation
  - Generate output in SIS-compatible format
- **Tools:** All tools (coordinates other agents)

### 2. **Taxonomy Agent** (Subagent)
- **Purpose:** Resolve and validate taxonomic information
- **Responsibilities:**
  - Verify scientific name
  - Get taxonomic hierarchy (kingdom → species)
  - Find synonyms and common names
  - Identify taxonomic authority
- **Data Sources:**
  - GBIF Backbone Taxonomy API
  - Catalogue of Life
  - ITIS (Integrated Taxonomic Information System)
- **Tools:** WebFetch, WebSearch, Bash (API calls)
- **Output:** Taxonomic data JSON

### 3. **Occurrence Agent** (Subagent)
- **Purpose:** Collect species occurrence and distribution data
- **Responsibilities:**
  - Fetch occurrence records from GBIF
  - Get country/region distribution
  - Identify biogeographical realms
  - Determine habitat systems (marine/terrestrial/freshwater)
- **Data Sources:**
  - GBIF API
  - iNaturalist API
  - Ocean Biodiversity Information System (OBIS)
- **Tools:** WebFetch, Bash (API calls), Write (save data)
- **Output:** Occurrence records JSON, country list

### 4. **Geographic Analysis Agent** (Subagent)
- **Purpose:** Calculate geographic range metrics
- **Responsibilities:**
  - Calculate Extent of Occurrence (EOO)
  - Calculate Area of Occupancy (AOO)
  - Determine elevation ranges
  - Create distribution map data
  - Assess geographic range criteria (Criterion B)
- **Data Sources:**
  - Occurrence data from Occurrence Agent
  - Elevation data (if available)
- **Tools:** Bash (Python/R scripts), Write (save calculations)
- **Output:** EOO, AOO, range metrics, Criterion B assessment

### 5. **Literature Mining Agent** (Subagent)
- **Purpose:** Extract information from scientific literature
- **Responsibilities:**
  - Search for relevant publications
  - Extract population estimates and trends
  - Identify reported threats
  - Find habitat descriptions
  - Gather conservation action information
- **Data Sources:**
  - Google Scholar
  - Crossref
  - PubMed (for relevant taxa)
  - Biodiversity Heritage Library
- **Tools:** WebSearch, WebFetch, Write (save extracted data)
- **Output:** Literature summary JSON with citations

### 6. **Population Analysis Agent** (Subagent)
- **Purpose:** Analyze population data and trends
- **Responsibilities:**
  - Compile population estimates
  - Analyze population trends (time series)
  - Calculate population reduction percentages
  - Assess Criterion A (population reduction)
  - Assess Criteria C & D (small populations)
  - Determine generation length
- **Data Sources:**
  - Literature mining results
  - Historical IUCN assessments
  - Population monitoring databases
- **Tools:** Bash (statistical analysis), Write
- **Output:** Population metrics, Criteria A/C/D assessment

### 7. **Habitat Classification Agent** (Subagent)
- **Purpose:** Classify species habitats using IUCN scheme
- **Responsibilities:**
  - Extract habitat descriptions from literature
  - Map to IUCN habitat classification codes
  - Determine habitat suitability
  - Identify seasonality (breeding vs non-breeding)
  - Assess habitat importance
- **Data Sources:**
  - Literature mining results
  - Field guides and species accounts
- **Tools:** WebSearch, Write
- **Output:** Habitat classification JSON with codes

### 8. **Threat Assessment Agent** (Subagent)
- **Purpose:** Identify and classify threats
- **Responsibilities:**
  - Extract threats from literature
  - Classify using IUCN threat taxonomy (codes 1.x - 11.x)
  - Score threat severity (high/medium/low)
  - Assess threat timing (ongoing/past/future)
  - Determine threat scope (majority/minority/whole)
  - Calculate threat impact scores
- **Data Sources:**
  - Literature mining results
  - Conservation reports
- **Tools:** WebSearch, Write
- **Output:** Threats JSON with classifications and scores

### 9. **Conservation Actions Agent** (Subagent)
- **Purpose:** Document conservation measures
- **Responsibilities:**
  - Identify existing conservation actions
  - Classify using IUCN action taxonomy
  - Determine action status (on-going/needed)
  - Identify research needs
  - Check protected area coverage
- **Data Sources:**
  - Literature mining results
  - Protected Planet database
  - IUCN Conservation Actions classification
- **Tools:** WebSearch, WebFetch, Write
- **Output:** Conservation actions JSON

### 10. **Criteria Evaluation Agent** (Subagent)
- **Purpose:** Synthesize all data and evaluate IUCN criteria
- **Responsibilities:**
  - Review all calculated metrics
  - Determine which criteria (A-E) are met
  - Assign preliminary Red List category
  - Identify sub-criteria (e.g., A2abc, B1ab(i,ii,iii))
  - Flag uncertainties and data gaps
  - Provide confidence scores
- **Inputs:** All outputs from previous agents
- **Tools:** Read (agent outputs), Write
- **Output:** Criteria assessment with category recommendation

### 11. **Rationale Generation Agent** (Subagent)
- **Purpose:** Generate assessment documentation text
- **Responsibilities:**
  - Write rationale for category assignment
  - Generate geographic range description
  - Write population description
  - Write habitat & ecology text
  - Write threats narrative
  - Write conservation actions narrative
  - Ensure all text follows IUCN guidelines
  - Include proper citations
- **Inputs:** All outputs from previous agents
- **Tools:** Read (agent outputs), Write
- **Output:** Documentation texts for all required fields

### 12. **Validation Agent** (Subagent)
- **Purpose:** Quality assurance and completeness check
- **Responsibilities:**
  - Verify all required fields are present
  - Check data consistency across sections
  - Validate geographic calculations
  - Verify citations are properly formatted
  - Check criteria application logic
  - Flag potential issues for expert review
  - Generate confidence scores by section
- **Inputs:** Complete draft assessment
- **Tools:** Read, Write
- **Output:** Validation report + final assessment JSON

## Data Flow

```
Input: Species Name (e.g., "Panthera leo")
  │
  ├─→ Taxonomy Agent ────────────→ taxonomic_data.json
  │
  ├─→ Occurrence Agent ──────────→ occurrence_data.json
  │       │
  │       └─→ Geographic Agent ──→ range_metrics.json
  │
  ├─→ Literature Agent ──────────→ literature_summary.json
  │       │
  │       ├─→ Population Agent ──→ population_analysis.json
  │       │
  │       ├─→ Habitat Agent ─────→ habitat_classification.json
  │       │
  │       ├─→ Threat Agent ──────→ threat_assessment.json
  │       │
  │       └─→ Conservation Agent ─→ conservation_actions.json
  │
  ├─→ Criteria Agent ────────────→ criteria_evaluation.json
  │       (uses all above data)
  │
  ├─→ Rationale Agent ───────────→ documentation_texts.json
  │       (uses all above data)
  │
  └─→ Validation Agent ──────────→ final_assessment.json
          (checks everything)            + validation_report.json

Output: Complete IUCN Red List Assessment
```

## Implementation Structure

```
accelerate-redlist-assessments/
├── .claude/
│   ├── agents/              # Subagent definitions
│   │   ├── taxonomy.md
│   │   ├── occurrence.md
│   │   ├── geographic.md
│   │   ├── literature.md
│   │   ├── population.md
│   │   ├── habitat.md
│   │   ├── threat.md
│   │   ├── conservation.md
│   │   ├── criteria.md
│   │   ├── rationale.md
│   │   └── validation.md
│   ├── commands/            # Slash commands
│   │   ├── assess.md        # Main pipeline command
│   │   └── validate.md      # Validation only
│   └── settings.local.json
├── src/
│   ├── orchestrator.py      # Main orchestration script
│   ├── utils/
│   │   ├── api_clients.py   # API wrapper functions
│   │   ├── geographic.py    # EOO/AOO calculations
│   │   ├── criteria.py      # Criteria evaluation logic
│   │   └── formatters.py    # Output formatting
│   └── config/
│       ├── api_keys.env     # API credentials
│       └── iucn_schemas.json # IUCN data schemas
├── data/
│   ├── panthera_leo/        # Example species directory
│   │   ├── 01_taxonomic_data.json
│   │   ├── 02_occurrence_data.json
│   │   ├── 03_range_metrics.json
│   │   ├── 04_literature_summary.json
│   │   ├── 05_population_analysis.json
│   │   ├── 06_habitat_classification.json
│   │   ├── 07_threat_assessment.json
│   │   ├── 08_conservation_actions.json
│   │   ├── 09_criteria_evaluation.json
│   │   ├── 10_documentation_texts.json
│   │   ├── 11_validation_report.json
│   │   └── final_assessment.json
│   └── templates/           # Output templates
│       └── sis_format.json
├── scripts/
│   ├── setup_apis.sh        # API key setup
│   ├── install_deps.sh      # Install dependencies
│   └── test_pipeline.sh     # Test full pipeline
├── tests/
│   ├── test_panthera_leo.py # Validate against known assessment
│   └── test_agents.py       # Unit tests for agent outputs
├── docs/
│   ├── ARCHITECTURE.md      # This file
│   ├── AGENT_SPECS.md       # Detailed agent specifications
│   └── API_REFERENCE.md     # API documentation
├── README.md
├── SAMPLE_ASSESSMENT_DATA.md
└── example_assessment.json
```

## Execution Flow

### Phase 1: Data Collection (Parallel Execution)
```python
# Can run in parallel - no dependencies
parallel_results = await asyncio.gather(
    invoke_agent("taxonomy", species_name),
    invoke_agent("occurrence", species_name),
    invoke_agent("literature", species_name)
)
```

### Phase 2: Analysis (Sequential/Parallel Mixed)
```python
# Geographic depends on occurrence
geographic_results = await invoke_agent("geographic", occurrence_data)

# These can run in parallel after literature mining
parallel_analysis = await asyncio.gather(
    invoke_agent("population", literature_data),
    invoke_agent("habitat", literature_data),
    invoke_agent("threat", literature_data),
    invoke_agent("conservation", literature_data)
)
```

### Phase 3: Synthesis (Sequential)
```python
# Criteria evaluation needs all previous results
criteria_results = await invoke_agent("criteria", all_data)

# Rationale generation needs criteria results
documentation = await invoke_agent("rationale", all_data + criteria_results)
```

### Phase 4: Validation (Sequential)
```python
# Final validation
final_assessment = await invoke_agent("validation", complete_draft)
```

## Key Technologies

### APIs & Data Sources
- **GBIF API** - Occurrence data (https://api.gbif.org/v1/)
- **Catalogue of Life** - Taxonomy (https://api.catalogueoflife.org/)
- **Crossref** - Literature metadata (https://api.crossref.org/)
- **IUCN Red List API** - Historical assessments (https://apiv3.iucnredlist.org/)

### Tools & Libraries
- **Python 3.10+** - Main language
- **GeoPandas** - Geographic calculations (EOO/AOO)
- **Pandas** - Data manipulation
- **Requests** - API calls
- **Beautiful Soup** - Web scraping (if needed)
- **Claude API** - LLM operations (via subagents)

### Geographic Calculations
- **ConR R package** - EOO/AOO calculations (IUCN-compliant)
- **Python geospatial libraries** - Alternative implementation

## Agent Communication Protocol

### Input Format (to subagent)
```json
{
  "task": "taxonomy_resolution",
  "species_name": "Panthera leo",
  "context": {
    "assessment_id": "panthera_leo_2024",
    "timestamp": "2025-10-20T12:00:00Z"
  },
  "config": {
    "data_sources": ["gbif", "col", "itis"],
    "confidence_threshold": 0.8
  }
}
```

### Output Format (from subagent)
```json
{
  "status": "success",
  "agent": "taxonomy",
  "species_name": "Panthera leo",
  "confidence": 0.95,
  "data": {
    // Agent-specific data structure
  },
  "metadata": {
    "execution_time": "2.3s",
    "sources": ["gbif", "col"],
    "timestamp": "2025-10-20T12:00:02Z"
  },
  "warnings": [],
  "errors": []
}
```

## Error Handling & Resilience

### Retry Strategy
- API failures: 3 retries with exponential backoff
- Data validation failures: Flag for manual review
- Missing data: Continue with warnings, flag in validation

### Confidence Scoring
Each agent provides confidence scores:
- **High (>0.8)**: Data from authoritative sources, good coverage
- **Medium (0.5-0.8)**: Limited data, some uncertainties
- **Low (<0.5)**: Insufficient data, requires expert input

### Fallback Mechanisms
1. If GBIF API fails → try iNaturalist
2. If automated literature mining fails → suggest manual literature review
3. If EOO/AOO calculation fails → flag for manual calculation

## Quality Assurance

### Validation Checks
- ✓ All required fields present
- ✓ Taxonomic name valid in major databases
- ✓ EOO > AOO (geographic logic)
- ✓ Criteria thresholds correctly applied
- ✓ Threat codes valid
- ✓ Habitat codes valid
- ✓ Citations properly formatted
- ✓ No contradictions across sections

### Comparison with Existing Assessment
For Panthera leo, compare:
- Category assigned (should match VU)
- Criteria used (should match A2abcd)
- Population trend (should match Decreasing)
- Key threats identified
- Geographic range estimates

### Expert Review Interface
Generate summary for expert review:
```markdown
# Assessment Review: Panthera leo

## Confidence Summary
- Taxonomy: HIGH (0.98)
- Distribution: MEDIUM (0.72)
- Population: MEDIUM (0.65)
- Threats: HIGH (0.85)
- Category: MEDIUM (0.70)

## Recommended Category: VU (Vulnerable)
## Criteria Met: A2abcd

## Requires Expert Review:
⚠️ Population reduction estimate: 30-50% (threshold boundary)
⚠️ Limited recent population data for some regions
✓ All other fields have high confidence
```

## Performance Targets

- **Total Pipeline Time**: 5-10 minutes per species
- **Data Collection Phase**: 2-3 minutes
- **Analysis Phase**: 2-3 minutes
- **Synthesis Phase**: 1-2 minutes
- **Validation Phase**: 30 seconds

## Future Enhancements

### Version 2.0
- Real-time monitoring integration
- Automated reassessment triggers
- Multi-species batch processing
- Integration with SIS API (when available)

### Version 3.0
- Interactive expert review interface
- Machine learning for criteria prediction
- Automated map generation
- Integration with conservation databases

## Usage

### Command-line Interface
```bash
# Run full pipeline for a species
python src/orchestrator.py --species "Panthera leo" --output data/panthera_leo/

# Run with specific agents only
python src/orchestrator.py --species "Panthera leo" --agents taxonomy,occurrence,geographic

# Validate existing assessment
python src/orchestrator.py --validate data/panthera_leo/final_assessment.json
```

### Slash Command
```
/assess Panthera leo
```

This will trigger the orchestrator to run the full pipeline.

## Success Criteria

### For Panthera leo Replication
✅ Matches official category (VU)
✅ Matches official criteria (A2abcd)
✅ Population trend matches (Decreasing)
✅ Key threats identified match
✅ Geographic range within ±20% of official
✅ All required fields populated
✅ Documentation quality comparable to official

### For Pipeline Generalization
✅ Can process any terrestrial mammal
✅ Generates complete draft in <10 minutes
✅ Validation report identifies gaps
✅ Expert review time reduced by >50%
✅ Output compatible with SIS format

---

**Next Steps:** Implement subagent definitions in `.claude/agents/`
