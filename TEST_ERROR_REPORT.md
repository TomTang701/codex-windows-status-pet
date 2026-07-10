# Codex Windows Status Pet — Test Error Report

**Audit date:** 2026-07-09  
**Scope:** Windows launcher, overlay, tray icon, settings, activity detection, Codex app-server boundary, packaging, and documentation.  
**Rule for this audit:** findings only. No production fix was applied during this audit.

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

## Highest-priority release blockers

1. **ERR-001:** main menu first-click failure.
2. **ERR-002 / ERR-014 / ERR-015:** configuration corruption and unhandled settings I/O can make the app disappear or lose state.
3. **ERR-004 / ERR-005:** duplicate-process and startup lifecycle failures.
4. **ERR-007:** incorrect idle status for long-running Codex work.
5. **ERR-010 / ERR-011 / ERR-012:** tray/dependency failures are silent under `pythonw.exe`.

## Explicit non-actions

No production code, launcher, settings file, or runtime behavior was changed during this audit.
The only intended repository artifact from this audit is this report.
