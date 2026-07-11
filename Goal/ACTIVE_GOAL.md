# ACTIVE GOAL — 完成 v0.3.2 Windows 11 稳定化并保护 main

> **Repository:** `TomTang701/codex-windows-status-pet`
> **Authority:** 本文件替换旧的 `Goal/ACTIVE_GOAL.md`，是唯一规范性Goal
> **Verified remote main:** `d4a69e9ce4a6adc7d519ff1a37b00617d548e8dd`
> **Verified remote product version:** `0.3.1`
> **Verified remote tag:** `v0.3.1` points to the current `main`
> **Current target version:** `0.3.2`
> **Release theme:** Windows 11 physical stabilization and strict Release Candidate closure
> **Supported platform:** Windows 11 x64
> **Repository safety gate:** Protect `main` before merging v0.3.2 when the GitHub plan supports it
> **Execution model:** One active version, one branch, one PR, one tag
> **Authorized sequence:** first complete v0.3.2, then implement v0.4.0 as a separate release
> **Final end condition:** v0.4.0 merged, verified, tagged, and reported

---

# 0. Immediate instruction

Read this file completely before changing production code or release evidence.

Continue the existing local v0.3.2 work if it exists.

Do **not**:

- discard or reset verified local v0.3.2 work;
- recreate the branch from scratch without checking local and remote state;
- start v0.3.3 or v0.4.0;
- add product features;
- use browser automation to control Chrome;
- claim a physical pass without direct evidence;
- change `main` directly;
- weaken Release Candidate checks to obtain a pass.

The first action is repository and checkpoint reconciliation, not implementation.

---

# 1. Current verified repository state

Remote state verified before this Goal was created:

```text
main SHA: d4a69e9ce4a6adc7d519ff1a37b00617d548e8dd
main version: 0.3.1
tag v0.3.1: identical to main
latest merged PR: #10 [v0.3.1] Extract main-window controllers
latest Quality workflow: Windows Quality
required-quality job candidate: quality
open v0.3.2 PR: none observed at inspection time
```

Important repository inconsistency:

```text
Goal/ACTIVE_GOAL.md metadata still describes the old 0.2.0 / 0.2.1 baseline.
Goal/ACTIVE_VERSION_BRIEF.md on remote main still describes v0.3.1.
```

This Goal corrects the active target to v0.3.2.

Do not edit remote `main` directly to fix those files. Update them on the active v0.3.2 release branch and merge through the normal release PR.

---

# 2. Existing local v0.3.2 physical checkpoint

Treat the following as maintainer-provided evidence that must be recorded accurately, not reinterpreted.

## Confirmed

```text
Operating system:
Windows 11 Home x64
Build 26200

Display environment:
Two monitors
Both monitors at 96 DPI
Bottom taskbar

Runtime:
Overlay HWND was observed and valid
Repeated launch stabilized at one actual application process
No persistent CMD window remained

Visual smoke:
Application window displayed successfully
Five independent status rows were visible
Reset Credit date was visible
```

## Not yet confirmed

```text
Compact idle shrink
Hover expansion
Context-menu physical behavior
Strict Release Candidate success
Any remaining blocker reported by the current strict readiness checker
```

## Interruption cause

The previous automation attempt stopped because it could not reliably confirm the active Chrome URL and the safety mechanism terminated the operation.

This is **not** a product defect.

Do not resume browser automation.

Use only:

- repository commands;
- PowerShell;
- process inspection;
- Win32/Tk inspection;
- direct interaction with the status-pet window;
- user-confirmed manual steps when a physical action cannot be identified safely.

---

# 3. Scope lock

## 3.1 One-sentence outcome

```text
v0.3.2 truthfully closes the claimed Windows 11 x64 physical release gates and passes the strict Release Candidate without adding a feature.
```

## 3.2 Allowed

```text
Goal/ACTIVE_GOAL.md
Goal/ACTIVE_VERSION_BRIEF.md
Goal/EXECUTION_STATE.md while the version is active
docs/quality/COMPATIBILITY_MATRIX.md
direct Chinese translation if one exists
docs/quality/test-records/*
scripts/check_release_readiness.py only when needed to make the existing release policy accurate
tests for release-readiness behavior
version sources
CHANGELOG.md
CHANGELOG.zh-CN.md
release documentation directly affected by physical evidence
minimum defect fixes discovered by physical validation
```

## 3.3 Forbidden

```text
new user feature
new menu item
manual refresh
theme presets
new provider
new settings option
new external dependency
Windows 10 implementation
automatic updater
installer redesign
telemetry
cloud logging
third-party API
unrelated controller refactor
unrelated status-row redesign
v0.4.0 planning implementation
```

## 3.4 Defect rule

A defect discovered during v0.3.2 may be fixed in v0.3.2 only when:

1. it directly blocks the declared Windows 11 physical result;
2. the fix is minimal;
3. the fix does not create a second product outcome;
4. focused regression tests are added;
5. all affected physical evidence is rerun.

Otherwise, record it for a later patch and do not expand this version.

---

# 4. Gate 0 — Reconcile the local working state

Run:

```powershell
git fetch --all --prune --tags
git status
git branch --show-current
git log -10 --oneline --decorate
git diff
git diff --cached
git branch -vv
git tag --points-at origin/main
```

Then determine:

```text
current local branch
whether release/v0.3.2-* already exists
whether local commits are unpushed
whether files are modified but uncommitted
whether a cherry-pick/rebase/merge is active
whether the local branch started from d4a69e9
whether remote main has moved
```

Rules:

- If a valid v0.3.2 branch already exists, continue it.
- If verified work is uncommitted, preserve it and inspect the diff before committing.
- If verified work is committed but unpushed, run the relevant checks and push a checkpoint.
- If no v0.3.2 branch exists, create:

```powershell
git switch -c release/v0.3.2-win11-stabilization origin/main
```

- Never branch v0.3.2 from the old v0.3.1 release branch.
- Never reset hard or delete local evidence without a maintainer-approved recovery plan.

---

# 5. Gate 1 — Create the v0.3.2 Active Version Brief

Replace the old brief with:

```text
Goal/ACTIVE_VERSION_BRIEF.md
```

Required identity:

```text
Version: 0.3.2
Branch: actual active v0.3.2 branch
Base: verified latest main SHA
PR: [v0.3.2] Complete Windows 11 release stabilization
Tag: v0.3.2
```

Required Product decision:

```text
GO
```

Required role applicability:

| Role | Applicability |
|---|---|
| Product | Yes |
| Visual/UI/UX | Physical verification only |
| Frontend | Yes |
| Backend | Lifecycle/process verification only |
| QA/Release | Yes |
| Security/Resource | Yes |
| Repository administration | Yes |

The Brief must explicitly state:

```text
No new feature
No v0.4.0 work
No Windows 10 claim
No browser automation
No new network/IPC/worker/polling path
```

Keep the Brief concise. Do not paste complete test logs.

---

# 6. Gate 2 — Inventory the actual strict blockers

Before editing matrix statuses, run:

```powershell
python scripts/check_release_readiness.py --strict
```

Save the JSON output temporarily.

Create an exact blocker table:

| Matrix row | Current status | Why blocked | Required evidence | Planned resolution |
|---|---|---|---|---|

Rules:

- Use the checker output as the source of truth for executable blockers.
- Do not assume an older list of blockers is still accurate.
- Do not change a row from `partial` or `pending` merely to make the script pass.
- Every blocker must receive either:
  - physical pass evidence; or
  - an explicit maintainer-approved limitation outside the supported claim.

If the matrix wording and executable checker disagree, correct the smallest possible policy defect and add tests.

---

# 7. Gate 3 — Record already completed physical evidence

Create or update a dated record under:

```text
docs/quality/test-records/
```

Recommended filename:

```text
YYYY-MM-DD-v0.3.2-win11-physical-validation.md
```

Record:

```text
version/branch/commit
Windows edition and build
display count
DPI per monitor
taskbar location
HWND observation method
process observation method
repeated-launch result
CMD-window result
five-row result
Reset Credit date result
date/time and tester
```

Evidence integrity rules:

- State exactly what was observed.
- Do not call a visual observation “automated.”
- Do not call an automated/headless test “physical.”
- Do not include tokens, prompts, responses, session contents, browser history, private project paths, or unrelated desktop content.
- Screenshots are optional.
- If a screenshot is used, crop it to the application or relevant Windows control and remove unrelated personal content.
- A dated textual record is acceptable when it contains reproducible steps and actual results.

Already confirmed evidence does not need to be repeated unless runtime code affecting it changed after the observation.

---

# 8. Gate 4 — Complete remaining physical validation

## 8.1 Compact idle shrink and hover expansion

Verify in this order:

```text
1. Start from the intended v0.3.2 branch/build.
2. Confirm the overlay is expanded.
3. Ensure no menu, dialog, drag, or active interaction is preventing compact mode.
4. Wait through the configured idle threshold without generating artificial Codex work.
5. Observe the compact geometry.
6. Move the pointer over the overlay.
7. Confirm expansion.
8. Move the pointer away.
9. Confirm the application can become compact again.
10. Confirm all five rows return after expansion.
```

Do not consume Codex quota merely to alter activity state.

If the current Codex session itself prevents idle:

- use the existing application behavior and a genuine idle period;
- do not add a debug-only product setting;
- do not change production timing solely for the test;
- document the exact environmental limitation if the result cannot be obtained.

## 8.2 Context-menu physical behavior

Verify the menu contains exactly:

```text
显示设置
置顶
锁定位置
隐藏窗口
退出
```

Verify:

```text
right-click opens on first attempt
menu stays inside the active monitor work area
first selected action dispatches once
Escape closes
Focus loss closes
grab is released
Settings opens
Always on Top changes the intended state
Lock Position prevents drag and can be reversed
Hide Window hides without ending the process
tray Show restores the window
Exit ends the process
next launch succeeds
```

Do not restore removed actions.

## 8.3 Single-monitor evidence

The current matrix on remote main still identifies single-monitor physical evidence as incomplete.

Handle safely:

- Do not change Windows display configuration through automation without explicit maintainer confirmation.
- When the maintainer agrees, temporarily select a one-display Windows mode, launch the app, verify placement/menu/exit, then restore the original display mode.
- A sanitized textual test record is sufficient.
- If the maintainer does not approve changing display mode, record the limitation; do not falsely mark a pass.

Because single-monitor use is common within the Windows 11 support claim, prefer a real physical pass rather than making it non-blocking.

## 8.4 Bottom taskbar versus alternate taskbar edges

The supported physical target is the normal bottom taskbar.

Do not block v0.3.2 on top/left/right taskbar arrangements that are not part of the current claim.

Update the matrix so that:

```text
bottom taskbar physical behavior = blocking and physically verified
alternate taskbar edges = not claimed / non-blocking
```

Do not claim physical testing of unsupported taskbar layouts.

## 8.5 DPI

Current physical evidence:

```text
two monitors at 96 DPI
```

If no mixed-DPI environment exists:

- retain automated mixed-DPI coverage;
- mark physical mixed-DPI certification as not claimed or an approved non-blocking limitation;
- do not mark it `Physical pass`.

Do not change system scaling automatically.

## 8.6 Clean-machine startup

A separate clean Windows machine is not available in the supplied checkpoint.

Use:

```text
fresh temporary virtual environment
requirements installation
Quality
package smoke
launcher smoke on the physical Windows 11 host
```

If a separate clean-machine test remains unavailable, classify it honestly as a distribution limitation, not a core runtime physical pass.

Do not let an unclaimed clean-machine scenario masquerade as a completed physical result.

---

# 9. Gate 5 — Make the compatibility matrix truthful and executable

After physical tests:

1. Update only rows for which evidence changed.
2. Link each physical pass to a dated test record.
3. Remove wording that requires evidence outside the supported claim.
4. Ensure every row that remains partial/pending is intentionally blocking.
5. Ensure non-blocking limitations contain explicit rationale.

The current checker treats:

```text
pending
partial
```

as blockers unless a status contains:

```text
non-blocking
```

Use statuses consistently with that executable rule.

Do not exploit wording tricks.

Recommended status forms:

```text
Physical pass
Automated pass
Approved limitation / Non-blocking
Deferred / Not claimed / Non-blocking
```

When changing `scripts/check_release_readiness.py`:

- keep changes limited to policy correctness;
- update stale wording such as a hardcoded old release version;
- add focused tests;
- do not redesign the entire release framework in v0.3.2.

Then run:

```powershell
python scripts/check_release_readiness.py --strict
```

It must pass for truthful reasons.

---

# 10. Repository Safety Gate — Protect main

This is a repository-administration requirement, not a user-facing v0.3.2 feature.

It must not be described as a product feature in Changelog.

## 10.1 Why it is required

Without server-side protection, an administrator, collaborator, integration, or mistaken automation path may:

```text
push directly to main
force-push main
delete main
merge before required CI completes
bypass the small-version PR process
```

The Goal alone cannot enforce GitHub server behavior.

## 10.2 Do not automate the GitHub web UI

Because browser URL identity could not be confirmed reliably:

- do not control Chrome;
- do not use browser automation for repository settings;
- provide the maintainer with exact manual steps;
- continue after human confirmation or record a plan limitation.

## 10.3 Recommended GitHub configuration

In the repository UI:

```text
Settings
→ Rules
→ Rulesets
→ New branch ruleset
```

Target:

```text
main
```

Minimum required settings when available:

```text
Require a pull request before merging
Require status checks to pass
Block force pushes
Restrict deletions
Require linear history
```

Required status:

```text
Select the exact recent GitHub Actions check shown for the successful
Windows Quality workflow and quality job.
Do not guess the status-check context.
```

Recommended:

```text
Require conversation resolution
Require branch to be up to date before merging
Apply to administrators / do not allow bypassing, after verifying the normal PR merge still works
```

Do not require for this solo-maintainer repository unless another qualified reviewer is available:

```text
one approving review
approval of the most recent push by another person
CODEOWNER approval
```

Do not require signed commits in this Goal; it may interfere with the current squash release workflow and is a separate policy decision.

## 10.4 Safe verification

Do not test protection by:

```text
force-pushing main
deleting main
performing a destructive direct push
```

Verify safely through:

```text
the ruleset/branch-protection UI no longer showing main as unprotected
the v0.3.2 PR merge box displaying the required Quality check
the PR being unmergeable while the check is pending
normal squash merge becoming available after the check succeeds
```

Record a short repository test record:

```text
docs/quality/test-records/YYYY-MM-DD-main-protection.md
```

Do not commit screenshots that expose private repository information unless sanitized.

## 10.5 Plan limitation

GitHub plan availability may prevent branch protection on a private repository.

If the setting is unavailable:

1. Record the exact plan/UI limitation.
2. Do not change repository visibility merely to obtain protection.
3. Do not purchase or upgrade a plan automatically.
4. Ask the maintainer whether to upgrade.
5. Until then, apply all compensating controls below.

Compensating controls:

```text
never push directly to main
merge only through a version PR
verify the exact PR head SHA before merge
wait for Windows Quality / quality success
squash merge only
fetch and retest main after merge
verify the tag is reachable from main
delete the release branch
record the unprotected-main limitation in release documentation
```

An unavailable paid feature does not justify pretending that main is protected.

---

# 10A. Lightweight Runtime Sanity Gate

A previous physical run briefly showed obsolete menu entries even though current source contains only the approved five-item menu. After a full application restart the obsolete entries disappeared, which is consistent with an old in-memory process.

Before recording final v0.3.2 UI evidence:

1. Exit the existing status-pet through its own `退出` action.
2. Confirm no project-related `pythonw.exe` process remains.
3. Start the application from the current v0.3.2 working-tree root.
4. Confirm the process command line points to that working tree's `scripts/codex_status_pet.py`.
5. Confirm the context menu contains exactly:

```text
显示设置
置顶
锁定位置
隐藏窗口
退出
```

6. Confirm the following are absent:

```text
立即刷新
复制诊断摘要
恢复上次设置
```

If these checks pass, continue normal v0.3.2 physical validation.

Perform the full runtime-provenance audit only if:

- an obsolete item appears again;
- menu contents change between launches;
- the process path points to another directory;
- the running UI contradicts the checked-out source.

Do not expand v0.3.2 into a general path-discovery project when the lightweight check passes.

---

# 11. Gate 6 — Full verification and strict RC

Run focused tests first.

Then run:

```powershell
python -m compileall -q scripts
python -m unittest discover -s tests -q
python scripts/run_quality_checks.py
python scripts/package_smoke_test.py
python scripts/check_release_readiness.py --strict
git diff --check
python scripts/run_release_candidate_checks.py
```

Required results:

```text
Quality approved
Package smoke approved
Strict compatibility ready
Whitespace clean
Release Candidate approved
```

If the RC fails:

- preserve the exact output;
- fix the current v0.3.2 blocker only;
- do not disable or skip the check;
- rerun the smallest affected tests, then the full RC.

---

# 12. Gate 7 — Version, Changelog, PR, and CI

Only after the physical evidence and strict RC pass:

## 12.1 Version

Update all authoritative sources:

```text
0.3.1 → 0.3.2
```

Run the version-source check.

## 12.2 Changelog

Add formal English and Chinese sections:

```text
0.3.2
```

Describe only:

- Windows 11 physical stabilization;
- evidence closure;
- any minimal directly discovered defect fix;
- strict RC completion.

Do not list branch protection as an application feature.

It may be mentioned under repository/release process when appropriate.

## 12.3 PR

Branch:

```text
release/v0.3.2-win11-stabilization
```

Title:

```text
[v0.3.2] Complete Windows 11 release stabilization
```

PR body must include:

```text
single outcome
physical environment
confirmed evidence
newly completed evidence
remaining approved limitations
strict RC result
resource/security impact
main-protection status
rollback
No v0.4.0 work was included
```

Push the branch and open the PR.

Wait for the remote Windows Quality workflow.

Do not merge based only on local tests.

---

# 13. Gate 8 — Merge, main convergence, and tag

Before merge:

```text
[ ] PR contains only v0.3.2
[ ] remote Quality succeeded
[ ] strict RC succeeded locally
[ ] physical records are complete
[ ] matrix is truthful
[ ] main protection is enabled or limitation is explicitly recorded
[ ] expected PR head SHA is known
```

Merge with:

```text
squash
```

Use expected-head-SHA protection when the available merge tool supports it.

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

Then tag the exact verified main commit:

```text
v0.3.2
```

Verify:

```powershell
git merge-base --is-ancestor v0.3.2 origin/main
```

Delete the release branch only after:

```text
remote tag exists
post-merge checks pass
post-release smoke passes
```

---

# 14. Gate 9 — Post-release physical smoke

On the tagged build verify:

```text
launch
five status rows
Reset Credit date
compact/hover
right-click menu
hide/show
exit
relaunch
single-process behavior
no persistent CMD
```

Record only regressions that actually occur.

If a serious startup, privacy, data-loss, or lifecycle defect appears:

- do not start v0.4.0;
- prepare a focused `v0.3.3` patch Goal.

Do not silently add the fix to an unrelated future feature.

---

# 15. Checkpoint and interruption protocol

Update:

```text
Goal/EXECUTION_STATE.md
```

after each major checkpoint.

Required fields:

```markdown
# Execution State

- Target version: 0.3.2
- Branch:
- Base main SHA:
- Current head SHA:
- Last pushed SHA:
- Current gate:
- Confirmed physical evidence:
- Remaining physical evidence:
- Strict blocker output:
- Main-protection status:
- Completed tests:
- Remaining:
- Next exact action:
- Known limitations:
- Last updated:
```

When interrupted:

1. finish only the current safe Git/filesystem operation;
2. do not leave a merge/rebase/cherry-pick active;
3. run the smallest relevant tests;
4. commit verified work only;
5. push the checkpoint branch;
6. update `EXECUTION_STATE.md`;
7. resume from `Next exact action`.

---

# 16. Required final report

Report:

```text
remote base SHA
active branch
v0.3.2 PR URL
merge SHA
v0.3.2 tag SHA
Windows edition/build
monitor/DPI/taskbar environment
previously confirmed physical evidence
newly completed physical evidence
strict readiness blocker list before
strict readiness result after
Quality result
RC result
main protection enabled: Yes/No
required status-check context
GitHub plan limitation, if any
compensating controls, if any
post-release smoke
resource impact
security/privacy impact
rollback
```

Explicitly state:

```text
No v0.4.0 work was included in the v0.3.2 branch, PR, merge commit, or tag.
```

---

# 17. Definition of Done

```text
[ ] local v0.3.2 work was preserved and reconciled
[ ] ACTIVE_GOAL metadata reflects v0.3.2
[ ] ACTIVE_VERSION_BRIEF reflects v0.3.2
[ ] existing physical checkpoint is recorded
[ ] exact strict blockers were inventoried
[ ] compact shrink and hover expansion were physically verified
[ ] context menu was physically verified
[ ] single-monitor result is physically verified or honestly unresolved
[ ] bottom taskbar is physically verified
[ ] alternate taskbar edges are not falsely claimed
[ ] mixed-DPI limitation is honest
[ ] clean-machine limitation is honest
[ ] compatibility matrix links dated evidence
[ ] strict readiness passes truthfully
[ ] full Quality passes
[ ] strict Release Candidate passes
[ ] main protection is configured when available
[ ] required Quality check is enforced when available
[ ] no destructive branch-protection test was performed
[ ] branch-protection plan limitation is documented when applicable
[ ] version sources read 0.3.2
[ ] bilingual Changelog contains 0.3.2
[ ] focused PR is opened
[ ] remote CI passes
[ ] PR is squash-merged
[ ] main is retested
[ ] v0.3.2 tag points to verified main
[ ] release branch is deleted
[ ] tagged physical smoke passes
[ ] no new feature was added
[ ] no v0.4.0 work was included
```

After every v0.3.2 box is complete:

1. close and delete the v0.3.2 release branch;
2. verify `v0.3.2` is reachable from `origin/main`;
3. ensure the working tree is clean;
4. create a new v0.4.0 Brief;
5. create the v0.4.0 branch directly from the latest `origin/main`;
6. begin the separate v0.4.0 scope below.

No v0.4.0 production file may be modified before the v0.3.2 transition gate is complete.


---

# 18. Transition Gate — v0.3.2 to v0.4.0

Before opening or coding v0.4.0:

```text
[ ] v0.3.2 PR is merged
[ ] origin/main contains the v0.3.2 merge commit
[ ] v0.3.2 tag exists remotely
[ ] v0.3.2 tag is an ancestor of origin/main
[ ] post-release v0.3.2 smoke passed
[ ] v0.3.2 release branch is deleted
[ ] no v0.3.2 Git operation remains
[ ] working tree is clean
[ ] main protection is enabled or its plan limitation is recorded
[ ] ACTIVE_VERSION_BRIEF is replaced, not appended
```

Required commands:

```powershell
git fetch origin --prune --tags
git switch main
git pull --ff-only origin main
git merge-base --is-ancestor v0.3.2 origin/main
git status
git switch -c release/v0.4.0-unified-window-scale origin/main
```

Never create v0.4.0 from the v0.3.2 branch.

---

# 19. v0.4.0 — Unified Window Scale

## 19.1 One-sentence outcome

```text
Replace separate font-size and free-form window-size controls with one proportional window-size slider that scales the overlay and its typography together.
```

This is a user-visible minor feature and must remain separate from v0.3.2 stabilization.

## 19.2 User intent

The settings dialog should have exactly two `Scale` widgets:

```text
透明度
窗口大小
```

“Exactly two sliders” does not mean the entire settings dialog has only two controls. The following ordinary settings may remain:

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

## 19.3 Controls to remove from the UI

Remove:

```text
字体大小 slider
窗口宽度 input
窗口高度 input
窗口大小 − button
窗口大小 + button
等比例缩放 checkbox
```

Do not leave hidden, disabled, or advanced duplicates of those controls in the normal dialog.

## 19.4 New window-size control

Add one slider:

```text
Label: 窗口大小
Presentation: percentage
Recommended initial range: 80%–200%
Recommended step: 5%
Default: 100%
```

The final minimum and maximum must be validated against the real five-row layout.

If 80% clips any required content, increase the minimum to the smallest physically and automatically verified safe percentage. Do not keep an unsafe range merely for symmetry.

The slider should display an understandable percentage rather than an internal decimal where practical.

## 19.5 Fixed aspect ratio

Use one canonical base geometry.

Initial canonical values:

```text
BASE_WINDOW_WIDTH = 330
BASE_WINDOW_HEIGHT = 138
BASE_TEXT_FONT_SIZE = 10
BASE_FACE_FONT_SIZE = 28
```

Canonical ratio:

```text
330 : 138
```

All normal expanded sizes must be derived from one scale value:

```text
width = round(BASE_WINDOW_WIDTH × scale)
height = round(BASE_WINDOW_HEIGHT × scale)
```

The user may no longer independently change width and height.

The window ratio must not drift after repeated Apply, Save, restart, Restore Defaults, or migration.

## 19.6 Adaptive typography and visual metrics

At minimum, derive the status font from the same scale:

```text
font_size = clamp(round(BASE_TEXT_FONT_SIZE × scale), supported_min, supported_max)
```

Also review whether the following should scale through one pure metrics function:

```text
paw/face font
horizontal padding
vertical padding
row wraplength
compact size inputs
```

Professional UI requirement:

- scale all metrics necessary to keep the composition visually balanced;
- do not scale arbitrary unrelated settings;
- do not introduce blurry bitmap resizing;
- keep text rendered through Tk fonts;
- preserve five-row readability.

Create one pure calculation boundary, for example:

```text
scripts/api/window_scale_api.py
```

Suggested output:

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

The exact API may differ, but scale calculations must not be duplicated across the dialog and main window.

## 19.7 Configuration compatibility

Current settings contain independent fields such as:

```text
font_size
window_width
window_height
scale_mode
```

Do not delete compatibility support abruptly.

Recommended compatible model:

```text
new canonical field: window_scale_percent
legacy/derived fields: font_size, window_width, window_height, scale_mode
```

Rules:

1. `window_scale_percent` becomes the source of truth for new saves.
2. Width, height, and font size may remain persisted as derived compatibility fields.
3. `scale_mode` should normalize to proportional behavior.
4. An older released application should still receive usable derived width/height/font values if it reads the file.
5. Current/future malformed-schema write protection must remain intact.
6. Do not bump the schema merely because it is convenient; decide through an explicit compatibility review.
7. If a schema bump is truly necessary, document migration, downgrade, and protected-write behavior.

## 19.8 Legacy-settings migration

For a valid existing configuration without `window_scale_percent`:

- infer one deterministic scale from the existing window geometry;
- clamp to the supported range;
- quantize to the slider step;
- derive the new fixed-ratio width, height, and font metrics;
- preserve position, alpha, colors, refresh interval, topmost, locked, and compact settings.

Recommended inference basis:

```text
old visual area relative to canonical visual area
```

For example:

```text
raw_scale = sqrt(
    (old_width × old_height) /
    (BASE_WINDOW_WIDTH × BASE_WINDOW_HEIGHT)
)
```

Then clamp and quantize.

This avoids letting one unusually wide or tall legacy dimension dominate the migration.

The chosen algorithm must be pure, documented, and covered by tests.

Migration must not overwrite an unsupported or malformed protected source automatically.

## 19.9 Transactional settings behavior

Preserve:

```text
Apply previews without closing
Save persists and closes
Close discards unsaved draft
Restore Defaults resets to 100% and other defaults
```

Required behavior:

- moving the window-size slider changes only the draft until Apply or Save;
- Apply updates size and typography together;
- Save persists the unified scale;
- Close without Apply/Save does not mutate runtime or disk;
- repeated Apply at the same percentage is idempotent;
- Restore Defaults resets the size slider to 100%;
- protected-configuration behavior remains unchanged.

## 19.10 Main-window behavior

On Apply/load:

```text
one scale value
→ one pure WindowMetrics result
→ geometry, status font, face font, padding, and wraplength update together
```

Requirements:

- no intermediate mismatched font/window state visible where practical;
- position recovery uses the derived width and height;
- Hide/Show restores the derived expanded size;
- Compact/Expanded restores the correct scale;
- monitor reconnect logic uses derived expanded geometry;
- no new worker, thread, subprocess, IPC, network, polling, or disk-write frequency.

## 19.11 Frontend/UI design

Target settings-dialog hierarchy:

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

- no empty gaps left by removed controls;
- align both sliders;
- preserve clear label-to-control relationships;
- percentage is understandable;
- settings dialog remains compact;
- no additional popup or advanced panel;
- no decorative animation;
- keyboard and first-click behavior remain usable.

## 19.12 Allowed production scope

Preferred files:

```text
scripts/ui/settings_dialog.py
scripts/ui/main_window.py
scripts/api/config_api.py
scripts/api/window_scale_api.py
scripts/api/settings_session_api.py if required
scripts/api/window_recovery_api.py only if derived geometry requires it
scripts/api/compact_state_api.py or display_mode_api only if directly required
```

Allowed tests:

```text
window scale calculations
legacy migration
config normalization
settings transaction
dialog exact-control contract
main-window metrics application
compact/expanded restoration
position recovery
restart persistence
```

Allowed docs:

```text
CHANGELOG.md
CHANGELOG.zh-CN.md
configuration documentation pair
API/architecture documentation pair
product overview/settings documentation pair
Windows 11 physical record
```

## 19.13 Explicit exclusions

Do not include:

```text
new color system
theme presets
font-family selection
manual window resize handles
manual width/height entry
manual font-size entry
manual aspect-ratio toggle
new refresh behavior
new quota behavior
new menu items
installer work
automatic updater
Windows 10 support
telemetry
external services
unrelated cleanup
```

## 19.14 Obsolete APIs and cleanup

Existing helpers such as free-size or resize-session APIs may become unused.

Rules:

- do not delete them merely because the UI no longer calls them;
- first prove no runtime, test, or compatibility caller remains;
- remove dead APIs in v0.4.0 only when removal is small and directly required to prevent two competing size models;
- otherwise schedule a separate v0.4.1 cleanup patch;
- do not keep two active sources of truth.

## 19.15 Required automated tests

Pure scale tests:

```text
100% produces canonical metrics
minimum produces readable bounded metrics
maximum stays within supported dimensions
percentage quantization is deterministic
aspect ratio remains fixed within rounding tolerance
font size changes monotonically
repeated derivation is stable
```

Migration tests:

```text
legacy default maps to 100%
legacy arbitrary dimensions map deterministically
legacy extreme dimensions clamp safely
legacy font field does not remain an independent source of truth
missing scale field migrates
valid new scale reloads identically
malformed scale falls back safely
unsupported future schema remains protected
```

Settings-dialog tests:

```text
exactly two Tk Scale widgets exist
labels are 透明度 and 窗口大小
字体大小 control is absent
width/height inputs are absent
minus/plus size buttons are absent
等比例缩放 is absent
position and refresh entries remain
Apply/Save/Close/Restore Defaults semantics remain
```

Main-window tests:

```text
geometry and fonts update from one metrics result
five rows remain stable
Hide/Show preserves scale
Compact/Expand preserves expanded scale
position recovery uses derived size
restart loads the same scale
```

## 19.16 Windows 11 physical validation

Test at:

```text
minimum supported percentage
100%
a middle-large value
maximum supported percentage
```

At each size verify:

```text
fixed visual aspect ratio
five rows visible
Reset Credit date visible
no text clipping
paw/text balance
right-click menu placement
drag/lock behavior
Hide/Show
Compact/Hover
settings dialog usability
restart persistence
```

Use both current 96-DPI monitors where practical.

Do not claim mixed-DPI physical certification without such hardware.

## 19.17 Resource and privacy review

Expected impact:

```text
no new network
no new IPC
no new worker
no new polling
no new paid service
no telemetry
bounded constant-time metric calculation
small additional configuration field only
```

The feature must not increase Codex usage or trigger refreshes while the slider moves.

## 19.18 Version and release

Branch:

```text
release/v0.4.0-unified-window-scale
```

PR title:

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

PR must state:

```text
one unified scale feature
removed controls
fixed aspect-ratio contract
migration behavior
configuration compatibility
automated tests
Windows 11 physical evidence
resource impact
rollback
No v0.4.1 or later work was included
```

Run full Quality and all release gates applicable to the released support contract.

## 19.19 Rollback

Rollback is the single squashed v0.4.0 merge commit.

Before merge, verify that a v0.3.2 binary/config can still read the derived compatibility fields produced by v0.4.0.

If downgrade compatibility cannot be preserved safely:

- document it before merge;
- do not hide the limitation;
- require explicit Product and Security/Resource approval.

---

# 20. v0.4.0 Definition of Done

```text
[ ] v0.3.2 was fully released before v0.4.0 began
[ ] v0.4.0 branch started directly from latest main
[ ] ACTIVE_VERSION_BRIEF describes only v0.4.0
[ ] Product Decision is GO
[ ] settings dialog contains exactly two Scale widgets
[ ] transparency slider remains
[ ] unified window-size slider exists
[ ] font-size slider is removed
[ ] width/height inputs are removed
[ ] minus/plus size buttons are removed
[ ] proportional checkbox is removed
[ ] aspect ratio is fixed
[ ] font size derives from window scale
[ ] required visual metrics derive from one pure API
[ ] five rows remain readable throughout the supported range
[ ] legacy settings migrate deterministically
[ ] protected configuration remains protected
[ ] Apply/Save/Close/Restore Defaults semantics pass
[ ] Hide/Show and Compact/Expand preserve scale
[ ] no new resource or privacy boundary is introduced
[ ] focused automated tests pass
[ ] full Quality passes
[ ] Windows 11 physical size matrix passes
[ ] version sources read 0.4.0
[ ] bilingual Changelog contains 0.4.0
[ ] focused PR passes remote CI
[ ] PR is squash-merged
[ ] main is retested
[ ] v0.4.0 tag points to verified main
[ ] release branch is deleted
[ ] post-release smoke passes
[ ] no later-version work was included
```

Then stop.

Do not begin v0.4.1 or v0.5.0 under this Goal.
