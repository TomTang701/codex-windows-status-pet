# Execution State

- Program Goal: `COMPLETE / STOPPED — v0.6.1 → v0.6.3 Quota Presentation Controls`
- Latest released product: `v0.6.3` at `7991c38ab19f05966025a46999c83852ea4c5b15`.
- Active implementation version: `None`.
- Active phase: `final release-state reconciliation`.
- Current branch: `docs/v0.6.3-final-reconciliation` from product main `7991c38ab19f05966025a46999c83852ea4c5b15`.
- Blocker: `None`.
- Human fact required: `None`.

## Release evidence

- v0.6.1: PR #28 exact-head Windows CI passed; product squash merge, tag, and GitHub Release target are `40d59c8b7d9f9f536299aacc67686ed7a70467eb`.
- v0.6.2: PR #29 exact-head Windows Quality passed at `ff51ef0672310065b6599dfa287f93d7abf948a1`; product squash merge, tag, and GitHub Release target are `8b7c7fec2a864fa94601ed8235d04cb5cb716a03`; reconciliation PR #30 merged at `9b42a16088daa05b61f8c4951401b5b50c6c7d1c`.
- v0.6.3: PR #31 exact-head Windows Quality passed at `318d3ab116978a3add1dd2e6c6d97dfdbf0b929c`; product squash merge, annotated tag target, and GitHub Release target are `7991c38ab19f05966025a46999c83852ea4c5b15`.
- v0.6.3 verified candidate evidence: focused RED/GREEN for configuration/snapshot, controller/main-window forwarding, and settings selector; 153 core tests; 26 UI tests; source matrices at 96/120 DPI; legacy content-fit, mixed-DPI, position, runtime, Shell identity, package smoke, and strict readiness.
- Formal RC/Quality evidence: exact child gates completed locally because the monolithic terminal runners exceed the observation window; exact-head Windows Quality CI passed for every product PR.

## Final product state

- v0.6.1: truthful quota-window identity with missing windows unavailable and weekly default battery source without fallback.
- v0.6.2: independent 5-hour, weekly, and reset-credit visibility with canonical, equal dynamic row distribution.
- v0.6.3: persisted 5-hour/weekly battery selector, weekly default, no fallback, and source/row-visibility independence.
- Next action: `None — Program Goal complete; STOP and wait for Tom's next approved Goal.`
- Last updated: `2026-07-12`.
