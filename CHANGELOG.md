# Changelog

## Unreleased

- Added transactional settings sessions: Apply previews runtime values, Save persists them, and Close restores the opening snapshot.
- Added shared integer validation that supports typing negative coordinates while rejecting malformed pasted values.
- Added reversible percentage resize sessions; plus and minus scale width and height symmetrically.
- Split Activity and Quota refreshes into independent single-flight channels with stale-generation and shutdown guards.
- Added strict quota parsing, typed quota-domain models, and last-good/stale state tracking.
- Added delayed compact-state transitions, hover/activity expansion, edge anchoring, and nearest-work-area recovery for disconnected displays.
- Removed unreachable legacy native context-menu code after the tested popup implementation.
- Added Windows GitHub Actions quality gates and a package metadata/smoke ZIP check.
- Corrected plugin metadata author/developer attribution to `Zixuan Tang`.
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
