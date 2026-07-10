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

| ID | Area | Coverage | Status | Evidence / next action | Blocking |
|---|---|---|---|---|---|
| WIN-10 | Windows version | Windows 10 | Pending | Run the launcher and full UI smoke test on a Windows 10 machine. | Yes |
| WIN-11 | Windows version | Windows 11 Home 10.0.26200 (build 26200) | Physical pass | 2026-07-10 host probe via `Win32_OperatingSystem`; launcher and overlay were manually started. | No |
| DISPLAY-1 | Displays | Single monitor | Partial | Geometry API tests pass; physical single-monitor run still needs a dated record. | Yes |
| DISPLAY-2 | Displays | Two monitors | Physical pass | [2026-07-10 topology record](test-records/2026-07-10-win11-dual-monitor.md); secondary coordinate `(4150,1248)` remains supported. | No |
| COORD-NEGATIVE | Coordinates | Negative virtual coordinates | Automated pass | `Display API` intersection and placement tests cover negative coordinates. | No |
| COORD-LARGE | Coordinates | Large secondary coordinate `(4151,1248)` | Physical pass | Overlay and context menu were observed on the secondary monitor. | No |
| TASKBAR-EDGES | Popup | Four corners and taskbar work area | Partial | Bottom taskbar is physically observed and geometry tests pass; top/left/right edges remain pending. | Yes |
| POPUP-FIRST-CLICK | Popup | First click | Physical pass | First click on settings opened the dialog during the secondary-monitor test. | No |
| SETTINGS-RESIZE | Settings | Width/height and proportional resize | Automated pass | `Window Size API` tests cover free, proportional, bounded, and invalid-factor cases. | No |
| INPUT-PASTE | Settings | Digit-only entries and interval 1–10 | Partial | Automated malformed/boundary fixtures pass; manual illegal-paste evidence remains pending. | Yes |
| CONFIG-BOM | Settings | UTF-8 BOM JSON from Windows editors | Automated pass | Configuration API accepts UTF-8 and UTF-8-BOM fixtures without losing coordinates. | No |
| QUOTA-DISPLAY | Quota display | Primary, weekly, and Reset Credit expiry contract | Partial | Automated format/parser/snapshot tests pass; expanded-mode physical visibility remains pending. | Yes |
| LIFECYCLE-HIDE | Lifecycle | Hidden overlay remains running | Physical pass | Hide removed the overlay while `pythonw.exe` remained alive. | No |
| TRAY-RESTORE | Lifecycle | Tray show after hide | Physical pass | Hide then Show restored the overlay to secondary coordinate `(4150,1248)`. | No |
| DPI-MIXED | DPI | 100% / 125% / 150% / 200% | Partial | Simulated DPI paths pass; physical mixed-DPI evidence remains pending. | Yes |
| COMPACT-HOVER | Compact mode | Idle shrink and hover expand | Partial | Pure state tests pass; physical idle shrink/hover expansion remains pending. | Yes |
| CLEAN-MACHINE | Dependencies | Bundled runtime and fallback requirements | Partial | Temporary venv and Windows CI pass; separate clean Windows startup remains pending. | Yes |
| QUALITY-GATE | Automated gate | Documents, compile, tests, and package | Automated pass | `scripts/run_quality_checks.py` passes and intentionally does not grant release approval. | No |
| SINGLE-INSTANCE | Launcher | Root launcher and repeated launch | Physical pass | Two launches produced one overlay process and no persistent CMD window. | No |
| STARTUP-CLEAN | Startup cleanup | Former legacy shortcut | Physical pass | Startup audit reports `clean: true`; no current project startup entry exists. | No |

## Release gate

Do not mark the product release-ready until all rows marked `Pending` have either a physical Windows result or an explicitly documented environment limitation approved by the maintainer.
