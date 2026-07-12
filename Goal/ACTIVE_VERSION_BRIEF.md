# ACTIVE VERSION BRIEF — v0.5.4 Position Persistence Investigation (Closed)

## Released history

- `v0.5.3` is the released product baseline and latest product version at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.
- `v0.5.4` is a closed position-persistence investigation with no product tag or GitHub Release.

## Closed investigation outcome

The reported restart position-loss symptom is no longer reproducible. The production-equivalent round trip preserved `(4143, 1182)` through persistence, normal tray Exit, loading, safe-position validation, and final root placement.

## Investigation conclusion

No first coordinate divergence or valid RED was established. Design Verification therefore failed correctly, and no production persistence correction is justified. Tom confirmed that restarting the software no longer loses the window position.

v0.5.3 Shell Identity remains protected: the root HWND must retain `WS_EX_TOOLWINDOW=true` and `WS_EX_APPWINDOW=false`. No v0.6.0 feature work is in scope.

## Status

`v0.5.4 CLOSED INVESTIGATION / NO PROVEN PRODUCTION DEFECT / NO PRODUCT RELEASE / v0.6.0 NOT STARTED`
