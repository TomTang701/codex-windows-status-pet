# ACTIVE VERSION BRIEF — v0.5.3 Windows Shell Identity Correctness

## Released history

- `v0.5.1` remains the released product baseline at `10de01410126a1877ac9406fc02e3bc583659df3`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.

## Active outcome

Restore the overlay's intended Windows Shell identity: visible desktop overlay and tray icon, but absent from Task View, Alt+Tab, and the ordinary taskbar application surface.

## Investigation contract

The root cause is unknown. `overrideredirect(True)`, the v0.5.1 withdrawn startup lifecycle, `WS_EX_TOOLWINDOW`, ownership, and `WS_EX_APPWINDOW` are hypotheses only until the real overlay HWND and historical working state are measured and compared.

No production style, owner, mapping-lifecycle, geometry, or font change is allowed until Design Verification records an evidence-derived shell-identity RED and one root-cause hypothesis.

## Status

`v0.5.3 ACTIVE / DESIGN VERIFICATION PENDING / v0.6.0 BATTERY FEATURE DEFERRED`
