# API and Test Boundary Specification

## Purpose

The Windows companion is split into small, testable APIs so failures can be isolated without
starting Tk or the notification area. Each API has one responsibility and must remain usable from
headless tests.

| API | Module | Responsibility | Test boundary |
|---|---|---|---|
| Configuration API | `scripts/api/config_api.py` | Validate, normalize, load, and atomically save settings. | Temporary JSON files; no Tk. |
| Activity API | `scripts/api/activity_api.py` | Read Codex session JSONL and derive active/recent status. | Synthetic JSONL directory; injectable clock. |
| Runtime API | `scripts/api/runtime_api.py` | Own the named Windows single-instance mutex. | Windows mutex acquisition/release. |
| Diagnostics API | `scripts/api/diagnostics_api.py` | Capture uncaught main-thread and worker exceptions when `pythonw.exe` hides the console. | Temporary log path and synthetic exception. |
| Codex transport API | `AppServer` in `scripts/codex_status_pet.py` | Start local app-server, perform JSON-RPC requests, and report protocol failures. | Mock subprocess/stdout response matrix. |
| UI/tray adapter | `Pet` and `TrayIcon3` in `scripts/codex_status_pet.py` | Translate API results into Tk and tray actions. | Windows UI/manual interaction tests only. |

## Invariants

- Configuration API never raises for malformed user JSON; it returns defaults plus warnings.
- Configuration writes use a same-directory temporary file and atomic replacement.
- Activity API uses the latest session event as the inactivity clock, not only task start time.
- Runtime API never kills an unrelated process to obtain the mutex.
- UI callbacks must not perform blocking app-server or filesystem work on the Tk thread.
- The overlay displays only the active conversation count; plan-step text is not part of the UI contract.
- A major behavior or performance change requires a changelog entry, specification update, and regression test.

## Test commands

```powershell
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m unittest discover -s .\tests -v
$api = Get-ChildItem .\scripts\api -Filter *.py | ForEach-Object FullName
& $py -m py_compile .\scripts\codex_status_pet.py $api
```

## Change classification

- **Major behavior:** menu dispatch, visibility, tray actions, single-instance policy, settings semantics, or displayed status. Requires a focused regression test and a manual Windows check.
- **Performance:** session scan duration, refresh interval, thread count, or disk-write frequency. Requires a benchmark or bounded test fixture and a note in `CHANGELOG.md`.
- **Documentation-only:** wording or examples with no runtime effect. Still requires checking English and Chinese specifications for drift.
