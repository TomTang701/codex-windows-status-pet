"""Exercise public-release bootstrap without allowing GitHub CLI access."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


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


def _write_failing_gh_probe(directory):
    command = directory / "gh.cmd"
    command.write_text(
        "@echo off\r\n"
        "echo unexpected gh invocation 1>&2\r\n"
        "exit /b 97\r\n",
        encoding="ascii",
    )


def release_bootstrap_smoke():
    """Prove bootstrap acquisition, installation, and cleanup stay product-scoped."""
    if sys.platform != "win32":
        raise RuntimeError("release bootstrap smoke requires Windows")
    with tempfile.TemporaryDirectory(prefix="CodexStatusPet-bootstrap-") as temporary:
        root = Path(temporary)
        fake_bin = root / "fake-bin"
        fake_bin.mkdir()
        _write_failing_gh_probe(fake_bin)
        user = root / "User"
        sentinel = user / ".codex/unrelated-sentinel.txt"
        sentinel.parent.mkdir(parents=True)
        sentinel.write_text("preserve", encoding="utf-8")
        environment = dict(os.environ)
        environment.update({
            "PATH": str(fake_bin) + os.pathsep + environment["PATH"],
            "LOCALAPPDATA": str(root / "Local"),
            "APPDATA": str(root / "Roaming"),
            "USERPROFILE": str(user),
            "HOMEDRIVE": user.drive,
            "HOMEPATH": str(user)[len(user.drive):],
        })
        _powershell(ROOT / "scripts/install_release.ps1", "-Tag", "v0.9.0", environment=environment)
        install_root = Path(environment["LOCALAPPDATA"]) / "Programs/CodexStatusPet"
        shortcut = Path(environment["APPDATA"]) / "Microsoft/Windows/Start Menu/Programs/Codex Windows Status Pet.lnk"
        if not (install_root / "CodexStatusPet.exe").is_file() or not shortcut.is_file():
            raise RuntimeError("bootstrap did not create the installed executable and Start Menu shortcut")
        _powershell(install_root / "uninstall.ps1", "-PurgeSettings", environment=environment)
        if install_root.exists() or shortcut.exists() or not sentinel.is_file():
            raise RuntimeError("bootstrap lifecycle cleanup crossed the product data boundary")
    return "CodexStatusPet-v0.9.0-win11-x64.zip"


def main():
    artifact = release_bootstrap_smoke()
    print(f"release bootstrap smoke passed: {artifact}")


if __name__ == "__main__":
    main()
