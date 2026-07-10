---
document_id: COMPATIBILITY-MATRIX
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: docs/quality/COMPATIBILITY_MATRIX.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 30
---
# Windows Compatibility Matrix

**Status:** Living test record  
**Rule:** A simulated or headless result never replaces a physical Windows result.

| ID | Area | Coverage | Status | Blocking | Evidence / next action |
|---|---|---|---|---|---|
| WIN10-DEFERRED | Windows version | Windows 10 | Deferred | No | Outside current release scope; support is not claimed. |
| WIN11-X64 | Windows version | Windows 11 Home x64 10.0.26200 | Physical pass | Yes | 2026-07-10 host probe and launcher/overlay start passed. |
| DISPLAY-1 | Displays | Single monitor | Partial | Yes | Geometry tests pass; physical single-monitor record remains. |
| DISPLAY-2 | Displays | Two monitors | Physical pass | Yes | [2026-07-10 topology record](test-records/2026-07-10-win11-dual-monitor.md); `(4150,1248)` remains supported. |
| COORD-NEGATIVE | Coordinates | Negative virtual coordinates | Automated pass | No | Display API tests cover negative coordinates. |
| COORD-LARGE | Coordinates | Large secondary coordinate `(4151,1248)` | Physical pass | No | Overlay and context menu were observed on the secondary monitor. |
| TASKBAR-BOTTOM | Popup | Normal Windows 11 bottom taskbar | Physical pass | Yes | Bottom taskbar and corner placement were physically observed. |
| TASKBAR-ALT | Popup | Top, left, and right geometry | Automated pass | No | Pure geometry tests cover alternate work areas; unsupported registry changes are not required. |
| POPUP-FIRST-CLICK | Popup | First click | Physical pass | No | First click opened settings during the secondary-monitor test. |
| SETTINGS-RESIZE | Settings | Width/height and proportional resize | Automated pass | No | Window Size API tests cover free, proportional, bounded, and invalid factors. |
| INPUT-PASTE | Settings | Digit-only entries and interval 1–10 | Automated pass | No | Validation fixtures reject malformed paste and clamp bounds. |
| CONFIG-BOM | Settings | UTF-8 BOM JSON | Automated pass | No | Configuration API accepts UTF-8 and UTF-8-BOM fixtures. |
| QUOTA-DISPLAY | Quota display | Complete Reset Credit expiry | Physical pass | Yes | [2026-07-10 status-row record](test-records/2026-07-10-win11-reset-credit-status-rows.md) shows complete `HH:MM M/D` in the saved 330x138 window. |
| LIFECYCLE-HIDE | Lifecycle | Hidden overlay remains running | Physical pass | No | Hide removed the overlay while `pythonw.exe` remained alive. |
| TRAY-RESTORE | Lifecycle | Tray show after hide | Physical pass | Yes | Hide then Show restored the overlay on the secondary monitor. |
| DPI-MIXED | DPI | Mixed scaling | Deferred | No | Automated geometry coverage exists; mixed-DPI physical evidence is outside the v0.3.0 claim. |
| DISPLAY-RECONNECT | Displays | Disconnect and reconnect | Partial | Yes | Required when practical on the available dual-monitor host. |
| WORKAREA-RUNTIME | Taskbar | Runtime work-area change | Automated pass | No | Runtime recovery paths are covered without requiring unsupported taskbar layouts. |
| COMPACT-HOVER | Compact mode | Idle shrink and hover expand | Partial | Yes | Pure state tests pass; physical idle/hover record remains. |
| CLEAN-ENV | Dependencies | Fresh local Windows 11 venv | Automated pass | Yes | 2026-07-10 fresh venv installed requirements, ran tests, and passed package smoke. |
| SOAK-8H | Reliability | Eight-hour soak | Deferred | No | Useful future reliability evidence, not a v0.3.0 physical requirement. |
| QUALITY-GATE | Automated gate | Documents, compile, tests, package | Automated pass | No | Daily Quality passes and does not itself grant release approval. |
| SINGLE-INSTANCE | Launcher | Repeated launch | Physical pass | Yes | Two launches produced one overlay process and no persistent CMD window. |
| STARTUP-CLEAN | Startup cleanup | Legacy shortcut audit | Physical pass | No | Startup audit reports `clean: true`. |

## Release gate

Do not mark the product release-ready until all rows marked `Pending` have either a physical Windows result or an explicitly documented environment limitation approved by the maintainer.
