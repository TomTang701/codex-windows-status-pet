"""Build the lightweight source-based Windows release artifact."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

from api.release_artifact_api import RELEASE_ROOT_NAME, release_archive_name, sha256_file, validate_release_root


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
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


def write_manifest(root, version):
    (root / "release-manifest.json").write_text(json.dumps({
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
    }, indent=2) + "\n", encoding="utf-8")


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
        for path in sorted(runtime.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(runtime.parent).as_posix())


def main():
    require_windows_x64()
    version = app_version()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "check_version_sources.py")], check=True)
    clean_build_paths((RELEASE,))
    runtime = RELEASE / RELEASE_ROOT_NAME
    runtime.mkdir(parents=True)
    copy_source_tree(ROOT, runtime)
    for name in ("LICENSE", "THIRD_PARTY_NOTICES.md", "install.ps1", "uninstall.ps1", "launch.ps1", "launch.vbs", "launch.cmd", "requirements-runtime.txt"):
        shutil.copy2(ROOT / name, runtime / name)
    shutil.copytree(ROOT / "assets", runtime / "assets")
    write_manifest(runtime, version)
    validate_release_root(runtime, expected_version=version)
    artifact = RELEASE / release_archive_name(version)
    zip_runtime(runtime, artifact)
    checksum = sha256_file(artifact)
    artifact.with_suffix(artifact.suffix + ".sha256").write_text(f"{checksum}  {artifact.name}\n", encoding="ascii")
    shutil.copy2(ROOT / "scripts" / "install_release.ps1", RELEASE / "CodexStatusPet-bootstrap.ps1")
    print(f"artifact={artifact}")
    print(f"sha256={checksum}")
    print(f"compressed_bytes={artifact.stat().st_size}")
    print(f"unpacked_bytes={sum(path.stat().st_size for path in runtime.rglob('*') if path.is_file())}")


if __name__ == "__main__":
    main()
