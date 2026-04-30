# groupmrk Constitution

## Core Principles

### I. Open Source (MIT)
The project MUST be strictly Open Source under the MIT license. All source code, documentation, and distribution MUST be freely available under MIT terms.

### II. Extreme Simplicity
The focus MUST be on extreme simplicity for the end user. All technical barriers to entry MUST be eliminated. The tool MUST provide executables or one-click scripts whenever possible.

### III. LLM Orchestration (LangChain/LangGraph)
The tool MUST use LangChain and/or LangGraph for LLM orchestration to enable intelligent bookmark categorization and processing.

### IV. Local-First Models (No API Keys)
The tool MUST prioritize models that do NOT require API key configuration, such as local models via Ollama or pre-configured integrations. Users without API keys MUST be able to use the tool.

### V. HTML Input/Output
The tool MUST accept HTML input (browser bookmark exports) and generate organized HTML output that can be re-imported into browsers. Markdown output is also acceptable.

## Language & Documentation Standards

### Code Language
All source code, variable names, function names, and inline comments MUST be written exclusively in English.

### Interface & Documentation Language
The README.md file in the root, file headers, and any interface tooltips MUST be bilingual (English and Portuguese).

### User Documentation
User documentation MUST assume zero knowledge of programming, package management (pip, npm, etc.), or development environments. Instructions MUST be hands-on and visual, avoiding technical terms like "dependencies", "virtual environment", or "repository".

## Development Workflow

### Spec-Driven Development (SDD)
The project MUST follow Spec-Driven Development methodology:
- Every new feature MUST pass through `/speckit.specify`, `/speckit.plan`, and `/speckit.tasks` commands before implementation.
- The "what" and "why" MUST be specified before the "how".
- All feature specifications, plans, and tasks MUST be documented in `.specify/` directory.

## Governance

### Amendment Procedure
- The Constitution supersedes all other practices and documentation.
- Any amendments to the Constitution MUST be documented, approved, and include a migration plan if applicable.
- Version changes follow semantic versioning (MAJOR for backward-incompatible changes, MINOR for new principles, PATCH for clarifications).

### Compliance
- All features, plans, and tasks MUST verify compliance with this Constitution.
- Complexity that violates any principle MUST be justified in the Complexity Tracking section of the plan.

**Version**: 1.0.0 | **Ratified**: 2026-04-29 | **Last Amended**: 2026-04-29