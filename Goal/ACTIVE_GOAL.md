# ACTIVE PROGRAM GOAL — v0.9.1 Public Distribution Correction

> **Status:** COMPLETED / RELEASED AND RECONCILED
> **Program owner:** Tom
> **Repository:** `TomTang701/codex-windows-status-pet`
> **Repository visibility:** PUBLIC
> **Released baseline:** `v0.9.0` at `bdae1942856ffa00677e64c63142457d0f79efce`
> **Final target:** released and reconciled `v0.9.1`
> **Execution model:** published asset provenance audit → public PowerShell bootstrap → product ZIP discoverability → lifecycle verification → one v0.9.1 patch release
> **STOP:** satisfied after v0.9.1 release, release-state reconciliation, temporary branch cleanup, final remote `main`-only state, and final verification

## Active Goal authority

This file is the only authoritative active Program Goal.

The completed v0.9.0 Program is the released baseline and historical context. It is not a second active Goal.

Conflicting stale statements that still describe the repository as private or require `gh auth login` for normal user installation are superseded by this Program.

## Program sequence

```text
Phase A: audit the actual published v0.9.0 Release assets and ZIP provenance
→ Phase B: replace private/authenticated bootstrap acquisition with public HTTPS acquisition
→ Phase C: make product ZIP and source-ZIP distinction unmistakable
→ Phase D: verify ZIP direct use and public PowerShell install / repair / pinned-version behavior
→ focused regression
→ formal RC
→ exact-head GitHub Windows CI
→ squash merge
→ merged-main RC
→ annotated v0.9.1 tag and GitHub Release
→ verify v0.9.1 public assets from the public Release surface
→ release-state reconciliation
→ proven-safe temporary branch cleanup
→ confirm remote branch list is exactly main
→ STOP
```

## Product decisions already approved by Tom

Do not reopen or re-ask these decisions:

- `CodexStatusPet.exe` is the formal application launcher / packaged program entry point.
- `CodexStatusPet.exe` is not an installer executable.
- The product remains a PyInstaller onedir package unless evidence proves the existing architecture cannot satisfy this Program.
- ZIP direct use is supported:
  `download product Release ZIP → extract complete ZIP → run CodexStatusPet.exe`.
- PowerShell is the supported installation / repair / upgrade deployment path.
- PowerShell installation deploys the product runtime only, not the repository.
- `start_codex_status_pet.cmd` remains development / debugging / source-verification tooling only.
- The repository is public.
- Normal public installation must not require Git, GitHub CLI, `gh auth login`, a GitHub account, Python, pip, or a repository clone.
- The public PowerShell default is the latest published stable Release.
- An advanced optional `-Tag vMAJOR.MINOR.PATCH` path must allow installation of one explicitly requested published stable version.
- `main` is the only long-lived remote branch and the final remote branch list after Program closure must contain exactly `main`.

## Phase A — published Release asset provenance audit

Before changing bootstrap code or documentation, inspect the actual public v0.9.0 GitHub Release and its downloadable assets.

The expected v0.9.0 product ZIP is exactly:

`CodexStatusPet-v0.9.0-win11-x64.zip`

Do not confuse it with:

- repository `Code → Download ZIP`;
- GitHub-generated `Source code (zip)`;
- GitHub-generated `Source code (tar.gz)`;
- a GitHub Actions workflow artifact;
- a source checkout;
- a locally rebuilt artifact.

Download the actual v0.9.0 Release product ZIP and matching `.sha256` sidecar from the public Release surface.

Verify:

- the product ZIP asset exists;
- the matching SHA-256 sidecar exists;
- the published checksum matches the downloaded product ZIP;
- the archive has one runtime root named `CodexStatusPet`;
- `CodexStatusPet/CodexStatusPet.exe` exists;
- `CodexStatusPet/_internal` exists;
- `CodexStatusPet/release-manifest.json` exists;
- the manifest entry point is exactly `CodexStatusPet.exe`;
- the manifest version is `0.9.0`;
- the ZIP does not contain repository-only material.

Repository-only material prohibited from the product ZIP includes at minimum:

- `tests`;
- `docs`;
- `Goal`;
- `skills`;
- `.github`;
- `.githooks`;
- `.codex-plugin`;
- `.build`;
- source `.py` files;
- the repository source launcher as a normal product entry point.

If the official v0.9.0 product ZIP is correct, record that the previously observed CMD-based ZIP was a source archive / repository ZIP confusion and do not mutate published v0.9.0 history.

If the official v0.9.0 product ZIP is missing, corrupt, or lacks the EXE, treat that as a proven release publication defect. Do not rewrite the v0.9.0 tag and do not silently replace historical v0.9.0 release truth. Correct the release path in v0.9.1.

## Phase B — public PowerShell bootstrap

Replace the current private-repository / authenticated GitHub CLI bootstrap contract.

The canonical public Quick Install command is intended to be:

```powershell
irm 'https://github.com/TomTang701/codex-windows-status-pet/releases/latest/download/CodexStatusPet-bootstrap.ps1' | iex
```

The canonical optional pinned-version form is intended to be:

```powershell
& ([scriptblock]::Create((irm 'https://github.com/TomTang701/codex-windows-status-pet/releases/latest/download/CodexStatusPet-bootstrap.ps1'))) -Tag v0.9.0
```

The exact commands must be verified on the supported Windows PowerShell environment before publication. If syntax must be adjusted for real Windows behavior, keep the user model unchanged:

- default command installs the latest published stable Release;
- optional `-Tag` installs one explicitly requested published stable `vMAJOR.MINOR.PATCH` Release.

### Public acquisition architecture

Use public GitHub HTTPS / REST Release metadata.

Do not scrape GitHub HTML.

Default resolution:

`GET public GitHub releases/latest metadata`

Pinned resolution:

`GET public GitHub releases/tags/<Tag> metadata`

Use exact Release asset metadata and `browser_download_url` values from the resolved published Release.

The public bootstrap must not invoke or require `gh`.

Remove the normal-user dependency on:

- `gh auth status`;
- `gh release view`;
- `gh release download`;
- `gh auth login`.

Do not add token, PAT, cookie, credential, or GitHub-account requirements.

Use an explicit non-secret User-Agent for GitHub REST requests when required by the selected PowerShell implementation.

### Stable Release selection

The default path must resolve the latest published stable GitHub Release.

Reject:

- draft Releases;
- prerelease Releases;
- malformed tags;
- tags that do not match `^v\d+\.\d+\.\d+$`.

The optional `-Tag` path must resolve exactly the requested published stable Release.

Do not silently fall back from an invalid or missing requested tag to latest.

Do not infer product version only from the ZIP filename when Release metadata and the release manifest provide authoritative version information.

### Exact required assets

For resolved version `X.Y.Z`, require exactly the intended product asset names:

- `CodexStatusPet-vX.Y.Z-win11-x64.zip`;
- `CodexStatusPet-vX.Y.Z-win11-x64.zip.sha256`;
- `install.ps1`.

The bootstrap Release itself remains published as:

- `CodexStatusPet-bootstrap.ps1`.

Fail before installation when any required asset is missing.

Do not download a GitHub-generated source archive as a fallback.

### Download and verification

The bootstrap must:

1. create a unique project-owned temporary staging directory;
2. resolve the intended published stable Release;
3. identify the exact required Release assets;
4. download the product ZIP;
5. download the matching SHA-256 sidecar;
6. download or otherwise execute the same Release's authoritative `install.ps1`;
7. parse the sidecar strictly;
8. verify the product ZIP SHA-256 before installation;
9. invoke the existing `install.ps1` authority with:
   - product artifact path;
   - expected SHA-256;
   - expected semantic version;
10. preserve the existing install transaction and rollback authority;
11. clean bootstrap staging in `finally`.

The bootstrap must not create a second independent installer implementation.

`install.ps1` remains authoritative for:

- release manifest validation;
- supported per-user install root;
- settings preservation;
- source-instance mutex safety;
- installed runtime shutdown;
- backup;
- replacement;
- rollback;
- Start Menu shortcut;
- installed EXE launch.

### Public bootstrap error categories

Keep errors understandable and distinguish at minimum:

- Release resolution failure;
- unsupported or malformed Release tag;
- draft / prerelease rejection;
- public GitHub API request failure;
- public Release asset missing;
- public Release asset download failure;
- GitHub unauthenticated API rate-limit failure when it can be identified truthfully;
- invalid checksum sidecar;
- checksum mismatch;
- installation failure.

Do not print tokens, credentials, machine-unique local paths beyond what is necessary for a local error, or unrelated environment details.

## Phase C — product ZIP discoverability and source ZIP distinction

The user must not reasonably mistake a repository source ZIP for the product.

Update README.md and README.zh-CN.md together.

The first user-facing installation section must clearly state the exact latest-version product asset naming pattern:

`CodexStatusPet-vX.Y.Z-win11-x64.zip`

For v0.9.1 examples, use:

`CodexStatusPet-v0.9.1-win11-x64.zip`

Explicitly state:

- download the product ZIP under the GitHub Release `Assets` section;
- do not use `Code → Download ZIP`;
- do not use GitHub-generated `Source code (zip)` for normal product use;
- source archives contain development files and can use the `.cmd` source launcher;
- the product Release ZIP contains the packaged EXE runtime;
- after full extraction, the entry point is:
  `CodexStatusPet\CodexStatusPet.exe`;
- do not copy only the EXE away from the onedir runtime.

### README user flow order

Use this normal-user order:

1. Quick Install — public PowerShell.
2. ZIP Direct Use — exact product ZIP.
3. Upgrade / repair.
4. Install a specific stable version.
5. Uninstall.
6. Tray icon discovery.
7. Development.

The Development section may retain `.cmd` and source-runtime instructions.

Do not place the `.cmd` source launcher in normal user Quick Start.

### Release notes discoverability

The v0.9.1 GitHub Release notes must clearly identify:

`Product ZIP: CodexStatusPet-v0.9.1-win11-x64.zip`

Also state that GitHub-generated `Source code (zip)` is source, not the packaged Windows application.

Do not claim GitHub's automatic source archive can be removed if GitHub always exposes it.

Solve the confusion through exact naming, placement in documentation, Release notes, and verified asset publication.

## Phase D — install, repair, upgrade, and pinned-version verification

### ZIP direct use

Verify the actual release-format product ZIP:

`extract complete ZIP → CodexStatusPet\CodexStatusPet.exe`

Prove the packaged runtime does not require:

- repository checkout;
- `.cmd`;
- system Python;
- development venv;
- source imports outside the package.

Verify overlay, tray, Settings, normal Exit, process cleanup, and mutex cleanup using existing authoritative evidence where still valid.

### Public latest install

From a Windows environment that does not rely on GitHub CLI authentication, execute the documented public Quick Install command.

Prove:

- no `gh` executable is required;
- no `gh auth login` is required;
- no GitHub token is supplied;
- the latest published stable Release is resolved;
- the exact product ZIP is downloaded;
- checksum verification occurs before install;
- `%LOCALAPPDATA%\Programs\CodexStatusPet` is the installed runtime root;
- the Start Menu shortcut targets the installed `CodexStatusPet.exe`;
- the installed EXE launches successfully.

### Same-version repair

Run the supported public deployment path against the same installed version.

Preserve the existing verified behavior:

`same version → verified reinstall / repair`

Prove settings and unrelated `.codex` data are preserved.

### Pinned stable version

Verify the optional `-Tag` path with an actual published stable tag.

The requested tag must be resolved exactly.

Do not claim a pinned-version pass by merely setting a local variable without performing public Release resolution.

### Upgrade behavior

Preserve the existing deployment model:

`run the public Quick Install command again after a newer stable Release exists → resolve latest stable → verify → transactional replacement → preserve settings → relaunch installed EXE`

For v0.9.1 release verification, use the strongest truthful existing controlled upgrade authority and existing v0.8.0-to-v0.9.0 evidence where applicable.

Do not falsely call same-version repair an upgrade.

Do not create an in-app updater in this Program.

## TDD and focused verification

Use TDD RED / GREEN for reproducible bootstrap behavior.

At minimum, focused coverage must prove:

- default release endpoint selects latest stable metadata;
- `-Tag` selects the exact tag endpoint;
- no GitHub CLI command is required by the public bootstrap;
- malformed tags fail;
- draft Releases fail;
- prerelease Releases fail;
- missing requested tag fails without fallback;
- required product ZIP asset name is exact;
- source archives are never selected as product fallback;
- missing product ZIP fails;
- missing SHA-256 sidecar fails;
- missing `install.ps1` fails;
- malformed sidecar fails;
- checksum mismatch fails closed;
- expected version passed to `install.ps1` matches authoritative Release version;
- staging cleanup occurs on success;
- staging cleanup occurs on failure;
- existing installer transaction / rollback contract remains authoritative.

Use the smallest test boundary compatible with the current PowerShell testing architecture.

Do not create a second generalized GitHub client framework.

Do not add a production dependency for this patch.

## Release artifact boundary

The sole Windows product ZIP remains:

`CodexStatusPet-vX.Y.Z-win11-x64.zip`

The archive must contain only the distributable product runtime root and approved end-user runtime files.

The product ZIP must contain the packaged application entry point:

`CodexStatusPet/CodexStatusPet.exe`

The product ZIP must not contain repository development material.

At minimum prohibit:

- tests;
- docs;
- Goal;
- skills;
- GitHub workflow files;
- git hook files;
- build staging;
- Python source files.

Release scripts such as bootstrap / install entry assets may be separate GitHub Release assets.

Do not place the whole repository inside the product ZIP.

Do not replace the product ZIP with GitHub's source archive.

## Protected product contracts

Preserve:

- local official Codex app-server quota authority;
- approved local session metadata only;
- no token reader;
- no third-party quota endpoint;
- no telemetry;
- no hosted backend;
- no Codex-core or built-in pet modification;
- five stable row identities;
- truthful duration-based quota identity;
- row visibility and battery-source independence;
- selected battery source with no fallback;
- bilingual runtime UI;
- manual Compact;
- settings transactions;
- proportional 80–200% Window Size scale;
- DPI recovery;
- position persistence;
- shell identity;
- tray reachability;
- one instance;
- bounded refresh;
- safe shutdown;
- existing settings path and privacy boundary;
- normal uninstall settings preservation;
- purge uninstall CodexStatusPet-settings deletion;
- unrelated `.codex` preservation.

## Explicitly excluded from v0.9.1

Do not add:

- MSI;
- MSIX;
- ClickOnce;
- WiX;
- Inno Setup;
- NSIS;
- another installer framework;
- installer EXE;
- PyInstaller onefile conversion without proven necessity;
- in-app automatic update installation;
- background updater;
- Windows service;
- scheduled-task updater;
- automatic update polling;
- telemetry;
- hosted service;
- new quota provider;
- new quota UI;
- new battery style;
- new theme;
- Windows 10 support expansion;
- ARM64 support;
- unrelated UI redesign;
- repository visibility changes.

Do not redesign the application to solve a distribution-documentation defect.

## Documentation and state updates

Update the closest authoritative files required by the current repository governance.

At minimum inspect and update when applicable:

- `Goal/ACTIVE_GOAL.md`;
- `Goal/EXECUTION_STATE.md`;
- `README.md`;
- `README.zh-CN.md`;
- public-install / release lifecycle documentation already managed by the repository;
- verification inventory;
- compatibility / release evidence that is invalidated or extended by this Program;
- release-state documentation.

Do not add duplicate authority files when an existing authority already owns the fact.

Tracked Markdown must not expose real maintainer machine paths, Windows usernames, drive letters, workspace parent paths, or external launcher locations.

## Required release sequence

- Activate this file as the sole `Goal/ACTIVE_GOAL.md`.
- Update `Goal/EXECUTION_STATE.md` to:
  - released baseline = v0.9.0 at `bdae1942856ffa00677e64c63142457d0f79efce`;
  - active Program = v0.9.1 Public Distribution Correction;
  - current phase = Phase A;
  - final target = released and reconciled v0.9.1.
- Verify repository visibility is actually public.
- Audit actual v0.9.0 public Release assets before implementation.
- Use `using-superpowers` for routing.
- Use `systematic-debugging` before fixing unexpected behavior or test failures.
- Use TDD RED / GREEN for public bootstrap behavior.
- Preserve valid v0.9.0 installer and package evidence unless a v0.9.1 change invalidates it.
- Run focused public bootstrap and release-artifact tests.
- Run public latest-install lifecycle evidence without GitHub CLI authentication.
- Run pinned stable-tag lifecycle evidence.
- Run same-version repair evidence.
- Verify ZIP direct-use EXE provenance.
- Verify product ZIP excludes repository-only material.
- Run English / Simplified Chinese documentation parity and governance checks.
- Run privacy, version, link, whitespace, and sensitive-data checks.
- Run the authoritative formal RC.
- Review the complete diff and unrelated changes.
- Push the active v0.9.1 branch.
- Create or update the v0.9.1 PR.
- Require exact-head GitHub Windows CI.
- Squash merge only after required gates pass.
- Run merged-main RC.
- Create the annotated `v0.9.1` tag.
- Create the v0.9.1 GitHub Release.
- Publish:
  - `CodexStatusPet-v0.9.1-win11-x64.zip`;
  - `CodexStatusPet-v0.9.1-win11-x64.zip.sha256`;
  - `install.ps1`;
  - `CodexStatusPet-bootstrap.ps1`.
- Verify the public Release surface anonymously / without `gh auth login` to the strongest practical extent.
- Verify the product ZIP from the published Release contains `CodexStatusPet/CodexStatusPet.exe`.
- Verify the published public Quick Install command installs v0.9.1.
- Complete release-state reconciliation.
- Verify the temporary v0.9.1 branch is fully merged and has no active dependency.
- Delete the proven-safe temporary remote branch.
- Prune safe stale tracking refs when practical.
- Confirm the final remote branch list contains exactly:
  `main`.
- Mark execution state `COMPLETED / STOP`.
- STOP.

## Scoped remote authorization

This approved Program explicitly authorizes the following workflow for:

`TomTang701/codex-windows-status-pet`

and v0.9.1 only:

```text
replace the completed Goal/ACTIVE_GOAL.md with this approved Program
→ create / switch active v0.9.1 temporary branch
→ implement and verify
→ push active branch
→ create / update PR
→ obtain exact-head GitHub Windows CI
→ squash merge after required gates pass
→ run merged-main RC
→ create intended annotated v0.9.1 tag
→ create intended v0.9.1 GitHub Release
→ publish intended ZIP, SHA-256, install.ps1, and bootstrap assets
→ perform required release-state reconciliation
→ delete the temporary remote branch after proving it is fully merged and no longer active
→ confirm final remote branch list is main only
```

Do not repeatedly request the same push, PR, CI, merge, tag, Release, asset-publication, reconciliation, or proven-safe temporary branch cleanup permission.

Still require Tom's separate explicit authorization for:

- force push;
- rewriting published history;
- deleting or retargeting the existing v0.9.0 tag;
- silently replacing historical v0.9.0 truth instead of releasing the v0.9.1 correction;
- deleting the repository;
- transferring repository ownership;
- changing repository visibility;
- changing collaborators or permissions;
- modifying repository or GitHub Actions secrets;
- bypassing required CI or security controls;
- publishing to a new external registry, store, service, or production environment;
- destructive production-data operations.

## Definition of Done

v0.9.1 is complete only when:

1. This file is the sole authoritative `Goal/ACTIVE_GOAL.md`.
2. The repository is verified public.
3. The actual v0.9.0 public Release assets have been audited.
4. The audit truthfully records whether the previously observed CMD-based ZIP was a source archive confusion or a real v0.9.0 product-asset defect.
5. Published v0.9.0 history is not rewritten.
6. `CodexStatusPet.exe` remains the formal application entry point and not an installer.
7. The v0.9.1 product ZIP is exactly `CodexStatusPet-v0.9.1-win11-x64.zip`.
8. The v0.9.1 product ZIP contains `CodexStatusPet/CodexStatusPet.exe`.
9. The v0.9.1 product ZIP contains the required onedir runtime and manifest.
10. The v0.9.1 product ZIP excludes tests, docs, Goal files, CI files, build staging, and Python source.
11. ZIP direct use is verified as `extract complete product ZIP → run CodexStatusPet.exe`.
12. Normal public Quick Install requires no GitHub CLI.
13. Normal public Quick Install requires no `gh auth login`.
14. Normal public Quick Install requires no GitHub account or token.
15. The default public PowerShell command resolves the latest published stable Release.
16. The optional `-Tag vMAJOR.MINOR.PATCH` path resolves exactly the requested published stable Release.
17. Invalid or missing pinned tags fail without falling back to latest.
18. Draft and prerelease Releases are rejected.
19. Product Release assets are selected by exact expected names.
20. GitHub-generated source archives are never used as product fallback.
21. Product ZIP checksum mismatch fails closed before installation.
22. Existing `install.ps1` remains the installer transaction authority.
23. Normal install targets `%LOCALAPPDATA%\Programs\CodexStatusPet`.
24. The Start Menu shortcut targets the installed `CodexStatusPet.exe`.
25. Same-version public deployment performs verified reinstall / repair.
26. Normal install / repair / upgrade preserves CodexStatusPet settings.
27. Normal install / repair / upgrade preserves unrelated `.codex` data.
28. Existing rollback behavior remains verified.
29. Bootstrap staging is cleaned on success and failure.
30. README.md and README.zh-CN.md lead with public PowerShell Quick Install.
31. README.md and README.zh-CN.md explicitly identify `CodexStatusPet-vX.Y.Z-win11-x64.zip` as the product ZIP.
32. README.md and README.zh-CN.md explicitly warn that `Code → Download ZIP` and `Source code (zip)` are source archives, not the packaged application.
33. Normal-user documentation does not direct users to the `.cmd` source launcher.
34. v0.9.1 Release notes explicitly identify the product ZIP asset and source-ZIP distinction.
35. Focused public bootstrap RED / GREEN tests pass.
36. Public latest-install lifecycle evidence passes without GitHub CLI authentication.
37. Pinned stable-tag lifecycle evidence passes.
38. Same-version repair evidence passes.
39. ZIP direct-use EXE provenance evidence passes.
40. Formal RC passes.
41. Exact-head GitHub Windows CI passes.
42. Merged-main RC passes.
43. The annotated `v0.9.1` tag and GitHub Release target the verified released product commit.
44. The v0.9.1 Release publishes the intended ZIP, SHA-256 sidecar, installer, and bootstrap assets.
45. The published v0.9.1 product ZIP is downloaded from the public Release surface and independently verified to contain `CodexStatusPet/CodexStatusPet.exe`.
46. The published public Quick Install command is verified against the published v0.9.1 Release.
47. Release-state reconciliation is complete.
48. The v0.9.1 temporary remote branch is deleted after proven-safe merge verification.
49. Final remote branch list contains exactly `main`.
50. Final diff and sensitive-data review pass.
51. No excluded feature or unapproved high-risk GitHub operation is introduced.
52. `Goal/EXECUTION_STATE.md` records `COMPLETED / STOP`.
