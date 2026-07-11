# Execution State

- Active phase: `Phase 1 — Correctness Stabilization` release verification after DPI-aware correction
- Active version: `0.4.1`
- Branch / HEAD: `fix/v0.4.1-correctness` / `97b9e772eb5f80f495c63fed7593f3452d3a3624`; remote branch not created
- Active skill: `systematic-debugging`
- Current design/spec: `docs/superpowers/specs/2026-07-11-v0.4.1-correctness-stabilization-design.md`; DPI-aware revision is `DESIGN VERIFIED`
- Current plan: `docs/superpowers/plans/2026-07-11-v0.4.1-correctness-stabilization.md`
- Current task: complete exact-build documentation, Quality/RC, PR/CI, merge, and v0.4.1 release reconciliation
- Latest RED: Tom's 2026-07-11 screenshot shows the Reset Credit row clipped in the actual v0.4.1 candidate despite all-step Tk tests passing
- Root cause: the old mapped-Tk test skipped production `enable_dpi_awareness()` and mixed Tk point fonts with unscaled physical-pixel geometry, so it passed at 96 DPI while the production 120-DPI path clipped every scale step
- Latest GREEN: production-order isolated Tk probe reports effective DPI 120 and `all_fit=true` for all 25 scale steps; 80% Reset Credit allocation/request is 23/23 px; root launcher has one exact-repository `pythonw.exe` and no persistent CMD
- Latest verification: final branch Quality passed 130 core + 22 Tk tests; package smoke passed; strict readiness reports zero blockers; full Release Candidate is approved
- Human fact required: `None`
- Blocker: `None`
- Next exact action: commit final evidence, push the verified branch, create the v0.4.1 PR, and monitor exact-head CI
- Last updated: 2026-07-11
