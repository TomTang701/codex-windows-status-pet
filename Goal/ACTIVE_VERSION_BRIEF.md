# ACTIVE VERSION BRIEF — v0.2.4 Windows 11 Support Matrix

## Identity

- Version: `0.2.4`
- Branch: `release/v0.2.4-windows11-support-matrix`
- Base: `main` at `ef00ce812811220181cc6ab40c5e0e82ff07aa8c`
- PR: `[v0.2.4] Align Windows support and release gates`
- Tag: `v0.2.4`

## Product

- One-sentence outcome: Published support claims and executable release blockers consistently define Windows 11 x64 as supported.
- User problem: Windows 10 is not claimed but is currently represented as a release blocker, contradicting the support policy.
- Success criteria: Windows 10 is exactly Deferred / Not claimed / Non-blocking in English, Chinese, and machine assessment; real Windows 11 scope gaps remain blockers.
- Explicit non-goals: Windows 10 implementation/testing, CI workflow separation, UI behavior, configuration, quota, status rows, dependencies.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| Backend/tooling | Yes | PASS |
| QA/Release | Yes | PASS |
| Documentation | Yes | PASS |
| Frontend | No | N/A |
| Security/Resource | Limited | PASS |

## Product / Documentation

- Supported: Windows 11 x64.
- Deferred and not claimed: Windows 10.
- Not claimed: ARM64 and 32-bit Windows.
- README, installation, release policy, product overview, roadmap, and compatibility matrix must not request Windows 10 evidence as a current release requirement.
- Historical archive/test records remain historical and are not rewritten.
- Decision: PASS

## Tooling / QA

- Compatibility rows may explicitly declare `Non-blocking` in the status cell.
- Readiness assessment excludes explicit non-blocking rows even if they also contain Deferred or partial wording.
- Pending/partial rows without Non-blocking remain blockers.
- Output reports deferred exclusions separately so policy is visible rather than silently discarded.
- Strict mode fails only for real blockers.
- Tests cover Windows 10 deferred exclusion, real pending blockers, mixed case, and all-pass readiness.
- Decision: PASS

## Security / Resource

- Pure local Markdown parsing only; no network, IPC, process, timer, disk write, dependency, or runtime UI change.
- No unsupported platform is falsely claimed.
- Decision: PASS

## Scope Lock

- Allowed production files: release-readiness checker only.
- Allowed tests: release-readiness policy tests.
- Allowed release files: canonical version sources, bilingual Changelog, directly affected support/release documents.
- Forbidden: Windows 10 support work, CI quality/RC split, UI/runtime/config/quota changes, dependencies, historical archive rewrites.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.2.5 or later is included.
