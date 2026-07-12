# ACTIVE GOAL — v0.5.1 Runtime Geometry Reapplication Stabilization

> **Status:** COMPLETE — released as `v0.5.1`; v0.6.0 Productization design may resume
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Scope:** one correctness patch release; no productization or unrelated refactor
> **Authority:** repository `AGENTS.md`, protected-core contracts, systematic debugging, Design Verification, TDD, and verification-before-completion remain mandatory. The repository standing authorization covers routine GitHub workflow operations within this Goal; listed high-risk operations remain separately permissioned.

## Product outcome

Cold start and every supported runtime settings, lock, and window-lifecycle transition must preserve one coherent DPI-aware expanded-window geometry contract, and all five stable status rows must remain completely visible.

## Production evidence

New v0.5.0 screenshots show a cold start with all five rows visible, followed by a settings/parameter/lock lifecycle where the expanded window geometry changes and the final Reset Credit row becomes partially hidden. The failure affects the whole expanded geometry, so a fixed pixel addition or padding reduction is not an accepted diagnosis.

This evidence limits the authority of the per-scale fresh-`Pet` DPI probe. Passing 25 isolated scale instances does not prove one long-lived production instance remains coherent through transitions.

## Required debugging sequence

1. Verify process provenance, runtime version, repository HEAD, HWND, position, monitor/work area, and effective window DPI without asking Tom.
2. Trace cold-start geometry, `apply_settings`, lock/settings transactions, `show_window`/`ensure_visible`, Hide/Show, Compact/Expand, and combined transitions.
3. Use one long-lived production-equivalent `Pet` and record logical settings, effective metrics, every geometry call, monitor/DPI, requested/actual/client geometry, packing, and all five row bounds before and after updates.
4. Reproduce one exact transition where cold-start fit passes and post-transition fit fails.
5. State one primary root-cause hypothesis and compare two or three minimal fixes.
6. Pass Design Verification before production code changes.
7. Use TDD: RED → minimum root-cause fix → GREEN → full transition/scale regression → Quality → package → formal RC → release verification.

## Protected behavior

- five stable row identities and truthful activity/quota presentation;
- local official Codex app-server and approved local session metadata only;
- 80–200% canonical logical scaling and schema-1 compatibility fields;
- per-monitor DPI awareness and legal multi-monitor coordinates;
- settings Apply/Save/Close/Defaults semantics, lock, drag, topmost, Hide/Show, Compact/Expand, tray reachability, single instance, and idempotent shutdown;
- v0.4.2 release-verification contracts and v0.5.0 lean-core boundaries.

## Prohibited shortcuts

- arbitrary height additions or random padding reductions;
- a new layout subsystem, manager, controller, service, or framework rewrite without evidence that the existing owner cannot hold the fix;
- productization, installer/startup work, or unrelated lean-core refactoring;
- human visual confirmation for machine-observable clipping facts.

## Completion gate

The Goal completes only when the released v0.5.0 failure transition is regression-protected and green, the entire long-lived transition matrix and supported scale matrix remain content-safe, full gates pass, exact-head CI succeeds, v0.5.1 is merged/tagged/released, branches are cleaned, and active state is reconciled. Only then may v0.6.0 Productization design resume.
