# Feature Specification: AI-Powered Bookmarks Manager

**Feature Branch**: `001-bookmarks-manager`  
**Created**: 2026-04-29  
**Status**: Clarified  
**Input**: "An open-source browser bookmarks manager powered by LLM..."

## Technical Clarifications

| Aspect | Decision |
|--------|----------|
| LLM Orchestration | LangGraph with Orchestrator + Theme Agents (max 10, configurable) |
| Model | Theme classification model (input: text → output: main theme) |
| Output Format | HTML with browser-import structure + emoji per theme |
| Project Structure | Single module, simplest possible |
| CLI | Flags with easy options for lay users |
| Dev Tools | uv (dev) / pip (user) - "download and use" approach |
| Testing | pytest with VSCode integration |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Import and Organize Bookmarks with AI (Priority: P1)

As a user, I want to import my browser bookmarks from an HTML export file and have AI automatically organize them into logical categories/folders.

**Why this priority**: Core value proposition - without import and AI organization, tool has no purpose.

**Independent Test**: Provide sample HTML bookmark file → verify output is valid HTML importable by browser.

**Acceptance Scenarios**:

1. **Given** valid Chrome/Firefox/Edge HTML export, **When** user runs import command, **Then** system parses all bookmarks with titles, URLs, and folder structure.
2. **Given** parsed bookmarks, **When** LLM processes them, **Then** bookmarks are categorized into themes (max 10, configurable).
3. **Given** organized bookmarks, **When** user requests output, **Then** valid HTML with emojis per theme, importable by browsers.
4. **Given** no API keys configured, **When** user runs tool, **Then** automatically uses HuggingFace Inference API (free, no key).

---

### User Story 2 - Search Bookmarks Using Natural Language (Priority: P2)

As a user, I want to search bookmarks using natural language to find links quickly.

**Why this priority**: Demonstrates AI value; folder navigation becomes tedious with many bookmarks.

**Independent Test**: Load bookmarks → run "Find my Python tutorials" → verify relevant results.

**Acceptance Scenarios**:

1. **Given** loaded collection, **When** user types query, **Then** returns bookmarks ranked by relevance.
2. **Given** query matches multiple categories, **Then** results grouped by category with explanations.

---

### User Story 3 - Local Model Support with Ollama (Priority: P3)

As a privacy-conscious user, I want local LLM via Ollama instead of cloud APIs.

**Why this priority**: Addresses privacy concerns; expands user base.

**Independent Test**: Configure Ollama endpoint → verify tool works without internet.

**Acceptance Scenarios**:

1. **Given** Ollama running locally, **When** user configures it, **Then** system uses local models.
2. **Given** Ollama unavailable, **Then** gracefully falls back to HuggingFace API.

---

### User Story 4 - Manual Category Override (Priority: P4)

As a user, I want to manually adjust AI categories or create custom ones.

**Why this priority**: AI isn't perfect; users should fine-tune to match their mental model.

**Independent Test**: View categorized output → modify category → regenerate output.

**Acceptance Scenarios**:

1. **Given** AI-categorized bookmarks, **When** user specifies different category, **Then** bookmark moves to user category.
2. **Given** custom category request, **When** user creates new category name, **Then** new folder created in output.

---

### LangGraph Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator Agent                   │
│  (receives all bookmarks, coordinates theme agents)    │
└─────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        ▼                 ▼                 ▼
   ┌─────────┐      ┌─────────┐       ┌─────────┐
   │ Theme   │      │ Theme   │  ...  │ Theme   │
   │ Agent 1 │      │ Agent 2 │       │ Agent N │
   │ (max 10)│      │         │       │         │
   └─────────┘      └─────────┘       └─────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ▼
              ┌─────────────────────────┐
              │   Final HTML Generator  │
              │   (combines all themes  │
              │    with emojis)         │
              └─────────────────────────┘
```

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept HTML bookmark files from Chrome, Firefox, and Edge
- **FR-002**: System MUST parse: title, URL, add_date, icon, folder hierarchy
- **FR-003**: System MUST use HuggingFace Inference API by default (no API key required)
- **FR-004**: System MUST support optional Ollama for local models
- **FR-005**: System MUST output valid HTML bookmark format (browser-importable)
- **FR-006**: System MUST use LangGraph with Orchestrator + Theme Agents architecture
- **FR-007**: System MUST categorize using theme classification model
- **FR-008**: System MUST add emoji per theme category in output
- **FR-009**: System MUST allow manual category override
- **FR-010**: System MUST provide natural language search
- **FR-011**: System MUST handle API failures gracefully with fallback

### Key Entities

- **Bookmark**: title, URL, metadata, assigned theme
- **Theme**: group of bookmarks with emoji identifier
- **ThemeAgent**: LLM agent specialized in one theme (max 10)
- **Orchestrator**: LangGraph agent coordinating theme agents
- **BookmarkCollection**: all bookmarks with original + AI categories

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Import + organize 500 bookmarks in under 30 seconds
- **SC-002**: Output HTML successfully importable to Chrome, Firefox, Edge
- **SC-003**: At least 80% of bookmarks categorized (not "Uncategorized")
- **SC-004**: Zero-config: works without any user configuration
- **SC-005**: Search returns results in under 5 seconds for 1000 bookmarks

## Assumptions

- Users have Python 3.10+
- Users may have zero technical knowledge
- Free HuggingFace Inference API tier sufficient for personal use
- Browser HTML follows Netscape Bookmark format
- Single module structure for easy contribution

## CLI Options (User-Friendly)

```
groupmrk import bookmarks.html           # Import and organize
groupmrk search "python tutorials"       # Natural language search
groupmrk export output.html               # Export organized bookmarks
groupmrk organize --max-themes 5         # Customize theme count
groupmrk --help                          # Show simple help
```