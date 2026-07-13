# ACTIVE VERSION BRIEF — v0.8.0 Windows Productization and Menu Unification

## Baseline and target

- Latest released product: `v0.8.0` at `788f870bceb3d457e4b0708fa3620637092b5808`.
- Active candidate: none.
- v0.8.0 is tagged and published; it is the current product baseline.

## Approved outcome

v0.8.0 packages the existing Windows application as a checksum-verified,
per-user onedir install; adds a safe installer/uninstaller and Start Menu entry;
unifies localized tray/overlay menu semantics; and supplies truthful packaged
Windows 11 evidence in English and Simplified Chinese.

## Protected contracts

Keep the v0.7.1 quota, activity, localization, manual Compact, settings, DPI,
position recovery, Shell identity, one-instance, threading, and shutdown
contracts. No new product feature, automatic startup, background updater,
telemetry, token reader, third-party quota endpoint, or Codex-core change is in
scope.

## Current release gate

`RELEASED / RECONCILED. Packaged runtime, installed lifecycle, six authentic
screenshots, formal RC, exact-head Windows CI, merged-main RC, tag, and GitHub
Release are proven. Windows Sandbox, clean VM, and cross-user coverage remain
approved non-blocking limitations, not passing evidence. No implementation scope
is active.`
