import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.release_artifact_api import ReleaseManifest, validate_release_root


class SourceReleaseContractTests(unittest.TestCase):
    def write_source_root(self, root, *, manifest=None):
        runtime = root / "CodexStatusPet"
        (runtime / "scripts").mkdir(parents=True)
        (runtime / "assets").mkdir()
        (runtime / "scripts" / "codex_status_pet.py").write_text("# entrypoint\n", encoding="utf-8")
        (runtime / "launch.vbs").write_text("' launcher\n", encoding="utf-8")
        (runtime / "launch.ps1").write_text("# launcher\n", encoding="utf-8")
        (runtime / "install.ps1").write_text("# installer\n", encoding="utf-8")
        (runtime / "uninstall.ps1").write_text("# uninstaller\n", encoding="utf-8")
        (runtime / "requirements-runtime.txt").write_text(
            "Pillow==12.2.0\npystray==0.19.5\n", encoding="utf-8"
        )
        (runtime / "assets" / "CodexStatusPet.ico").write_bytes(b"ico")
        (runtime / "LICENSE").write_text("MIT", encoding="utf-8")
        (runtime / "THIRD_PARTY_NOTICES.md").write_text("notices", encoding="utf-8")
        (runtime / "release-manifest.json").write_text(
            json.dumps(manifest or {
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
            }),
            encoding="utf-8",
        )
        return runtime

    def test_source_root_requires_schema_two_python_entrypoint_and_canonical_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            manifest = validate_release_root(self.write_source_root(Path(directory)), expected_version="1.0.0")
        self.assertEqual(
            manifest,
            ReleaseManifest(
                version="1.0.0",
                runtime="python",
                entrypoint="scripts/codex_status_pet.py",
                launcher="launch.vbs",
                icon="assets/CodexStatusPet.ico",
            ),
        )

    def test_source_root_rejects_executable_internal_and_development_material(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = self.write_source_root(Path(directory))
            (runtime / "CodexStatusPet.exe").write_bytes(b"exe")
            with self.assertRaisesRegex(ValueError, "prohibited"):
                validate_release_root(runtime, expected_version="1.0.0")

    def test_source_root_requires_exact_runtime_dependencies(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = self.write_source_root(Path(directory))
            (runtime / "requirements-runtime.txt").write_text("Pillow>=10\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "runtime requirements"):
                validate_release_root(runtime, expected_version="1.0.0")


if __name__ == "__main__":
    unittest.main()
