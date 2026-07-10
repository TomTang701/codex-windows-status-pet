# Test Record: Windows 11 Dual Monitor Topology

- Date: 2026-07-10
- Commit: `b4fbc78`
- Application version: `0.2.0`
- Windows version/build: Windows 11 Home, build 26200
- Monitor topology: `DISPLAY1` at `0,0–2048,1152`; `DISPLAY2` at `2560,354–4480,1434`
- Work areas: `DISPLAY1` `0,0–2048,1104`; `DISPLAY2` `2560,354–4480,1386`
- DPI: 96 / 96
- Taskbar: primary, bottom, probe rectangle `0,1380–2560,1440`
- Result: Physical topology pass; UI behaviors are recorded separately in the compatibility matrix.
- Evidence: [`2026-07-10-display-probe.json`](2026-07-10-display-probe.json)
- Limitations: This record does not claim Windows 10, mixed-DPI, alternate taskbar-edge, or clean-machine coverage.

## Steps

1. Capture the virtual desktop, monitor work areas, DPI, and primary taskbar rectangle with `scripts/probe_display.py`.
2. Compare the result with the configured secondary coordinate `(4151,1248)` and the window-recovery geometry fixtures.

## Expected

The probe reports both monitors, their work areas, DPI values, and the taskbar reservation without exposing credentials or session content.

## Actual

The virtual desktop was `0,0–4480,1434`; both monitors reported 96 DPI; the primary taskbar was at the bottom; the secondary work area included `(4151,1248)` as a valid top-left coordinate for the configured overlay dimensions within the documented rounding tolerance.

## Follow-up

Repeat this record after a taskbar-edge change or monitor disconnect/reconnect and add a new dated record rather than overwriting this evidence.
