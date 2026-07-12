# CLOSED GOAL — v0.5.2 Rendered Visibility Incident Investigation

> **Status:** CLOSED — NO RELEASE / NO PRODUCT DEFECT REPRODUCED
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released product baseline:** `v0.5.1`
> **v0.5.1 release commit:** `10de01410126a1877ac9406fc02e3bc583659df3`
> **v0.5.2 product version:** NOT CREATED
> **v0.5.2 tag / GitHub Release:** NONE
> **Production code change required:** NO

## Terminal finding

The supplied clipping screenshot was genuine, but it came from PID 7164, a stale in-memory process started before the v0.5.1 fix was committed or released. Reading the later on-disk `APP_VERSION` and Git HEAD beside that process incorrectly attributed v0.5.1 to code it had never loaded.

After a provenance-correct restart, released v0.5.1 did not reproduce the defect. The exact HWND client showed all five real production rows, including the complete `reset_credit` row.

## Reconciled truth

- Released product baseline: v0.5.1 at `10de014`.
- Screenshot incident: resolved as stale pre-fix process / incorrect version attribution.
- Released v0.5.1 product defect reproduced: No.
- Production code change required: No.
- v0.5.2 product version: Not created.
- v0.5.2 tag / GitHub Release: None.
- Design Verification: FAILED because the required released-v0.5.1 RED could not be established.
- Investigation status: CLOSED — NO RELEASE / NO PRODUCT DEFECT REPRODUCED.
- Blocker: None.
- v0.6.0 Productization design: unblocked, but not started and requires Tom's next direction.

## Historical evidence

- PR #17 and release v0.5.1 remain valid historical facts.
- PR #18 remains the v0.5.1 release-state reconciliation.
- PR #19 preserves the provenance audit and Design Verification failure.
- `docs/quality/test-records/2026-07-11-v0.5.2-rendered-visibility-investigation.md` remains the authoritative incident record.
- `docs/superpowers/specs/2026-07-11-v0.5.2-rendered-visibility-design.md` remains the authoritative failed Design Verification record.

The original terminal path—released-v0.5.1 RED, production fix, and v0.5.2 release—is superseded because investigation disproved its prerequisite. No RED, production change, tag, or Release may be manufactured to satisfy the obsolete path.

## Stop condition

Do not begin v0.6.0 brainstorming or implementation. Wait for Tom to choose the next product direction.
