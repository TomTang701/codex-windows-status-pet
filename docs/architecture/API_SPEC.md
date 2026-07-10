---
document_id: API-SPEC
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/architecture/API_SPEC.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# API and Test Boundary Specification

## Purpose

The Windows companion is split into small, testable APIs so failures can be isolated without
starting Tk or the notification area. Each API has one responsibility and must remain usable from
headless tests.

| API | Module | Responsibility | Test boundary |
|---|---|---|---|
| Configuration API | `scripts/api/config_api.py` | Validate, normalize, classify schema state, load, atomically save, back up, and restore settings. | Temporary JSON files and future/malformed write guards; no Tk. |
| Activity API | `scripts/api/activity_api.py` | Read Codex session JSONL and derive active/recent status with unchanged-file caching. | Synthetic JSONL directory; injectable clock and cache. |
| Runtime API | `scripts/api/runtime_api.py` | Own the named Windows single-instance mutex. | Windows mutex acquisition/release. |
| Diagnostics API | `scripts/api/diagnostics_api.py` | Capture uncaught main-thread and worker exceptions when `pythonw.exe` hides the console. | Temporary log path and synthetic exception. |
| Display API | `scripts/api/display_api.py` | Query virtual-desktop bounds/DPI and test coordinate intersection without clamping legal monitor coordinates. | Simulated 96/144/192 DPI and virtual bounds. |
| Input Validation API | `scripts/api/input_validation_api.py` | Validate signed and unsigned integer candidates and submitted values for settings fields. | Empty, partial negative, malformed, pasted, and bounded integer fixtures. |
| Settings Session API | `scripts/api/settings_session_api.py` | Keep persisted, runtime, draft, and opening settings distinct across Apply, Save, Close, and Defaults. | Apply/Save/Close transaction tests without Tk. |
| Popup Geometry API | `scripts/api/display_api.py` | Select a monitor work area and place a popup fully inside it. | Four corners, secondary monitor, negative coordinates, and taskbar work areas. |
| Quota Format API | `scripts/api/quota_format_api.py` | Select the earliest future credit expiry and format primary resets as local `HH:MM` or weekly/Reset Credit expiry as `HH:MM M/D`. | Epoch/ISO input, invalid/past expiry values, missing dates, and no-leading-zero formatting. |
| Quota Status API | `scripts/api/quota_status_api.py` | Classify valid quota windows as healthy, caution, critical, or unavailable. | Boundary percentages and malformed windows. |
| Display Mode API | `scripts/api/display_mode_api.py` | Decide opt-in idle compaction and calculate compact geometry. | Opt-in, active, hovered, and malformed-size cases. |
| Compact State API | `scripts/api/compact_state_api.py` | Delay idle compaction, expand on activity/hover, and preserve edge anchors. | Idle delay, activity, hover, blockers, and edge geometry. |
| Window Recovery API | `scripts/api/window_recovery_api.py` | Preserve legal monitor coordinates, correct taskbar-partial windows, and recover off-screen windows to the nearest work area. | Negative/secondary coordinates, DPI rounding tolerance, taskbar coverage, disconnected displays, and clamping. |
| Window Size API | `scripts/api/window_size_api.py` | Transform free or proportional width/height changes with bounds. | Free, proportional, bounded, and invalid-factor cases. |
| Resize Session API | `scripts/api/resize_session_api.py` | Apply reversible percentage steps from an opening base size. | Exact plus/minus symmetry and bounded dimensions. |
| Quota Provider API | `scripts/api/quota_provider_api.py` | Normalize already-fetched local app-server data without reading auth or making network calls. | Valid, malformed, and credential-bearing payload fixtures. |
| Quota Parse API | `scripts/api/quota_parse_api.py` | Normalize only approved quota fields and bounded Reset Credit containers with explicit camelCase/snake_case aliases. | Scalar/list/nested expiry shapes, unknown or credential fields, invalid numbers, aliases, and missing fields. |
| Quota State API | `scripts/api/quota_state_api.py` | Retain last-good data and classify loading, ok, stale, and explicit failures. | Success recovery, recent failure, stale timeout, and no-data failures. |
| Domain Models API | `scripts/api/models_api.py` | Define typed usage-window, reset-credit, and quota-snapshot values. | Dataclass construction and type-boundary tests. |
| Tray Lifecycle API | `scripts/api/tray_lifecycle_api.py` | Validate tray actions and guarantee one recovery restart request. | Action allowlist, visibility policy, duplicate failure, and shutdown cases. |
| Refresh Scheduler API | `scripts/api/refresh_scheduler_api.py` | Use a validated interval and one in-flight worker at a time. | Repeated refresh calls and interval clamp fixtures. |
| Refresh Controller API | `scripts/api/refresh_controller_api.py` | Keep Activity and Quota channels independent with generation, cancellation, and shutdown guards. | Independent single-flight channels, stale generations, and shutdown callbacks. |
| Codex transport API | `scripts/api/codex_transport_api.py` | Start local app-server, perform JSON-RPC requests, and report protocol failures. | Mock subprocess/stdout response matrix. |
| UI/tray adapter | `Pet` in `scripts/ui/main_window.py` and `TrayIcon3` in `scripts/ui/tray_adapter.py` | Translate API results into Tk and tray actions. | Windows UI/manual interaction tests only. |
| Context Menu UI | `scripts/ui/context_menu.py` | Own first-click-safe popup construction, placement, command dispatch, and close behavior. | Existing first-click/settings popup integration test and physical corner checks. |
| Settings Dialog UI | `scripts/ui/settings_dialog.py` | Own settings controls, validation binding, transaction actions, and reachable-dialog placement. | Settings session tests and Windows secondary-monitor interaction checks. |
| Status Rows UI | `scripts/ui/status_rows.py` | Render five independent labels while retaining the main-window adapter surface. | Tk adapter smoke plus pure row-contract tests. |
| Tray UI | `scripts/ui/tray_adapter.py` | Own icon construction, pystray callbacks, tray thread, and stop handling; actions return through a queue. | Tray failure, action allowlist, repeated launch, and physical show/hide checks. |
| Codex Transport API | `scripts/api/codex_transport_api.py` | Discover the local Codex CLI and perform app-server stdio JSON-RPC without UI ownership. | Configured-path discovery, stopped-process rejection, and mocked transport boundaries. |
| Diagnostic Summary API | `scripts/api/diagnostic_summary_api.py` | Produce copyable operational diagnostics while excluding credentials, prompts, responses, session contents, and raw quota. | State/path formatting and sensitive-data exclusion tests. |
| Status Snapshot API | `scripts/api/status_snapshot_api.py` | Convert approved activity/quota state into display text, color, and active-count values without Tk. | Truthful formatting, stale color, and raw-field exclusion tests. |
| Status Rows API | `scripts/api/status_rows_api.py` | Preserve stable activity, progress, primary 5h, weekly, and Reset Credit row identities independently from Tk. | Exact row order, missing-line padding, and Reset Credit full-format assertions. |
| Startup Audit | `scripts/startup_audit.py` | Read-only detection of known legacy Codex Status Pet entries in the Startup folder and Run/RunOnce registry keys. | Known legacy name/path, unrelated entry, and no-modification tests. |
| Taskbar API | `scripts/api/taskbar_api.py` | Read the current primary taskbar edge and rectangle for physical compatibility evidence. | Stable edge mapping and Windows probe output. |

## Invariants

- Configuration API never raises for malformed user JSON; `ConfigLoadResult` returns defaults, warnings, schema status, and a writable flag.
- Configuration API accepts UTF-8 and UTF-8-BOM JSON produced by common Windows editors.
- Configuration writes use a same-directory temporary file and atomic replacement.
- A successful save keeps one previous valid settings file in the `.bak` sidecar; malformed current or backup files are never promoted or restored.
- Configuration schema v1 is written on save; legacy files without a schema version are normalized. Unknown future or malformed files are read-only and cannot be overwritten by exit, drag, hide, toggles, recovery, or settings-save paths until the user explicitly selects Restore Defaults and Save.
- Activity API uses the latest session event as the inactivity clock, not only task start time.
- Runtime initialization requests per-monitor DPI awareness before creating Tk windows.
- Runtime API never kills an unrelated process to obtain the mutex.
- A settings Apply changes runtime preview only; only Save changes persisted settings.
- A settings Close restores the opening snapshot, including after an Apply preview.
- Coordinate fields accept a temporary `-` while typing but reject malformed signed integers on submit.
- Resize buttons apply the same percentage to width and height and remain reversible around the session base size.
- UI callbacks must not perform blocking app-server or filesystem work on the Tk thread.
- Tray and application shutdown operations are idempotent; repeated stop calls do not invoke a stopped backend again.
- The overlay displays only the active conversation count; plan-step text is not part of the UI contract.
- Status text uses a bounded label width so long diagnostics wrap instead of expanding past the overlay.
- Popup rectangles must be completely contained by the selected monitor work area.
- Window placement is re-evaluated during the running session so monitor disconnects and taskbar work-area changes can recover the overlay.
- Coordinates may be negative; dimensions are clamped to 180–1200 by 80–800; refresh interval is clamped to 1–10 seconds.
- The primary 5h reset uses local `HH:MM` only. Weekly and Reset Credit expiry use local `HH:MM M/D` without leading zeroes. Missing provider dates are not invented.
- The default quota provider accepts local app-server results only; it never reads auth files, sends tokens, or persists credentials.
- A major behavior or performance change requires a changelog entry, specification update, and regression test.
- The context-menu implementation has one reachable popup path; obsolete native-menu code must not remain after an unconditional return.
- Diagnostic summaries may include paths and operational states, but must never include tokens, prompts, responses, session contents, or raw quota payloads.

## Test commands

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m unittest discover -s .\tests -v
$api = Get-ChildItem .\scripts\api -Filter *.py | ForEach-Object FullName
& $py -m py_compile .\scripts\codex_status_pet.py .\scripts\ui\main_window.py $api
# Live Windows display evidence (run with the companion visible)
& $py .\scripts\probe_display.py
& $py .\scripts\check_doc_parity.py
# Reproducible automated release gate (does not replace physical checks)
& $py .\scripts\run_release_checks.py
& $py .\scripts\package_smoke_test.py
& $py .\scripts\check_release_readiness.py
```

The live probe must be rerun after connecting a monitor with a different Windows scaling setting.
Save its JSON output with the test record; a mixed-DPI result is not inferred from simulated values.

The package smoke test checks manifest/app version consistency, verified author metadata, required
launcher/docs, and creates a non-release ZIP. GitHub Actions runs these checks on Windows.
`check_release_readiness.py` is intentionally non-blocking by default and reports the physical
compatibility rows that still prevent a v0.3.0 release; use `--strict` only in a release decision.
`startup_audit.py` is also report-only by default; it never removes unrelated startup entries.

## Live Windows display evidence (run with the companion visible)

## Change classification

- **Major behavior:** menu dispatch, visibility, tray actions, single-instance policy, settings semantics, or displayed status. Requires a focused regression test and a manual Windows check.
- **Performance:** session scan duration, refresh interval, thread count, or disk-write frequency. Requires a benchmark or bounded test fixture and a note in `CHANGELOG.md`.
- **Documentation-only:** wording or examples with no runtime effect. Still requires checking English and Chinese specifications for drift.

## Git change gate

Substantial changes require automated release checks, `git diff --check`, paired English/Chinese documentation updates, an intentional focused commit, and a push to the verified repository owner. The local pre-push hook must remain enabled through `.githooks`.
