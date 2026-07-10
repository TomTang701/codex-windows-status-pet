# File Specification

## Repository layout

| Path | Purpose |
|---|---|
| `.codex-plugin/plugin.json` | Codex plugin manifest and cache-busting version. |
| `scripts/codex_status_pet.py` | Main Windows overlay, tray integration, app-server client, activity monitor, and settings UI. |
| `scripts/ui/context_menu.py` | Isolated first-click-safe context-menu Tk adapter. |
| `scripts/ui/settings_dialog.py` | Isolated transactional settings-dialog Tk adapter. |
| `scripts/ui/tray_adapter.py` | Isolated notification-area icon and callback adapter. |
| `scripts/start_pet.ps1` | Optional PowerShell launcher for environments that permit it. |
| `start_codex_status_pet.cmd` | Recommended double-click launcher using `pythonw.exe`. |
| `skills/codex-windows-status-pet/SKILL.md` | Codex skill instructions for using the companion. |
| `README.md` | Primary English documentation. |
| `README.zh-CN.md` | Chinese maintenance and quick-reading translation. |
| `FILE_SPEC.md` | Primary English file and configuration specification. |
| `FILE_SPEC.zh-CN.md` | Chinese file specification. |
| `CHANGELOG.md` | Primary English release history. |
| `CHANGELOG.zh-CN.md` | Chinese release history. |
| `API_SPEC.md` / `API_SPEC.zh-CN.md` | API boundaries, test contracts, and change classification. |
| `PRODUCT_REVIEW.md` / `PRODUCT_REVIEW.zh-CN.md` | Product review and synchronized Chinese translation. |
| `requirements.txt` | Runtime dependency floor for fallback Python environments. |
| `tests/` | Headless API and UI-adapter regression tests. |
| `DEVELOPMENT_PLAN.md` | Canonical phased development plan. |
| `DEVELOPMENT_PLAN.zh-CN.md` | Synchronized Chinese translation copy of the development plan. |
| `scripts/api/quota_format_api.py` | UI-independent quota/date formatting API. |
| `scripts/api/quota_status_api.py` | UI-independent quota health classification API. |
| `scripts/api/display_mode_api.py` | UI-independent compact/expanded display-mode API. |
| `scripts/api/window_size_api.py` | UI-independent free/proportional window-size API. |
| `scripts/api/quota_provider_api.py` | Local-only provider response normalization API; no auth or network ownership. |
| `COMPATIBILITY_MATRIX.md` / `COMPATIBILITY_MATRIX.zh-CN.md` | Living Windows compatibility and release-gate record. |
| `scripts/api/tray_lifecycle_api.py` | UI-independent tray action and recovery policy API. |
| `scripts/api/refresh_scheduler_api.py` | UI-independent single-flight refresh scheduling API. |
| `scripts/check_doc_parity.py` | Structural parity checker for English/Chinese document pairs. |
| `scripts/run_release_checks.py` | Reproducible automated release gate; physical checks remain separate. |
| `scripts/package_smoke_test.py` | Validate package metadata and create a non-release smoke ZIP. |
| `.github/workflows/ci.yml` | Windows GitHub Actions quality gate and smoke artifact workflow. |
| `scripts/api/compact_state_api.py` | UI-independent timed compact/expanded state and edge geometry. |
| `scripts/api/window_recovery_api.py` | UI-independent off-screen recovery and nearest work-area selection. |
| `scripts/api/refresh_controller_api.py` | Independent Activity/Quota refresh channel lifecycle. |
| `scripts/api/quota_parse_api.py` | Strict approved-field quota response parser. |
| `scripts/api/quota_state_api.py` | Last-good, stale, and explicit quota failure state. |
| `scripts/api/models_api.py` | Typed quota-domain dataclasses. |
| `scripts/api/codex_transport_api.py` | Local Codex CLI discovery and app-server stdio JSON-RPC transport. |

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
  "y": 1248,
  "window_width": 330,
  "window_height": 138,
  "scale_mode": "free",
  "refresh_interval_seconds": 5,
  "compact_when_idle": false
}
```

`x` and `y` are virtual-desktop coordinates and may refer to any connected monitor, including negative coordinates or coordinates beyond the primary display.

Diagnostics are written to `%USERPROFILE%\.codex\codex-windows-status-pet.log`; the log must never contain auth tokens, project files, or full session text.

## Runtime invariants

- Only one companion instance may run at a time.
- API boundaries and regression-test contracts are defined in `API_SPEC.md`; major behavior and performance changes require specification and changelog updates.
- Startup claims the named Windows mutex before creating the UI. If another instance owns it, the new instance exits without killing the existing process.
- Hiding changes opacity to zero and does not overwrite the saved position.
- Opening or closing settings restores the main overlay to visible state.
- The second overlay line is always `Active conversations N`; plan-step details are intentionally not displayed.
- Menu commands execute once on the first click and close the context menu after the command runs.
- Background workers never call Tk APIs directly; UI scheduling remains on the Tk main thread.
- Substantial changes are committed promptly after the automated release gate passes; remote owner and author identity are verified by the local Git configuration and pre-push hook.
