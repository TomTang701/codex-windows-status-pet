# Lean-Core Renewal Baseline — 2026-07-11

This dated audit is evidence, not an active development specification. The authoritative direction is `Goal/ACTIVE_GOAL.md`; the active release contract is `Goal/ACTIVE_VERSION_BRIEF.md`.

## Current repository truth

| Fact | Observed state |
|---|---|
| Local branch | `main` |
| Local HEAD | `02ab1f60a1e8a6b91e4b212bb47773e88d068c84` |
| `origin/main` | `02ab1f60a1e8a6b91e4b212bb47773e88d068c84` |
| Application version | `0.4.0` |
| Latest merged PR | `#12` — `[v0.4.0] Unify window and typography scaling`, merge `02ab1f60a1e8a6b91e4b212bb47773e88d068c84` |
| Latest release | `v0.4.0`, published 2026-07-11 07:26 UTC |
| Latest tag target | annotated `v0.4.0` peels to `02ab1f60a1e8a6b91e4b212bb47773e88d068c84` |
| Latest CI | Windows Quality run `29144378871`, success on merged `main` |
| GitHub owner/authentication | remote owner and active `gh` account both `TomTang701` |
| Commit identity | `Zixuan Tang <143047729+TomTang701@users.noreply.github.com>` |

The pre-renewal active state was false in several places: `ACTIVE_GOAL.md` still described the v0.3.2/v0.4.0 release sequence; `ACTIVE_VERSION_BRIEF.md` still treated v0.4.0 as active; `EXECUTION_STATE.md` said PR #12 did not exist; the Roadmap called v0.4.0 a candidate and reported only 88 tests; README documented removed font/width/height controls and incorrectly claimed the repository launcher automatically installed sign-in startup.

## Counting method

- **Runtime production Python:** `scripts/codex_status_pet.py` plus every `*.py` under `scripts/api/` and `scripts/ui/`, including package `__init__.py` files. Release/quality/probe scripts are reported separately.
- **Tooling Python:** top-level `scripts/*.py` excluding `codex_status_pet.py`.
- **Tests:** every top-level `tests/*.py` file.
- **Active normative documents:** the three active Goal files plus canonical manifest entries with `class: normative` and `status: active`. Descriptive Roadmap/README files and translations are excluded so the same metric can be recomputed later.
- **LOC:** physical lines returned by PowerShell `Get-Content`; blank and comment lines are included. Generated build output and `__pycache__` are excluded.
- **API modules:** every `scripts/api/*.py`, including `__init__.py`; controller modules are filenames containing `controller`.
- **Runtime consumer count:** direct Python imports from non-test files, normalized across both `api.<module>` and `scripts.api.<module>` import forms. Relative imports within `scripts/api` were then inspected directly.

## Measured baseline

| Metric | Baseline |
|---|---:|
| Runtime production Python files | 39 |
| Runtime production Python LOC | 2,702 |
| Tooling Python files | 13 |
| Tooling Python LOC | 756 |
| All `scripts` Python files / LOC | 52 / 3,458 |
| Test files | 35 |
| Test LOC | 1,850 |
| Active normative files | 10 |
| Active normative LOC | 2,675 |
| API modules | 32 |
| Controller modules | 5 |
| Runtime dependencies | 2 (`Pillow>=10.0`, `pystray>=0.19`) |
| Routine Quality | 6.372 seconds; failed only because the supplied replacement Goal still existed under an unapproved extra filename |
| Core/UI tests during Quality | 124 / 17 passed |
| Package smoke | passed in 0.106 seconds |
| Strict RC | 6.147 seconds; failed because it correctly included the same failed Quality governance check; compatibility and package checks passed |

The failed baseline gate is not a product regression. `scripts/check_doc_governance.py` permits only `ACTIVE_GOAL.md`, `ACTIVE_VERSION_BRIEF.md`, `EXECUTION_STATE.md`, and `README.md` under `Goal/`. The supplied file explicitly directs replacement of `ACTIVE_GOAL.md`; leaving both files present is therefore the root cause.

## Consumer and duplication findings

- `window_size_api.py` and `resize_session_api.py` have no runtime consumer and are documented as historical compatibility utilities. Each is imported only by its implementation-detail test.
- `models_api.py` has no runtime or test consumer.
- `quota_provider_api.py` is a 14-line pass-through wrapper around `quota_parse_api.parse_quota_payload` with one runtime consumer.
- `window_lifecycle_controller_api.py` is a 14-line lifecycle owner used by the main window; its responsibility is real, but its boundary is small enough to re-evaluate after behavior-level shutdown tests exist.
- `scripts/codex_status_pet.py` is a compatibility launcher facade. It has user-facing launcher value and injectable test compatibility, so it cannot be removed from import counts alone.
- `StatusPresentationController` owns normal row presentation, but tray and transport failures bypass it through two legacy `self.text.config(text=..., fg=...)` calls in `scripts/ui/main_window.py`.
- `ApplicationController` legitimately composes refresh generation and single-flight scheduling. Its two subordinate modules are consumed through relative imports, so a naive absolute-import scan incorrectly reports zero consumers.
- Strict RC invokes routine Quality, while local release procedures often run Quality separately immediately beforehand. This is a duplicate execution candidate, not proof that either gate can be removed without Phase 2 classification.
- Active Goal, Brief, Execution State, and Roadmap duplicated completed-release facts and volatile SHAs. This duplication already produced contradictory release state.

## Candidate classification

| Candidate | Class | Evidence and protected scenario |
|---|---|---|
| Local Codex transport, config persistence, parsing/normalization, display/Win32, Tk adapters, refresh coordination | `KEEP` | These isolate real IO, platform, persistence, state, or UI boundaries required by the protected core. |
| `scripts/codex_status_pet.py` facade | `KEEP` | Root launcher and historical injectable import surface remain active; compatibility must be evaluated at contract level before any later simplification. |
| `status_presentation_controller_api.py` | `KEEP` | It is the intended authoritative row mapping boundary needed to close Phase 1 error-path bugs. |
| `window_size_api.py` | `DELETE` candidate for Phase 3 | No runtime consumer; only historical free/proportional behavior and its own test remain. Deletion waits for rollback/config evidence. |
| `resize_session_api.py` | `DELETE` candidate for Phase 3 | No runtime consumer; only historical +/- behavior and its own test remain. |
| `models_api.py` | `DELETE` candidate for Phase 3 | No runtime or test consumer and no current typed-domain flow uses it. |
| `quota_provider_api.py` | `MERGE` candidate for Phase 3 | One-method pass-through wrapper with one consumer; parsing/privacy behavior must remain protected. |
| `window_lifecycle_controller_api.py` | `DEFER` | Responsibility is real, but evidence is insufficient to decide whether merging improves ownership without weakening shutdown tests. |
| Normal and emergency status rendering | `MERGE` in Phase 1 | Two legacy Label-style error paths bypass the authoritative five-row presentation route. |
| Quality plus strict RC repeated execution | `DEFER` to Phase 2 | Duplicate work is observable, but every gate must first be classified as automated, automatable, physical-only, obsolete, or duplicate. |
| Completed release prose in active documents | `DELETE` in Phase 0 | Git tags, releases, changelog, and archived evidence already own history; active documents should own current direction only. |

No production component is deleted in Phase 0. These labels are evidence-backed candidates, not implementation authorization.

## Ranked backlog

1. **Correctness — Phase 1 / v0.4.1:** reproduce the reported final-row clipping with actual/requested Tk geometry and add a content-fit regression contract before the minimum root-cause fix.
2. **Correctness — Phase 1 / v0.4.1:** reproduce tray and quota transport errors through production integration paths; remove invalid `StatusRows.config(text=..., fg=...)` calls and use the authoritative presentation boundary.
3. **Missing automated contracts — Phase 2 / v0.4.2:** classify every Quality, RC, compatibility, and host check; convert machine-observable facts and consolidate duplicates.
   - Include RC subprocess decoding: a UTF-8 `git diff --check` diagnostic containing non-ASCII text currently crashes the GBK parent reader instead of returning the underlying whitespace failure cleanly.
4. **Removable complexity — Phase 3 / v0.5.0:** evaluate and, where protected behavior permits, delete `models_api`, `window_size_api`, and `resize_session_api`; merge the quota provider pass-through.
5. **Duplicate state/boundaries — Phase 3 or conditional Phase 4:** remeasure lifecycle, refresh, and presentation ownership after Phase 1 and Phase 3. Mark Phase 4 not needed if one authoritative route already remains.
6. **Productization — Phase 5 decision only:** evaluate installation value after the lean core and supported-host automation are proven; do not implement automatically.

## Phase 1 activation

Phase 1 / v0.4.1 Correctness Stabilization is the only active implementation scope after this Phase 0 reconciliation. Phase 0 changes documentation and evidence only; no runtime behavior, application version, dependency, release, or remote state changes here.

## Phase 0 measured result

| Metric | Before | After Phase 0 |
|---|---:|---:|
| Runtime production Python files | 39 | 39 |
| Runtime production Python LOC | 2,702 | 2,702 |
| API / controller modules | 32 / 5 | 32 / 5 |
| Active normative files | 10 | 10 |
| Active normative LOC | 2,675 | 1,012 |
| Runtime dependencies | 2 | 2 |
| Routine Quality duration | 6.372 s (governance failed) | 5.441 s (approved) |

Phase 0 removed 1,663 lines from the active normative set by replacing completed release workflow/state with the 652-line cross-release renewal Goal, a 110-line v0.4.1 brief, and a 17-line execution checkpoint. Full historical text remains recoverable from Git; the archive contains a short non-normative pointer instead of duplicating 2,366 stale lines.

Final Phase 0 evidence: document manifest/governance/links/parity passed; version sources remained 0.4.0; 124 core and 17 UI tests passed; package smoke passed; strict compatibility readiness and strict RC passed. No runtime, test, dependency, launcher, GitHub, tag, release, or remote branch state changed.
