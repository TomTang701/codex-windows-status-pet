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
- Updated evidence: the real v0.8.0 ZIP lifecycle smoke now proves mutex
  acquisition, PyInstaller parent/child process-tree ownership, native
  duplicate-instance dialog detection, genuine dialog-button confirmation,
  first-instance survival, and normal cleanup. Core Quality evidence is green
  (191 tests plus document, version, dependency, compile, privacy, inventory,
  and startup checks); UI modules were exercised individually, with content-fit
  layout tests and the 25-step DPI probe separately confirmed green.
- Next exact action: perform clean-environment installer verification and
  capture the eight authentic packaged-runtime screenshots. The current `.build`
  EXE test instance must first exit through its tray because the build staging
  root is intentionally protected from in-use deletion.
- Blocker: `The no-frame Tk tool window cannot be enumerated by available Windows
  UI automation. Tom must open its tray Settings window (or otherwise expose a
  targetable product window) for authentic overlay/menu/settings screenshot
  capture; physical screenshot and clean-environment evidence remain unproven.`
