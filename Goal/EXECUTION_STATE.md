# Execution State

- Active phase: `Phase 1 — Correctness Stabilization`; Phase 0 reconciliation complete locally
- Active version: `0.4.1`
- Branch / HEAD: local `main` / `02ab1f60a1e8a6b91e4b212bb47773e88d068c84`; equals `origin/main`
- Active skill: `verification-before-completion`; `systematic-debugging` used for Phase 0 governance and RC decoding failures
- Current design/spec: `Goal/ACTIVE_VERSION_BRIEF.md`; Phase 1 design verification is `PENDING`
- Current plan: `docs/superpowers/plans/2026-07-11-repository-truth-and-baseline.md`
- Current task: begin Phase 1 clipping/error-path investigation and Design Verification
- Latest RED: baseline Quality failed because `Goal/CODEX_PROJECT_RENEWAL_ACTIVE_GOAL.md` existed as an unapproved second Goal file
- Root cause: the supplied file explicitly required replacement of `ACTIVE_GOAL.md`; the replacement had not yet occurred, and governance correctly rejected the duplicate
- Latest GREEN: Goal governance, manifest, links, 17 document pairs, Quality, package smoke, strict readiness, whitespace, and strict RC pass after reconciliation
- Latest verification: 124 core and 17 UI tests passed; active normative LOC reduced from 2,675 to 1,012; runtime Python files/LOC and dependencies remain 39/2,702 and 2
- Human fact required: `None`
- Blocker: `None`
- Next exact action: create a v0.4.1 work branch, reproduce clipping and both legacy error paths, and complete Design Verification before production changes
- Last updated: 2026-07-11
