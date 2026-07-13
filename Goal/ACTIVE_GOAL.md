# ACTIVE PROGRAM GOAL — v0.9.0 Distribution, Upgrade, and Repository Hygiene

> **Status:** APPROVED PROGRAM / SEQUENTIAL DELIVERY
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Released baseline:** `v0.8.0` at `788f870bceb3d457e4b0708fa3620637092b5808`
> **Final target:** released and reconciled `v0.9.0`
> **Execution model:** user distribution contract → install/upgrade lifecycle → repository branch hygiene → one v0.9.0 product release
> **STOP:** only after v0.9.0 release, final reconciliation, proven-safe remote branch cleanup, and final verification

## Program sequence

```text
Phase A: EXE / ZIP / source-launch contract and user documentation
→ Phase B: formal ZIP direct-use verification
→ Phase C: truthful one-command PowerShell deployment
→ Phase D: script-driven reinstall / repair / upgrade / uninstall lifecycle
→ Phase E: remote branch audit and repository hygiene
→ full regression and release gates
→ exact-head Windows CI
→ squash merge
→ merged-main RC
→ v0.9.0 annotated tag and GitHub Release
→ final release-state reconciliation
→ proven-safe temporary remote branch cleanup
→ STOP
```

## Phase A — product entry point and user distribution contract

- `CodexStatusPet.exe` is the formal packaged application entry point.
- `CodexStatusPet.exe` is not an installer executable.
- The existing PyInstaller onedir package remains the default architecture unless evidence proves it cannot satisfy this Program.
- ZIP direct use is a formal user path:
  `download ZIP → extract the complete package → run CodexStatusPet\CodexStatusPet.exe`.
- Do not claim that copying only `CodexStatusPet.exe` out of the onedir package is supported.
- Installed use is a formal user path:
  `PowerShell deployment → %LOCALAPPDATA%\Programs\CodexStatusPet → Start Menu → CodexStatusPet.exe`.
- `start_codex_status_pet.cmd` remains available only for development, debugging, source verification, and release engineering.
- README Quick Start must no longer direct normal users to the repository `.cmd` launcher.
- English and Simplified Chinese user documentation remain synchronized.
- Preserve the authentic tray-icon discovery guidance and packaged screenshots already established by v0.8.0.

## Phase B — formal ZIP direct-use contract

The real release-format ZIP must prove:

- the extracted package contains the authoritative release manifest;
- the manifest entry point is `CodexStatusPet.exe`;
- the application runs without repository checkout, `.cmd`, system Python, development venv, or source imports outside the packaged runtime;
- existing CodexStatusPet settings remain readable;
- existing approved local Codex data boundaries remain unchanged;
- overlay, tray menu, Settings, and normal Exit remain available;
- normal Exit cleans up the packaged process tree and `Local\CodexWindowsStatusPet` mutex;
- ZIP direct use does not create a Start Menu shortcut or claim installed state unless the user runs the deployment path.

Extend the smallest existing packaged-runtime authority where practical. Do not duplicate equivalent smoke architecture.

## Phase C — truthful one-command PowerShell deployment

- The intended experience is:
  `one documented command → official release acquisition → SHA-256 verification → install/update → Start Menu shortcut → launch CodexStatusPet.exe`.
- Reuse the existing verified `install.ps1` authority.
- Prefer one small bootstrap / release-acquisition layer instead of a second installer implementation.
- The official release ZIP and matching SHA-256 authority remain mandatory.
- Checksum mismatch must fail closed before installation.
- Normal deployment installs per-user under `%LOCALAPPDATA%\Programs\CodexStatusPet`.
- The Start Menu shortcut targets the installed `CodexStatusPet.exe`.
- Existing CodexStatusPet settings must survive normal deployment.
- Unrelated `.codex` data must remain untouched.
- A conflicting source instance holding `Local\CodexWindowsStatusPet` must block unsafe replacement.
- Successful deployment launches the installed EXE.
- Temporary ZIP, staging directories, and incomplete install residue must be removed after success.
- Transactional replacement must restore the previous installed runtime when failure occurs after backup creation.
- PowerShell errors must distinguish release resolution, acquisition, checksum, manifest, running-instance, and installation failures.

### Private repository constraint

- Inspect actual GitHub repository visibility and supported authentication before selecting the final Quick Install command.
- The repository is currently expected to be private unless GitHub state proves otherwise.
- Do not document anonymous public `irm ... | iex` installation when the Release cannot actually be downloaded anonymously.
- While private, implement and document the smallest truthful authenticated path available to Tom and authorized collaborators.
- Prefer existing authenticated GitHub tooling when it materially simplifies private Release acquisition.
- Never embed a token, PAT, cookie, credential, or personal secret.
- Do not require a hard-coded personal access token.
- Anonymous public one-command installation remains unavailable while the repository is private.
- Repository visibility changes are outside this Program and require Tom's separate explicit authorization.

## Phase D — reinstall, repair, upgrade, and uninstall lifecycle

### Reinstall / repair

- Running the supported deployment command against the same installed version performs one verified reinstall / repair transaction.
- Do not build a separate repair subsystem.

### Upgrade

The supported model is:

`run the PowerShell deployment/update command again → resolve intended newer Release → verify → preserve settings → transactionally replace runtime → relaunch EXE`

The upgrade path must:

- recognize installed-runtime provenance;
- use authoritative release metadata or manifest version, not filenames alone;
- verify the replacement artifact before replacing the installed runtime;
- preserve CodexStatusPet settings byte-for-byte when no migration is required;
- preserve unrelated `.codex` data;
- close the installed product through the safest practical product-local path;
- restore the prior installed runtime if a supported replacement fails after backup creation;
- remove temporary backup state after a successful upgrade;
- refresh the Start Menu shortcut when required;
- relaunch the new installed EXE;
- leave no source `pythonw.exe ... scripts\codex_status_pet.py` process as the user's normal runtime.

Do not add in-app update installation, a background updater, Windows service, scheduled-task updater, or update polling timer in v0.9.0.

### Uninstall

Normal uninstall removes:

- installed runtime;
- Start Menu shortcut.

Normal uninstall preserves:

- CodexStatusPet settings;
- unrelated `.codex` data.

Purge uninstall removes:

- installed runtime;
- Start Menu shortcut;
- CodexStatusPet settings.

Purge uninstall preserves:

- unrelated `.codex` data.

Keep uninstall script-based. Do not create a GUI uninstaller.

## Phase E — repository branch hygiene

### Long-lived remote branch

The only intended long-lived remote branch is:

`main`

### Temporary branches

Goal, feature, fix, documentation, test, chore, and release branches may exist while active.

After a PR is merged:

1. verify the head branch is fully merged into the intended base;
2. verify no active Goal or open PR still depends on it;
3. delete the proven-safe merged remote head branch;
4. prune safe stale remote-tracking references when practical.

Do not preserve historical branches merely as version archives. Tags and GitHub Releases own released-version history.

### Historical remote branch audit

Audit every current non-main remote branch and classify it as exactly one of:

- fully merged and safe to delete;
- closed / abandoned with no unique required work and safe to delete;
- active / open work;
- unique unmerged work;
- unclear.

This Program authorizes deletion when evidence proves that a remote branch:

- is fully merged into `main`; or
- belongs to closed historical work, has no unique required content after comparison, and has no open PR or active Goal dependency.

Do not force-delete unclear or unique unmerged work.

Do not force push.

Do not rewrite Git history.

The local uncommitted / divergent documentation work previously identified around `53670bc` must not be destroyed, overwritten, or treated as a safe remote branch deletion merely because it diverges from `main`.

### Automatic merged-head deletion

Inspect the GitHub repository setting for automatic deletion of PR head branches after merge.

If the available GitHub tooling safely supports enabling `Automatically delete head branches`, enable it.

If the tooling cannot safely modify that setting:

- record the exact maintainer action required;
- do not claim it is enabled;
- continue performing authorized proven-safe post-merge cleanup during this Program.

Do not modify repository visibility, collaborators, permissions, secrets, branch protection, or rulesets.

## User documentation contract

README and README.zh-CN.md must lead normal users through:

1. Quick Install.
2. ZIP Direct Use.
3. Upgrade.
4. Uninstall.
5. Tray Icon.
6. Development.

### Quick Install

- Show one truthful command that actually works under the repository's real visibility and authentication constraints.
- State the authentication requirement clearly when the repository remains private.

### ZIP Direct Use

Document:

```text
download official Release ZIP
→ verify checksum when manually validating the artifact
→ extract the complete ZIP
→ open the CodexStatusPet directory
→ run CodexStatusPet.exe
```

Explicitly warn:

`Do not copy only CodexStatusPet.exe out of the extracted onedir package.`

### Upgrade

- Re-run the supported deployment/update command.
- Normal upgrade preserves settings.

### Daily launch

Installed users:

`Start Menu → Codex Windows Status Pet`

ZIP direct-use users:

`extracted CodexStatusPet\CodexStatusPet.exe`

### Development

- Move `.cmd`, source Python, test, and release-engineering instructions under a clearly separate development section.
- Do not direct normal users to `start_codex_status_pet.cmd`.

## Protected contracts

- Local official Codex app-server quota authority.
- Approved local session metadata only.
- No token reader.
- No third-party quota endpoint.
- No telemetry.
- No hosted backend.
- No Codex-core or built-in pet modification.
- Five stable row identities.
- Truthful duration-based quota identity.
- Row visibility and battery-source independence.
- Selected battery source with no fallback.
- Bilingual runtime UI.
- Manual Compact.
- Settings transactions.
- Proportional 80–200% Window Size scale.
- DPI recovery.
- Position persistence.
- Shell identity.
- Tray reachability.
- One instance.
- Bounded refresh.
- Safe shutdown.
- Existing settings path and privacy boundary.

## Explicitly excluded from v0.9.0

- MSI or MSIX.
- ClickOnce.
- WiX.
- Inno Setup.
- NSIS.
- Another installer framework.
- PyInstaller onefile conversion without proven necessity.
- In-app automatic update installation.
- Background updater.
- Windows service.
- Scheduled-task updater.
- Automatic update polling.
- Telemetry.
- Hosted service.
- New quota provider.
- New quota visualization.
- New battery style.
- New theme.
- Windows 10 support expansion.
- ARM64 support.
- Unrelated UI redesign.
- Repository visibility change.

## Required verification and release sequence

- Use `using-superpowers` to route technical work.
- Use `systematic-debugging` before fixing unexpected behavior or failing tests.
- Use TDD RED/GREEN for reproducible bootstrap, install, reinstall, upgrade, rollback, and branch-classification behavior.
- Preserve already-valid v0.8.0 evidence unless a v0.9.0 change invalidates it.
- Run focused distribution / install / lifecycle tests.
- Verify checksum mismatch fails closed.
- Verify private-repository acquisition behavior selected for this Program.
- Verify ZIP direct EXE provenance without source runtime dependency.
- Verify first install.
- Verify Start Menu launch.
- Verify same-version reinstall / repair.
- Verify a truthful upgrade transaction; do not call same-version repair an upgrade.
- Verify settings preservation.
- Verify unrelated `.codex` preservation.
- Verify failed replacement rollback.
- Verify temporary-file and stale-backup cleanup.
- Verify normal uninstall.
- Verify purge uninstall.
- Verify current remote branch classification before deleting any branch.
- Run English / Simplified Chinese documentation parity, governance, link, privacy, version, and sensitive-data checks.
- Run the authoritative formal RC.
- Review the complete diff and unrelated changes.
- Require exact-head GitHub Windows CI.
- Squash merge the approved v0.9.0 product PR.
- Run merged-main RC.
- Create the annotated `v0.9.0` tag and GitHub Release.
- Publish the intended v0.9.0 ZIP and SHA-256 sidecar.
- Complete authoritative release-state reconciliation.
- Verify temporary remote branches are safe before deletion.
- Delete proven-safe temporary remote branches.
- Confirm final remote branch state.
- STOP.

## Scoped remote authorization

This approved Program explicitly authorizes the following workflow for:

`TomTang701/codex-windows-status-pet`

and v0.9.0 only:

```text
create / switch active Goal branch
→ push active Goal branch
→ create / update PR
→ obtain exact-head GitHub Windows CI
→ merge after required gates pass
→ create intended annotated v0.9.0 tag
→ create intended v0.9.0 GitHub Release
→ publish intended ZIP and SHA-256 sidecar
→ perform required release-state reconciliation
→ delete temporary remote branches proven safe under this Program
```

Do not repeatedly request the same push, PR, CI, merge, tag, Release, or proven-safe branch-cleanup permission.

Still require Tom's separate explicit authorization for:

- force push;
- rewriting published history;
- deleting the repository;
- transferring repository ownership;
- changing repository visibility;
- changing collaborators or permissions;
- modifying repository or GitHub Actions secrets;
- bypassing required CI or security controls;
- publishing to a new external registry, store, service, or production environment;
- destructive production-data operations.

## Definition of Done

- `Goal/ACTIVE_GOAL.md` identifies this Program as the only active Program Goal.
- v0.8.0 remains the released baseline until v0.9.0 is formally published.
- `CodexStatusPet.exe` remains the formal application entry point and is not an installer.
- Official ZIP direct use is verified as `extract → run CodexStatusPet.exe`.
- ZIP direct use does not require repository source, `.cmd`, system Python, or development venv.
- One truthful PowerShell Quick Install command exists for the actual GitHub visibility and authentication state.
- Official Release ZIP and matching checksum authority are acquired and verified.
- Checksum mismatch fails closed before installation.
- Installation targets `%LOCALAPPDATA%\Programs\CodexStatusPet`.
- The Start Menu shortcut targets the installed EXE.
- Normal install, reinstall, and upgrade preserve CodexStatusPet settings.
- Normal install, reinstall, and upgrade preserve unrelated `.codex` data.
- Same-version execution is a documented verified reinstall / repair transaction.
- A truthful newer-version or controlled-version upgrade transaction is verified.
- Supported failed replacement restores the previous installed runtime after backup creation.
- Successful deployment leaves no temporary artifact or stale backup residue.
- Normal uninstall preserves settings.
- Purge uninstall removes CodexStatusPet settings.
- Both uninstall paths preserve unrelated `.codex` data.
- README Quick Start no longer leads users to the repository `.cmd`.
- README and README.zh-CN.md clearly separate normal EXE use from source development.
- All current non-main remote branches are audited and classified.
- Every proven-safe merged or approved closed historical remote branch is deleted.
- No active, unclear, or unique unmerged work is deleted.
- `main` is the only intended long-lived remote branch.
- Automatic merged-head deletion is enabled when safely supported by available tooling, or the exact uncompleted maintainer action is recorded truthfully.
- Future release workflow includes proven-safe post-merge branch cleanup.
- Focused RED/GREEN tests pass.
- Windows lifecycle evidence passes.
- Formal RC passes.
- Exact-head GitHub Windows CI passes.
- Merged-main RC passes.
- `v0.9.0` tag and GitHub Release resolve to the verified released product commit.
- The Release contains the intended ZIP and SHA-256 sidecar.
- Release-state reconciliation is complete.
- Final remote branch state matches this Program's repository-hygiene policy.
- Final diff and sensitive-data review pass.
- No explicitly excluded feature or unapproved high-risk GitHub operation is introduced.
- Final execution state records `STOP` after v0.9.0 release, reconciliation, branch cleanup, and verification.
