# ACTIVE PROGRAM GOAL – v0.5.5 Release Completion → v0.6.0 Delivery

> **Status:** ACTIVE PROGRAM / SEQUENTIAL VERSION DELIVERY
> **Released baseline:** `v0.5.3`
> **Historical v0.5.4:** closed position-persistence investigation without product release
> **New production evidence date:** `2026-07-12`
> **Scope:** v0.5.5 release completion followed by v0.6.0 battery and layout delivery
> **Target product version:** `v0.5.5` only if the defect is reproduced, root cause is proven, the minimum fix passes verification, and release gates succeed
> **v0.6.0:** automatically activates only after the v0.5.5 hard version gate
> **Execution:** systematic-debugging → production-equivalent RED → root-cause proof → Design Verification → writing-plans → TDD → minimum fix → verification-before-completion → authorized release workflow → state reconciliation → STOP

---

## 0. Mission

Investigate and correct the newly reproducible startup position shift on a mixed-DPI multi-monitor desktop.

Tom has identified a specific physical pattern:

```text
primary monitor scale = 125%
secondary monitor scale = 100%

primary monitor:
restart preserves the saved position at tested locations

secondary monitor:
normal interior positions restart correctly
positions near the right or bottom work-area edge can restart shifted inward
```

The prior v0.5.4 A-path proved that one drag → tray Exit → restart path preserved `(4143, 1182)`.

That historical result remains true for the tested coordinate and path.

It is no longer sufficient authority for the position-persistence product contract because the newly discovered failure is spatially conditional and DPI-topology dependent.

The new production evidence changes the active interpretation:

```text
v0.5.4 closure = historical fact
v0.5.4 no-product-release classification = historical fact
v0.5.4 A-path trace = valid for its tested coordinate
"position persistence has no reproducible defect" = invalidated by new production evidence
v0.5.5 mixed-DPI startup position recovery = ACTIVE
v0.6.0 = BLOCKED
```

The Goal is not to increase edge tolerance or disable position recovery.

The Goal is:

> **Preserve a saved position that is legal for the target monitor at the target monitor's effective DPI, while still recovering genuinely off-screen positions after display topology changes.**

---

## 1. Primary root-cause hypothesis

Treat the following as a strong hypothesis that must be measured before production code changes:

```text
Pet.__init__
→ root created
→ withdraw()
→ load settings
→ _sync_compatibility_metrics(settings)
→ dpi_for_window(self.winfo_id())
→ withdrawn/bootstrap HWND receives DPI associated with the primary monitor or another non-target monitor
→ derive_window_metrics(..., dpi=bootstrap_dpi)
→ safe_position(saved_x, saved_y)
→ recover_position(saved_x, saved_y, bootstrap_width, bootstrap_height, monitors, fallback)
→ a position that is legal on the 100% secondary monitor for the actual 96-DPI window is evaluated using 125% / 120-DPI physical dimensions
→ rectangle_contained_in_work_area() returns false near the right or bottom edge
→ recover_position() clamps to right - inflated_width and/or bottom - inflated_height
→ saved logical position is replaced in self.settings
→ geometry moves the HWND to the clamped coordinate
→ the HWND later reaches the target secondary monitor and obtains 96 DPI
→ window metrics shrink to the correct target-monitor size
→ original legal saved coordinate has already been lost for this startup
```

This hypothesis explains all currently reported behavior:

- primary 125% monitor positions survive because bootstrap and target DPI agree;
- interior secondary positions survive because both inflated and correct rectangles still fit;
- only near-edge secondary positions shift because inflated startup dimensions cross the work-area boundary;
- the shift is toward the work-area interior because `recover_position()` clamps against `right - width` and `bottom - height`;
- the prior `(4143, 1182)` A-path can pass when that tested coordinate is not inside the narrow edge-sensitive region.

Do not declare this root cause proven until the first incorrect boundary is measured.

---

## 2. Historical truth and active-state correction

Preserve repository history.

These remain facts:

- `v0.5.3` is the latest released product version.
- PR `#23` closed v0.5.4 as an investigation without product release.
- merged main closure commit is `e7cca6e8c934186ca11752496b119dc58460e608`.
- v0.5.4 has no product tag or GitHub Release.
- investigation commit `5d3e453` proved one production-equivalent A-path retained `(4143, 1182)`.
- no production persistence correction was shipped as v0.5.4.

Do not rewrite v0.5.4 as a failed product release.

Do not delete its valid investigation evidence merely because a narrower reproduction has now been found.

Before implementation, reconcile the authoritative active state to show:

```text
released baseline = v0.5.3
v0.5.4 = historical closed investigation / no product release
new physical evidence = mixed-DPI edge-sensitive startup shift reproduced by Tom
active correction = v0.5.5 Mixed-DPI Startup Position Recovery Correctness
v0.6.0 = blocked / not started
```

Update only authoritative active-state documents that must change, including as applicable:

```text
Goal/ACTIVE_GOAL.md
Goal/ACTIVE_VERSION_BRIEF.md
Goal/EXECUTION_STATE.md
docs/product/ROADMAP.md
paired Chinese canonical translation when required
```

---

## 3. Protected product behavior

Preserve unless root-cause evidence proves an exact contract must change.

### Position behavior

- Dragged positions remain persisted.
- Signed virtual-desktop coordinates remain valid.
- Legal multi-monitor positions remain unchanged across restart.
- Genuinely disconnected/off-screen positions are recovered to a reachable work area.
- Intentional positions near a right or bottom work-area edge must not be moved merely because startup temporarily uses a different monitor DPI.
- Hide/Show position semantics remain stable.
- Compact/Expand position semantics remain stable.
- Settings Apply / Save / Close / Restore Defaults semantics remain transactional.

### Window and DPI behavior

- Canonical `window_scale_percent` remains the user-visible size authority.
- Physical window metrics remain DPI-aware.
- Target-window DPI geometry and font behavior remain protected.
- Mixed-DPI monitor transitions must end in one coherent target-monitor metric set.
- Do not globally force 96 DPI.
- Do not globally force primary-monitor DPI.
- Do not disable per-monitor DPI awareness.

### Runtime and Shell identity

Preserve:

```text
desktop overlay = visible
tray icon = visible
WS_EX_TOOLWINDOW = true
WS_EX_APPWINDOW = false
ordinary taskbar application identity = absent
Alt+Tab / Win+Tab ordinary app presence = absent
```

Also preserve:

- Windows 11 x64 baseline;
- single instance;
- main-thread Tk ownership;
- bounded single-flight refresh;
- safe idempotent shutdown;
- no persistent console requirement.

### Data and privacy

Preserve all existing local-data boundaries.

Do not add telemetry, hosted services, third-party quota providers, token readers, or Codex core modifications.

---

## 4. Required workflow

Route this Goal as:

```text
using-superpowers
→ systematic-debugging
→ exact mixed-DPI reproduction
→ startup geometry/DPI boundary trace
→ one primary root-cause hypothesis
→ compare minimum correction approaches
→ DESIGN VERIFICATION
→ writing-plans when multi-step coordination is required
→ test-driven-development
→ minimum root-cause fix
→ verification-before-completion
→ authorized GitHub release workflow
→ active-state reconciliation
→ STOP
```

Iron rule:

> **NO PRODUCTION POSITION OR DPI FIX BEFORE THE CURRENT MAIN BUILD FAILS A RED FOR THE NEW 125% PRIMARY / 100% SECONDARY EDGE CASE.**

Do not guess from the production report alone.

The report defines the reproduction shape; the first wrong boundary must still be measured.

---

## 5. Phase 1 — prove exact running provenance and physical topology

Inspect the currently running instance used for the reproduction.

Record:

- PID;
- executable;
- full CommandLine;
- loaded source path where safely inspectable;
- application version;
- repository branch and HEAD for the running source;
- relationship to merged main `e7cca6e8c934186ca11752496b119dc58460e608`;
- working-tree state;
- settings path;
- root HWND;
- current window rectangle;
- current client rectangle;
- current monitor identity;
- monitor rectangles and work areas;
- primary-monitor identity;
- per-monitor DPI values as observed by the existing display API and Win32 authority available to the process;
- effective `GetDpiForWindow` for the real root HWND.

Confirm the physical topology relevant to the report:

```text
primary monitor = 125% / expected effective DPI approximately 120
secondary monitor = 100% / expected effective DPI approximately 96
```

Use measured DPI values as authority rather than relying only on Windows Settings labels.

Do not ask Tom whether the process is current when machine-readable provenance can establish it.

---

## 6. Phase 2 — reproduce the edge-sensitive failure

Use current main before any production fix.

Find one legal secondary-monitor coordinate satisfying all of the following:

```text
target monitor = measured 100% / 96-DPI secondary
saved coordinate is inside the target work area
correct target-DPI window rectangle is fully contained in the target work area
same coordinate evaluated with measured bootstrap/primary 125% / 120-DPI metrics is not fully contained
coordinate is near the secondary right edge, bottom edge, or bottom-right region
```

Prefer deriving this coordinate from measured work area and real `WindowMetrics` rather than hard-coding Tom's machine coordinates into permanent tests.

Conceptually:

```text
target_width_96 = derive_window_metrics(scale, dpi=96).width
target_height_96 = derive_window_metrics(scale, dpi=96).height
bootstrap_width_120 = derive_window_metrics(scale, dpi=120).width
bootstrap_height_120 = derive_window_metrics(scale, dpi=120).height

choose saved_x such that:
saved_x + target_width_96 <= secondary_right
saved_x + bootstrap_width_120 > secondary_right + allowed_rounding_tolerance

and/or choose saved_y such that:
saved_y + target_height_96 <= secondary_bottom
saved_y + bootstrap_height_120 > secondary_bottom + allowed_rounding_tolerance
```

Run the real startup path with the saved coordinate.

The required RED is:

```text
saved rectangle is legal using target-monitor DPI metrics
→ current main startup begins
→ startup recovery evaluates the saved coordinate
→ first DPI/metric set used for recovery differs from target-monitor DPI/metrics
→ recover_position marks the legal target coordinate as recovered
→ settings x/y or root geometry changes from the saved coordinate
→ final target-monitor window uses the correct smaller DPI metrics
→ final root position does not equal the legal saved coordinate
```

The RED must fail current main for the same mechanism as the physical symptom.

A pure assertion that two DPI metric sizes differ is insufficient.

A test that manually calls `recover_position()` with intentionally wrong dimensions is insufficient by itself.

The authoritative RED must include the startup decision path that selects those dimensions.

---

## 7. Phase 3 — trace the first wrong boundary

Instrument the minimum safe startup boundaries.

Capture, in order:

```text
raw persisted x/y
raw loaded settings x/y
root mapped/withdrawn state
root HWND
root rectangle before initial recovery
GetDpiForWindow before initial recovery
window_dpi before initial recovery
logical window_scale_percent
WindowMetrics width/height before initial recovery
monitor containing saved x/y
saved-point target monitor DPI
saved-point target monitor work area
safe_position input
recover_position width/height input
rectangle_contained result per work area
recover_position output and recovered flag
settings x/y immediately after safe_position
first geometry request
GetDpiForWindow after first geometry/update_idletasks
WindowMetrics after DPI resync
final geometry request
final root x/y
final effective window DPI
final monitor identity
persisted JSON before and after startup
```

The investigation must identify the first exact boundary where:

```text
expected coordinate = original legal saved coordinate
actual coordinate = changed/clamped coordinate
```

Answer explicitly:

1. What DPI did the root HWND report before the saved coordinate was placed?
2. Which monitor did that DPI correspond to?
3. What DPI belongs to the monitor containing the saved coordinate?
4. What width/height did `safe_position()` use?
5. What width/height should define containment for the saved coordinate's target monitor?
6. Did the inflated or otherwise wrong metrics alone make `rectangle_contained_in_work_area()` change from true to false?
7. Did `recover_position()` produce exactly the observed inward shift?
8. After the HWND reached the secondary monitor, did the effective DPI/metrics become correct while the coordinate remained already clamped?

Do not proceed to implementation unless these questions establish one coherent mechanism or the evidence establishes a different exact root cause.

---

## 8. Verification-authority audit

Audit why `tests/test_ui_position_persistence.py` and the v0.5.4 A-path passed.

The audit must compare:

```text
v0.5.4 tested coordinate
vs
new edge-sensitive coordinate

v0.5.4 tested monitor DPI
vs
bootstrap DPI
vs
new target secondary DPI

correct target-DPI rectangle containment
vs
bootstrap-DPI rectangle containment
```

Determine whether `(4143, 1182)` simply remained inside the target work area even under the larger bootstrap metric rectangle.

Also inspect the test lifecycle.

The retained v0.5.4 test explicitly cancels scheduled callbacks before the close chain. Determine whether that matters to this exact new failure.

Do not assume callback cancellation is relevant merely because it differs from production.

The audit outcome must state the exact false-negative reason.

Preferred form:

```text
old test passed because <measured reason>
new physical case fails because <measured difference>
old test authority was narrower than the claimed mixed-DPI edge-persistence contract because <exact blind spot>
```

---

## 9. Compare minimum correction approaches

After root-cause proof, compare at least these approaches.

### A. Target-monitor DPI recovery metrics

Determine the monitor/work area containing the saved position, obtain the target monitor's DPI through an existing or minimally extended display boundary, derive physical `WindowMetrics` for that DPI, and use those dimensions only for deciding whether the saved rectangle is legal.

Potential advantages:

- recovery decision matches the monitor the saved coordinate actually targets;
- small change near the existing display/recovery boundary;
- preserves immediate off-screen recovery.

Required concern:

- monitor DPI authority must be reliable in the process DPI-awareness mode;
- do not use legacy monitor DPI data blindly if measured evidence shows it does not match effective window DPI.

### B. Bootstrap placement before final recovery

Preserve raw saved x/y during initial bootstrap, position the withdrawn/root HWND onto the saved monitor, allow Windows/Tk to establish the target-window DPI, recompute metrics, then perform legal-position recovery exactly once using target-window metrics before deiconify.

Potential advantages:

- recovery uses actual `GetDpiForWindow` authority for the real HWND;
- avoids separate target-monitor DPI inference.

Required concerns:

- must not visibly flash off-screen;
- must still recover disconnected monitor coordinates;
- must not create geometry/DPI feedback loops;
- must preserve v0.5.3 Shell identity.

### C. Relax containment or increase edge tolerance

Examples:

- increase `edge_tolerance`;
- accept partial intersection;
- skip recovery near right/bottom edges.

Treat this as presumptively rejected unless evidence proves the contract itself is wrong.

Why it is dangerous:

- it hides incorrect metric authority;
- can preserve genuinely unreachable windows;
- the required tolerance would vary with DPI difference and window scale;
- it converts a root-cause bug into a heuristic.

Selection rule:

> Choose the smallest approach that uses the correct geometry authority for the target monitor and still truthfully recovers genuinely invalid positions.

Do not preselect A or B before the RED trace proves the startup sequence.

---

## 10. Design Verification Gate

Before production code changes, record:

### Problem evidence

- exact physical topology;
- exact legal saved coordinate;
- target monitor/work area;
- target DPI;
- bootstrap/root DPI before recovery;
- bootstrap metric width/height;
- correct target metric width/height;
- exact `recover_position` input/output;
- exact final shifted coordinate.

### Root-cause statement

Provide one primary hypothesis in this format:

```text
I think <exact startup authority mismatch> is the root cause because <measured evidence connecting the saved coordinate, DPI-derived dimensions, containment result, clamp output, and final position>.
```

### RED quality question

Answer:

> **Would this exact RED have failed current main at `e7cca6e8c934186ca11752496b119dc58460e608` for the same reason Tom's 125% primary / 100% secondary near-edge restart shifts?**

If the answer is not demonstrably yes:

```text
DESIGN VERIFICATION = FAILED
→ return to investigation
→ do not modify production code
```

### Observable corrected contract

Define:

```text
Given a saved position P on monitor M,
and window scale S,
if the window rectangle derived from S and M's authoritative target DPI is legally contained in M's work area,
startup preserves P exactly.

If P is not legal for any current monitor using the correct relevant geometry authority,
startup recovers P to a reachable current work area.
```

### Regression surface

Cover at minimum:

- 125% primary → 125% primary interior;
- 125% primary → 125% primary right edge;
- 125% primary → 125% primary bottom edge;
- 125% primary + 100% secondary → secondary interior;
- mixed-DPI secondary right edge;
- mixed-DPI secondary bottom edge;
- mixed-DPI secondary bottom-right;
- signed/negative virtual-desktop coordinates when topology supports them;
- genuinely disconnected/off-screen saved position;
- drag → save → tray Exit → restart;
- Hide/Show;
- Compact/Expand;
- settings Apply / Save / Close;
- target-window DPI metric coherence;
- v0.5.3 root-HWND Shell identity.

---

## 11. TDD and implementation constraints

After Design Verification passes:

```text
RED
→ run and confirm expected failure on current main behavior
→ implement one minimum root-cause correction
→ run focused RED and confirm GREEN
→ run recovery regressions
→ run persistence lifecycle regressions
→ refactor only if directly required while tests stay green
```

Prefer modifying the current owners of the proven defect:

```text
scripts/ui/main_window.py
scripts/api/display_api.py
scripts/api/window_recovery_api.py
```

Only touch files actually required by the measured root cause.

Expected test locations include the closest existing authoritative tests, such as:

```text
tests/test_ui_position_persistence.py
existing window recovery tests
existing DPI/runtime geometry tests
```

Do not create a new manager, service, controller, or framework unless the current owners are proven unable to express the correction.

Forbidden shortcuts:

- arbitrary X/Y offsets;
- `+N px` or `-N px` edge corrections;
- increasing `edge_tolerance` solely until the test passes;
- disabling `safe_position()` on startup;
- accepting any intersecting rectangle as valid;
- persisting the clamped coordinate before root-cause correction to hide the startup shift;
- forcing 96 DPI;
- forcing 120 DPI;
- forcing primary-monitor DPI;
- hard-coding Tom's monitor coordinates;
- hard-coding monitor names;
- moving the window to center screen;
- removing disconnected-display recovery;
- delaying position save with arbitrary sleeps;
- rewriting the UI framework;
- broad geometry refactoring;
- v0.6.0 work.

One root cause.

One minimum correction.

---

## 12. Required verification

The release claim is:

> **On mixed-DPI Windows desktops, startup preserves saved positions that are legal at the target monitor's DPI, including near right and bottom work-area edges, while genuinely invalid positions are still recovered.**

Before completion:

1. Run the exact new mixed-DPI edge RED against the pre-fix behavior and record the expected failure.
2. Run the same focused test after the correction and record GREEN.
3. Run all position persistence tests.
4. Run all window recovery tests.
5. Run relevant DPI/runtime geometry tests.
6. Run v0.5.3 Shell identity lifecycle checks.
7. Run:

```powershell
python scripts/run_quality_checks.py
```

8. Run the formal release candidate gate if v0.5.5 is release-bound:

```powershell
python scripts/run_release_candidate_checks.py
```

9. Verify APP_VERSION and all authoritative version surfaces are `0.5.5` only after implementation and release readiness are established.
10. Review the complete diff.
11. Check for unrelated changes.
12. Check for debug artifacts and temporary tracing.
13. Check for secrets or credentials.
14. Check whitespace and repository document consistency.

### Physical mixed-DPI verification

Because Tom's machine currently provides the exact physical 125% primary / 100% secondary topology that revealed the defect, use machine-observable Tk/Win32 evidence whenever possible.

The release must not rely only on synthetic monitor dictionaries if the real host can measure the target HWND, work area, effective DPI, startup coordinate, and final coordinate.

Required physical host evidence should prove, for at least one secondary near-edge legal position:

```text
saved x/y
= loaded x/y
= legal target-DPI position
= startup post-recovery x/y
= final root x/y
```

Also prove one genuinely invalid position is still recovered.

Do not ask Tom for repeated visual approval when the host can measure these facts.

If one physical interaction is genuinely unavoidable, ask one bounded factual question only after documenting the automation methods attempted and why they cannot establish the fact.

---

## 13. Release and version rules

`v0.5.5` is a product patch candidate only after:

```text
current-main RED proven
→ root cause proven
→ Design Verification PASSED
→ minimum correction GREEN
→ regressions pass
→ Quality passes
→ formal RC passes
→ exact-head Windows CI passes where required by repository release workflow
```

If the root cause is not proven or the RED cannot be established:

```text
DO NOT RELEASE v0.5.5
DO NOT CREATE v0.5.5 TAG
DO NOT CREATE GITHUB RELEASE
```

Do not reopen or retag v0.5.4.

Do not create a v0.5.4 product Release.

If release succeeds, reconcile history truthfully:

```text
v0.5.3 = previous released baseline
v0.5.4 = closed investigation / no product release
v0.5.5 = mixed-DPI startup position recovery correctness release
v0.6.0 = not started
```

Follow repository `AGENTS.md` Git, GitHub identity, branch, commit, remote-write, review, verification, and release authorization rules.

Before remote actions inspect:

```text
git remote -v
gh auth status
git config user.name
git config user.email
```

Expected Tom-owned repository/account target:

```text
TomTang701/codex-windows-status-pet
GitHub username = tomtang701
```

Do not infer commit author identity from the Windows username.

---

## 14. Completion report

Report in this order.

### Conclusion

State whether the mixed-DPI startup position shift was reproduced and whether v0.5.5 was released.

### Root cause

Report the first wrong boundary and the measured DPI/metric mismatch.

Do not say only "mixed DPI issue".

### Correction

Report the exact geometry authority changed and why the fix is minimal.

### Verification evidence

Include:

- pre-fix RED result;
- target monitor work area;
- saved coordinate;
- bootstrap DPI/metrics;
- target DPI/metrics;
- pre-fix recovery output;
- post-fix recovery output;
- final root coordinate;
- invalid-position recovery result;
- focused test results;
- Quality result;
- RC result when release-bound;
- exact-head CI result when required;
- final diff review.

### Repository state

Report actual state:

```text
released baseline/latest version = <actual>
v0.5.4 = historical closed investigation / no release
v0.5.5 = <actual status>
v0.6.0 = not started
```

### Remote state

Report actual commit, PR, merge, tag, and GitHub Release results only if those actions were performed.

---

## 15. STOP condition

After one of these outcomes:

### Outcome A — release completed

```text
root cause proven
→ RED/GREEN proven
→ minimum correction verified
→ v0.5.5 release workflow completed
→ active state reconciled
→ final evidence reported
→ STOP
```

### Outcome B — investigation cannot prove the defect mechanism

```text
new physical evidence recorded
→ required RED not established or hypothesis disproven
→ no production correction
→ no v0.5.5 release
→ actual blocker recorded
→ final evidence reported
→ STOP
```

Do not start:

- v0.6.0 5H Battery Indicator;
- layout tightening;
- installer work;
- auto-start integration;
- unrelated refactoring;
- another speculative position patch.

Wait for Tom's next approved Goal.
