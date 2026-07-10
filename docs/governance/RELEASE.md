# Release

## Gates

Before a release, automated checks, required physical rows, version-source consistency, bilingual parity, sensitive-file scan, clean-environment startup, changelog, known issues, and rollback instructions must be complete. Current physical blockers are reported by `scripts/check_release_readiness.py`.

## Version and rollback

Use Semantic Versioning. Keep application, manifest, changelog, package, artifact, and diagnostic versions aligned. Record the previous stable version, configuration compatibility, reinstall path, downgrade limits, and backup/restore path.

Substantial changes use focused commits and are pushed only after `scripts/run_release_checks.py` and `git diff --check` pass. The remote owner must remain `TomTang701`.
