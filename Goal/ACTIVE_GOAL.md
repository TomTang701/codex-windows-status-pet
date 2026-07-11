# ACTIVE GOAL — Autonomous Verification and Lean-Core Renewal
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Authority:** Replace the current `Goal/ACTIVE_GOAL.md` with this file.
> **Mission:** Reduce unnecessary human verification and reduce project complexity while preserving the proven product core.
> **Execution:** autonomous-first, evidence-first, design-verified, sequential releases, one active version at a time.
> **Supported baseline:** Windows 11 x64.
> **Permission boundary:** Repository-root `AGENTS.md` grants standing authorization for routine GitHub workflow operations only for `TomTang701/codex-windows-status-pet` within this Goal. Its listed high-risk operations remain separately permissioned; destructive unrelated Git, deployment, credential access, remote-owner changes, and repository-setting changes are not implied.
---
## 0. Highest-priority direction
Read this file completely before repository changes.
Tom has two primary requirements:
1. **Automate verification whenever a fact is machine-verifiable.**
2. **Make the project materially leaner without breaking proven bottom-level behavior.**
The new development path is:
```text
reconcile reality
→ measure complexity
→ protect core contracts
→ close known correctness gaps
→ automate routine verification
→ delete or merge unjustified complexity
→ unify fragmented state only when evidence requires it
→ decide the next product direction
```
Do not perform a big-bang rewrite. Do not continue the previous rapid feature-release cadence. Do not solve every problem in one version.
Default rule:
> **Preserve behavior. Automate facts. Delete unnecessary complexity. Make the smallest verified change.**
---
## 1. Instruction and Superpowers routing
Priority:
1. Tom's current explicit request.
2. Repository/directory `AGENTS.md`.
3. Tom's global engineering instructions.
4. This Goal.
5. Applicable allowed Superpowers workflow.
6. General engineering judgment.
Before materially new technical work:
```text
using-superpowers
→ classify work
→ invoke the relevant allowed skill
→ continue under this Goal
```
Allowed default skills:
- using-superpowers
- brainstorming
- writing-plans
- systematic-debugging
- test-driven-development
- verification-before-completion
Routing:
```text
bug / unexpected behavior
→ systematic-debugging
→ TDD when reproducible
→ verification-before-completion
meaningful behavior / architecture change
→ brainstorming
→ Design Verification Gate in Section 4
→ writing-plans
→ TDD when applicable
→ verification-before-completion
documentation-only factual correction
→ inspect authoritative state
→ smallest correction
→ relevant document checks
→ verification-before-completion
release administration
→ inspect exact Git/GitHub/source state
→ do not ask Tom to verify machine-readable facts
→ verification-before-completion before readiness claims
```
Skills must improve correctness, not create repeated approval loops, magic phrases, duplicated plans, or unnecessary "continue?" questions.
---
## 2. Protected product core
Slimming may change internals. It must preserve these observable contracts unless Tom explicitly changes the product.
### Data and privacy
- Quota data comes from the local official Codex app-server path.
- Activity detection uses approved local Codex session metadata.
- Do not read `auth.json` or Codex access tokens.
- Do not add third-party quota endpoints, telemetry, a backend, or a hosted service.
- Do not expose prompt, response, session content, tokens, or credentials.
- Do not modify Codex core or built-in pet files.
### Runtime
- Windows 11 x64 remains the supported baseline.
- Only one companion instance may run.
- A second launch must not kill an unrelated process.
- Workers must not call Tk APIs directly; Tk/UI work stays on the Tk main thread.
- Refresh behavior remains bounded and single-flight.
- Shutdown remains safe and idempotent.
- Normal launch does not require a persistent console.
### User-visible behavior
Keep five stable status-row identities:
```text
activity
progress
primary_5h
weekly
reset_credit
```
Preserve:
- truthful quota display;
- validated and recoverable settings;
- distinct Apply / Save / Close / Restore Defaults behavior;
- canonical proportional window scaling;
- Hide/Show and Compact/Expand;
- drag/lock and topmost;
- position recovery and tray reachability;
- restart persistence;
- current valid configuration compatibility;
- documented rollback compatibility until evidence supports removal.
"Preserve the core" does **not** mean preserving every historical API, wrapper, controller, helper, test, plan, or document.
---
## 3. Reconcile reality before development
Current active documents contain release-state drift. At Goal start, Codex must autonomously determine:
```text
current branch and HEAD
remote main HEAD
application version
latest merged PR
latest release tag
CI state
ACTIVE_GOAL state
ACTIVE_VERSION_BRIEF state
EXECUTION_STATE state
ROADMAP claims
README and installation claims
```
Use Git, GitHub connector/API, source files, and repository checks. Do not ask Tom for these facts.
### Active-document ownership
- `Goal/ACTIVE_GOAL.md`: multi-release direction, invariants, phase order, cross-phase rules.
- `Goal/ACTIVE_VERSION_BRIEF.md`: one current version's outcome, scope, contracts, exit criteria.
- `Goal/EXECUTION_STATE.md`: current branch/task/evidence/blocker/next action.
- `docs/product/ROADMAP.md`: product sequence and released/pending direction.
- architecture docs: stable technical contracts.
- quality records: dated evidence.
- archive: historical, non-normative work.
Do not store volatile facts such as current SHA, "no PR yet", or one-time release instructions in this Goal.
Do not duplicate the same branch, SHA, test output, release state, and next action across multiple active documents.
---
## 4. Autonomous verification and Design Verification
### 4.1 Verification priority
Use the lowest-cost truthful method that determines the fact:
```text
1. source / repository inspection
2. pure unit or contract test
3. integration test
4. Tk widget / geometry introspection
5. process / CommandLine / filesystem inspection
6. Win32/runtime introspection
7. safe app-local interaction
8. CI / GitHub machine-readable state
9. exact-build existing evidence
10. maintainer factual confirmation
```
This is a priority order, not a requirement to run every layer.
Do not create complicated automation merely to imitate unavailable hardware. A truthful environment limitation may be simpler and more correct.
### 4.2 Human Interaction Admission Gate
Codex may ask Tom to verify a technical fact only when all applicable conditions pass:
```text
[ ] one exact fact or physical action is required
[ ] it materially blocks the active version
[ ] source inspection cannot determine it
[ ] tests cannot determine it
[ ] simple safe automation cannot determine it
[ ] Tk/Win32/process/filesystem inspection cannot determine it
[ ] app-local automation cannot determine it
[ ] exact-build evidence cannot determine it
[ ] the question is not asking Tom to repeat a machine-readable fact
```
Before asking, record in `Goal/EXECUTION_STATE.md`:
```text
Human fact required:
Methods attempted:
Observed evidence:
Why automation is insufficient:
Why the fact blocks the version:
Exact factual question:
```
Ask one concise factual question. After Tom answers sufficiently, record the evidence and resume automatically. Do not ask whether to continue.
### 4.3 Normally prohibited human verification
Do not ask Tom to manually confirm:
- Git branch, SHA, status, or remote state;
- source/application version;
- PR, CI, or tag state;
- process count or CommandLine;
- module path or window HWND;
- Tk widget, menu, or settings-control inventory;
- exact Tk text when widgets can be introspected;
- requested or allocated Tk geometry;
- configuration or changelog contents;
- version-source consistency;
- document parity;
- Quality/RC output;
- whether an automated test passed.
Human input can remain necessary for physical hardware changes, unavailable display topology, genuinely subjective visual preference, credentials/permissions, or explicit authorization required by `AGENTS.md`.
Do not confuse **authorization** with **verification**.
### 4.4 Design Verification Gate
Meaningful behavior or architecture work uses:
```text
evidence
→ design
→ DESIGN VERIFICATION
→ implementation plan
→ TDD / implementation
→ completion verification
```
A design is verified only when applicable items below pass.
**Problem evidence**
- For a bug: reproduce or objectively evidence the symptom, inspect relevant logs/errors and recent changes, trace the affected flow, and state one root-cause hypothesis.
- For a new capability: define product intent, success criteria, and confirm the active phase allows it.
**Observable contract**
Every outcome must be machine-checkable when practical.
Bad:
```text
make scaling better
clean architecture
improve errors
```
Good:
```text
At each supported scale, every approved status row remains fully inside the
status container and an approved single-line row does not wrap unexpectedly.
```
Good:
```text
Injecting a quota transport failure through the production queue path renders
the approved state through the row presentation API without a Tk config error.
```
**Failure-path map**
Identify:
```text
input/event
→ owning state
→ controller/domain boundary
→ presentation/output boundary
→ visible/persisted result
```
A design fails if an error path bypasses the intended authoritative boundary without evidence-based reason.
**Regression surface**
List only relevant protected behavior. Layout work should consider supported scale points, five rows, Compact/Expand, Hide/Show, settings transactions, and restart persistence. Runtime-state work should consider loading, available, stale with last-good data, unavailable, transport error, malformed response, tray error, and shutdown with in-flight work where relevant.
**RED definition**
For a reproducible bug, define the smallest check the current code is expected to fail for a known reason.
Ask:
> Would this check have caught the real bug before Tom saw it?
If no, the design is not ready.
**Scope**
Reject a design that uses a small problem to justify framework replacement, product redesign, a new backend/provider, telemetry, unnecessary dependencies, many new abstractions, or unrelated cleanup.
Record:
```text
DESIGN VERIFIED
Problem evidence: PASS
Root-cause hypothesis: PASS / N/A
Observable contract: PASS
Failure paths: PASS
Regression surface: PASS
RED definition: PASS / N/A
Scope bounded: PASS
Human verification required: NONE / exact fact
```
If an applicable item fails, return to investigation/design. Do not implement production behavior first.
---
## 5. Lean-core complexity policy
The target is the smallest architecture that truthfully supports current behavior, not minimum line count.
### 5.1 Baseline before slimming
Record:
```text
production Python files
production Python LOC
test files and test LOC
active normative document files and LOC
API modules
controller modules
runtime dependencies
routine Quality duration
package smoke result
strict RC result
```
Identify:
```text
runtime consumer count by API/controller
compatibility-only modules
duplicate state ownership
duplicate presentation paths
duplicate validation logic
pass-through or one-method wrappers
historical controls still represented in production code
active docs containing release-history detail
```
Use existing repository tools, Python, and `rg`. Do not add a production dependency for this audit.
### 5.2 Classify candidates
Every complexity candidate is `KEEP`, `MERGE`, `DELETE`, or `DEFER`.
**KEEP**
- owns a real responsibility;
- has active runtime/release value;
- isolates a meaningful Tk/Windows/IO/domain boundary.
**MERGE**
- responsibility is real;
- the current boundary adds more indirection than isolation;
- merge does not create a new oversized component.
**DELETE**
- no runtime consumer;
- no required compatibility or tooling consumer;
- no protected public contract;
- behavior remains protected after removal.
**DEFER**
- evidence is incomplete;
- removal may affect compatibility/rollback;
- the current phase does not need the decision.
Do not keep a module solely because its own unit test imports it.
### 5.3 New abstraction budget
A new production module/controller/API/manager/adapter is not the default answer.
Before adding one, state:
```text
Responsibility:
Why the existing owner cannot own it:
Boundary isolated:
Consumers:
Testing benefit:
Complexity removed or prevented:
```
A one-method wrapper is not justified by "separation of concerns" alone. Prefer deleting, merging, or simplifying before adding another layer.
### 5.4 Compatibility code
Compatibility code may remain when it protects current config loading, documented rollback, an active public/import boundary, or launcher/package behavior.
For compatibility-only code:
```text
identify protected scenario
→ verify whether it still matters
→ protect behavior at contract level
→ remove the helper/module when the scenario no longer needs it
```
Do not preserve a module solely to preserve its unit test.
### 5.5 Active-document budget
Soft limits:
```text
ACTIVE_GOAL           < 700 lines
ACTIVE_VERSION_BRIEF  < 180 lines
EXECUTION_STATE       < 100 lines
```
Exceeding a limit requires a concrete execution reason.
Completed plans/specs may remain archived history, but they must not become required reading for unrelated future work.
---
## 6. Known renewal findings
Treat these as backlog evidence, not permission to guess a fix.
### A. Status-row content-fit regression
Tom observed that after proportional scaling, the final refresh/reset-credit row can be incompletely displayed.
Required path:
```text
reproduce
→ measure actual/requested Tk geometry
→ trace layout allocation
→ one root-cause hypothesis
→ regression contract that catches the real symptom
→ RED
→ minimum root-cause fix
→ GREEN
```
Do not start by adding arbitrary height.
The contract must determine whether approved text is fully visible, requested geometry fits allocated geometry, the final row remains inside its container, and a single-line row wraps unexpectedly.
### B. Legacy Label-style error rendering
`StatusRows` is a Tk frame with row-specific rendering, but current error paths still contain old-style calls shaped like:
```python
self.text.config(text=..., fg=...)
```
Known areas include tray-error and quota transport-error handling.
Required direction:
```text
runtime/domain state
→ presentation boundary
→ approved row mapping
→ StatusRows.configure_rows
```
Do not create a second error-rendering subsystem.
### C. Active-state and README drift
Active planning/release documents contain completed-release facts. README and installation claims must be checked against current settings controls and startup behavior.
Update only files whose factual state or contract changed.
### D. Complexity accumulation
Audit compatibility-only APIs or APIs documented as having no normal UI consumer. Audit duplicate presentation/error paths, duplicate state ownership, old resize/control logic, repeated release prose, and implementation-detail tests that protect dead internals.
No component is pre-approved for deletion. Consumer and compatibility evidence decides.
---
## 7. Multi-release renewal path
One version is active at a time. Later phases are roadmap direction only. Do not start later-phase work early because code is nearby.
### Phase 0 — Repository truth and baseline
**Release:** none unless behavior changes.
**Outcome:** establish a truthful starting point.
Required work:
1. Reconcile Git/GitHub/version/tag/release state.
2. Replace the completed old Goal with this Goal.
3. Archive or mark the old Goal historical/non-normative.
4. Reconcile Active Version Brief, Execution State, Roadmap, README, and installation claims.
5. Record the Section 5 baseline.
6. Rank findings as correctness, missing automated contract, duplicate state/presentation, removable complexity, or stale process/docs.
7. Make Phase 1 the only active implementation scope.
Exit:
- active state is truthful;
- no active doc treats released work as pending;
- no stale Goal forbids the next release;
- baseline and ranked backlog exist;
- no unrelated product change occurred.
### Phase 1 — v0.4.1 Correctness Stabilization
**Outcome:** close known correctness gaps without features.
Scope:
1. Reproduce and resolve status-row content clipping.
2. Add an automated content-fit contract that catches Tom's real symptom.
3. Reproduce tray-error and quota-error behavior through production integration paths.
4. Remove invalid legacy Label-style rendering against `StatusRows`.
5. Route affected visible status/error output through the authoritative presentation path.
6. Correct directly affected v0.4.0 documentation facts.
Non-goals:
- installer, themes, animation, new menu actions;
- new provider;
- framework rewrite;
- broad main-window decomposition;
- broad API deletion;
- Windows 10 support claim.
Verification:
- focused RED/GREEN for reproducible bugs;
- supported-scale content-fit checks;
- error-path integration tests;
- relevant settings/Compact/Hide/Show regression;
- routine Quality;
- package smoke;
- strict RC before release-ready claim;
- human verification only if Section 4 admits one exact blocker.
Exit:
- the real clipping symptom is test-protected and resolved;
- tray/quota error paths no longer misuse old Label config behavior;
- affected visible status/errors use one presentation route;
- no feature is included.
### Phase 2 — v0.4.2 Autonomous Verification Conversion
**Outcome:** remove routine human verification from machine-observable release checks.
Audit each Quality, RC, compatibility, and host-validation step. Classify:
```text
AUTOMATED
AUTOMATABLE
PHYSICAL-ONLY
OBSOLETE
DUPLICATE
```
For `AUTOMATABLE`, prefer existing mechanisms: contract tests, Tk integration/introspection, Win32/process inspection, temporary config paths, app-local action invocation, package/launcher smoke, Git/GitHub inspection, and machine-readable results.
Rule:
```text
one fact
→ one authoritative check
→ one clear failure message
```
Do not create multiple scripts that verify the same fact.
Routine release validation on Tom's current supported Windows host should require **zero human visual confirmation** for facts source, Tk, Win32, process, filesystem, or GitHub inspection can determine.
Record physical-only limitations once instead of repeatedly asking, including unavailable mixed-DPI hardware, unavailable alternate physical taskbar edge, or unavailable separate clean Windows machine.
A limitation is not a failed test. A simulation is not physical evidence.
Complexity constraint:
> automation added in this phase must replace or remove equal-or-greater manual procedure, duplicate gate logic, or repeated release prose.
Exit:
- every release check is classified;
- machine-observable checks do not depend on Tom;
- duplicate verification is consolidated;
- physical-only limitations are explicit;
- release output separates pass, blocker, and limitation.
### Phase 3 — v0.5.0 Lean-Core Simplification
**Outcome:** materially simplify the product without changing protected behavior.
Use the Phase 0 baseline and Phase 2 verification contracts.
Audit in order:
1. dead production code;
2. unused compatibility APIs with no protected scenario;
3. duplicate presentation/error paths;
4. duplicate state ownership;
5. pass-through wrappers without a real boundary;
6. historical resize/control logic unreachable from normal behavior;
7. duplicated active docs/release procedure;
8. tests protecting only deleted implementation details.
For each simplification:
```text
identify protected behavior
→ locate consumers
→ ensure behavior-level regression protection
→ make one focused removal/merge
→ run focused tests
→ run relevant regression
→ inspect diff
```
Do not rewrite a working subsystem wholesale. Prefer a negative production-code diff when equal behavior can be preserved more simply.
Keep meaningful boundaries around Tk/Windows calls, local Codex transport, config persistence, parsing/normalization, presentation state, and async refresh coordination. Other boundaries must justify themselves.
Exit report:
```text
production Python files: before → after
production Python LOC: before → after
API/controller modules: before → after
active normative doc LOC: before → after
runtime dependencies: before → after
routine Quality duration: before → after
```
Pass only when protected behavior remains verified, the measured project is objectively no more complex, metric increases are justified, no unapproved dependency is added, and repository structure is easier to explain.
### Phase 4 — v0.5.1 Runtime/Presentation State Unification
**Outcome:** finish one coherent state-to-presentation path only if fragmentation still exists.
This phase is conditional. If Phase 1 and Phase 3 already leave one authoritative presentation route with no meaningful duplicate state ownership, mark:
```text
PHASE 4 NOT NEEDED
```
Do not invent work.
When needed, evaluate truthful states: loading, available/ok, stale with last-good data, unavailable, signed-out only if distinguishable, malformed/protocol error, and tray failure/recovery when user-visible status is justified.
Required direction:
```text
transport/activity result
→ normalized domain state
→ coordination state
→ presentation result
→ five-row mapping/color
→ Tk adapter
```
`Pet` composes and orchestrates Tk behavior. It must not become a second formatter.
Exit:
- each visible runtime state has one owner;
- visible status strings/colors have one presentation boundary;
- no emergency direct-string path duplicates presentation logic;
- stale/unavailable behavior stays truthful;
- no unnecessary state abstraction is added.
### Phase 5 — v0.6.0 Productization Decision
Do not automatically implement productization.
First answer:
```text
Is the lean core stable?
Are supported-host routine checks automated?
Are active docs truthful and small?
Is installation now the largest real usability problem?
Would productization add more value than another stabilization release?
```
Only after an approved design may candidate work include install/uninstall paths, explicit startup behavior, a release artifact, clean-machine strategy, user-oriented README, license completion, and evidence-based troubleshooting.
If the answer is no, remain on v0.5.x.
---
## 8. Scope, testing, and release discipline
At all times:
```text
one active version
one Active Version Brief
one bounded implementation outcome
one current Execution State
```
A release is too large when its outcome cannot be accurately explained in one paragraph. Split bug-fix + installer, state cleanup + framework migration, simplification + unrelated feature, or automation + duplicate new gate infrastructure.
Until Phase 3 completes, defer unrelated features unless they address correctness, security/privacy, data truthfulness, a release blocker, or regression in documented behavior.
### Testing layers
Use pure tests for parsing, formatting, scale derivation, state transitions, validation, geometry, and migration.
Use Tk integration for widget identity, actual/requested geometry, content fit, row rendering, settings transactions, Compact/Expand, Hide/Show, menu action paths, and error presentation.
Use host/runtime checks for process count, CommandLine, persistent-console state, HWND, monitor/work-area facts, DPI, launcher/relaunch, single instance, and current-build provenance.
Use physical-only evidence only for facts unavailable to safe machine inspection.
Do not call source assertions physical tests, simulations physical evidence, or "widget exists" proof that content fully fits.
When slimming, tests tied only to a deleted internal helper may be removed when product behavior remains protected at a higher-value contract boundary. Do not preserve dead architecture solely to keep implementation-detail tests passing.
### Git/GitHub permissions
Follow repository-root `AGENTS.md` and Tom's global Git/GitHub safety policy. Tom's project-level standing authorization permits the routine verified branch → PR → CI → squash merge → main verification → tag/Release → branch cleanup workflow for this repository throughout this Goal.
Do not request repeated authorization for those routine operations. Separately request permission only for the high-risk exclusions listed in `AGENTS.md`; do not combine that request with unnecessary manual technical verification.
---
## 9. Release-state reconciliation
Every completed release ends with:
```text
finalized branch/merge state
→ main verification
→ tag/release inspection when applicable
→ post-release smoke when applicable
→ ACTIVE STATE RECONCILIATION
```
Inspect:
- `Goal/ACTIVE_GOAL.md`
- `Goal/ACTIVE_VERSION_BRIEF.md`
- `Goal/EXECUTION_STATE.md`
- `docs/product/ROADMAP.md`
- `README.md`
- changelog/version sources
- directly affected architecture/operations docs
Update only files whose facts or contracts changed.
A release is not closed while an active document still claims a merged PR does not exist, a released version is a candidate, a completed task is the next action, or a stale Goal forbids the real next phase.
Prefer automated checks for stable facts such as version-source consistency. Avoid volatile GitHub facts in long-lived normative prose.
### Small active-document formats
`Goal/EXECUTION_STATE.md` should normally stay below 100 lines and contain only:
```text
Active phase
Active version
Branch / HEAD
Active skill
Current design/spec
Current plan
Current task
Latest RED
Latest GREEN
Latest verification
Human fact required
Blocker
Next exact action
Last updated
```
`Goal/ACTIVE_VERSION_BRIEF.md` should normally stay below 180 lines and contain:
```text
Outcome
Why now
In scope
Out of scope
Protected behavior
Observable contracts
Failure paths
Regression surface
Design verification result
Verification evidence classes
Exit criteria
```
The Goal defines direction. The Version Brief defines the active release. Execution State records current work. Do not mix them.
---
## 10. Completion criteria
This renewal is complete only with measured evidence.
### Autonomous verification
- machine-observable checks do not depend on Tom's manual confirmation;
- remaining physical-only checks are explicit;
- repeated human confirmation is not used instead of inspection;
- release output separates automated pass, real blocker, and limitation.
### Correctness
- the observed status-row clipping is protected by a check that would have caught it;
- affected error paths no longer use invalid legacy Label-style configuration against `StatusRows`;
- affected visible status/error output uses the intended presentation path.
### Lean core
- baseline and final comparison exist;
- dead or unjustified complexity found by the audit is removed or evidence-deferred;
- protected behavior remains verified;
- active planning/governance is less duplicated;
- no broad framework rewrite occurred;
- no unnecessary dependency was added.
### Development path
- development is evidence-driven and phase-bounded;
- Design Verification happens before meaningful implementation;
- only one version is active;
- release state is reconciled before the next phase;
- productization is a decision after simplification, not an automatic target.
### Final report
Report actual measurements:
```text
Versions completed:
Correctness issues closed:
Human verification steps removed:
Physical-only checks remaining:
Production Python files before → after:
Production Python LOC before → after:
API/controller modules before → after:
Active normative doc LOC before → after:
Runtime dependencies before → after:
Quality duration before → after:
Components deleted or merged:
Protected behavior evidence:
Remaining risks:
Recommended next Goal:
```
Do not claim "simpler", "leaner", "automated", "renewed", or "焕然一新" without measured evidence.
---
## 11. Final operating principle
> **Automate facts. Preserve behavior. Delete unnecessary complexity. Make the smallest verified change.**
The project should finish this Goal easier to verify, easier to understand, easier to modify, and less dependent on Tom for routine technical confirmation.
That is the definition of success.
