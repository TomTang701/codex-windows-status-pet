---
document_id: CONTRIBUTING
status: active
document_version: 1.0.0
canonical_language: en
translation_pair: CONTRIBUTING.zh-CN.md
owner: maintainer
last_reviewed: 2026-07-10
review_cycle_days: 90
---
# Contributing

The active [Engineering Standard](docs/governance/ENGINEERING_STANDARD.md) is the highest-level authority for every contribution; this file adds contributor workflow details without overriding it.

Use short-lived branches for substantial work and keep `main` releasable. A change should have a requirement, API/file ownership, tests, compatibility impact, security impact, rollback plan, and synchronized English/Chinese documentation when applicable.

Before committing, run the relevant tests, `scripts/check_doc_parity.py`, `scripts/run_release_checks.py`, and `git diff --check`. Use one coherent imperative commit and verify the remote owner and author identity. Do not mix unrelated user changes.

## Branch, change, and review rules

Substantial work uses a short-lived branch and focused commits; do not accumulate unrelated major changes directly on `main`. Classify each change as behavior, API, configuration schema, UI, performance, security, documentation, packaging, or physical evidence. New behavior requires an owned API boundary, negative and compatibility tests, English canonical documentation, same-commit Chinese translation, changelog entry, and rollback note.

Before every substantial commit run `scripts/run_quality_checks.py` and `git diff --check`, inspect the staged paths, and verify author/remote owner. Formal release work additionally runs `scripts/run_release_candidate_checks.py`; an expected strict physical failure must remain visible rather than bypassed.

Pull requests state requirement, root cause, user impact, security/privacy impact, compatibility evidence, tests, documentation, and rollback. Review must reject hidden provider changes, blocking Tk I/O, raw dict parsing in UI, credential access, duplicated date/version logic, unsupported schema overwrite, or physical claims based only on simulation.
