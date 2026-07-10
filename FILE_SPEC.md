# File Specification

## Repository layout

| Path | Purpose |
|---|---|
| `.codex-plugin/plugin.json` | Codex plugin manifest and cache-busting version. |
| `scripts/codex_status_pet.py` | Main Windows overlay, tray integration, app-server client, activity monitor, and settings UI. |
| `scripts/start_pet.ps1` | Optional PowerShell launcher for environments that permit it. |
| `start_codex_status_pet.cmd` | Recommended double-click launcher using `pythonw.exe`. |
| `skills/codex-windows-status-pet/SKILL.md` | Codex skill instructions for using the companion. |
| `README.md` | Primary English documentation. |
| `README.zh-CN.md` | Chinese maintenance and quick-reading translation. |
| `FILE_SPEC.md` | Primary English file and configuration specification. |
| `FILE_SPEC.zh-CN.md` | Chinese file specification. |
| `CHANGELOG.md` | Primary English release history. |
| `CHANGELOG.zh-CN.md` | Chinese release history. |

## Runtime configuration

`%USERPROFILE%\.codex\codex-windows-status-pet.json`

```json
{
  "alpha": 0.35,
  "font_color": "#e5e7eb",
  "font_size": 10,
  "background_color": "#000000",
  "topmost": true,
  "locked": true,
  "x": 4151,
  "y": 1248
}
```

`x` and `y` are virtual-desktop coordinates and may refer to any connected monitor, including negative coordinates or coordinates beyond the primary display.

## Runtime invariants

- Only one companion instance may run at a time.
- Starting the launcher first terminates stale `python.exe`/`pythonw.exe` companion processes whose window title is `Codex Windows Status Pet`, then claims the named Windows mutex. This prevents duplicate overlays and duplicate tray icons during testing or repeated launches.
- Hiding changes opacity to zero and does not overwrite the saved position.
- Opening or closing settings restores the main overlay to visible state.
- The second overlay line is always `Active conversations N`; plan-step details are intentionally not displayed.
- Menu commands execute once on the first click and close the context menu after the command runs.
- Background workers never call Tk APIs directly; UI scheduling remains on the Tk main thread.
