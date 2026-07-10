# Contributing

Use short-lived branches for substantial work and keep `main` releasable. A change should have a requirement, API/file ownership, tests, compatibility impact, security impact, rollback plan, and synchronized English/Chinese documentation when applicable.

Before committing, run the relevant tests, `scripts/check_doc_parity.py`, `scripts/run_release_checks.py`, and `git diff --check`. Use one coherent imperative commit and verify the remote owner and author identity. Do not mix unrelated user changes.
