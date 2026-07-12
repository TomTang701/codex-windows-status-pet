# ACTIVE PROGRAM GOAL — v0.8.0 Windows Productization and Menu Unification

> **Status:** APPROVED / ACTIVE
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released baseline:** `v0.7.1` at `e45c457361d0ac3592e7d1e20671bc54f690661e`
> **Target product:** `v0.8.0`

## Objective

Ship the existing Windows companion as an independently installable Windows 11
x64 application while preserving v0.7.1 behavior, unifying tray and overlay
menu semantics, and publishing authentic bilingual packaged-runtime evidence.

## Scope and non-negotiable contracts

- Use one committed PyInstaller **onedir** configuration and the existing
  production entry path. The installed product must need no repository checkout,
  Python, pip, or Git.
- The release ZIP contains only the `CodexStatusPet/` runtime root, EXE,
  `_internal/`, manifest, MIT license, third-party notices, and uninstall script;
  it excludes source, tests, Goal files, docs, CI, build tooling, local settings,
  credentials, and tokens.
- `install.ps1` performs checksum-verified per-user install/upgrade at
  `%LOCALAPPDATA%\Programs\CodexStatusPet`; `uninstall.ps1` preserves settings
  unless its explicit purge option removes only the product settings JSON. No
  automatic startup or updater is permitted.
- Tray and overlay menus expose the same localized Settings, Always on top, Lock
  position, Compact, visibility, and Exit controls. Visible menus use Hide;
  the hidden overlay remains recoverable through tray Show. Tk owns state
  transitions; the pystray thread only queues stable actions.
- Preserve official local app-server quota authority, approved session activity
  authority, English/Simplified Chinese UI, manual Compact, settings, DPI,
  position recovery, Shell identity, one-instance behavior, and safe shutdown.
  Do not add pet, quota, battery, activity, telemetry, or updater features.
- Capture exactly eight authentic Windows 11 screenshots from the packaged
  v0.8.0 EXE: tray, overlay, context menu, and Settings for English and for
  Simplified Chinese. No mock, source-run, or generated image is evidence.
- RC and Windows CI must build, validate, smoke-test, and upload the actual EXE
  ZIP and SHA-256. Clean Sandbox/VM evidence must remain truthfully classified.

## Execution order

```text
Design verification → TDD implementation → real onedir build → static and
runtime package smoke → installer/clean-environment evidence → eight authentic
screenshots → Quality and formal RC → exact-head Windows CI → squash merge →
merged-main RC → annotated tag and GitHub Release → reconciliation → STOP
```

## Completion gate

Do not release or mark v0.8.0 complete without all required code, package,
installer, screenshot, clean-environment, RC, CI, merge, tag, Release, and
state-reconciliation evidence. The approved detailed design and implementation
plan are `docs/superpowers/specs/2026-07-12-v0.8.0-productization-menu-design.md`
and `docs/superpowers/plans/2026-07-12-v0.8.0-productization-menu.md`.

## STOP rule

After v0.8.0 reconciliation, do not begin another version or product feature
without Tom's next approved Goal.
