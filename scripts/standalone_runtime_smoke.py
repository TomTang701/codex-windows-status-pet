"""Launch the extracted Standalone EXE with Python removed from its PATH."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

from api.release_artifact_api import RELEASE_ROOT_NAME, STANDALONE_CHANNEL, validate_release_archive
from package_smoke_test import app_version, static_package_smoke


ROOT = Path(__file__).resolve().parents[1]


def standalone_environment(environment=None):
    """Return a child environment which cannot resolve a system Python command."""
    environment = dict(os.environ if environment is None else environment)
    environment.pop("PYTHONHOME", None)
    environment.pop("PYTHONPATH", None)
    system_root = Path(environment.get("SystemRoot", os.environ["SystemRoot"]))
    environment["PATH"] = os.pathsep.join((str(system_root / "System32"), str(system_root)))
    return environment


def cleanup_directory(directory):
    for _ in range(20):
        try:
            shutil.rmtree(directory)
            return
        except PermissionError:
            time.sleep(0.5)
    shutil.rmtree(directory)


def standalone_runtime_smoke():
    if sys.platform != "win32":
        raise RuntimeError("standalone runtime smoke requires Windows")
    artifact = static_package_smoke(channel=STANDALONE_CHANNEL)
    validate_release_archive(artifact, expected_version=app_version(), expected_channel=STANDALONE_CHANNEL)
    directory = tempfile.mkdtemp(prefix="CodexStatusPet-standalone-")
    try:
        extraction = Path(directory) / "extract"
        with zipfile.ZipFile(artifact) as archive:
            archive.extractall(extraction)
        executable = extraction / RELEASE_ROOT_NAME / "CodexStatusPet.exe"
        if not executable.is_file():
            raise RuntimeError("standalone executable is missing after extraction")
        process = subprocess.Popen([str(executable)], cwd=executable.parent, env=standalone_environment())
        try:
            time.sleep(2)
            if process.poll() is not None:
                raise RuntimeError(f"standalone executable exited during direct launch: {process.returncode}")
        finally:
            if process.poll() is None:
                subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"], check=False, capture_output=True)
                process.wait(timeout=10)
    finally:
        cleanup_directory(directory)
    return artifact


def main():
    artifact = standalone_runtime_smoke()
    print(f"standalone runtime smoke passed: {artifact}")


if __name__ == "__main__":
    main()
