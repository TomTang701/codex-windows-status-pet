# Execution State

- Goal status: `ACTIVE`
- Active phase: `v0.5.1 design verified; TDD planning`
- Active version: `0.5.1`
- Branch / base: `fix/v0.5.1-runtime-geometry` from `main` `bd11bb0f6ea29e2bd2aa9760d85228084abd336b`
- Active skill: `writing-plans`
- Current design/spec: `docs/superpowers/specs/2026-07-11-v0.5.1-runtime-geometry-design.md`; `DESIGN VERIFIED`
- Current task: convert the proven long-lived transition RED into an automated regression and implementation plan
- Production RED: cold start five-row fit can pass, then runtime settings/lock lifecycle changes expanded geometry and clips the final Reset Credit row
- Existing verification gap: `dpi_content_probe.py` uses a fresh `Pet` per scale and isolated `apply_settings`; it does not cover long-lived transitions
- Root cause: cold start derives geometry at pre-position DPI 120, runtime reapply derives at target DPI 96, and Tk point fonts retain process-global 120-DPI metrics; `show_window` preserves but does not initiate the failure
- Design Verification: `PASS`
- Human fact required: `None`
- Blocker: `None`
- v0.6.0 Productization: `PAUSED` until v0.5.1 is fully released and reconciled
- Next exact action: write the v0.5.1 implementation plan, then add an automated long-lived cold-start-to-toggle RED before production edits
- Last updated: 2026-07-11
