# Execution State

- Program Goal: `ACTIVE — v0.8.0 Windows Productization and Menu Unification`.
- Released baseline: `v0.7.1` at `e45c457361d0ac3592e7d1e20671bc54f690661e`.
- Active candidate: `v0.8.0` on `feat/v0.8.0-productization-menu`.
- Current phase: `packaged artifact, installer, and CI/RC verification`.
- Completed evidence: shared menu model RED/GREEN; versioned PyInstaller onedir
  ZIP and SHA-256 static validation; real packaged EXE launch on Windows 11;
  source-instance collision now gives an explicit notification rather than a
  silent second-launch exit.
- Known limitation: Windows UI automation cannot enumerate the no-frame tool
  window in this environment, so authentic packaged screenshots and full visual
  menu evidence remain pending; no substitute screenshot is permitted.
- Next exact action: implement packaged-runtime lifecycle smoke and installer
  verification, then update RC/CI and release-facing documentation.
- Blocker: `None for implementation; physical screenshot and clean-environment
  evidence remain unproven.`
