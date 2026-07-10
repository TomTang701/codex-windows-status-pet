---
document_id: RELEASE
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/governance/RELEASE.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Release

The active [Engineering Standard](ENGINEERING_STANDARD.md) is the highest-level authority for this release process.

## Gates

`scripts/run_quality_checks.py` is the daily push/PR gate. It runs manifest and link checks, version/sensitive/dependency/bilingual checks, recursive compilation of every Python file under `scripts`, tests, startup audit, a non-strict readiness report, and package smoke. The legacy `run_release_checks.py` name remains a compatibility alias.

`scripts/run_release_candidate_checks.py` is the formal manual/tag gate. It reruns Quality and additionally requires strict physical readiness, a matching version tag when tag-triggered, a formal changelog version, rollback guidance, a non-empty artifact, and a SHA-256 checksum. A green daily Quality result is not release approval.

Before a release, automated checks, required physical rows, version-source consistency, bilingual parity, sensitive-file scan, clean-environment startup, changelog, known issues, and rollback instructions must be complete. Current physical blockers are reported by `scripts/check_release_readiness.py --strict`.

The runtime dependency policy uses minimum compatible bounds in `requirements.txt`. The release gate verifies that each declaration is installed, meets its minimum version, and imports successfully; the current verified environment uses Pillow 12.2.0 and pystray 0.19.5.

## Supported runtime declaration

- Supported OS: Windows 11 x64 is physically tested; Windows 10 remains pending physical validation.
- Python/runtime: Python 3.11 is the CI baseline; Python 3.12.13 is locally verified. The fallback runtime must provide `pythonw.exe` and install `requirements.txt`.
- Architecture: x64 Windows is the tested architecture; ARM64 and 32-bit Windows are not claimed.
- Unsigned behavior: the project does not ship a signed binary; Windows SmartScreen or policy warnings may appear and must be documented for any packaged release.

## Version and rollback

Use Semantic Versioning. Keep application, manifest, changelog, package, artifact, and diagnostic versions aligned. Record the previous stable version, configuration compatibility, reinstall path, downgrade limits, and backup/restore path.

Substantial changes use focused commits and are pushed only after `scripts/run_quality_checks.py` and `git diff --check` pass. Formal candidates must also pass `scripts/run_release_candidate_checks.py`. The remote owner must remain `TomTang701`.

## Candidate and tag procedure

1. Choose the canonical version and update runtime, plugin manifest, changelog, diagnostics, and package sources together.
2. Run Quality, complete every blocking physical record, then run the strict Release Candidate suite.
3. Inspect the ZIP contents, checksum, dependency list, unsigned status, clean-machine evidence, known issues, and configuration downgrade limits.
4. Create tag `v<version>` only from the verified commit; the tag workflow must reproduce the same artifact checks.
5. Publish artifact and `.sha256` together with supported Windows/runtime scope and rollback instructions.

## Rollback procedure

Stop the tray process, retain the current settings file and `.bak`, reinstall the previous known-good artifact, and restart through the root launcher. If the current configuration schema is newer than the previous application supports, do not launch the old version against it; preserve the file and restore a compatible backup or explicitly reset after user confirmation. Record the withdrawn commit/tag, artifact checksum, reason, user-visible impact, and replacement version. Never rewrite old evidence or silently move a release tag.
