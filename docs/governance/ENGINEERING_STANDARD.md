# Codex Windows Status Pet Engineering Standard

> **Document-Version:** 1.0.0  
> **Status:** Active canonical standard
> **Canonical-Language:** English  
> **Translation-Pair:** `ENGINEERING_STANDARD.zh-CN.md`  
> **Applies-To:** `TomTang701/codex-windows-status-pet`  
> **Baseline:** `main` at the documentation-framework adoption baseline
> **Owner:** Project maintainer  
> **Review-Cadence:** At least once per minor release and every 90 days  
> **Last-Reviewed:** 2026-07-10

---

## 1. Purpose

This document is the highest-level engineering standard for Codex Windows Status Pet. It defines the rules that remain stable across features, refactors, UI changes, packaging changes, and future contributors.

It is intentionally separate from:

- `docs/product/ROADMAP.md`, which describes roadmap priorities;
- `docs/architecture/API_SPEC.md`, which catalogs concrete API contracts and invariants;
- `docs/architecture/REPOSITORY_STRUCTURE.md` and `docs/architecture/CONFIGURATION.md`, which document repository layout and persisted formats;
- `docs/quality/COMPATIBILITY_MATRIX.md`, which records test evidence;
- `CHANGELOG.md`, which records released and unreleased changes.

When documents conflict, the precedence order is:

1. Security and privacy requirements in this standard;
2. Runtime invariants in this standard;
3. Approved Architecture Decision Records;
4. `docs/architecture/API_SPEC.md`;
5. `docs/architecture/CONFIGURATION.md`;
6. `docs/product/ROADMAP.md`;
7. README and examples.

---

## 2. Normative Language

The keywords **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

- **MUST / MUST NOT:** mandatory for merge or release;
- **SHOULD / SHOULD NOT:** expected unless an approved exception is recorded;
- **MAY:** optional and context-dependent.

An exception to a MUST requires:

1. A written rationale;
2. Scope and expiration date;
3. Risk analysis;
4. Maintainer approval;
5. A tracking issue or ADR.

---

## 3. Product Contract

### 3.1 Product objective

The product is a low-distraction Windows desktop companion that:

- reports real local Codex activity;
- displays truthful quota and reset information;
- remains recoverable on multi-monitor Windows desktops;
- does not modify Codex core files;
- does not require a project-owned backend;
- preserves a narrow local data boundary.

### 3.2 Core differentiators

The following are product-defining capabilities and MUST receive regression protection:

1. Activity is derived from local Codex session events rather than inferred only from quota changes.
2. Quota is read through the local Codex app-server boundary.
3. The overlay remains reachable through the tray and display recovery paths.
4. User settings are validated, transactional, and recoverable.
5. Virtual desktop coordinates, including negative coordinates, are supported.
6. Missing or malformed provider data is never replaced with fabricated values.

### 3.3 Explicit non-goals

The following remain out of scope unless approved through security review and an ADR:

- direct reading of `auth.json`;
- access-token extraction or persistence;
- third-party quota services;
- telemetry or analytics;
- cloud synchronization;
- modification of Codex core or built-in pet files;
- collection of prompt, response, or project content;
- automatic redemption of reset credits;
- macOS or Linux support;
- a Tauri or other framework rewrite.

---

## 4. Documentation Architecture

### 4.1 Required normative documents

The repository SHOULD maintain the following document set:

| Document | Purpose | Update trigger |
|---|---|---|
| `ENGINEERING_STANDARD.md` | Stable project-wide engineering rules | Policy or governance change |
| `ARCHITECTURE.md` | Components, dependency direction, lifecycle, concurrency | Architectural change |
| `docs/architecture/API_SPEC.md` | API contracts, types, invariants, error behavior | API behavior change |
| `docs/architecture/REPOSITORY_STRUCTURE.md` and `docs/architecture/CONFIGURATION.md` | Repository layout, config schema, file ownership | File/schema change |
| `SECURITY.md` | Threat model, privacy boundary, vulnerability process | Security boundary change |
| `TESTING.md` | Test levels, fixtures, commands, evidence rules | Test strategy change |
| `RELEASE.md` | Versioning, gates, packaging, rollback | Release process change |
| `CONTRIBUTING.md` | Branch, commit, PR, review workflow | Collaboration change |
| `docs/product/ROADMAP.md` | Current roadmap and priorities | Planning change |
| `docs/quality/COMPATIBILITY_MATRIX.md` | Living physical and automated evidence | Compatibility result |
| `CHANGELOG.md` | Release history | User-visible change |
| `README.md` | User-facing introduction and installation | User workflow change |

### 4.2 Document classes

Documents are classified as:

- **Normative:** defines required behavior or process;
- **Descriptive:** explains current design;
- **Evidence:** records test results;
- **Generated:** created by tooling.

Normative English documents MUST have synchronized Chinese translation pairs. Evidence and generated files MAY remain language-neutral or English-only when duplication would add no maintenance value.

### 4.3 Source-of-truth rule

English is canonical. A Chinese document:

- MUST be a translation of its English pair;
- MUST NOT add requirements absent from English;
- MUST preserve headings, API names, IDs, tables, versions, and code examples;
- MUST be updated in the same commit as a substantive English change.

---

## 5. Architecture Principles

### 5.1 Dependency direction

Dependencies MUST flow inward:

```text
Windows/Tk adapters
        ↓
Application controllers
        ↓
Domain services and state machines
        ↓
Pure models, validation, formatting, and policies
```

Rules:

- Domain APIs MUST NOT import Tkinter or pystray.
- Pure APIs MUST NOT perform filesystem, subprocess, network, or Windows UI calls.
- UI adapters MAY call domain APIs.
- Transport adapters MAY return domain values but MUST NOT mutate UI.
- Background workers MUST communicate with Tk through queues or scheduled main-thread callbacks.
- Circular imports are prohibited.

### 5.2 Module ownership

Each module MUST have:

- one primary responsibility;
- an explicit public surface;
- documented side effects;
- documented thread expectations;
- deterministic tests where practical;
- a named owner category: domain, transport, platform, application, or UI.

A module SHOULD be split when it simultaneously owns two or more of:

- persistence;
- transport;
- parsing;
- state transitions;
- scheduling;
- Windows platform calls;
- UI widgets.

### 5.3 UI adapter rule

UI code MAY:

- create and arrange widgets;
- bind user actions;
- render domain state;
- call application controllers;
- display validated warnings.

UI code MUST NOT:

- parse raw quota payloads;
- read or write configuration files directly;
- implement retry or backoff policy;
- own token or credential handling;
- perform blocking subprocess or filesystem work;
- contain the canonical validation or geometry algorithms.

### 5.4 Architecture Decision Records

A significant architectural choice MUST have an ADR under:

```text
docs/adr/NNNN-short-title.md
```

An ADR is required for:

- changing UI framework;
- adding a provider;
- changing credential boundaries;
- changing configuration format;
- changing packaging technology;
- changing supported Windows versions;
- introducing a database or backend;
- replacing the concurrency model;
- breaking an established API.

Accepted ADRs are immutable. A later ADR supersedes an earlier one.

---

## 6. API Contract Standard

### 6.1 Contract requirements

Every public API MUST document:

- purpose;
- accepted inputs;
- returned values;
- side effects;
- thread-safety;
- error behavior;
- security boundary;
- compatibility promise;
- test boundary.

### 6.2 Input and output design

APIs SHOULD use typed dataclasses, enums, and explicit result objects instead of unstructured dictionaries.

Raw provider dictionaries:

- MUST remain inside the transport/parsing boundary;
- MUST NOT reach UI code;
- MUST NOT be persisted;
- MUST NOT be logged in full.

Time values SHOULD be timezone-aware `datetime` objects inside the domain layer. Formatting belongs in formatting APIs.

### 6.3 Error contracts

Expected failures SHOULD be represented by typed results or documented exception types.

APIs MUST distinguish:

- invalid caller input;
- malformed external data;
- temporary transport failure;
- authentication/signed-out state;
- unsupported protocol response;
- internal programming error.

A broad `except Exception` MAY exist only at a process, worker, or UI safety boundary, where it MUST log a sanitized diagnostic and preserve recovery.

### 6.4 Backward compatibility

A public API change is breaking when it:

- removes or renames a public function or field;
- changes accepted units or value meaning;
- changes error semantics;
- changes persistence behavior;
- changes thread-safety guarantees.

Breaking changes require:

- an ADR;
- a major version or documented pre-1.0 migration;
- migration notes;
- compatibility tests;
- synchronized documentation.

---

## 7. Domain Models and State

### 7.1 Typed domain values

Quota, activity, settings-session, refresh-channel, and window-state data SHOULD use typed immutable values.

Recommended core models include:

- `UsageWindow`;
- `ResetCreditSummary`;
- `QuotaSnapshot`;
- `QuotaDisplayState`;
- `ActivitySnapshot`;
- `DisplaySnapshot`;
- `SettingsSnapshot`;
- `WindowPlacement`;
- `RefreshChannelState`.

### 7.2 State machine requirement

Behavior with meaningful transitions MUST be modeled as a state machine rather than scattered booleans.

State-machine candidates include:

- quota loading/ok/stale/signed-out/unavailable;
- settings persisted/runtime/draft/opening state;
- compact/expanded/hovered/dragging/menu-open;
- tray starting/running/failed/restarting/stopped;
- refresh idle/running/cancelled/shutdown.

Every state machine MUST define:

- states;
- events;
- valid transitions;
- invalid transition behavior;
- persistence behavior;
- recovery behavior;
- tests for each transition.

---

## 8. Configuration and Persistence

### 8.1 Configuration schema

The persisted configuration MUST include a schema version:

```json
{
  "schema_version": 1
}
```

Each setting MUST define:

- type;
- default;
- minimum/maximum or allowed values;
- whether it is user-editable;
- whether it is security-sensitive;
- migration behavior;
- UI control.

### 8.2 Validation layers

Editable settings MUST be validated at three layers:

1. Keystroke or candidate validation;
2. Apply/Save submission validation;
3. Configuration-load validation.

No single layer is sufficient.

### 8.3 Transaction semantics

Settings MUST preserve separate concepts:

- persisted settings;
- active runtime settings;
- draft settings;
- opening snapshot.

Required behavior:

- Apply previews without persistence;
- Save applies and persists;
- Close restores the opening snapshot when changes were not saved;
- Restore Defaults changes the draft first;
- a failed save does not destroy the previous valid file.

### 8.4 Atomicity and recovery

Writes MUST use:

- same-directory temporary files;
- flush and `fsync`;
- atomic replacement;
- sanitized errors.

The project SHOULD retain one last-known-good backup once schema migrations are introduced.

### 8.5 Schema migration

A schema change MUST include:

- old and new version;
- deterministic migration;
- idempotency test;
- corrupt/partial input test;
- downgrade or rollback statement;
- changelog entry.

Silent destructive migration is prohibited.

---

## 9. Concurrency, Scheduling, and Lifecycle

### 9.1 Thread ownership

- Tk APIs MUST run on the Tk main thread.
- pystray ownership MUST remain isolated from Tk.
- Transport and filesystem work MUST run off the Tk thread.
- Shared mutable state MUST be protected or confined to one thread.
- A queue payload MUST have a documented schema.

### 9.2 Refresh channels

Activity and Quota refreshes MUST remain independent.

Each refresh channel MUST define:

- interval source;
- single-flight behavior;
- generation/token behavior;
- cancellation behavior;
- shutdown behavior;
- error backoff;
- success recovery;
- maximum worker count.

A delayed callback MUST verify that its generation is current before scheduling more work.

### 9.3 Shutdown

Shutdown MUST be idempotent.

The shutdown sequence SHOULD be:

1. mark application closing;
2. invalidate scheduled generations;
3. prevent new workers;
4. stop tray;
5. stop app-server;
6. flush safe persisted state;
7. release the mutex;
8. destroy Tk.

No callback may reschedule itself after shutdown begins.

### 9.4 Single instance

The application MUST use a named mutex or equivalent ownership primitive.

It MUST NOT:

- kill another process based only on name or title;
- create duplicate tray icons;
- overwrite settings during a failed second launch.

Future “show existing instance” behavior requires an explicit IPC design and ADR.

---

## 10. Reliability and Recovery

### 10.1 Reliability goals

The application MUST fail visibly and recoverably rather than silently disappear.

Critical recovery paths:

- tray can restore a hidden overlay;
- settings can recover an off-screen overlay;
- malformed settings fall back field-by-field;
- app-server failure does not stop Activity updates;
- transient quota failure retains last-good data;
- monitor topology changes do not permanently lose the window.

### 10.2 Last-good and stale policy

The quota state model MUST define:

- loading before first success;
- ok after valid success;
- last-good retention after temporary failure;
- stale after a documented age;
- signed-out when explicitly detected;
- unavailable for unsupported or malformed provider data.

The UI MUST communicate both data age and failure state.

### 10.3 Retry and backoff

Retry policy MUST be centralized.

It MUST define:

- initial retry delay;
- maximum delay;
- multiplier or sequence;
- reset-on-success behavior;
- non-retryable errors;
- user-triggered refresh behavior.

Retries MUST NOT create overlapping workers or unbounded logs.

### 10.4 Window recovery

Window placement MUST:

- preserve valid secondary and negative coordinates;
- detect when the complete window is outside all current work areas;
- restore to a visible nearest work area;
- account for taskbar reservations;
- define behavior when a monitor is disconnected;
- remain testable without physical monitors.

---

## 11. Security and Privacy

### 11.1 Security boundary

The default product MUST:

- use local Codex app-server data;
- never read `auth.json`;
- never store access tokens or account IDs;
- never send prompts, responses, project files, or session text to third parties;
- never log raw quota responses;
- never add telemetry without explicit opt-in design and security review.

### 11.2 Threat model

`SECURITY.md` MUST consider:

- malicious or malformed settings files;
- malicious session JSONL content;
- protocol response changes;
- executable path substitution;
- command injection;
- symlink/reparse-point behavior where relevant;
- log disclosure;
- dependency compromise;
- unsigned binary warnings;
- unsafe update mechanisms.

### 11.3 Sensitive data handling

Sensitive values MUST be:

- excluded from logs;
- excluded from crash reports;
- excluded from test fixtures;
- excluded from screenshots;
- excluded from repository history.

Sanitization SHOULD occur before data crosses into diagnostics APIs.

### 11.4 External providers

Any external provider requires:

1. A provider interface contract;
2. An ADR;
3. Threat-model update;
4. Permission and credential design;
5. Token storage decision;
6. Endpoint allowlist;
7. Timeout and response-size limits;
8. Redaction tests;
9. Failure fallback;
10. User-visible disclosure.

---

## 12. Diagnostics and Observability

### 12.1 Logging requirements

Logs MUST include enough context to diagnose:

- startup;
- Codex discovery;
- app-server lifecycle;
- refresh failures;
- parsing failures;
- tray failures;
- window recovery;
- settings migration;
- shutdown.

Logs MUST NOT include sensitive content.

### 12.2 Structured events

Diagnostics SHOULD use stable event IDs, for example:

```text
APP-START-001
QUOTA-TRANSPORT-002
CONFIG-MIGRATION-003
TRAY-RECOVERY-004
DISPLAY-RECOVERY-005
```

Each event SHOULD include:

- timestamp;
- severity;
- component;
- event ID;
- sanitized message;
- exception type when relevant.

### 12.3 Log lifecycle

The project MUST define:

- log path;
- encoding;
- maximum size;
- rotation count;
- retention;
- behavior when logging fails.

Normal successful polling SHOULD NOT produce repetitive log entries.

### 12.4 Diagnostic summary

A user-facing diagnostic summary SHOULD expose:

- application version;
- Windows version;
- display count and DPI;
- configured paths without sensitive content;
- app-server status;
- last successful quota refresh;
- last Activity refresh;
- current state;
- log location.

---

## 13. Coding Standard

### 13.1 Python baseline

The project MUST document its minimum and tested Python versions.

Code SHOULD:

- use type hints for public APIs;
- use dataclasses/enums for domain values;
- use `pathlib.Path`;
- avoid mutable default arguments;
- avoid hidden global state;
- keep functions focused;
- use explicit encodings;
- use monotonic time for durations;
- use timezone-aware wall-clock values for timestamps.

### 13.2 Naming

- Modules: `snake_case`;
- Functions and variables: `snake_case`;
- Classes: `PascalCase`;
- Constants: `UPPER_SNAKE_CASE`;
- Private implementation details: leading underscore;
- Test names: `test_<behavior>_<condition>_<expected>` where practical.

### 13.3 Function quality

A function SHOULD be split when:

- it exceeds one responsibility;
- it mixes platform calls with policy;
- it performs validation, persistence, and rendering together;
- it has deeply nested control flow;
- its tests require constructing unrelated infrastructure.

### 13.4 Comments and docstrings

Comments SHOULD explain why, constraints, or platform behavior—not restate the code.

Public APIs MUST have docstrings describing behavior and error contracts.

Dead code, unreachable code, commented-out implementations, and obsolete compatibility paths MUST be removed.

---

## 14. Dependency and Supply-Chain Policy

### 14.1 Dependency criteria

A new runtime dependency requires:

- documented purpose;
- maintenance activity check;
- license compatibility;
- security history review;
- package size impact;
- startup impact;
- clean-machine installation test;
- removal plan if abandoned.

### 14.2 Pinning

The project MUST define whether dependencies use:

- minimum compatible bounds;
- tested lock versions;
- reproducible build constraints.

Release builds SHOULD use a reviewed lock or constraints file.

### 14.3 Update policy

Dependency updates SHOULD be isolated commits or PRs and MUST run:

- unit tests;
- clean import test;
- packaging smoke test;
- security scan where available;
- Windows launch smoke test for UI/runtime dependencies.

---

## 15. Testing Standard

### 15.1 Test layers

The test strategy MUST distinguish:

| Level | Purpose | Examples |
|---|---|---|
| Unit | Pure deterministic behavior | formatting, validation, state transitions |
| Contract | Adapter/provider assumptions | app-server payload and error matrix |
| Integration | Multiple components together | settings session plus persistence |
| UI contract | Tk adapter behavior | menu closes, Apply/Close semantics |
| Platform | Windows-specific APIs | mutex, work areas, DPI |
| Physical | Real desktop evidence | mixed DPI, taskbar edge, tray |
| Packaging | Clean-machine execution | EXE/installer startup |
| Soak | Long-running stability | timer/thread/resource growth |

### 15.2 Test requirements by change

| Change | Minimum required tests |
|---|---|
| Pure domain API | Unit tests |
| Parser/transport | Unit + contract tests |
| Settings schema | Unit + migration + integration |
| Threading/scheduler | Unit + race/lifecycle tests |
| UI behavior | API tests + manual Windows evidence |
| Display/DPI | Geometry tests + physical matrix |
| Packaging | Clean-machine smoke |
| Security boundary | Negative/redaction tests |
| Performance change | Benchmark or bounded fixture |

### 15.3 Determinism

Tests SHOULD inject:

- clocks;
- filesystem roots;
- payloads;
- monitor layouts;
- scheduler generations;
- process factories.

Tests MUST NOT depend on the maintainer’s live Codex account unless explicitly marked manual.

### 15.4 Test evidence

A passing simulation MUST NOT be recorded as a physical pass.

Physical evidence SHOULD record:

- date;
- Windows build;
- display topology;
- DPI;
- taskbar position;
- application version/commit;
- result;
- screenshot or probe output when safe.

### 15.5 Coverage policy

Coverage percentage is a signal, not the release criterion. Critical state transitions and failure paths MUST have explicit tests even if overall line coverage is high.

---

## 16. Windows and UI Compatibility

### 16.1 Supported platform policy

The release documentation MUST list:

- supported Windows versions;
- tested Windows builds;
- supported architectures;
- minimum display resolution;
- supported Python/runtime model;
- known unsigned-binary behavior.

### 16.2 Display requirements

The application MUST account for:

- single and multiple monitors;
- negative virtual coordinates;
- monitor gaps;
- mixed DPI;
- taskbar on each edge;
- auto-hidden taskbar;
- monitor disconnect/reconnect;
- work area rather than full monitor bounds;
- popup larger than available work area.

### 16.3 Accessibility

The UI SHOULD support:

- readable minimum font sizes;
- high contrast;
- status text in addition to color;
- keyboard dismissal with Escape;
- reduced motion;
- no inaccessible hover-only critical action;
- clear focus behavior.

### 16.4 Localization

User-facing strings SHOULD move toward a localization catalog rather than remaining embedded in UI code.

Formatting rules MUST define:

- local timezone;
- `M/D` without leading zeros where required;
- 24-hour or 12-hour time policy;
- pluralization;
- fallback text;
- maximum display length.

---

## 17. Performance and Resource Budgets

The project MUST define measurable budgets. Initial targets:

| Metric | Target |
|---|---|
| Tk callback blocking work | No filesystem, subprocess, or network blocking |
| Concurrent quota workers | Maximum 1 |
| Concurrent Activity workers | Maximum 1 |
| UI queue polling | 100–500 ms |
| Normal quota refresh | User setting, 1–10 seconds |
| Activity refresh | Approximately 1 second |
| Popup geometry calculation | Under 5 ms on supported hardware |
| Configuration load | Under 50 ms for normal file size |
| Idle CPU | Document and measure before release |
| Idle memory | Document and measure before release |
| Log growth | Bounded by rotation |
| Soak test | At least 8 hours before stable release |

A performance claim MUST include environment and method.

---

## 18. Versioning, Release, and Rollback

### 18.1 Versioning

Use Semantic Versioning:

- patch: compatible fixes;
- minor: compatible features;
- major: breaking contracts.

Before 1.0, breaking changes MUST still be documented and migrated deliberately.

All version sources MUST agree:

- application constant;
- plugin manifest;
- changelog;
- package metadata;
- artifact name;
- release tag;
- diagnostic output.

### 18.2 Release gates

A release MUST NOT be published until:

- automated checks pass;
- required physical matrix rows pass or have an approved limitation;
- version sources match;
- English and Chinese normative documents are synchronized;
- changelog is finalized;
- sensitive-file scan passes;
- clean-machine or clean-environment startup passes;
- rollback instructions exist;
- known issues are documented.

### 18.3 Release channels

Recommended channels:

- development build;
- preview/beta;
- stable.

A preview build MUST be clearly labeled and MUST NOT be presented as release-ready.

### 18.4 Rollback

Every release SHOULD define:

- previous stable version;
- configuration compatibility;
- uninstall/reinstall path;
- downgrade limitations;
- backup/restore path;
- emergency withdrawal procedure.

---

## 19. Git, Commit, and Review Workflow

### 19.1 Branching

Recommended model:

- protected `main`;
- short-lived feature/fix branches;
- pull requests for substantial changes;
- no direct unreviewed release changes.

### 19.2 Commit quality

Each commit SHOULD:

- contain one coherent change;
- compile and pass relevant tests;
- avoid unrelated formatting;
- include synchronized documentation when required;
- use an imperative subject;
- avoid generated secrets or local paths.

### 19.3 Pull request requirements

A substantial PR MUST include:

- problem statement;
- scope and non-scope;
- design summary;
- API/file changes;
- tests;
- manual evidence;
- security/privacy impact;
- performance impact;
- compatibility impact;
- documentation updates;
- rollback plan.

### 19.4 Review checklist

Reviewers MUST check:

- requirement-to-code traceability;
- API boundaries;
- thread ownership;
- error handling;
- settings migration;
- sensitive data;
- tests and negative cases;
- dead code;
- documentation truthfulness;
- release impact.

---

## 20. Change Classification and Governance

### 20.1 Change classes

| Class | Examples | Required governance |
|---|---|---|
| C0 Documentation | wording without behavior change | parity check |
| C1 Internal refactor | no contract change | tests, no behavior claim |
| C2 Compatible behavior | new setting or state | spec, tests, changelog |
| C3 Performance/concurrency | scheduler, caching, threads | benchmark, lifecycle tests |
| C4 Compatibility/platform | DPI, Windows version, packaging | matrix evidence |
| C5 Security boundary | provider, credential, logging | ADR, threat review |
| C6 Breaking change | schema/API removal | migration, version decision |

### 20.2 Traceability

Substantial work SHOULD have an issue or roadmap ID.

The preferred trace is:

```text
Requirement → Issue/ADR → API contract → Tests → Changelog → Compatibility evidence
```

### 20.3 Risk register

The project SHOULD maintain a small risk register containing:

- risk;
- likelihood;
- impact;
- mitigation;
- owner;
- review date;
- current status.

---

## 21. Deprecation and Removal

A public feature, setting, file format, or API MUST NOT be removed silently.

Deprecation requires:

1. Announcement in changelog;
2. Replacement guidance;
3. Compatibility period;
4. Warning behavior when appropriate;
5. Removal version;
6. Migration test.

Obsolete internal code SHOULD be removed promptly once no supported path depends on it.

---

## 22. Definition of Ready

A feature is ready for implementation when:

- user outcome is clear;
- scope and non-scope are written;
- dependencies are identified;
- API ownership is proposed;
- security/privacy impact is considered;
- compatibility impact is considered;
- acceptance criteria are testable;
- documentation pairs are identified;
- rollback or disable strategy exists.

---

## 23. Definition of Done

A feature is done only when:

1. Behavior matches approved acceptance criteria;
2. API boundaries are documented;
3. Public types and errors are documented;
4. Unit and required integration tests pass;
5. Negative and failure paths are tested;
6. Tk thread remains non-blocking;
7. Scheduler and shutdown behavior are safe;
8. Settings migration/persistence is tested when relevant;
9. Sensitive data is excluded;
10. Performance impact is measured when relevant;
11. Compatibility matrix is updated when relevant;
12. English normative documentation is updated;
13. Chinese translation is updated in the same commit;
14. Changelog is updated;
15. Dead code is removed;
16. Release checks pass;
17. Physical evidence exists when required;
18. Version claims are truthful.

---

## 24. Exception Process

An exception request MUST include:

```text
Rule:
Reason:
Scope:
Risk:
Mitigation:
Owner:
Expiration:
Tracking issue:
```

Expired exceptions automatically become violations until renewed.

Security and sensitive-data rules SHOULD NOT receive permanent exceptions.

---

## 25. Maintenance Cadence

### Every substantial change

- run relevant tests;
- run document parity;
- update changelog/specification;
- inspect staged files;
- verify no sensitive data;
- make a focused commit.

### Every minor release

- review this standard;
- review supported Windows matrix;
- review dependencies;
- review open P0/P1 defects;
- run a soak test;
- validate clean installation;
- review logs for sensitive data;
- reconcile all version sources.

### Every 90 days

- archive obsolete roadmap items;
- review ADRs;
- review risk register;
- review dependency health;
- test restore/rollback;
- verify bilingual document pairs;
- remove dead compatibility paths.

---

# Appendix A — API Contract Template

```markdown
## API Name

**Module:**  
**Owner layer:**  
**Purpose:**  
**Public symbols:**  
**Inputs:**  
**Outputs:**  
**Side effects:**  
**Thread model:**  
**Errors:**  
**Security boundary:**  
**Compatibility promise:**  
**Tests:**  
**Observability:**  
```

---

# Appendix B — ADR Template

```markdown
# ADR-NNNN: Title

- Status: Proposed / Accepted / Superseded
- Date:
- Decision owners:

## Context

## Decision

## Alternatives considered

## Consequences

## Security and privacy impact

## Compatibility and migration

## Test and rollout plan

## Rollback plan
```

---

# Appendix C — Feature Specification Template

```markdown
# Feature: Name

## User outcome

## Scope

## Non-scope

## Current behavior

## Required behavior

## State transitions

## API changes

## Persistence changes

## Error behavior

## Security/privacy impact

## Compatibility impact

## Performance budget

## Acceptance tests

## Manual Windows evidence

## Rollback/disable strategy

## Documentation changes
```

---

# Appendix D — Release Checklist

```text
[ ] Version sources match
[ ] Automated release checks pass
[ ] Unit/contract/integration tests pass
[ ] Required physical matrix rows pass
[ ] Clean-machine startup passes
[ ] Soak test passes
[ ] English/Chinese documents match
[ ] Changelog finalized
[ ] No sensitive files or logs included
[ ] Known issues documented
[ ] Upgrade/downgrade behavior documented
[ ] Artifacts named and checksummed
[ ] Rollback path verified
```

---

# Appendix E — Severity Matrix

| Severity | Meaning | Expected response |
|---|---|---|
| P0 | Security breach, destructive corruption, or release-blocking crash | Block release; fix immediately |
| P1 | Core workflow failure, incorrect status, lost recovery path | Fix before stable release |
| P2 | Recoverable defect or major maintainability risk | Schedule in current/next minor |
| P3 | Polish, documentation, low-risk edge case | Backlog with rationale |

---

# Appendix F — Adoption Plan

Adopt this standard incrementally:

### Phase 1 — Governance baseline

1. Add this English file and Chinese pair.
2. Add them to document parity checks.
3. Declare this document the highest-level standard.
4. Correct stale statements in existing documents.

### Phase 2 — Split specialized standards

Create paired:

- `ARCHITECTURE.md`;
- `SECURITY.md`;
- `TESTING.md`;
- `RELEASE.md`;
- `CONTRIBUTING.md`.

Move details out of `docs/architecture/API_SPEC.md` and `docs/product/ROADMAP.md` without changing runtime behavior.

### Phase 3 — Automate gates

Add checks for:

- document versions and pairs;
- API names;
- changelog version headings;
- config schema version;
- version-source consistency;
- sensitive-file patterns;
- test and package smoke results.

### Phase 4 — Enforce on pull requests

Protect `main`, require CI, and use PR templates based on this standard.
