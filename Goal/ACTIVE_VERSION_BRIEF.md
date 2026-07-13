# ACTIVE VERSION BRIEF — v0.9.0 Distribution, Upgrade, and Repository Hygiene

## Baseline and target

- Latest released product: `v0.8.0` at `788f870bceb3d457e4b0708fa3620637092b5808`.
- Active candidate: local `v0.9.0` distribution candidate; not released.
- Target product: `v0.9.0`, not yet released.

## Approved outcome

v0.9.0 makes the packaged EXE and full release ZIP the normal user paths,
provides truthful authenticated PowerShell deployment for the private GitHub
Release, verifies repair/upgrade/rollback/uninstall lifecycle behavior, and
leaves `main` as the only long-lived remote branch after proven-safe cleanup.

## Protected contracts

Keep the v0.8.0 onedir architecture, local Codex quota/activity boundaries,
bilingual UI, manual Compact, settings, DPI, position recovery, Shell identity,
tray reachability, one-instance behavior, threading, and safe shutdown. Do not
add MSI/MSIX, an installer framework, in-app or background updating, telemetry,
a token reader, a third-party quota endpoint, or a Codex-core change.

## Current release gate

`ACTIVE / Phase D. v0.8.0 remains the released baseline. ZIP direct use and the
authenticated bootstrap are verified locally; the next gate is the complete
v0.8.0-to-v0.9.0 repair, rollback, and uninstall lifecycle without a second
installer.`
