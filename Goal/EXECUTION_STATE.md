# Execution State

- Program Goal: `ACTIVE — v0.9.0 Distribution, Upgrade, and Repository Hygiene`.
- Released baseline: `v0.8.0` at `788f870bceb3d457e4b0708fa3620637092b5808`.
- Active candidate: none.
- Current phase: `Phase B — formal ZIP direct-use verification`.
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
- Next exact action: establish a focused production-equivalent ZIP direct-use
  RED that proves the current packaged-runtime smoke does not yet cover every
  required v0.9.0 provenance and installed-state boundary, then extend the
  smallest existing packaged-runtime authority to GREEN.
- STOP only after `v0.9.0` release, authoritative reconciliation, proven-safe
  remote branch cleanup, and final verification.
- Blocker: none.
