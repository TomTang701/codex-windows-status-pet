# Diagnostics

Diagnostics are written to `%USERPROFILE%\.codex\codex-windows-status-pet.log`. Logs must never contain auth tokens, project files, full session text, or raw provider responses.

The diagnostic boundary should cover startup, Codex discovery, app-server lifecycle, refresh failures, parsing failures, tray failures, window recovery, settings migration, and shutdown. User-facing summaries should expose application version, Windows/display information, sanitized configured paths, provider status, last successful refreshes, current state, and log location.

Diagnostic and logging policy is governed by [`ENGINEERING_STANDARD.md`](../governance/ENGINEERING_STANDARD.md).
