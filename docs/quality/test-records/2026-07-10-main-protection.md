# Main Protection Check — 2026-07-10

- Repository: `TomTang701/codex-windows-status-pet`
- Visibility: private
- Default branch: `main`
- Required Quality context observed on recent PRs: workflow `Windows Quality`, job/check `quality`

## Result

Server-side rulesets and classic branch protection are unavailable on the current GitHub plan for this private repository. Read-only API requests for both features returned HTTP 403 with the explicit message: upgrade to GitHub Pro or make the repository public.

The repository was not made public, no purchase or plan upgrade was attempted, and no destructive push/deletion/force-push test was performed.

## Compensating controls

- Never push release changes directly to `main`.
- Use one version branch and one focused PR.
- Record and verify the expected PR head SHA before merge.
- Wait for the exact `Windows Quality / quality` check to succeed.
- Squash merge only.
- Fetch and retest the merged `main`.
- Verify the release tag is reachable from `origin/main`.
- Delete the release branch only after post-release verification.

If the maintainer later upgrades to GitHub Pro, create a `main` ruleset requiring PRs and the exact `quality` check, blocking force pushes and deletions, and requiring linear history. Do not guess the status-check context.
