# ACTIVE VERSION BRIEF — v0.9.0 Distribution, Upgrade, and Repository Hygiene

## Released state

- Latest released product: `v0.9.0` at `bdae1942856ffa00677e64c63142457d0f79efce`.
- Annotated tag and GitHub Release: `v0.9.0`, targeting the same commit.
- Active implementation scope: none.

## Approved outcome

v0.9.0 makes the packaged EXE and full release ZIP the normal user paths,
provides truthful authenticated PowerShell deployment for the private GitHub
Release, and verifies repair, upgrade, rollback, and uninstall behavior.

## Protected contracts

Keep the v0.8.0 onedir architecture, local Codex quota/activity boundaries,
bilingual UI, manual Compact, settings, DPI, position recovery, Shell identity,
tray reachability, one-instance behavior, threading, and safe shutdown. Do not
add MSI/MSIX, an installer framework, in-app or background updating, telemetry,
a token reader, a third-party quota endpoint, or a Codex-core change.

## Completion record

The merged-main formal RC passed. Exact-head GitHub Windows CI for PR #40
passed before squash merge. The Release contains the versioned Windows ZIP,
its SHA-256 sidecar, `install.ps1`, and the authenticated bootstrap script.
Repository hygiene enabled automatic deletion of merged head branches and
removed only branches proven merged or byte-for-byte duplicate. The distinct
closed, unmerged `goal/reset-credit-repo-hardening` history remains retained.

**Status:** `COMPLETED / STOP — wait for Tom's next approved Goal.`
