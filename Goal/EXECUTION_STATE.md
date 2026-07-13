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
  window in this environment. This does not invalidate visual evidence because
  authentic maintainer-provided packaged screenshots now cover every required
  language/view combination; no substitute or generated screenshot was used.
- Primary-display screenshot attempt: the packaged EXE was normalized to
  `(100,100)`, 100% Window Size, 100% opacity, expanded mode, and all five
  rows enabled. Its real PyInstaller parent/child EXE processes remained alive,
  but Windows UI automation still enumerated no overlay window. This is recorded
  as a tool limitation, not a product defect; no shell-identity change will be
  made for screenshot tooling. The authentic maintainer-provided overlay and
  context-menu captures now satisfy the four affected language/view combinations.
- Screenshot evidence: maintainer-provided packaged-EXE captures now supply all
  six required views at `docs/assets/readme/en/` and `docs/assets/readme/zh-CN/`.
  The companion `docs/assets/tray-icon.png` is an authentic tray capture used
  only for icon discoverability, not as a duplicate formal screenshot gate.
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
- Installed-lifecycle evidence: on 2026-07-12, the real v0.8.0 artifact
  completed fresh install, Start Menu shortcut creation, installed EXE startup,
  test-owned reinstall, normal uninstall settings preservation, purge uninstall,
  and unrelated `.codex` sentinel preservation on this physical Windows host.
  A detached PowerShell supervisor recorded child `ExitCode = 0`; the smoke's
  structured result recorded `passed: true`. Final boundary checks found no
  installed EXE, mutex, install root, or shortcut, and restored the pre-run
  settings SHA-256 unchanged.
- Formal RC evidence: the 2026-07-12 serial detached-supervisor run recorded
  `ExitCode = 0` and `release_candidate_approved: true`; Quality, release
  build, static package smoke, packaged runtime smoke, README screenshots,
  strict compatibility, and whitespace all passed against the fresh v0.8.0
  artifact (`12c6c14d5cc54ce794d81fdf1108dc7906a50b8fb30c055eb02f039b373b0743`).
- Next exact action: complete final local diff and sensitive-data review, then
  obtain current explicit remote-write authorization before pushing the branch
  for exact-head GitHub Windows CI.
- Blocker: no local technical blocker. Exact-head GitHub CI is pending a remote
  branch push and is not claimed locally.
- CI investigation: PR #38 heads `306e6b4` and `0e630e9` both passed formal
  RC but failed the clean-runner installed lifecycle smoke. The second run
  proved that explicitly selecting Windows PowerShell 5.1 was insufficient:
  its command line was correct, but `Get-FileHash` itself was unavailable.
  The installer now computes the same fail-closed SHA-256 digest through the
  .NET cryptography API and does not depend on that optional cmdlet. Focused
  installer/lifecycle RED/GREEN tests and a fresh real local artifact lifecycle
  run passed. Next action: push this narrow compatibility correction and verify
  a new exact-head Windows workflow.
