# ACTIVE VERSION BRIEF — v0.2.2 Reset Credit Expiry

## Identity

- Version: `0.2.2`
- Branch: `release/v0.2.2-reset-credit-expiry`
- Base: `main` at `1dee7c9787709c909222e18ec7bf07afb4f536c1`
- PR: `[v0.2.2] Show the earliest Reset Credit expiry`
- Tag: `v0.2.2`

## Product

- One-sentence outcome: The Reset Credit row truthfully shows `重置 N 次 / HH:MM M/D` when a future expiry is supplied.
- Target user: A Windows 11 Codex user monitoring Reset Credit availability.
- User problem: The count is visible, but valid provider expiry shapes are discarded before presentation.
- Success criteria: Approved expiry aliases and containers normalize to the earliest future expiry; the 5h row remains time-only.
- Explicit non-goals: Status-row refactor, configuration protection, menu changes, CI changes, Windows support scope, new providers.
- Resource impact: Pure bounded parsing only; no new refresh, worker, IPC, network, disk write, or dependency.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Backend | Yes | PASS |
| Frontend | Display verification only | PASS |
| QA/Release | Yes | PASS |
| Security/Resource | Yes | PASS |
| Visual/UI/UX | No layout change | N/A |

## Backend

- Affected boundary: `scripts/api/quota_parse_api.py` and existing quota-format/status-snapshot APIs.
- Input contract: Accept only approved Reset Credit expiry names (`expiresAt`, `expires_at`, `resetsAt`, `resets_at`, `resetAt`, `reset_at`) inside approved containers (`expirations`, `credits`) to bounded depth.
- Output contract: Normalize scalar/list approved expiries into `rateLimitResetCredits.resetsAt`.
- Failure behavior: Ignore booleans, nulls, malformed objects, unknown containers, past and invalid values; never invent a date.
- Concurrency/persistence/network: Unchanged.
- Rollback: Revert the v0.2.2 release commit.
- Decision: PASS

## Frontend Verification

- Reset Credit row: `重置 N 次 / HH:MM M/D` for a valid future expiry.
- Missing valid future expiry: `重置 N 次` with no fabricated suffix.
- 5h row: remains `5h N% / HH:MM`; no date is added.
- Weekly row: unchanged.
- No layout, setting, menu, color, or interaction change.
- Decision: PASS

## QA / Release

- Positive cases: camelCase/snake_case aliases, scalar/list values, `expirations` and `credits` containers, earliest future selection.
- Negative cases: malformed values, booleans, unknown/credential containers, expired values, absent expiry.
- Integration case: parsed provider payload reaches the final Reset Credit display line with local no-leading-zero date.
- Regression case: 5h remains time-only and raw provider fields never reach display text.
- Gates: focused parser/format/snapshot tests, full release checks, `git diff --check`, Windows 11 launcher smoke.
- Decision: PASS

## Security / Resource

- Parser traversal is allowlisted and depth-bounded.
- Unknown credential-like fields are not traversed or propagated.
- No raw payload, token, prompt, response, or session content reaches UI/logs.
- No additional Codex calls, quota consumption, timers, processes, memory retention, or writes.
- Decision: PASS

## Scope Lock

- Allowed production files: Reset Credit parser plus the minimum existing format/presentation integration required for correctness.
- Allowed tests: quota parser, quota formatting, status snapshot, and direct integration regression tests.
- Allowed release files: canonical version sources, bilingual Changelog, directly affected API/README text.
- Forbidden: status-row API/refactor, configuration schema work, menu work, controller work, CI/release-policy work, dependencies, new settings.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.2.3 or later is included.
