"""Pure validation for the lightweight source-based Windows release."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath


RELEASE_ROOT_NAME = "CodexStatusPet"
ENTRYPOINT = "scripts/codex_status_pet.py"
REQUIRED_FILES = frozenset({
    ENTRYPOINT,
    "launch.vbs",
    "launch.ps1",
    "install.ps1",
    "uninstall.ps1",
    "requirements-runtime.txt",
    "release-manifest.json",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "assets/CodexStatusPet.ico",
})
PROHIBITED_PARTS = frozenset({
    "tests", "docs", "Goal", "skills", ".git", ".github", ".githooks",
    ".codex-plugin", ".build", "__pycache__", "_internal",
})
PINNED_RUNTIME_REQUIREMENTS = "Pillow==12.2.0\npystray==0.19.5\n"


@dataclass(frozen=True)
class ReleaseManifest:
    version: str
    runtime: str = "python"
    entrypoint: str = ENTRYPOINT
    launcher: str = "launch.vbs"
    icon: str = "assets/CodexStatusPet.ico"


def release_archive_name(version):
    return f"CodexStatusPet-v{version}-win11-x64.zip"


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_release_archive(artifact, *, expected_version):
    artifact = Path(artifact)
    expected_name = release_archive_name(expected_version)
    if artifact.name != expected_name:
        raise ValueError("release archive name is invalid")
    sidecar = artifact.with_suffix(artifact.suffix + ".sha256")
    try:
        checksum_record = sidecar.read_text(encoding="ascii").strip()
    except OSError as exc:
        raise ValueError("release checksum sidecar is missing") from exc
    match = re.fullmatch(r"([0-9a-f]{64})  (.+)", checksum_record)
    if match is None or match.group(2) != artifact.name:
        raise ValueError("release checksum sidecar is invalid")
    if sha256_file(artifact) != match.group(1):
        raise ValueError("release checksum does not match")
    try:
        with zipfile.ZipFile(artifact) as archive:
            files = [entry.filename for entry in archive.infolist() if not entry.is_dir()]
            for name in files:
                path = PurePosixPath(name)
                if (
                    "\\" in name
                    or path.is_absolute()
                    or ".." in path.parts
                    or len(path.parts) < 2
                    or path.parts[0] != RELEASE_ROOT_NAME
                ):
                    raise ValueError("release archive must contain one runtime root")
            with tempfile.TemporaryDirectory() as directory:
                archive.extractall(directory)
                return validate_release_root(
                    Path(directory) / RELEASE_ROOT_NAME,
                    expected_version=expected_version,
                )
    except zipfile.BadZipFile as exc:
        raise ValueError("release archive is invalid") from exc


def validate_release_root(root, *, expected_version):
    root = Path(root)
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        raise ValueError("missing required runtime files: " + ", ".join(sorted(missing)))
    prohibited = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        parts = relative.parts
        if any(part in PROHIBITED_PARTS for part in parts):
            prohibited.append(relative.as_posix())
        if path.is_file() and (path.suffix.lower() in {".exe", ".pyc", ".pyo"} or (path.name.lower().startswith("python") and path.suffix.lower() != ".py")):
            prohibited.append(relative.as_posix())
    if prohibited:
        raise ValueError("prohibited release material: " + ", ".join(sorted(set(prohibited))))
    try:
        payload = json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("invalid release manifest") from exc
    required = {
        "schema_version": 2,
        "product": "codex-windows-status-pet",
        "display_name": "Codex Windows Status Pet",
        "version": expected_version,
        "platform": "windows",
        "arch": "x64",
        "runtime": "python",
        "minimum_python": "3.10",
        "entrypoint": ENTRYPOINT,
        "launcher": "launch.vbs",
        "icon": "assets/CodexStatusPet.ico",
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise ValueError(f"release manifest {key} is invalid")
    if (root / "requirements-runtime.txt").read_text(encoding="utf-8") != PINNED_RUNTIME_REQUIREMENTS:
        raise ValueError("runtime requirements are not pinned to the tested versions")
    return ReleaseManifest(
        version=payload["version"],
        runtime=payload["runtime"],
        entrypoint=payload["entrypoint"],
        launcher=payload["launcher"],
        icon=payload["icon"],
    )
