"""Pure naming and validation for the two Windows release channels."""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


RELEASE_ROOT_NAME = "CodexStatusPet"
STANDALONE_CHANNEL = "standalone"
SOURCE_CHANNEL = "source"
CHANNELS = frozenset({STANDALONE_CHANNEL, SOURCE_CHANNEL})
SOURCE_ENTRYPOINT = "scripts/codex_status_pet.py"
STANDALONE_ENTRYPOINT = "CodexStatusPet.exe"
SOURCE_REQUIRED_FILES = frozenset({
    SOURCE_ENTRYPOINT,
    "launch.vbs",
    "launch.ps1",
    "launch.cmd",
    "install.ps1",
    "uninstall.ps1",
    "requirements-runtime.txt",
    "release-manifest.json",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "assets/CodexStatusPet.ico",
})
STANDALONE_REQUIRED_FILES = frozenset({
    STANDALONE_ENTRYPOINT,
    "release-manifest.json",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "uninstall.ps1",
    "assets/CodexStatusPet.ico",
})
COMMON_PROHIBITED_PARTS = frozenset({
    "tests", "docs", "Goal", "skills", ".git", ".github", ".githooks",
    ".codex-plugin", ".build", "__pycache__",
})
PINNED_RUNTIME_REQUIREMENTS = "Pillow==12.2.0\npystray==0.19.5\n"


@dataclass(frozen=True)
class ReleaseManifest:
    version: str
    runtime: str = "python"
    entrypoint: str = SOURCE_ENTRYPOINT
    launcher: str = "launch.vbs"
    icon: str = "assets/CodexStatusPet.ico"


def normalize_channel(channel):
    normalized = str(channel).lower()
    if normalized not in CHANNELS:
        raise ValueError("release channel is invalid")
    return normalized


def release_archive_name(version, *, channel=STANDALONE_CHANNEL):
    channel = normalize_channel(channel)
    source_suffix = "-source" if channel == SOURCE_CHANNEL else ""
    return f"CodexStatusPet-v{version}{source_suffix}-win11-x64.zip"


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _channel_from_archive_name(name, version):
    for channel in (STANDALONE_CHANNEL, SOURCE_CHANNEL):
        if name == release_archive_name(version, channel=channel):
            return channel
    raise ValueError("release archive name is invalid")


def validate_release_archive(artifact, *, expected_version, expected_channel=None):
    artifact = Path(artifact)
    channel = (
        normalize_channel(expected_channel)
        if expected_channel is not None
        else _channel_from_archive_name(artifact.name, expected_version)
    )
    if artifact.name != release_archive_name(expected_version, channel=channel):
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
                    expected_channel=channel,
                )
    except zipfile.BadZipFile as exc:
        raise ValueError("release archive is invalid") from exc


def _read_manifest(root):
    try:
        return json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("invalid release manifest") from exc


def _manifest_channel(payload):
    if payload.get("schema_version") == 1 and payload.get("entrypoint") == STANDALONE_ENTRYPOINT:
        return STANDALONE_CHANNEL
    if payload.get("schema_version") == 2 and payload.get("runtime") == "python":
        return SOURCE_CHANNEL
    raise ValueError("release manifest channel is invalid")


def _validate_common_manifest(payload, expected_version):
    for key, expected in {
        "product": "codex-windows-status-pet",
        "display_name": "Codex Windows Status Pet",
        "version": expected_version,
        "platform": "windows",
        "arch": "x64",
    }.items():
        if payload.get(key) != expected:
            raise ValueError(f"release manifest {key} is invalid")


def validate_release_root(root, *, expected_version, expected_channel=None):
    root = Path(root)
    payload = _read_manifest(root)
    channel = _manifest_channel(payload)
    if expected_channel is not None and channel != normalize_channel(expected_channel):
        raise ValueError("release manifest channel is invalid")

    required_files = SOURCE_REQUIRED_FILES if channel == SOURCE_CHANNEL else STANDALONE_REQUIRED_FILES
    missing = [name for name in required_files if not (root / name).is_file()]
    if missing:
        raise ValueError("missing required runtime files: " + ", ".join(sorted(missing)))
    if channel == STANDALONE_CHANNEL:
        internal = root / "_internal"
        if not internal.is_dir() or not any(path.is_file() for path in internal.rglob("*")):
            raise ValueError("standalone runtime material is missing")

    prohibited = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        parts = relative.parts
        if any(part in COMMON_PROHIBITED_PARTS for part in parts):
            prohibited.append(relative.as_posix())
        if channel == SOURCE_CHANNEL and path.is_file() and (
            path.suffix.lower() in {".exe", ".pyc", ".pyo"}
            or path.name.lower().startswith("python") and path.suffix.lower() != ".py"
            or "_internal" in parts
        ):
            prohibited.append(relative.as_posix())
    if prohibited:
        raise ValueError("prohibited release material: " + ", ".join(sorted(set(prohibited))))

    _validate_common_manifest(payload, expected_version)
    if channel == SOURCE_CHANNEL:
        required = {
            "schema_version": 2,
            "runtime": "python",
            "minimum_python": "3.10",
            "entrypoint": SOURCE_ENTRYPOINT,
            "launcher": "launch.vbs",
            "icon": "assets/CodexStatusPet.ico",
        }
        if (root / "requirements-runtime.txt").read_text(encoding="utf-8") != PINNED_RUNTIME_REQUIREMENTS:
            raise ValueError("runtime requirements are not pinned to the tested versions")
    else:
        required = {
            "schema_version": 1,
            "entrypoint": STANDALONE_ENTRYPOINT,
        }
    for key, expected in required.items():
        if payload.get(key) != expected:
            raise ValueError(f"release manifest {key} is invalid")
    return ReleaseManifest(
        version=payload["version"],
        runtime="standalone" if channel == STANDALONE_CHANNEL else payload["runtime"],
        entrypoint=payload["entrypoint"],
        launcher=payload.get("launcher", ""),
        icon=payload.get("icon", "assets/CodexStatusPet.ico"),
    )
