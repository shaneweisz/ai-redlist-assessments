# Documentation

Complete documentation for the AI-assisted IUCN Red List assessment pipeline.

## 📖 Getting Started

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Setup instructions and usage guide
  - Prerequisites and installation
  - Running your first assessment
  - Understanding the output
  - Troubleshooting

## 🏗️ Architecture & Design

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system design
  - Multi-agent architecture (12 agents, 5 phases)
  - Data flow and communication protocols
  - Agent specifications
  - Performance targets

- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Current status and roadmap
  - What's implemented (Phases 1-2)
  - What's planned (Phases 3-5)
  - Success metrics
  - Future enhancements

- **[STRUCTURE.md](STRUCTURE.md)** - Project organization
  - Directory structure
  - File descriptions
  - Usage patterns

## 🤖 AI Transparency

- **[AI_DEVELOPMENT_LOG.md](AI_DEVELOPMENT_LOG.md)** - Complete development session log
  - Timeline and phases
  - Human vs AI decision-making
  - Prompts and interactions
  - Reproducibility guide
  - Ethical considerations

## 📊 Reference Materials

See [reference/](reference/) folder for:
- **[SAMPLE_ASSESSMENT_DATA.md](reference/SAMPLE_ASSESSMENT_DATA.md)** - IUCN data structure guide
  - Complete field descriptions
  - API endpoints
  - Criteria interpretation
  - Example JSON structures

- **[example_assessment.json](reference/example_assessment.json)** - Atlantic Puffin reference
  - Complete real assessment
  - All required fields populated
  - Shows expected output format

## 🧪 Test Results

See [results/](results/) folder for:
- **[PANTHERA_LEO_RESULTS.md](results/PANTHERA_LEO_RESULTS.md)** - Lion assessment results
  - Complete test run documentation
  - Comparison with official IUCN assessment
  - Performance metrics
  - Validation findings

## 📚 Additional Resources

### IUCN Official Documentation
- Red List Website: https://www.iucnredlist.org
- Categories & Criteria: https://www.iucnredlist.org/resources/categories-and-criteria
- Guidelines: https://www.iucnredlist.org/resources/redlistguidelines
- API Documentation: https://api.iucnredlist.org/api-docs

### Data Sources
- GBIF: https://www.gbif.org
- Catalogue of Life: https://www.catalogueoflife.org
- iNaturalist: https://www.inaturalist.org

### Related Tools
- sRedList (R package): For IUCN-compliant assessments
- rredlist (R): IUCN API client
- ConR (R): Geographic range calculations

---

**Navigation:**
- [← Back to main README](../README.md)
- [View code →](../scripts/)
- [View agents →](../.claude/agents/)
