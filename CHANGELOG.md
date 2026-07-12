# Changelog

## Unreleased

## 0.6.2 - 2026-07-12

- Added independent, persisted visibility controls for the 5-hour, weekly, and reset-credit rows while keeping activity and conversation progress visible.
- Hidden rows leave Tk layout management instead of showing blank values; every visible row evenly shares the unchanged text region.
- Preserved truthful unavailable/stale row text, the classified weekly battery source, five stable row identities, the 10-cell battery, compact behavior, DPI recovery, Shell identity, and existing settings transactions.

## 0.6.1 - 2026-07-12

- Classify official local quota windows by the safe `windowDurationMins` metadata instead of raw `primary`/`secondary` keys.
- Keep a missing 5-hour window visibly unavailable, keep weekly data on the weekly row, and use the truthfully classified weekly window for the battery without fallback.

## 0.6.0 - 2026-07-12

- Replaced the paw with a right-side, bottom-up, 2×5 ten-segment 5H battery in expanded mode and the same complete battery in compact mode.
- Kept the five stable text rows and truthful remaining-quota text; battery fill uses the same remaining percentage, ceiling segment count, and fixed red/orange/yellow/light-green/strong-green position bands.
- Preserved mixed-DPI position recovery, Shell identity, lifecycle interactions, and all supported window-scale content-fit contracts.

## 0.5.5 - 2026-07-12

- Fixed mixed-DPI startup recovery so a saved position that is legal at its target monitor DPI is not clamped using the withdrawn bootstrap window's DPI.
- Added production-equivalent Windows regressions for secondary right, bottom, bottom-right, and interior positions, primary-edge preservation, invalid-position recovery, and drag-to-edge restart persistence on a 125% primary / 100% secondary topology.

## 0.5.3 - 2026-07-11

- Restored the overlay's Windows tool-window Shell identity after Tk's transparency lifecycle cleared it during the v0.5.1 startup sequence.
- Kept the desktop overlay and notification-area companion visible and reachable while removing ordinary application-window identity from the real top-level HWND.
- Added real-HWND regression coverage for cold start and settings, lock, Hide/Show, Compact/Expand, opacity, scale, and topmost transitions.

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

## 0.5.1 - 2026-07-11

- Stabilized one long-lived overlay across settings, lock, visibility, compact, restore, and mixed-DPI monitor transitions by deriving geometry and pixel fonts from one positioned HWND DPI authority.
- Added an automated production-equivalent regression covering all 25 scale steps at DPI 96 and 120 plus the complete runtime transition sequence that exposed the v0.5.0 clipping false positive.

## 0.5.0 - 2026-07-11

- Deleted unused quota-domain model, historical free-resize, and historical resize-session modules whose only consumers were implementation-detail tests.
- Removed the one-function quota-provider pass-through and connected the existing main-window worker directly to the strict approved-field quota parser.
- Preserved token/unknown-field exclusion, malformed-input behavior, schema-1 downgrade geometry, canonical window scaling, and all protected UI/lifecycle contracts.
- Reduced runtime production Python from 39 files / 2,742 lines to 35 files / 2,650 lines and API modules from 32 to 28; runtime dependencies remain 2.

## 0.4.2 - 2026-07-11

- Added a machine-validated inventory that classifies release facts as automated, automatable, physical-only, obsolete, or duplicate and names one authority for each fact.
- Consolidated Windows CI on the single formal Release Candidate runner instead of repeating Quality, package smoke, and whitespace as separate workflow steps.
- Separated release output into passes, blockers, and non-blocking limitations, and made child-process diagnostics UTF-8-safe on Windows.
- Replaced generic manual UI confirmation requirements with deterministic Tk/Win32/process evidence or one explicit physical-only limitation.
- Added no product runtime feature, dependency, provider, network path, polling, telemetry, configuration field, or credential access.

## 0.4.1 - 2026-07-11

- Prevented reset-credit row clipping across all 25 supported Window Size steps by scaling runtime pixel geometry, padding, gaps, and wrapping for the effective window DPI while preserving 96-DPI logical configuration values and Tk point-font sizing.
- Replaced the false-positive 96-DPI-only mapped Tk check with a production-order DPI-aware subprocess regression covering actual/requested window, status-container, and five-row geometry, including the full Reset Credit date/time row at 120 DPI.
- Routed tray and quota transport failures through the authoritative five-row presentation boundary instead of invalid Label-style configuration against `StatusRows`.
- Preserved truthful last-good/stale quota behavior, stopped displaying raw transport exception text, and restored single-scheduled tray recovery after a tray failure.
- Added no feature, dependency, provider, network path, worker, polling loop, telemetry, configuration field, or schema change.

## 0.4.0 - 2026-07-11

- Replaced the independent font-size, free width/height, plus/minus, and proportional-mode controls with one 80–200% Window Size slider while retaining opacity as the only other slider.
- Added one pure Window Scale API that derives fixed-ratio 330:138 geometry, adaptive text/paw fonts, wrapping, and spacing from a canonical percentage.
- Kept configuration schema 1, migrated legacy geometry deterministically by geometric-mean area, and persisted derived legacy fields so v0.3.2 can load a usable downgraded size.
- Preserved transactional Apply/Save/Close/Defaults behavior, five stable rows, position recovery, Hide/Show, Compact/Expand, drag/lock, menu placement, and restart persistence across 80/100/150/200 Windows host validation.
- Added no network, IPC, worker, subprocess, polling, telemetry, dependency, credential path, or Codex quota consumption for scaling.

## 0.3.2 - 2026-07-10

- Closed the declared Windows 11 x64 physical release gates with dated one- and two-monitor, launcher, single-instance, status-row, Reset Credit date, menu, hide/show, and Compact interaction evidence.
- Approved the strict Release Candidate after 127 automated tests, document and dependency gates, package smoke, and executable compatibility readiness completed successfully.
- Retained explicit non-blocking limitations for unclaimed Windows 10, alternate taskbar-edge, mixed-DPI physical, and separate clean-machine scenarios.

## 0.3.1 - 2026-07-10

- Extracted pure application, status-presentation, settings-persistence, and window-lifecycle controllers from the Tk main window.
- Preserved Activity/Quota timing and generation behavior, compact decisions, protected configuration/reset semantics, five-row rendering, and idempotent shutdown.
- Retained compatibility views for existing refresh, scheduler, compact-state, and settings-path integrations while moving ownership out of `Pet`.

## 0.3.0 - 2026-07-10

- Replaced the single multiline status Label with five persistent independently updated rows: activity, active-conversation progress, 5h quota, weekly quota, and Reset Credit.
- Added a pure stable-row snapshot contract while preserving byte-for-byte compatible joined status text for existing callers.
- Preserved compact hide/show, drag, hover, right-click, style, wrapping, refresh, and controller behavior across every row.

## 0.2.6 - 2026-07-10

- Added one focused executable document-governance check: `Goal/ACTIVE_GOAL.md` is the only normative goal and the Goal directory uses a strict allowlist.
- Required archived plans to declare archived/non-normative front matter and a valid supersession target; archived manifest entries cannot block release.
- Deliberately avoided archive parity, freshness, prose-style, review-age, and other low-value documentation gates.

## 0.2.5 - 2026-07-10

- Replaced the ambiguous automated release runner with a routine Quality runner that makes no release-readiness decision.
- Added a strict Release Candidate runner that requires Quality, package smoke, whitespace, and blocking physical compatibility checks to pass.
- Split GitHub Actions into push/PR Quality and a manual Release Candidate workflow; candidate artifacts upload only after strict approval.

## 0.2.4 - 2026-07-10

- Aligned the supported platform declaration on Windows 11 x64 across README, installation, release, product, roadmap, and compatibility documents.
- Classified Windows 10 as Deferred / Not claimed / Non-blocking instead of an executable release blocker; ARM64 and 32-bit Windows remain not claimed.
- Updated release-readiness assessment to report explicit non-blocking rows separately while retaining every pending or partial Windows 11 x64 evidence gap as a blocker.

## 0.2.3 - 2026-07-10

- Protected future-schema, malformed, non-object, and invalid configuration files from all routine save paths, including drag, hide, toggles, recovery, and shutdown.
- Added source compatibility metadata while retaining the existing settings/warnings unpacking contract.
- Allowed replacement of protected configuration only through the explicit Restore Defaults then Save flow; protected failures create no backup or partial write.

## 0.2.2 - 2026-07-10

- Fixed Reset Credit expiry normalization for approved nested provider shapes, including `credits[].expiresAt` and snake_case aliases.
- The Reset Credit row now shows the earliest future expiry as `重置 N 次 / HH:MM M/D`; missing valid expiry data remains undisplayed, and the 5h row remains time-only.
- Added bounded allowlist parsing and end-to-end regression coverage without exposing unknown or credential-like fields.

## 0.2.1 - 2026-07-10

- Simplified the overlay context menu to exactly five actions: Open Settings, Always on Top, Lock Position, Hide Window, and Exit.
- Removed the manual refresh, diagnostic-copy, and previous-settings restore entries from the context menu while preserving automatic refresh and internal diagnostic/configuration mechanisms.
- Added regression coverage for the exact menu contract, first-click single dispatch, immediate close, and Escape dismissal.

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
