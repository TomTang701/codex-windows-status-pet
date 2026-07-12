# ACTIVE GOAL — v0.5.2 Rendered Content Visibility Contract Correction
> **Status:** ACTIVE
> **Released baseline:** `v0.5.1`
> **v0.5.1 release commit:** `10de01410126a1877ac9406fc02e3bc583659df3`
> **Current reconciled main baseline:** `71c2719fca0ac4cfe3fa9ce1ffb6d675fe074fa8`
> **Scope:** one correctness incident plus correction of the verification authority that falsely approved it
> **Productization:** `v0.6.0` is BLOCKED
> **Execution:** autonomous-first, evidence-first, systematic-debugging, Design Verification, TDD, verification-before-completion
> **Remote workflow:** repository `AGENTS.md` standing authorization applies to routine GitHub operations inside this Goal
---
## 0. Mission
Released `v0.5.1` still shows a production-visible defect:
> The fifth status row, containing the manual reset count / reset time information, can remain visibly clipped by the bottom edge of the expanded window.
The new production screenshot is an authoritative counterexample to the previous rendered-visibility completion claim.
This Goal has two inseparable outcomes:
1. find and fix the real remaining rendered-content visibility defect;
2. correct the verification authority that repeatedly approved the defect as fixed.
The Goal is not to make another geometry guess pass.
The Goal is:
> **Make the real five-row rendered result correct, and make the release gate capable of catching the same visible failure before release.**
Default rule:
> **Reproduce the real symptom. Explain the false positive. Fix one root cause. Verify at the rendered boundary.**
---

## 1. Historical truth and active-state correction

Do not rewrite release history.

These remain facts:

- `v0.5.1` was released;
- PR `#17` was merged;
- `10de01410126a1877ac9406fc02e3bc583659df3` is the released v0.5.1 code commit;
- PR `#18` reconciled the release state;
- prior Quality, Tk, DPI/scale, lifecycle, and RC checks passed under their then-current contracts.

The new screenshot changes the interpretation of that evidence:

```text
v0.5.1 release = historical fact
v0.5.1 rendered-visibility completion claim = INVALIDATED BY NEW PRODUCTION EVIDENCE
prior checks = insufficient authority for the visible outcome
current root cause = UNKNOWN / UNDER INVESTIGATION
v0.5.2 = ACTIVE
v0.6.0 Productization = BLOCKED
```

Before further technical work, reconcile:

- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`

Replace the current completed Goal with this v0.5.2 Goal.

Do not reopen v0.5.1 as if the release never happened.

---

## 2. Why this is a verification-authority incident

Multiple completion claims for this clipping family have now been invalidated by real runtime evidence.

Previous approaches included:

- fixed/proportional height correction;
- DPI-aware content-fit validation;
- startup/runtime DPI reconciliation;
- target-DPI pixel fonts;
- 25 scale steps;
- DPI 96/120 coverage;
- 15 lifecycle transitions;
- formal RC with zero blockers.

The fifth row is still visibly clipped.

Repository engineering rules require stopping speculative patch stacking after repeated failed fixes and reassessing architecture, assumptions, or the problem definition.

Therefore:

> **Do not make another production geometry, padding, font, or DPI-order patch until the old verification authority has been audited and a stronger RED reproduces the real symptom.**

This Goal explicitly permits questioning:

- fixed proportional expanded height as final height authority;
- Tk requested/allocated geometry as proof of rendered glyph completeness;
- direct-method lifecycle tests as production-equivalent evidence;
- static synthetic row strings as sufficient presentation evidence.

This Goal does not authorize a UI framework rewrite.

---

## 3. Protected product core

Preserve unless exact root-cause evidence proves a protected contract itself must change.

### Data and privacy

- Local official Codex app-server remains the quota source.
- Activity uses approved local Codex session metadata.
- Do not read `auth.json` or Codex access tokens.
- Do not add third-party quota providers, telemetry, a backend, or hosted service.
- Do not expose prompt, response, session content, tokens, or credentials.

### Runtime

- Windows 11 x64 remains the supported baseline.
- Only one companion instance may run.
- Workers must not call Tk APIs directly.
- Tk/UI work stays on the main thread.
- Refresh remains bounded and single-flight.
- Shutdown remains safe and idempotent.
- Normal launch does not require a persistent console.

### User-visible behavior

Keep exactly five stable row identities:

```text
activity
progress
primary_5h
weekly
reset_credit
```

Preserve:

- truthful activity/quota presentation;
- validated and recoverable settings;
- Apply / Save / Close / Restore Defaults semantics;
- canonical `window_scale_percent` and configuration compatibility;
- Hide/Show and Compact/Expand;
- drag/lock and topmost;
- legal position recovery and tray reachability;
- restart persistence.

Width scaling semantics remain protected unless evidence requires a compatible correction.

Fixed proportional expanded height is not protected merely because old tests encode it.

---

## 4. Required workflow

Route this work as:

```text
using-superpowers
→ systematic-debugging
→ verification-authority audit
→ production-equivalent reproduction
→ one primary root-cause hypothesis
→ compare 2–3 minimum fixes
→ DESIGN VERIFICATION
→ writing-plans when multi-step coordination requires it
→ test-driven-development
→ minimum root-cause fix
→ verification-before-completion
→ authorized GitHub release workflow
→ active-state reconciliation
→ STOP
```

No production fix before Design Verification.

Do not ask Tom to confirm machine-readable facts.

Do not require Tom to visually approve the same clipping fix again when an automated rendered-boundary contract can verify it.

---

## 5. Phase 1 — prove exact production provenance

Autonomously inspect the running application represented by the failure.

Record:

- PID and executable;
- full CommandLine;
- loaded script/module path where safely inspectable;
- reported application version;
- repository/worktree relationship;
- current branch/HEAD for the running source path when applicable;
- relationship to `71c2719fca0ac4cfe3fa9ce1ffb6d675fe074fa8`;
- relationship to v0.5.1 `10de01410126a1877ac9406fc02e3bc583659df3`;
- working-tree state;
- HWND;
- outer window rect and client rect;
- monitor identity and work area;
- `GetDpiForWindow`;
- safe non-secret persisted settings snapshot;
- logical `window_scale_percent`;
- actual root geometry.

Do not ask Tom whether:

- the newest version is running;
- the app was restarted;
- the screenshot is really v0.5.1;
- the correct branch is active.

Determine these facts from process, filesystem, Git, source, Tk, and Win32 evidence.

If provenance disproves v0.5.1 execution, prove that first and resolve the runtime mismatch before layout diagnosis.

---

## 6. Phase 2 — audit the v0.5.1 verification authority

Audit every check used to support:

- `50 DPI/scale combinations fit`;
- `15 lifecycle transitions fit`;
- `all five rows visible`;
- `formal RC zero blockers`;
- `v0.5.1 clipping fixed`.

Produce:

```text
claim
→ authoritative check
→ exact observable measured
→ blind spot
→ why the production screenshot could still fail
```

Inspect at minimum:

- `tests/test_content_fit.py`;
- DPI content probe;
- lifecycle transition probe/tests;
- settings tests;
- Compact/Expand and Hide/Show tests;
- RC/readiness checks consuming those results;
- PR #17 completion evidence;
- active release records that promoted those checks into release authority.

The audit must identify the exact false-positive mechanism.

Do not stop at:

> “the test missed this transition.”

Measure whether the blind spot is:

- `winfo_reqheight() <= winfo_height()` being used as a proxy for visible glyph completeness;
- label bounds checked only against `StatusRows` rather than final client/render output;
- static `APPROVED_ROWS` differing from real production presentation strings;
- direct method calls bypassing real settings/menu/Toplevel/grab/focus/`after_idle` behavior;
- missing asynchronous `poll → render_status → configure_rows` updates after lifecycle transitions;
- insufficient event-loop stabilization;
- font metrics differing from rasterized glyph bounds;
- negative-pixel font/Tk scaling behavior not represented by the check;
- HWND outer/client geometry differences;
- DPI lifecycle timing;
- another measured mechanism.

Do not choose the answer in advance.

---

## 7. Phase 3 — reproduce the real symptom, not a proxy

Create a RED against the exact released v0.5.1 implementation.

Use one long-lived, production-equivalent `Pet`.

Use the real production presentation route.

Do not rely only on handwritten `APPROVED_ROWS`.

Drive the real UI lifecycle where practical:

- settings open;
- Apply;
- Save;
- Close rollback;
- lock;
- Hide/Show;
- Compact/Expand;
- relevant menu/tray dispatch;
- relevant `after` / `after_idle` callbacks.

Include real presentation updates:

```text
queue/poll
→ activity/quota state
→ render_status()
→ presentation controller
→ five-row mapping
→ StatusRows.configure_rows()
```

At relevant boundaries capture:

- logical scale;
- effective DPI;
- monitor/work area;
- WindowMetrics;
- every geometry request and caller;
- relevant `<Configure>` events;
- root requested/actual geometry;
- HWND outer rect and client rect;
- pack order/options;
- text container requested/actual geometry;
- `StatusRows` requested/actual geometry;
- all five row texts and label bounds;
- each label's requested/actual width and height;
- each label's bottom boundary;
- internal border/padding/highlight values;
- Tk font specification and metrics;
- state before/after `render_status()`;
- state before/after `configure_rows()`;
- relevant pending `after` / `after_idle` callbacks.

Required RED:

```text
same real Pet
→ cold-start five-row rendered result is valid
→ execute exact or autonomously discovered production-equivalent interaction sequence
→ execute real production presentation update
→ fifth row violates the actual visible client/render boundary
```

A RED based only on:

```text
winfo_reqheight() > winfo_height()
```

is insufficient unless Phase 2 proves that condition is the exact production failure.

The RED must fail released v0.5.1 for the same underlying visible reason represented by the screenshot.

---

## 8. Phase 4 — choose the correct visibility authority

Compare at least three minimum approaches.

### A. Corrected Tk/native rendered-line measurement

Use actual production text, active font, mapped row composition, font line metrics, padding/border, and actual client boundary.

Use only if it demonstrably distinguishes released v0.5.1 failure from the corrected result.

### B. Content-derived expanded height

Derive expanded physical height from the actual five mapped rows and current DPI/font composition rather than treating fixed proportional height as final authority.

Allowed if evidence proves fixed proportional height cannot guarantee the five-row text surface.

Avoid geometry feedback loops or unstable resizing.

### C. Minimal host-only HWND/client capture

Capture only this application's HWND/client area and verify that the fifth-row rendered region is not truncated at the client bottom.

Use only if geometry/font metrics cannot truthfully observe the rendered defect.

Do not build a general screenshot-testing framework.

Selection rule:

> Choose the least complex authority that fails released v0.5.1 for the real symptom and remains trustworthy after the minimum fix.

---

## 9. Design Verification Gate

Before production code changes, record all of the following.

### Problem evidence

- exact production provenance;
- exact failing runtime state;
- exact reproducible interaction sequence;
- exact final client/render failure.

### False-positive explanation

Explain:

- why scale/DPI checks passed;
- why the 15 lifecycle checks passed;
- why RC remained zero-blocker;
- the precise verification blind spot.

### One primary root-cause hypothesis

The hypothesis must explain:

```text
why an earlier/cold state can look correct
why the failing runtime state clips
why old checks pass
why the new RED fails
```

### Observable contract

Define “fully visible” at the authoritative boundary.

At minimum:

- exactly five stable rows exist;
- all five real production strings are mapped;
- approved single-line rows remain single-line;
- no row is vertically truncated;
- the fifth row's full rendered line region stays above the actual visible client bottom;
- lifecycle and presentation updates preserve the contract;
- DPI change ends in a coherent target-window layout.

### Regression surface

Cover:

- startup;
- settings open/Apply/Save/Close/Defaults;
- lock;
- Hide/Show;
- Compact/Expand;
- monitor/DPI transition;
- asynchronous activity update;
- asynchronous quota update;
- five-row tray/error presentation where applicable.

### RED quality question

Answer:

> **Would this exact RED have failed and blocked the released v0.5.1 build represented by the production counterexample?**

If not demonstrably yes:

```text
DESIGN VERIFICATION = FAILED
→ return to investigation
```

Do not implement.

---

## 10. Implementation constraints

After Design Verification:

```text
RED
→ minimum root-cause fix
→ GREEN
→ focused refactor only when directly required
```

Forbidden shortcuts:

- arbitrary `+N px`;
- scale-specific height exceptions without root-cause evidence;
- random padding reductions;
- another unverified DPI-order patch;
- changing row text to hide the defect;
- removing the fifth row;
- shrinking the font merely to fit;
- disabling settings, lock, Hide/Show, or Compact to avoid reproduction;
- UI framework rewrite;
- new general layout subsystem;
- new manager/controller/service/module unless the current owner is proven insufficient;
- installer/productization work;
- unrelated cleanup.

Prefer the existing owner of the proven root cause.

One root cause.

One minimum fix.

---

## 11. Required verification

The release claim is:

> **The production-equivalent five-row rendered result remains fully visible through the reproduced failing lifecycle and presentation sequence.**

### Exact defect regression

Run the new RED against:

1. released v0.5.1 behavior — FAIL for the expected real reason;
2. v0.5.2 candidate — PASS.

Preserve before/after evidence.

### Real production presentation

Verify actual production row content through the real presentation route.

Static synthetic strings cannot be the only authority.

### Long-lived lifecycle

Use the same long-lived `Pet` through the relevant sequence.

Fresh `Pet` per transition cannot be the only lifecycle authority.

### Asynchronous updates

Verify after the failing lifecycle:

- activity update;
- quota update;
- fifth-row Reset Credit update.

### Scale and DPI

Run affected supported-scale checks.

Retain DPI 96/120 checks where available.

Scale/DPI matrix success alone is not proof of rendered visibility.

### Repository gates

Run fresh:

- focused regression;
- relevant Tk integration;
- core tests;
- `python scripts/run_quality_checks.py`;
- package smoke;
- strict readiness/compatibility when required;
- formal RC;
- `git diff --check`;
- complete diff review;
- unrelated-change check;
- secret/credential scan.

Completion evidence must name the corrected rendered-visibility authority separately from generic test counts.

---

## 12. GitHub and release workflow

Repository `AGENTS.md` grants standing authorization for routine GitHub workflow operations within the current active Goal.

After required verification passes, autonomously execute:

```text
verify repository/remote/account
→ push verified v0.5.2 branch
→ create PR
→ monitor CI
→ investigate evidence-backed CI failures
→ fix only v0.5.2 scope
→ rerun required verification
→ push verified correction
→ CI success
→ exact PR head verification
→ squash merge
→ synchronize and verify main
→ create/push v0.5.2 tag
→ create GitHub Release
→ verify tag/Release target
→ delete completed merged release branch
→ active-state reconciliation
```

Do not request repeated authorization for normal:

- branch push;
- PR creation/update;
- CI monitoring and verified correction push;
- squash merge after gates pass;
- main verification;
- v0.5.2 tag/Release;
- merged release-branch cleanup.

Standing authorization does not permit high-risk actions excluded by repository `AGENTS.md`, including force push, history rewrite, repository/permission/secrets changes, owner/target changes, credential access, or destructive unrelated Git operations.

---

## 13. Release-state reconciliation

After v0.5.2 is actually merged, verified, tagged, and released, inspect and update only authoritative files whose facts changed:

- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`
- version sources;
- changelog;
- directly affected testing/architecture docs.

Final truth must distinguish:

```text
v0.5.1 = released historical version
v0.5.1 rendered-visibility claim = invalidated by later production counterexample
v0.5.2 = released correction
new rendered-visibility authority = named and evidenced
v0.6.0 = not started
```

---

## 14. Completion criteria

This Goal is COMPLETE only when all are true.

### Provenance

- exact failing runtime provenance was machine-verified.

### False-positive mechanism

- the exact reason old visibility checks passed while the production screenshot failed is documented with evidence.

### Reproduction

- released v0.5.1 is reproduced by a production-equivalent RED for the same underlying visible failure.

### Verification authority

- one authoritative rendered-visibility check is named;
- it fails released v0.5.1 for the expected reason;
- it passes the corrected candidate;
- its blind spots are explicit;
- generic geometry-fit checks are not presented as rendered-completeness proof when they are not.

### Correctness

- all five production rows are completely visible at the authoritative boundary;
- the fifth row is not bottom-clipped;
- the reproduced runtime lifecycle remains correct after real presentation updates.

### Regression safety

- protected core remains intact;
- affected lifecycle, presentation, DPI, and scale checks pass;
- no arbitrary pixel patch or unrelated subsystem was added.

### Release

- Quality and required release gates pass;
- exact-head CI succeeds;
- v0.5.2 is squash-merged;
- merged main is verified;
- v0.5.2 tag and Release target the verified commit;
- merged release branch is cleaned;
- active state is reconciled.

---

## 15. Mandatory stop condition

After v0.5.2 release and active-state reconciliation:

> **STOP.**

Do not:

- begin v0.6.0 brainstorming;
- create a v0.6.0 ACTIVE_GOAL;
- implement installer/uninstaller;
- implement startup selection;
- create productization artifacts;
- continue feature development.

Set final `EXECUTION_STATE` next action to:

```text
Wait for Tom to review the v0.5.2 verification-authority correction and choose the next product direction.
```

---

## Final operating principle

> **The screenshot is a real counterexample. Passing geometry numbers are not permission to deny visible failure. Reproduce the rendered defect, repair the verification authority, fix one root cause, prove the real output, release, reconcile, and stop.**
