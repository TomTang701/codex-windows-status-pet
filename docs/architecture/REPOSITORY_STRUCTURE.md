# Repository Structure

This document describes where project files belong. Configuration values belong in `CONFIGURATION.md`; runtime API contracts belong in `API_SPEC.md`.

## Top-level layout

| Path | Purpose |
|---|---|
| `.codex-plugin/plugin.json` | Codex plugin manifest and cache-busting version. |
| `scripts/codex_status_pet.py` | Stable launcher/import facade for the Windows companion. |
| `scripts/ui/main_window.py` | Main Tk window lifecycle, rendering, recovery, refresh orchestration, and UI composition. |
| `scripts/api/status_rows_api.py` | Pure five-row identity and compatibility-text contract. |
| `scripts/ui/status_rows.py` | Five-label Tk status rendering adapter. |
| `scripts/api/` | UI-independent domain, transport, validation, refresh, quota, geometry, and diagnostics APIs. |
| `scripts/api/*_controller_api.py` | Pure application, presentation, persistence, and lifecycle coordination state. |
| `scripts/ui/` | Tk and notification-area adapters. |
| `start_codex_status_pet.cmd` | Recommended double-click launcher using `pythonw.exe`. |
| `skills/codex-windows-status-pet/SKILL.md` | Codex skill instructions. |
| `tests/` | Headless API and UI-adapter regression tests. |
| `docs/` | Layered project documentation and evidence. |
| `.github/workflows/ci.yml` | Windows CI quality gate and smoke artifact workflow. |
| `requirements.txt` | Runtime dependency floor for fallback Python environments. |

## Placement rules

- New pure behavior belongs in `scripts/api/` with deterministic tests.
- Windows or Tk calls belong in platform/UI adapters and must not become domain dependencies.
- User-facing installation and troubleshooting belong in `docs/operations/`.
- Normative governance belongs in `docs/governance/`.
- Architecture and configuration contracts belong in `docs/architecture/`.
- Compatibility results belong in `docs/quality/`; one-time audits belong in `docs/archive/audits/`.
- Generated smoke packages, probe output, logs, and local settings must not be committed.

## Runtime ownership invariants

- Only one companion instance may run at a time; a second launch exits without killing the existing process.
- Background workers never call Tk APIs directly; UI scheduling remains on the Tk main thread.
- `Pet` owns Tk composition; pure controllers own coordination state and never import Tk or pystray.
- Menu commands execute once on the first click and close the context menu after execution.
- Five status rows retain stable identities and persistent Tk widgets across updates.
- Substantial changes are committed after routine Quality passes, with remote owner and author identity verified by local Git configuration and the pre-push hook. Formal Release Candidate approval remains separate.
