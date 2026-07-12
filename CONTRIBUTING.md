# Contributing

简体中文: [中文版本](CONTRIBUTING.zh-CN.md)

Use short-lived branches for substantial work and keep `main` releasable. A change should have a requirement, API/file ownership, tests, compatibility impact, security impact, rollback plan, and synchronized English/Chinese documentation when applicable.

Before committing, run the relevant tests, `scripts/check_doc_parity.py`, `scripts/check_doc_governance.py`, `scripts/run_quality_checks.py`, and `git diff --check`. Only `Goal/ACTIVE_GOAL.md` is normative; archived plans must remain explicitly non-normative. Use `scripts/run_release_candidate_checks.py` only for a formal candidate. Use one coherent imperative commit and verify the remote owner and author identity. Do not mix unrelated user changes.
