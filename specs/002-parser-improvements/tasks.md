# Tasks: Bookmark Parser Improvements

**Feature**: Bookmark Parser Improvements  
**Branch**: `002-parser-improvements`  
**Generated**: 2026-04-30  
**Plan**: [plan.md](./plan.md)

## MVP Scope

**User Story 1** (Validate URLs with Security Checks) is the MVP. This story delivers the core security value and can be tested independently.

## Phase 1: Setup

- [ ] T001 Install httpx dependency (verify in pyproject.toml)
- [ ] T002 [P] Create src/groupmrk/validator.py (empty module structure)
- [ ] T003 [P] Create src/groupmrk/verifier.py (empty module structure)

## Phase 2: Foundational

- [ ] T004 Extend models.py with ValidationResult class in src/groupmrk/models.py
- [ ] T005 Extend models.py with URLVerificationResult class in src/groupmrk/models.py
- [ ] T006 Extend models.py with InvalidURLLog class in src/groupmrk/models.py
- [ ] T007 Extend BookmarkCollection with invalid_urls and unreachable_urls fields in src/groupmrk/models.py

## Phase 3: User Story 1 - Validate URLs with Security Checks (P1)

**Goal**: Validate each URL for security threats and log invalid/suspicious URLs

**Independent Test**: Import bookmarks with invalid URLs and verify they are logged with reasons

### Implementation

- [ ] T008 [P] [US1] Implement validate_url() function in src/groupmrk/validator.py
- [ ] T009 [P] [US1] Implement detect_sql_injection() pattern detection in src/groupmrk/validator.py
- [ ] T010 [P] [US1] Implement detect_xss() pattern detection in src/groupmrk/validator.py
- [ ] T011 [P] [US1] Implement detect_path_traversal() pattern detection in src/groupmrk/validator.py
- [ ] T012 [US1] Integrate validation into parser.py parse flow in src/groupmrk/parser.py
- [ ] T013 [US1] Add invalid URL logging to collection in src/groupmrk/parser.py
- [ ] T014 [US1] Output validation summary to console in src/groupmrk/cli.py

### Tests

- [ ] T015 [P] [US1] Create tests/unit/test_validator.py with pattern detection tests
- [ ] T016 [P] [US1] Add validation integration tests in tests/unit/test_parser.py

## Phase 4: User Story 2 - Remove Duplicate Bookmarks (P2)

**Goal**: Eliminate duplicate bookmarks based on normalized URL

**Independent Test**: Import bookmarks with duplicates and verify only first occurrence remains

### Implementation

- [ ] T017 [P] [US2] Implement normalize_url() function in src/groupmrk/validator.py
- [ ] T018 [US2] Implement deduplication logic in parser.py in src/groupmrk/parser.py
- [ ] T019 [US2] Preserve first occurrence, discard duplicates in src/groupmrk/parser.py

### Tests

- [ ] T020 [P] [US2] Add deduplication tests in tests/unit/test_parser.py

## Phase 5: User Story 3 - Group Local Links Together (P3)

**Goal**: Group localhost, file://, and private IPs into dedicated "Local Network" category

**Independent Test**: Import bookmarks with local URLs and verify they appear in Local Network category

### Implementation

- [ ] T021 [P] [US3] Implement is_local_url() detection in src/groupmrk/validator.py
- [ ] T022 [P] [US3] Add Local Network emoji to EMOJI_MAP in src/groupmrk/models.py
- [ ] T023 [US3] Add local network categorization in parser.py in src/groupmrk/parser.py

### Tests

- [ ] T024 [P] [US3] Add local link detection tests in tests/unit/test_validator.py

## Phase 6: User Story 4 - Separate IP Address URLs (P4)

**Goal**: Detect and separate URLs with IP addresses from domain-based URLs

**Independent Test**: Import bookmarks with IP URLs and verify they are categorized separately

### Implementation

- [ ] T025 [P] [US4] Implement is_ip_address() detection in src/groupmrk/validator.py
- [ ] T026 [US4] Add IP-based URL categorization in parser.py in src/groupmrk/parser.py

### Tests

- [ ] T027 [P] [US4] Add IP address detection tests in tests/unit/test_validator.py

## Phase 7: URL Verification

**Goal**: Verify URL accessibility via HTTP HEAD requests

### Implementation

- [ ] T028 [P] Implement URLVerifier class in src/groupmrk/verifier.py
- [ ] T029 [P] Implement verify_single() method with 5s timeout in src/groupmrk/verifier.py
- [ ] T030 [P] Implement verify_batch() with 10 concurrent connections in src/groupmrk/verifier.py
- [ ] T031 [P] Implement redirect limit (max 1 hop) in src/groupmrk/verifier.py
- [ ] T032 Skip local network URLs from verification in src/groupmrk/verifier.py
- [ ] T033 [US1] Integrate URL verification into parser flow in src/groupmrk/parser.py
- [ ] T034 [US1] Mark unreachable URLs with warning status in src/groupmrk/parser.py
- [ ] T035 Output verification summary to console in src/groupmrk/cli.py

### Tests

- [ ] T036 [P] Create tests/unit/test_verifier.py with mock HTTP tests

## Phase 8: Polish & Cross-Cutting

- [ ] T037 Run all existing tests to verify no regression
- [ ] T038 Verify performance (< 50% overhead with dedup enabled)
- [ ] T039 Update README if needed for new features

---

## Summary

| Metric | Count |
|--------|-------|
| Total Tasks | 39 |
| Setup | 3 |
| Foundational | 4 |
| User Story 1 (P1 - MVP) | 9 |
| User Story 2 (P2) | 3 |
| User Story 3 (P3) | 3 |
| User Story 4 (P4) | 2 |
| URL Verification | 8 |
| Polish | 3 |

### Parallel Opportunities

- T002, T003 (Setup - validator.py and verifier.py creation)
- T008-T011 (US1 - pattern detection functions)
- T015, T016 (US1 - tests)
- T017, T021, T022, T025 (validator functions)
- T020, T024, T027 (tests for multiple stories)
- T028-T031 (verifier class methods)
- T036 (verifier tests)

### Dependency Graph

```
Setup (T001-T003)
    │
    ▼
Foundational (T004-T007)
    │
    ├─────────────────────┬─────────────────────┐
    ▼                     ▼                     ▼
US1 (T008-T016)      US2 (T017-T020)      US3 (T021-T024)
    │                     │                     │
    └──────────┬──────────┘                     │
               ▼                                ▼
         US4 (T025-T027)              US4 (T025-T027)
               │                                │
               └────────────┬───────────────────┘
                            ▼
                   Verification (T028-T036)
                            │
                            ▼
                      Polish (T037-T039)
```

### Independent Test Criteria

| User Story | Test Criteria |
|------------|---------------|
| US1 | Import file with invalid URLs → All logged with reasons |
| US2 | Import file with duplicates → Only first occurrence retained |
| US3 | Import file with localhost/private IPs → All in Local Network category |
| US4 | Import file with IP URLs → Separate from domain URLs |
| Verification | All URLs verified (except local) → Summary output to console |