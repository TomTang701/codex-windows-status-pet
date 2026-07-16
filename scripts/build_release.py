"""Build the Standalone and Source Windows release artifacts once each."""

from __future__ import annotations

import importlib.metadata
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from api.release_artifact_api import (
    RELEASE_ROOT_NAME,
    SOURCE_CHANNEL,
    STANDALONE_CHANNEL,
    release_archive_name,
    sha256_file,
    validate_release_root,
)


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
PYINSTALLER_DIST = BUILD / "pyinstaller-dist"
PYINSTALLER_WORK = BUILD / "pyinstaller-work"
SOURCE_STAGE = BUILD / "source-release"
STANDALONE_STAGE = BUILD / "standalone-release"
RELEASE = BUILD / "release"
SOURCE_EXCLUDES = {"tests", "docs", "Goal", "skills", ".git", ".github", ".build", "__pycache__"}


def app_version():
    namespace = {}
    text = (ROOT / "scripts" / "ui" / "main_window.py").read_text(encoding="utf-8")
    exec(text.split("try:", 1)[0], namespace)
    return namespace["APP_VERSION"]


def require_windows_x64():
    import platform

    if sys.platform != "win32" or platform.machine().upper() not in {"AMD64", "X86_64"}:
        raise SystemExit("release builds require Windows x64")


def verify_build_dependencies():
    for package, expected in {"pyinstaller": "6.16.0", "pillow": "12.2.0", "pystray": "0.19.5"}.items():
        actual = importlib.metadata.version(package)
        if actual != expected:
            raise SystemExit(f"{package} must be {expected}; found {actual}")


def release_artifact_paths(version):
    return {
        STANDALONE_CHANNEL: RELEASE / release_archive_name(version, channel=STANDALONE_CHANNEL),
        SOURCE_CHANNEL: RELEASE / release_archive_name(version, channel=SOURCE_CHANNEL),
    }


def write_manifest(root, version, *, channel):
    if channel == SOURCE_CHANNEL:
        manifest = {
            "schema_version": 2,
            "product": "codex-windows-status-pet",
            "display_name": "Codex Windows Status Pet",
            "version": version,
            "platform": "windows",
            "arch": "x64",
            "runtime": "python",
            "minimum_python": "3.10",
            "entrypoint": "scripts/codex_status_pet.py",
            "launcher": "launch.vbs",
            "icon": "assets/CodexStatusPet.ico",
        }
    elif channel == STANDALONE_CHANNEL:
        manifest = {
            "schema_version": 1,
            "product": "codex-windows-status-pet",
            "display_name": "Codex Windows Status Pet",
            "version": version,
            "platform": "windows",
            "arch": "x64",
            "entrypoint": "CodexStatusPet.exe",
        }
    else:
        raise ValueError("release channel is invalid")
    (Path(root) / "release-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def clean_build_paths(paths):
    for path in paths:
        shutil.rmtree(path, ignore_errors=True)
        if Path(path).exists():
            raise RuntimeError(f"release staging path is in use: {path}; close the packaged test instance and retry")


def copy_source_tree(source, runtime):
    source, runtime = Path(source), Path(runtime)
    allowed = [source / "scripts" / "codex_status_pet.py", source / "scripts" / "api", source / "scripts" / "ui"]
    for base in allowed:
        paths = [base] if base.is_file() else base.rglob("*")
        for path in paths:
            relative = path.relative_to(source)
            if any(part in SOURCE_EXCLUDES for part in relative.parts):
                continue
            target = runtime / relative
            if path.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            elif path.suffix.lower() not in {".pyc", ".pyo"}:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, target)


def zip_runtime(runtime, artifact):
    with zipfile.ZipFile(artifact, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(Path(runtime).rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(Path(runtime).parent).as_posix())


def build_source_runtime(version):
    runtime = SOURCE_STAGE / RELEASE_ROOT_NAME
    runtime.mkdir(parents=True)
    copy_source_tree(ROOT, runtime)
    for name in (
        "LICENSE", "THIRD_PARTY_NOTICES.md", "install.ps1", "uninstall.ps1",
        "launch.ps1", "launch.vbs", "launch.cmd", "requirements-runtime.txt",
    ):
        shutil.copy2(ROOT / name, runtime / name)
    shutil.copytree(ROOT / "assets", runtime / "assets")
    write_manifest(runtime, version, channel=SOURCE_CHANNEL)
    validate_release_root(runtime, expected_version=version, expected_channel=SOURCE_CHANNEL)
    return runtime


def build_standalone_runtime(version):
    subprocess.run([
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
        "--distpath", str(PYINSTALLER_DIST), "--workpath", str(PYINSTALLER_WORK),
        str(ROOT / "packaging" / "CodexStatusPet.spec"),
    ], cwd=ROOT, check=True)
    runtime = STANDALONE_STAGE / RELEASE_ROOT_NAME
    shutil.copytree(PYINSTALLER_DIST / RELEASE_ROOT_NAME, runtime)
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md", "uninstall.ps1"):
        shutil.copy2(ROOT / name, runtime / name)
    shutil.copytree(ROOT / "assets", runtime / "assets", dirs_exist_ok=True)
    write_manifest(runtime, version, channel=STANDALONE_CHANNEL)
    validate_release_root(runtime, expected_version=version, expected_channel=STANDALONE_CHANNEL)
    return runtime


def write_artifact(runtime, artifact):
    zip_runtime(runtime, artifact)
    checksum = sha256_file(artifact)
    artifact.with_suffix(artifact.suffix + ".sha256").write_text(
        f"{checksum}  {artifact.name}\n", encoding="ascii"
    )
    return checksum


def main():
    require_windows_x64()
    version = app_version()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "check_version_sources.py")], check=True)
    verify_build_dependencies()
    clean_build_paths((PYINSTALLER_DIST, PYINSTALLER_WORK, SOURCE_STAGE, STANDALONE_STAGE, RELEASE))
    RELEASE.mkdir(parents=True)

    runtimes = {
        STANDALONE_CHANNEL: build_standalone_runtime(version),
        SOURCE_CHANNEL: build_source_runtime(version),
    }
    artifacts = release_artifact_paths(version)
    checksums = {
        channel: write_artifact(runtime, artifacts[channel])
        for channel, runtime in runtimes.items()
    }
    shutil.copy2(ROOT / "scripts" / "install_release.ps1", RELEASE / "CodexStatusPet-bootstrap.ps1")
    shutil.copy2(ROOT / "install.ps1", RELEASE / "install.ps1")
    for channel, artifact in artifacts.items():
        print(f"{channel}_artifact={artifact}")
        print(f"{channel}_sha256={checksums[channel]}")
        print(f"{channel}_compressed_bytes={artifact.stat().st_size}")
        runtime = runtimes[channel]
        print(f"{channel}_unpacked_bytes={sum(path.stat().st_size for path in runtime.rglob('*') if path.is_file())}")


if __name__ == "__main__":
    main()
