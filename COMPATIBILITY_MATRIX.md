# Windows Compatibility Matrix

**Status:** Living test record  
**Rule:** A simulated or headless result never replaces a physical Windows result.

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| Windows version | Windows 10 | Pending | Run the launcher and full UI smoke test on a Windows 10 machine. |
| Windows version | Windows 11 Home 10.0.26200 (build 26200) | Physical pass | Current host version was collected with `Win32_OperatingSystem`; launcher and overlay were manually started. |
| Displays | Single monitor | Automated + partial physical | Geometry API tests pass; physical single-monitor run still needs a saved screenshot. |
| Displays | Two monitors | Physical pass | Current `DISPLAY1` and `DISPLAY2` probe completed; work areas are `0,0-2048,1104` and `2560,354-4480,1386`; secondary coordinate `(4150,1248)` displayed the overlay. |
| Coordinates | Negative virtual coordinates | Automated | `Display API` intersection and placement tests cover negative coordinates. |
| Coordinates | Large secondary coordinate `(4151,1248)` | Physical pass | Overlay and context menu were observed on the secondary monitor. |
| Popup | Four corners and taskbar work area | Automated + partial physical | Geometry tests pass; physical taskbar-edge matrix remains pending. |
| Popup | First click | Physical pass | First click on settings opened the dialog during the secondary-monitor test. |
| Settings | Width/height and proportional resize | Automated | `Window Size API` tests cover free, proportional, bounded, and invalid-factor cases. |
| Settings | Digit-only entries and interval 1–10 | Automated | Configuration and scheduler tests cover malformed and bounded values; manual paste test remains pending. |
| Settings | UTF-8 BOM JSON from Windows editors | Automated pass | Configuration API accepts UTF-8 and UTF-8-BOM fixtures without losing coordinates. |
| Lifecycle | Hidden overlay remains running | Physical pass | Hide action removed the overlay while `pythonw.exe` remained alive. |
| Lifecycle | Tray show after hide | Physical pass | Windows keyboard notification-area path (`Win+B` → Apps) opened the tray menu; Hide then Show restored the overlay to secondary coordinate `(4150,1248)`. |
| DPI | 100% / 125% / 150% / 200% | Automated partial | Simulated 96/120/144/192 DPI paths pass; physical mixed-DPI monitor run remains pending. |
| Compact mode | Idle shrink and hover expand | Automated partial | Pure mode API passes; physical run accepted the BOM-enabled setting and preserved `(4150,1248)` but the current Codex session was active, so idle shrink/hover expansion was not observed. |
| Dependencies | Bundled runtime and fallback requirements | Automated partial | Current bundled runtime compiles and tests; clean-machine installation remains pending. |
| Automated gate | Document parity, compilation, and unit tests | Pass | `scripts/run_release_checks.py` passed; this gate intentionally excludes physical Windows checks. |
| Launcher | Root `start_codex_status_pet.cmd`, repeated launch | Physical pass | Two consecutive launches produced one `pythonw.exe` overlay process and no console window. |

## Release gate

Do not mark the product release-ready until all rows marked `Pending` have either a physical Windows result or an explicitly documented environment limitation approved by the maintainer.
