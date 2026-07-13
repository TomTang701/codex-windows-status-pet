"""Exercise the real per-user installer lifecycle on a Windows host or runner."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

from api.installer_contract_api import installation_paths
from package_smoke_test import static_package_smoke


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class InstalledLifecyclePaths:
    install_root: Path
    shortcut: Path
    settings_file: Path


def installed_lifecycle_paths(*, local_app_data, app_data, user_profile):
    """Return the exact product-owned paths the lifecycle smoke may inspect."""
    installation = installation_paths(local_app_data, user_profile)
    return InstalledLifecyclePaths(
        install_root=installation.install_root,
        shortcut=Path(app_data) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Codex Windows Status Pet.lnk",
        settings_file=installation.settings_file,
    )


def ensure_clean_install_root(paths):
    """Never replace or uninstall a product installation this smoke did not create."""
    if paths.install_root.exists():
        raise RuntimeError("refusing to mutate an existing installed product")


def windows_powershell_executable(system_root):
    """Return the Windows PowerShell host that supplies installer cmdlets."""
    return Path(system_root) / "System32" / "WindowsPowerShell" / "v1.0" / "powershell.exe"


def _powershell_executable():
    return str(windows_powershell_executable(Path(os.environ["SystemRoot"])))


def _powershell_file(script, *arguments):
    return subprocess.run(
        [_powershell_executable(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *map(str, arguments)],
        check=True,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def installed_process_probe_command(executable):
    """Return a PowerShell probe with a literal, safely quoted EXE path."""
    target = Path(executable).as_posix().replace("'", "''")
    return (
        f"$target = [IO.Path]::GetFullPath('{target}'); "
        "$match = Get-CimInstance Win32_Process -Filter \"Name = 'CodexStatusPet.exe'\" | "
        "Where-Object { $_.ExecutablePath -and [IO.Path]::GetFullPath($_.ExecutablePath) -eq $target }; "
        "if (!$match) { exit 1 }"
    )


def _installed_process_is_running(executable):
    command = installed_process_probe_command(executable)
    completed = subprocess.run(
        [_powershell_executable(), "-NoProfile", "-Command", command],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.returncode == 0


def _release_checksum(artifact):
    return Path(f"{artifact}.sha256").read_text(encoding="ascii").split()[0]


def _release_version(artifact):
    return artifact.name.split("-v", 1)[1].split("-win11", 1)[0]


def installed_lifecycle_smoke():
    """Prove install, reinstall, normal uninstall, and purge stay product-scoped."""
    if sys.platform != "win32":
        raise RuntimeError("installed lifecycle smoke requires Windows")
    artifact = static_package_smoke()
    paths = installed_lifecycle_paths(
        local_app_data=Path(os.environ["LOCALAPPDATA"]),
        app_data=Path(os.environ["APPDATA"]),
        user_profile=Path(os.environ["USERPROFILE"]),
    )
    ensure_clean_install_root(paths)
    checksum = _release_checksum(artifact)
    sentinel = paths.settings_file.parent / f"codex-status-pet-lifecycle-{uuid.uuid4().hex}.sentinel"
    prior_settings = paths.settings_file.read_bytes() if paths.settings_file.exists() else None
    paths.settings_file.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text("unrelated Codex data", encoding="utf-8")
    try:
        _powershell_file(ROOT / "install.ps1", "-ArtifactPath", artifact, "-Sha256", checksum, "-ExpectedVersion", _release_version(artifact))
        executable = paths.install_root / "CodexStatusPet.exe"
        if not executable.is_file() or not paths.shortcut.is_file():
            raise RuntimeError("installed product executable or Start Menu shortcut is missing")
        if not _installed_process_is_running(executable):
            raise RuntimeError("installed executable did not remain running")
        paths.settings_file.write_text('{"lifecycle_smoke": true}', encoding="utf-8")
        _powershell_file(paths.install_root / "uninstall.ps1")
        if paths.install_root.exists() or paths.shortcut.exists() or not paths.settings_file.exists():
            raise RuntimeError("normal uninstall did not remove only product files")
        _powershell_file(ROOT / "install.ps1", "-ArtifactPath", artifact, "-Sha256", checksum, "-ExpectedVersion", _release_version(artifact))
        _powershell_file(paths.install_root / "uninstall.ps1", "-PurgeSettings")
        if paths.install_root.exists() or paths.shortcut.exists() or paths.settings_file.exists():
            raise RuntimeError("purge uninstall did not remove the product settings file")
        if not sentinel.exists():
            raise RuntimeError("purge uninstall removed unrelated .codex data")
    finally:
        if paths.install_root.exists():
            _powershell_file(paths.install_root / "uninstall.ps1")
        sentinel.unlink(missing_ok=True)
        if prior_settings is None:
            paths.settings_file.unlink(missing_ok=True)
        else:
            paths.settings_file.write_bytes(prior_settings)
    return artifact


def main(arguments=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--result-file",
        type=Path,
        help="write structured success evidence after the lifecycle smoke passes",
    )
    options = parser.parse_args(arguments)
    artifact = installed_lifecycle_smoke()
    if options.result_file:
        options.result_file.parent.mkdir(parents=True, exist_ok=True)
        options.result_file.write_text(
            json.dumps({"artifact": str(artifact), "passed": True}) + "\n",
            encoding="utf-8",
        )
    print(f"installed lifecycle smoke passed: {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
