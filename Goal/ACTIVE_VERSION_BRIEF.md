# ACTIVE VERSION BRIEF — v0.3.1 Controller Refactor

## Identity

- Version: `0.3.1`
- Branch: `release/v0.3.1-controller-refactor`
- Base: `main` at `a6a7177424850ba9afcf14a3d55fa48622ac2aa5`
- PR: `[v0.3.1] Extract main-window controllers`
- Tag: `v0.3.1`

## Product

- One-sentence outcome: The Tk main window delegates coordination state to four pure controllers without changing user-visible behavior.
- User problem: `Pet` directly owns refresh generations/scheduling, compact presentation decisions, persistence compatibility, and idempotent close state, making regression isolation difficult.
- Success criteria: Controller contracts own those decisions; `Pet` remains the Tk adapter/composer; all existing UI text, timing, settings, menu, tray, geometry, five-row, and failure behavior remain equivalent.
- Explicit non-goals: New UI or behavior, physical evidence closure, status content/layout, configuration schema, refresh interval semantics, dependencies.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Backend/Architecture | Yes | PASS |
| Frontend adapter | Yes | PASS |
| QA/Release | Yes | PASS |
| Visual/UI/UX | Behavior verification only | PASS |
| Security/Resource | Yes | PASS |

## Controller Boundaries

- `ApplicationController`: Activity/Quota generations, quota single-flight schedule, interval, finish, current-generation checks, shutdown.
- `StatusPresentationController`: pure status snapshot plus compact-state decision/force-expanded behavior.
- `SettingsPersistenceController`: path, source compatibility metadata, load, atomic save, explicit reset authorization, backup restore.
- `WindowLifecycleController`: one-way idempotent close transition.
- Controllers import no Tk or pystray and expose no UI widgets.
- Existing lower-level APIs remain independently testable and are not deleted.
- Decision: PASS

## Behavior Equivalence

- Activity remains 1-second scheduled and independent from quota.
- Quota retains configured 1–10 second single-flight delay and stale-generation rejection.
- Status text/rows/colors and compact conditions remain identical.
- Protected configuration and explicit Restore Defaults then Save semantics remain identical.
- Close remains idempotent and stops scheduling before tray/server teardown.
- Existing Pet methods and settings-path behavior used by UI/tests remain compatible.
- Decision: PASS

## QA / Release

- Pure controller tests cover channel independence, quota re-entry, finish/delay, shutdown, compact decisions, protected/current/reset persistence, backup restore, and close idempotence.
- Integration tests cover Pet controller wiring, settings-path replacement, five-row rendering, settings reset, and repeated close-safe cleanup.
- Existing full Quality and package smoke must remain green; no snapshot changes are expected.
- Decision: PASS

## Security / Resource

- No additional workers, timers, subprocesses, network/IPC, polling, writes, retained payloads, dependencies, or Codex quota usage.
- Controllers only consolidate existing bounded state.
- Decision: PASS

## Scope Lock

- Allowed production files: four pure controller APIs and minimum main-window wiring.
- Allowed tests: controller contracts and direct equivalence/integration regressions.
- Allowed release files: canonical version sources, bilingual Changelog, directly affected architecture/API/repository docs.
- Forbidden: v0.3.2 physical matrix closure, UI/content/layout changes, new settings/features, lower-level API deletion, dependencies.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.3.2 is included.
