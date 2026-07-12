# Execution State

- Goal status: `ACTIVE`
- Active phase: `v0.5.1 systematic debugging`
- Active version: `0.5.1`
- Branch / base: `fix/v0.5.1-runtime-geometry` from `main` `bd11bb0f6ea29e2bd2aa9760d85228084abd336b`
- Active skill: `systematic-debugging`
- Current task: verify current production provenance and build a long-lived transition reproduction harness
- Production RED: cold start five-row fit can pass, then runtime settings/lock lifecycle changes expanded geometry and clips the final Reset Credit row
- Existing verification gap: `dpi_content_probe.py` uses a fresh `Pet` per scale and isolated `apply_settings`; it does not cover long-lived transitions
- Root-cause hypothesis: `PENDING`; monitor/DPI context timing and position-only show lifecycle are investigation priorities only
- Design Verification: `PENDING`
- Human fact required: `None`
- Blocker: `None`
- v0.6.0 Productization: `PAUSED` until v0.5.1 is fully released and reconciled
- Next exact action: record process/version/HEAD/HWND/position/monitor/DPI, then trace one long-lived `Pet` across the required transitions
- Last updated: 2026-07-11
