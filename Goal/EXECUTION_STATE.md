# Execution State

- Program Goal: `COMPLETED — v0.7.1 Activity Localization and Compact Geometry Correctness`.
- Latest released product: `v0.7.1` at `e45c457361d0ac3592e7d1e20671bc54f690661e`.
- Active implementation version: `None`.
- Active phase: `release-state reconciliation`.
- Current branch: `docs/v0.7.1-release-reconciliation` from released main.
- Blocker: `None`.
- Human fact required: `None`.

## Released baseline evidence

- v0.6.1: PR #28 exact-head Windows CI passed; product squash merge, tag, and GitHub Release target are `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- v0.6.2: PR #29 exact-head Windows Quality passed at `ff51ef0672310065b6599dfa287f93d7abf948a1`; product squash merge, tag, and GitHub Release target are `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`; reconciliation PR #30 merged at `9b42a16088daa05b61f8c4951401b5b50c6c7d1c`.
- v0.6.3: PR #31 exact-head Windows Quality passed at `318d3ab116978a3add1dd2e6c6d97dfdbf0b929c`; product squash merge, annotated tag target, and GitHub Release target are `7991c38ab19f05966025a46999c83852ea4c5b15`.
- v0.7.0: PR #33 exact-head Windows Quality passed at `873697c03557052aa32420b398988874967bc1ce`; squash merge is `46912952b200d8a296e94d1429e33c1484dc91b5`; merged-main package smoke, strict readiness, privacy/navigation, and version gates passed; annotated `v0.7.0` tag and GitHub Release target that merged commit.
- v0.6.3 verified candidate evidence: focused RED/GREEN for configuration/snapshot, controller/main-window forwarding, and settings selector; 153 core tests; 26 UI tests; source matrices at 96/120 DPI; legacy content-fit, mixed-DPI, position, runtime, Shell identity, package smoke, and strict readiness.
- Formal RC/Quality evidence: exact child gates completed locally because the monolithic terminal runners exceed the observation window; exact-head Windows Quality CI passed for every product PR.

## Current product and next action

- v0.6.1: truthful quota-window identity with missing windows unavailable and weekly default battery source without fallback.
- v0.6.2: independent 5-hour, weekly, and reset-credit visibility with canonical, equal dynamic row distribution.
- v0.6.3: persisted 5-hour/weekly battery selector, weekly default, no fallback, and source/row-visibility independence.
- v0.7.0: Phase A privacy/navigation gates, bilingual runtime UI, Settings transactions, localized normal error/warning text, and persisted manual Compact are released. Legacy automatic Compact input is ignored and no longer controls runtime behavior.
- v0.7.1: language-independent activity semantics localize only at presentation; manual Compact survives settings re-application; Compact drag validates visible-square bounds and persists canonical expanded coordinates. PR #35 exact-head Windows Quality passed; tag and GitHub Release target are `e45c457361d0ac3592e7d1e20671bc54f690661e`.
- Next action: `STOP — wait for Tom's next approved Goal.`
- Last updated: `2026-07-12`.
