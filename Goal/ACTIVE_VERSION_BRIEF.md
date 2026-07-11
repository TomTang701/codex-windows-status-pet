# ACTIVE VERSION BRIEF — v0.2.5 Quality / Release Candidate Separation

## Identity

- Version: `0.2.5`
- Branch: `release/v0.2.5-quality-rc-separation`
- Base: `main` at `28fead56d0a68256f436831efcb3877c1b81c5ac`
- PR: `[v0.2.5] Separate quality and release-candidate gates`
- Tag: `v0.2.5`

## Product

- One-sentence outcome: Routine Quality proves automated code health, while Release Candidate separately enforces all formal release blockers.
- User problem: A script and CI step named “release gates” currently pass while physical release blockers remain, making green Quality look like release approval.
- Success criteria: Distinct commands, workflows, outputs, and documentation; Quality never says release-ready; RC fails while any blocking matrix row remains.
- Explicit non-goals: Closing physical evidence gaps, UI/runtime/config/quota changes, Windows support changes, document governance redesign.
- Decision: GO

## Applicability Matrix

| Role | Applicable | Decision |
|---|---:|---|
| Product | Yes | GO |
| CI/Tooling | Yes | PASS |
| QA/Release | Yes | PASS |
| Documentation | Release instructions only | PASS |
| Frontend/Backend runtime | No | N/A |
| Security/Resource | Limited | PASS |

## CI / Tooling

- `run_quality_checks.py`: documents, versions, secrets, dependencies, compile, tests, startup audit; no release-readiness decision.
- `run_release_candidate_checks.py`: runs Quality, package smoke, strict compatibility readiness, and whitespace checks; any failure rejects the candidate.
- Pull requests and pushes to main run only the Quality workflow plus smoke artifact.
- A separate manual Release Candidate workflow runs the strict RC command and uploads an artifact only on success.
- The ambiguous `run_release_checks.py` entry point is removed and all active references migrate.
- Decision: PASS

## QA / Release

- Unit tests prove Quality contains no readiness command.
- Unit tests prove RC invokes readiness with `--strict` and fails when it fails.
- Unit tests prove RC succeeds only when every child gate succeeds.
- Current repository RC is expected to fail because five Windows 11 x64 evidence blockers remain.
- Quality remains green and explicitly reports `quality_approved`, not `release_ready`.
- Decision: PASS

## Security / Resource

- No runtime behavior, network path, dependency, process lifetime, quota usage, or user data changes.
- CI permissions remain read-only.
- Manual RC avoids unnecessary per-commit physical-release evaluation.
- Decision: PASS

## Scope Lock

- Allowed files: CI workflows, check orchestration scripts, their tests, canonical version sources, bilingual Changelog, and directly affected release/testing instructions.
- Forbidden: product code other than version constants, physical evidence fabrication, matrix policy changes, UI/config/quota/controller work, dependency changes, general document-governance redesign.
- Release shape: one focused implementation/release commit, one PR, one tag.
- No work from v0.2.6 or later is included.
