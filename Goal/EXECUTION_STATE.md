# Execution State

- Goal status: `ACTIVE`
- Active version: `v0.5.5`
- Released product baseline and latest product version: `v0.5.3` at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`
- Historical v0.5.2: `CLOSED investigation / no product release`
- Active phase: `GREEN candidate; formal Quality, RC, and exact-head CI pending`
- v0.5.4 investigation: `CLOSED historical investigation / no product release`
- Current reported regression: `100% secondary near right/bottom edge saved position shifts inward on startup from 125% primary bootstrap`
- Root cause: `withdrawn bootstrap HWND reports primary 120 DPI; safe_position uses inflated 120-DPI metrics to recover a 96-DPI-secondary legal edge coordinate before target DPI resync`
- Design Verification: `PASSED — current-main RED and first clamp boundary recorded`
- Production-code changes: `target-monitor geometry authority correction implemented after current-main RED and focused GREEN`
- v0.6.0 5H Battery Indicator and Layout Tightening: `BLOCKED / NOT STARTED`
- Human fact required: `None`
- Blocker: `None`
- Next exact action: run Quality, package smoke, formal RC, final review, then the authorized exact-head GitHub release workflow
- Last updated: 2026-07-12
