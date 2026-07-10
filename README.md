# Codex Windows Status Pet

An unofficial Windows companion for Codex. It provides a small desktop overlay and a notification-area icon for live Codex activity, plan progress, rate limits, and reset credits.

## Features

- Reads rate limits from the local `codex app-server --stdio` JSON-RPC interface.
- Detects active Codex sessions from local session JSONL files.
- Shows the latest plan completion as `N/M` when a plan is available.
- Supports multiple monitors and preserves user-supplied virtual-desktop coordinates.
- Settings: opacity, font size, font color, background color, default X/Y position, always-on-top, and position lock.
- Settings actions: Save, Apply, Restore Defaults, and Close.
- Notification-area menu: show, hide, open settings, and exit.
- Uses `pythonw.exe`; no persistent command prompt window is required.
- Starts automatically at Windows sign-in through a Startup shortcut.

## Quick start

Double-click `start_codex_status_pet.cmd` in this repository, or use the workspace launcher `启动Codex状态宠物.cmd`.

The bundled Python runtime is preferred. If it is unavailable, the launcher falls back to `pythonw.exe` on `PATH`.

## Data and security boundary

The companion starts only the local Codex app-server and reads local Codex session metadata. It does not read `auth.json`, send project files to a third-party service, or maintain its own backend. The only network activity comes from the official local Codex app-server process.

Local settings are stored at `%USERPROFILE%\.codex\codex-windows-status-pet.json`.

## Development checks

```powershell
python -m py_compile .\scripts\codex_status_pet.py
```

The application is intentionally an external companion. Codex custom pets currently provide a static spritesheet contract, so dynamic text remains in this companion overlay rather than being injected into the built-in pet.

## License

MIT. See `LICENSE` if one is added by the project owner.
