# ACTIVE VERSION BRIEF — v0.5.0 Lean-Core Simplification

## Outcome

Delete four proven unnecessary production boundaries while preserving all current product behavior and verification authority:

1. remove unused typed quota models;
2. remove two historical resize APIs that have no runtime consumer;
3. remove the one-function quota provider pass-through and call the strict parser directly.

## Evidence and classification

| Candidate | Runtime consumers | Other consumers | Decision |
|---|---:|---:|---|
| `models_api.py` | 0 | 0 | DELETE |
| `window_size_api.py` | 0 | its own implementation-detail test | DELETE |
| `resize_session_api.py` | 0 | its own implementation-detail test | DELETE |
| `quota_provider_api.py` | 1 | its own wrapper test | MERGE into existing `quota_parse_api` consumer/contract |
| application/settings/presentation/lifecycle controllers | active UI and test consumers | behavior-level tests | KEEP |

## Protected behavior

- v0.4.2 release verification, inventory, RC, CI, and encoding contracts.
- 80–200% canonical window scaling and schema-1 downgrade fields.
- Strict approved quota fields, credential/token exclusion, local app-server-only transport, last-good/stale behavior, and five stable rows.
- Settings transactions, tray reachability, single instance, safe shutdown, Compact/Expand, Hide/Show, and DPI-aware content fit.

## Observable contracts

- The four obsolete/pass-through modules are absent from production.
- No active source or normative document imports or advertises them.
- `main_window.py` calls `parse_quota_payload` directly.
- Token/unknown fields remain excluded and malformed quota input remains unavailable.
- All protected runtime and release tests pass.
- Production Python file/LOC and API-module counts decrease; runtime dependency count does not increase.

## Out of scope

- Controller/state-owner merging without new evidence.
- Config schema change or removal of downgrade compatibility fields.
- Framework replacement, UI redesign, provider changes, installer, startup productization, or Phase 4 work.

## Design verification result

```text
DESIGN VERIFIED
Problem evidence: PASS
Root-cause hypothesis: N/A
Observable contract: PASS
Failure paths: PASS
Regression surface: PASS
RED definition: PASS — a source-boundary test fails while the four modules/imports remain
Scope bounded: PASS
Human verification required: NONE
```
