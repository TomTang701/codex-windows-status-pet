---
document_id: CHANGELOG
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: CHANGELOG.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Changelog

## Unreleased

- Fixed Reset Credit expiry display so valid future expirations retain local `HH:MM M/D`, while the primary 5h reset remains time-only; added bounded provider-shape parsing and presentation regressions.
- Added typed configuration load status and blocked every automatic save when a future or malformed schema is read; only an explicit Restore Defaults and Save action re-enables persistence.
- Split daily non-strict quality checks from strict release-candidate checks, changed compilation to recursive `compileall`, and added tag, artifact, checksum, changelog, physical-readiness, and rollback gates.
- Activated the Engineering Standard as a required-for-release, highest-precedence repository standard.
- Added enforced document front matter, manifest identity/version checks, review-age policy, required-release validation, and orphan Active-document detection.
- Strengthened bilingual parity checks for API names, versions, stable test/table IDs, fence languages, document metadata, and configuration schema references.
- Replaced the completion-heavy roadmap with future-only Now, Next, Later, Blocked, and Out of scope sections.
- Expanded architecture, testing, security, contribution, and release standards and added five bilingual architecture decision records.
- Split alternate taskbar edges into separate physical gates and added monitor reconnect, runtime work-area change, and eight-hour soak release blockers.
- Defined Windows 11 x64 with the normal bottom taskbar as the current support target; deferred Windows 10 and alternate-edge physical testing outside v0.3.0 blockers.
- Reorganized documentation into governance, architecture, product, quality, operations, and archive layers with a manifest-driven bilingual gate.
- Added repository, configuration, architecture, testing, release, security, installation, troubleshooting, and contribution guides.
- Added a manifest validator to the automated release checks; the suite now passes 88 tests and 17 registered bilingual pairs.
- Added an internal Markdown-link validator to the release checks so document moves cannot silently leave broken navigation.
- Added a validated settings backup sidecar and a context-menu action to restore the previous settings snapshot.
- Strengthened runtime window recovery to correct taskbar-partial placements and re-check topology changes periodically while preserving legal secondary-monitor coordinates within DPI rounding tolerance.
- Added dated physical test-record storage and linked the current Windows 11 dual-monitor topology evidence from the compatibility matrix.
- Extracted the main Tk window into `scripts/ui/main_window.py` while retaining `scripts/codex_status_pet.py` as a stable launcher and import facade.
- Updated package smoke and compile gates to validate the modular main-window version source and entry point.
- Added a dedicated version-source consistency gate for the manifest, main window, app-server client, and changelog.
- Added a high-confidence sensitive-file and secret-material scan to the release checks.
- Added an offline dependency gate that validates requirements, minimum versions, and imports before tests and packaging.
- Documented the tested Python/runtime baseline, x64 scope, pending Windows 10 coverage, and unsigned-binary behavior.
- Made notification-area shutdown explicitly idempotent and added a repeated-stop regression test.
- Expanded Activity API coverage for multiple active sessions, recent completion, malformed lines, and file-stat races.
- Added configuration schema v1 migration, legacy-file normalization, and safe fallback for unknown future versions.
- Added transactional settings sessions: Apply previews runtime values, Save persists them, and Close restores the opening snapshot.
- Added shared integer validation that supports typing negative coordinates while rejecting malformed pasted values.
- Added reversible percentage resize sessions; plus and minus scale width and height symmetrically.
- Split Activity and Quota refreshes into independent single-flight channels with stale-generation and shutdown guards.
- Added strict quota parsing, typed quota-domain models, and last-good/stale state tracking.
- Added delayed compact-state transitions, hover/activity expansion, edge anchoring, and nearest-work-area recovery for disconnected displays.
- Removed unreachable legacy native context-menu code after the tested popup implementation.
- Added Windows GitHub Actions quality gates and a package metadata/smoke ZIP check.
- Corrected plugin metadata author/developer attribution to `Zixuan Tang`.
- Extracted the context-menu Tk adapter from the main application module without changing its behavior contract.
- Extracted the transactional settings-dialog Tk adapter without changing Apply/Save/Close semantics.
- Extracted the notification-area icon adapter while keeping all actions on the Tk-owned queue.
- Extracted local Codex CLI discovery and app-server stdio JSON-RPC transport from the UI composition module.
- Added a copyable diagnostic summary menu action with an explicit no-token/no-content data boundary.
- Extracted status text/color formatting into a Tk-independent presentation API.
- Recorded the latest Windows 11 dual-monitor launcher and single-instance physical evidence in the compatibility matrix.
- Added a non-blocking release-readiness report that enumerates the physical gates still blocking v0.3.0.
- Removed the stale Windows Startup shortcut that targeted the former `.agents` copy; the current repository does not install an automatic startup entry.
- Recorded a successful isolated-venv dependency install, 65-test run, and package smoke check; clean-machine startup remains distinct.
- Added a report-only startup audit to detect known legacy Codex Status Pet entries without modifying unrelated startup items.
- Added the startup audit to the automated release-check output; the current host reports no legacy entry.
- Extended startup auditing to detect legacy names and paths in Run/RunOnce registry values.
- Added taskbar-edge diagnostics to `probe_display.py`; the current host records a bottom taskbar without inferring other edges.
- Added the active development roadmap and synchronized Chinese translation.
- Added validated window dimensions, scale mode, and 1–10 second refresh interval settings.
- Added popup work-area placement and pure quota date/earliest-expiry formatting APIs.
- Added a dedicated single-flight refresh scheduler API with bounded delay tests.
- Added a structural parity checker for six English/Chinese document pairs.
- Added a pure quota health-status API and healthy/caution/critical overlay colors.
- Added opt-in idle compaction with hover expansion; the default remains expanded.
- Ensured showing the overlay from a compact state expands it before settings or tray recovery.
- Added a tray lifecycle policy API for action allowlisting and single-scheduled recovery.
- Extracted free/proportional window resizing into a dedicated tested API.
- Added a bilingual compatibility matrix with explicit physical-test release gates.
- Added a local-only quota provider normalization API with an explicit no-token boundary.
- Added a reproducible automated release-gate runner that keeps physical checks separate.
- Added Git/GitHub change discipline to the bilingual development and API specifications.
- Fixed settings loading for UTF-8 BOM files commonly produced by Windows editors and PowerShell.
- Added regression coverage for bottom-right popup placement, secondary monitors, and quota formatting.

## 0.2.0 - 2026-07-10

- Added isolated configuration, activity, runtime, diagnostics, and test-boundary APIs.
- Replaced process-killing singleton startup with named-mutex ownership and added durable diagnostics logging.
- Hardened configuration normalization, activity timeout handling, and the PowerShell launcher path/process check.
- Replaced the unreliable native popup path with a first-click-testable Tk popup adapter.
- Removed plan-step text from the overlay; the second line now always shows only the active conversation count.
- Added stale-process cleanup plus a named mutex so repeated launches leave at most one overlay and tray icon.
- Reworked the overlay context menu to execute on the first click and close immediately.
- Added a Windows notification-area integration with show, hide, settings, and exit actions.
- Switched the launcher and Startup shortcut to `pythonw.exe` to avoid a persistent console window.
- Added persistent opacity, colors, font size, topmost, lock, and multi-monitor X/Y settings.
- The legacy implementation replaced tool-call counts with activity count; the current UI contract displays only active conversation count.
- Fixed hidden-window state recovery and preserved virtual-desktop coordinates.
- Fixed context-menu command dispatch and main-thread Tk scheduling.
- Added bilingual README, file specification, and changelog documents.

## 0.1.0 - 2026-07-09

- Initial Windows external companion implementation.
- Added local Codex app-server rate-limit polling and session activity inference.
- Added a draggable desktop overlay and basic settings menu.
