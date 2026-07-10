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
