# Tasks: Bookmark Parser Improvements

**Feature**: Bookmark Parser Improvements  
**Branch**: `002-parser-improvements`  
**Generated**: 2026-04-30  
**Plan**: [plan.md](./plan.md)

## MVP Scope

**User Story 1** (Validate URLs with Security Checks) is the MVP. This story delivers the core security value and can be tested independently.

## Phase 1: Setup

- [X] T001 Install httpx dependency (add to pyproject.toml if needed)
- [X] T002 [P] Create src/groupmrk/validator.py (empty module structure)
- [X] T003 [P] Create src/groupmrk/verifier.py (empty module structure)
- [X] T004 Update src/groupmrk/__init__.py exports for new modules

## Phase 2: Foundational

- [X] T005 Extend models.py with URL value object class in src/groupmrk/models.py
- [X] T006 Extend models.py with ValidationResult class in src/groupmrk/models.py
- [X] T007 Extend models.py with URLVerificationResult class in src/groupmrk/models.py
- [X] T008 Extend models.py with InvalidURLLog class in src/groupmrk/models.py
- [X] T009 Extend BookmarkCollection with invalid_urls and unreachable_urls fields in src/groupmrk/models.py

## Phase 3: User Story 1 - Validate URLs with Security Checks (P1)

**Goal**: Validate each URL for security threats and log invalid/suspicious URLs

**Independent Test**: Import bookmarks with invalid URLs and verify they are logged with reasons

### Implementation

- [X] T010 [P] [US1] Implement validate_url() function in src/groupmrk/validator.py
- [X] T011 [P] [US1] Implement detect_sql_injection() pattern detection in src/groupmrk/validator.py
- [X] T012 [P] [US1] Implement detect_xss() pattern detection in src/groupmrk/validator.py
- [X] T013 [P] [US1] Implement detect_path_traversal() pattern detection in src/groupmrk/validator.py
- [X] T014 [P] [US1] Implement detect_invalid_characters() validation in src/groupmrk/validator.py
- [X] T015 [US1] Integrate validation into parser.py parse flow in src/groupmrk/parser.py
- [X] T016 [US1] Add invalid URL logging to collection (InvalidURLLog) in src/groupmrk/parser.py
- [X] T017 [US1] Output validation summary to console with valid/invalid counts in src/groupmrk/cli.py
- [X] T018 [US1] Implement secure logging (exclude sensitive query params from logs) in src/groupmrk/validator.py

### Tests

- [X] T019 [P] [US1] Create tests/unit/test_validator.py with pattern detection tests
- [X] T020 [P] [US1] Add validation integration tests in tests/unit/test_parser.py
- [X] T021 [P] [US1] Add edge case tests for malformed URLs in tests/unit/test_validator.py

## Phase 4: User Story 2 - Remove Duplicate Bookmarks (P2)

**Goal**: Eliminate duplicate bookmarks based on normalized URL

**Independent Test**: Import bookmarks with duplicates and verify only first occurrence remains

### Implementation

- [X] T022 [P] [US2] Implement normalize_url() function in src/groupmrk/validator.py
- [X] T023 [US2] Implement deduplication logic in parser.py in src/groupmrk/parser.py
- [X] T024 [US2] Preserve first occurrence, discard duplicates in src/groupmrk/parser.py

### Tests

- [X] T025 [P] [US2] Add deduplication tests in tests/unit/test_parser.py

## Phase 5: User Story 3 - Group Local Links Together (P3)

**Goal**: Group localhost, file://, and private IPs into dedicated "Local Network" category

**Independent Test**: Import bookmarks with local URLs and verify they appear in Local Network category

### Implementation

- [X] T026 [P] [US3] Implement is_local_url() detection in src/groupmrk/validator.py
- [X] T027 [P] [US3] Add Local Network emoji (🔗) to EMOJI_MAP in src/groupmrk/models.py
- [X] T028 [US3] Add local network categorization in parser.py in src/groupmrk/parser.py
- [ ] T029 [US3] Reject non-RFC1918 internal IP ranges in src/groupmrk/validator.py

### Tests

- [X] T030 [P] [US3] Add local link detection tests in tests/unit/test_validator.py

## Phase 6: User Story 4 - Separate IP Address URLs (P4)

**Goal**: Detect and separate URLs with IP addresses from domain-based URLs

**Independent Test**: Import bookmarks with IP URLs and verify they are categorized separately

### Implementation

- [X] T031 [P] [US4] Implement is_ip_address() detection in src/groupmrk/validator.py
- [X] T032 [US4] Add IP-based URL categorization in parser.py in src/groupmrk/parser.py

### Tests

- [X] T033 [P] [US4] Add IP address detection tests in tests/unit/test_validator.py

## Phase 7: URL Verification

**Goal**: Verify URL accessibility via HTTP HEAD requests with security measures

### Implementation

- [X] T034 [P] Implement URLVerifier class with httpx security config in src/groupmrk/verifier.py
- [X] T035 [P] Implement verify_single() with 5s timeout and max_redirects=1 in src/groupmrk/verifier.py
- [X] T036 [P] Implement verify_batch() with 10 concurrent connections in src/groupmrk/verifier.py
- [X] T037 [P] Configure httpx: HEAD-only requests, SSL verify enabled in src/groupmrk/verifier.py
- [X] T038 Skip local network URLs from verification in src/groupmrk/verifier.py
- [X] T039 Integrate URL verification into parser flow in src/groupmrk/parser.py
- [X] T040 Mark unreachable URLs with warning status in src/groupmrk/parser.py
- [X] T041 Output verification summary to console (valid/invalid/unreachable) in src/groupmrk/cli.py

### Tests

- [X] T042 [P] Create tests/unit/test_verifier.py with mock HTTP tests

## Phase 8: Polish & Cross-Cutting

- [ ] T043 Run all existing tests to verify no regression
- [ ] T044 Verify performance (< 50% overhead with dedup enabled)
- [ ] T045 Add end-to-end integration test for full parser flow
- [ ] T046 Update README if needed for new features

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 46 |
| Setup | 4 |
| Foundational | 5 |
| User Story 1 (P1 - MVP) | 12 |
| User Story 2 (P2) | 3 |
| User Story 3 (P3) | 4 |
| User Story 4 (P4) | 2 |
| URL Verification | 9 |
| Polish | 4 |

### Parallel Opportunities

- T002, T003 (Setup - validator.py and verifier.py creation)
- T010-T014 (US1 - pattern detection functions)
- T019-T021 (US1 - tests)
- T022, T026, T027, T031 (validator functions)
- T025, T030, T033 (tests for multiple stories)
- T034-T037 (verifier class methods)
- T042 (verifier tests)

### Dependency Graph

```
Setup (T001-T004)
    │
    ▼
Foundational (T005-T009)
    │
    ├─────────────────────┬─────────────────────┐
    ▼                     ▼                     ▼
US1 (T010-T021)      US2 (T022-T025)      US3 (T026-T030)
    │                     │                     │
    └──────────┬──────────┘                     │
               ▼                                ▼
          US4 (T031-T033)              US4 (T031-T033)
                │                                │
                └────────────┬───────────────────┘
                             ▼
                   Verification (T034-T042)
                             │
                             ▼
                       Polish (T043-T046)
```

### Independent Test Criteria

| User Story | Test Criteria |
|------------|---------------|
| US1 | Import file with invalid URLs → All logged with reasons |
| US2 | Import file with duplicates → Only first occurrence retained |
| US3 | Import file with localhost/private IPs → All in Local Network category |
| US4 | Import file with IP URLs → Separate from domain URLs |
| Verification | All URLs verified (except local) → Summary shows valid/invalid/unreachable counts |
| MVP Acceptance | Must detect SQL injection, XSS, path traversal patterns and log with specific reasons |