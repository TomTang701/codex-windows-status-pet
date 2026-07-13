# Installation

简体中文: [中文版本](INSTALLATION.zh-CN.md)

## Current v0.8.0 deployment boundary

The published ZIP is the current normal-user path: verify its SHA-256 if you
validate manually, extract the complete archive, then run
`CodexStatusPet\CodexStatusPet.exe`. The EXE is the application entry point, not
an installer. Do not copy it out of its onedir runtime.

The repository is private, so only Tom and authorized collaborators can acquire
the v0.8.0 Release through an authenticated GitHub path. A public anonymous
PowerShell download command would be untruthful and is not provided.

The following artifact-path invocation is retained for source verification and
release engineering. It is not the normal-user Quick Start:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1 `
  -ArtifactPath .\CodexStatusPet-v0.8.0-win11-x64.zip `
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

## Current source-verified upgrade and uninstall boundary

Run the same source-verified installer command with a newer verified ZIP to
perform an in-place per-user upgrade. The product settings file remains at
`%USERPROFILE%\.codex\codex-windows-status-pet.json` and is preserved.

To uninstall the installed release, run the `uninstall.ps1` copied inside its
application directory. Normal uninstall removes the EXE and Start Menu shortcut
but preserves settings. To explicitly remove only the product settings file:

```powershell
.\uninstall.ps1 -PurgeSettings
```

It never removes the broader `.codex` directory, Codex sessions, credentials,
or unrelated configuration.

## Security and migration boundary

v0.8.0 binaries are unsigned. Windows SmartScreen or an organization policy may
show a warning; verify the published SHA-256 before use. The
`start_codex_status_pet.cmd` source launcher remains for development, debugging,
source verification, and release engineering only. It is not a normal-user
entry point. v0.9.0 will add the authenticated release-acquisition deployment
path without adding a second installer implementation.
