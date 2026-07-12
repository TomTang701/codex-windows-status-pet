# Execution State

- Program Goal: `ACTIVE — Post-v0.6.3 Hygiene → v0.7.0 Bilingual UI and Manual Compact`
- Latest released product: `v0.6.3` at `7991c38ab19f05966025a46999c83852ea4c5b15`.
- Active implementation version: `v0.7.0`.
- Active phase: `release-candidate verification and release preparation`.
- Current branch: `feat/v0.7.0-bilingual-ui-manual-compact` at `b676752` before the current release-candidate changes.
- Blocker: `None`.
- Human fact required: `None`.

## Released baseline evidence

- v0.6.1: PR #28 exact-head Windows CI passed; product squash merge, tag, and GitHub Release target are `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- v0.6.2: PR #29 exact-head Windows Quality passed at `ff51ef0672310065b6599dfa287f93d7abf948a1`; product squash merge, tag, and GitHub Release target are `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`; reconciliation PR #30 merged at `9b42a16088daa05b61f8c4951401b5b50c6c7d1c`.
- v0.6.3: PR #31 exact-head Windows Quality passed at `318d3ab116978a3add1dd2e6c6d97dfdbf0b929c`; product squash merge, annotated tag target, and GitHub Release target are `7991c38ab19f05966025a46999c83852ea4c5b15`.
- v0.6.3 verified candidate evidence: focused RED/GREEN for configuration/snapshot, controller/main-window forwarding, and settings selector; 153 core tests; 26 UI tests; source matrices at 96/120 DPI; legacy content-fit, mixed-DPI, position, runtime, Shell identity, package smoke, and strict readiness.
- Formal RC/Quality evidence: exact child gates completed locally because the monolithic terminal runners exceed the observation window; exact-head Windows Quality CI passed for every product PR.

## Current product and next action

- v0.6.1: truthful quota-window identity with missing windows unavailable and weekly default battery source without fallback.
- v0.6.2: independent 5-hour, weekly, and reset-credit visibility with canonical, equal dynamic row distribution.
- v0.6.3: persisted 5-hour/weekly battery selector, weekly default, no fallback, and source/row-visibility independence.
- Phase A: privacy/navigation gates are implemented and passed. Phase B/C: language normalization, translated runtime/menu/tray UI, in-place Settings language preview/rollback, and persisted manual Compact are implemented with focused RED/GREEN evidence.
- Current candidate updates: old automatic-Compact configuration output and state APIs are removed; legacy input is ignored; reset-credit text is localized; version sources and release documentation are being reconciled to `0.7.0`.
- Next action: `run the full v0.7.0 regression matrix, Quality child gates, package smoke, and formal RC; then complete diff/security review and the authorized GitHub release workflow.`
- Last updated: `2026-07-12`.
