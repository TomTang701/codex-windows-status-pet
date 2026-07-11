# Execution State

- Active phase: `Phase 1 — Correctness Stabilization` reopened after screenshot disproved clipping completion
- Active version: `0.4.1`
- Branch / HEAD: `fix/v0.4.1-correctness` / current local branch tip; remote branch not created
- Active skill: `systematic-debugging`
- Current design/spec: `docs/superpowers/specs/2026-07-11-v0.4.1-correctness-stabilization-design.md`; clipping portion invalidated, Design Verification `PENDING`
- Current plan: `docs/superpowers/plans/2026-07-11-v0.4.1-correctness-stabilization.md`
- Current task: reproduce screenshot clipping using the production DPI initialization path and identify why the mapped-Tk contract was false-positive
- Latest RED: Tom's 2026-07-11 screenshot shows the Reset Credit row clipped in the actual v0.4.1 candidate despite all-step Tk tests passing
- Root-cause hypothesis: UI tests instantiate `Pet` without production `enable_dpi_awareness()`; production has reported 120-DPI window metrics while tests measured 96-DPI row heights
- Latest GREEN: error-presentation fixes remain test-protected; clipping has no valid GREEN evidence
- Latest verification: release administration stopped; no branch push/PR/tag/Release performed; screenshot is authoritative contradictory evidence
- Human fact required: `None`
- Blocker: `None`
- Next exact action: run an isolated production-order DPI/Tk geometry probe, define a failing regression that reproduces the screenshot, and re-verify the bounded design before changing production layout
- Last updated: 2026-07-11
