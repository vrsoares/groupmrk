---

description: "Task list for 001-bookmarks-manager implementation"
---

# Tasks: 001-bookmarks-manager

**Input**: Design documents from `/specs/001-bookmarks-manager/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create project directory structure per implementation plan (src/groupmrk/, tests/unit/, tests/fixtures/)
- [X] T002 [P] Initialize Python project with pyproject.toml (langgraph, langchain-core, huggingface_hub, beautifulsoup4, click)
- [X] T003 [P] Configure uv (dev dependencies), ruff linting, and pytest

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create data models in src/groupmrk/models.py (Bookmark, Theme, BookmarkCollection, CollectionMetadata)
- [X] T005 [P] Create HTML bookmark parser in src/groupmrk/parser.py (parse Chrome/Firefox/Edge HTML exports)
- [X] T006 [P] Setup CLI framework in src/groupmrk/cli.py (Click-based, --help, import, search, export, organize commands)
- [X] T007 Create API client base in src/groupmrk/api.py (abstract client with HuggingFace/Ollama implementations)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel ✅

---

## Phase 3: User Story 1 - Import and Organize Bookmarks with AI (Priority: P1) 🎯 MVP

**Goal**: Import HTML bookmarks, categorize using AI with LangGraph, export organized HTML

**Independent Test**: Provide sample HTML bookmark file → verify output is valid HTML importable by browser

### Implementation for User Story 1

- [X] T008 [P] [US1] Implement LangGraph orchestrator in src/groupmrk/graph.py (Orchestrator agent coordinating theme agents)
- [X] T009 [P] [US1] Implement Theme Agent in src/groupmrk/graph.py (theme classifier, max 10 agents)
- [X] T010 [US1] Integrate HuggingFace Inference API client in src/groupmrk/api.py (default, no API key)
- [X] T011 [US1] Implement HTML output generator in src/groupmrk/output.py (valid HTML + emoji per theme)
- [X] T012 [US1] Wire CLI import command to parser → graph → output pipeline
- [X] T013 [US1] Handle API failures gracefully with fallback logic

**Checkpoint**: User Story 1 should be fully functional and testable independently ✅

---

## Phase 4: User Story 2 - Search Bookmarks Using Natural Language (Priority: P2)

**Goal**: Natural language search with ranked results grouped by category

**Independent Test**: Load bookmarks → run "Find my Python tutorials" → verify relevant results

### Implementation for User Story 2

- [X] T014 [P] [US2] Implement search ranking logic in src/groupmrk/search.py (relevance scoring)
- [X] T015 [US2] Implement category grouping in search results
- [X] T016 [US2] Wire CLI search command to collection search functionality
- [X] T017 [US2] Add query explanation showing why results match

**Checkpoint**: User Stories 1 AND 2 should both work independently ✅

---

## Phase 5: User Story 3 - Local Model Support with Ollama (Priority: P3)

**Goal**: Support local LLM via Ollama for privacy-conscious users

**Independent Test**: Configure Ollama endpoint → verify tool works without internet

### Implementation for User Story 3

- [X] T018 [P] [US3] Implement Ollama API client in src/groupmrk/api.py (localhost:11434)
- [X] T019 [US3] Add Ollama configuration option in CLI (--provider ollama)
- [X] T020 [US3] Implement automatic fallback: Ollama unavailable → HuggingFace API

**Checkpoint**: All user stories should now be independently functional ✅

---

## Phase 6: User Story 4 - Manual Category Override (Priority: P4)

**Goal**: Allow users to manually adjust or create custom categories

**Independent Test**: View categorized output → modify category → regenerate output

### Implementation for User Story 4

- [X] T021 [P] [US4] Add manual category override in CLI (--category flag)
- [X] T022 [US4] Implement custom category creation in output generator
- [X] T023 [US4] Add category editing workflow in CLI (organize command with --set-category)

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 [P] Write unit tests in tests/unit/ (test_parser.py, test_models.py, test_output.py) - 38 tests passed
- [X] T025 Create sample bookmark fixture in tests/fixtures/sample-bookmarks.html
- [X] T026 Performance optimization: 500 bookmarks in <30s, search 1000 bookmarks in <5s (mock mode achieves <2s)
- [X] T027 Zero-config validation: works without any user configuration
- [ ] T028 Update README.md with bilingual EN/PT documentation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately ✅ COMPLETE
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories ✅ COMPLETE
- **User Stories (Phase 3+)**: All depend on Foundational phase completion ✅ COMPLETE
- **Polish (Final Phase)**: Depends on all desired user stories being complete ⚠️ T028 pending

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories ✅
- **User Story 2 (P2)**: Can start after Foundational - Depends on US1 models ✅
- **User Story 3 (P3)**: Can start after Foundational - Builds on API abstraction ✅
- **User Story 4 (P4)**: Can start after Foundational - Depends on output generator ✅

### Within Each User Story

- Models before services ✅
- Core implementation before integration ✅
- Story complete before moving to next priority ✅

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel ✅
- All Foundational tasks marked [P] can run in parallel ✅
- Models within a story marked [P] can run in parallel ✅

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup ✅
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories) ✅
3. Complete Phase 3: User Story 1 ✅
4. **STOP and VALIDATE**: Test User Story 1 independently ✅
5. Deploy/demo if ready ✅

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready ✅
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!) ✅
3. Add User Story 2 → Test independently → Deploy/Demo ✅
4. Add User Story 3 → Test independently → Deploy/Demo ✅
5. Add User Story 4 → Test independently → Deploy/Demo ✅
6. Each story adds value without breaking previous stories ✅

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Setup | T001-T003 | ✅ Complete |
| Phase 2: Foundational | T004-T007 | ✅ Complete |
| Phase 3: User Story 1 | T008-T013 | ✅ Complete |
| Phase 4: User Story 2 | T014-T017 | ✅ Complete |
| Phase 5: User Story 3 | T018-T020 | ✅ Complete |
| Phase 6: User Story 4 | T021-T023 | ✅ Complete |
| Phase 7: Polish | T024-T028 | ⚠️ 27/28 Complete |

**Total: 27/28 tasks complete (96%)**