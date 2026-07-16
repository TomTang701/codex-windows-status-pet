# Release

简体中文: [中文版本](RELEASE.zh-CN.md)

## Gates

Routine `run_quality_checks.py` provides fast automated code-health feedback and
never approves a release. `run_release_candidate_checks.py` is the single formal
automated release command. It executes Quality, the source ZIP build, static
ZIP/SHA validation, installed-source lifecycle smoke, README screenshot
validation, strict compatibility readiness, and whitespace exactly once. It
reports passes, blockers, and limitations separately. The canonical fact
classification and authority are recorded in `docs/quality/verification-inventory.json`.

The release runtime dependency policy is exact and private: `requirements-runtime.txt`
pins Pillow 12.2.0 and pystray 0.19.5 under the installed product directory.

## Supported runtime declaration

- Supported OS: Windows 11 x64 is physically tested and claimed. Windows 10 is Deferred, Not claimed, and Non-blocking.
- Installed runtime: the supported installed product is source-based and uses a
  discovered x64 Python 3.10+ runtime with Tkinter, pip, and pythonw.exe. The
  discovery order is Codex bundled Python, `py.exe`, then PATH `python.exe`.
  Pillow and pystray remain private to the install directory.
- Architecture: x64 Windows is the tested architecture; ARM64 and 32-bit Windows are not claimed.
- Unsigned behavior: the project does not ship a signed binary; Windows SmartScreen or policy warnings may appear and must be documented for any packaged release.

## Version and rollback

Use Semantic Versioning. Keep application, manifest, changelog, package, artifact, and diagnostic versions aligned. Record the previous stable version, configuration compatibility, reinstall path, downgrade limits, and backup/restore path.

Substantial changes use focused commits and are pushed only after `scripts/run_quality_checks.py` and `git diff --check` pass. The remote owner must remain `TomTang701`. A green Quality result must never be described as formal release approval.

The current candidate workflow uploads `CodexStatusPet-v…-win11-x64.zip` and its `.sha256`
sidecar, not a source ZIP. The release notes must disclose the unsigned binary,
per-user installation path, settings-preservation behavior, Codex CLI dependency,
and any clean-environment evidence classification.
