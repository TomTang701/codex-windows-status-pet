# ACTIVE VERSION BRIEF — v0.4.2 Autonomous Verification Conversion

## Outcome

Make the formal release path machine-authoritative for every fact observable from source, tests, Tk, Win32, process state, filesystem, package output, or GitHub state. Routine supported-host release work must require zero human visual confirmation.

## In scope

- Classify every Quality, RC, compatibility, and host-validation fact as `AUTOMATED`, `AUTOMATABLE`, `PHYSICAL-ONLY`, `OBSOLETE`, or `DUPLICATE`.
- Keep one authoritative check for each machine-observable fact.
- Replace CI's duplicated Quality/package/whitespace sequence with the formal RC orchestrator.
- Make RC output separate passes, blockers, and non-blocking limitations.
- Make subprocess decoding deterministic for UTF-8 diagnostics on Windows.
- Replace blanket manual-verification wording with exact physical-only limitations.
- Add no product feature, runtime dependency, provider, polling path, or credential access.

## Protected behavior

- All v0.4.1 runtime behavior and configuration compatibility.
- Quality remains useful as a fast non-release gate.
- RC remains the only formal automated release approval command.
- Simulation never becomes physical evidence.
- Windows 10, unavailable alternate taskbar edges, arbitrary mixed-DPI hardware, and a separate clean machine remain explicit limitations rather than failed tests.

## Observable contracts

- Every inventory item has one class, one authority, and one release disposition.
- Duplicate or obsolete items cannot be presented as independent release requirements.
- `run_release_candidate_checks.py` executes each formal child gate once and returns one JSON document with `passes`, `blockers`, and `limitations`.
- A UTF-8 child diagnostic never crashes the Windows parent decoder.
- CI invokes the same RC orchestration used locally and uploads the package produced by that run.
- Machine-observable UI facts are protected by deterministic adapter/Tk/Win32/process checks, not generic manual confirmation prose.

## Out of scope

- New runtime host-control framework or desktop automation dependency.
- Repeating historical physical tests on every release.
- Claiming unavailable physical hardware coverage.
- Phase 3 API/controller deletion or application architecture simplification.
- Installer/startup productization.

## Design verification result

`DESIGN VERIFIED`

- Problem evidence: PASS — CI repeats Quality/package/whitespace outside RC; active docs still require generic manual UI evidence; readiness output calls limitations `deferred`; Windows child decoding is locale-dependent.
- Root-cause hypothesis: N/A — this is a bounded process capability, not a runtime bug.
- Observable contract: PASS.
- Failure paths: PASS — inventory validation and child-gate failures map to blockers; physical-only facts map once to limitations; malformed output remains diagnostic evidence rather than crashing orchestration.
- Regression surface: PASS — Quality/RC command composition, readiness classification, CI workflow, package artifact, bilingual governance, and all existing runtime tests remain protected.
- RED definition: N/A; focused failing tests are specified by the implementation plan.
- Scope bounded: PASS — no product runtime or dependency change.
- Human verification required: NONE.
