# ACTIVE VERSION BRIEF — v0.5.5 Mixed-DPI Startup Position Recovery Correctness

## Released history

- `v0.5.3` remains the released product baseline and latest product version at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.
- `v0.5.4` remains a closed position-persistence investigation with no product tag or GitHub Release.
- `v0.5.5` is active only to investigate the new mixed-DPI secondary edge-recovery symptom.

## Active outcome

Preserve saved positions that are legal using the target monitor's effective DPI, including secondary right/bottom edge positions, while still recovering genuinely invalid or disconnected positions.

## Investigation boundary

Tom's new physical 125% primary / 100% secondary evidence shows a spatially conditional startup shift near secondary right/bottom edges. The bootstrap-DPI metric mismatch is a strong hypothesis only; the current main must first fail a production-equivalent RED and show the first wrong coordinate boundary.

v0.5.4's `(4143, 1182)` A-path remains valid historical evidence for its tested coordinate. v0.5.3 Shell Identity remains protected: the root HWND must retain `WS_EX_TOOLWINDOW=true` and `WS_EX_APPWINDOW=false`. No v0.6.0 feature work is in scope.

## Status

`v0.5.5 ACTIVE / ROOT-CAUSE VERIFICATION REQUIRED / v0.6.0 BLOCKED`
