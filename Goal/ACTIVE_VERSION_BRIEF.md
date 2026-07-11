# ACTIVE VERSION BRIEF — v0.4.1 Correctness Stabilization

## Outcome

Close two known correctness gaps without adding product features:

1. The final reset-credit row remains fully visible at every supported window scale.
2. Tray and quota transport failures render through the authoritative five-row presentation path without calling Label-only configuration methods on `StatusRows`.

## Why now

Tom observed incomplete final-row content after proportional scaling. Source inspection also found two legacy `self.text.config(text=..., fg=...)` error paths even though `self.text` is now a `StatusRows` frame. These are correctness regressions in the released product core and must be protected before automation or architecture slimming.

## In scope

- Reproduce clipping using actual and requested Tk geometry at 80%, 100%, 150%, and 200%.
- Measure status container and five row bounds, text requested size, and unexpected wrapping.
- Define a regression check that would have caught the observed clipping.
- Apply the minimum root-cause layout fix supported by evidence.
- Reproduce tray-error and quota transport-error behavior through production integration paths.
- Route affected visible output through `StatusPresentationController` and `StatusRows.configure_rows`.
- Correct only documentation facts directly affected by these fixes.

## Out of scope

- New settings, menu actions, themes, animations, providers, telemetry, backends, installers, or startup changes.
- Broad main-window decomposition, framework replacement, broad API deletion, or Phase 2/3 simplification.
- Windows 10, ARM64, mixed-DPI physical, or alternate physical taskbar-edge support claims.
- Version v0.4.2 or later work.

## Protected behavior

- Local official Codex app-server quota path and approved local session metadata only.
- Five stable row identities: `activity`, `progress`, `primary_5h`, `weekly`, `reset_credit`.
- Single instance, main-thread Tk ownership, bounded single-flight refresh, safe idempotent shutdown, and no persistent console.
- Valid/recoverable settings, Apply/Save/Close/Restore Defaults semantics, 80–200% proportional scaling, Hide/Show, Compact/Expand, drag/lock, topmost, position recovery, tray reachability, persistence, and schema-1 compatibility.

## Observable contracts

### Content fit

At each supported scale point:

- all five approved rows exist in stable order;
- every row's actual bounding box lies inside the expanded status container;
- the final `reset_credit` row is mapped and has positive visible height;
- the status container's requested dimensions fit within its allocated dimensions and the window's content area;
- an approved single-line reset-credit value does not wrap unexpectedly;
- date/time text such as `重置 5 次 / 18:40 7/12` is fully represented.

### Error presentation

- A tray startup failure injected through the production path produces the approved five-row presentation without a Tk configuration error.
- A quota transport failure injected through the production queue path produces the approved state without a Tk configuration error.
- Both paths use the same row presentation boundary as normal runtime updates; no second direct-string renderer is added.

## Failure paths

```text
scale/config
→ window metrics
→ Tk geometry and packing
→ StatusRows allocation
→ five row bounds/text layout
→ fully visible reset-credit row

tray worker failure
→ tray action queue
→ main-thread action handling
→ presentation state/result
→ StatusRows.configure_rows
→ visible approved error rows

quota transport failure
→ production result queue
→ main-thread polling/state normalization
→ presentation state/result
→ StatusRows.configure_rows
→ visible approved unavailable/error rows
```

## Regression surface

- 80%, 100%, 150%, and 200% expanded layout with five rows.
- Compact/Expand and Hide/Show preserve scale and row readability.
- Apply, Save, Close, Restore Defaults, restart persistence, and protected configurations.
- Loading, available, stale with last-good data, unavailable, transport error, malformed response, tray error/recovery, and shutdown with in-flight work where affected.

## Design verification result

`PENDING` — implementation must not begin until investigation records objective problem evidence, one root-cause hypothesis per bug family, RED checks, failure-path validation, and bounded scope in a design document.

## Verification evidence classes

- Source/control-flow inspection.
- Focused pure and Tk integration RED/GREEN tests.
- Actual/requested Tk geometry and widget introspection.
- Relevant settings, Compact/Expand, Hide/Show, lifecycle, and queue-path regressions.
- Routine Quality, package smoke, strict readiness, and strict RC.
- Safe Windows 11 app-local runtime inspection if unit/Tk integration evidence is insufficient.

## Exit criteria

- The observed clipping symptom is reproduced by a check that fails before the fix and passes afterward.
- Supported-scale content-fit checks pass and the final row is fully visible.
- Tray and quota error integrations fail before the fix for the expected legacy-rendering reason and pass afterward.
- No affected error path calls Label-only text configuration against `StatusRows`.
- Affected output has one authoritative presentation route.
- Protected regressions and complete release gates pass.
- No feature or later-phase simplification is included.
