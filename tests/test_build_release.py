"""Release builder fails before PyInstaller when a project staging path is in use."""

from __future__ import annotations

import sys
import tempfile
import unittest
import json
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import build_release


class BuildReleaseTests(unittest.TestCase):
    def test_clean_build_paths_fails_clearly_when_release_staging_remains(self):
        with tempfile.TemporaryDirectory() as directory:
            staging = Path(directory) / "release"
            staging.mkdir()
            with mock.patch.object(build_release.shutil, "rmtree"):
                with self.assertRaisesRegex(RuntimeError, "staging path is in use"):
                    build_release.clean_build_paths((staging,))

    def test_source_manifest_contains_python_entrypoint_and_no_exe(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / "CodexStatusPet"
            runtime.mkdir()
            build_release.write_manifest(runtime, "1.1.0", channel="source")
            manifest = json.loads((runtime / "release-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 2)
        self.assertEqual(manifest["runtime"], "python")
        self.assertEqual(manifest["entrypoint"], "scripts/codex_status_pet.py")
        self.assertNotIn(".exe", manifest["entrypoint"])

    def test_standalone_manifest_contains_the_direct_executable_entrypoint(self):
        with tempfile.TemporaryDirectory() as directory:
            runtime = Path(directory) / "CodexStatusPet"
            runtime.mkdir()
            build_release.write_manifest(runtime, "1.1.0", channel="standalone")
            manifest = json.loads((runtime / "release-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["entrypoint"], "CodexStatusPet.exe")
        self.assertNotIn("runtime", manifest)

    def test_release_build_declares_one_zip_per_channel(self):
        artifacts = build_release.release_artifact_paths("1.1.0")
        self.assertEqual(
            artifacts["standalone"].name,
            "CodexStatusPet-v1.1.0-win11-x64.zip",
        )
        self.assertEqual(
            artifacts["source"].name,
            "CodexStatusPet-v1.1.0-source-win11-x64.zip",
        )

    def test_release_build_dependencies_are_pinned_for_the_standalone_channel(self):
        requirements = (Path(__file__).parents[1] / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("PyInstaller==6.16.0", requirements)
        self.assertIn("Pillow==12.2.0", requirements)
        self.assertIn("pystray==0.19.5", requirements)

    def test_source_tree_copy_excludes_development_material(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            runtime = Path(directory) / "runtime"
            (source / "scripts" / "ui").mkdir(parents=True)
            (source / "tests").mkdir()
            (source / "scripts" / "codex_status_pet.py").write_text("entry", encoding="utf-8")
            (source / "scripts" / "ui" / "main.py").write_text("ui", encoding="utf-8")
            (source / "tests" / "bad.py").write_text("test", encoding="utf-8")
            build_release.copy_source_tree(source, runtime)
            self.assertTrue((runtime / "scripts" / "codex_status_pet.py").exists())
            self.assertFalse((runtime / "tests").exists())


if __name__ == "__main__":
    unittest.main()
