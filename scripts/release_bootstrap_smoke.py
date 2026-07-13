"""Exercise authenticated-release bootstrap with a test-owned fake GitHub CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from api.release_artifact_api import release_archive_name


ROOT = Path(__file__).resolve().parents[1]


def _powershell(script, *arguments, environment):
    executable = Path(os.environ["SystemRoot"]) / "System32/WindowsPowerShell/v1.0/powershell.exe"
    return subprocess.run(
        [str(executable), "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script), *map(str, arguments)],
        text=True,
        capture_output=True,
        check=True,
        env=environment,
    )


def _version():
    namespace = {}
    exec((ROOT / "scripts/ui/main_window.py").read_text(encoding="utf-8").split("try:", 1)[0], namespace)
    return namespace["APP_VERSION"]


def _write_fake_gh(directory, release_directory, version):
    metadata = directory / "release.json"
    zip_name = release_archive_name(version)
    metadata.write_text(json.dumps({
        "tagName": f"v{version}", "isDraft": False, "isPrerelease": False,
        "assets": [{"name": name} for name in (zip_name, f"{zip_name}.sha256", "install.ps1")],
    }), encoding="utf-8")
    command = directory / "gh.cmd"
    command.write_text(
        "@echo off\r\n"
        "if /I \"%~1\"==\"auth\" exit /b 0\r\n"
        "if /I \"%~1\"==\"release\" if /I \"%~2\"==\"view\" (type \"%FAKE_RELEASE_JSON%\" & exit /b 0)\r\n"
        "if /I \"%~1\"==\"release\" if /I \"%~2\"==\"download\" goto download\r\n"
        "exit /b 1\r\n"
        ":download\r\n"
        "set \"destination=\"\r\n"
        ":args\r\n"
        "if \"%~1\"==\"\" goto copied\r\n"
        "if /I \"%~1\"==\"--dir\" (set \"destination=%~2\" & shift & shift & goto args)\r\n"
        "shift\r\n"
        "goto args\r\n"
        ":copied\r\n"
        "if \"%destination%\"==\"\" exit /b 1\r\n"
        "copy /Y \"%FAKE_RELEASE_DIR%\\*\" \"%destination%\\\" >nul\r\n"
        "exit /b 0\r\n",
        encoding="ascii",
    )
    return metadata


def release_bootstrap_smoke():
    """Prove bootstrap acquisition, installation, and cleanup stay product-scoped."""
    if sys.platform != "win32":
        raise RuntimeError("release bootstrap smoke requires Windows")
    version = _version()
    release = ROOT / ".build/release"
    zip_name = release_archive_name(version)
    required = (release / zip_name, release / f"{zip_name}.sha256", release / "install.ps1")
    if not all(path.is_file() for path in required):
        raise RuntimeError("release bootstrap smoke requires a current built ZIP, checksum, and installer")
    with tempfile.TemporaryDirectory(prefix="CodexStatusPet-bootstrap-") as temporary:
        root = Path(temporary)
        assets = root / "assets"
        assets.mkdir()
        for path in required:
            shutil.copy2(path, assets / path.name)
        fake_bin = root / "fake-bin"
        fake_bin.mkdir()
        metadata = _write_fake_gh(fake_bin, assets, version)
        user = root / "User"
        sentinel = user / ".codex/unrelated-sentinel.txt"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text("preserve", encoding="utf-8")
        environment = dict(os.environ)
        environment.update({
            "PATH": str(fake_bin) + os.pathsep + environment["PATH"],
            "FAKE_RELEASE_DIR": str(assets),
            "FAKE_RELEASE_JSON": str(metadata),
            "LOCALAPPDATA": str(root / "Local"),
            "APPDATA": str(root / "Roaming"),
            "USERPROFILE": str(user),
            "HOMEDRIVE": user.drive,
            "HOMEPATH": str(user)[len(user.drive):],
        })
        _powershell(ROOT / "scripts/install_release.ps1", "-Tag", f"v{version}", environment=environment)
        install_root = Path(environment["LOCALAPPDATA"]) / "Programs/CodexStatusPet"
        shortcut = Path(environment["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Codex Windows Status Pet.lnk"
        if not (install_root / "CodexStatusPet.exe").is_file() or not shortcut.is_file():
            raise RuntimeError("bootstrap did not create the installed executable and Start Menu shortcut")
        _powershell(install_root / "uninstall.ps1", "-PurgeSettings", environment=environment)
        if install_root.exists() or shortcut.exists() or not sentinel.is_file():
            raise RuntimeError("bootstrap lifecycle cleanup crossed the product data boundary")
    return zip_name


def main():
    artifact = release_bootstrap_smoke()
    print(f"release bootstrap smoke passed: {artifact}")


if __name__ == "__main__":
    main()
