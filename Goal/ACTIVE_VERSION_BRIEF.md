# ACTIVE PROGRAM VERSION BRIEF – v0.5.5 Release Completion → v0.6.0 Delivery

## Released history

- `v0.5.3` remains the released product baseline and latest product version at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.
- `v0.5.4` remains a closed position-persistence investigation with no product tag or GitHub Release.
- `v0.5.5` is the active implementation version and its release candidate is under PR review; v0.6.0 begins automatically only after the Program Goal hard version gate.

## Active outcome

Preserve saved positions that are legal using the target monitor's effective DPI, including secondary right/bottom edge positions, while still recovering genuinely invalid or disconnected positions.

## Investigation boundary

The current-main production-equivalent RED proved that a withdrawn bootstrap root reports 120 DPI before recovery, applies `350x146` metrics to legal secondary saved `(4200,1269)`, and clamps it to `(4130,1240)`. The minimum fix now uses the saved point's target-monitor geometry authority for recovery containment only. Physical Windows GREEN coverage preserves secondary right, bottom, bottom-right, and interior coordinates plus drag-to-edge restart persistence, without weakening invalid-position recovery.

v0.5.4's `(4143, 1182)` A-path remains valid historical evidence for its tested coordinate. v0.5.3 Shell Identity remains protected: the root HWND must retain `WS_EX_TOOLWINDOW=true` and `WS_EX_APPWINDOW=false`. No v0.6.0 feature work is in scope.

## Status

`PROGRAM ACTIVE / v0.5.5 CI-ADMISSION CORRECTION / v0.6.0 PENDING HARD VERSION GATE`
