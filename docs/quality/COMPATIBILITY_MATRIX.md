# Windows Compatibility Matrix

简体中文: [中文版本](COMPATIBILITY_MATRIX.zh-CN.md)

**Status:** Living test record  
**Rule:** A simulated or headless result never replaces a physical Windows result.

## v0.8.0 Adjusted release evidence

Windows Sandbox, a separate clean Windows 11 VM, and cross-Windows-user desktop
automation are approved non-blocking environment limitations in the current
context. They are not passed or claimed. Packaged EXE lifecycle evidence from
the current Windows host remains client-runtime evidence; GitHub Windows runner
installation results are clean runner automation and are not physical Windows
11 client evidence unless that operating system is independently verified.

## v0.9.0 distribution and lifecycle evidence

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| v0.9.0 ZIP direct use | Extract complete onedir ZIP and run `CodexStatusPet.exe` without source runtime | Automated Windows host pass | Isolated packaged-runtime smoke passed with `PYTHONPATH` removed and no installed state or Start Menu shortcut. |
| v0.9.0 authenticated deployment | Historical private GitHub Release resolution, ZIP/SHA acquisition, and installer delegation | Historical pass | Superseded by the v0.9.1 public REST bootstrap correction; v0.9.0 history is unchanged. |
| v0.9.0 installed lifecycle | Upgrade from v0.8.0, repair, rollback, normal uninstall, and purge uninstall | Physical Windows host and GitHub Windows CI pass | The focused lifecycle smoke preserves settings bytes and unrelated `.codex` data, removes test residue, and passed locally plus exact-head CI for PR #40. |
| v0.9.0 release | Merged-main RC, annotated tag, Release ZIP and SHA-256 sidecar | Pass | RC passed on `bdae1942856ffa00677e64c63142457d0f79efce`; tag and public GitHub Release target the same commit. |

## v0.9.1 public distribution correction

v0.9.1 replaces authenticated `gh` acquisition with public REST Release metadata
and exact `browser_download_url` assets. The release gate passed after packaging,
publication, and verification from the public latest and pinned bootstrap paths.

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| v0.9.1 public distribution | Public latest/pinned bootstrap, exact product ZIP/SHA/install assets, and existing installer delegation | Pass | PR #43 exact-head Windows CI passed; merged main `821d58a`; tag/Release `v0.9.1`; latest public install lifecycle passed; product ZIP SHA-256 `706f24bab7bc3054dd2bd410ab3ff60144972a20690796e0036568f8211ec338`. |

## v0.9.2-beta.1 Signal HUD candidate

| Area | Coverage | Status | Evidence / next action |
|---|---|---|---|
| v0.9.2-beta.1 UI regression | Expanded four-row HUD, compact percentage battery, unified quota text color, progress-bar color, and Settings preview/menu coverage | Automated Windows host pass | Quality UI suite and screenshot checks pass on the isolated branch. |
| v0.9.2-beta.1 Shell close paths | Settings Save, Close, window-manager close, topmost restoration, and delayed Shell identity normalization | Automated HWND lifecycle pass; physical observation pending | Run fresh physical taskbar observations before accepting a 1.0 replacement of `main`; this beta branch does not claim that evidence. |

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
| DPI | 125% primary / 100% secondary startup recovery | Automated Windows host pass | The physical host now has a 120-DPI primary and 96-DPI secondary. The v0.5.5 production-equivalent suite proves legal secondary edge coordinates survive startup and restart; simulated 96/120/144/192-DPI paths remain regression coverage. |
| Compact mode | Idle shrink and hover expand | Physical pass | On 2026-07-10 the maintainer confirmed genuine idle shrink and hover expansion in the running application; pure mode API regression tests also pass. |
| Window scale | 80% / 100% / 150% / 200% unified geometry and typography | Windows host runtime pass | [2026-07-10 v0.4.0 scale record](test-records/2026-07-10-v0.4.0-window-scale-validation.md); real Tk geometry/fonts/wrap/padding, five rows, Reset Credit date, menu, drag/lock, Hide/Show, Compact/Expand, and temporary-file restart persistence passed at all four scales. |
| v0.4.1 content and errors | All 25 scale steps; tray/quota failure paths | Pass | [2026-07-11 v0.4.1 correctness record](test-records/2026-07-11-v0.4.1-correctness-validation.md) retains the invalidated 96-DPI result, reproduces the production 120-DPI failure, and records the replacement production-order probe passing all 25 steps. Error-path integration remains green. |
| v0.4.2 release verification | Quality, RC, compatibility, CI, and host-fact classification | Pass | [2026-07-11 v0.4.2 verification record](test-records/2026-07-11-v0.4.2-autonomous-verification.md); 23 facts classified with one authority, duplicate CI/local gates consolidated, UTF-8-safe output protected, 162 tests and formal RC passed with zero blockers. |
| v0.5.0 lean core | Obsolete compatibility boundaries and quota parser path | Pass | [2026-07-11 v0.5.0 lean-core record](test-records/2026-07-11-v0.5.0-lean-core.md); four production modules removed, quota privacy/malformed behavior moved to the parser authority, 159 behavior/release tests and formal RC passed with zero blockers. |
| v0.5.1 runtime geometry | Long-lived settings/lifecycle transitions; 80-200% at DPI 96/120 | Automated Windows host pass | [2026-07-11 v0.5.1 investigation](test-records/2026-07-11-v0.5.1-runtime-geometry-investigation.md); the v0.5.0 cold-fit/runtime-clip transition is locked as a RED, and one positioned-HWND DPI authority keeps all five rows fitted across 50 DPI/scale combinations and 15 lifecycle transitions. |
| v0.5.3 Shell identity | Desktop/tray visibility with no ordinary application-window identity | Automated Windows host pass | [2026-07-11 v0.5.3 investigation](test-records/2026-07-11-v0.5.3-shell-identity-investigation.md); real root HWND RED/GREEN proves `WS_EX_TOOLWINDOW=true`, `WS_EX_APPWINDOW=false`, owner `0`, and lifecycle persistence. The launcher retains one process and the Windows app inventory does not enumerate the overlay as an ordinary application window. |
| v0.5.5 mixed-DPI startup recovery | 125% primary / 100% secondary legal edge-position restart preservation | Automated Windows host pass | [2026-07-12 v0.5.5 investigation](test-records/2026-07-12-v0.5.5-mixed-dpi-startup-position-investigation.md); production-equivalent RED traced the first incorrect clamp to bootstrap 120-DPI recovery metrics, and GREEN preserves secondary right, bottom, bottom-right, and interior coordinates while retaining invalid-position recovery. |
| v0.6.0 battery and layout | Five text rows plus a 2×5 / ten-cell battery; compact complete battery; 80–200% and DPI 96/120 content fit | Automated Windows host pass | Focused presentation and BatteryView RED/GREEN, all 25 scale steps, DPI probes, lifecycle regressions, formal RC, and exact-head Windows CI passed for v0.6.0 PR #25. The battery uses the same authoritative remaining-quota presentation as the `primary_5h` text. |
| Dependencies | Bundled runtime and fallback requirements | Approved limitation / Non-blocking | A fresh Python 3.12 venv installed only `requirements.txt`, passed 127 tests, Quality, package smoke, and repeated-launch smoke; Windows CI also passed. A separate clean Windows machine is unavailable and is not claimed as physically tested. |
| Automated Quality | Document parity, compilation, and unit tests | Pass | `scripts/run_quality_checks.py` passed; Quality intentionally makes no release-readiness decision. |
| Launcher | Root `start_codex_status_pet.cmd`, repeated launch | Physical pass | 2026-07-10 two consecutive launches produced one actual `pythonw.exe` overlay process and no persistent CMD window; command-line self-match was excluded from the process count. |
| Startup cleanup | Former `Codex Status Pet.lnk` | Physical pass | 2026-07-10 inspected Startup folder and shortcut target; removed the shortcut pointing to the obsolete `.agents\plugins\plugins\codex-windows-status-pet` copy. `startup_audit.py` now reports `clean: true`; no current project startup entry remains. |
| v0.8.0 package | PyInstaller onedir EXE, manifest, notices, SHA-256, and denylist | Automated pass | `python scripts/build_release.py` and `python scripts/package_smoke_test.py` produced and validated the versioned EXE ZIP. |
| v0.8.0 packaged lifecycle | GUI EXE first launch, duplicate-instance preservation, and normal close | Automated Windows host pass | `python scripts/packaged_runtime_smoke.py` passed against the real versioned EXE ZIP; no source process stood in for the artifact. |
| v0.8.0 installed lifecycle | Fresh install, Start Menu entry, test-owned reinstall, normal uninstall preservation, and purge safety | Physical Windows host pass | 2026-07-12 real artifact run completed under a detached PowerShell supervisor with child `ExitCode = 0` and smoke result `passed: true`; final checks found no installed EXE, mutex, install root, or shortcut, and restored the original settings SHA-256 unchanged. A future GitHub runner result is clean lifecycle automation, not physical Windows 11 client evidence unless its OS is independently verified. |
| v0.8.0 clean VM/Sandbox/cross-user | Separate clean Windows 11 VM, Sandbox, or cross-user desktop automation | Approved limitation / Non-blocking | These environments are unavailable in the current execution context. They are not passed or claimed, and no VM/cross-user infrastructure will be added solely for v0.8.0. |
| v0.8.0 README evidence | Three packaged English and three packaged Simplified Chinese product views | Physical Windows host pass | Maintainer-provided screenshots from the real packaged EXE show the normalized expanded overlay, overlay context menu, and Settings window in both languages; `python scripts/check_readme_screenshots.py` validates the exact six files and README language mapping. |

## Release gate

Windows 11 x64 is the supported platform. Do not mark the product release-ready until every blocking `Pending` or `partial` row has a physical Windows result or an explicitly documented environment limitation approved by the maintainer. Rows explicitly marked `Non-blocking` are reported but excluded from the executable blocker set.
