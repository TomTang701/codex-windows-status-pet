# ACTIVE VERSION BRIEF — v0.5.4 Position Persistence Correctness

## Released history

- `v0.5.3` is the released product baseline at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.
- `v0.5.4` is the active position-persistence correctness patch; it has no product tag or GitHub Release yet.

## Active outcome

Restore durable overlay position persistence through drag, normal tray Exit, and restart, while preserving legal topology recovery.

## Investigation boundary

The root cause is unknown. The exact A-path coordinates must be traced from the stable post-drag root through runtime state, JSON after `finish_drag`, normal tray Exit, raw Pet B load, `safe_position`, and Pet B's final root. No production position fix is permitted before the first divergence and Design Verification.

v0.5.3 Shell Identity remains protected: the root HWND must retain `WS_EX_TOOLWINDOW=true` and `WS_EX_APPWINDOW=false`. No battery feature is in scope.

## Status

`v0.5.4 ACTIVE / DESIGN VERIFICATION PENDING / v0.6.0 BATTERY FEATURE DEFERRED`
