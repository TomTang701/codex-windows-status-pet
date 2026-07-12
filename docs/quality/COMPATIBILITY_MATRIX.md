# Windows Compatibility Matrix

**Status:** Living test record  
**Rule:** A simulated or headless result never replaces a physical Windows result.

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| Windows version | Windows 10 | Deferred / Not claimed / Non-blocking | Outside the current Windows 11 x64 support declaration; future evidence may expand support but does not block current releases. |
| Windows version | Windows 11 Home 10.0.26200 (build 26200) | Physical pass | 2026-07-10 host probe via `Win32_OperatingSystem`; launcher and overlay were manually started. |
| Displays | Single monitor | Physical pass | On 2026-07-10 the maintainer authorized and confirmed the single-monitor run. `DisplaySwitch.exe /internal` reported one `2048x1152` display with work area `(0,0)-(2048,1104)`; the root launcher stabilized at one project process; extended two-monitor mode was restored afterward. |
| Displays | Two monitors | Physical pass | [2026-07-10 topology record](test-records/2026-07-10-win11-dual-monitor.md); `DISPLAY1`/`DISPLAY2` probe completed; virtual desktop is `0,0-4480,1434`, work areas are `0,0-2048,1104` and `2560,354-4480,1386`; secondary coordinate `(4150,1248)` remains supported. |
| Coordinates | Negative virtual coordinates | Automated | `Display API` intersection and placement tests cover negative coordinates. |
| Coordinates | Large secondary coordinate `(4151,1248)` | Physical pass | Overlay and context menu were observed on the secondary monitor. |
| Popup | Bottom taskbar and monitor work areas | Physical pass | The 2026-07-10 physical probe reports the primary taskbar at the bottom (`0,1380-2560,1440`); the overlay and menu remained inside the detected two-monitor work areas. |
| Popup | Top, left, and right taskbar edges | Deferred / Not claimed / Non-blocking | These taskbar placements are not part of the v0.4.0 physical support claim; geometry API tests remain regression evidence only. |
| Popup | First click | Physical pass | First click on settings opened the dialog during the secondary-monitor test. |
| Settings | Canonical scale and downgrade geometry | Automated | `Window Scale API` and configuration tests cover 80–200% proportional metrics, malformed values, legacy inference, bounds, and schema-1 downgrade fields. |
| Settings | Digit-only entries and interval 1–10 | Automated | Input-validation, configuration, and scheduler tests cover typing/paste candidates, malformed values, and bounds. |
| Settings | UTF-8 BOM JSON from Windows editors | Automated pass | Configuration API accepts UTF-8 and UTF-8-BOM fixtures without losing coordinates. |
| Lifecycle | Hidden overlay remains running | Physical pass | Hide action removed the overlay while `pythonw.exe` remained alive. |
| Lifecycle | Tray show after hide | Physical pass | Windows keyboard notification-area path (`Win+B` → Apps) opened the tray menu; Hide then Show restored the overlay to secondary coordinate `(4150,1248)`. |
| DPI | 100% / 125% / 150% / 200% | Approved limitation / Non-blocking | The physical host has two 96-DPI monitors, and simulated 96/120/144/192-DPI paths pass. Mixed-DPI physical certification is unavailable in this environment and is not claimed for v0.4.0. |
| Compact mode | Idle shrink and hover expand | Physical pass | On 2026-07-10 the maintainer confirmed genuine idle shrink and hover expansion in the running application; pure mode API regression tests also pass. |
| Window scale | 80% / 100% / 150% / 200% unified geometry and typography | Windows host runtime pass | [2026-07-10 v0.4.0 scale record](test-records/2026-07-10-v0.4.0-window-scale-validation.md); real Tk geometry/fonts/wrap/padding, five rows, Reset Credit date, menu, drag/lock, Hide/Show, Compact/Expand, and temporary-file restart persistence passed at all four scales. |
| v0.4.1 content and errors | All 25 scale steps; tray/quota failure paths | Pass | [2026-07-11 v0.4.1 correctness record](test-records/2026-07-11-v0.4.1-correctness-validation.md) retains the invalidated 96-DPI result, reproduces the production 120-DPI failure, and records the replacement production-order probe passing all 25 steps. Error-path integration remains green. |
| v0.4.2 release verification | Quality, RC, compatibility, CI, and host-fact classification | Pass | [2026-07-11 v0.4.2 verification record](test-records/2026-07-11-v0.4.2-autonomous-verification.md); 23 facts classified with one authority, duplicate CI/local gates consolidated, UTF-8-safe output protected, 162 tests and formal RC passed with zero blockers. |
| v0.5.0 lean core | Obsolete compatibility boundaries and quota parser path | Pass | [2026-07-11 v0.5.0 lean-core record](test-records/2026-07-11-v0.5.0-lean-core.md); four production modules removed, quota privacy/malformed behavior moved to the parser authority, 159 behavior/release tests and formal RC passed with zero blockers. |
| v0.5.1 runtime geometry | Long-lived settings/lifecycle transitions; 80-200% at DPI 96/120 | Automated Windows host pass | [2026-07-11 v0.5.1 investigation](test-records/2026-07-11-v0.5.1-runtime-geometry-investigation.md); the v0.5.0 cold-fit/runtime-clip transition is locked as a RED, and one positioned-HWND DPI authority keeps all five rows fitted across 50 DPI/scale combinations and 15 lifecycle transitions. |
| v0.5.3 Shell identity | Desktop/tray visibility with no ordinary application-window identity | Automated Windows host pass | [2026-07-11 v0.5.3 investigation](test-records/2026-07-11-v0.5.3-shell-identity-investigation.md); real root HWND RED/GREEN proves `WS_EX_TOOLWINDOW=true`, `WS_EX_APPWINDOW=false`, owner `0`, and lifecycle persistence. The launcher retains one process and the Windows app inventory does not enumerate the overlay as an ordinary application window. |
| Dependencies | Bundled runtime and fallback requirements | Approved limitation / Non-blocking | A fresh Python 3.12 venv installed only `requirements.txt`, passed 127 tests, Quality, package smoke, and repeated-launch smoke; Windows CI also passed. A separate clean Windows machine is unavailable and is not claimed as physically tested. |
| Automated Quality | Document parity, compilation, and unit tests | Pass | `scripts/run_quality_checks.py` passed; Quality intentionally makes no release-readiness decision. |
| Launcher | Root `start_codex_status_pet.cmd`, repeated launch | Physical pass | 2026-07-10 two consecutive launches produced one actual `pythonw.exe` overlay process and no persistent CMD window; command-line self-match was excluded from the process count. |
| Startup cleanup | Former `Codex Status Pet.lnk` | Physical pass | 2026-07-10 inspected Startup folder and shortcut target; removed the shortcut pointing to the obsolete `.agents\plugins\plugins\codex-windows-status-pet` copy. `startup_audit.py` now reports `clean: true`; no current project startup entry remains. |

## Release gate

Windows 11 x64 is the supported platform. Do not mark the product release-ready until every blocking `Pending` or `partial` row has a physical Windows result or an explicitly documented environment limitation approved by the maintainer. Rows explicitly marked `Non-blocking` are reported but excluded from the executable blocker set.
