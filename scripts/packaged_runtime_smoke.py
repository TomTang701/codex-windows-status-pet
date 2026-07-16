"""Validate the source-based release package without importing the checkout."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path

from api.installer_contract_api import installation_paths
from api.release_artifact_api import RELEASE_ROOT_NAME, validate_release_archive
from package_smoke_test import app_version, static_package_smoke


@dataclass(frozen=True)
class ZipDirectUseBoundary:
    environment: dict[str, str]
    settings_file: Path
    install_root: Path
    desktop_shortcut: Path
    start_menu_shortcut: Path


def zip_direct_use_boundary(root, environment=None):
    root = Path(root)
    user_profile = root / "User"
    local_app_data = root / "Local"
    app_data = root / "Roaming"
    paths = installation_paths(local_app_data, user_profile)
    (user_profile / "Desktop").mkdir(parents=True, exist_ok=True)
    child_environment = dict(os.environ if environment is None else environment)
    child_environment.pop("PYTHONPATH", None)
    child_environment.update({
        "USERPROFILE": str(user_profile),
        "LOCALAPPDATA": str(local_app_data),
        "APPDATA": str(app_data),
    })
    return ZipDirectUseBoundary(
        environment=child_environment,
        settings_file=paths.settings_file,
        install_root=paths.install_root,
        desktop_shortcut=user_profile / "Desktop" / "Codex Windows Status Pet.lnk",
        start_menu_shortcut=app_data / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Codex Windows Status Pet.lnk",
    )


def assert_zip_direct_use_exit(boundary, expected_settings):
    actual = json.loads(boundary.settings_file.read_text(encoding="utf-8"))
    for key, expected in expected_settings.items():
        if actual.get(key) != expected:
            raise RuntimeError(f"ZIP direct use changed existing product setting: {key}")
    if boundary.install_root.exists() or boundary.desktop_shortcut.exists() or boundary.start_menu_shortcut.exists():
        raise RuntimeError("ZIP inspection created installed state or shortcuts")


def source_entrypoint_compile(entrypoint):
    """Compile the extracted entrypoint with the selected test interpreter."""
    completed = subprocess.run(
        [sys.executable, "-m", "py_compile", str(entrypoint)],
        cwd=entrypoint.parent.parent,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise RuntimeError(completed.stderr or "source entrypoint compilation failed")


def packaged_runtime_smoke():
    if sys.platform != "win32":
        raise RuntimeError("source runtime smoke requires Windows")
    artifact = static_package_smoke(channel="source")
    version = app_version()
    validate_release_archive(artifact, expected_version=version, expected_channel="source")
    with tempfile.TemporaryDirectory(prefix="CodexStatusPet-runtime-") as directory:
        root = Path(directory)
        boundary = zip_direct_use_boundary(root)
        boundary.settings_file.parent.mkdir(parents=True)
        expected_settings = {"schema_version": 1, "x": 30, "y": 120, "language": "zh-CN"}
        boundary.settings_file.write_text(json.dumps(expected_settings) + "\n", encoding="utf-8")
        extraction = root / "extract"
        with zipfile.ZipFile(artifact) as archive:
            archive.extractall(extraction)
        package_root = extraction / RELEASE_ROOT_NAME
        entrypoint = package_root / "scripts" / "codex_status_pet.py"
        names = [path.relative_to(package_root).as_posix() for path in package_root.rglob("*") if path.is_file()]
        if any(name.endswith((".exe", ".pyc", ".pyo")) for name in names):
            raise RuntimeError("source package contains executable or bytecode material")
        source_entrypoint_compile(entrypoint)
        assert_zip_direct_use_exit(boundary, expected_settings)
    return artifact


def main():
    artifact = packaged_runtime_smoke()
    print(f"source runtime smoke passed: {artifact}")


if __name__ == "__main__":
    main()
