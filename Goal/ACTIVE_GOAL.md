# ACTIVE PROGRAM GOAL — v0.6.1 Quota Identity → v0.6.3 Presentation Controls

> **Status:** APPROVED PROGRAM / SEQUENTIAL v0.6.n DELIVERY
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released baseline:** `v0.6.0`
> **Final target:** released and reconciled `v0.6.3`
> **Execution model:** one active implementation version at a time
> **Automatic sequence:** `v0.6.1 → v0.6.2 → v0.6.3`
> **STOP:** only after v0.6.3 release, reconciliation, and final verification
> **Default battery source:** weekly
> **Battery fallback:** forbidden

---

## 0. Program mission

Start from the verified released `v0.6.0` baseline and deliver:

```text
v0.6.1 Quota Window Identity Correctness
→ HARD VERSION GATE
→ v0.6.2 Quota Row Visibility and Dynamic Distribution
→ HARD VERSION GATE
→ v0.6.3 Battery Quota Source Selector
→ final reconciliation
→ STOP
```

The current product may no longer safely assume:

```text
primary == 5h
secondary == weekly
```

The observed product symptom is that the official Codex UI can show a weekly remaining value while the companion shows the same value on the `5h` line and leaves the weekly line unavailable.

Treat that as evidence of a possible identity-classification defect, not proof of the exact payload shape.

The final product must:

```text
truthfully identify 5h and weekly quota windows
show missing 5h as `5h -- / --` when its row is enabled
allow 5h / weekly / reset-credit text rows to be independently shown or hidden
keep activity and progress always visible
equally distribute all currently visible text rows vertically
keep font size and window size unchanged when rows are hidden
allow the battery to select exactly one source: 5h or weekly
default the battery source to weekly
never automatically fallback to another battery source
```

Do not require all work to fit into one release.

Do not STOP after v0.6.1 or v0.6.2.

---

# 1. Program governance

## 1.1 One active version at a time

```text
while v0.6.1 is active:
    v0.6.2 and v0.6.3 production implementation are forbidden

after v0.6.1 release + reconciliation + Hard Gate:
    automatically activate v0.6.2

after v0.6.2 release + reconciliation + Hard Gate:
    automatically activate v0.6.3

after v0.6.3 release + reconciliation + final verification:
    STOP
```

Do not ask Tom for another Goal between versions.

Do not create a generic quota framework, settings framework, layout engine, or renderer framework.

Use the smallest complete change inside the existing architecture.

## 1.2 Required workflow

Follow repository and Tom global instructions.

Use only the approved Superpowers workflows by default:

```text
using-superpowers
brainstorming
writing-plans
systematic-debugging
test-driven-development
verification-before-completion
```

For each active version:

```text
inspect repository truth
→ update active state
→ required design work
→ Design Verification
→ writing-plans
→ TDD
→ focused verification
→ broad regression
→ Quality
→ package smoke
→ formal RC
→ complete diff review
→ unrelated-change check
→ secret/credential check
→ PR
→ exact-head CI
→ merge
→ merged-main RC
→ tag / GitHub Release
→ reconciliation
→ Hard Version Gate
```

Completion claims require fresh evidence.

## 1.3 GitHub execution authorization

The existing standing authorization for routine remote actions inside an approved active Goal remains applicable.

Within this Program scope Codex may:

```text
create the active-version branch
push focused commits
create the scoped PR
monitor required CI
push focused correction commits after verified gate failures
require CI for every new exact PR head SHA
squash merge according to repository practice after all gates pass
verify merged main
create and verify the scoped version tag
create and verify the GitHub Release
clean up the completed release branch according to repository practice
```

Before remote writes verify:

```text
git remote -v
gh auth status
git config user.name
git config user.email
git status
current branch
exact HEAD
```

Expected Tom-owned GitHub account:

```text
tomtang701
```

Do not infer GitHub identity from Windows username `tangz`.

Not authorized:

```text
force push
history rewrite
repository permissions or visibility changes
secret changes
credential changes
unrelated destructive Git operations
unrelated repository work
```

---

# 2. Protected product core

Preserve:

```text
local-only Windows companion
quota authority = official local Codex app-server JSON-RPC
activity authority = approved local Codex session metadata
no auth.json reading
no access-token reading or persistence
no third-party quota endpoint
no telemetry
no backend
no hosted service
no Codex core modification
Windows 11 x64 baseline
one companion instance
Tk main-thread ownership
bounded/single-flight refresh
safe idempotent shutdown
no persistent console in normal launch
```

Preserve exactly five persistent row identities:

```text
activity
progress
primary_5h
weekly
reset_credit
```

Rows may be hidden from layout in v0.6.2+, but their persistent identity and owners remain.

Preserve:

```text
Settings Apply / Save / Close / Restore Defaults semantics
configuration validation and recovery
window_scale_percent compatibility
80–200% scale in 5% steps
Hide / Show
Compact / Expand
drag / lock
topmost
multi-monitor recovery
mixed-DPI startup position persistence
tray reachability
restart persistence
```

Preserve Shell identity:

```text
WS_EX_TOOLWINDOW = true
WS_EX_APPWINDOW = false
no ordinary taskbar app button
no ordinary Alt+Tab identity
no ordinary Win+Tab identity
```

Preserve the v0.6.0 battery visual contract:

```text
2 columns × 5 rows
10 persistent cells
remaining-percentage semantics
bottom-up fill
left-to-right inside a partially filled pair
0% → 0 lit
remaining > 0 → ceil(remaining / 10)
segments 1–2 red
segments 3–4 orange
segments 5–6 yellow
segments 7–8 light green / yellow-green
segments 9–10 stronger green
top two cells visibly greener than segments 7–8
compact mode = complete same ten-cell battery only
```

Do not add a sixth row.

---

# PROGRAM PHASE A — v0.6.1 QUOTA WINDOW IDENTITY CORRECTNESS

## 3. Product outcome

Deliver **v0.6.1 Quota Window Identity Correctness**.

The product must truthfully distinguish:

```text
real 5-hour quota window
real weekly quota window
missing/unavailable 5-hour window
missing/unavailable weekly window
```

Do not continue using fixed positional business meaning unless official evidence proves it.

Forbidden speculative fixes:

```text
swap primary and secondary
rename primary to weekly
assume the first window is weekly
assume the only window is weekly
hardcode the current screenshot value
```

Use `systematic-debugging`.

## 4. Root-cause investigation

Before production changes:

1. Read the complete current quota transport, parser, quota-state, presentation, and battery path.
2. Review the v0.6.0 quota/battery changes and tests.
3. Use the approved official local `codex app-server --stdio` JSON-RPC path.
4. Inspect only safe quota fields needed to identify window identity and presentation.
5. Do not read `auth.json`.
6. Do not read or persist access tokens.
7. Do not propagate credential-like or arbitrary unknown fields.
8. Record exact safe quota-window identity evidence in a dated investigation/test record.
9. Compare live evidence with the current parser assumptions.
10. State one explicit root-cause hypothesis.
11. Create a focused RED that fails because current classification is wrong or insufficient.
12. Only then implement the minimum correction.

The investigation must answer:

```text
Which official safe field(s) distinguish a 5-hour window?
Which official safe field(s) distinguish a weekly window?
How is an absent window represented?
Can only one window be present?
Can both be present?
Does current normalization discard identity metadata needed for truthful classification?
```

Prefer explicit official window metadata such as a proven duration/window identity field.

Do not use dictionary order, array order, `primary`, or `secondary` naming as business identity unless exact current official evidence proves that contract.

If the parser currently drops a required safe identity field, normalize only the minimum approved metadata needed.

Do not expose raw quota payloads outside the approved parsing/presentation boundary.

If no safe official metadata can distinguish the windows, do not invent a classifier. Use the Human Interaction Admission Gate only after source, tests, safe live app-server evidence, and simple automation are insufficient.

## 5. Truthful presentation contract

### 5h row

Real 5h exists:

```text
5h <remaining>% / <reset time>
```

5h row enabled and no real 5h exists:

```text
5h -- / --
```

Never place a weekly percentage or weekly reset time on this row.

### Weekly row

Real weekly exists:

```text
周 <remaining>% / <existing truthful reset formatting>
```

No real weekly exists:

```text
周 -- / --
```

Never place a 5h value on this row.

### Battery during v0.6.1

Tom approved weekly as the v0.6.n default battery source.

Before the selector exists, v0.6.1 may move the battery's fixed source to the truthfully classified weekly window.

Required behavior:

```text
battery source = classified weekly window
weekly available → battery uses weekly remaining
weekly unavailable → battery unavailable
5h availability does not change battery source
```

This is the approved default source, not fallback.

Do not automatically switch to 5h.

Do not add the selector until v0.6.3.

Expanded and compact battery modes must still consume one authoritative battery presentation result.

## 6. Design and TDD requirements

Write a concrete v0.6.1 design under the repository design/spec path.

Inspect and name the exact current owners, including as applicable:

```text
scripts/api/quota_parse_api.py
scripts/api/status_snapshot_api.py
scripts/api/status_presentation_controller_api.py
scripts/ui/battery_view.py
scripts/ui/main_window.py
current quota transport owner
current quota-state / last-good owner
```

The design must define:

```text
safe official identity metadata
normalized parser contract
5h classification
weekly classification
absence semantics
malformed semantics
last-good/stale semantics
battery source semantics
unknown/credential field drop boundary
```

Design Verification question:

> Does the design identify 5h and weekly windows from safe official evidence, keep missing 5h visibly `5h -- / --`, preserve weekly data on the weekly row, and prevent the battery from consuming a misidentified window without broad quota architecture changes?

If yes, mark Design Verification PASSED and invoke `writing-plans`.

Use TDD for parser normalization, classification, transformations, presentation mapping, and battery-source semantics.

Minimum RED/GREEN matrix:

```text
5h + weekly both present
5h absent + weekly present
5h present + weekly absent
both absent
one unknown/unclassifiable window
malformed identity metadata
malformed usedPercent
out-of-range usedPercent
unknown fields dropped
credential-like fields never propagated
5h row never receives weekly value
weekly row never receives 5h value
5h missing → `5h -- / --`
weekly missing → truthful unavailable weekly line
battery uses classified weekly window
weekly unavailable → battery unavailable
5h available while weekly unavailable → no fallback
stale/last-good text and battery remain coherent
```

Do not rewrite quota acquisition.

## 7. v0.6.1 verification and release

Run fresh relevant:

```text
parser/classification tests
status snapshot tests
battery presentation tests
transport tests
quota-state / last-good tests
UI battery integration
all-scale/DPI content fit
settings regression
mixed-DPI regression
Shell identity regression
Quality
package smoke
formal RC
git diff --check
complete diff review
unrelated-change check
secret/credential scan
```

Only after candidate gates are green:

```text
establish coherent 0.6.1 version/changelog
create scoped v0.6.1 PR
require exact-head Windows CI
review complete PR diff
squash merge
verify merged main
run fresh merged-main formal RC
create and verify v0.6.1 tag
create and verify GitHub Release
reconcile authoritative state
```

Release notes must describe truthful quota-window identity, missing 5h presentation, weekly battery default direction, no automatic source fallback, and continued local official app-server authority.

Do not claim a temporary OpenAI policy is permanent.

## 8. HARD VERSION GATE — v0.6.1 → v0.6.2

All must be true:

```text
v0.6.1 PR merged
exact-head required CI passed
merged-main RC passed
v0.6.1 tag target verified
v0.6.1 GitHub Release target verified
quota identity evidence recorded
authoritative state reconciled
closure checks passed
```

Then automatically:

```text
close v0.6.1
set released baseline to v0.6.1
activate v0.6.2
create dedicated v0.6.2 branch from verified reconciled main
continue without asking Tom
```

---

# PROGRAM PHASE B — v0.6.2 QUOTA ROW VISIBILITY AND DYNAMIC DISTRIBUTION

## 9. Product outcome

Deliver **v0.6.2 Quota Row Visibility and Dynamic Distribution**.

Add three independent checkboxes to the current settings dialog:

```text
☑ 显示 5小时
☑ 显示每周
☑ 显示重置次数
```

Defaults:

```text
show 5h = true
show weekly = true
show reset credit = true
```

Always-visible rows:

```text
activity
progress
```

Optional mapping:

```text
显示 5小时    → primary_5h
显示每周      → weekly
显示重置次数  → reset_credit
```

Checkboxes control layout visibility only.

They do not change quota acquisition, quota identity, or battery source.

## 10. Hidden versus unavailable

Enabled + official data unavailable:

```text
显示 5小时 = checked
real 5h absent
→ visible `5h -- / --`
```

Disabled:

```text
显示 5小时 = unchecked
→ primary_5h Label hidden from layout
```

Do not use blank text as the visibility mechanism.

Do not confuse hidden rows with unavailable data.

## 11. Dynamic equal vertical distribution

Exactly five persistent row identities and persistent Label owners remain.

Do not delete rows from `ROW_IDS`.

Visibility only changes which persistent Labels participate in layout.

Canonical order remains:

```text
activity
progress
primary_5h
weekly
reset_credit
```

All currently visible rows must be vertically distributed equally across the same existing left text region.

Required invariants:

```text
font size unchanged because rows are hidden
font still follows window_scale_percent
window width unchanged because rows are hidden
window height unchanged because rows are hidden
battery size unchanged because rows are hidden
battery position/layout region unchanged because rows are hidden
```

All five visible:

```text
1 activity
2 progress
3 primary_5h
4 weekly
5 reset_credit
```

Weekly hidden:

```text
1 activity
2 progress
3 primary_5h
5 reset_credit
```

Those four visible rows equally share the same text-region height.

All three optional rows hidden:

```text
activity
progress
```

Those two rows equally share the same text-region height.

Do not leave fixed blank slots.

Do not resize the window.

Do not enlarge the font.

Do not move text into the battery region.

## 12. Settings persistence

Recommended keys:

```text
show_primary_5h
show_weekly
show_reset_credit
```

Defaults:

```text
true
true
true
```

If current repository naming evidence supports a more consistent exact name, use that consistent name and document it in the design.

Existing valid settings without these keys must load successfully with all three defaults `true`.

Malformed booleans must use existing normalization/warning behavior.

Do not break v0.6.0/v0.6.1 settings compatibility.

Do not bump schema merely because additive defaulted booleans exist if current normalization safely supports them. If a schema bump is truly required, record the exact reason before changing it.

Transactional behavior:

### Apply

```text
draft checkbox values
→ Apply
→ runtime row visibility and distribution update immediately
→ not yet required to persist
```

### Save

```text
apply
→ persist normalized values
→ update opening snapshot
→ existing close behavior
```

### Close after unsaved Apply

```text
return runtime visibility/distribution to opening snapshot
```

### Restore Defaults

```text
show_primary_5h = true
show_weekly = true
show_reset_credit = true
```

Preserve current config write protection and Restore Defaults authorization semantics.

## 13. Implementation boundary

Prefer existing owners after source confirmation:

```text
scripts/api/config_api.py
scripts/api/settings_session_api.py
scripts/ui/settings_dialog.py
scripts/ui/status_rows.py
scripts/ui/main_window.py
relevant config/settings/status rows/UI/content-fit tests
```

`StatusRows` should remain the owner of its internal Label layout.

Compare:

```text
A. repack persistent Labels with equal expansion
B. grid persistent Labels with uniform weights
C. manual absolute placement
```

Recommended selection rule:

> Choose the smallest Tk implementation that proves equal vertical distribution across all eight optional-row visibility combinations and all supported scale/DPI cases while preserving row identity and event behavior.

Manual absolute placement is disfavored unless measured evidence proves pack/grid cannot satisfy the contract.

Do not move row-visibility layout ownership into quota parsing.

Do not manually calculate row y coordinates in `main_window.py` if `StatusRows` can own the behavior.

## 14. Required TDD and layout verification

Verify all 8 checkbox combinations:

```text
5h weekly reset
1   1      1
1   1      0
1   0      1
1   0      0
0   1      1
0   1      0
0   0      1
0   0      0
```

For every combination verify:

```text
all five persistent identities still exist
activity visible
progress visible
enabled optional rows visible
disabled optional rows absent from layout
visible order canonical
visible rows equally distributed within reasonable Tk integer-pixel tolerance
font size unchanged for the current scale
window geometry unchanged for the current scale/DPI
battery geometry unchanged for the current scale/DPI
no overlap
no clipping
visible row surfaces retain right-click/hover/drag interaction
```

Also verify hidden/unavailable distinction.

Scale matrix:

```text
80, 85, 90, 95, 100,
105, 110, 115, 120, 125,
130, 135, 140, 145, 150,
155, 160, 165, 170, 175,
180, 185, 190, 195, 200
```

DPI:

```text
96
120
```

Required development-only automated layout verification:

Prefer extending existing content-fit/Tk probe infrastructure.

A failure must identify, as applicable:

```text
visibility combination
scale
DPI
mode
requested text-region geometry
actual text-region geometry
visible row positions/heights
battery requested/actual geometry
window geometry
violated fit or equal-distribution condition
```

If current tests already provide equivalent matrix coverage and diagnostics, extend them instead of creating a duplicate framework.

No production dependency.

## 15. v0.6.2 verification and release

Run:

```text
config normalization
settings-session transaction tests
settings-dialog tests
StatusRows visibility/distribution tests
all 8 visibility combinations
all 25 scales
DPI 96/120
expanded content fit
compact battery regression
interaction/lifecycle
mixed-DPI
Shell identity
Quality
package smoke
formal RC
git diff --check
complete diff review
unrelated-change check
secret scan
```

Then:

```text
coherent 0.6.2 version/changelog
scoped PR
exact-head CI
final diff review
squash merge
verify merged main
fresh merged-main RC
v0.6.2 tag
v0.6.2 GitHub Release
verify targets
state reconciliation
```

## 16. HARD VERSION GATE — v0.6.2 → v0.6.3

All must be true:

```text
v0.6.2 PR merged
exact-head required CI passed
merged-main RC passed
v0.6.2 tag target verified
v0.6.2 GitHub Release target verified
all 8 visibility combinations passed
all-scale/DPI layout verification passed
settings transactional regression passed
authoritative state reconciled
closure checks passed
```

Then automatically activate v0.6.3 from verified reconciled main without asking Tom.

---

# PROGRAM PHASE C — v0.6.3 BATTERY QUOTA SOURCE SELECTOR

## 17. Product outcome

Deliver **v0.6.3 Battery Quota Source Selector**.

Add a two-state slider-like control to the existing settings dialog:

```text
电池显示内容

5小时   [ two-state slider ]   每周
```

Exactly two legal states:

```text
primary_5h
weekly
```

Visual meaning:

```text
left  = 5小时
right = 每周
```

Default:

```text
weekly
```

Tom explicitly selected weekly as the default for all normalized settings when the field is absent.

Do not preserve 5h as a migration default merely because v0.6.0 historically displayed a 5h battery.

## 18. Selector independence

The selector controls battery source only.

The three row-visibility checkboxes control text layout only.

They are independent.

Examples:

```text
show_primary_5h = false
battery source = primary_5h

→ 5h text row hidden
→ battery still uses real 5h quota or unavailable
```

```text
show_weekly = false
battery source = weekly

→ weekly text row hidden
→ battery still uses real weekly quota or unavailable
```

Do not auto-change battery source because its corresponding text row is hidden.

Do not auto-show a row because the battery selects that source.

## 19. Strict source semantics

Selected `primary_5h`:

```text
real 5h available → battery displays real 5h remaining
5h absent/unavailable/malformed → battery unavailable
```

Never consume weekly data.

Selected `weekly`:

```text
real weekly available → battery displays real weekly remaining
weekly absent/unavailable/malformed → battery unavailable
```

Never consume 5h data.

Forbidden:

```text
automatic fallback
automatic selector movement
automatic persisted source change
```

The user-selected source is authoritative for battery source selection.

Official quota data is authoritative for the selected source value.

## 20. Settings contract

Recommended key:

```text
battery_quota_source
```

Allowed values:

```text
primary_5h
weekly
```

Default:

```text
weekly
```

Missing field:

```text
weekly
```

Malformed/unknown/null/numeric/unsupported value:

```text
normalize to weekly
use existing repository-appropriate warning behavior
```

Preserve atomic persistence, backup, restore, write protection, and compatibility.

Do not add a second settings file.

## 21. Two-state slider UI

The intended interaction is slider-like and analogous to on/off.

Compare the smallest Tk approaches:

```text
A. tk.Scale with discrete 0/1 values and explicit left/right labels
B. focused two-state custom Frame using existing Tk controls
C. two radio buttons styled as a binary choice
```

Prefer a discrete `tk.Scale` or the smallest reliable existing-Tk composition that clearly reads as left/right two-state control.

No continuous intermediate state.

No third state.

Do not use a dropdown unless exact Tk/platform evidence proves the required two-state control unreliable.

Do not add a third-party UI dependency.

Do not add a generic settings-control framework.

Measure the settings dialog requested geometry after adding the controls.

Preserve:

```text
resizable(False, False)
topmost dialog behavior
popup placement within work area
owner visibility recovery
```

## 22. Shared battery presentation authority

Required data flow:

```text
truthfully classified 5h/weekly windows
+ battery_quota_source
→ selected real quota window or unavailable
→ one pure battery presentation transformation
→ one battery presentation result
→ expanded BatteryView
→ compact BatteryView
```

Do not independently compute battery semantics in:

```text
settings_dialog
main_window
BatteryView
compact path
expanded path
```

Preserve current battery transformation:

```text
remaining
→ 0% special case
→ ceil(remaining / 10)
→ ten ordered segment states
→ fixed position colors
```

No battery animation.

## 23. Transactional settings behavior

### Apply

```text
change selector
→ Apply
→ runtime battery source updates immediately
→ battery updates to selected source
→ no restart
→ no Save required for runtime preview
→ row visibility unchanged
```

### Save

Persist the normalized source through the normal settings path.

### Close after unsaved Apply

```text
battery source and presentation return to opening snapshot
```

### Restore Defaults

```text
battery_quota_source = weekly
show_primary_5h = true
show_weekly = true
show_reset_credit = true
```

Preserve current Apply/Save/Close/Restore Defaults semantics.

## 24. Required TDD

Pure/state tests:

```text
default source = weekly
missing source field → weekly
valid primary_5h retained
valid weekly retained
invalid source → weekly + appropriate warning
selected primary_5h selects only real 5h
selected weekly selects only real weekly
selected primary_5h + missing 5h → unavailable
selected weekly + missing weekly → unavailable
5h selection never consumes weekly
weekly selection never consumes 5h
no fallback after source becomes unavailable
selected source recovers when its real quota returns
battery text/segment semantics still agree
expanded and compact consume the same battery result
```

Settings/UI tests:

```text
two legal selector positions only
left maps to primary_5h
right maps to weekly
default position = weekly
Apply updates runtime source
Save persists source
Close reverts applied-unsaved source
Restore Defaults sets weekly
row checkboxes remain independent
selector change does not alter row visibility
row visibility does not alter selector
```

Required value scenarios:

```text
5h 80%, weekly 55%, selector 5h
→ battery 80%
→ 8 lit segments

5h 80%, weekly 55%, selector weekly
→ battery 55%
→ 6 lit segments

5h absent, weekly 55%, selector 5h
→ battery unavailable

5h absent, weekly 55%, selector weekly
→ battery 55%
→ 6 lit segments

5h 9%, weekly 100%, selector 5h
→ 1 lit segment

5h 0%, weekly 100%, selector 5h
→ 0 lit segments
```

Run both battery sources against all 8 row-visibility combinations to prove independence.

## 25. Full v0.6.3 regression

Verify:

```text
8 row-visibility combinations
2 battery sources
selected source available
selected source unavailable
selected source malformed
selected source restored
stale/last-good behavior
25 scale steps from 80–200
DPI 96
DPI 120
expanded
compact
Apply
Save
Close
Restore Defaults
startup
restart persistence
drag
lock
Hide/Show
Compact/Expand
topmost
tray exit
mixed-DPI edge persistence
Shell identity
```

Expanded:

```text
visible rows equally distributed
five persistent identities remain
hidden selected text row does not affect battery source
10 battery cells visible
no clipping
no overlap
truthful 5h when visible
truthful weekly when visible
truthful reset-credit when visible
```

Compact:

```text
battery only
complete 2×5 / 10-cell identity
all cells visible
selected-source semantics preserved
no fallback
no clipping
```

## 26. v0.6.3 verification and release

Run:

```text
battery source tests
quota identity regression
status snapshot regression
config normalization
settings-session transaction tests
settings dialog tests
StatusRows visibility/distribution
8 visibility combinations × 2 sources
all-scale/DPI content fit
expanded/compact battery integration
lifecycle regression
mixed-DPI regression
Shell identity regression
Quality
package smoke
formal RC
git diff --check
complete diff review
unrelated-change check
secret/credential scan
```

Only with zero release blockers:

```text
coherent 0.6.3 version/changelog
scoped PR
exact-head Windows CI
complete PR review
squash merge
verify merged main
fresh merged-main RC
v0.6.3 tag
GitHub Release
verify tag/Release target
```

---

# PROGRAM PHASE D — FINAL STATE RECONCILIATION

## 27. Final repository truth

After v0.6.3 Release exists, reconcile the actual authoritative documents, including:

```text
Goal/ACTIVE_GOAL.md
Goal/ACTIVE_VERSION_BRIEF.md
Goal/EXECUTION_STATE.md
docs/product/ROADMAP.md
docs/product/ROADMAP.zh-CN.md
CHANGELOG.md
CHANGELOG.zh-CN.md
repository version/plugin manifests
current compatibility/state matrices when present
```

Final truth:

```text
latest released product = v0.6.3
v0.6.0 = released segmented battery baseline
v0.6.1 = released quota-window identity correctness
v0.6.2 = released quota-row visibility and dynamic distribution
v0.6.3 = released battery quota source selector
current implementation scope = none
Program Goal = COMPLETE / STOPPED
```

Record actual PR numbers, exact-head CI SHAs/results, merged-main SHAs, merged-main RCs, tag targets, and GitHub Release targets for v0.6.1, v0.6.2, and v0.6.3.

Do not leave stale active-version claims.

## 28. Final verification-before-completion

Fresh evidence must prove:

```text
required version surfaces = 0.6.3
v0.6.1/v0.6.2/v0.6.3 tags and Release targets verified
quota identity regression passes
5h missing + row enabled = `5h -- / --`
weekly real value remains on weekly row
weekly value cannot populate 5h row
5h value cannot populate weekly row
three visibility settings default true
all 8 visibility combinations pass
visible rows equally distribute vertically
five persistent row identities remain
font size does not change because rows are hidden
window dimensions do not change because rows are hidden
battery geometry does not change because rows are hidden
battery source default = weekly
battery source values = primary_5h / weekly only
no automatic fallback
battery source independent from row visibility
expanded battery retains 10 cells
compact battery retains 10 cells
all 25 scale steps pass
DPI 96/120 pass
Settings Apply/Save/Close/Restore Defaults pass
mixed-DPI regression passes
Shell identity passes
Quality passes
package smoke passes
formal RC passes
clean worktree
complete history/diff review
no unrelated changes
no secrets or credentials
```

## 29. Human Interaction Admission Gate

Ask Tom only when one exact material fact blocks the active version and cannot be determined from:

```text
source
repository docs
tests
safe automation
official local app-server inspection
Tk
Win32
process/filesystem inspection
app-local evidence
exact-build evidence
existing physical-host evidence
```

Before asking:

```text
record required fact in Goal/EXECUTION_STATE.md
record methods
record observed evidence
record why evidence is insufficient
record why the fact blocks the active version
ask one concise factual question
```

Do not ask Tom to repeat machine-readable facts.

Tom has already approved:

```text
enabled 5h + official 5h missing → `5h -- / --`
disabled optional row → hide its persistent Label from layout
visible rows equally distribute vertically
activity and progress always visible
with all optional rows hidden, activity and progress equally split the text region
font size unchanged because rows are hidden
font still follows window scale
window dimensions unchanged because rows are hidden
battery geometry unchanged because rows are hidden
three optional visibility settings default true
battery selector is left/right two-state
left = 5小时 / primary_5h
right = 每周 / weekly
battery source default = weekly
battery source independent from row visibility
automatic battery-source fallback forbidden
```

Do not re-ask these questions.

## 30. Scope exclusions

Do not add:

```text
battery animation
charging animation
battery history
quota graphs
usage forecasting
automatic battery source fallback
automatic selector movement
third battery source
combined 5h+weekly battery
user-configurable battery colors
user-configurable segment count
row reordering
row drag-and-drop
activity/progress visibility toggles
window auto-resize based on visible rows
font auto-resize based on visible rows
generic settings framework
generic layout engine
generic renderer framework
third-party UI dependency
telemetry
backend
hosted service
token reader
auth.json reader
Codex core changes
installer
auto-start
auto-update
v0.7.0 work
```

Record unrelated findings when important.

Do not expand active scope unless an unrelated issue blocks correctness, security, or required verification.

---

# 31. Immediate activation sequence

The previous `v0.5.5 → v0.6.0` Program is complete and stopped.

Activate this Program as the new current Goal.

Execute:

```text
1. Verify current main and released v0.6.0 truth.
2. Verify remote, GitHub auth, Git author, branch, exact HEAD, and worktree state.
3. Replace Goal/ACTIVE_GOAL.md with the COMPLETE contents of this Program Goal.
4. Update Goal/ACTIVE_VERSION_BRIEF.md to active v0.6.1.
5. Update Goal/EXECUTION_STATE.md:
   Program Goal = ACTIVE
   released baseline = v0.6.0
   active implementation version = v0.6.1
   active phase = quota-window identity root-cause investigation
   blocker = none unless evidence proves one
   next exact action = inspect safe official local app-server quota-window identity metadata and reproduce the current classification mismatch
6. Update roadmap authority only to record approved v0.6.n direction; do not describe unreleased work as released.
7. Create the dedicated v0.6.1 branch from verified reconciled main.
8. Invoke systematic-debugging for the quota identity mismatch.
9. Establish safe live payload evidence.
10. Establish the focused v0.6.1 RED.
11. Complete v0.6.1 design and Design Verification.
12. Invoke writing-plans.
13. Complete v0.6.1 through release and reconciliation.
14. Pass the v0.6.1 Hard Version Gate.
15. Automatically activate and complete v0.6.2.
16. Pass the v0.6.2 Hard Version Gate.
17. Automatically activate and complete v0.6.3.
18. Complete final reconciliation.
19. Run verification-before-completion.
20. STOP only when v0.6.3 is released and reconciled with all final evidence green.
```

Do not only change the Active Goal header.

The entire approved Program Goal must become the active Goal authority.

Do not resume the completed old Program.

---

# 32. Final completion report

Report:

## Conclusion

Whether v0.6.3 is released and reconciled.

## Released outcomes

```text
v0.6.1 quota-window identity correctness
v0.6.2 quota-row visibility and equal dynamic vertical distribution
v0.6.3 two-state battery quota-source selector
```

## Product behavior

State actual verified behavior for:

```text
5h missing + row enabled
weekly row identity
three visibility checkboxes
hidden-row dynamic distribution
two always-visible row distribution
battery selector left/right mapping
weekly default
no fallback
row visibility/source independence
```

## Verification evidence

Report actual:

```text
focused RED/GREEN
8 visibility combinations
2 battery sources
25 scale steps
DPI 96/120
Settings lifecycle
mixed-DPI
Shell identity
Quality
package smoke
formal RC
exact-head CI
merged-main RC
tag/Release targets
```

## Remaining limitations or risks

Only actual remaining limitations.

Do not begin another version.
