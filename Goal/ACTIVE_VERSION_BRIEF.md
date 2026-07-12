# ACTIVE VERSION BRIEF — v0.5.3 Windows Shell Identity Correctness (Released)

## Released history

- `v0.5.1` remains the previous released product baseline at `10de01410126a1877ac9406fc02e3bc583659df3`.
- `v0.5.2` remains a closed rendered-visibility investigation and has no product version, tag, or GitHub Release.
- `v0.5.3` is released at `b6a53e85b004d0bd707e7e7e4f03c5ad09a1a5cf`, via PR #21, tag `v0.5.3`, and the matching GitHub Release.

## Released outcome

Restore the overlay's intended Windows Shell identity: visible desktop overlay and tray icon, but absent from Task View, Alt+Tab, and the ordinary taskbar application surface.

## Investigation result

The real root HWND comparison is complete. Both historical working and current windows have owner `0`; only the historical window retains `WS_EX_TOOLWINDOW`. The v0.5.1 lifecycle maps early, then Tk alpha processing clears that bit before the final `deiconify()`. v0.5.3 restores the evidence-required bit only after each native mapping boundary and keeps `WS_EX_APPWINDOW` absent.

The release has a real-HWND RED/GREEN and lifecycle regression coverage, exact-head CI, merged-main RC, a semantic tag, and a matching GitHub Release. No battery feature is in scope.

## Status

`v0.5.3 RELEASED / DESIGN VERIFIED / v0.6.0 BATTERY FEATURE NOT STARTED`
