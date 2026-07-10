# Windows 11 Reset Credit status-row record

- Date: 2026-07-10
- Commit under test: `a814d85` plus the focused status-row padding fix in the working tree
- App version: `0.2.0`
- Windows: Windows 11 Home x64, build 26200
- Runtime: bundled Python 3.12.x `pythonw.exe`
- Monitor topology: two monitors, virtual desktop `0,0-4480,1440`
- DPI/scaling: target window DPI 120
- Taskbar: normal bottom taskbar
- Window: `330x138`, font size 10, secondary coordinate `(4151,1248)`

## Steps

1. Restart the root launcher after terminating only the verified repository instance.
2. Wait for Activity and Quota refresh.
3. Capture only the overlay rectangle; do not capture the desktop or unrelated content.
4. Inspect all five independently rendered rows.

## Expected

- Primary 5h shows local `HH:MM` only.
- Weekly shows local `HH:MM M/D`.
- Reset Credit shows `重置 N 次 / HH:MM M/D` without clipping.

## Actual

- Primary: `5h 0% / 17:23`.
- Weekly: `周 80% / 12:23 7/17`.
- Reset Credit: `重置 5 次 / 21:09 7/11`.
- All five rows were visible inside the saved `330x138` window.
- One repository `pythonw.exe` instance was running and the startup log contained no new exception.

## Result

Physical pass.

## Limitations

This record covers the current dual-monitor Windows 11 host, font size 10, and the normal bottom taskbar. It does not claim Windows 10, ARM64, 32-bit Windows, or alternate physical taskbar edges.

## Safe evidence

A cropped overlay-only screenshot was inspected locally. It contained status percentages/times only and no token, account ID, prompt, response, session content, or project content.
