# ACTIVE GOAL — v0.5.4 Position Persistence Correctness
> **Status:** ACTIVE
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released baseline:** `v0.5.3`
> **Scope:** one position-persistence correctness release
> **Supported platform:** Windows 11 x64
> **Next product direction:** `v0.6.0 5H Battery Indicator and Layout Tightening` remains deferred until this Goal is released and reconciled
> **Execution:** autonomous-first, evidence-first, systematic-debugging, Design Verification, TDD, verification-before-completion
> **Remote workflow:** repository-root `AGENTS.md` standing authorization applies to routine GitHub workflow inside this Goal
---
## 0. Mission
Restore durable overlay position persistence across a normal user exit and restart.
Confirmed production symptom:
```text
user drags the overlay to a new legal position
→ releases the mouse
→ exits through the tray menu
→ launches the app again
→ overlay returns to the default/original position
```
Tom confirmed the authoritative reproduction is the normal tray Exit path.
Tom also confirmed:
```text
opacity persists across restart
Window Size persists across restart
position does not persist across restart
```
The v0.5.4 product outcome is:
> **A legal stable root position chosen by dragging survives mouse release, normal tray Exit, and the next launch unchanged unless display topology genuinely requires position recovery.**
The real stable post-drag root coordinates are the round-trip truth source.
Default rule:
> **Trace the real coordinates through runtime state, persistence, close, load, recovery, and startup. Find the first divergence. Fix one root cause.**
Do not solve this by adding another blind save.
Do not begin the battery feature.
---
## 1. Historical truth
Preserve repository history:
```text
v0.5.1 = released runtime geometry stabilization
v0.5.2 = closed rendered-visibility investigation; no product release
v0.5.3 = released Windows Shell Identity correctness patch
v0.5.4 = active Position Persistence correctness patch
v0.6.0 battery feature = deferred
```
Do not reopen or rewrite the v0.5.2 investigation.
Do not alter the v0.5.3 shell-identity historical record.
At Goal activation reconcile:
- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`
- required paired Chinese copies
Record v0.5.4 as the only active implementation version.
Avoid duplicating volatile PR, CI, and current-head facts across long-lived active documents.
---
## 2. Protected product core
### Data and privacy
Preserve:
- local official Codex app-server as the quota source;
- approved local Codex session metadata for activity;
- no `auth.json` or token reading;
- no telemetry;
- no backend or hosted service;
- no third-party quota provider;
- no prompt, response, session-content, token, or credential exposure.
### Runtime
Preserve:
- Windows 11 x64 supported baseline;
- single companion instance;
- second launch does not kill unrelated processes;
- all Tk work on the Tk main thread;
- workers never call Tk directly;
- bounded single-flight refresh;
- safe idempotent shutdown;
- no persistent console requirement.
### User-visible behavior
Preserve:
- exactly five stable row identities:
  - `activity`
  - `progress`
  - `primary_5h`
  - `weekly`
  - `reset_credit`
- truthful quota/activity presentation;
- 80–200% canonical Window Size scaling;
- Apply / Save / Close / Restore Defaults semantics;
- Hide/Show;
- Compact/Expand;
- drag/lock;
- topmost;
- legal multi-monitor coordinates;
- restart persistence for settings that already work;
- v0.5.1 target-window-DPI geometry/font authority;
- v0.5.3 Windows Shell Identity.
### v0.5.3 Shell Identity
The released shell contract remains protected:
```text
desktop overlay = visible
tray = visible
Win+Tab / Task View = absent
Alt+Tab = absent
ordinary taskbar application button = absent
```
The current verified real root HWND identity remains:
```text
WS_EX_TOOLWINDOW = true
WS_EX_APPWINDOW = false
```
Do not modify shell-identity behavior unless exact position evidence proves it participates in the first coordinate divergence.
---
## 3. Required workflow
Route the Goal exactly as:
```text
using-superpowers
→ systematic-debugging
→ exact A-path reproduction
→ coordinate data-flow trace
→ first coordinate divergence
→ one primary root-cause hypothesis
→ compare evidence-relevant minimum fixes
→ DESIGN VERIFICATION
→ writing-plans
→ test-driven-development
→ minimum root-cause fix
→ verification-before-completion
→ authorized GitHub release workflow
→ active-state reconciliation
→ STOP
```
Iron rule:
> **NO POSITION FIX BEFORE THE FIRST DIVERGENCE IS IDENTIFIED.**
Do not invoke `writing-plans` for production implementation until Design Verification passes.
Do not assume in advance that the root cause is:
- missing `save_settings()`;
- `hidden_position`;
- `expanded_position`;
- `safe_position()`;
- `recover_position()`;
- Settings Session;
- v0.5.3 shell identity;
- a DPI issue.
Measure first.
---
## 4. Exact A-path reproduction
The authoritative reproduction must match Tom's confirmed path:
```text
Pet A starts
→ drag the visible overlay to a different legal position
→ allow the Tk root geometry to stabilize
→ release the mouse
→ normal tray Exit
→ launch Pet B using the same settings file
→ observe final stable root position
```
Do not use:
- Task Manager termination;
- forced process kill;
- direct `destroy()` as a substitute for tray Exit;
- Settings-dialog position editing;
- manually injected final coordinates as the authoritative reproduction.
A test may invoke the same tray dispatch/close path programmatically, but it must exercise the production route:
```text
tray action "exit"
→ process_tray_actions()
→ close()
→ save_settings()
→ destroy()
```
The target coordinate must:
- differ materially from the initial/default coordinate;
- be known legal under the unchanged test topology;
- not require recovery.
Prefer a known legal secondary-monitor coordinate on the supported Windows host when available.
---
## 5. Round-trip truth source
The truth source is:
> **Pet A's actual stable root coordinates after the drag completes.**
After dragging and settling, record:
```text
expected_x = Pet A winfo_rootx()
expected_y = Pet A winfo_rooty()
```
These are authoritative.
Every later relevant boundary must preserve `(expected_x, expected_y)`:
```text
runtime settings after drag
JSON after finish_drag
settings immediately before normal close
JSON after normal close
Pet B raw loaded settings
Pet B safe_position input
Pet B safe_position output
Pet B final stable root
```
Exception:
```text
display topology genuinely makes the saved coordinates invalid
→ recovery is allowed
```
The authoritative RED must use unchanged topology and a known-valid coordinate so recovery is not expected.
---
## 6. Required coordinate trace
Produce a machine-readable trace or directly assertable equivalent.
At minimum capture:
```text
boundary
actual_root_x
actual_root_y
settings_x
settings_y
persisted_json_x
persisted_json_y
safe_position_input_x
safe_position_input_y
safe_position_output_x
safe_position_output_y
window_metrics_width
window_metrics_height
effective_dpi
monitor identity
monitor work area
```
Required boundary sequence:
```text
Pet A initial
after drag actual root
after drag settings
after finish_drag JSON
before close settings
after close JSON
Pet B raw loaded settings
Pet B before safe_position
Pet B after safe_position
Pet B final root
```
Identify:
> **The first exact state, persistence, recovery, or startup-lifecycle boundary where the intended final root coordinates stop being preserved.**
Do not report only:
```text
position persistence is broken
```
Name the exact first divergence.
---
## 7. Primary root-cause tree
Follow the shortest real reproduction.
### A. Runtime position ownership
This class applies only if:
```text
actual stable root after drag = expected
but runtime position state diverges before persistence
```
Inspect:
- `Pet.start_drag()`
- `Pet.drag()`
- `Pet.finish_drag()`
- actual root geometry
- `settings["x"]`
- `settings["y"]`
- `hidden_position`
- `expanded_position`
- lifecycle callbacks occurring between drag settlement and save
Do not blindly synchronize every position variable after every geometry call.
Identify:
```text
authoritative position owner
→ exact stale consumer
→ first overwrite
```
### B. Persistence handoff
This class applies only if:
```text
runtime settings x/y = expected
but finish_drag persisted JSON differs
```
Inspect:
- `Pet.save_settings()`
- `SettingsPersistenceController.save()`
- `save_settings_atomic()`
- the exact dictionary passed into persistence
- write-protection result
- final JSON
Do not declare generic configuration persistence broken.
Opacity and Window Size already survive restart under the confirmed production path.
### C. Close-time overwrite
This class applies only if:
```text
JSON after finish_drag = expected
but normal tray Exit changes runtime state or final JSON
```
Inspect:
- tray `exit` dispatch;
- `process_tray_actions()`;
- `Pet.close()`;
- callbacks scheduled between `finish_drag()` and `close()`;
- settings immediately before close;
- close-time persistence input.
### D. Startup recovery authority
This class applies only if:
```text
normal-close JSON = expected
Pet B raw load = expected
but safe_position output differs
```
Inspect:
- provisional window metrics;
- target-window DPI;
- monitor/work-area snapshot;
- `Pet.safe_position()`;
- `recover_position()`;
- containment/intersection logic.
A legal saved position under unchanged topology must not be misclassified as invalid.
Do not disable recovery globally.
### E. Startup geometry/lifecycle reapplication
This class applies only if:
```text
safe_position output = expected
but final Pet B root differs
```
Inspect every startup position/geometry boundary:
```text
withdraw
→ initial settings load
→ provisional metric derivation
→ safe_position
→ position-only geometry
→ update_idletasks
→ target-DPI metric sync
→ full geometry
→ apply_settings
→ deiconify
→ ensure_overlay_toolwindow
→ scheduled callbacks
→ final stable root
```
Record every geometry call and caller that can change position.
Do not modify shell identity simply because `deiconify()` is nearby.
---
## 8. Settings Session is secondary only
The confirmed A-path does not open Settings.
Therefore:
> **Settings Session is not a primary root-cause branch.**
Do not investigate Settings Session during the first root-cause trace unless:
```text
the exact A-path cannot reproduce the defect
```
or:
```text
runtime evidence proves a settings dialog/session participates in the actual failing sequence
```
Settings Open/Close/Apply/Save/Defaults remains a final regression surface.
Do not use an unobserved Settings Session theory to justify the production fix.
---
## 9. Authoritative RED
Build one production-equivalent round-trip regression against released/current pre-fix behavior.
Required logical sequence:
```text
Pet A
→ start
→ drag through production drag handlers to legal X,Y
→ settle
→ actual stable root = expected_x, expected_y
→ finish_drag
→ JSON x/y = expected_x, expected_y
→ queue/process normal tray Exit
→ JSON x/y remains expected_x, expected_y
Pet B
→ uses same settings file
→ raw loaded x/y = expected_x, expected_y
→ safe_position input = expected_x, expected_y
→ safe_position output = expected_x, expected_y
→ final stable root = expected_x, expected_y
```
The current implementation must fail this test before the production fix for the same underlying reason Tom observed.
Insufficient REDs:
```text
save_settings() was called
normalize_settings preserves x/y
manual JSON x/y survives load
safe_position pure test only
drag method changes settings only
```
These may be supporting tests but cannot replace the authoritative round trip.
The RED quality question is:
> **Would this exact test have blocked the build before Tom observed “drag → tray Exit → restart → default position”?**
If the answer is not demonstrably Yes:
```text
DESIGN VERIFICATION = FAILED
→ return to reproduction and tracing
```
---
## 10. Candidate minimum fixes
Compare only candidates relevant to the first measured divergence.
### Candidate 1 — runtime position handoff
Use only when runtime state is the first divergence.
Correct the authoritative position owner/consumer boundary.
Reject:
```text
sync settings, hidden_position, expanded_position after every geometry call
```
unless evidence proves each is a required owner.
### Candidate 2 — persistence input/timing
Use only when persistence receives stale coordinates.
Correct the source state or exact handoff timing.
Reject repeated saves used as compensation.
### Candidate 3 — recovery/startup authority
Use only when persisted/load coordinates are correct and startup changes them.
Correct the exact metric, DPI, topology, recovery, or geometry-lifecycle authority.
Reject:
- disabling recovery;
- hard-coding Tom's monitor coordinates;
- suppressing `safe_position()` globally.
### Selection rule
> **Choose the smallest candidate that fixes the first divergence and makes the full authoritative RED green.**
Do not combine candidates speculatively.
---
## 11. Design Verification Gate
Before production behavior changes, record:
```text
DESIGN VERIFIED
Exact A-path reproduction: PASS
Stable post-drag root coordinates captured: PASS
Full drag→Exit→restart RED: PASS
First divergence from intended final root coordinates identified at an exact state/persistence/lifecycle boundary: PASS
One primary root-cause hypothesis: PASS
Minimum candidates compared against evidence: PASS
Recommended minimum fix: PASS
Observable round-trip contract: PASS
v0.5.1 geometry authority protected: PASS
v0.5.3 Shell Identity protected: PASS
Recovery contract protected: PASS
Regression surface: PASS
Scope bounded: PASS
Human verification required: NONE / exact admitted fact
```
Explicitly answer:
> **Would this exact RED have blocked the current build before Tom observed the production position-reset symptom?**
Required answer:
```text
Yes
```
If not demonstrably Yes:
```text
DESIGN VERIFICATION = FAILED
→ return to investigation
```
Do not modify production behavior.
After `DESIGN VERIFIED`, write the exact implementation plan using `writing-plans`.
---
## 12. Implementation constraints
After Design Verification:
```text
RED
→ one minimum root-cause fix
→ GREEN
→ focused cleanup only when directly required
```
Forbidden:
- blind extra save;
- synchronizing every position variable everywhere;
- disabling position recovery;
- changing default position to hide the bug;
- hard-coded production monitor coordinates;
- broad settings refactor;
- battery indicator;
- paw replacement;
- layout tightening;
- compact battery geometry;
- Shell Identity redesign;
- installer/productization;
- auto-update;
- UI framework replacement;
- unrelated lean-core work;
- unrelated historical branch cleanup.
Prefer the existing owner of the proven failing boundary.
A new production module/controller/manager requires evidence that the current owner cannot safely own the correction.
---
## 13. Required regression surface
### Exact defect
Verify:
```text
drag
→ finish_drag
→ persisted JSON
→ normal tray Exit
→ persisted JSON
→ new Pet
→ safe_position
→ final stable root
```
### Position behavior
Cover:
- legal primary-monitor coordinate;
- known legal secondary-monitor coordinate when supported;
- large legal secondary coordinate remains legal;
- invalid/off-screen coordinate still recovers;
- negative virtual-coordinate recovery contracts remain correct;
- drag while unlocked changes position;
- drag while locked does not change persisted position.
### Lifecycle
Cover:
- cold start;
- normal tray Exit;
- restart;
- Hide/Show;
- Compact/Expand;
- lock/unlock;
- settings Open/Close;
- opacity-only Apply;
- scale Apply;
- Save;
- draft change → Close rollback;
- Restore Defaults;
- repeated settings cycles.
### Scale and DPI
Preserve:
- Window Size 80–200%;
- DPI 96 supported path;
- automated DPI 120 path;
- v0.5.1 long-lived geometry transition contract;
- five rows fully visible in expanded mode.
### Shell identity
Run the v0.5.3 real-HWND shell identity regression.
Preserve:
```text
TOOLWINDOW = true
APPWINDOW = false
```
and the named shell exclusion contract.
---
## 14. Required verification
All evidence must be fresh.
### Focused
Run:
- authoritative drag→Exit→restart RED/GREEN;
- first-divergence trace;
- root-cause-specific focused tests.
### Existing product regression
Run:
- v0.5.1 long-lived runtime geometry transitions;
- five-row content-fit;
- settings lifecycle;
- Hide/Show;
- Compact/Expand;
- tray/menu;
- lock/drag;
- single instance;
- shutdown;
- v0.5.3 real-HWND Shell Identity suite.
### Repository gates
Run fresh:
```text
python scripts/run_quality_checks.py
python scripts/package_smoke_test.py
python scripts/run_release_candidate_checks.py
git diff --check
complete diff review
unrelated-change check
sensitive-file / secret scan
version-source consistency
document parity / manifest / links where affected
```
Do not reuse prior v0.5.3 completion output as v0.5.4 evidence.
---
## 15. Version and documentation scope
The patch version is exactly:
```text
0.5.4
```
After runtime GREEN, update version-bearing sources controlled by the repository version checker.
Update only directly affected documentation:
- `CHANGELOG.md`
- `CHANGELOG.zh-CN.md`
- `docs/quality/COMPATIBILITY_MATRIX.md`
- `docs/quality/COMPATIBILITY_MATRIX.zh-CN.md`
- a focused v0.5.4 investigation/test record
- active Goal/version/execution state
- roadmap and required paired copy
The investigation/design/implementation records must not claim the root cause before evidence proves it.
Do not document battery behavior as implemented.
---
## 16. GitHub and release workflow
After fresh verification passes, use repository `AGENTS.md` standing authorization:
```text
verify repository / remote / GitHub identity
→ push verified v0.5.4 branch
→ create PR
→ verify exact PR head
→ monitor Windows Quality CI
→ investigate failures using systematic-debugging
→ focused TDD correction if required
→ rerun required verification
→ squash merge
→ synchronize main
→ verify merged main
→ run merged-main formal RC
→ create and push annotated v0.5.4 tag
→ create GitHub Release
→ verify tag and Release target
→ delete completed merged v0.5.4 branch
→ active-state reconciliation
```
Do not repeatedly request normal Goal-scoped GitHub authorization.
High-risk exclusions in repository `AGENTS.md` remain separately permissioned.
---
## 17. Release-state reconciliation
After v0.5.4 is actually merged, verified, tagged, and released, reconcile the authoritative state.
Final truth must be:
```text
v0.5.3 = previous released Shell Identity correctness baseline
v0.5.4 = released Position Persistence correctness patch
drag → normal tray Exit → restart position round trip = named verified contract
v0.6.0 Battery Indicator and Layout Tightening = NOT STARTED
```
Update only files whose facts or contracts changed.
Do not begin v0.6.0 during reconciliation.
---
## 18. Completion criteria
This Goal is COMPLETE only when all are true.
### Root cause
- exact A-path is reproduced;
- stable post-drag root coordinates are captured;
- the first coordinate divergence is identified;
- one root-cause hypothesis explains the full symptom;
- the selected fix corrects the first divergence.
### Position persistence
Under unchanged legal display topology:
```text
drag to X,Y
→ release
→ normal tray Exit
→ restart
→ final stable root = X,Y
```
### Recovery
- invalid/off-screen positions still recover;
- legal multi-monitor positions remain legal;
- no hard-coded topology assumption is introduced.
### Regression safety
- opacity persistence remains correct;
- Window Size persistence remains correct;
- settings transaction semantics remain correct;
- five expanded rows remain fully visible;
- v0.5.1 geometry authority remains green;
- v0.5.3 Shell Identity remains green;
- tray, single instance, and shutdown remain correct.
### Release
- authoritative RED/GREEN evidence exists;
- fresh Quality passes;
- package smoke passes;
- formal RC passes;
- exact-head CI succeeds;
- v0.5.4 is squash-merged;
- merged main is verified;
- v0.5.4 tag and GitHub Release target the verified commit;
- completed merged branch is deleted;
- active state is reconciled.
---
## 19. Mandatory stop condition
After v0.5.4 release and active-state reconciliation:
> **STOP.**
Do not begin battery implementation.
Do not create a v0.6.0 branch.
Set final `Goal/EXECUTION_STATE.md` next action to exactly:
```text
Wait for Tom to start the approved v0.6.0 5H Battery Indicator and Layout Tightening Goal.
```
---
## Final operating principle
> **Use the stable post-drag root coordinates as truth. Trace them through normal tray Exit and restart. Find the first divergence. Fix one root cause. Preserve recovery, geometry, and Shell identity. Release v0.5.4, reconcile, and stop.**
