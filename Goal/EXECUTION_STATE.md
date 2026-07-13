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
- Primary-display screenshot attempt: the packaged EXE was normalized to
  `(100,100)`, 100% Window Size, 100% opacity, expanded mode, and all five
  rows enabled. Its real PyInstaller parent/child EXE processes remained alive,
  but Windows UI automation still enumerated no overlay window. This is recorded
  as a tool limitation, not a product defect; no shell-identity change will be
  made for screenshot tooling. Authentic maintainer-provided overlay and context
  menu captures are required for the four affected language/view combinations.
- Approved release-gate adjustment: clean Windows 11 VM, Windows Sandbox, and
  cross-user automation coverage are unavailable non-blocking environment
  limitations. They are not passed or claimed. A fresh GitHub Windows runner
  will provide clean lifecycle automation where practical, but is not physical
  Windows 11 client evidence unless its operating system is independently
  verified.
- Updated evidence: the real v0.8.0 ZIP lifecycle smoke now proves mutex
  acquisition, PyInstaller parent/child process-tree ownership, native
  duplicate-instance dialog detection, genuine dialog-button confirmation,
  first-instance survival, and normal cleanup. Core Quality evidence is green
  (191 tests plus document, version, dependency, compile, privacy, inventory,
  and startup checks); UI modules were exercised individually, with content-fit
  layout tests and the 25-step DPI probe separately confirmed green.
- Next exact action: run the safe installed-lifecycle smoke on a fresh Windows
  runner, capture six authentic packaged-runtime screenshots on the primary
  display at 100% Window Size and opacity, then run RC and exact-head CI. The
  current `.build` EXE test instance must first exit through its tray because
  the build staging root is intentionally protected from in-use deletion.
- Blocker: `The no-frame Tk tool window cannot be enumerated by available Windows
  UI automation. Tom must provide the specific authentic packaged overlay/menu
  screenshots that cannot be captured after primary-display normalization;
  physical screenshot evidence remains unproven.`
