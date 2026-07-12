# ACTIVE VERSION BRIEF — v0.8.0 Windows Productization and Menu Unification

## Baseline and target

- Latest released product: `v0.7.1` at `e45c457361d0ac3592e7d1e20671bc54f690661e`.
- Active candidate: `v0.8.0`; it is not released, tagged, or published.
- v0.7.1 remains the product baseline until all v0.8.0 release gates pass.

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

`ACTIVE — implementation and evidence gathering. Do not create a v0.8.0 tag or
GitHub Release until packaged runtime, installer/clean environment, screenshots,
Quality, formal RC, and exact-head CI are all proven.`
