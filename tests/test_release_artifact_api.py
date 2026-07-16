import json
import zipfile
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.release_artifact_api import (
    RELEASE_ROOT_NAME,
    ReleaseManifest,
    release_archive_name,
    sha256_file,
    validate_release_archive,
    validate_release_root,
)


class ReleaseArtifactTests(unittest.TestCase):
    def write_runtime_root(self, root, *, manifest=None):
        runtime = root / RELEASE_ROOT_NAME
        (runtime / "scripts").mkdir(parents=True)
        (runtime / "assets").mkdir()
        (runtime / "scripts" / "codex_status_pet.py").write_text("entry", encoding="utf-8")
        (runtime / "launch.vbs").write_text("launcher", encoding="utf-8")
        (runtime / "launch.ps1").write_text("launcher", encoding="utf-8")
        (runtime / "launch.cmd").write_text("@echo off", encoding="utf-8")
        (runtime / "install.ps1").write_text("installer", encoding="utf-8")
        (runtime / "uninstall.ps1").write_text("uninstaller", encoding="utf-8")
        (runtime / "requirements-runtime.txt").write_text("Pillow==12.2.0\npystray==0.19.5\n", encoding="utf-8")
        (runtime / "assets" / "CodexStatusPet.ico").write_bytes(b"ico")
        (runtime / "LICENSE").write_text("MIT", encoding="utf-8")
        (runtime / "THIRD_PARTY_NOTICES.md").write_text("notices", encoding="utf-8")
        (runtime / "release-manifest.json").write_text(json.dumps(manifest or {
            "schema_version": 2,
            "product": "codex-windows-status-pet",
            "display_name": "Codex Windows Status Pet",
            "version": "1.0.0",
            "platform": "windows",
            "arch": "x64",
            "runtime": "python",
            "minimum_python": "3.10",
            "entrypoint": "scripts/codex_status_pet.py",
            "launcher": "launch.vbs",
            "icon": "assets/CodexStatusPet.ico",
        }), encoding="utf-8")
        return runtime

    def test_valid_source_root_returns_typed_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = validate_release_root(self.write_runtime_root(Path(directory)), expected_version="1.0.0")
        self.assertEqual(manifest, ReleaseManifest("1.0.0"))

    def test_source_root_rejects_executable_and_development_material(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = self.write_runtime_root(Path(directory))
            (runtime / "CodexStatusPet.exe").write_bytes(b"exe")
            with self.assertRaisesRegex(ValueError, "prohibited"):
                validate_release_root(runtime, expected_version="1.0.0")

    def test_release_archive_name_and_sha256_are_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            artifact = Path(directory) / release_archive_name("1.0.0")
            artifact.write_bytes(b"CodexStatusPet")
            self.assertEqual(artifact.name, "CodexStatusPet-v1.0.0-win11-x64.zip")
            self.assertEqual(sha256_file(artifact), "d97973705307089bea79cbed5fe81f5eaeb2fe9d6c72b3e9137493f0056979a4")

    def test_release_archive_validates_checksum_and_single_source_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runtime = self.write_runtime_root(root)
            artifact = root / release_archive_name("1.0.0")
            with zipfile.ZipFile(artifact, "w") as archive:
                for path in runtime.rglob("*"):
                    if path.is_file():
                        archive.write(path, path.relative_to(root).as_posix())
            artifact.with_suffix(artifact.suffix + ".sha256").write_text(f"{sha256_file(artifact)}  {artifact.name}\n", encoding="ascii")
            self.assertEqual(validate_release_archive(artifact, expected_version="1.0.0"), ReleaseManifest("1.0.0"))

            with zipfile.ZipFile(artifact, "a") as archive:
                archive.writestr("README.md", "not a runtime file")
            artifact.with_suffix(artifact.suffix + ".sha256").write_text(f"{sha256_file(artifact)}  {artifact.name}\n", encoding="ascii")
            with self.assertRaisesRegex(ValueError, "runtime root"):
                validate_release_archive(artifact, expected_version="1.0.0")


if __name__ == "__main__":
    unittest.main()
