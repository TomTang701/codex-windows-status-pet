# Codex Windows Status Pet — Test Error Report

**Audit date:** 2026-07-09  
**Scope:** Windows launcher, overlay, tray icon, settings, activity detection, Codex app-server boundary, packaging, and documentation.  
**Rule for this audit:** findings only. No production fix was applied during this audit.

> Historical baseline: this report records the defects as observed on 2026-07-09. The original
> findings table is intentionally preserved for traceability; the remediation status below is the
> authoritative current-state summary and reflects subsequent implementation and testing.

## Executive summary

The product is not ready for a high-confidence release. The most visible defect remains the main
overlay context menu: the first left click does not reliably invoke the selected item. There are
also several crash, data-loss, lifecycle, and observability risks that can make the companion appear
to disappear because it runs through `pythonw.exe` without a console.

## Severity definitions

- **P0:** data loss, security boundary failure, or a release-blocking crash.
- **P1:** major user workflow failure, silent exit, duplicate process, or incorrect status.
- **P2:** recoverable functional defect or significant usability/maintenance risk.
- **P3:** documentation, polish, or low-probability edge case.

## Reproducible findings

| ID | Severity | Area | Finding | Evidence / reproduction | User impact |
|---|---|---|---|---|---|
| ERR-001 | P1 | Main context menu | The first left click on a main-window menu item is still not reliably dispatched. | Right-clicked the running overlay at virtual-desktop coordinates `(4151,1248)` and issued one left click against the settings entry. No settings window was observed. This matches the reported user behavior. Relevant code: `scripts/codex_status_pet.py:602-648`. | Refresh/settings/hide/exit may appear dead; users may click repeatedly and trigger uncertain state changes. |
| ERR-002 | P1 | Settings startup | Non-numeric or null values in the JSON settings file crash startup instead of being rejected field-by-field. | Test cases `{"alpha":"bad"}`, `{"font_size":null}`, and `{"x":"abc"}` raised `ValueError`/`TypeError` from `load_settings()` at `scripts/codex_status_pet.py:517-531`. | A damaged or manually edited config can make the window disappear with no visible error because the launcher uses `pythonw.exe`. |
| ERR-003 | P2 | Settings semantics | JSON strings such as `"topmost":"false"` are interpreted as `True` because Python applies `bool()` to a non-empty string. The same issue affects `locked`. | Test case `{"topmost":"false"}` loaded with `topmost=True` at `scripts/codex_status_pet.py:527-528`. | Settings can reopen with a state different from the value the user entered. |
| ERR-004 | P1 | PowerShell launcher | `scripts/start_pet.ps1` checks only `python.exe`, not `pythonw.exe`, when deciding whether an instance is already running. | The root CMD launcher runs `pythonw.exe` (`start_codex_status_pet.cmd:4-12`), while the PowerShell launcher filters only `Name='python.exe'` (`scripts/start_pet.ps1:7-11`). | Running the PowerShell launcher can create a second companion and duplicate tray icons. |
| ERR-005 | P1 | Single-instance lifecycle | The executable kills the existing titled companion before proving that the new instance can initialize. | `ensure_single_instance()` calls `taskkill /F` before creating the mutex (`scripts/codex_status_pet.py:36-59`). | A bad dependency, broken Codex path, or startup exception can turn a working instance into no instance. |
| ERR-006 | P2 | Process safety | Stale-process cleanup is based on image name plus window title, not a recorded process identity or executable path. | Cleanup targets every `python.exe` and `pythonw.exe` matching the exact title (`scripts/codex_status_pet.py:43-51`). | An unrelated Python application using the same title can be forcibly terminated; title reuse is not impossible. |
| ERR-007 | P1 | Activity detection | A conversation is marked inactive after ten minutes from `task_started`, even if new session records continue arriving. | The active test is `now - started <= self.stale_seconds` (`scripts/codex_status_pet.py:221-222`); `last_event_time` is collected but not used for the timeout. | Long-running Codex work can incorrectly show no active conversation. |
| ERR-008 | P2 | Activity scan robustness | `p.stat()` is executed outside the per-file `try` block while building the candidate list. A file deleted, locked, or changed during the recursive scan can abort the entire snapshot. | Candidate construction at `scripts/codex_status_pet.py:177-178` calls `p.stat()` before the guarded file read. | A transient session-file race can prevent status refresh and leave stale UI text. |
| ERR-009 | P2 | Activity scan performance | Every refresh recursively scans recent JSONL files and rereads each candidate from the beginning. There is no file index, byte offset, or session cache. | `ActivityMonitor.snapshot()` uses `rglob()` and full `readline` iteration (`scripts/codex_status_pet.py:170-219`). | Large session histories or frequent concurrent Codex activity can cause unnecessary disk I/O and delayed refreshes. |
| ERR-010 | P1 | Tray reliability | The pystray worker has no visible failure channel or restart path. If `icon.run()` fails, the main UI is not told that the tray is gone. | `TrayIcon3` starts a daemon thread directly with `self.icon.run` (`scripts/codex_status_pet.py:453-475`). | The user can lose the only reliable way to show a hidden window or exit it. |
| ERR-011 | P1 | Silent failures | The production launcher deliberately uses `pythonw.exe`, but startup exceptions, Tk callback exceptions, and pystray thread exceptions are not written to a guaranteed diagnostic log. | Root launcher uses `pythonw.exe` (`start_codex_status_pet.cmd:4-12`); only the unused legacy tray classes contain debug logging. | A crash looks like “nothing happened”; troubleshooting requires external process inspection. |
| ERR-012 | P1 | Dependency packaging | `PIL` and `pystray` are imported unconditionally, but the plugin manifest and repository do not declare or install these runtime dependencies. | Imports are at `scripts/codex_status_pet.py:14-19`; `.codex-plugin/plugin.json` has no dependency declaration or setup action. | A clean machine or refreshed runtime can fail before any window or diagnostic appears. |
| ERR-013 | P1 | Off-screen recovery | Arbitrary virtual-desktop coordinates are intentionally accepted, but there is no guaranteed visible recovery path when the configured monitor is disconnected. | `safe_position()` returns any integer pair (`scripts/codex_status_pet.py:533-538`); startup immediately applies it (`scripts/codex_status_pet.py:485-488`). | The overlay can start entirely off-screen; the user may depend on a tray settings dialog whose placement is also not explicitly controlled. |
| ERR-014 | P2 | Settings durability | Settings are written directly to the final JSON path without a temporary file, flush, replace, or backup. | `save_settings()` calls `write_text()` directly (`scripts/codex_status_pet.py:540-542`). | A crash, power loss, or simultaneous write can corrupt settings and cause later startup failure or silent defaults. |
| ERR-015 | P2 | Settings error handling | `save_settings()` is not guarded in `close()`, `hide_window()`, or drag completion. A write failure can interrupt the close/hide workflow. | Calls occur at `scripts/codex_status_pet.py:582`, `:600`, and `:831`; no exception handling surrounds them. | The user may be unable to close cleanly or may lose the last position. |
| ERR-016 | P2 | Menu lifecycle | The menu is explicitly posted and grabbed, but there is no general dismissal path for Escape, focus loss, outside click, or window destruction. `close_menu()` is only reached through a command wrapper. | Menu lifecycle is at `scripts/codex_status_pet.py:602-648`; `close_menu()` is not bound to dismissal events. | A failed first click can leave a stuck popup/grab and make the main window appear unresponsive. |
| ERR-017 | P2 | Menu exception safety | `run_and_close()` closes the menu only after the command returns successfully. If a command raises, the menu is left open. | `run_and_close()` is `command(); close_menu()` at `scripts/codex_status_pet.py:621-623`. | A refresh/settings/exit exception can reproduce the “menu does nothing” symptom and retain the grab. |
| ERR-018 | P2 | Settings validation | Text-entry conversion happens inside Tk callbacks with no validation or user-facing error state. | `sync_draft()` directly calls `float()`/`int()` (`scripts/codex_status_pet.py:709-715`). | A typo in X/Y can produce a Tk callback traceback and no visible feedback. |
| ERR-019 | P2 | Shutdown race | A delayed `after(150, ...)` callback from `show_window()` can execute after the root window has been destroyed. | The delayed lambda is scheduled at `scripts/codex_status_pet.py:571`; shutdown destroys the root at `scripts/codex_status_pet.py:835`. | Closing soon after showing/settings can produce callback exceptions or noisy hidden failures. |
| ERR-020 | P2 | Codex discovery | `find_codex()` uses ad-hoc line parsing for `config.toml` and returns the literal fallback `codex.exe`/`codex` even when no executable was verified. | Candidate parsing and fallback are at `scripts/codex_status_pet.py:62-77`. | Valid TOML layouts, quoted values, or PATH differences can make the app report a generic failure instead of locating Codex. |
| ERR-021 | P2 | App-server protocol | `_send()` does not check the response for initialization errors, and pending callbacks are mutated from the reader thread without the same lock used for insertion. | Initialization is sent and ignored at `scripts/codex_status_pet.py:101-104`; pending map access is split across `:112-135`. | Protocol failures can surface later as timeouts or race-dependent behavior. |
| ERR-022 | P3 | Coordinate/display scaling | Coordinates are treated as raw Tk geometry values with no DPI-awareness or scale conversion test. | Geometry is constructed directly at `scripts/codex_status_pet.py:488`, `:547`, and `:562`. | High-DPI or mixed-scale multi-monitor desktops may place or size the overlay incorrectly. |
| ERR-023 | P3 | UI layout | The fixed `330x138` window has no text wrapping or adaptive sizing. Long error messages and localized status strings can clip or overlap. | Fixed geometry at `scripts/codex_status_pet.py:488`; label text is not wrapped at `:502` and `:816-822`. | Small fonts, long errors, or localization changes can make information unreadable. |
| ERR-024 | P3 | Version consistency | The manifest version is `0.1.0+...`, the app-server client advertises `0.2.0`, and the changelog documents `0.2.0`. | `.codex-plugin/plugin.json`, `scripts/codex_status_pet.py:101`, and `CHANGELOG.md` disagree. | Support, cache invalidation, and bug reports can refer to different versions for the same binary. |
| ERR-025 | P3 | Documentation drift | `PRODUCT_REVIEW.md` still describes plan `N/M` display even though the runtime no longer displays plan steps. | `PRODUCT_REVIEW.md:5,13,20` conflicts with current `README.md` and `scripts/codex_status_pet.py`. | Users and maintainers can rely on a feature that no longer exists. |
| ERR-026 | P3 | Dead implementation | Two older tray implementations (`TrayIcon`, `TrayIcon2`) remain beside the active `TrayIcon3`. | `scripts/codex_status_pet.py:236-451` is not used by `Pet`, which constructs `TrayIcon3` at `:512`. | Future fixes may be applied to the wrong class; audit and maintenance cost increase. |
| ERR-027 | P3 | Launcher portability | The PowerShell launcher contains a hardcoded profile path for `tangz`, unlike the CMD launcher which uses `%USERPROFILE%`. | `scripts/start_pet.ps1:3-5`. | Other Windows users, renamed profiles, or copied installations cannot use the fallback launcher reliably. |

## Test execution record

| Test | Result | Notes |
|---|---|---|
| Python syntax compilation | PASS | Bundled Python `-m py_compile scripts/codex_status_pet.py`. |
| Bundled dependency import | PASS | `tkinter`, `PIL`, and `pystray` imported in the current machine. This does not prove clean-machine installability. |
| Repeated root CMD launch | PASS for this machine | Two launches left one titled `pythonw.exe` process and no Codex command window. This does not clear the PowerShell duplicate risk. |
| Multi-monitor coordinate observation | PASS for this machine | Running overlay window rect was `(4151,1248)-(4481,1386)`. |
| Settings type-fuzz cases | FAIL | Invalid `alpha`, `font_size`, and `x` values raised uncaught exceptions; string `"false"` was interpreted as `True`. |
| Main menu first-click behavior | FAIL | User-reported defect reproduced in the running build; a Win32 click attempt did not produce the settings window after one click. |
| Full Codex app-server/rate-limit validation | NOT COMPLETED | Requires a controlled Codex server response matrix; no production behavior was changed for this audit. |
| Clean-machine dependency/startup validation | NOT COMPLETED | Current machine already has the bundled dependencies installed. |
| Isolated virtual-environment dependency validation | PASS | A temporary venv installed `requirements.txt`; imports and all eight tests passed. This is not a separate Windows installation. |
| Current DPI/virtual-desktop probe | PARTIAL | `enable_dpi_awareness()` returned true; running window reported 96 DPI and virtual bounds `0,0,4480,1434`. No physically mixed-DPI monitor was available for the matrix. |
| Live display probe | PASS for current desktop | `scripts/probe_display.py` reported DISPLAY1 `(0,0)-(2048,1152)` and DISPLAY2 `(2560,354)-(4480,1434)`; both reported 96 DPI. The output is reusable evidence for a future mixed-DPI run. |

## Highest-priority release blockers

1. **ERR-001:** main menu first-click failure.
2. **ERR-002 / ERR-014 / ERR-015:** configuration corruption and unhandled settings I/O can make the app disappear or lose state.
3. **ERR-004 / ERR-005:** duplicate-process and startup lifecycle failures.
4. **ERR-007:** incorrect idle status for long-running Codex work.
5. **ERR-010 / ERR-011 / ERR-012:** tray/dependency failures are silent under `pythonw.exe`.

## Explicit non-actions

No production code, launcher, settings file, or runtime behavior was changed during this audit.
The only intended repository artifact from this audit is this report.

## Follow-up remediation status (2026-07-09 continuation)

The audit report above is the original baseline. In the continuation work, the following changes
were implemented and are now covered by the API/test boundary specification:

- **Addressed:** ERR-001, ERR-002, ERR-003, ERR-004, ERR-005, ERR-006, ERR-007, ERR-008, ERR-009, ERR-011, ERR-013, ERR-014, ERR-015, ERR-016, ERR-017, ERR-018, ERR-019, ERR-020, ERR-021, ERR-023, ERR-024, ERR-025, ERR-026, and ERR-027.
- **Partially addressed:** ERR-022 (per-monitor DPI awareness is requested and the current 96-DPI desktop passed the call, but mixed-scale geometry still needs a matrix).
- **Test coverage added:** ten tests in `tests/`, including first-click command invocation through the popup control, malformed settings fallback, atomic settings round-trip, long-running activity detection, stale activity rejection, malformed JSONL tolerance, unchanged-file activity caching, injected tray failure reporting, and simulated 96/144/192 DPI geometry boundaries. Physical Windows checks opened settings on the first click, closed the popup by an outside click, and restored `(4151,1248)`.
- **Still open:** ERR-022 mixed-scale geometry validation on physically different-DPI monitors.

This status section records progress only; it does not claim the product is fully release-ready.

## Follow-up implementation status (2026-07-10)

### Current remediation summary (latest)

- The repository now has 63 automated tests, seven bilingual document-pair checks, a Windows GitHub Actions gate, and a package smoke check.
- The first-click menu, settings transactions, input validation, single-instance lifecycle, tray recovery policy, off-screen recovery, strict quota parsing, independent refresh channels, diagnostics summary, and UI/API module boundaries are implemented and tested.
- Windows 11 dual-monitor evidence is current; Windows 10, mixed-DPI, taskbar-edge, clean-machine physical evidence, and a full idle Compact run remain release-gate items.
- The repository is not marked release-ready or versioned as v0.3.0 until those remaining evidence gates are closed or explicitly approved by the maintainer.

- **Implemented and headlessly tested:** popup work-area placement, secondary-monitor work-area selection, bounded window dimensions, scale mode persistence, digit-only settings entries, 1–10 second refresh interval normalization, weekly `M/D` display, and earliest future reset-credit expiry formatting.
- **Regression suite:** 33 tests pass; Python compilation passes.
- **Still requires physical Windows validation:** mixed-DPI monitors, taskbar positions, and full manual settings interaction at the bottom-right edge. These are not inferred from headless tests.
- **Physical Windows evidence (2026-07-10):** launched with `pythonw.exe` and no console window; on the secondary monitor near `(4150,1248)`, the context menu was fully visible above the overlay and the first click on “Open Settings” opened the settings dialog while the main overlay remained visible. The captured monitor work area was `DISPLAY2 (2560,354)-(4480,1386)`.
- **Host evidence:** current host is Windows 11 Home `10.0.26200` (build `26200`); the live display probe reports both connected monitors at 96 DPI. This does not satisfy mixed-DPI coverage.
- **Launcher smoke evidence:** two consecutive root CMD launches produced exactly one `pythonw.exe` overlay process and no console window; the existing instance was preserved.
- **Physical Windows evidence (lifecycle):** selecting “Hide Window” removed the overlay from the desktop without terminating the `pythonw.exe` process. Tray-driven restoration was not claimed because the tray icon was not exposed to the UI automation window list; it remains a manual verification item.
- **Tray follow-up:** the icon was visible in the primary taskbar notification area, but coordinate-level automated left/right clicks did not yield a reliable tray menu or restore action. This remains a human-interaction test, not a product failure classification.
- **Tray physical pass:** the Windows notification-area keyboard path (`Win+B` then Apps) opened the tray menu; selecting Hide followed by Show restored the overlay to `(4150,1248)`.
- **Still planned:** any external quota provider. No access-token provider was added.
- **Implemented since this note:** the dedicated refresh scheduler, document parity checker, quota health classification, and opt-in compact/expanded display mode. Physical Windows validation remains required for those UI paths.
- **Added in the latest iteration:** tray action allowlisting and single-scheduled recovery policy, covered by deterministic tests; direct tray-menu automation remains environment-limited.
- **Added in the latest iteration:** free/proportional window-size transformation is now an independent tested API rather than UI-only logic.
- **Added in the latest iteration:** local-only quota provider normalization with tests proving credential-bearing fields are not propagated.
- **Security boundary:** no test or runtime path introduced an access-token reader or external quota client; that remains explicitly out of scope.
- **Automated release gate:** `scripts/run_release_checks.py` passed document parity, Python compilation, and all 33 tests. It intentionally does not claim physical monitor or tray coverage.
- **Latest regression:** UTF-8 BOM settings are now accepted; the automated release gate passes with 33 tests.
- **Compact-mode physical attempt:** a BOM-enabled `compact_when_idle` configuration preserved the secondary coordinate `(4150,1248)`; the current activity snapshot reported one active conversation, so the idle-only shrink path could not be physically observed in this run.
