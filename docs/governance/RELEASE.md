# Release

## Gates

Before a release, automated checks, required physical rows, version-source consistency, bilingual parity, sensitive-file scan, clean-environment startup, changelog, known issues, and rollback instructions must be complete. Current physical blockers are reported by `scripts/check_release_readiness.py`.

The runtime dependency policy uses minimum compatible bounds in `requirements.txt`. The release gate verifies that each declaration is installed, meets its minimum version, and imports successfully; the current verified environment uses Pillow 12.2.0 and pystray 0.19.5.

## Supported runtime declaration

- Supported OS: Windows 11 x64 is physically tested; Windows 10 remains pending physical validation.
- Python/runtime: Python 3.11 is the CI baseline; Python 3.12.13 is locally verified. The fallback runtime must provide `pythonw.exe` and install `requirements.txt`.
- Architecture: x64 Windows is the tested architecture; ARM64 and 32-bit Windows are not claimed.
- Unsigned behavior: the project does not ship a signed binary; Windows SmartScreen or policy warnings may appear and must be documented for any packaged release.

## Version and rollback

Use Semantic Versioning. Keep application, manifest, changelog, package, artifact, and diagnostic versions aligned. Record the previous stable version, configuration compatibility, reinstall path, downgrade limits, and backup/restore path.

Substantial changes use focused commits and are pushed only after `scripts/run_release_checks.py` and `git diff --check` pass. The remote owner must remain `TomTang701`.
