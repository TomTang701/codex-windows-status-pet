# Release

简体中文: [中文版本](RELEASE.zh-CN.md)

## Gates

Routine `run_quality_checks.py` provides fast automated code-health feedback and never approves a release. `run_release_candidate_checks.py` is the single formal automated release command; it executes Quality, package smoke, strict compatibility readiness, and whitespace exactly once and reports passes, blockers, and limitations separately. The canonical fact classification and authority are recorded in `docs/quality/verification-inventory.json`.

The runtime dependency policy uses minimum compatible bounds in `requirements.txt`. Quality verifies that each declaration is installed, meets its minimum version, and imports successfully; the current verified environment uses Pillow 12.2.0 and pystray 0.19.5.

## Supported runtime declaration

- Supported OS: Windows 11 x64 is physically tested and claimed. Windows 10 is Deferred, Not claimed, and Non-blocking.
- Python/runtime: Python 3.11 is the CI baseline; Python 3.12.13 is locally verified. The fallback runtime must provide `pythonw.exe` and install `requirements.txt`.
- Architecture: x64 Windows is the tested architecture; ARM64 and 32-bit Windows are not claimed.
- Unsigned behavior: the project does not ship a signed binary; Windows SmartScreen or policy warnings may appear and must be documented for any packaged release.

## Version and rollback

Use Semantic Versioning. Keep application, manifest, changelog, package, artifact, and diagnostic versions aligned. Record the previous stable version, configuration compatibility, reinstall path, downgrade limits, and backup/restore path.

Substantial changes use focused commits and are pushed only after `scripts/run_quality_checks.py` and `git diff --check` pass. The remote owner must remain `TomTang701`. A green Quality result must never be described as formal release approval.
