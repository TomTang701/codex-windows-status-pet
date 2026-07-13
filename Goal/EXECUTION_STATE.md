# Execution State

- Program Goal: `COMPLETED — v0.9.1 Public Distribution Correction`.
- Released baseline: `v0.9.0` at `bdae1942856ffa00677e64c63142457d0f79efce`.
- Repository visibility: public; authenticated `gh` is not part of the normal-user install path.
- Current phase: `Completed — v0.9.1 released and reconciled`.
- Final target: released and reconciled `v0.9.1`.
- Phase A evidence: the public v0.9.0 product ZIP `CodexStatusPet-v0.9.0-win11-x64.zip`
  was downloaded from the GitHub Release asset URL. Its 56,291,064-byte payload matches
  the published SHA-256 `c45819da6ecf2531fa22d331dbb05319d06bf96187f499697c1e72a794eb6002`.
  The archive has one `CodexStatusPet` runtime root, contains the EXE, `_internal`, and
  release manifest, and reports version `0.9.0` with entrypoint `CodexStatusPet.exe`.
  The prohibited repository-only material audit found zero blocked files.
- Provenance finding: the v0.9.0 product Release asset is valid; the earlier CMD-launched
  ZIP observation is recorded as source-archive / product-asset confusion, not a v0.9.0
  publication defect. Published v0.9.0 history remains unchanged.
- Current implementation finding: public REST latest/pinned Release resolution now selects
  exact product assets and delegates to the existing installer; the PowerShell child-script
  result check uses `$?`, not `$LASTEXITCODE`.
- Preserved local-work boundary: the local backup branch for Tom's `53670bc` documentation
  work remains protected and is not to be overwritten, deleted, absorbed, or committed.
- Current remote state: `main` only; no open pull requests; merged-head auto-deletion enabled.
- Candidate evidence: `scripts/check_version_sources.py` passed; public bootstrap focused
  tests passed 6/6; real public v0.9.0 bootstrap smoke passed; v0.9.1 package build passed.
  Candidate ZIP SHA-256 is `8ba8ef5f1ea6cbe8ba55ea5fff52032d4bcebcd12e4c7f1b4627f013366dd327`.
- Release evidence: PR #43 merged to main at `821d58a499984bea79c7a57234920c77ff7549e1`;
  tag `v0.9.1` and public Release exist; merged-main package SHA-256 is
  `706f24bab7bc3054dd2bd410ab3ff60144972a20690796e0036568f8211ec338`; latest public
  install lifecycle passed and cleaned its temporary install root.
- Final state: remote branch list is reconciled to main only. Next action: STOP and wait
  for Tom's next approved Goal.
- Blocker: none.
- STOP only after v0.9.1 Release, reconciliation, proven-safe temporary branch cleanup,
  final remote branch list exactly `main`, and final verification.
