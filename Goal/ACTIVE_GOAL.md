# Active Goal: Lightweight Source-Based v1.0.0 Release

> **For Codex:** Work directly in the existing `codex-windows-status-pet-ui` checkout on branch `feat/signal-hud-settings-ui-isolated`. Read the repository-root `AGENTS.md` and Tom's global engineering instructions before changing files. Use the smallest complete implementation, TDD where behavior is reproducible, systematic debugging for failures, and fresh verification before completion.

**Goal:** Complete the current UI version, replace the PyInstaller application-EXE distribution with a lightweight source-based installation, merge the verified UI branch into `main`, and publish it as stable `v1.0.0`.

**Architecture:** The GitHub Release contains the application source, launch/install/uninstall scripts, a release manifest, pinned runtime requirements, and one canonical Windows icon—but no packaged `CodexStatusPet.exe`, no bundled Python runtime, and no PyInstaller `_internal` directory. The bootstrap installer detects an existing compatible Windows Python, installs the two runtime dependencies into an application-private directory, deploys under `%LOCALAPPDATA%\Programs\CodexStatusPet`, and creates Desktop and Start Menu shortcuts that launch the app without a visible console.

**Tech Stack:** Python 3.10+, Tkinter, Pillow, pystray, PowerShell, VBScript or an equivalent hidden script launcher, Windows Shell shortcuts, GitHub Actions, GitHub Releases.

## 1. Confirmed Product Decisions

The following decisions are final for this goal:

- The local working folder is `codex-windows-status-pet-ui`.
- The working branch remains `feat/signal-hud-settings-ui-isolated`.
- This UI branch is the intended `v1.0.0` product and will replace the old implementation on `main`.
- Do not create a third repository copy, release worktree, or parallel replacement UI.
- Do not modify or delete the repository-root `AGENTS.md`.
- The Windows taskbar/Shell identity issue is fixed and physically verified.
- Do not repeat the same physical taskbar test unless later code changes affect Shell identity.
- Do not produce a packaged application executable named `CodexStatusPet.exe`.
- Do not bundle a Python interpreter or PyInstaller `_internal` runtime.
- Do not add MSI, MSIX, NSIS, Inno Setup, or another installer framework.
- Keep one-line PowerShell deployment as the normal installation and upgrade path.
- Create both a Desktop shortcut and a Start Menu shortcut by default.
- Both shortcuts must use the same visual icon as the running app and notification-area icon.
- Do not automatically pin the app to the Windows taskbar.
- Do not add automatic sign-in startup in this release.
- Do not add unrelated features or broad refactoring.

## 2. Protected Existing Behavior

Preserve the approved UI and runtime behavior:

- Four-row expanded Signal HUD.
- Five stable logical row identities.
- Compact ten-cell quota battery with percentage.
- 5-hour and Weekly progress bars.
- Reset Credit display.
- English and Simplified Chinese UI.
- Settings Apply, Save, Close, and Restore Defaults.
- Font color, background color, opacity, scale, coordinates, topmost, lock, row visibility, battery source, and refresh interval.
- Context menu and tray Show, Hide, Settings, and Exit behavior.
- Multi-monitor position persistence and recovery.
- Single-instance behavior.
- Existing Shell identity and taskbar fixes.
- Local Codex app-server and approved local session-metadata boundary.
- No access-token reader, telemetry, hosted backend, third-party quota service, or Codex core modification.
- Settings at `%USERPROFILE%\.codex\codex-windows-status-pet.json`.
- Preservation of unrelated `.codex` data.

## 3. Target Installation Experience

The public latest install command remains:

```powershell
& ([scriptblock]::Create((irm 'https://github.com/TomTang701/codex-windows-status-pet/releases/latest/download/CodexStatusPet-bootstrap.ps1')))
```

Expected user experience:

```text
resolve stable GitHub Release
→ download source product ZIP + SHA-256 + install.ps1
→ verify checksum and manifest
→ detect a compatible existing Python
→ deploy application files
→ install pinned dependencies into an application-private directory
→ create Desktop shortcut
→ create Start Menu shortcut
→ launch without a visible console window
```

The user must not need to:

- clone the repository;
- install Git or GitHub CLI;
- authenticate to GitHub;
- open the installed folder to launch the app;
- manually run `pip install`;
- manually create shortcuts;
- copy source files;
- receive or run an application-specific EXE.

## 4. Installation Layout

Use the existing per-user installation root:

```text
%LOCALAPPDATA%\Programs\CodexStatusPet
```

The installed product must contain a compact, explicit structure similar to:

```text
CodexStatusPet\
├─ scripts\
│  ├─ codex_status_pet.py
│  ├─ api\
│  └─ ui\
├─ runtime-packages\
├─ assets\
│  └─ CodexStatusPet.ico
├─ launch.vbs
├─ launch.ps1
├─ install.ps1
├─ uninstall.ps1
├─ requirements-runtime.txt
└─ release-manifest.json
```

Exact supporting source packages may follow the repository's current structure, but:

- do not include tests;
- do not include `.git`;
- do not include `.build`;
- do not include screenshots or development plans unless runtime-required;
- do not include PyInstaller output;
- do not include a bundled Python runtime;
- do not include secrets, local paths, caches, or user files.

## 5. Runtime Strategy

### 5.1 Compatible Python

Support Windows x64 Python 3.10 or newer.

The installer must discover candidates in this order:

1. The current Codex-bundled Python path already used by the repository, when present.
2. A compatible interpreter available through `py.exe`.
3. A compatible `python.exe` available through `PATH`.

A candidate is acceptable only when all required checks pass:

```text
Windows x64
Python >= 3.10
tkinter import succeeds
pip is available
pythonw.exe or another verified no-console launch path is available
```

Do not assume that the Codex internal Python path is permanently available.

Do not edit, upgrade, uninstall, or install packages into Codex's own site-packages or the user's global Python site-packages.

When no compatible interpreter exists, stop cleanly and display a clear message explaining that Python 3.10+ with Tkinter and pip is required. Do not leave a partial install or broken shortcuts.

### 5.2 Application-Private Dependencies

Install pinned runtime dependencies into:

```text
%LOCALAPPDATA%\Programs\CodexStatusPet\runtime-packages
```

Use application-local target installation rather than global installation:

```powershell
<selected-python> -m pip install `
  --disable-pip-version-check `
  --no-warn-script-location `
  --upgrade `
  --target <install-root>\runtime-packages `
  -r <install-root>\requirements-runtime.txt
```

Create `requirements-runtime.txt` with exact tested versions, initially matching the repository's release-tested dependency versions:

```text
Pillow==12.2.0
pystray==0.19.5
```

If current repository tests prove a different exact compatible version is required, use the tested version and update all version checks consistently.

Do not use unbounded `>=` requirements for the stable installer.

### 5.3 Hidden Launcher

Create a stable launcher that:

- locates the installation root relative to itself;
- reads the selected Python record written by the installer;
- revalidates that interpreter before launch;
- sets `PYTHONPATH` to `runtime-packages`;
- starts `scripts\codex_status_pet.py` without a visible console;
- preserves the existing single-instance behavior;
- reports a useful error when the recorded runtime is missing instead of silently doing nothing.

Prefer the smallest existing-platform solution. A `launch.vbs` wrapper calling a focused `launch.ps1` is acceptable.

Do not add a launcher EXE.

## 6. Shortcut Requirements

Create these shortcuts during install and repair:

### Desktop

Resolve the actual Windows Desktop special folder instead of hard-coding `%USERPROFILE%\Desktop`, because Desktop may be redirected by OneDrive or organizational policy.

Shortcut display name:

```text
Codex Windows Status Pet
```

### Start Menu

Create:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Codex Windows Status Pet.lnk
```

### Shared Shortcut Contract

Both shortcuts must:

- launch the hidden source launcher;
- use the installed product directory as working directory;
- include a description identifying Codex Windows Status Pet;
- set `IconLocation` to the installed canonical ICO;
- work when launched after Windows Explorer restarts;
- be recreated during same-version repair;
- be removed during uninstall;
- not create duplicate shortcuts on upgrade or repair.

The shortcut icon, Tk root icon, Settings window icon, Windows taskbar window icon, and notification-area icon must use the same canonical visual design.

Do not claim automatic taskbar pinning. A user may manually pin the Start Menu shortcut.

## 7. Canonical Icon

Create and track:

```text
assets/CodexStatusPet.ico
```

The ICO must use the existing pet/tray design, not a new unrelated logo.

Include standard Windows sizes:

```text
16x16
20x20
24x24
32x32
48x48
64x64
128x128
256x256
```

Use this file as the canonical source for:

- Desktop shortcut;
- Start Menu shortcut;
- Tk main window;
- Settings dialog;
- Windows taskbar identity;
- notification-area icon.

If runtime rendering requires a PIL image, load or derive it from this canonical asset rather than maintaining a visually different icon implementation.

## 8. Release Artifact Contract

Keep the established public product asset name unless a test proves that changing it is necessary:

```text
CodexStatusPet-v1.0.0-win11-x64.zip
CodexStatusPet-v1.0.0-win11-x64.zip.sha256
CodexStatusPet-bootstrap.ps1
install.ps1
```

The ZIP is now a lightweight source runtime package, not a PyInstaller package.

Update `release-manifest.json` to describe the new contract. It must include at least:

```json
{
  "schema_version": 2,
  "product": "codex-windows-status-pet",
  "display_name": "Codex Windows Status Pet",
  "version": "1.0.0",
  "platform": "windows",
  "arch": "x64",
  "runtime": "python",
  "minimum_python": "3.10",
  "entrypoint": "scripts/codex_status_pet.py",
  "launcher": "launch.vbs",
  "icon": "assets/CodexStatusPet.ico"
}
```

Do not include an `entrypoint` value ending in `.exe`.

## 9. Files to Inspect and Modify

Inspect actual repository state before changing anything. At minimum, expect coordinated changes in:

```text
Goal/ACTIVE_GOAL.md
Goal/ACTIVE_VERSION_BRIEF.md
Goal/EXECUTION_STATE.md

scripts/build_release.py
scripts/run_release_candidate_checks.py
scripts/package_smoke_test.py
scripts/packaged_runtime_smoke.py
scripts/installed_lifecycle_smoke.py
scripts/install_release.ps1
scripts/check_version_sources.py

install.ps1
uninstall.ps1
start_codex_status_pet.cmd
requirements.txt
requirements-runtime.txt

packaging/CodexStatusPet.spec

scripts/ui/main_window.py
scripts/ui/settings_dialog.py
scripts/ui/tray or icon-related modules

tests/test_release_artifact_api.py
tests/test_release_build.py
tests/test_package_smoke.py
tests/test_packaged_runtime.py
tests/test_installed_lifecycle.py
tests/test_ci_workflow.py
tests/test_version_sources.py
tests/test_ui_shell_identity.py
tests/test_ui_menu.py
tests for launcher, Python discovery, shortcuts, and uninstall behavior

.github/workflows/ci.yml
.github/workflows/release-candidate.yml

README.md
README.zh-CN.md
CHANGELOG.md
CHANGELOG.zh-CN.md
docs/operations/INSTALLATION.md
docs/operations/INSTALLATION.zh-CN.md
docs/governance/RELEASE.md
docs/governance/RELEASE.zh-CN.md
docs/quality/COMPATIBILITY_MATRIX.md
docs/quality/COMPATIBILITY_MATRIX.zh-CN.md
docs/product/ROADMAP.md
docs/product/ROADMAP.zh-CN.md
```

File names in the current repository may differ. Reuse existing modules and tests instead of creating duplicate mechanisms.

Remove `packaging/CodexStatusPet.spec` only after no active build, test, workflow, or document depends on it.

## 10. Implementation Tasks

### Task 1: Reconcile Active Goal State

- Replace the beta-only `Goal/ACTIVE_GOAL.md` with this goal.
- Update the version brief and execution state.
- Record that the UI branch is the intended 1.0 product.
- Record the completed physical taskbar/Shell validation.
- Remove the old restriction that prohibits a verified PR into `main`.
- Keep `main` unchanged until PR merge.

Verification:

```powershell
python scripts/check_doc_manifest.py
python scripts/check_doc_governance.py
python scripts/check_doc_links.py
git diff --check
```

### Task 2: Define the Source Release Contract with Tests

Use TDD.

Add focused failing tests that require:

- schema version 2;
- Python runtime;
- source entrypoint;
- hidden launcher;
- canonical icon;
- no application EXE;
- no `_internal` runtime;
- no tests or development caches in the product ZIP;
- exact pinned runtime requirements.

Run the focused tests and confirm they fail for the expected old-EXE contract.

Implement the smallest manifest/artifact API changes required.

Rerun focused tests until green.

### Task 3: Replace PyInstaller Build with Source Packaging

Modify the release builder so it:

- validates Windows x64 release context;
- copies only required application source and assets;
- creates the canonical source manifest;
- includes launch/install/uninstall scripts;
- includes pinned runtime requirements;
- excludes tests and development-only files;
- creates the established ZIP and SHA-256 sidecar;
- copies bootstrap and installer assets into the Release staging directory;
- prints artifact path, checksum, unpacked size, and compressed size.

Remove PyInstaller from the production release path.

Do not remove historical files until all references are updated.

Focused verification:

```powershell
python -m unittest <release-build-and-artifact-test-modules> -v
python scripts/build_release.py
```

Inspect the generated ZIP contents.

### Task 4: Implement Python Discovery and Private Dependencies

Use TDD for the discovery and validation logic.

Required test cases:

- valid Codex Python selected first;
- invalid or missing Codex Python falls back;
- `py.exe` candidate works;
- PATH candidate works;
- Python below 3.10 rejected;
- non-x64 Python rejected;
- missing Tkinter rejected;
- missing pip rejected;
- no valid candidate causes clean failure;
- no global or Codex site-packages are modified;
- dependencies install only into `runtime-packages`.

The installer must clean temporary staging and preserve the previous working installation on any failure.

### Task 5: Implement Hidden Source Launch

Use a launcher that starts the UI without a visible terminal window.

Tests must verify:

- launcher resolves relative paths;
- application-private packages are added to import path;
- recorded Python is used when valid;
- missing runtime gives a visible actionable error;
- launch does not invoke `CodexStatusPet.exe`;
- repeated launch preserves single-instance behavior;
- source and installed launches preserve Shell identity.

Do not rework the UI itself unless the source-launch transition exposes a real regression.

### Task 6: Add Unified Icon and Dual Shortcuts

Create the multi-resolution canonical ICO from the current tray design.

Update runtime icon loading so all relevant windows and tray surfaces use the same asset.

Update install/repair to create:

- Desktop shortcut in the resolved Desktop special folder;
- Start Menu shortcut in the current user's Programs folder.

Tests must verify:

- both shortcuts exist;
- both use the same `IconLocation`;
- the icon path exists;
- both launch successfully;
- no console remains visible;
- repair recreates missing shortcuts;
- upgrade does not duplicate shortcuts;
- uninstall removes both shortcuts;
- taskbar/Shell regression tests remain green.

### Task 7: Migrate Upgrade, Repair, Rollback, and Uninstall

The architecture changes from the existing v0.9.1 EXE package to the v1.0.0 source package.

Required lifecycle behavior:

```text
v0.9.1 EXE install
→ v1.0.0 source-package upgrade
→ settings preserved
→ old executable runtime removed
→ new source runtime installed
→ both new shortcuts created
```

Also verify:

- same-version repair;
- missing dependency repair;
- missing shortcut repair;
- failure after backup restores the previous installation;
- normal uninstall preserves settings;
- purge uninstall removes only the product settings file;
- unrelated `.codex` data remains;
- runtime-packages and both shortcuts are removed;
- no installed process remains after uninstall.

Use the published v0.9.1 product artifact as the upgrade baseline.

### Task 8: Simplify the Release Candidate Gate

Replace EXE-specific checks with source-release checks.

The formal RC should run each major layer once:

```text
Quality
source release build
static source-package validation
installed source runtime smoke
public bootstrap smoke against the currently published stable release
README screenshot validation
strict compatibility/readiness
git diff --check
```

Do not run full Quality separately inside multiple nested scripts.

During development, run focused tests only. Run full Quality once after the migration is functionally complete. Run formal RC once on the final local candidate.

### Task 9: Promote Active Version to 1.0.0

After the source deployment path is green:

- update all active version sources to `1.0.0`;
- update artifact expectations;
- update bootstrap User-Agent;
- add stable bilingual changelog entries;
- preserve historically correct beta records;
- update documentation from EXE-centric instructions to source-based installation;
- clearly state that an existing compatible Python is required;
- state that the installer creates both Desktop and Start Menu shortcuts;
- state that no automatic taskbar pin or Windows sign-in startup is created.

### Task 10: Final Local Verification

Run targeted tests during implementation.

When functionality is frozen, run once:

```powershell
python scripts/run_quality_checks.py
```

Then run the final local release gate once:

```powershell
python scripts/run_release_candidate_checks.py
```

Required result:

```json
{
  "release_candidate_approved": true,
  "blockers": []
}
```

Also run:

```powershell
git diff --check
git status --short
git diff --stat main...HEAD
git diff --name-status main...HEAD
```

Review the entire diff for unrelated changes, debug files, local paths, credentials, tokens, generated caches, and obsolete EXE claims.

### Task 11: PR and Exact-Head CI

Push the existing branch:

```text
feat/signal-hud-settings-ui-isolated
```

Create a PR into:

```text
main
```

Suggested title:

```text
release: publish lightweight Codex Status Pet v1.0.0
```

The PR must describe:

- completed UI redesign;
- accepted taskbar/Shell validation;
- removal of the packaged application EXE;
- Python runtime requirements and fallback behavior;
- app-private dependency installation;
- Desktop and Start Menu shortcuts;
- unified icon;
- v0.9.1-to-v1.0.0 migration;
- local Quality and RC results;
- remaining non-blocking limitations.

Require exact-head Windows CI.

CI is the authoritative full installed lifecycle evidence. Do not repeat the entire lifecycle locally after exact-head CI passes unless CI finds a problem.

### Task 12: Merge and Publish

After exact-head CI passes and the full diff is approved:

- squash merge into `main`;
- require the normal `main` Windows workflow to pass on the merged commit;
- do not rerun duplicate local full suites when merged-main CI already covers the exact commit;
- create annotated tag `v1.0.0`;
- publish the GitHub Release;
- upload ZIP, SHA-256, bootstrap, and installer assets;
- verify the Release manifest contains no EXE entrypoint;
- verify the ZIP contains no application EXE or bundled Python.

### Task 13: Public Install Verification

Perform one complete public latest installation test:

```powershell
& ([scriptblock]::Create((irm 'https://github.com/TomTang701/codex-windows-status-pet/releases/latest/download/CodexStatusPet-bootstrap.ps1')))
```

Verify:

- latest resolves to `v1.0.0`;
- checksum passes;
- Python detection passes;
- dependencies are installed only under the product directory;
- Desktop shortcut exists with the canonical icon;
- Start Menu shortcut exists with the canonical icon;
- both shortcuts launch the app;
- no persistent console window appears;
- overlay and tray work;
- normal uninstall removes both shortcuts and preserves settings.

For the pinned path, verify `-Tag v1.0.0` resolution and perform a same-version repair rather than repeating the entire lifecycle.

### Task 14: Final State Reconciliation

After public verification:

- mark `v1.0.0` as latest stable;
- record merge SHA, tag SHA, CI run, artifact SHA-256, compressed size, and installed size;
- record Python versions actually tested;
- record dual-shortcut and icon verification;
- remove obsolete claims that normal users run `CodexStatusPet.exe`;
- retain approved limitations honestly;
- delete the completed UI branch only after it is merged and no longer needed.

## 11. Verification Budget

Avoid redundant test repetition.

Use this schedule:

```text
during implementation
→ focused tests for the files changed

after source deployment migration is complete
→ one full Quality run

final local candidate
→ one formal RC run

PR
→ one exact-head Windows CI lifecycle

merged main
→ normal main CI on exact merge commit

published release
→ one complete public latest install
→ pinned v1.0.0 same-version repair
```

Do not run UI gate, Quality, RC, installed lifecycle, and public bootstrap repeatedly after every documentation or metadata edit.

A later commit invalidates earlier exact-head evidence only when that commit changes code, packaging, installation, workflows, version identity, or release artifacts. For documentation-only corrections, run the relevant document checks and rely on CI policy.

## 12. Definition of Done

The release is complete only when:

- the current UI version is stable and merged into `main`;
- active version sources equal `1.0.0`;
- no packaged application `CodexStatusPet.exe` is produced;
- no Python runtime or PyInstaller `_internal` directory is bundled;
- the Release ZIP is source-based and checksum-verified;
- Python 3.10+ discovery has tested fallbacks;
- dependencies install only into the product directory;
- the app starts without a visible console;
- Desktop and Start Menu shortcuts are created;
- both shortcuts use the canonical pet/tray icon;
- shortcut launch works;
- existing taskbar/Shell behavior remains correct;
- v0.9.1 EXE-to-v1.0.0 source upgrade succeeds;
- repair, rollback, uninstall, and settings preservation succeed;
- one full Quality run passes;
- one final local RC passes;
- exact-head PR CI passes;
- merged-main CI passes;
- `v1.0.0` tag and GitHub Release exist;
- public latest install passes;
- pinned `v1.0.0` repair passes;
- final documentation matches the actual source-based product.

## 13. Final Report Format

Report in this order:

1. Conclusion.
2. Final branch and commit SHA.
3. Files and architecture changed.
4. Final source ZIP contents and sizes.
5. Python discovery results and tested Python versions.
6. Dependency installation location.
7. Desktop and Start Menu shortcut evidence.
8. Unified icon evidence.
9. Quality and RC command results.
10. v0.9.1 upgrade lifecycle result.
11. PR and exact-head CI.
12. Merge commit and tag SHA.
13. Release asset names and SHA-256.
14. Public latest install and pinned repair results.
15. Remaining limitations.
16. Anything not verified and the actual reason.

Do not use old evidence, predictions, or “should work” statements as substitutes for fresh verification.
