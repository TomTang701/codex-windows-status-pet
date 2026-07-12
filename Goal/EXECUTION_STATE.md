# Execution State

- Goal status: `ACTIVE`
- Active phase: `v0.5.1 TDD GREEN implementation`
- Active version: `0.5.1`
- Branch / base: `fix/v0.5.1-runtime-geometry` from `main` `bd11bb0f6ea29e2bd2aa9760d85228084abd336b`
- Active skill: `test-driven-development`
- Current design/spec: `docs/superpowers/specs/2026-07-11-v0.5.1-runtime-geometry-design.md`; `DESIGN VERIFIED`
- Current plan: `docs/superpowers/plans/2026-07-11-v0.5.1-runtime-geometry.md`
- Current task: implement one target-window-DPI geometry and pixel-font authority
- Production RED: cold start five-row fit can pass, then runtime settings/lock lifecycle changes expanded geometry and clips the final Reset Credit row
- Automated RED: `test_toggle_preserves_cold_start_fit` fails on released behavior because the same `Pet` changes from `330x138` to `264x110` after `toggle_locked`
- Existing verification gap: `dpi_content_probe.py` uses a fresh `Pet` per scale and isolated `apply_settings`; it does not cover long-lived transitions
- Root cause: cold start derives geometry at pre-position DPI 120, runtime reapply derives at target DPI 96, and Tk point fonts retain process-global 120-DPI metrics; `show_window` preserves but does not initiate the failure
- Design Verification: `PASS`
- Human fact required: `None`
- Blocker: `None`
- v0.6.0 Productization: `PAUSED` until v0.5.1 is fully released and reconciled
- Next exact action: minimally preposition the withdrawn HWND and derive both geometry and fonts from its target DPI
- Last updated: 2026-07-11
