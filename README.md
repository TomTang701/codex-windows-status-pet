# Codex Windows Status Pet

An unofficial Windows companion for Codex. It provides a small desktop overlay and a notification-area icon for live Codex activity, rate limits, and reset credits.

## Features

- Reads rate limits from the local `codex app-server --stdio` JSON-RPC interface.
- Detects active Codex sessions from local session JSONL files.
- Shows the number of currently active conversations without exposing plan-step details.
- Supports multiple monitors and preserves user-supplied virtual-desktop coordinates.
- Keeps the context menu fully inside the active monitor work area, including bottom-right edges.
- Settings: opacity, font size, font color, background color, default X/Y position, always-on-top, and position lock.
- Settings also include width, height, proportional scaling controls, and a 1–10 second refresh interval.
- Optional idle compaction shrinks the overlay and expands it again on hover; it is off by default.
- Weekly quota and the earliest future reset-credit expiry use local `HH:MM M/D` formatting without leading zeroes.
- Settings actions: Save, Apply, Restore Defaults, and Close.
- Notification-area menu: show, hide, open settings, and exit.
- Uses `pythonw.exe`; no persistent command prompt window is required.
- Starts automatically at Windows sign-in through a Startup shortcut.

## Quick start

Double-click `start_codex_status_pet.cmd` in this repository, or use the workspace launcher `启动Codex状态宠物.cmd`.

The bundled Python runtime is preferred. If it is unavailable, the launcher falls back to `pythonw.exe` on `PATH`.
The fallback environment must install the packages listed in `requirements.txt`.

## Data and security boundary

The companion starts only the local Codex app-server and reads local Codex session metadata. Its quota provider normalizes already-fetched local data only; it does not read `auth.json`, access tokens, or project files, send data to a third-party service, or maintain its own backend. The only network activity comes from the official local Codex app-server process.

Local settings are stored at `%USERPROFILE%\.codex\codex-windows-status-pet.json`.

See [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) for the phased roadmap and [API_SPEC.md](API_SPEC.md) for test boundaries.
See [COMPATIBILITY_MATRIX.md](COMPATIBILITY_MATRIX.md) for current Windows evidence and release gates.

## Development checks

```powershell
python -m py_compile .\scripts\codex_status_pet.py
$py = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
& $py -m unittest discover -s .\tests -v
```

The reproducible automated gate is `python scripts/run_release_checks.py`. It does not replace the physical Windows checks listed in `COMPATIBILITY_MATRIX.md`.
The package smoke gate is `python scripts/package_smoke_test.py`; GitHub Actions runs both gates on Windows.
Use `python scripts/check_release_readiness.py` to see whether physical compatibility evidence still blocks v0.3.0. The current repository does not install a Startup-folder entry automatically.

Before publishing, approve the intended GitHub owner in the local repository. The tracked
`.githooks/pre-push` guard rejects pushes until this is set and rejects any remote whose owner
differs from it:

```powershell
git config --local core.hooksPath .githooks
git config --local codex.expected-owner <your-github-username>
git config --local user.name "Your GitHub display name"
git config --local user.email "your-github-noreply-email"
git config --local codex.expected-author-email "your-github-noreply-email"
```

The hook validates both the remote owner and the commit author email. This is deliberate: the
GitHub CLI account, credential helper, and global Git identity are machine-level state and must not
silently determine where a project is published or whose name appears on commits.

The application is intentionally an external companion. Codex custom pets currently provide a static spritesheet contract, so dynamic text remains in this companion overlay rather than being injected into the built-in pet.

## License

MIT. See `LICENSE` if one is added by the project owner.
