# ACTIVE VERSION BRIEF — v0.2.1 Minimal Context Menu

## Identity

- Version: `0.2.1`
- Branch: `release/v0.2.1-minimal-context-menu`
- Base: `main` at `477acc20e635e76a98fb3e4579bd796b264bd12e`
- PR: to be created as `[v0.2.1] Simplify the context menu`
- Tag: `v0.2.1`

## Product

- One-sentence outcome: The overlay context menu contains only five ordinary window controls.
- Target user: A Windows 11 Codex user who keeps the passive status overlay running.
- User problem: Maintenance actions make the menu longer and easier to misuse.
- Why now: It is the first independently releasable cleanup in the authorized train.
- Success criteria: Exactly Settings, Topmost, Lock Position, Hide Window, and Exit remain; automatic refresh and internal recovery continue unchanged.
- Explicit non-goals: Reset Credit formatting, schema protection, status rows, controllers, Windows support scope, CI, document governance, new features.
- Misuse risk: Reduced because refresh, diagnostics, and restore actions are removed from the ordinary menu.
- User-resource impact: No new worker, IPC, network, disk write, refresh, animation, or dependency.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Visual/UI/UX | Yes | PASS |
| Frontend | Yes | PASS |
| Backend | Limited | PASS |
| QA/Release | Yes | PASS |
| Security/Resource | Yes | PASS |

## Visual/UI/UX

- Applicable: Yes
- Affected component: Right-click popup menu only.
- Before: Eight actions, including refresh, diagnostics, and backup recovery.
- After: Five approved controls with one separator before Hide/Exit.
- Labels: `显示设置`, `置顶`, `锁定位置`, `隐藏窗口`, `退出`.
- Layout/spacing: Preserve existing compact Windows 11 styling and work-area placement.
- Interaction states: First click invokes once; Escape and FocusOut close; grab is released.
- Accessibility: Preserve text labels and keyboard Escape behavior; do not add icon-only controls.
- Misclick prevention: Remove maintenance actions; keep Exit separated.
- Windows 11 physical check: Open at a screen edge and invoke each safe control path.
- Decision: PASS

## Frontend

- Applicable: Yes
- Components: `scripts/ui/context_menu.py` and menu tests.
- State transitions: Open → invoke/escape/focus-out → close and release grab.
- Event flow: Approved item delegates once to the existing owner method.
- Thread boundary: Tk main thread only; unchanged.
- Layout impact: Popup becomes shorter; placement algorithm remains unchanged.
- Tests: Exact labels/count, removed labels absent, dispatch once, Escape, FocusOut, grab release.
- Physical verification: Windows 11 first-click and edge placement smoke.
- Decision: PASS

## Backend

- Applicable: Limited
- Data/API contract: No provider, Activity, Quota, configuration, or persistence change.
- Ownership: Existing automatic refresh and internal backup remain owned by current modules.
- Concurrency: No worker or scheduler change.
- Persistence: Removing a UI restore entry does not remove `.bak` creation or validation.
- Failure modes: Menu command exceptions remain sanitized and close the popup.
- Network/IPC: No change.
- CPU/memory/disk: No increase.
- Tests: Existing refresh scheduler/controller tests remain green.
- Rollback: Revert the single release commit.
- Decision: PASS

## QA / Release

- Positive cases: All five approved items exist and dispatch to the correct method.
- Negative cases: Three removed labels/widgets/bindings are absent.
- Regression cases: First click, Escape, FocusOut, grab release, edge placement, automatic refresh unchanged.
- Resource checks: No new imports, threads, timers, subprocesses, writes, or network paths.
- Security/privacy checks: No new data access; diagnostics remain internal but lose the ordinary UI entry.
- Windows 11 checks: Bottom-taskbar popup opens, stays in work area, and closes after first invocation.
- Quality commands: Focused menu tests, full `run_quality_checks.py`, `git diff --check`.
- Rollback: Revert v0.2.1 and retag only through a patch release if already published.
- Decision: PASS

## Security / Resource

- New network or IPC: No.
- New worker or subprocess: No.
- Refresh frequency increase: No.
- Additional disk writes/data retention/log/cache: No.
- Additional UI attention or misclick cost: Reduced.
- Possible user cost or additional Codex quota use: No; manual refresh is removed.
- Decision: PASS

## Scope Lock

- Allowed production files: `scripts/ui/context_menu.py`; only remove dead menu-only callers after proving no other callers.
- Allowed tests: context-menu and direct regression tests only.
- Allowed release files: canonical version sources, English/Chinese Changelog, directly affected menu documentation.
- Forbidden: all v0.2.2+ implementation, unrelated refactors, formatting churn, dependency changes, new settings, new buttons.
- Release shape: one focused implementation commit plus required release metadata; one PR; one tag.
- No work from the next version will be included.
