# ACTIVE VERSION BRIEF — v0.5.1 Runtime Geometry Reapplication Stabilization

## Outcome

One long-lived `Pet` must keep one coherent DPI-aware expanded geometry and fully visible five-row content through every supported settings, lock, visibility, compact, and restore transition.

## Current evidence

- Released v0.5.0 cold start can fit.
- A later settings/lock/parameter lifecycle produces a visibly different expanded geometry and clips the final Reset Credit row.
- The existing `dpi_content_probe.py` creates a fresh `Pet` per scale and therefore does not prove transition stability.

## Investigation focus

- `Pet.__init__` calls `_sync_compatibility_metrics()` before saved monitor geometry is applied.
- `_sync_compatibility_metrics()` derives display metrics from `dpi_for_window(self.winfo_id())`.
- `apply_settings()` re-derives and reapplies full geometry; lock and all settings transaction outcomes can enter it.
- `show_window()` applies position-only geometry around normal/deiconify/update lifecycle.
- Settings opening/restoration calls `show_window()` and later `after_idle(ensure_visible)`.

High-priority hypothesis, not yet root cause: cold-start and runtime reapplication may derive the same logical scale under different HWND monitor/DPI contexts or geometry lifecycle stages.

## Required transition matrix

Cold start/no action; open settings only; Close without changes; toggle lock; toggle lock then settings; opacity-only Apply; scale-change Apply; Save; draft scale then Close rollback; Restore Defaults; repeated settings open/close; Hide/Show; Compact/Expand; and the closest reproducible combined sequence.

## Regression contract

After every transition exactly five stable rows exist; requested heights fit allocations; all rows and the final row bottom stay inside the actual visible root/client boundary; approved single-line rows do not unexpectedly wrap; unchanged logical scale does not silently produce incoherent expanded geometry unless monitor DPI truly changes; and a true DPI change ends with geometry/content fit matching target-window DPI.

## Design status

`PENDING` — systematic runtime evidence and a reproducible long-lived RED are required before design verification or production changes.
