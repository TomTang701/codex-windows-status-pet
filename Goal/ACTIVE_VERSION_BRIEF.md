# ACTIVE VERSION BRIEF — v0.5.1 Runtime Geometry Reapplication Stabilization

## Outcome

One long-lived `Pet` keeps one coherent target-window-DPI expanded geometry and fully visible five-row content through every supported settings, lock, visibility, compact, restore, and monitor transition.

## Root cause and design

Released v0.5.0 derived cold-start and runtime reapplication geometry under different HWND monitor/DPI contexts while Tk point fonts retained process-global scaling. The verified minimum design positions the withdrawn HWND first, then derives physical geometry and explicit negative-pixel fonts from that target-window DPI. `Pet._sync_compatibility_metrics()` remains the sole runtime metric authority; no new subsystem or persisted physical dimensions were added.

## Required transition matrix

Cold start/no action; open settings only; Close without changes; toggle lock; toggle lock then settings; opacity-only Apply; scale-change Apply; Save; draft scale then Close rollback; Restore Defaults; repeated settings open/close; Hide/Show; Compact/Expand; and the closest reproducible combined sequence.

## Regression contract

After every transition exactly five stable rows exist; requested heights fit allocations; all rows and the final row bottom stay inside the actual visible root/client boundary; approved single-line rows do not unexpectedly wrap; unchanged logical scale and DPI preserve expanded geometry; and a true DPI change ends with exact Window Scale API geometry and matching pixel fonts.

## Current evidence

- Authoritative released-behavior RED: one `Pet` changed from `330x138` to `264x110` after `toggle_locked`.
- Cross-monitor RED: reapplication moved the HWND to DPI 120 while retaining DPI 96 metrics.
- GREEN: all 25 scale steps at DPI 96 and 120 fit all five rows.
- GREEN: all 15 required production-equivalent lifecycle transitions report `fits: true`.
- GREEN: routine Quality approved with 137 core tests and 23 Tk UI tests.

## Status

`DESIGN VERIFIED / IMPLEMENTATION GREEN / FORMAL RC APPROVED / REMOTE RECONCILIATION PENDING`

The branch package and formal RC are approved. The patch is not complete until exact-head PR CI, squash merge, merged-main RC, tag `v0.5.1`, GitHub Release, branch cleanup, and active-state reconciliation are verified.
