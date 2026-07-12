# ACTIVE GOAL — v0.5.3 Windows Shell Identity Correctness
> **Status:** ACTIVE
> **Released baseline:** `v0.5.1`
> **Scope:** one Windows shell-identity correctness release
> **Supported platform:** Windows 11 x64
> **Next feature:** `v0.6.0 5H Battery Indicator and Layout Tightening` is DEFERRED until this Goal is fully released and reconciled
> **Execution:** autonomous-first, evidence-first, systematic-debugging, Design Verification, TDD, verification-before-completion
> **Remote workflow:** repository `AGENTS.md` standing authorization applies to routine GitHub operations inside this Goal
---
## 0. Mission
Restore the companion's intended Windows shell identity.
The Codex Windows Status Pet is a desktop overlay plus notification-area companion. It is not a normal task-switchable application window.
Required visible behavior:
```text
desktop overlay = visible
notification-area / tray icon = visible
Win+Tab / Task View = Codex Status Pet absent
Alt+Tab = Codex Status Pet absent
ordinary taskbar application button = absent
```
This identity must remain stable through all supported overlay lifecycle transitions.
The product outcome is:
> **The overlay remains visible and tray-reachable while its main overlay HWND is consistently excluded from ordinary Windows task-switching and taskbar application identity.**
This Goal fixes only shell identity.
Do not implement the battery indicator, layout tightening, installer, auto-update, or unrelated UI redesign here.
---
## 1. Historical truth and version selection

The released product baseline remains `v0.5.1`.

The prior `v0.5.2` rendered-visibility work was an investigation closed without a product release. Repository documents already use `v0.5.2` as that incident identifier.

Therefore the next actual product patch version is:

```text
v0.5.3
```

Do not rewrite the historical v0.5.2 investigation.

Do not create a v0.5.2 product tag or Release.

At Goal activation, reconcile the active-state documents to show:

```text
released baseline = v0.5.1
active implementation = v0.5.3 Shell Identity Correctness
v0.5.2 = historical closed investigation without product release
v0.6.0 battery feature = deferred until v0.5.3 closes
```

Update only the authoritative active state that must change:

- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`
- paired Chinese roadmap when the English canonical roadmap changes
---
## 2. Production evidence

Tom reports a new regression:

> The overlay previously did not appear as content in Windows Task View / Win+Tab, but it now appears again.

The intended product identity is confirmed:

```text
desktop overlay visible
tray icon visible
Win+Tab absent
Alt+Tab absent
taskbar application button absent
```

Current `Pet` still calls `overrideredirect(True)`, but this alone is not accepted as proof of shell exclusion.

Released v0.5.1 also changed the startup mapping lifecycle to include:

```text
Tk root creation
→ withdraw
→ position for target-monitor DPI
→ create/configure widgets
→ deiconify
```

This lifecycle change is a high-priority investigation direction, not a proven root cause.

Do not change production code until the actual main HWND shell identity has been measured and compared with a known-working historical state or equivalent working window contract.
---
## 3. Protected product core

Preserve unless exact root-cause evidence proves a protected behavior must change.

### Data and privacy

- Quota data continues to use the local official Codex app-server path.
- Activity continues to use approved local Codex session metadata.
- Do not read `auth.json` or access tokens.
- Do not add telemetry, a backend, hosted services, or third-party quota providers.
- Do not expose prompt, response, session content, token, or credential data.

### Runtime

- Windows 11 x64 remains the supported baseline.
- One companion instance only.
- A second launch must not kill unrelated processes.
- Tk work remains on the Tk main thread.
- Background workers must not call Tk directly.
- Refresh remains bounded and single-flight.
- Shutdown remains safe and idempotent.
- No persistent console is required.

### User-visible behavior

Preserve:

- exactly five stable status-row identities;
- truthful activity/quota presentation;
- settings Apply / Save / Close / Restore Defaults semantics;
- canonical 80–200% Window Size scaling;
- Hide/Show;
- Compact/Expand;
- drag/lock;
- topmost;
- legal multi-monitor position recovery;
- tray reachability;
- restart persistence;
- v0.5.1 target-window-DPI geometry and font authority.

The shell-identity correction must not reintroduce the v0.5.0 geometry regression.
---
## 4. Required workflow

Route this Goal as:

```text
using-superpowers
→ systematic-debugging
→ shell identity evidence collection
→ historical/working pattern comparison
→ one root-cause hypothesis
→ compare 2–3 minimum fixes
→ DESIGN VERIFICATION
→ writing-plans
→ test-driven-development
→ minimum root-cause fix
→ verification-before-completion
→ routine authorized GitHub release workflow
→ active-state reconciliation
→ STOP
```

Iron rule:

> **NO SHELL-STYLE FIX BEFORE ROOT-CAUSE INVESTIGATION.**

Do not assume `withdraw`, `deiconify`, `overrideredirect`, `WS_EX_TOOLWINDOW`, ownership, or `WS_EX_APPWINDOW` is the root cause before measuring the real HWND.
---
## 5. Phase 1 — prove exact running provenance

Autonomously inspect the currently running overlay.

Record:

- PID;
- process executable;
- full CommandLine;
- loaded source path where safely inspectable;
- running-source relationship to current repository main;
- current application version;
- process start time;
- repository branch and HEAD for the running source;
- working-tree state;
- HWND used by the visible overlay;
- Tk root mapped/withdrawn state;
- current monitor/work area;
- effective `GetDpiForWindow`;
- outer window rect;
- client rect.

Do not infer running code identity only from the current on-disk `APP_VERSION`.

Use the stale-process lesson from the closed v0.5.2 investigation:

```text
on-disk version != proof of already-loaded process code
```

If the running process is not provenance-correct for current released v0.5.1/main behavior, establish that before shell diagnosis.
---
## 6. Phase 2 — measure the actual Windows shell identity

For the visible main overlay HWND, record before and after relevant lifecycle transitions:

- HWND;
- top-level root HWND relationship;
- parent from `GetParent`;
- owner relationship where available;
- `GWL_STYLE`;
- `GWL_EXSTYLE`;
- `WS_EX_TOOLWINDOW` present/absent;
- `WS_EX_APPWINDOW` present/absent;
- visibility from `IsWindowVisible`;
- iconic/minimized state;
- enabled state;
- cloak state when safely queryable;
- title/class name;
- Tk `overrideredirect` state;
- mapped/withdrawn state.

Do not rely on one source-level setting.

The measured contract is about the real Win32 window Windows Shell classifies.

Capture the same identity snapshot at minimum for:

```text
cold start after stable mapping
settings open
settings Close
settings Apply
settings Save
Restore Defaults
lock
unlock
Hide
Show
Compact
Expand
scale reapply
target-DPI reapply
```

Identify the exact first transition, if any, where shell identity changes.
---
## 7. Phase 3 — compare against a working pattern

Find the last repository revision or exact historical runtime state for which the overlay was known not to appear in ordinary task switching.

Use Git history and repository evidence.

Compare the complete relevant window lifecycle and HWND state, not only one line.

At minimum compare:

```text
root creation order
overrideredirect timing
withdraw timing
initial geometry
update_idletasks timing
deiconify timing
show_window behavior
state("normal")
focus_force
lift
temporary topmost handling
owner/parent state
GWL_STYLE
GWL_EXSTYLE
```

Produce an evidence table:

```text
fact
→ known-working state
→ current failing state
→ exact difference
→ why the difference can or cannot affect shell classification
```

Do not treat chronology alone as causation.
---
## 8. Phase 4 — reproduce and define RED

The RED must be against current released/current-main behavior before the fix.

A source assertion such as:

```text
overrideredirect == True
```

is not sufficient.

The RED must inspect the effective Win32 shell identity of the actual overlay HWND.

Create the smallest reliable contract that current behavior violates for the same reason the window is exposed to ordinary shell switching.

Candidate measurable contract:

```text
overlay HWND exists
→ overlay is visible
→ tray remains available
→ effective shell-exclusion identity is present
→ ordinary application-window identity is absent
→ lifecycle transition
→ the same exclusion identity remains present
```

The exact style/owner assertions must follow Phase 2 evidence.

Do not hard-code `WS_EX_TOOLWINDOW` as the RED unless the evidence establishes it as the correct authority.

### Task View / Win+Tab evidence

Because Windows Task View does not expose a simple documented public enumeration contract equivalent to a unit-test API, use this priority:

```text
1. Win32 shell-identity contract
2. safe UI Automation inspection of Task View / task switcher if available
3. safe app-local host automation that can identify this app without capturing unrelated desktop content
4. one exact maintainer physical fact only if the Human Interaction Admission Gate passes
```

Do not build against undocumented internal Shell COM interfaces merely to avoid one honest physical limitation.

Do not capture or persist unrelated desktop content, application previews, prompts, or private windows.

If one human fact is truly required, record:

```text
Human fact required:
Methods attempted:
Observed evidence:
Why automation is insufficient:
Why the fact blocks v0.5.3:
Exact factual question:
```

Ask only one factual question.
---
## 9. Root-cause hypothesis and considered fixes

Before production code changes, state exactly one primary root-cause hypothesis.

It must explain:

```text
why the current main overlay becomes shell-visible
why the prior known-working state did not
which measured HWND property or lifecycle transition differs
why existing tests did not catch it
why the new RED fails
```

Compare 2–3 minimum approaches supported by evidence.

Candidate approaches may include:

### A. Explicit overlay extended-style identity

Apply the evidence-required extended styles to the actual Tk root HWND and clear a conflicting ordinary application style if present.

### B. Correct owner-window relationship

Use a stable owner relationship only if evidence proves the missing/changed ownership causes shell classification.

### C. Reapply shell identity at the proven lifecycle boundary

If Tk or Windows recreates/resets effective shell identity after a specific mapping/state transition, reapply the existing identity at that exact boundary.

Do not combine A, B, and C speculatively.

Choose the smallest solution that addresses the measured root cause.
---
## 10. Design Verification Gate

Before modifying production behavior, record:

```text
DESIGN VERIFIED

Problem evidence: PASS
Running provenance: PASS
Current HWND shell identity measured: PASS
Known-working/current comparison: PASS
Root-cause hypothesis: PASS
Observable contract: PASS
Lifecycle failure path: PASS
RED definition: PASS
2–3 minimum approaches compared: PASS
Recommended minimum fix: PASS
Scope bounded: PASS
Human verification required: NONE / exact admitted fact
```

The design must answer:

> **Would this RED have blocked the current build before Tom saw the Win+Tab regression?**

If the answer is not demonstrably yes:

```text
DESIGN VERIFICATION = FAILED
→ return to investigation
```

Do not implement.
---
## 11. Implementation constraints

After Design Verification:

```text
RED
→ minimum root-cause fix
→ GREEN
→ focused cleanup only if directly required
```

Forbidden:

- battery indicator work;
- paw replacement;
- layout tightening;
- installer/productization;
- auto-update;
- new UI framework;
- general Window Manager subsystem;
- broad main-window refactor;
- arbitrary style flags without measured evidence;
- undocumented Shell COM dependencies;
- killing generic Python processes;
- changing five-row text to hide the issue;
- unrelated branch cleanup.

Prefer the existing Windows/runtime or Tk owner of the proven behavior.

A new production abstraction requires evidence that the existing owner cannot safely own the fix.
---
## 12. Required regression surface

The shell-identity contract must remain stable across:

```text
cold start
settings open
settings Close without change
opacity-only Apply
scale-change Apply
Save
draft change → Close rollback
Restore Defaults
lock
unlock
Hide
Show
Compact
Expand
repeated settings open/close
80–200% scale reapplication
DPI 96 supported path
DPI 120 automated path
relevant combined sequence
```

After each relevant transition, verify:

- one main overlay HWND;
- overlay visibility state is correct;
- shell-exclusion identity remains correct;
- no ordinary app-window identity appears;
- five stable rows remain intact when expanded;
- v0.5.1 geometry/content-fit contract remains green;
- Compact/Expand returns to authoritative expanded geometry;
- tray remains reachable;
- single-instance behavior remains unchanged.
---
## 13. Required verification

### Focused RED/GREEN

Preserve evidence showing:

```text
released/current pre-fix behavior = RED
v0.5.3 candidate = GREEN
```

The RED and GREEN must use the same authoritative shell-identity observable.

### Windows host identity verification

Verify on Windows 11 x64:

```text
desktop overlay visible
tray icon present
ordinary taskbar app button absent
Alt+Tab app entry absent
Win+Tab / Task View app content absent
```

Automate these facts when safely practical.

For any unavoidable physical-only Task View fact, follow the Human Interaction Admission Gate exactly.

### Existing correctness

Run fresh:

- v0.5.1 long-lived runtime geometry transition checks;
- all supported relevant scale checks;
- five-row content-fit checks;
- settings lifecycle tests;
- Hide/Show;
- Compact/Expand;
- tray/menu;
- single instance;
- shutdown.

### Repository gates

Run fresh:

```text
focused shell-identity tests
relevant Tk/Win32 integration
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

Do not claim completion from old output.
---
## 14. GitHub and release workflow

Repository `AGENTS.md` standing authorization applies to routine verified GitHub operations within this active Goal.

After the required verification passes:

```text
verify repository / remote / account
→ push verified v0.5.3 branch
→ create PR
→ monitor exact-head Windows CI
→ investigate evidence-backed CI failures
→ focused fix cycle if required
→ rerun required verification
→ verify exact PR head
→ squash merge
→ synchronize main
→ verify merged main
→ rerun merged-main formal RC
→ create/push v0.5.3 tag
→ create GitHub Release
→ verify tag/Release target
→ delete completed merged v0.5.3 branch
→ active-state reconciliation
```

Do not request repeated permission for normal branch push, PR, CI monitoring, verified correction push, squash merge, main verification, tag/Release, or merged branch cleanup inside this Goal.

High-risk exclusions in repository `AGENTS.md` remain separately permissioned.
---
## 15. Release-state reconciliation

After v0.5.3 is actually merged, verified, tagged, and released, update only authoritative files whose facts changed:

- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`
- paired Chinese documents where required
- version sources
- changelog
- compatibility/testing documentation directly affected by shell identity

Final truth:

```text
v0.5.1 = previous released baseline
v0.5.2 = closed historical investigation without product release
v0.5.3 = released Shell Identity Correctness patch
Win+Tab / Alt+Tab / ordinary taskbar exclusion = named verification contract
v0.6.0 battery feature = not started
```

Do not document battery behavior as implemented.
---
## 16. Completion criteria

This Goal is COMPLETE only when all are true.

### Root cause

- current real HWND identity was measured;
- known-working/current evidence was compared;
- one root cause is documented;
- the selected fix addresses that root cause rather than a guessed flag.

### Shell identity

- desktop overlay remains visible;
- tray remains visible/reachable;
- ordinary taskbar application button is absent;
- Alt+Tab application entry is absent;
- Win+Tab / Task View application content is absent.

### Lifecycle

- supported settings, lock, visibility, compact, scale, and DPI transitions preserve shell identity.

### Regression safety

- v0.5.1 geometry authority remains green;
- five expanded rows remain fully visible;
- no protected runtime/data/privacy behavior changes;
- no new unnecessary dependency or subsystem is added.

### Release

- focused RED/GREEN evidence exists;
- fresh Quality, package smoke, and formal RC pass;
- exact-head CI succeeds;
- v0.5.3 is squash-merged;
- merged main is verified;
- v0.5.3 tag and GitHub Release target the verified commit;
- completed merged branch is deleted;
- active state is reconciled.
---
## 17. Mandatory stop condition

After v0.5.3 release and active-state reconciliation:

> **STOP.**

Do not begin implementing the battery feature.

Do not create the v0.6.0 battery branch.

Do not change paw rendering.

Do not change compact geometry for battery.

Set the final `EXECUTION_STATE` next action to:

```text
Wait for Tom to start the approved v0.6.0 5H Battery Indicator and Layout Tightening Goal.
```
---
## Final operating principle

> **Prove the real HWND identity, find the exact shell-classification difference, fix one root cause, keep the overlay out of ordinary Windows switching surfaces, release v0.5.3, reconcile, and stop.**
