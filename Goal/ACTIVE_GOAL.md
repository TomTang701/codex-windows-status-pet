# ACTIVE PROGRAM GOAL — v0.5.5 Release Completion → v0.6.0 Delivery

> **Status:** FINAL RECONCILIATION / NO ACTIVE IMPLEMENTATION SCOPE
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Current reconciliation branch:** `docs/v0.6.0-release-state`
> **Latest released product:** `v0.6.0` at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`
> **Previous released baseline:** `v0.5.5` at `4662414c16e6892d02634dd5139b3ca93f281d37`
> **Historical v0.5.4:** closed investigation / no product release
> **Program final target:** released and reconciled `v0.6.0`
> **Execution model:** one active implementation version at a time; multiple sequential phases are allowed inside this Program Goal
> **STOP:** after this documentation-only reconciliation is merged and main is verified

## 0. Program mission

Execute one continuous program from the v0.5.5 mixed-DPI startup-position candidate through the v0.6.0 product release. Do not stop after v0.5.5 or ask Tom to reactivate v0.6.0: this Program Goal is the approval for the sequential transition.

```text
v0.5.5 candidate → PR → exact-head CI → merge → merged-main RC → tag / Release → v0.5.5 reconciliation
→ HARD VERSION GATE → automatic v0.6.0 activation → brainstorming / design / Design Verification
→ writing-plans → TDD → implementation → verification → PR / exact-head CI / merge / RC / tag / Release
→ final reconciliation → STOP
```

## 1. Program governance

The governing rule is: **one active implementation version at a time; multiple sequential version phases are allowed inside one approved Program Goal.**

- While v0.5.5 is active, v0.6.0 implementation is forbidden.
- After v0.5.5 is released and reconciled, v0.5.5 implementation is closed and v0.6.0 becomes the only active implementation version.
- After v0.6.0 is released and reconciled, current implementation scope is none and the Program stops.
- Do not mix v0.6.0 code into the v0.5.5 PR.
- Follow repository `AGENTS.md`, the approved Superpowers workflows, scope control, identity checks, secret protection, and verification rules.

## 2. Protected product core

Preserve the following throughout the Program unless direct evidence proves an exact required change:

- quota data from the local official Codex app-server JSON-RPC path; activity from approved local session metadata; no tokens, telemetry, third-party provider, backend, hosted service, or Codex-core modification;
- Windows 11 x64, one companion instance, main-thread Tk ownership, bounded single-flight refresh, safe idempotent shutdown, and no persistent console;
- transactional Settings Apply / Save / Close / Restore Defaults, proportional 80–200% `window_scale_percent`, configuration compatibility, Hide/Show, Compact/Expand, drag/lock, topmost, legal multi-monitor recovery, tray reachability, and restart persistence;
- exactly five stable status-row identities: `activity`, `progress`, `primary_5h`, `weekly`, `reset_credit`;
- Shell identity: visible overlay and tray, `WS_EX_TOOLWINDOW=true`, `WS_EX_APPWINDOW=false`, and no ordinary taskbar / Alt+Tab / Win+Tab application identity.

# PROGRAM PHASE A — v0.5.5 RELEASE COMPLETION

## 3. Phase A mission and candidate

Complete v0.5.5 mixed-DPI startup position recovery. The established root cause is that a withdrawn bootstrap HWND reports primary 120 DPI before saved-position recovery, inflates containment metrics for a legal 96-DPI secondary edge coordinate, and clamps it before target DPI becomes correct. The minimum correction uses geometry authority appropriate to the monitor targeted by the saved position. Do not redesign the production correction unless new evidence contradicts it.

Before remote writes inspect branch, exact HEAD, recent commits, remote, `gh auth status`, and Git author identity. If HEAD moved beyond the named candidate, inspect every added commit and verify it belongs to Phase A.

## 4. Candidate verification and CI-admission rule

Run fresh candidate gates:

```powershell
python scripts/run_quality_checks.py
python scripts/package_smoke_test.py
python scripts/run_release_candidate_checks.py
git diff main...HEAD --check
git diff --stat main...HEAD
```

Confirm mixed-DPI RED/GREEN evidence, legal secondary right/bottom/bottom-right preservation, invalid/off-screen recovery, Shell identity coverage, coherent 0.5.5 version surfaces, no v0.6.0 code, no unrelated changes/debug artifacts/secrets.

Physical-topology-dependent tests must explicitly skip, with a reason that names the unavailable required topology, when the host lacks the required 125% primary / 100% right-side-secondary topology. They must not convert a real logic assertion failure into a skip, and synthetic tests must not be presented as physical mixed-DPI evidence. Tom's real host remains the physical RED/GREEN authority.

If any CI or release gate fails, use `systematic-debugging`: read exact logs, identify one root cause, add a focused RED when behavior changes, implement the minimum correction, verify locally, push, and require CI for the new exact PR head SHA.

## 5. PR, merge, and v0.5.5 release

Create or use one PR with base `main`, head `fix/v0.5.5-mixed-dpi-startup-position`, title `fix: preserve mixed dpi startup positions`, and a body stating summary, root cause, minimum correction, RED/GREEN evidence, Quality/package-smoke/RC, and explicit exclusion of v0.6.0.

Require repository required Windows CI for the exact PR head SHA. Review the complete PR diff for requirements, mixed-DPI correctness, off-screen recovery, Shell identity, version consistency, complexity, temporary files, secrets, and credentials. Only then squash merge according to repository practice.

On merged main, run fresh formal RC. Only when merged-main RC passes with zero blockers and version 0.5.5, create and verify tag `v0.5.5` and its GitHub Release targeting the verified merged-main commit. Release notes must describe the 120-DPI bootstrap containment cause, target-monitor geometry correction, retained invalid recovery, and edge/restart coverage. Never release v0.5.4.

## 6. v0.5.5 reconciliation

After the release exists, reconcile `Goal/ACTIVE_GOAL.md`, `Goal/ACTIVE_VERSION_BRIEF.md`, `Goal/EXECUTION_STATE.md`, roadmap pair, compatibility matrix pair, and changelog pair truthfully:

```text
v0.5.3 = previous released baseline
v0.5.4 = historical closed investigation / no product release
v0.5.5 = released mixed-DPI startup position recovery patch
```

Record PR number, exact-head CI SHA/result, merged-main SHA, merged-main RC, tag, and GitHub Release target. Run documentation/state consistency and Quality checks.

# HARD VERSION GATE — v0.5.5 → v0.6.0

## 7. Automatic transition requirements

Do not begin v0.6.0 implementation until all are true:

```text
v0.5.5 PR merged
v0.5.5 exact-head required CI passed
v0.5.5 merged-main RC passed
v0.5.5 tag exists and target verified
v0.5.5 GitHub Release exists and target verified
v0.5.5 authoritative state reconciled
v0.5.5 closure checks passed
```

When true, close Phase A, set released baseline to v0.5.5, automatically activate Phase B/v0.6.0, and create a dedicated v0.6.0 feature branch from verified reconciled main. Do not stop or ask Tom for another Goal.

# PROGRAM PHASE B — v0.6.0 DESIGN

## 8. Product outcome

Deliver **v0.6.0 5H Battery Indicator and Layout Tightening** inside the existing five-row presentation architecture. `primary_5h` remains one row; no sixth row. The work changes presentation only, never official quota authority or quota meaning.

## 9. Mandatory brainstorming and evidence-based design

Before production implementation invoke `brainstorming` and inspect real `primary_5h` data semantics, parser/quota state, StatusRows, presentation controller, color/unavailable behavior, WindowMetrics, pack/layout behavior, all scale steps, content-fit tests, settings/compact lifecycle, mixed-DPI geometry, and v0.4.1/v0.5.1/v0.5.3/v0.5.5 lessons.

Compare at least these approaches:

1. inline text battery using glyphs and percentage: smallest surface but must measure Windows glyph widths;
2. composed battery row/widget: clearer visual proportion but larger DPI/layout surface;
3. Unicode/emoji battery plus percentage: compact but low granularity and glyph-variation risk.

Choose the smallest Windows 11/DPI-stable approach that clearly communicates the official 5H proportion without a row-rendering rewrite.

Define and record the data contract:

```text
raw official value → normalized bounded presentation value → battery fill meaning → percentage text meaning
```

Battery fill and text must have the same used/remaining semantics. Do not infer semantics from variable names, invent values, invert one representation, or render a fake full/empty state when quota is unavailable.

Measure current padding, face/text gap, wrap length, requested/actual geometry, and all five rows before any layout change. Layout tightening must remove measured unnecessary whitespace while preserving every row, readability, reset-credit content, battery content, edge safety, and canonical scale behavior from 80 through 200 in 5% steps.

## 10. Design Verification

Write a concrete v0.6.0 design under the repository design path. It must define selected architecture, exact existing classes/functions in the data flow, semantics, unavailable/error/last-good behavior, exact measured layout adjustment, and regression boundaries for five rows, all scale steps, DPI 96/120, target-window coherence, lifecycle, mixed-DPI persistence, and Shell identity.

Answer: **Does the design improve 5H presentation and tighten layout with the smallest architecture-compatible change without weakening truthful quota semantics or geometry contracts?** If not, revise and do not implement. If yes, mark Design Verification PASSED and invoke `writing-plans`.

# PROGRAM PHASE C — v0.6.0 IMPLEMENTATION

## 11. Planning, TDD, and minimum implementation

After Design Verification passes, write an executable plan with exact paths/interfaces and RED for battery semantics/rendering plus content-fit/layout. Use `test-driven-development` for semantics, transformations, state transitions, deterministic helpers, and reproducible content-fit behavior. Do not create production behavior before an appropriate RED.

Prefer existing owners, confirmed from source, including `scripts/ui/status_rows.py`, `scripts/ui/main_window.py`, `scripts/api/status_presentation_controller_api.py`, `scripts/api/window_scale_api.py`, and current quota presentation/parsing owners. Do not create a manager, renderer framework, animation service, dependency, worker, or sixth row. Update Tk only on changed presentation data; no animation or unbounded canvas items.

## 12. Required v0.6.0 regression matrix

Verify valid/lower/upper/middle 5H quota, unavailable, malformed, and transport-error last-good behavior; agreement of battery/text semantics; exactly five identities; every 5% scale from 80–200 with five rows/battery/reset-credit visible and unclipped; DPI 96/120 and existing broader DPI regression; startup/drag/tray exit/restart/mixed-DPI edge persistence/Hide/Show/Compact/Expand/settings Apply-Save-Close-Defaults/lock/topmost; and `WS_EX_TOOLWINDOW=true` / `WS_EX_APPWINDOW=false`.

Run focused tests, relevant UI/presentation/geometry/persistence/DPI/Shell tests, Quality, package smoke, formal RC, diff review, unrelated-change check, and secret scan. Candidate state requires all gates passing and zero release blockers.

# PROGRAM PHASE D — v0.6.0 RELEASE

## 13. Version, PR, merge, and release

Only after Phase C is green, establish coherent 0.6.0 version/changelog surfaces truthfully and create a v0.6.0 PR from its dedicated branch. Require exact-head CI and final review. Merge only with candidate verification, exact-head CI, and review passing. On merged main run fresh formal RC, then create and verify `v0.6.0` tag and GitHub Release targeting the verified merged-main commit.

Release notes must describe the battery indicator, what its proportion means, layout tightening, five-row preservation, truthful quota authority, mixed-DPI persistence preservation, and Shell identity preservation without claiming unsupported physical environments.

# PROGRAM PHASE E — FINAL STATE RECONCILIATION

## 14. Final repository truth and verification-before-completion

After v0.6.0 Release exists, reconcile authoritative state so it says:

```text
latest released product version = v0.6.0
v0.5.4 = historical closed investigation / no release
v0.5.5 = released mixed-DPI startup position recovery patch
v0.6.0 = released 5H Battery Indicator and Layout Tightening
current implementation scope = none
```

Record actual v0.5.5/v0.6.0 PRs, exact-head CI SHAs/results, merged-main SHAs, merged-main RCs, tags, and Release targets. Remove stale claims that v0.5.5 is active or v0.6.0 is blocked/not started. Run final Quality and state/document verification. Before completion prove v0.5.5/v0.6.0 releases and target identities, APP_VERSION 0.6.0, five stable rows, mixed-DPI regression, all-scale fit, Shell identity, reconciled state, clean worktree, complete history/diff review, and no secrets.

## 15. Human Interaction Admission Gate and STOP

Ask Tom only when one exact material fact cannot be determined from source, tests, safe automation, Tk/Win32/process/filesystem/app-local inspection, or current physical-host evidence. First record the required fact, methods, observed evidence, insufficiency, blocker, and exact question in `EXECUTION_STATE.md`; then ask one concise factual question. After an answer resume this same Program.

STOP only after v0.5.5 is released/reconciled, the Hard Version Gate passes, v0.6.0 is designed, implemented, verified, merged, released, reconciled, and final evidence is reported. Do not begin v0.6.1, installer, auto-start, auto-update, or unrelated work.

## 16. Recorded release facts (2026-07-12)

- v0.5.5 PR [#24](https://github.com/TomTang701/codex-windows-status-pet/pull/24) merged; exact-head Windows CI #83 passed at `94df8ed`; merged main and tag/Release target `4662414c16e6892d02634dd5139b3ca93f281d37`.
- v0.6.0 design, written plan, focused RED/GREEN cycles, all-scale/DPI fit coverage, lifecycle regressions, Quality, package smoke, and formal RC completed before PR.
- v0.6.0 PR [#25](https://github.com/TomTang701/codex-windows-status-pet/pull/25) merged at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`; exact-head Windows CI passed at `8670b0f82ef272a24df870d4756aea71c2182b80`.
- Merged-main formal RC passed at `b7915d86a5007d76a62a7870ad248b9230fe0f4a`; [`v0.6.0`](https://github.com/TomTang701/codex-windows-status-pet/releases/tag/v0.6.0) tag and GitHub Release target that same commit.
- v0.5.4 remains historical `CLOSED INVESTIGATION / NO PRODUCT RELEASE`; no v0.5.4 tag or Release exists.
- Remaining work is documentation-state reconciliation only. No production runtime code change is authorized or required.
