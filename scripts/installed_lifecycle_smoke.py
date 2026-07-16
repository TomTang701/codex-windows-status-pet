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
import zipfile

from api.installer_contract_api import installation_paths
from api.release_artifact_api import validate_release_archive
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


def validate_legacy_upgrade_archive(artifact, expected_version):
    """Validate only the published v0.9.1 EXE baseline used for migration."""
    with zipfile.ZipFile(artifact) as archive:
        manifest = json.loads(archive.read("CodexStatusPet/release-manifest.json"))
        if (
            manifest.get("schema_version") != 1
            or manifest.get("product") != "codex-windows-status-pet"
            or manifest.get("version") != expected_version
            or manifest.get("entrypoint") != "CodexStatusPet.exe"
            or "CodexStatusPet/CodexStatusPet.exe" not in archive.namelist()
        ):
            raise RuntimeError("previous artifact is not the expected v0.9.1 EXE migration baseline")


def _install(artifact, *, test_fail_after_backup=False):
    arguments = [
        "-ArtifactPath", artifact,
        "-Sha256", _release_checksum(artifact),
        "-ExpectedVersion", _release_version(artifact),
    ]
    if test_fail_after_backup:
        arguments.append("-TestFailAfterBackup")
    _powershell_file(ROOT / "install.ps1", *arguments)


def _installed_manifest_version(install_root):
    return json.loads((install_root / "release-manifest.json").read_text(encoding="utf-8"))["version"]


def installed_lifecycle_smoke(*, previous_artifact=None):
    """Prove a real update, repair, rollback, and both uninstall scopes."""
    if sys.platform != "win32":
        raise RuntimeError("installed lifecycle smoke requires Windows")
    artifact = static_package_smoke()
    if previous_artifact is None:
        raise RuntimeError("installed lifecycle smoke requires --previous-artifact for a real upgrade")
    previous_artifact = Path(previous_artifact)
    previous_version = _release_version(previous_artifact)
    target_version = _release_version(artifact)
    if previous_version == target_version:
        raise RuntimeError("previous release must have a different version from the candidate")
    if previous_version == "0.9.1":
        validate_legacy_upgrade_archive(previous_artifact, previous_version)
    else:
        validate_release_archive(previous_artifact, expected_version=previous_version)
    paths = installed_lifecycle_paths(
        local_app_data=Path(os.environ["LOCALAPPDATA"]),
        app_data=Path(os.environ["APPDATA"]),
        user_profile=Path(os.environ["USERPROFILE"]),
    )
    ensure_clean_install_root(paths)
    sentinel = paths.settings_file.parent / f"codex-status-pet-lifecycle-{uuid.uuid4().hex}.sentinel"
    prior_settings = paths.settings_file.read_bytes() if paths.settings_file.exists() else None
    paths.settings_file.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text("unrelated Codex data", encoding="utf-8")
    try:
        _install(previous_artifact)
        executable = paths.install_root / "CodexStatusPet.exe"
        if not executable.is_file() or not paths.shortcut.is_file():
            raise RuntimeError("installed product executable or Start Menu shortcut is missing")
        if not _installed_process_is_running(executable):
            raise RuntimeError("installed executable did not remain running")
        if _installed_manifest_version(paths.install_root) != previous_version:
            raise RuntimeError("initial installation does not retain the prior release provenance")
        expected_settings = b'{\n  "lifecycle_smoke": true,\n  "x": 4151\n}\n'
        paths.settings_file.write_bytes(expected_settings)

        _install(artifact)
        if _installed_manifest_version(paths.install_root) != target_version:
            raise RuntimeError("upgrade did not install the candidate manifest version")
        if paths.settings_file.read_bytes() != expected_settings or not sentinel.exists():
            raise RuntimeError("upgrade did not preserve settings bytes and unrelated Codex data")

        _install(artifact)
        if _installed_manifest_version(paths.install_root) != target_version or paths.settings_file.read_bytes() != expected_settings:
            raise RuntimeError("same-version repair did not preserve the installed release and settings bytes")

        try:
            _install(artifact, test_fail_after_backup=True)
        except subprocess.CalledProcessError:
            pass
        else:
            raise RuntimeError("test replacement failure unexpectedly installed")
        if (_installed_manifest_version(paths.install_root) != target_version
                or paths.settings_file.read_bytes() != expected_settings):
            raise RuntimeError("failed replacement did not restore the prior installed runtime and settings")
        if list(paths.install_root.parent.glob("CodexStatusPet.backup-*")):
            raise RuntimeError("failed replacement left stale backup state")

        _powershell_file(paths.install_root / "uninstall.ps1")
        if paths.install_root.exists() or paths.shortcut.exists() or not paths.settings_file.exists():
            raise RuntimeError("normal uninstall did not remove only product files")
        if paths.settings_file.read_bytes() != expected_settings:
            raise RuntimeError("normal uninstall did not preserve settings bytes")
        _install(artifact)
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
        "--previous-artifact",
        type=Path,
        help="a verified earlier release ZIP used to exercise a real upgrade transaction",
    )
    parser.add_argument(
        "--result-file",
        type=Path,
        help="write structured success evidence after the lifecycle smoke passes",
    )
    options = parser.parse_args(arguments)
    artifact = installed_lifecycle_smoke(previous_artifact=options.previous_artifact)
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
