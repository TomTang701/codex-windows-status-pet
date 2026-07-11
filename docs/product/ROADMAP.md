# Codex Windows Status Pet Development Plan

**Status:** Active roadmap  
**Baseline:** `docs/architecture/API_SPEC.md`, `docs/archive/audits/2026-07-09-test-error-report.md`, and the Windows portion of [quota-float](https://github.com/change-42-yhmm/quota-float)

## Current progress

- **Completed:** P0/P1 reliability and truthful quota work, v0.3.2 Windows stabilization, and the v0.4.0 unified-scale implementation boundary: one canonical percentage, schema-1 legacy migration, exact two-slider settings UI, and coherent main/Compact metrics.
- **Verified:** 88 automated tests, 17 manifest-registered bilingual document pairs, Windows 11 launcher smoke test, secondary-monitor menu/settings path, and keyboard-driven tray hide/show recovery.
- **Automated gates:** GitHub Actions runs routine Quality on pushes/PRs; a separate manual workflow runs strict Release Candidate checks and uploads a candidate artifact only on success.
- **Application modularization:** Context menu, settings dialog, tray adapter, and main window now live in `scripts/ui/`; Codex discovery/transport, safe diagnostics, and status presentation live in `scripts/api/`; `scripts/codex_status_pet.py` is a stable launcher facade.
- **Pending physical evidence:** v0.4.0 scale validation at 80/100/150/200; mixed-DPI and separate clean-machine certification remain explicit environment limitations.
- **Release decision:** v0.3.2 is released. v0.4.0 remains a candidate until full Quality, strict RC, Windows scale evidence, remote CI, main retest, and tag gates pass.
- **Explicitly out of scope:** access-token readers, third-party quota endpoints, telemetry, and modifying Codex core or built-in pet files.

## Product objective

Provide a reliable Windows companion that remains reachable on any monitor, reports Codex activity and quota data without inventing values, and exposes settings that are validated, persisted, and recoverable.

## Delivery order

### P0 — reliability and reachability

1. Place the context menu completely inside the work area of the monitor containing the pointer, including bottom-right, secondary monitors, negative virtual coordinates, and taskbar reservations.
2. Centralize validation for coordinates, window dimensions, colors, font size, opacity, booleans, and refresh interval.
3. Make refresh scheduling single-flight, cancellable, and independent from the Tk event thread.
4. Preserve the existing safe single-instance mutex; never kill an unrelated process.

**Exit criteria:** headless geometry and validation tests pass; the first menu click invokes exactly once; no menu is clipped in the four corners; invalid configuration falls back field-by-field.

### P1 — settings and truthful quota display

1. Add persisted width and height.
2. Add free resize and proportional plus/minus controls.
3. Add a digit-only refresh interval setting, clamped to 1–10 seconds.
4. Display weekly quota and the earliest future reset-credit expiry as local `HH:MM M/D`, with no leading zero.
5. Keep Save, Apply, Restore Defaults, and Close semantics distinct.

**Exit criteria:** settings survive restart; Apply does not close; Save closes after persistence; Close discards the draft; date formatting has deterministic tests.

### P2 — product polish inspired by quota-float

1. Add explicit loading, stale, unavailable, signed-out, and healthy/caution/critical states.
2. Consider compact-orb and hover-expand modes after P0/P1 stability.
3. Strengthen window-state recovery for monitor disconnect/reconnect and taskbar topology changes. Runtime periodic re-evaluation is now implemented; physical topology matrix evidence remains pending.

The current local app-server provider remains the default. Token-reading or external quota endpoints are out of scope until a separate security review and provider contract are approved.

### P3 — documentation and release quality

English files are canonical; Chinese files are synchronized translation copies in the same commit. Every major or performance change requires an API specification update, focused regression tests, a changelog entry, and a compatibility result. `scripts/check_doc_parity.py` reads `docs/document_manifest.json` and checks registered document pairs for structural drift.

## API boundaries

| API | Responsibility |
|---|---|
| `ConfigAPI` | Normalize, load, atomically save, back up, and restore preferences. |
| `InputValidationAPI` | Enforce digit-only fields and typed ranges. |
| `SettingsSessionAPI` | Separate persisted, runtime, draft, and opening settings snapshots. |
| `DisplayGeometryAPI` | Enumerate work areas and place/clamp popup rectangles. |
| `WindowScaleAPI` | Derive fixed-ratio geometry, typography, wrapping, and spacing from one canonical percentage and infer legacy scale. |
| `WindowSizeAPI` | Retain historical free/proportional transformations as a compatibility utility with no normal UI consumer. |
| `ResizeSessionAPI` | Retain historical reversible steps as a compatibility utility with no normal UI consumer. |
| `QuotaFormatAPI` | Select reset dates and format truthful local text. |
| `QuotaStatusAPI` | Classify quota health without network or UI dependencies. |
| `DisplayModeAPI` | Decide opt-in idle compaction and calculate compact geometry. |
| `CompactStateAPI` | Delay idle compaction, expand on activity/hover, and preserve edge anchors. |
| `WindowRecoveryAPI` | Recover only genuinely off-screen windows to the nearest current work area. |
| `TrayLifecycleAPI` | Validate tray actions and single-schedule recovery. |
| `RefreshSchedulerAPI` | Run one quota refresh at a time with a bounded user interval. |
| `RefreshControllerAPI` | Keep Activity and Quota refresh channels independent and generation-safe. |
| `QuotaProviderAPI` | Adapt local or future providers to one normalized snapshot schema. |
| `QuotaParseAPI` | Accept only approved quota fields and explicit naming aliases. |
| `QuotaStateAPI` | Track loading, last-good, stale, signed-out, and unavailable quota states. |
| `ModelsAPI` | Hold typed quota-domain values outside the UI. |
| `DiagnosticsAPI` | Persist startup, worker, UI, and tray failures. |

No performance feature may be added directly to UI code without its own API boundary and compatibility test.

## Compatibility matrix

Test Windows 11 x64 with one and two monitors, negative and large virtual coordinates, 100/125/150/200% DPI, each taskbar edge, hidden/shown, locked/unlocked, topmost/not-topmost, malformed settings, refresh values 1/10/0/11/empty/non-digit, network timeout, stale responses, missing reset dates, and repeated launches. Windows 10 evidence is deferred and may expand future support but is non-blocking. Maintain results in `docs/quality/COMPATIBILITY_MATRIX.md`.

## Documentation rule

Update the English canonical file first, translate the paired Chinese file in the same commit, and keep headings, API names, version numbers, test IDs, and tables structurally aligned. Run `python scripts/check_doc_parity.py` before committing; the check verifies structure without requiring literal line equality.

## Git and GitHub change discipline

Commit and push every substantial, verified change promptly instead of accumulating unrelated work. A substantial change includes a new API, user-visible behavior, settings-schema change, performance change, security-boundary change, launcher change, or compatibility-result update.

Before committing:

1. Run `python scripts/run_quality_checks.py`; this is not release approval.
2. Run `git diff --check`.
3. Update the English and Chinese specification/changelog pair.
4. Inspect the staged file list and commit with a focused message.
5. Push the approved branch to the configured GitHub owner; never silently change the remote or author identity.

Small documentation-only corrections may be grouped, but must still pass document parity and be committed promptly. Never mix unrelated user changes into a project commit.
