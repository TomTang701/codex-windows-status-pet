# Execution State

- Program Goal: `ACTIVE — v0.9.0 Distribution, Upgrade, and Repository Hygiene`.
- Released baseline: `v0.8.0` at `788f870bceb3d457e4b0708fa3620637092b5808`.
- Active candidate: local `v0.9.0` distribution candidate; not released.
- Current phase: `Phase D — script-driven reinstall / repair / upgrade / uninstall lifecycle`.
- Final target: released and reconciled `v0.9.0`.
- Active Goal branch: `goal/v0.9.0-distribution-hygiene`, created from verified
  `origin/main` at `c7bc05e7ef9e77cb6c06632ccc3afb1901fe4547`.
- Initial repository audit (2026-07-12): the configured remote is
  `TomTang701/codex-windows-status-pet`; GitHub reports a private repository,
  default branch `main`, no open pull requests, and automatic deletion of merged
  head branches disabled. Phase E must classify every non-main remote branch
  before any deletion and either safely enable the setting or record the exact
  maintainer action required.
- Preserved local-work boundary: the original `main` worktree remains untouched
  with Tom's divergent local documentation commit `53670bc`; it is not a v0.9.0
  branch and must not be overwritten, absorbed, or treated as a safe deletion.
- v0.8.0 release evidence remains valid baseline evidence unless a v0.9.0 change
  explicitly invalidates it: exact-head Windows CI, merged-main RC, published
  ZIP and SHA-256 sidecar, and physical installed lifecycle coverage passed.
- Phase A evidence: README, README.zh-CN.md, and paired installation documents
  now designate the complete ZIP and `CodexStatusPet.exe` as the normal user
  path, prohibit extracting the EXE alone, and restrict the repository `.cmd`
  launcher to development, debugging, source verification, and release
  engineering. Private-release acquisition is stated truthfully; no anonymous
  download command is claimed before Phase C implements it.
- Phase B evidence: the current onedir ZIP was rebuilt in the v0.9.0 worktree
  and exercised through the existing packaged-runtime smoke with a temporary
  isolated user profile. The extracted EXE ran from its own directory with
  `PYTHONPATH` removed, acquired/released the mutex, showed the duplicate notice,
  and exited normally. Existing settings remained readable with their seeded
  semantics intact; no installed runtime or Start Menu shortcut was created.
- Phase C evidence: `scripts/install_release.ps1` uses an authenticated existing
  GitHub CLI session to resolve a stable private Release, download the matching
  ZIP, SHA-256 sidecar, and existing `install.ps1`, and delegate verification and
  installation to that installer. It has no token reader or embedded secret.
  The fake-GitHub Windows smoke passed, and the live private-v0.8.0 probe reached
  the truthful missing-bootstrap-asset failure without creating installed state.
- Phase D is active: the lifecycle smoke now requires an explicitly supplied
  different previous release, verifies v0.8.0-to-v0.9.0 manifest provenance,
  byte-for-byte settings preservation, same-version repair, failed replacement
  rollback, normal uninstall, and purge uninstall. The installer snapshots
  settings before it asks an old runtime to close, then restores those bytes at
  the transaction boundary. Focused unit tests pass.
- CI now downloads the published v0.8.0 ZIP and sidecar using GitHub Actions'
  ephemeral `github.token`, then passes it explicitly to the v0.9.0 lifecycle
  smoke. This is CI-only release-artifact acquisition, not a new user credential
  path.
- Next exact action: complete the local v0.8.0-to-v0.9.0 lifecycle run with a
  definitive exit code, then update the bilingual Quick Install, Upgrade, and
  Uninstall documentation before the formal RC.
- STOP only after `v0.9.0` release, authoritative reconciliation, proven-safe
  remote branch cleanup, and final verification.
- Blocker: none.
