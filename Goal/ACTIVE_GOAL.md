# ACTIVE PROGRAM GOAL – v0.7.1 Activity Localization and Compact Geometry Correctness

> **Status:** APPROVED FOCUSED BUGFIX PROGRAM
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released baseline:** `v0.7.0` at `46912952b200d8a296e94d1429e33c1484dc91b5`
> **Final target:** released and reconciled `v0.7.1`
> **Execution model:** focused sequential bugfix release
> **STOP:** only after v0.7.1 release, reconciliation, and final verification

## Program sequence

```text
Phase A: documentation privacy and bilingual navigation
→ HARD MAINTENANCE GATE
→ Phase B: runtime English / Simplified Chinese UI
→ Phase C: persistent manual Compact
→ full regression and release gates
→ exact-head Windows CI
→ merged-main RC
→ v0.7.1 tag and GitHub Release
→ final reconciliation
→ STOP
```

## Phase A — documentation and repository hygiene

- `start_codex_status_pet.cmd` is the only documented supported launcher.
- Every tracked Markdown file must avoid local absolute paths, user-profile
  paths, UNC paths, file URIs, repository escapes, and actual user fragments.
- The documentation root may describe at most `codex-windows-status-pet/`.
- Only `docs/document_manifest.json` English/Chinese pairs require reciprocal
  language switches and same-language managed-document navigation.
- README files must truthfully describe released v0.6.3 row visibility,
  battery-source selector, weekly default, and no-fallback behavior.
- Phase A makes no runtime change, version bump, product tag, or Release.

## v0.7.0 runtime language contract

- Supported persisted values are exactly `en` and `zh-CN`; the default is `en`.
- Do not auto-detect operating-system language or add a localization dependency.
- A Tk-independent localization API owns static translations, language
  normalization, key parity, placeholder parity, and visible missing-key errors.
- Settings contains a read-only language dropdown with explicit label/code mapping.
- Apply previews without persisting; Close restores the opening language; Save
  persists atomically; Restore Defaults selects English.
- Translate normal overlay, Settings, context-menu, tray-menu, warning, and
  error text, while preserving stable row IDs and tray action IDs.

## v0.7.0 manual Compact contract

- Remove `compact_when_idle` from product settings UI and automatic idle/hover,
  activity, refresh, render, and menu-driven compaction behavior.
- Add persisted boolean `compact`, default `false`; legacy
  `compact_when_idle` never implies `compact=true`.
- Add localized context-menu checkbox `Compact` / `收缩` beside topmost and lock.
- Toggling the checkbox immediately changes the visual state and persists
  atomically; persistence failure remains safe and diagnostic-only.
- Manual compact state survives hover, activity, status render, right-click,
  Hide/Show, tray Show, Settings lifecycle, language preview, and restart.
- Compact stays a complete ten-cell selected-source battery with no fallback.

## v0.7.1 correctness contract

- The activity source returns language-independent activity and progress states
  plus a numeric active count. Only the presentation boundary localizes those
  states for `en` or `zh-CN`; reverse translation is forbidden.
- Persisted `x` and `y` remain canonical expanded-window coordinates. Compact
  geometry is derived from them, and Compact drag validates the visible square
  before converting it back to canonical coordinates for persistence.
- General settings re-application preserves the current manual mode. While
  Compact is active, lock, topmost, language, opacity, scale, row visibility,
  and battery-source changes keep a compact square containing the complete
  ten-cell battery.

## Protected contracts

- Local official app-server quota authority, no token reader, no third-party
  quota endpoint, no telemetry, no backend, and no Codex-core modification.
- Five stable row identities, truthful duration-based quota identity, row
  visibility/source independence, selected battery source, and no fallback.
- Settings transactions, proportional 80–200% scale, DPI recovery, position
  persistence, Shell identity, tray reachability, one instance, bounded refresh,
  and safe shutdown.

## Required verification and release sequence

- Use TDD RED/GREEN for new behavior and systematic debugging for failures.
- Run documentation privacy/navigation, governance, link, and parity checks;
  focused configuration/localization/UI/compact tests; Quality; package smoke;
  and formal RC where observable.
- Review complete diff, unrelated changes, and credentials before remote writes.
- Require exact-head Windows CI, squash merge, merged-main RC, annotated tag,
  GitHub Release, and final authoritative-state reconciliation.
- v0.7.1 is released, tagged, and published after exact-head Windows CI and merged-main verification. STOP.
