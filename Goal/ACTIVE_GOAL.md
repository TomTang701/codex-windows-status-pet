# ACTIVE GOAL — 高自动化发布闭环、Superpowers 执行纪律与统一窗口缩放迭代

> **Repository:** `TomTang701/codex-windows-status-pet`
> **Authority:** 本文件替换 `Goal/ACTIVE_GOAL.md`，并作为唯一规范性开发Goal
> **Verified remote main SHA:** `d4a69e9ce4a6adc7d519ff1a37b00617d548e8dd`
> **Verified remote released version:** `0.3.1`
> **Verified latest released tag:** `v0.3.1`
> **Current local candidate target:** `v0.3.2`
> **Maintainer-reported candidate state:** strict Release Candidate passed before formal version bump/release
> **Authorized release sequence:** finish `v0.3.2` → then implement and release `v0.4.0`
> **Execution model:** autonomous-first, Superpowers-routed, strictly sequential, one active version at a time
> **Enabled Superpowers skills:** Using Superpowers, Brainstorming, Writing Plans, Systematic Debugging, Test-Driven Development, Verification Before Completion
> **Supported platform:** Windows 11 x64
> **Final stop:** after `v0.4.0` merge, main verification, tag, and post-release smoke
> **Forbidden:** no `v0.4.1+` implementation under this Goal

---

# 0. Highest-priority execution instruction

Read this file completely.

Before any repository action, source edit, plan, fix, verification claim, commit, PR, merge, or release action:

```text
invoke Using Superpowers
→ determine which enabled skill applies
→ follow the skill routing policy in Section 2A
→ continue under this Goal and the Engineering Standard
```

Do not invoke a skill merely to create ceremony. Do not skip a relevant enabled skill merely because the task appears small.

This Goal is a direct maintainer instruction. Where a default Superpowers interaction gate conflicts with the explicit autonomous-first policy, Human Interaction Admission Gate, locked Product Decision, or exact release sequence in this Goal, this Goal controls the interaction behavior.

Do not restart v0.3.2 development from remote `main`.

The maintainer reports that the local v0.3.2 candidate has already passed the complete strict Release Candidate suite, while the formal application version is still `0.3.1`.

Therefore the first objective is:

```text
preserve local candidate
→ reconcile exact local state
→ push a verified checkpoint
→ autonomously close remaining release administration
→ formally release v0.3.2
```

Only after v0.3.2 is fully merged, verified, tagged, and closed may v0.4.0 begin.

---

# 1. Verified remote repository facts

At Goal creation time:

```text
remote main SHA:
d4a69e9ce4a6adc7d519ff1a37b00617d548e8dd

remote application version:
0.3.1

v0.3.1:
identical to remote main

latest merged release:
PR #10 — [v0.3.1] Extract main-window controllers

remote v0.3.2 PR:
not observed

remote v0.3.2 branch:
not observed in the queried remote branch state
```

Remote repository metadata is stale in two places:

```text
Goal/ACTIVE_GOAL.md still describes the old 0.2.0 / 0.2.1 baseline
Goal/ACTIVE_VERSION_BRIEF.md still describes v0.3.1
```

Correct those files on the active v0.3.2 release branch.

Do not push these corrections directly to `main`.

---

# 2. Autonomous-first operating policy

The default mode is autonomous execution.

Codex must perform safe local verification itself whenever the current environment and available local tools can truthfully determine the result.

## 2.1 Verification priority

Use this order:

```text
1. Repository and source inspection
2. Pure unit or contract test
3. Integration test
4. Process / CommandLine / filesystem inspection
5. Win32 / Tk / runtime introspection on the real Windows host
6. Safe interaction with the status-pet application itself
7. Existing evidence from the exact current build and commit
8. Maintainer factual confirmation only as a last resort
```

Do not delegate a check to the maintainer merely because manual confirmation is easier.

## 2.2 No artificial approval phrases

Never require exact wording such as:

```text
请回复：当前五项菜单测试通过
```

Do not invent a human approval token, magic phrase, or fixed sentence.

If human input is genuinely required, any clear natural-language answer to the factual question is sufficient.

Examples of valid replies:

```text
是
通过
只有五项
菜单正常
我已经切换成单屏
```

Interpret the answer by meaning, not exact string matching.

## 2.3 Human Interaction Admission Gate

Codex may pause for maintainer input only when all applicable conditions below are satisfied:

```text
[ ] one exact physical fact or action is required
[ ] source/tests/runtime inspection cannot truthfully determine it
[ ] safe app-local automation cannot determine it
[ ] the requested action requires physical hardware, OS display-mode change, or another user-only action
[ ] the missing fact blocks the current release
[ ] EXECUTION_STATE records what was attempted and why it was insufficient
```

Before asking, record:

```text
Fact required:
Methods attempted:
Why insufficient:
Why human action is necessary:
Exact factual question:
```

Then ask one concise factual question.

Do not repeatedly ask the same question unless the answer is ambiguous.

After sufficient confirmation:

```text
record evidence
resume automatically
do not wait for another “continue” message
```

## 2.4 No human-wait state for ordinary checks

The following normally do not justify waiting for the maintainer:

```text
menu item inventory
source version
Git branch state
PR status
CI status
tag existence
process count
process CommandLine
module path
window HWND existence
Tk widget inventory
settings control inventory
file contents
changelog contents
version-source consistency
strict RC execution
```

These should be verified autonomously.

## 2.5 Browser automation remains prohibited

Do not automate Chrome or another browser to:

```text
confirm a GitHub URL
configure repository rules
inspect private web state
approve a PR
```

Use Git/GitHub API, existing authenticated CLI, repository connectors, or documented compensating controls.

Never read or print credential values.

---


# 2A. Superpowers execution discipline

The following six enabled skills are part of the normative execution model for this Goal:

```text
Using Superpowers
Brainstorming
Writing Plans
Systematic Debugging
Test-Driven Development
Verification Before Completion
```

No other Superpowers skill is required by this Goal.

The skills strengthen engineering discipline. They must not create an artificial approval loop, duplicate an already locked product decision, or weaken the autonomous-first execution policy.

## 2A.1 Authority and interaction adaptation

Precedence for this Goal is:

```text
1. security/privacy requirements in ENGINEERING_STANDARD.md
2. runtime invariants in ENGINEERING_STANDARD.md
3. direct maintainer instructions in this ACTIVE_GOAL
4. applicable enabled Superpowers skill workflow
5. ordinary autonomous implementation judgment
```

This Goal explicitly supplies:

```text
approved release sequence
approved Product Decision for v0.3.2
approved Product Decision = GO for v0.4.0
locked v0.4.0 product outcome
locked user-visible control inventory
locked migration direction
locked resource/privacy expectations
locked version and branch sequence
```

Therefore a skill must not reopen these decisions as routine questions.

Examples of prohibited artificial questions:

```text
Should v0.4.0 use a slider or width/height inputs?
Should v0.4.0 keep an independent font-size control?
Should work begin on v0.4.0 before v0.3.2 is released?
Do you approve Product Decision GO?
Should I continue?
Which exact approval phrase should you reply with?
```

The Human Interaction Admission Gate in Section 2.3 remains authoritative.

## 2A.2 Using Superpowers — mandatory skill router

Use `Using Superpowers` before each materially new task category and when the nature of the task changes.

Route work as follows:

```text
new feature / behavior design
→ Brainstorming
→ Writing Plans
→ Test-Driven Development
→ Verification Before Completion

bug / failing test / unexpected runtime behavior / performance anomaly
→ Systematic Debugging
→ Test-Driven Development for the fix
→ Verification Before Completion

release administration / version bump / Changelog / branch / PR / CI / merge / tag
→ project Goal and Engineering Standard
→ Systematic Debugging only if failure or unexpected behavior occurs
→ Verification Before Completion before any success/readiness claim

documentation-only synchronization with no behavior change
→ project documentation rules
→ Verification Before Completion
```

Do not run Brainstorming merely because a release-administration step has multiple commands.

Do not run Writing Plans for a typo, bilingual parity correction, version-only metadata update, evidence reconciliation, or routine release closure unless implementation scope unexpectedly expands.

## 2A.3 v0.3.2 skill policy

v0.3.2 is a release-closure and stabilization administration phase for an already developed local candidate.

For v0.3.2:

```text
do not restart product brainstorming
do not produce a new feature design
do not create an implementation plan merely for release administration
preserve and reconcile the existing candidate
```

If a bug, failed check, source/runtime disagreement, stale evidence conflict, or unexpected behavior appears:

```text
invoke Systematic Debugging before proposing a fix
identify and record the root-cause hypothesis
test the smallest hypothesis
do not stack speculative fixes
```

If production code or externally observable behavior must change:

```text
invoke Test-Driven Development
write the smallest failing regression test first
run it and observe the expected RED failure
implement the minimum root-cause fix
run the focused test and observe GREEN
run relevant regression checks
refactor only while tests remain GREEN
```

Exceptions are limited to:

```text
version metadata
Changelog prose
Goal/Brief execution metadata
evidence records that do not alter runtime behavior
```

A change that appears administrative but changes runtime behavior is not exempt.

Before stating any form of:

```text
fixed
passed
clean
ready
merge-ready
release-ready
approved
complete
```

invoke Verification Before Completion and obtain fresh evidence for the exact claim.

## 2A.4 v0.4.0 Brainstorming policy

v0.4.0 must invoke Brainstorming before production implementation.

The purpose of Brainstorming is:

```text
inspect the actual current repository after v0.3.2 release
map existing config/settings/main-window/compact boundaries
compare 2–3 implementation approaches where implementation choices remain
select the approach that best fits the Engineering Standard
identify data flow, error behavior, compatibility behavior, and test boundaries
convert the locked Product Brief into an implementation design
```

Brainstorming must not redesign the already locked product outcome.

The following are implementation questions, not product reopening:

```text
which existing API owns legacy-scale inference
whether WindowMetrics belongs in a new pure module or an existing pure module
how current compact state stores expanded geometry
which exact config normalization boundary introduces window_scale_percent
what measured lower slider bound is safe
which focused tests prove migration and transactional semantics
```

For choices not fixed by the Goal:

1. inspect current code, docs, and recent relevant history;
2. identify 2–3 viable approaches when meaningful alternatives exist;
3. compare trade-offs against the Engineering Standard and Scope Lock;
4. choose the recommended approach autonomously when one is clearly superior and remains inside the locked product outcome;
5. record the rationale in the design spec.

Pause for maintainer input only when a material ambiguity produces incompatible product outcomes or would require one of:

```text
security/privacy boundary change
new network, IPC, subprocess, worker, telemetry, or backend
configuration schema bump unsupported by existing evidence
breaking public API
new provider
framework rewrite
scope expansion outside Section 20
a user-visible behavior decision not resolved by this Goal
```

Routine design approval is already delegated by this Goal when the design is a direct implementation of the locked requirements.

## 2A.5 Brainstorming design artifact

After repository exploration and design selection, write:

```text
docs/superpowers/specs/YYYY-MM-DD-unified-window-scale-design.md
```

The spec must cover:

```text
goal and non-goals
current architecture observations
selected approach
rejected alternatives and trade-offs
component boundaries
public interfaces
configuration compatibility
legacy migration
settings transaction flow
main-window metric application
compact/expanded restoration
error behavior
resource/privacy analysis
test strategy
Windows 11 host validation strategy
release-document impacts
```

Before moving on, self-review the spec for:

```text
placeholders
contradictions
scope drift
ambiguous requirements
API naming inconsistencies
conflict with ENGINEERING_STANDARD.md
conflict with this ACTIVE_GOAL
```

Fix discovered issues inline.

Because this Goal explicitly authorizes autonomous execution of the locked v0.4.0 outcome, do not enter a routine human approval wait after writing the spec.

Record the spec path and review result in `Goal/EXECUTION_STATE.md`, then continue automatically to Writing Plans unless the Human Interaction Admission Gate is satisfied.

Commit the validated spec as a focused documentation checkpoint before production implementation.

## 2A.6 Writing Plans policy

After the v0.4.0 design spec is validated, invoke Writing Plans before production implementation.

Write:

```text
docs/superpowers/plans/YYYY-MM-DD-unified-window-scale-implementation.md
```

The plan must:

```text
map exact files to create or modify
define responsibility of each touched file
state exact interfaces consumed and produced by each task
split work into independently testable tasks
use checkbox steps
show RED → verify RED → GREEN → verify GREEN → refactor/verify → commit
include exact commands and expected result categories
include documentation and host-validation tasks
include final release verification
contain no TBD/TODO/implement-later placeholders
```

The plan must preserve:

```text
DRY
YAGNI
the Scope Lock in Section 20
one canonical scale source
frequent focused commits
one active version
one active branch
```

Self-review the plan for:

```text
spec coverage
placeholder language
type/signature consistency
missing tests
task ordering
scope leakage
```

Fix issues inline.

This Goal selects direct sequential execution by the current Codex run.

Do not ask the maintainer to choose:

```text
Subagent-Driven
Inline Execution
another execution mode
```

Do not require disabled Superpowers execution skills.

After the validated plan is committed:

```text
execute it task-by-task in order
update checkbox progress truthfully
use Test-Driven Development for every feature, fix, refactor, or behavior change
use Systematic Debugging whenever execution encounters a bug or unexpected failure
```

## 2A.7 Systematic Debugging policy

Invoke Systematic Debugging for any:

```text
test failure
CI failure
strict RC failure
package smoke failure
unexpected runtime behavior
source/runtime disagreement
process provenance mismatch
menu inventory mismatch
migration mismatch
performance anomaly
Windows host behavior that differs from the documented contract
```

Before a fix:

```text
read the complete error or evidence
reproduce consistently when possible
inspect recent changes
trace data across component boundaries
find a working comparable pattern in the repository
state one root-cause hypothesis
test one variable with the smallest useful change
```

Do not:

```text
add sleep because timing looks suspicious
wrap a broad except around the symptom
add retries without identifying the failing boundary
change several APIs to see whether tests become green
weaken a test solely to make the suite pass
mark physical evidence PASS to bypass a release blocker
```

When the root cause is identified, transition to TDD for the actual fix.

Record significant debugging conclusions in the relevant test, spec, execution state, compatibility evidence, or release report. Do not create duplicate narrative files for trivial failures.

## 2A.8 Test-Driven Development policy

The default rule for production behavior is:

```text
NO PRODUCTION BEHAVIOR CHANGE WITHOUT AN OBSERVED FAILING TEST FIRST
```

Required cycle:

```text
RED
→ write one minimal behavior test
→ run the exact focused test
→ confirm it fails for the expected missing/broken behavior

GREEN
→ implement the smallest correct change
→ rerun the exact focused test
→ confirm it passes

REFACTOR
→ remove duplication or improve structure only when directly useful
→ rerun the focused test
→ keep it green

REGRESSION
→ run the relevant module/group tests
→ run broader project gates at the phase boundary required by this Goal
```

The RED run must be real.

The test must not fail because of:

```text
syntax error
wrong import path
misspelled test fixture
missing dependency unrelated to the behavior
an intentionally impossible assertion
```

For a regression fix, the test must demonstrate the original symptom or contract violation.

TDD exceptions:

```text
pure prose documentation
version strings
release Changelog text
Goal/Brief execution metadata
non-runtime evidence recording
```

Generated or configuration-only changes are exempt only when they do not alter application behavior. If a configuration change changes behavior, use TDD.

Do not delete a failing test because the implementation is inconvenient unless the Goal or canonical specification proves the test is invalid.

## 2A.9 Verification Before Completion policy

Verification Before Completion is mandatory before:

```text
claiming a bug is fixed
claiming focused tests pass
claiming Quality passes
claiming package smoke passes
claiming strict readiness is ready
claiming strict RC is approved
claiming CI passes
claiming a branch is clean
claiming a PR is merge-ready
claiming main converged
claiming a tag is correct
claiming a release is complete
moving from v0.3.2 to v0.4.0
stopping at Final Definition of Done
```

For each claim:

```text
1. identify the command or direct evidence that proves the claim
2. run or retrieve it fresh for the current relevant SHA/state
3. read the complete result and exit status where available
4. compare the result to the exact claim
5. state the actual status only after evidence supports it
```

Examples:

```text
unit tests passed
→ fresh test output with zero failures

working tree clean
→ fresh git status

CI passed
→ exact PR/head SHA and successful required check state

version consistent
→ fresh version-source checker output

release-ready
→ all exact release gates required by this Goal passed for the relevant state

tag correct
→ tag SHA identified and ancestor verification passed
```

Previous output may be accepted only where this Goal explicitly allows reconciliation of evidence from the exact unchanged HEAD, such as the pre-version-bump v0.3.2 candidate RC rule in Section 6.

Do not convert:

```text
should pass
likely fixed
looks good
agent reported success
old test output from a different SHA
partial checks
```

into a success claim.

## 2A.10 Skill workflow and Human Interaction Admission Gate

A Superpowers skill does not independently authorize a human-wait state.

Before asking the maintainer a skill-related question, apply Section 2.3.

Routine skill workflow steps are not, by themselves, sufficient reasons to pause.

The following do not justify a maintainer pause when the Goal already resolves the decision:

```text
design-section approval
spec review approval
plan execution-mode choice
permission to continue to the next planned task
permission to run tests
permission to inspect source
permission to commit a verified checkpoint
permission to monitor CI
```

When a material unresolved question satisfies Section 2.3:

```text
record the required fact and attempted methods
ask one concise factual or decision question
accept any clear natural-language answer
record the answer
resume automatically
```

## 2A.11 Skill artifacts and repository documentation rules

Superpowers spec and plan files are development artifacts, not new normative product authorities.

Authority remains:

```text
ENGINEERING_STANDARD.md and other canonical project standards
approved ADRs
API_SPEC / CONFIGURATION / ROADMAP according to project precedence
Goal/ACTIVE_GOAL.md for current execution
Goal/ACTIVE_VERSION_BRIEF.md for the active version
```

A Superpowers spec or plan:

```text
must not contradict canonical project documents
must not silently expand product scope
must not replace required API/configuration/product documentation
must be updated or superseded when implementation evidence invalidates a design assumption
```

English remains canonical for required normative bilingual document pairs.

The Superpowers development spec and plan may remain English-only unless the project manifest or document class rules explicitly register them as a required bilingual pair.

---

# 3. Continuous execution and version isolation

The same Codex execution may continue from v0.3.2 into v0.4.0, but never concurrently.

At all times:

```text
one active product version
one active release branch
one active PR
one Active Version Brief
one locked scope
```

Forbidden:

```text
coding v0.4.0 while v0.3.2 PR is open
putting v0.4.0 files into v0.3.2
creating v0.4.0 from the v0.3.2 branch
one PR with two versions
one tag representing two releases
postponing two completed versions and merging them together
```

---

# 4. Phase A — Reconcile and preserve the local v0.3.2 candidate

Run immediately:

```powershell
git fetch --all --prune --tags
git status
git branch --show-current
git log -15 --oneline --decorate
git diff
git diff --cached
git branch -vv
git tag --points-at origin/main
```

Determine:

```text
actual local branch
actual HEAD SHA
actual base SHA
working-tree changes
staged changes
unpushed commits
interrupted merge/rebase/cherry-pick state
whether strict RC was run at current HEAD
whether evidence files changed after the last strict RC
```

## 4.1 Preservation rules

Do not:

```text
git reset --hard
discard local evidence
recreate v0.3.2 from scratch
blindly copy remote main over local work
blindly cherry-pick old PR #2
```

If a valid v0.3.2 branch already exists, continue it.

If local candidate work exists on another branch, preserve it before reorganizing.

If no release branch exists but the local candidate is valid, create or move the work safely onto:

```text
release/v0.3.2-win11-stabilization
```

Do not alter content merely to normalize the branch name.

## 4.2 Candidate checkpoint push

Because remote state currently does not show v0.3.2, verified candidate work must not remain local-only.

When the candidate state is understood:

1. run the smallest checks needed to verify the checkpoint;
2. commit verified candidate/evidence work only;
3. push the v0.3.2 release branch;
4. update `Goal/EXECUTION_STATE.md`;
5. record the remote branch SHA.

This checkpoint may still report application version `0.3.1`.

Do not claim that the checkpoint is a released v0.3.2.

---

# 5. Phase B — Replace stale Goal metadata and Brief

On the v0.3.2 branch, replace stale execution metadata.

## 5.1 ACTIVE_GOAL

This file becomes:

```text
Goal/ACTIVE_GOAL.md
```

It is the only normative Goal.

## 5.2 ACTIVE_VERSION_BRIEF

Replace the old v0.3.1 Brief with a concise v0.3.2 Brief.

Required identity:

```text
Version: 0.3.2
Branch: actual active v0.3.2 branch
Base: actual main SHA from which the candidate originated
PR: [v0.3.2] Complete Windows 11 release stabilization
Tag: v0.3.2
```

Product outcome:

```text
Close the declared Windows 11 x64 physical release gates and formally publish the already validated stabilization candidate without adding a feature.
```

Product Decision:

```text
GO
```

Explicit non-goals:

```text
unified window scaling
settings redesign
new menu actions
new quota behavior
new provider
Windows 10
installer
updater
telemetry
v0.4.0 code
```

---

# 6. Phase C — Accept prior candidate evidence without manufacturing a new human gate

The maintainer reports:

```text
v0.3.2 complete strict RC passed
application version is still 0.3.1
formal release steps were not performed
```

Treat this as a candidate-state fact to reconcile.

## 6.1 Validate the fact against local state

Check:

```text
current HEAD
current working tree
strict RC output if recorded
compatibility matrix state
dated physical test records
EXECUTION_STATE
```

If the strict RC was run at the exact current HEAD and no RC-relevant file changed afterward:

```text
accept it as the pre-version-bump candidate RC result
```

Do not repeat physical confirmation solely to obtain another human statement.

If RC-relevant files changed afterward:

```text
rerun strict RC autonomously
```

## 6.2 Menu sanity check

A previous old menu was observed, then disappeared after a full application restart.

Remote source contract contains exactly five menu items.

Before final release evidence:

1. exit the project process through its own Exit action or a verified app-local shutdown path;
2. confirm the project process is gone;
3. start from the current v0.3.2 working tree;
4. verify process CommandLine points to the current working tree;
5. inspect the current menu implementation and runtime/Tk menu structure;
6. verify exactly:

```text
显示设置
置顶
锁定位置
隐藏窗口
退出
```

7. verify these are absent:

```text
立即刷新
复制诊断摘要
恢复上次设置
```

If the source, process path, and runtime menu structure agree:

```text
record PASS and continue automatically
```

Do not ask the maintainer to repeat the five-item confirmation.

Escalate to the full runtime-provenance audit only if the obsolete menu reappears or runtime and source disagree again.

---

# 7. Phase D — Complete v0.3.2 release administration autonomously

When candidate physical evidence and strict RC are valid:

## 7.1 Version bump

Update all authoritative version sources:

```text
0.3.1 → 0.3.2
```

Use the repository version-source checker to discover authoritative sources.

Do not create a second version constant.

## 7.2 Changelog

Add formal bilingual sections:

```text
## 0.3.2 - YYYY-MM-DD
```

Describe only:

```text
Windows 11 x64 stabilization evidence
physical release-gate closure
strict Release Candidate approval
minimal directly required stabilization correction, if one actually occurred
```

Do not describe v0.4.0.

Do not describe repository branch protection as an application feature.

The existing historical `Unreleased` section may contain stale accumulated items. Do not perform a broad Changelog rewrite in v0.3.2 unless a release checker requires it. Record a future documentation-hygiene candidate instead.

## 7.3 Final checks after version metadata changes

Run:

```powershell
python -m compileall -q scripts
python -m unittest discover -s tests -q
python scripts/run_quality_checks.py
python scripts/package_smoke_test.py
python scripts/check_release_readiness.py --strict
git diff --check
python scripts/run_release_candidate_checks.py
```

The final RC must run after the version and Changelog update.

Required:

```text
Quality approved
Package smoke approved
Strict readiness ready
Whitespace clean
Release Candidate approved
Version sources consistent at 0.3.2
```

## 7.4 Push and PR

Push the verified branch.

PR title:

```text
[v0.3.2] Complete Windows 11 release stabilization
```

PR body:

```text
single release outcome
physical Windows environment
evidence closed
candidate RC before version bump
final RC after version bump
known non-blocking limitations
resource impact
security/privacy impact
repository protection status
rollback
No v0.4.0 work was included
```

Open the PR and monitor CI autonomously.

Do not pause merely to tell the maintainer “CI is pending.”

Poll or re-check through available GitHub tooling at a reasonable bounded interval.

Do not busy-loop.

When CI succeeds, continue.

If CI fails:

```text
read the failing job
fix only the v0.3.2 issue
rerun focused tests
push
wait for CI
```

---

# 8. Repository safety — main protection with no browser dependency

`main` protection is repository administration, not a product version feature.

## 8.1 Autonomous inspection first

Use available GitHub API, connector, or an existing authenticated `gh` CLI session to inspect:

```text
branch protection
repository rulesets
required status contexts
```

Never read, print, or copy authentication tokens.

Do not automate a browser.

## 8.2 Desired policy

When repository plan/API supports it, configure `main` to require:

```text
pull request before merge
successful required status check
linear history
force pushes blocked
deletion blocked
conversation resolution
```

Use the actual successful check context associated with:

```text
Windows Quality
quality
```

Discover the exact status context from GitHub; do not invent it.

For the current solo-maintainer workflow, do not require:

```text
one external approving review
CODEOWNER approval
approval by another person
```

## 8.3 If settings can be changed safely through API/CLI

Apply the policy autonomously.

Verify non-destructively through repository metadata and the PR merge requirements.

Do not test by:

```text
force-pushing main
deleting main
making a destructive direct push
```

## 8.4 If API, repository plan, or permissions prevent configuration

Do not stop v0.3.2 and do not repeatedly ask the maintainer to open GitHub settings.

Record:

```text
exact API or plan limitation
main protection = unresolved repository administration risk
```

Use mandatory compensating controls:

```text
no direct main push
all changes through version PR
verify exact PR head SHA
wait for Windows Quality success
squash merge
fetch main after merge
rerun Quality and RC on main
tag only verified main
verify tag is reachable from main
delete release branch
```

Create a repository-administration follow-up note.

Only ask the maintainer when the remaining decision is specifically:

```text
whether to pay for or change the GitHub plan
```

Do not purchase, upgrade, or make the private repository public automatically.

---

# 9. Phase E — Merge, main convergence, tag v0.3.2

Before merge:

```text
[ ] exact PR head SHA known
[ ] remote Quality succeeded
[ ] final strict RC succeeded
[ ] version sources = 0.3.2
[ ] formal bilingual 0.3.2 Changelog exists
[ ] physical evidence is truthful
[ ] no v0.4.0 file or behavior included
```

Use:

```text
squash merge
```

After merge:

```powershell
git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
python scripts/run_quality_checks.py
python scripts/package_smoke_test.py
python scripts/check_release_readiness.py --strict
python scripts/run_release_candidate_checks.py
```

Run a lightweight tagged-build smoke on the physical Windows 11 host.

Verify:

```text
launch
five stable rows
Reset Credit date
five-item menu
compact/hover behavior already closed by current evidence
hide/show
exit
relaunch
single process
no persistent CMD
```

Create:

```text
v0.3.2
```

on the exact verified main commit.

Push the tag.

Verify:

```powershell
git merge-base --is-ancestor v0.3.2 origin/main
```

Delete the v0.3.2 release branch.

Write the v0.3.2 release report.

Then, and only then, transition to v0.4.0.

---

# 10. v0.3.2 → v0.4.0 Transition Gate

Every item must be true:

```text
[ ] v0.3.2 PR merged
[ ] origin/main contains v0.3.2
[ ] post-merge Quality passed
[ ] post-merge strict RC passed
[ ] v0.3.2 remote tag exists
[ ] v0.3.2 tag is reachable from origin/main
[ ] v0.3.2 post-release smoke passed
[ ] v0.3.2 branch deleted
[ ] working tree clean
[ ] no interrupted Git operation
[ ] v0.3.2 release report complete
[ ] ACTIVE_VERSION_BRIEF ready to be replaced
```

If any box is false:

```text
remain in v0.3.2
```

When all pass:

```powershell
git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git switch -c release/v0.4.0-unified-window-scale origin/main
```

Replace the Brief with v0.4.0.

Then execute the Section 2A v0.4.0 skill sequence:

```text
Using Superpowers
→ Brainstorming
→ validated design spec
→ focused spec commit
→ Writing Plans
→ validated implementation plan
→ focused plan commit
→ sequential TDD implementation
```

Do not begin v0.4.0 production implementation before the design spec and implementation plan are validated.

Do not append v0.4.0 content to the v0.3.2 Brief.

---

# 11. v0.4.0 Product Brief — Unified Window Scale

## 11.1 Product outcome

```text
Replace separate font-size and free-form window-size controls with one proportional Window Size slider that scales the overlay and typography together.
```

Product Decision:

```text
GO
```

## 11.2 User problem

Current settings expose too many coupled low-level controls:

```text
Font Size slider
Window Width input
Window Height input
minus button
plus button
Proportional Scaling checkbox
```

The user must understand relationships between font size, window geometry, aspect ratio, and clipping.

This increases configuration complexity and makes unsafe combinations possible.

## 11.3 User-visible goal

The settings dialog must contain exactly two Tk `Scale` controls:

```text
透明度
窗口大小
```

The dialog may still contain non-slider settings:

```text
默认位置 X/Y
刷新间隔
置顶
锁定位置
空闲时收缩
字体颜色
背景颜色
保存
应用
恢复默认值
关闭
```

---

# 12. v0.4.0 Visual/UI/UX contract

Remove from the normal settings dialog:

```text
字体大小 slider
窗口宽度 input
窗口高度 input
− size button
+ size button
等比例缩放 checkbox
```

Add:

```text
窗口大小 [ proportional slider ]
```

Target hierarchy:

```text
透明度       [ slider ]
窗口大小     [ slider ]
默认位置     [ X ] , [ Y ]
刷新间隔     [ seconds ]
置顶         [ checkbox ]
锁定位置     [ checkbox ]
空闲时收缩   [ checkbox ]
字体颜色     [ button ]
背景颜色     [ button ]
保存 / 应用 / 恢复默认值 / 关闭
```

Design requirements:

```text
two sliders aligned
no gaps left by removed rows
percentage understandable to the user
no advanced size panel
no hidden duplicate font-size control
no free width/height mode
no resize animation
no decorative UI added
```

---

# 13. v0.4.0 Unified Scale model

Use one canonical scale source of truth.

Recommended constants:

```text
BASE_WINDOW_WIDTH = 330
BASE_WINDOW_HEIGHT = 138
BASE_TEXT_FONT_SIZE = 10
BASE_FACE_FONT_SIZE = 28
DEFAULT_WINDOW_SCALE_PERCENT = 100
```

All expanded geometry derives from:

```text
window_scale_percent
```

Core calculation:

```text
scale = window_scale_percent / 100

width  = round(BASE_WINDOW_WIDTH × scale)
height = round(BASE_WINDOW_HEIGHT × scale)
```

Fixed aspect contract:

```text
330 : 138
```

The user cannot independently change width and height.

## 13.1 Slider range

Initial engineering candidate:

```text
80% to 200%
step 5%
default 100%
```

Do not hard-code an unsafe minimum simply because 80% looks neat.

The final minimum must be the smallest percentage at which:

```text
all five rows remain readable
Reset Credit date remains visible
layout remains usable
menu and drag behavior remain intact
```

If 80% fails, raise the minimum.

The upper bound may be reduced if geometry or practical screen use becomes unreasonable.

Document the measured final range.

---

# 14. v0.4.0 Pure metrics API

Create one pure calculation boundary, preferably:

```text
scripts/api/window_scale_api.py
```

Recommended immutable result:

```python
@dataclass(frozen=True)
class WindowMetrics:
    scale_percent: int
    width: int
    height: int
    text_font_size: int
    face_font_size: int
    horizontal_padding: int
    vertical_padding: int
    wraplength: int
```

Provide pure functions for:

```text
clamp scale
quantize scale
derive metrics
infer scale from legacy geometry
```

Do not duplicate scale formulas in:

```text
settings dialog
main window
config API
compact logic
tests
```

The UI and runtime consume the same pure metrics result.

---

# 15. Adaptive typography and visual metrics

At minimum:

```text
text font size derives from scale
paw/face font derives from scale
window width derives from scale
window height derives from scale
wraplength derives from scale
```

Review and scale only the spacing metrics necessary to preserve visual balance:

```text
horizontal padding
vertical padding
face/text gap
```

Requirements:

- use Tk font rendering;
- no bitmap scaling;
- font size changes monotonically with window scale;
- no independent font-size source of truth;
- no clipping throughout supported range;
- five rows remain individually rendered.

---

# 16. Configuration compatibility

Current configuration uses independent fields:

```text
font_size
window_width
window_height
scale_mode
```

v0.4.0 introduces:

```text
window_scale_percent
```

## 16.1 Canonical source

For v0.4.0:

```text
window_scale_percent = canonical source of truth
```

Derived compatibility fields:

```text
font_size
window_width
window_height
scale_mode
```

Persist derived compatibility values so v0.3.2 can still read a usable configuration.

Recommended:

```text
scale_mode = proportional
window_width = derived width
window_height = derived height
font_size = derived text font size
```

## 16.2 Schema decision

Do not bump the configuration schema automatically.

First perform a compatibility review.

Because an older version can ignore an unknown `window_scale_percent` field while reading the derived legacy fields, the preferred design is:

```text
keep schema version 1
```

A schema bump is allowed only when implementation evidence proves that the old contract cannot safely represent the saved settings.

If a schema bump becomes necessary:

```text
stop scope implementation
document migration and downgrade consequences
perform Product + Backend + Security/Resource review
```

Do not silently change the schema.

---

# 17. Legacy settings migration

For a valid existing configuration without `window_scale_percent`:

1. read validated legacy width and height;
2. infer one deterministic scale;
3. clamp to supported range;
4. quantize to slider step;
5. derive fixed-ratio geometry and adaptive typography.

Preferred inference:

```text
raw_scale =
sqrt(
    (old_width × old_height)
    /
    (BASE_WINDOW_WIDTH × BASE_WINDOW_HEIGHT)
)
```

Then:

```text
scale_percent = quantize(clamp(raw_scale × 100))
```

Rationale:

```text
legacy free-width or free-height distortions do not let one dimension dominate
visual area is preserved approximately
migration is deterministic
```

Required properties:

```text
default legacy geometry maps to 100%
same legacy input always maps to same scale
extreme values clamp
invalid inputs use safe defaults
migration does not overwrite a protected malformed/future config
```

Preserve:

```text
position
alpha
font color
background color
refresh interval
topmost
locked
compact_when_idle
```

---

# 18. Transactional settings behavior

Preserve exact semantics:

```text
Apply = preview runtime draft, dialog remains open
Save = apply + persist + close
Close = discard unsaved draft/session changes
Restore Defaults = reset draft to defaults
```

Unified slider behavior:

```text
moving slider changes draft only
Apply derives and applies complete WindowMetrics
Save persists scale and derived compatibility fields
Close without Apply/Save does not mutate runtime or disk
repeated Apply at same scale is idempotent
Restore Defaults sets scale to 100%
```

Do not trigger quota refresh because the size slider moves.

Do not add a worker or timer for scaling.

---

# 19. Main-window integration

On load or Apply:

```text
window_scale_percent
→ derive WindowMetrics once
→ apply one coherent metrics result
```

Update together:

```text
geometry
status text font
paw font
wraplength
required visual padding
```

Preserve:

```text
five stable rows
position recovery
Hide/Show
Compact/Expanded
monitor recovery
lock
drag
menu
topmost
```

Compact mode must remember the derived expanded geometry.

Expanding after hover must restore the current unified scale, not an old width/height pair.

---

# 20. v0.4.0 Scope Lock

Preferred production files:

```text
scripts/api/window_scale_api.py
scripts/api/config_api.py
scripts/ui/settings_dialog.py
scripts/ui/main_window.py
scripts/api/settings_session_api.py if directly required
compact/display geometry API only if directly required
```

Tests:

```text
window scale API
legacy migration
configuration normalization
settings transaction
exact settings-control inventory
main-window metric application
compact/expanded restoration
Hide/Show
position recovery
restart persistence
```

Docs:

```text
CHANGELOG.md
CHANGELOG.zh-CN.md
configuration documentation pair
API/architecture documentation pair
product/settings documentation pair
Windows 11 test record
```

Forbidden:

```text
theme presets
font-family selection
manual resize handles
manual width
manual height
manual font size
aspect-ratio toggle
new quota feature
new refresh feature
new context-menu action
installer
updater
Windows 10
telemetry
external API
unrelated cleanup
```

---

# 21. v0.4.0 Automated test contract

## 21.1 Pure scale

Test:

```text
100% yields canonical metrics
minimum yields safe metrics
maximum yields bounded metrics
quantization deterministic
aspect ratio stable within rounding tolerance
text font monotonic
face font monotonic
repeated derivation stable
```

## 21.2 Migration

Test:

```text
legacy 330x138 maps to 100%
arbitrary legacy geometry maps deterministically
extreme geometry clamps
invalid scale falls back safely
valid new scale reloads identically
legacy font_size is not an independent source after migration
future schema remains protected
malformed config remains protected
```

## 21.3 Settings dialog

Test exact control inventory:

```text
exactly two Tk Scale widgets
透明度 exists
窗口大小 exists
字体大小 control absent
window width input absent
window height input absent
minus size button absent
plus size button absent
等比例缩放 absent
position entries remain
refresh entry remains
ordinary checkboxes remain
color buttons remain
```

Test:

```text
Apply
Save
Close
Restore Defaults
```

## 21.4 Main-window integration

Test:

```text
one scale result updates geometry and fonts
five rows persist
Hide/Show retains scale
Compact/Expand retains scale
position recovery uses derived geometry
restart retains scale
```

---

# 22. v0.4.0 Windows 11 host validation — autonomous-first

Test the current physical Windows 11 host at:

```text
minimum supported scale
100%
one middle-large scale
maximum supported scale
```

At each scale verify through the actual running build and safe local inspection:

```text
derived geometry
fixed ratio
five row widgets
Reset Credit date row
font metrics
menu placement
drag/lock
Hide/Show
Compact/Hover
restart persistence
```

Use Tk/Win32/widget/geometry inspection where it can establish the fact.

Human visual confirmation is not required merely because this is a UI feature.

Only use the Human Interaction Admission Gate for a fact that truly cannot be established through the running Windows host or safe app interaction.

Do not require exact confirmation wording.

---

# 23. v0.4.0 Resource and privacy gate

Expected:

```text
new network: No
new IPC: No
new worker: No
new subprocess: No
new polling: No
new paid service: No
new telemetry: No
Codex quota consumption caused by scaling: No
```

Metric calculation must be bounded and effectively constant time.

Slider movement must not trigger:

```text
quota requests
activity scans
disk writes before Save
background jobs
```

Any unexpected `Yes` requires a scope review before merge.

---

# 24. v0.4.0 Release lifecycle

Branch:

```text
release/v0.4.0-unified-window-scale
```

PR:

```text
[v0.4.0] Unify window and typography scaling
```

Version:

```text
0.4.0
```

Tag:

```text
v0.4.0
```

Before PR:

```text
focused tests
full Quality
package smoke
strict readiness
strict RC
version-source consistency
bilingual Changelog
Windows 11 host validation
```

Push promptly.

Monitor remote CI autonomously.

Merge only after CI success.

Use squash merge.

After merge:

```text
fetch main
full Quality
package smoke
strict RC
post-release Windows smoke
tag verified main
push tag
verify tag ancestor
delete branch
```

PR body must state:

```text
one unified-scale outcome
controls removed
fixed-ratio contract
adaptive typography contract
legacy migration
configuration compatibility
test results
Windows host evidence
resource impact
rollback
No v0.4.1 or later work was included
```

---

# 25. Branch protection and PR safety remain active during v0.4.0

If server-side `main` protection was successfully enabled:

```text
verify the v0.4.0 PR is subject to the required Quality check
```

If protection remains unavailable:

```text
verify exact head SHA
wait for Quality success
squash merge only
post-merge main retest
tag only verified main
```

Do not normalize direct pushes to main.

---

# 26. EXECUTION_STATE policy

Use:

```text
Goal/EXECUTION_STATE.md
```

only while execution is active or interrupted.

Required fields:

```markdown
# Execution State

- Active version:
- Branch:
- Base main SHA:
- Current HEAD:
- Last pushed SHA:
- Current phase:
- Product decision:
- Scope lock:
- Active Superpowers skill:
- Design spec:
- Implementation plan:
- Latest RED evidence:
- Latest GREEN evidence:
- Latest completion verification:
- Candidate RC state:
- Final RC state:
- Remote CI state:
- Main protection state:
- Autonomous checks completed:
- Human fact required:
- Methods attempted:
- Why human input is necessary:
- Completed:
- Remaining:
- Next exact action:
- Last updated:
```

Rules:

- `Human fact required` must be `None` by default.
- `Active Superpowers skill` records the current applicable enabled skill or `None` for ordinary administrative steps.
- `Design spec` and `Implementation plan` remain `None` during v0.3.2 and are populated for v0.4.0.
- RED/GREEN evidence records the latest material TDD cycle; do not fabricate a RED run retroactively.
- `Latest completion verification` records the fresh evidence used for the most recent success/readiness claim.
- Do not enter a human-wait state without satisfying the Human Interaction Admission Gate.
- When input is no longer required, clear the human-wait fields and resume.
- Never store credentials or private conversation content.

---

# 27. Checkpoint and usage interruption

Continue while official service capacity permits.

Do not stop because an arbitrary five-hour planning window ended.

Do not bypass or evade service limits.

Before a hard interruption:

```text
finish current safe operation
do not leave a speculative debugging stack without recording the current root-cause hypothesis
do not claim GREEN unless the focused test actually passed
run smallest relevant tests
commit verified work only
push checkpoint
update EXECUTION_STATE
record active skill and TDD/verification evidence where applicable
record Next exact action
```

Resume from the pushed checkpoint.

Do not redo completed verified work.

---

# 28. Required release reports

## v0.3.2 report

Include:

```text
local candidate branch and initial HEAD
candidate RC evidence
autonomous menu sanity result
version bump
final RC
PR URL
remote CI
main protection status
merge SHA
v0.3.2 tag SHA
post-release smoke
resource/security impact
Superpowers skills actually invoked
fresh verification evidence for the release-ready and complete claims
```

Explicitly state:

```text
No v0.4.0 work was included in v0.3.2.
```

## v0.4.0 report

Include:

```text
Product decision
final slider range
canonical base metrics
fixed-ratio result
removed control inventory
migration algorithm
schema decision
automated tests
Windows host validation
resource impact
PR URL
remote CI
merge SHA
v0.4.0 tag SHA
post-release smoke
rollback
Brainstorming design spec path
Writing Plans implementation plan path
material Systematic Debugging conclusions, if any
representative RED/GREEN evidence
fresh verification evidence for the release-ready and complete claims
```

Explicitly state:

```text
No v0.4.1 or later work was included.
```

---

# 29. Final Definition of Done

## v0.3.2

```text
[ ] local candidate preserved
[ ] candidate state reconciled
[ ] candidate checkpoint pushed to GitHub
[ ] Using Superpowers routed material task categories
[ ] any encountered bug/failure was root-cause investigated before a fix
[ ] any production-code fix used an observed failing regression test first
[ ] release-ready and completion claims use fresh verification evidence
[ ] ACTIVE_GOAL corrected
[ ] ACTIVE_VERSION_BRIEF corrected to v0.3.2
[ ] stale human five-menu approval gate removed
[ ] five-item menu sanity verified autonomously
[ ] candidate strict RC evidence reconciled
[ ] version sources updated to 0.3.2
[ ] bilingual 0.3.2 Changelog added
[ ] final Quality passed
[ ] final strict RC passed
[ ] v0.3.2 PR created
[ ] remote CI passed
[ ] main protection applied or exact limitation recorded
[ ] PR squash-merged
[ ] main retested
[ ] v0.3.2 tag pushed
[ ] tag reachable from main
[ ] release branch deleted
[ ] post-release smoke passed
```

## v0.4.0

```text
[ ] v0.3.2 transition gate passed before coding
[ ] v0.4.0 branch created from latest main
[ ] v0.4.0 Brief replaced the prior Brief
[ ] Using Superpowers routed the v0.4.0 workflow
[ ] Brainstorming inspected the actual post-v0.3.2 repository
[ ] Brainstorming design spec written, self-reviewed, and committed
[ ] Writing Plans implementation plan written, self-reviewed, and committed
[ ] production behavior changes followed observed RED → GREEN → REFACTOR discipline
[ ] any unexpected failure used Systematic Debugging before the fix
[ ] completion/readiness claims use fresh verification evidence
[ ] settings dialog has exactly two Scale widgets
[ ] transparency slider remains
[ ] unified window-size slider exists
[ ] font-size slider removed
[ ] width input removed
[ ] height input removed
[ ] minus/plus size buttons removed
[ ] proportional checkbox removed
[ ] one canonical scale source exists
[ ] aspect ratio is fixed
[ ] font size derives from scale
[ ] face font and required layout metrics derive coherently
[ ] legacy settings migrate deterministically
[ ] downgrade compatibility reviewed
[ ] protected configs remain protected
[ ] Apply/Save/Close/Restore Defaults semantics pass
[ ] five rows remain readable throughout supported range
[ ] Compact/Expand preserves scale
[ ] Hide/Show preserves scale
[ ] no new resource/privacy boundary introduced
[ ] focused tests passed
[ ] full Quality passed
[ ] strict RC passed
[ ] Windows 11 host validation passed
[ ] version sources = 0.4.0
[ ] bilingual 0.4.0 Changelog added
[ ] v0.4.0 PR remote CI passed
[ ] PR squash-merged
[ ] main retested
[ ] v0.4.0 tag pushed
[ ] tag reachable from main
[ ] release branch deleted
[ ] post-release smoke passed
```

Then stop.

Do not implement v0.4.1, v0.5.0, or later work under this Goal.

---

# 30. Non-executable long-term direction

The following is planning context only.

Possible future themes, each requiring a new Goal and one version at a time:

```text
v0.4.1 — only defects discovered after unified-scale release
v0.5.x — one passive display clarity improvement, selected after real use
v0.6.x — bounded resource/logging refinement if measurements justify it
v0.7.x — reproducible packaging and install/uninstall workflow
v0.8.x — upgrade/downgrade validation
v0.9.x — feature freeze, measured resource profile, release hardening
v1.0.0 — trustworthy stable product contract
```

Do not pre-implement these placeholders.

The long-term target remains:

```text
accurate
passive
compact
local-only
low-resource
recoverable
testable
small-versioned
honest about support
```
