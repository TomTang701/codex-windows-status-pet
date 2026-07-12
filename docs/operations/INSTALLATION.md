# Installation

简体中文: [中文版本](INSTALLATION.zh-CN.md)

## Supported v0.8.0 product path

On Windows 11 x64, install a versioned `CodexStatusPet-v…-win11-x64.zip`
release with its published SHA-256 value:

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

## Upgrade and uninstall

Run the same installer command with a newer verified ZIP to perform an in-place
per-user upgrade. The product settings file remains at
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
show a warning; verify the published SHA-256 before installation. The older
`start_codex_status_pet.cmd` source launcher remains a developer fallback only,
not the supported installed-product path.
