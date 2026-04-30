# Feature Specification: AI-Powered Bookmarks Manager

**Feature Branch**: `001-bookmarks-manager`  
**Created**: 2026-04-29  
**Status**: Draft  
**Input**: User description: "An open-source browser bookmarks manager powered by LLM. Organize, search, and categorize your bookmarks using artificial intelligence. The tool should accept HTML bookmark exports from browsers (Chrome, Firefox, Edge) and output organized HTML that can be imported back. It must work without requiring the user to configure any API keys - using free cloud models via HuggingFace Inference API, with optional Ollama support for local models. Built with LangChain/LangGraph for LLM orchestration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Import and Organize Bookmarks with AI (Priority: P1)

As a user, I want to import my browser bookmarks from an HTML export file and have AI automatically organize them into logical categories/folders.

**Why this priority**: This is the core value proposition - the primary reason users would use this tool. Without bookmark import and AI organization, the tool has no purpose.

**Independent Test**: Can be fully tested by providing a sample HTML bookmark file and verifying that the output contains organized bookmarks in a valid HTML format that can be imported back into a browser.

**Acceptance Scenarios**:

1. **Given** a valid Chrome/Firefox/Edge HTML bookmark export file, **When** the user runs the import command, **Then** the system parses all bookmarks with their titles, URLs, and folder structure.
2. **Given** parsed bookmarks, **When** the LLM processes them, **Then** bookmarks are categorized into meaningful groups (e.g., "Development", "News", "Shopping", "Research").
3. **Given** organized bookmarks, **When** the user requests output, **Then** a valid HTML file is generated that can be imported back into any major browser.
4. **Given** no API keys configured, **When** the user runs the tool, **Then** it automatically uses HuggingFace Inference API with free models without requiring user configuration.

---

### User Story 2 - Search Bookmarks Using Natural Language (Priority: P2)

As a user, I want to search my bookmarks using natural language queries to find relevant links quickly without navigating folders.

**Why this priority**: Once users have many bookmarks, folder navigation becomes tedious. Natural language search provides immediate value and demonstrates the AI capabilities.

**Independent Test**: Can be tested by loading bookmarks and running search queries like "Find my Python tutorials" and verifying relevant bookmarks are returned.

**Acceptance Scenarios**:

1. **Given** a loaded bookmark collection, **When** user types a natural language query, **Then** the system returns bookmarks ranked by relevance to the query.
2. **Given** a query that matches multiple categories, **Then** results are grouped by category with explanations of why each matched.

---

### User Story 3 - Local Model Support with Ollama (Priority: P3)

As a privacy-conscious user, I want to use local LLM models via Ollama instead of cloud APIs for complete data privacy.

**Why this priority**: Some users may have privacy concerns about sending bookmark data to cloud services. Providing local model support addresses this concern and expands the user base.

**Independent Test**: Can be tested by configuring Ollama endpoint and verifying the tool works without internet connectivity to HuggingFace.

**Acceptance Scenarios**:

1. **Given** Ollama is running locally, **When** user configures the tool to use Ollama, **Then** the system uses local models for all AI operations.
2. **Given** Ollama is not available or not configured, **Then** the system gracefully falls back to HuggingFace Inference API.

---

### User Story 4 - Manual Category Override and Editing (Priority: P4)

As a user, I want to manually adjust AIassigned categories or create custom categories for better organization.

**Why this priority**: AI categorization isn't perfect. Users should be able to fine-tune organization to match their mental model.

**Independent Test**: Can be tested by viewing categorized output and modifying a bookmark's category, then regenerating the output.

**Acceptance Scenarios**:

1. **Given** AI-categorized bookmarks, **When** user specifies a different category for a bookmark, **Then** the bookmark is moved to the user-specified category in the output.
2. **Given** custom category request, **When** user creates a new category name, **Then** a new folder is created in the output.

---

### Edge Cases

- What happens when the HTML file has malformed bookmark entries?
- How does system handle very large bookmark files (1000+ bookmarks)?
- What happens when HuggingFace API is unavailable or rate-limited?
- How are duplicate bookmarks handled?
- What happens when a bookmark has no title (only URL)?
- How does the system handle special characters in bookmark titles?
- What are the rate limits for the free HuggingFace API tier?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept HTML bookmark files from Chrome, Firefox, and Edge exports
- **FR-002**: System MUST parse bookmark metadata: title, URL, add_date, icon, and folder hierarchy
- **FR-003**: System MUST use HuggingFace Inference API by default without requiring API keys
- **FR-004**: System MUST support optional Ollama configuration for local model inference
- **FR-005**: System MUST output valid HTML bookmark format compatible with browser import
- **FR-006**: System MUST categorize bookmarks using LLM inference via LangChain/LangGraph
- **FR-007**: System MUST provide natural language search capability across bookmarks
- **FR-008**: System MUST allow users to override AI categorization with manual assignments
- **FR-009**: System MUST handle rate limiting and API failures gracefully with fallback behavior

### Key Entities

- **Bookmark**: Represents a single bookmark entry with title, URL, metadata, and assigned category
- **Category**: Grouping of bookmarks (e.g., "Development", "News") created by AI or user
- **BookmarkCollection**: Container for all bookmarks from an import, maintains original and AI-assigned categories
- **LLMProcessor**: LangChain/LangGraph workflow that orchestrates categorization logic

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can import a standard browser bookmark HTML file and receive organized output in under 30 seconds for files with up to 500 bookmarks
- **SC-002**: Generated HTML files are successfully importable into Chrome, Firefox, and Edge without errors
- **SC-003**: At least 80% of bookmarks are meaningfully categorized (not left in "Uncategorized")
- **SC-004**: System works out-of-the-box without any configuration required (zero-config experience)
- **SC-005**: Search returns relevant results within 5 seconds for collections up to 1000 bookmarks

## Assumptions

- Users have Python 3.10+ installed on their system
- Users have basic familiarity with command-line tools
- Free HuggingFace Inference API tier has sufficient rate limits for typical personal use
- Browser HTML export format follows standard Netscape Bookmark HTML format
- Privacy-conscious users will opt-in to Ollama support rather than it being the default
- The tool runs primarily as a CLI application with optional web interface in future versions