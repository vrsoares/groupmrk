# Tasks: HTTP Response Handling (Spec 003)

## Security Decisions

| Decision | Choice |
|----------|--------|
| Private IPs | Block ALWAYS (initial + redirects) |
| GET fallback | Content-Length header only (no body read) |
| Port restriction | Only 80/443 |
| Request cap | 5000 max |
| Credential URLs | Block |

---

## Phase 1: Data Model Setup (~70 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T1.1 | Add HTTP fields to Bookmark: `http_status_code`, `is_reachable`, `verification_error`, `final_url`, `redirect_chain`, `is_safe_extension`, `extension_get_used` | models.py:8-18 | Fields added with proper types |
| T1.2 | Add statistics to CollectionMetadata: `security_valid_count`, `reachable_count`, `filtered_count`, `filtered_4xx`, `filtered_5xx`, `filtered_timeout`, `filtered_connection`, `filtered_ssrf`, `filtered_redirect_loop`, `redirects_followed`, `extension_get_attempts`, `extension_get_successes` | models.py:41-49 | All counters initialized |
| T1.3 | Add constants: `SAFE_EXTENSIONS`, `PRIVATE_IP_RANGES` (include 0.0.0.0/8, 224.0.0.0/4, 240.0.0.0/4, 100.64.0.0/10, 198.18.0.0/15, 203.0.113.0/24), `ALLOWED_PORTS` (80, 443), `MAX_REQUESTS` (5000), `SENSITIVE_PARAMS` | models.py | All constants defined |
| T1.4 | Add `VerificationOutcome` enum and `VerificationResult` dataclass | models.py | Enum covers all outcomes; `should_keep` property works |

---

## Phase 2: Core Verification (~250 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T2.1 | Create `URLVerifier` class with `__init__` (timeout=10s, max_redirects=5) and `verify(url)` method | verifier.py | Class initializes; verify() returns VerificationResult |
| T2.2 | Implement HTTP status handling: 2xx→keep, 304→keep, 401→keep, 403→special, 404→remove, 5xx→remove | verifier.py | Correct outcome per status code |
| T2.3 | Implement SSRF protection: block ALL private IPs (initial + redirects) using `socket.getaddrinfo()` for DNS resolution BEFORE connection; add all missing IP ranges | verifier.py | Private IPs blocked always (AC4) |
| T2.4 | Implement redirect handling: `allow_redirects=False`, manual per-hop, block dangerous protocols, detect loops, max 5 hops, restrict to ports 80/443 only | verifier.py | SSRF at each hop; loops detected (AC8) |
| T2.5 | Implement extension GET fallback: check `has_safe_extension(url)`, if 403/405 try GET with `stream=True`, check `Content-Length` header only, DO NOT read body, close immediately | verifier.py | Safe extensions trigger fallback (AC2); no body read |
| T2.6 | Implement concurrency: `asyncio.Semaphore(5)`, process in batches of 3-5, 100ms delay | verifier.py | Max 5 concurrent; rate limiting |
| T2.7 | Add `redact_url(url)`: redact 16 sensitive params + long path segments | verifier.py | Sensitive params redacted (AC9) |
| T2.8 | Add URL validation: custom User-Agent `groupmrk/1.0`, reject URLs > 2048 chars, block credentials (`user:pass@host`) | verifier.py | UA set; long URLs rejected; credential URLs blocked |
| T2.9 | Add request counter: track total requests, stop at MAX_REQUESTS (5000) | verifier.py | Counter enforced; excess logged |

---

## Phase 3: Integration (~60 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T3.1 | Add verification step to CLI flow (Step 1.5/4): call `URLVerifier.verify_batch()`, filter unreachable, update metadata | cli.py:64-93 | New step between parse and organize |
| T3.2 | Update `Orchestrator.organize()` to filter `is_reachable=False` before classification | graph.py | Only reachable classified |
| T3.3 | Update `HTMLOutputGenerator` to filter `is_reachable=False` from output | output.py | Unreachable excluded from HTML |
| T3.4 | Import URLVerifier and redact_url in cli.py | cli.py | Clean imports |

---

## Phase 4: Classification Fix (~55 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T4.1 | Fix `HuggingFaceClient.classify_theme()`: add proper validation, check `result.labels` and `result.scores`, log errors | api.py:68-86 | No silent failures |
| T4.2 | Add `_keyword_fallback(title, url)`: map keywords to themes (github→Development, python→Programming, etc.) | api.py | Real themes returned |
| T4.3 | Add same `_keyword_fallback()` to `OllamaClient` | api.py | Consistent fallback |

---

## Phase 5: Statistics Display (~20 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T5.1 | Display: "Parsed: X → Security Valid: Y → Reachable: Z → Categorized: N themes" | cli.py | Pipeline counts shown (AC7) |
| T5.2 | Display: "Filtered: N (404: X, 403: Y, Timeout: Z)" | cli.py | Filter reasons shown |
| T5.3 | Display: "Redirects followed: N" | cli.py | Redirect count shown |

---

## Phase 6: Testing (~150 lines)

| ID | Task | File | Acceptance |
|----|------|------|------------|
| T6.1 | Create test_verifier.py: mock HTTP responses for 2xx, 3xx, 4xx, 5xx, timeout, connection error | test_verifier.py | All statuses handled |
| T6.2 | Test SSRF protection: private IPs blocked (all ranges) | test_verifier.py | All ranges blocked (AC4) |
| T6.3 | Test redirect loops: A→B→A detected, max 5 hops | test_verifier.py | Loop detected (AC8) |
| T6.4 | Test GET fallback: .pdf with 403 on HEAD, GET attempted | test_verifier.py | Fallback works (AC2) |
| T6.5 | Test redact_url(): sensitive params replaced | test_verifier.py | Params redacted (AC9) |
| T6.6 | Test auth-required: 401/403 with WWW-Authenticate kept | test_verifier.py | Auth kept (AC5) |
| T6.7 | Test credential URL blocking | test_verifier.py | user:pass@host blocked |
| T6.8 | Test port restriction: redirects to non-80/443 blocked | test_verifier.py | Ports restricted |
| T6.9 | Test classification fix: real themes returned | test_api.py | Themes work (AC6) |
| T6.10 | Test CLI statistics output | test_cli.py | Stats shown (AC7) |
| T6.11 | Test full pipeline: 404/500 excluded | test_pipeline.py | Bad URLs removed (AC1) |

---

## Summary

| Phase | Tasks | Lines |
|-------|-------|-------|
| 1 | T1.1-T1.4 | ~70 |
| 2 | T2.1-T2.9 | ~250 |
| 3 | T3.1-T3.4 | ~60 |
| 4 | T4.1-T4.3 | ~55 |
| 5 | T5.1-T5.3 | ~20 |
| 6 | T6.1-T6.11 | ~150 |
| **Total** | **32 tasks** | **~605** |

---

## Acceptance Criteria Coverage

| AC | Criterion | Task |
|----|-----------|------|
| AC1 | 404/500 NOT in output | T6.11 |
| AC2 | Extension GET fallback | T2.5, T6.4 |
| AC3 | Redirects followed | T2.4 |
| AC4 | SSRF protection | T2.3, T6.2 |
| AC5 | Auth-required kept | T6.6 |
| AC6 | Real themes | T4.1-T4.3, T6.9 |
| AC7 | Statistics shown | T5.1-T5.3, T6.10 |
| AC8 | Redirect loops blocked | T2.4, T6.3 |
| AC9 | Params redacted | T2.7, T6.5 |
| AC10 | Credential URLs blocked | T2.8, T6.7 |
| AC11 | Port restriction | T2.4, T6.8 |