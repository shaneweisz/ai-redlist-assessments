# Project Structure

```
accelerate-redlist-assessments/
│
├── 📋 Documentation
│   ├── README.md                    # Project overview and quick start
│   ├── ARCHITECTURE.md              # Complete agentic system design
│   ├── GETTING_STARTED.md           # Detailed setup and usage guide
│   ├── PROJECT_SUMMARY.md           # Current status and roadmap
│   ├── SAMPLE_ASSESSMENT_DATA.md    # IUCN data structure reference
│   └── STRUCTURE.md                 # This file
│
├── 📦 Example Data
│   └── example_assessment.json      # Atlantic Puffin reference assessment
│
├── 🤖 Agentic System (.claude/)
│   ├── agents/                      # Specialized subagent definitions
│   │   ├── taxonomy.md              # ✅ Resolves scientific names
│   │   ├── occurrence.md            # ✅ Collects distribution data
│   │   ├── geographic.md            # ✅ Calculates EOO/AOO
│   │   ├── literature.md            # ⏳ TO BE IMPLEMENTED
│   │   ├── population.md            # ⏳ TO BE IMPLEMENTED
│   │   ├── habitat.md               # ⏳ TO BE IMPLEMENTED
│   │   ├── threat.md                # ⏳ TO BE IMPLEMENTED
│   │   ├── conservation.md          # ⏳ TO BE IMPLEMENTED
│   │   ├── criteria.md              # ⏳ TO BE IMPLEMENTED
│   │   ├── rationale.md             # ⏳ TO BE IMPLEMENTED
│   │   └── validation.md            # ⏳ TO BE IMPLEMENTED
│   │
│   ├── commands/                    # Slash commands
│   │   └── assess.md                # ✅ Main pipeline orchestrator
│   │
│   └── settings.local.json          # Claude Code configuration
│
├── 🐍 Python Environment
│   ├── requirements.txt             # Python dependencies
│   └── venv/                        # Virtual environment (created by setup.sh)
│
├── 📊 Data Directory (data/)
│   ├── panthera_leo/                # Example: Lion assessment
│   │   ├── 01_taxonomic_data.json
│   │   ├── 02_occurrence_data.json
│   │   └── 03_range_metrics.json
│   │
│   ├── {species_name}/              # Generated per species
│   │   ├── 01_taxonomic_data.json
│   │   ├── 02_occurrence_data.json
│   │   ├── 03_range_metrics.json
│   │   ├── 04_literature_summary.json      # ⏳ Future
│   │   ├── 05_population_analysis.json     # ⏳ Future
│   │   ├── 06_habitat_classification.json  # ⏳ Future
│   │   ├── 07_threat_assessment.json       # ⏳ Future
│   │   ├── 08_conservation_actions.json    # ⏳ Future
│   │   ├── 09_criteria_evaluation.json     # ⏳ Future
│   │   ├── 10_documentation_texts.json     # ⏳ Future
│   │   ├── 11_validation_report.json       # ⏳ Future
│   │   └── final_assessment.json           # ⏳ Future
│   │
│   └── templates/                   # Output format templates
│       └── sis_format.json          # ⏳ TO BE CREATED
│
├── 🔧 Scripts (scripts/)
│   ├── setup.sh                     # ✅ Automated project setup
│   ├── calculate_eoo_aoo.py         # ✅ Geographic calculations
│   ├── test_pipeline.sh             # ⏳ TO BE CREATED
│   └── install_deps.sh              # ⏳ TO BE CREATED
│
├── 💻 Source Code (src/)
│   ├── orchestrator.py              # ⏳ TO BE CREATED (Python orchestrator)
│   ├── utils/                       # Utility functions
│   │   ├── api_clients.py           # ⏳ API wrappers (GBIF, IUCN, etc.)
│   │   ├── geographic.py            # ⏳ Geographic utilities
│   │   ├── criteria.py              # ⏳ Criteria evaluation logic
│   │   └── formatters.py            # ⏳ Output formatting
│   │
│   └── config/
│       ├── api_keys.env             # API credentials (created by setup)
│       └── iucn_schemas.json        # ⏳ IUCN data schemas
│
├── 🧪 Tests (tests/)
│   ├── test_panthera_leo.py         # ⏳ Validate against official assessment
│   └── test_agents.py               # ⏳ Unit tests for agent outputs
│
└── 📚 Documentation (docs/)
    └── [Additional documentation as needed]
```

## File Descriptions

### Core Documentation

| File | Purpose | Status |
|------|---------|--------|
| `README.md` | Project overview, quick start, key information | ✅ Complete |
| `ARCHITECTURE.md` | Detailed multi-agent system design, data flow | ✅ Complete |
| `GETTING_STARTED.md` | Step-by-step setup and usage instructions | ✅ Complete |
| `PROJECT_SUMMARY.md` | Current status, roadmap, success metrics | ✅ Complete |
| `SAMPLE_ASSESSMENT_DATA.md` | IUCN data structure and API reference | ✅ Complete |

### Agentic System

| Agent | Purpose | Input | Output | Status |
|-------|---------|-------|--------|--------|
| `taxonomy.md` | Validate scientific name, get hierarchy | Species name | `01_taxonomic_data.json` | ✅ Done |
| `occurrence.md` | Collect distribution data | Species name | `02_occurrence_data.json` | ✅ Done |
| `geographic.md` | Calculate EOO/AOO | Occurrence data | `03_range_metrics.json` | ✅ Done |
| `literature.md` | Mine scientific papers | Species name | `04_literature_summary.json` | ⏳ TODO |
| `population.md` | Analyze population trends | Literature data | `05_population_analysis.json` | ⏳ TODO |
| `habitat.md` | Classify habitats | Literature data | `06_habitat_classification.json` | ⏳ TODO |
| `threat.md` | Identify threats | Literature data | `07_threat_assessment.json` | ⏳ TODO |
| `conservation.md` | Document actions | Literature data | `08_conservation_actions.json` | ⏳ TODO |
| `criteria.md` | Evaluate all criteria | All previous data | `09_criteria_evaluation.json` | ⏳ TODO |
| `rationale.md` | Generate text | All previous data | `10_documentation_texts.json` | ⏳ TODO |
| `validation.md` | Quality checks | Complete draft | `11_validation_report.json` + `final_assessment.json` | ⏳ TODO |

### Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `setup.sh` | Install dependencies, create directories | ✅ Done |
| `calculate_eoo_aoo.py` | IUCN-compliant geographic calculations | ✅ Done |
| `test_pipeline.sh` | End-to-end testing | ⏳ TODO |

### Data Flow Per Species

```
Input: Species Name (e.g., "Panthera leo")
  ↓
[Taxonomy Agent] → 01_taxonomic_data.json
  ↓
[Occurrence Agent] → 02_occurrence_data.json
  ↓
[Geographic Agent] → 03_range_metrics.json
  ↓
[Literature Agent] → 04_literature_summary.json
  ↓
[4 Analysis Agents in parallel] → 05-08_*.json
  ↓
[Criteria Agent] → 09_criteria_evaluation.json
  ↓
[Rationale Agent] → 10_documentation_texts.json
  ↓
[Validation Agent] → 11_validation_report.json
                   → final_assessment.json
```

## Current Implementation Status

### ✅ Implemented (Functional)

**Phase 1: Data Collection**
- Taxonomy resolution via GBIF/IUCN APIs
- Occurrence data from GBIF/iNaturalist
- Country distribution identification
- Biogeographical realm assignment

**Phase 2: Geographic Analysis**
- EOO calculation (convex hull method)
- AOO calculation (2×2 km grid)
- Criterion B threshold evaluation
- Geographic validation checks

**Infrastructure**
- Subagent architecture
- Slash command orchestration
- Python environment setup
- File-based data flow

### ⏳ To Be Implemented

**Phase 3: Literature & Analysis**
- Literature mining from scientific databases
- Population trend analysis
- Habitat classification
- Threat identification and scoring
- Conservation action documentation

**Phase 4: Synthesis**
- Complete criteria evaluation (A-E)
- Red List category determination
- Rationale text generation
- Documentation compilation

**Phase 5: Validation**
- Quality assurance checks
- Confidence scoring
- SIS format export
- Expert review interface

## Usage Patterns

### Quick Assessment
```bash
# In Claude Code
/assess Panthera leo
```

### Manual Steps
```bash
# Setup
./scripts/setup.sh
source venv/bin/activate

# Individual components
python scripts/calculate_eoo_aoo.py panthera_leo

# View results
cat data/panthera_leo/03_range_metrics.json
```

### Batch Processing (Future)
```bash
# Process multiple species
/assess-batch species_list.txt
```

## Adding New Components

### To Add a New Agent

1. Create agent definition: `.claude/agents/your_agent.md`
2. Define input/output format
3. Specify data sources and APIs
4. Document workflow steps
5. Add to orchestrator in `assess.md`

### To Add a New Utility

1. Create script in `scripts/` or module in `src/utils/`
2. Add dependencies to `requirements.txt`
3. Document usage in `GETTING_STARTED.md`
4. Add tests in `tests/`

### To Add a New Data Source

1. Add API client to `src/utils/api_clients.py`
2. Update relevant agent(s) to use new source
3. Add API key to `api_keys.env`
4. Document in `ARCHITECTURE.md`

## Key Technologies per Component

| Component | Technologies |
|-----------|-------------|
| Orchestration | Claude Code subagents, Markdown prompts |
| Geographic calculations | Python, GeoPandas, Shapely |
| Data APIs | GBIF, IUCN, iNaturalist REST APIs |
| Data format | JSON (structured) |
| Environment | Python 3.10+, pip, virtualenv |
| Version control | Git |

## Dependencies

### System Requirements
- Python 3.10+
- GDAL (for GeoPandas)
- Claude Code CLI

### Python Packages
- geopandas - Geographic operations
- shapely - Geometric calculations
- pandas - Data manipulation
- requests - API calls
- python-dotenv - Environment variables

### API Keys (Free Registration)
- IUCN Red List API - Required
- Others - Optional (GBIF works without key)

---

**Legend:**
- ✅ = Implemented and functional
- ⏳ = Planned/To be implemented
- 📋 = Documentation
- 🤖 = AI agents
- 🐍 = Python code
- 📊 = Data files
- 🔧 = Scripts
- 💻 = Source code
- 🧪 = Tests
