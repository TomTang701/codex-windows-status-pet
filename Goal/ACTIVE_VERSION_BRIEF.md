# ACTIVE VERSION BRIEF — v0.3.0 Independent Stable Status Rows

## Identity

- Version: `0.3.0`
- Branch: `release/v0.3.0-independent-status-rows`
- Base: `main` at `77c15006f9884f7e3c426b13f2ae00dd168bb9fa`
- PR: `[v0.3.0] Render five independent status rows`
- Tag: `v0.3.0`

## Product

- One-sentence outcome: Activity, active-conversation progress, 5h quota, weekly quota, and Reset Credit each render through a stable independent row.
- User problem: A single multiline Label couples row identity, updates, wrapping, and event behavior, making individual status stability fragile.
- Success criteria: Exactly five ordered row IDs exist in pure presentation and five persistent Tk labels; each row can update without shifting or recreating siblings.
- Explicit non-goals: Controller refactor, new content, plan-step display, settings/menu/tray changes, refresh changes, layout redesign, new dependencies.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Visual/UI/UX | Yes | PASS |
| Frontend | Yes | PASS |
| Backend/presentation | Limited | PASS |
| QA/Release | Yes | PASS |
| Security/Resource | Yes | PASS |

## Visual / Frontend

- Stable row order: `activity`, `progress`, `primary_5h`, `weekly`, `reset_credit`.
- Five labels are created once and updated in place; blank progress stays in its own row and never shifts quota rows.
- Existing font, foreground/background, wrap width, compact hide/show, drag, hover, and right-click bindings apply to every row.
- The existing `text`/multiline compatibility surface remains available for callers during this release.
- No new icons, controls, animation, spacing concept, or window-size default.
- Decision: PASS

## Presentation API

- `StatusRowsSnapshot` owns exact row identity/order and exports ordered dict plus legacy joined text.
- `build_status_snapshot` produces both `rows` and byte-for-byte-equivalent `text` from the same snapshot.
- No provider payload or new raw field reaches the UI.
- No controller or scheduling ownership moves in v0.3.0.
- Decision: PASS

## QA / Release

- Pure tests: exact IDs/order, blank padding, excess-line truncation, dict/text consistency, no row shifting.
- Tk tests: exactly five persistent labels, one-row update preserves sibling widget identities/values, style propagation, event-widget coverage.
- Integration: main Pet renders approved row mapping and compact mode still hides/restores the row container.
- Full Quality, package smoke, `git diff --check`, Windows 11 visible-row smoke.
- Decision: PASS

## Security / Resource

- Five labels replace one label; no worker, timer, process, IPC, network, disk, dependency, data retention, or Codex quota increase.
- Updates are bounded to five existing widgets and perform no polling.
- Decision: PASS

## Scope Lock

- Allowed production files: pure status-row API, status snapshot integration, Tk status-row adapter, minimum main-window wiring.
- Allowed tests: row API/snapshot/Tk/main-window direct regressions.
- Allowed release files: canonical version sources, bilingual Changelog, directly affected architecture/repository/testing documents.
- Forbidden: v0.3.1 controllers, refresh/lifecycle/settings persistence refactors, new displayed fields, plan steps, menu/tray/settings changes, dependencies.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.3.1 or later is included.
