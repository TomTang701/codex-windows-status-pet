# Repository Engineering Instructions

These instructions apply only to `TomTang701/codex-windows-status-pet` and supplement Tom's global engineering instructions.

## GitHub and Remote Action Policy

Tom grants standing authorization for routine GitHub workflow operations within the scope and lifetime of the current `Goal/ACTIVE_GOAL.md`:

- push a verified work branch;
- create and update the current pull request;
- read and monitor GitHub Actions and CI;
- investigate CI failures under the repository debugging/TDD rules, fix them, and push the verified correction;
- squash-merge after required CI and verification pass;
- synchronize and verify `main`;
- create and push the normal semantic-version tag;
- create or update the corresponding GitHub Release;
- delete completed, merged, no-longer-needed remote work/release branches;
- reconcile active release state and continue automatically to the next ACTIVE_GOAL phase.

This standing authorization applies only when the configured target remains `TomTang701/codex-windows-status-pet` and the operation remains inside the active Goal's defined scope. Before remote writes, verify the remote owner, authenticated GitHub account, branch/head, scope, tests, Quality/RC when applicable, complete diff, unrelated changes, and secret/credential scan.

Standing authorization never permits bypassing CI, failed verification, scope locks, root-cause debugging, TDD, secret scanning, or completion verification.

For efficiency, documentation-only, release-metadata-only, or test-only changes do not require testing the main application. Run only the directly affected documentation, script syntax, packaging-contract, or version checks. Run application tests when production application code or runtime behavior changes.

The following operations still require Tom's separate explicit authorization:

- force push or rewrite published history;
- delete or rename the main/default branch;
- change repository visibility;
- transfer, archive, or delete the repository;
- change collaborators, repository permissions, secrets, or GitHub Actions secrets;
- purchase or upgrade a GitHub plan;
- publish packages to external registries;
- production deployment;
- change the remote owner or target repository;
- destructive Git operations against unrelated user work;
- credential access or credential rotation.

The authorized routine sequence is:

```text
verified scope
→ relevant tests
→ Quality / RC when applicable
→ complete diff review
→ unrelated-change check
→ secret/credential scan
→ push branch
→ PR
→ CI success
→ exact head verification
→ squash merge
→ main verification
→ tag / Release when applicable
→ release branch cleanup
→ active-state reconciliation
→ next Phase
```
