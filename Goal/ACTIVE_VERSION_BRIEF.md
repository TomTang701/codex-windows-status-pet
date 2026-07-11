# ACTIVE VERSION BRIEF — v0.2.3 Configuration Write Protection

## Identity

- Version: `0.2.3`
- Branch: `release/v0.2.3-config-write-protection`
- Base: `main` at `60189601a790067394f6f0ae0b74438ff2ae7bdf`
- PR: `[v0.2.3] Protect incompatible configuration files`
- Tag: `v0.2.3`

## Product

- One-sentence outcome: A future-schema, unreadable, structurally malformed, or invalid configuration is never overwritten by routine application saves.
- User problem: Safe in-memory fallback currently becomes destructive when drag, hide, toggle, recovery, or shutdown automatically saves defaults.
- Success criteria: Unsafe source bytes remain unchanged across every ordinary save path; only an explicit Restore Defaults then Save can replace them.
- Explicit non-goals: Ordinary-menu restore actions, status rows, quota behavior, controllers, CI policy, Windows support scope, dependencies.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Backend | Yes | PASS |
| Frontend | Explicit reset flow only | PASS |
| QA/Release | Yes | PASS |
| Security/Resource | Yes | PASS |
| Visual/UI/UX | Existing controls only | PASS |

## Backend

- `load_settings` reports source status and whether ordinary persistence is safe while retaining historical two-value unpacking.
- `save_settings_atomic` re-inspects the current on-disk source immediately before every write and raises a dedicated `OSError` subtype when unsafe.
- Unsafe means unreadable/invalid JSON, non-object root, unsupported schema, or validation warnings that would lose source intent.
- Missing, valid legacy, and valid current-schema files remain writable.
- Explicit replacement requires `allow_unsafe_overwrite=True`; it is never used by automatic paths.
- Existing atomic replacement and valid backup behavior remain unchanged.
- Decision: PASS

## Frontend / UX

- Ordinary Apply remains a runtime preview and performs no disk write.
- Ordinary Save reports failure and keeps the settings dialog open when the source is protected.
- Restore Defaults marks the current settings session as an explicit reset; its subsequent Save may replace the protected source.
- No new ordinary context-menu item or button is added.
- Automatic drag/hide/toggle/recovery/shutdown saves remain blocked for protected sources.
- Decision: PASS

## QA / Release

- Preserve exact bytes for future schema, malformed JSON, non-object roots, and invalid current settings under ordinary save.
- Confirm missing, valid legacy, and valid current configurations still save atomically.
- Confirm explicit reset replaces protected content with schema v1.
- Confirm malformed/current files are not promoted to backup.
- Exercise Pet routine save and settings-dialog explicit reset dispatch.
- Run focused tests, full release checks, package smoke, `git diff --check`, Windows 11 launcher smoke.
- Decision: PASS

## Security / Resource

- No new reads beyond the pre-write local configuration inspection.
- No network, IPC, worker, timer, dependency, credential, prompt, response, or session access.
- Failed protected writes create no temporary file, backup, or mutation.
- Explicit reset is user-driven and remains atomic.
- Decision: PASS

## Scope Lock

- Allowed production files: configuration API and minimum settings/main-window integration for explicit reset and error handling.
- Allowed tests: configuration API and direct UI persistence/reset regressions.
- Allowed release files: canonical version sources, bilingual Changelog, directly affected configuration/API documentation.
- Forbidden: ordinary menu changes, status-row refactor, quota changes, controller refactor, CI/release-policy work, Windows scope changes, dependencies.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.2.4 or later is included.
