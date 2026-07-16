# Active Version Brief: v1.0.0

## Release identity

- Product version: `1.0.0`
- Baseline: `v0.9.1` packaged EXE release
- Branch: `feat/signal-hud-settings-ui-isolated`
- Target: stable source-based release and verified PR into `main`

## User-visible scope

Keep the four-row Signal HUD, five stable logical row identities, compact
percentage battery, 5-hour/Weekly bars, Reset Credit, bilingual settings and
menus, scaling/position/lifecycle behavior, local app-server boundary, and the
accepted Windows Shell identity behavior.

## Deployment scope

The v1.0.0 product ZIP contains source, hidden launch/install/uninstall scripts,
requirements-runtime.txt, manifest schema 2, and the canonical ICO. It contains
no application EXE, bundled Python, PyInstaller `_internal`, tests, or docs.

Install uses compatible Python 3.10+ in this order: Codex bundled Python,
`py.exe`, then PATH `python.exe`. Pillow and pystray are installed only into
`runtime-packages`. Repair and upgrade recreate Desktop and Start Menu
shortcuts; uninstall removes them while preserving settings unless purge is
requested.

## Required release evidence

- Source ZIP and checksum validation.
- Python discovery fallback tests and private dependency installation.
- Shortcut/icon and hidden-launcher verification.
- v0.9.1 EXE-to-v1.0.0 source upgrade, repair, rollback, uninstall, and purge.
- One final Quality run and one final local RC.
- Exact-head PR CI, merge-main CI, v1.0.0 tag/Release, latest install, and
  pinned same-version repair.
