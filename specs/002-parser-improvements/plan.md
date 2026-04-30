# Implementation Plan: Bookmark Parser Improvements

**Branch**: `002-parser-improvements` | **Date**: 2026-04-30 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-parser-improvements/spec.md`

## Summary

Improve the bookmark parser to: (1) validate URLs for security threats (SQL injection, XSS, path traversal), (2) remove duplicate bookmarks via URL normalization, (3) group local/network links into dedicated category, (4) separate IP-based URLs from domain URLs, (5) verify URL accessibility via HTTP HEAD requests with security measures.

Technical approach: Use stdlib (urllib.parse, ipaddress, re) for validation to minimize dependencies, httpx for async batch HTTP verification, set-based deduplication with normalized URL keys.

## Technical Context

| Aspect | Value |
|--------|-------|
| Language/Version | Python 3.12 |
| Primary Dependencies | httpx (HTTP client), beautifulsoup4 (existing), pytest (existing) |
| Storage | N/A - in-memory processing |
| Testing | pytest (existing) |
| Target Platform | CLI tool (cross-platform) |
| Project Type | CLI tool |
| Performance Goals | Handle 1000+ bookmarks, <50% overhead with dedup, 5s URL timeout |
| Constraints | Max 10 concurrent HTTP connections, 10MB file size limit (existing) |
| Scale/Scope | Typical bookmark file: 100-10,000 URLs |

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Open Source (MIT) | PASS | No changes to licensing |
| II. Extreme Simplicity | PASS | Using stdlib where possible, minimizing new dependencies |
| III. LLM Orchestration | PASS | This feature doesn't affect LLM integration |
| IV. Local-First Models | PASS | No API key requirements added |
| V. HTML Input/Output | PASS | Maintaining HTML format compatibility |
| Code Language (English) | PASS | All code in English |
| Documentation (Bilingual) | PASS | Console output will be in English |

**Gate Result**: All gates pass - proceed to implementation.

## Project Structure

### Documentation (this feature)

```
specs/002-parser-improvements/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output (future)
├── contracts/           # N/A - no external interfaces
└── tasks.md             # Phase 2 output (via /speckit.tasks)
```

### Source Code (repository root)

```
src/groupmrk/
├── models.py            # Existing - add URL, ValidationResult classes
├── parser.py            # Existing - add validation and deduplication
├── validator.py         # NEW - URL security validation
├── verifier.py          # NEW - HTTP HEAD verification
├── cli.py               # Existing - may need output updates

tests/
├── unit/
│   ├── test_parser.py  # Existing - extend with new tests
│   ├── test_validator.py # NEW
│   └── test_verifier.py  # NEW
```

**Structure Decision**: Single project structure (Option 1). Adding new modules (validator.py, verifier.py) to src/groupmrk/ while extending existing parser.py and models.py.

## Implementation Details

### Module: validator.py (NEW)

Responsibility: URL security validation

```
Functions:
- validate_url(url: str) -> ValidationResult
- detect_sql_injection(url: str) -> list[str]
- detect_xss(url: str) -> list[str]
- detect_path_traversal(url: str) -> list[str]
- is_local_url(url: str) -> bool
- is_ip_address(host: str) -> bool
- normalize_url(url: str) -> str
```

### Module: verifier.py (NEW)

Responsibility: HTTP HEAD verification

```
Classes:
- URLVerifier
  - verify_batch(urls: list[str]) -> dict[str, URLVerificationResult]
  - verify_single(url: str) -> URLVerificationResult

Settings:
- timeout: 5 seconds
- max_redirects: 1
- max_concurrent: 10
- verify_ssl: true
```

### Changes: parser.py (EXISTING)

- Add deduplication logic using normalized URL set
- Add local network categorization
- Add IP-based URL detection

### Changes: models.py (EXISTING)

- Add URL class (value object)
- Add ValidationResult class
- Add URLVerificationResult class
- Extend BookmarkCollection with invalid_urls, unreachable_urls

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|---------------------------------------|
| New dependency (httpx) | Async batch HTTP requests required | stdlib urllib doesn't support async well; sync requests too slow for batch |
| Two new modules | Separation of concerns - validation vs verification | Combined module would violate single responsibility |

## Next Steps

1. Run `/speckit.tasks` to generate task list
2. Implement validator.py with security patterns
3. Implement verifier.py with httpx batch processing
4. Extend parser.py with deduplication and categorization
5. Extend models.py with new classes
6. Write tests for all new functionality
7. Run existing tests to ensure no regression