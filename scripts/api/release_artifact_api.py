"""Pure validation for the distributable Windows runtime root."""

from __future__ import annotations

import json
import hashlib
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path
from pathlib import PurePosixPath


RELEASE_ROOT_NAME = "CodexStatusPet"
ENTRYPOINT = "CodexStatusPet.exe"
REQUIRED_FILES = frozenset({
    ENTRYPOINT, "_internal", "release-manifest.json", "LICENSE",
    "THIRD_PARTY_NOTICES.md", "uninstall.ps1",
})
PROHIBITED_PARTS = frozenset({
    "tests", "docs", "Goal", "skills", ".github", ".githooks",
    ".codex-plugin", ".build", "__pycache__",
})


@dataclass(frozen=True)
class ReleaseManifest:
    version: str


def release_archive_name(version):
    """Return the sole supported Windows x64 release archive name."""
    return f"CodexStatusPet-v{version}-win11-x64.zip"


def sha256_file(path):
    """Return a lowercase SHA-256 digest without loading an artifact at once."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_release_archive(artifact, *, expected_version):
    """Validate the signed-by-checksum ZIP boundary before installation."""
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
    """Validate the strict v0.8 onedir runtime contract and return its manifest."""
    root = Path(root)
    missing = [name for name in REQUIRED_FILES if not (root / name).exists()]
    if missing:
        raise ValueError("missing required runtime files: " + ", ".join(sorted(missing)))
    prohibited = [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if any(part in PROHIBITED_PARTS for part in path.relative_to(root).parts)
        or path.suffix == ".py"
    ]
    if prohibited:
        raise ValueError("prohibited release material: " + ", ".join(sorted(prohibited)))
    try:
        payload = json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("invalid release manifest") from exc
    required = {
        "schema_version": 1,
        "product": "codex-windows-status-pet",
        "display_name": "Codex Windows Status Pet",
        "version": expected_version,
        "platform": "windows",
        "arch": "x64",
        "entrypoint": ENTRYPOINT,
    }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise ValueError(f"release manifest {key} is invalid")
    return ReleaseManifest(version=payload["version"])
