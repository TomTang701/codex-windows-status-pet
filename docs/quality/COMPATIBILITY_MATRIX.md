# Windows Compatibility Matrix

**Status:** Living test record  
**Rule:** A simulated or headless result never replaces a physical Windows result.

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| Windows version | Windows 10 | Deferred / Not claimed / Non-blocking | Outside the current Windows 11 x64 support declaration; future evidence may expand support but does not block current releases. |
| Windows version | Windows 11 Home 10.0.26200 (build 26200) | Physical pass | 2026-07-10 host probe via `Win32_OperatingSystem`; launcher and overlay were manually started. |
| Displays | Single monitor | Automated + partial physical | Geometry API tests pass; physical single-monitor run still needs a saved screenshot. |
| Displays | Two monitors | Physical pass | [2026-07-10 topology record](test-records/2026-07-10-win11-dual-monitor.md); `DISPLAY1`/`DISPLAY2` probe completed; virtual desktop is `0,0-4480,1434`, work areas are `0,0-2048,1104` and `2560,354-4480,1386`; secondary coordinate `(4150,1248)` remains supported. |
| Coordinates | Negative virtual coordinates | Automated | `Display API` intersection and placement tests cover negative coordinates. |
| Coordinates | Large secondary coordinate `(4151,1248)` | Physical pass | Overlay and context menu were observed on the secondary monitor. |
| Popup | Four corners and taskbar work area | Automated + partial physical | Current physical probe reports the primary taskbar at the bottom (`0,1380-2560,1440`); geometry tests pass; top/left/right taskbar-edge matrix remains pending. |
| Popup | First click | Physical pass | First click on settings opened the dialog during the secondary-monitor test. |
| Settings | Width/height and proportional resize | Automated | `Window Size API` tests cover free, proportional, bounded, and invalid-factor cases. |
| Settings | Digit-only entries and interval 1–10 | Automated | Configuration and scheduler tests cover malformed and bounded values; manual paste test remains pending. |
| Settings | UTF-8 BOM JSON from Windows editors | Automated pass | Configuration API accepts UTF-8 and UTF-8-BOM fixtures without losing coordinates. |
| Lifecycle | Hidden overlay remains running | Physical pass | Hide action removed the overlay while `pythonw.exe` remained alive. |
| Lifecycle | Tray show after hide | Physical pass | Windows keyboard notification-area path (`Win+B` → Apps) opened the tray menu; Hide then Show restored the overlay to secondary coordinate `(4150,1248)`. |
| DPI | 100% / 125% / 150% / 200% | Automated partial | Current physical probe observed 96 DPI on both monitors; simulated 96/120/144/192 DPI paths pass; physical mixed-DPI monitor run remains pending. |
| Compact mode | Idle shrink and hover expand | Automated partial | Pure mode API passes; physical run accepted the BOM-enabled setting and preserved `(4150,1248)` but the current Codex session was active, so idle shrink/hover expansion was not observed. |
| Dependencies | Bundled runtime and fallback requirements | Automated partial | 2026-07-10 temporary venv installed `requirements.txt`, ran 65 tests and package smoke successfully; Windows CI also passed; a separate clean Windows machine startup remains pending. |
| Automated gate | Document parity, compilation, and unit tests | Pass | `scripts/run_release_checks.py` passed; this gate intentionally excludes physical Windows checks. |
| Launcher | Root `start_codex_status_pet.cmd`, repeated launch | Physical pass | 2026-07-10 two consecutive launches produced one actual `pythonw.exe` overlay process and no persistent CMD window; command-line self-match was excluded from the process count. |
| Startup cleanup | Former `Codex Status Pet.lnk` | Physical pass | 2026-07-10 inspected Startup folder and shortcut target; removed the shortcut pointing to the obsolete `.agents\plugins\plugins\codex-windows-status-pet` copy. `startup_audit.py` now reports `clean: true`; no current project startup entry remains. |

## Release gate

Windows 11 x64 is the supported platform. Do not mark the product release-ready until every blocking `Pending` or `partial` row has a physical Windows result or an explicitly documented environment limitation approved by the maintainer. Rows explicitly marked `Non-blocking` are reported but excluded from the executable blocker set.
