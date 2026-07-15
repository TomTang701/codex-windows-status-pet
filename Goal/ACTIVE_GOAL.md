# Active Goal: v0.9.2-beta.1 Signal HUD Validation

**Status:** in progress on the isolated UI branch
**Branch:** `feat/signal-hud-settings-ui-isolated`
**Baseline:** `v0.9.1` remains the latest stable public release
**Constraint:** do not modify, merge into, or push `main` from this goal

## Objective

Validate and package the isolated Signal HUD redesign as a beta candidate while
preserving the existing local-only data boundary and runtime behavior. This goal
does not authorize replacing `main` with a 1.0 release.

## In scope

- Use SemVer `0.9.2-beta.1` consistently across runtime, manifest, changelog,
  CI artifact expectations, installer identity, and user-facing documentation.
- Keep five stable logical row identities while rendering at most four expanded
  rows: activity/progress, 5-hour quota, Weekly quota, and Reset Credit.
- Keep compact mode as the ten-cell battery with a percentage that fits at the
  supported scale range.
- Keep quota text in the configured font color; represent quota health only in
  progress-bar and battery colors.
- Preserve settings Apply/Save/Close/Restore Defaults semantics, bilingual UI,
  tray recovery, scaling, persistence, and local app-server boundaries.
- Normalize the real Tk root Shell identity after settings lifecycle, topmost,
  alpha, and delayed-close paths.
- Reduce active documentation duplication while retaining historical audits as
  archived, non-normative evidence.
- Run Quality, strict compatibility/readiness, package and release-candidate
  checks; commit and push this branch only.

## Explicit exclusions

- No edits, commits, pushes, merges, tags, or releases on `main`.
- No 1.0 promotion until fresh physical Windows taskbar observations cover
  Settings Save, Close, right-corner Close, and window-manager close paths.
- No keyboard-shortcut feature, third-party quota service, telemetry, token
  reader, or Codex core modification.

## Acceptance gates

1. Version and bilingual documentation checks pass.
2. Full Quality checks pass and test evidence is current.
3. Candidate packaging/RC checks pass or every environment limitation is
   explicitly recorded.
4. Final diff contains only this branch's UI fixes, release metadata, and docs.
5. `main` remains unchanged; the branch commit is verified on origin.
