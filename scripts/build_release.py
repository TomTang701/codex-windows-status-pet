"""Build the sole distributable Windows onedir release artifact."""

from __future__ import annotations

import importlib.metadata
import json
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from api.release_artifact_api import RELEASE_ROOT_NAME, release_archive_name, sha256_file, validate_release_root


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
PYINSTALLER_DIST = BUILD / "pyinstaller-dist"
PYINSTALLER_WORK = BUILD / "pyinstaller-work"
RELEASE = BUILD / "release"


def app_version():
    namespace = {}
    exec((ROOT / "scripts" / "ui" / "main_window.py").read_text(encoding="utf-8").split("try:", 1)[0], namespace)
    return namespace["APP_VERSION"]


def require_windows_x64():
    if sys.platform != "win32" or platform.machine().upper() not in {"AMD64", "X86_64"}:
        raise SystemExit("release builds require Windows x64")


def verify_build_dependencies():
    required = {"pyinstaller": "6.16.0", "pillow": "12.2.0", "pystray": "0.19.5"}
    for package, expected in required.items():
        actual = importlib.metadata.version(package)
        if actual != expected:
            raise SystemExit(f"{package} must be {expected}; found {actual}")


def write_manifest(root, version):
    (root / "release-manifest.json").write_text(json.dumps({
        "schema_version": 1,
        "product": "codex-windows-status-pet",
        "display_name": "Codex Windows Status Pet",
        "version": version,
        "platform": "windows",
        "arch": "x64",
        "entrypoint": "CodexStatusPet.exe",
    }, indent=2) + "\n", encoding="utf-8")


def clean_build_paths(paths):
    """Clean only project-owned staging paths or fail before a costly build."""
    for path in paths:
        shutil.rmtree(path, ignore_errors=True)
        if Path(path).exists():
            raise RuntimeError(
                f"release staging path is in use: {path}; close the packaged test instance and retry"
            )


def zip_runtime(runtime, artifact):
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(runtime.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(runtime.parent).as_posix())


def main():
    require_windows_x64()
    version = app_version()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "check_version_sources.py")], check=True)
    verify_build_dependencies()
    clean_build_paths((PYINSTALLER_DIST, PYINSTALLER_WORK, RELEASE))
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--distpath", str(PYINSTALLER_DIST), "--workpath", str(PYINSTALLER_WORK),
        str(ROOT / "packaging" / "CodexStatusPet.spec"),
    ], cwd=ROOT, check=True)
    runtime = RELEASE / RELEASE_ROOT_NAME
    shutil.copytree(PYINSTALLER_DIST / RELEASE_ROOT_NAME, runtime)
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md", "uninstall.ps1"):
        shutil.copy2(ROOT / name, runtime / name)
    write_manifest(runtime, version)
    validate_release_root(runtime, expected_version=version)
    artifact = RELEASE / release_archive_name(version)
    zip_runtime(runtime, artifact)
    checksum = sha256_file(artifact)
    sidecar = artifact.with_suffix(artifact.suffix + ".sha256")
    sidecar.write_text(f"{checksum}  {artifact.name}\n", encoding="ascii")
    print(f"artifact={artifact}")
    print(f"sha256={checksum}")


if __name__ == "__main__":
    main()
