# ACTIVE VERSION BRIEF — v0.2.6 Executable Document Governance

## Identity

- Version: `0.2.6`
- Branch: `release/v0.2.6-document-governance`
- Base: `main` at `bcbdc875ed25472bc016551835df77cabc597f14`
- PR: `[v0.2.6] Enforce minimal document governance`
- Tag: `v0.2.6`

## Product

- One-sentence outcome: One focused executable check guarantees the active Goal and archived-plan boundaries without adding low-value documentation bureaucracy.
- User problem: The rules are written down, but a duplicate Goal or normative-looking archived plan could silently reintroduce conflicting instructions.
- Success criteria: Only approved files can live in `Goal/`; `ACTIVE_GOAL.md` is unique and required; archived plans are explicitly non-normative and cannot be release-required.
- Explicit non-goals: Documentation rewrite, freshness enforcement, prose linting, review-cycle scheduling, v0.3.0 status-row work, runtime behavior.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product/Governance | Yes | GO |
| Tooling | Yes | PASS |
| QA/Release | Yes | PASS |
| Documentation | Yes | PASS |
| Runtime/Frontend/Backend | No | N/A |
| Security/Resource | Limited | PASS |

## Governance Contract

- Allowed Goal files: `ACTIVE_GOAL.md`, `ACTIVE_VERSION_BRIEF.md`, optional `EXECUTION_STATE.md`, and `README.md`.
- `ACTIVE_GOAL.md` must exist exactly once; version-specific Goal files and extra active-goal copies fail Quality.
- Every Markdown plan under `docs/archive/plans/` must begin with front matter declaring `status: archived`, `normative: false`, and a valid repository-relative `superseded_by` target.
- Manifest entries under `docs/archive/` may never set `required_for_release: true`.
- Archived plans are checked only for safe classification/linkage; their old content, parity, freshness, and historical claims do not block release.
- Existing manifest, link, and bilingual parity checks remain unchanged.
- Decision: PASS

## QA / Release

- Positive fixture: approved Goal set plus correctly classified archived plan.
- Negative fixtures: duplicate active Goal, version Goal, unknown Goal file, missing active Goal, missing/incorrect archive metadata, broken supersession target, release-required archive manifest entry.
- One new check is added to routine Quality; no separate prose style, timestamp, ownership, or review-age gate is introduced.
- Decision: PASS

## Security / Resource

- Local bounded filesystem/JSON/text inspection only.
- No network, subprocess, runtime process, dependency, user data, credential, or product behavior change.
- Decision: PASS

## Scope Lock

- Allowed files: document-governance checker/tests, Quality registration, Goal/docs governance instructions, manifest if needed, canonical version sources, bilingual Changelog.
- Forbidden: product/runtime code other than version constants, document content rewrites, archive parity/freshness gates, status-row/controller work, CI policy changes, dependencies.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.3.0 or later is included.
