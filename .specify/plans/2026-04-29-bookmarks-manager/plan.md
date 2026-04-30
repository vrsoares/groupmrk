# Implementation Plan: 001-bookmarks-manager

**Branch**: `001-bookmarks-manager` | **Date**: 2026-04-29 | **Spec**: [spec.md](../specs/001-bookmark-manager/spec.md)

## Summary

AI-powered bookmarks manager that imports browser HTML exports and organizes them into themed categories using LangGraph orchestration with Ollama/HuggingFace Inference API (no API key required). Outputs valid HTML importable by browsers with emoji per theme.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: langgraph, huggingface_hub, beautifulsoup4, click  
**Storage**: File-based (JSON for bookmark collection cache)  
**Testing**: pytest with VSCode integration  
**Target Platform**: Cross-platform CLI (Windows/macOS/Linux)  
**Project Type**: CLI tool / single module  
**Performance Goals**: 500 bookmarks in <30s, search 1000 bookmarks in <5s  
**Constraints**: Zero-config (no API keys), offline fallback to Ollama  
**Scale/Scope**: Single-user personal bookmark collections (~100-5000 bookmarks)

## Constitution Check

- **Open Source**: MIT license confirmed
- **Extreme Simplicity**: Single-module structure, CLI flags only
- **LLM Orchestration**: LangGraph with Orchestrator + Theme Agents
- **No API Keys**: HuggingFace Inference API (free tier) default
- **HTML I/O**: Netscape Bookmark HTML format

## Project Structure

```text
groupmrk/
├── src/
│   └── groupmrk/
│       ├── __init__.py
│       ├── cli.py           # Click-based CLI
│       ├── parser.py        # HTML bookmark parser
│       ├── graph.py         # LangGraph orchestrator + theme agents
│       ├── models.py        # Data models (Bookmark, Theme, Collection)
│       ├── api.py           # HuggingFace + Ollama API clients
│       └── output.py        # HTML generator with emojis
├── tests/
│   ├── unit/
│   │   ├── test_parser.py
│   │   ├── test_models.py
│   │   └── test_output.py
│   └── fixtures/
│       └── sample-bookmarks.html
├── pyproject.toml
├── uv.lock
└── README.md
```

## Data Model

```
BookmarkCollection
├── bookmarks: List[Bookmark]
├── themes: List[Theme]
└── metadata: CollectionMetadata

Bookmark
├── title: str
├── url: str
├── add_date: Optional[datetime]
├── icon: Optional[str]
├── folder: str
└── theme: Optional[str]

Theme
├── name: str
├── emoji: str
└── agent_id: int
```

## API Strategy

| Provider | Endpoint | Auth | Fallback |
|----------|----------|------|----------|
| HuggingFace (default) | `https://api-inference.huggingface.co/...` | None | Ollama |
| Ollama (optional) | `http://localhost:11434/api/generate` | None | HuggingFace |

## LangGraph Architecture

```
Orchestrator
├── receives: raw bookmarks
├── spawns: Theme Agents (max 10)
└── aggregates: theme assignments

Theme Agent (x N)
├── input: bookmark subset
├── model: theme classifier
└── output: theme assignment per bookmark

HTML Generator
├── input: categorized bookmarks + themes
└── output: browser-importable HTML
```

## Implementation Phases

1. **Phase 1**: Core parser + models + basic CLI
2. **Phase 2**: LangGraph setup + theme agents
3. **Phase 3**: HuggingFace/Ollama integration
4. **Phase 4**: HTML output generator
5. **Phase 5**: Natural language search
6. **Phase 6**: Manual override + configuration

## Dependencies (pyproject.toml)

```toml
dependencies = [
    "langgraph>=0.0.15",
    "langchain-core>=0.1.0",
    "huggingface_hub>=0.20.0",
    "beautifulsoup4>=4.12.0",
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.1.0",
]

[project.scripts]
groupmrk = "groupmrk.cli:main"
```

## Project Agents

### Agent 1: Senior Python Developer
- **Role**: Code implementation, architecture, clean code, best practices
- **Experience**: Vast Python experience, clean code, documentation, agentic AI development
- **Responsibilities**:
  - Write production-quality Python code
  - Apply clean code principles (SOLID, DRY, KISS)
  - Implement LangGraph agents and orchestration
  - Create comprehensive inline documentation
  - Ensure type hints and error handling

### Agent 2: Documentation Writer
- **Role**: User-facing documentation, tutorials, guides
- **Level**: Technical level of a high school student
- **Responsibilities**:
  - Write README.md in bilingual format (EN/PT)
  - Create simple, visual "hands-on" instructions
  - Avoid technical jargon (no "dependencies", "virtual environment", etc.)
  - Focus on "download and use" experience
  - Explain concepts in plain language
```