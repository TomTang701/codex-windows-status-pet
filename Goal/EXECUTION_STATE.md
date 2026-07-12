# Execution State

- Program Goal: `ACTIVE — v0.8.0 Windows Productization and Menu Unification`.
- Released baseline: `v0.7.1` at `e45c457361d0ac3592e7d1e20671bc54f690661e`.
- Active candidate: `v0.8.0` on `feat/v0.8.0-productization-menu`.
- Current phase: `packaged artifact, installer, and CI/RC verification`.
- Completed evidence: shared menu model RED/GREEN; versioned PyInstaller onedir
  ZIP and SHA-256 static validation; real packaged EXE launch on Windows 11;
  source-instance collision now gives an explicit notification rather than a
  silent second-launch exit; runtime smoke RED/GREEN now recognizes the normal
  PyInstaller parent EXE → GUI child EXE process tree before requesting a normal
  close.
- Known limitation: Windows UI automation cannot enumerate the no-frame tool
  window in this environment, so authentic packaged screenshots and full visual
  menu evidence remain pending; no substitute screenshot is permitted.
- Next exact action: run the packaged-runtime lifecycle smoke with no existing
  instance, then perform clean-environment installer verification and capture
  the eight authentic packaged-runtime screenshots.
- Blocker: `None for implementation; physical screenshot and clean-environment
  evidence remain unproven.`
