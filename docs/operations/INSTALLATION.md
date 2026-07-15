# Installation

简体中文: [中文版本](INSTALLATION.zh-CN.md)

## v0.9.2-beta.1 deployment boundary

This branch is a beta candidate. The latest stable public Release remains
v0.9.1; beta artifacts are for controlled testing until the current UI and
Windows Shell evidence are accepted for a formal release.

The published ZIP is the current normal-user path: verify its SHA-256 if you
validate manually, extract the complete archive, then run
`CodexStatusPet\CodexStatusPet.exe`. The EXE is the application entry point, not
an installer. Do not copy it out of its onedir runtime.

The repository is public. Normal installation does not require Git, GitHub CLI,
`gh auth login`, an account, a token, Python, pip, or a repository checkout.
Use this Quick Install command for the latest stable Release:

```powershell
& ([scriptblock]::Create((irm 'https://github.com/TomTang701/codex-windows-status-pet/releases/latest/download/CodexStatusPet-bootstrap.ps1')))
```

The bootstrap resolves the stable Release, downloads its matching ZIP, SHA-256
sidecar, and existing `install.ps1`, then delegates verification and installation
to that installer. It does not read or embed a token. To pin an exact stable
version, invoke the downloaded bootstrap with `-Tag vX.Y.Z`; a missing or
malformed pinned tag fails without falling back to latest.

GitHub Code -> Download ZIP and the Release Source code archive are source
archives, not the product package. The product ZIP is named
`CodexStatusPet-vX.Y.Z-win11-x64.zip`.

The following artifact-path invocation is retained for source verification and
release engineering. It is not the normal-user Quick Start:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 `
  -ArtifactPath .\CodexStatusPet-v0.9.1-win11-x64.zip `
  -Sha256 <published-sha256>
```

The installer verifies the ZIP before extraction, validates its release manifest,
and installs the application per user at `%LOCALAPPDATA%\Programs\CodexStatusPet`.
It creates one Start Menu shortcut named **Codex Windows Status Pet**. No
administrator elevation, Python, pip, Git, repository checkout, automatic
sign-in startup, or background updater is required for this product path.

The installed EXE still uses the local Codex CLI for live quota data. If Codex
is unavailable, the application reports its existing unavailable diagnostic; it
does not use a third-party quota service.

If the installer reports that an instance is running, choose **Exit** from the
application tray menu and run the installer again. This prevents an old source
or installed process from being mistaken for a successful new launch.

## Upgrade and uninstall

Run the Quick Install command again to upgrade to a newer Release or to perform
a verified same-version reinstall / repair. The product settings file remains at
`%USERPROFILE%\.codex\codex-windows-status-pet.json` and is preserved byte for
byte when no migration is required. Unrelated `.codex` data remains untouched.

To uninstall the installed release, run the `uninstall.ps1` copied inside its
application directory. Normal uninstall removes the EXE and Start Menu shortcut
but preserves settings. To explicitly remove only the product settings file:

```powershell
.\uninstall.ps1 -PurgeSettings
```

It never removes the broader `.codex` directory, Codex sessions, credentials,
or unrelated configuration.

## Security and migration boundary

v0.9.2-beta.1 binaries are unsigned. Windows SmartScreen or an organization policy may
show a warning; verify the published SHA-256 before use. The
`start_codex_status_pet.cmd` source launcher remains for development, debugging,
source verification, and release engineering only. It is not a normal-user
entry point. The public release-acquisition path reuses the same
`install.ps1` implementation; it is not a second installer.
