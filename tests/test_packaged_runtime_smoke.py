"""Pure checks supporting the source-package smoke."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import packaged_runtime_smoke as smoke


class PackagedRuntimeSmokeTests(unittest.TestCase):
    def test_boundary_isolates_user_paths_and_strips_source_imports(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            boundary = smoke.zip_direct_use_boundary(root, {"PATH": "C:/Windows", "PYTHONPATH": "C:/source"})
            self.assertEqual(boundary.settings_file, root / "User" / ".codex" / "codex-windows-status-pet.json")
            self.assertEqual(boundary.install_root, root / "Local" / "Programs" / "CodexStatusPet")
            self.assertEqual(boundary.desktop_shortcut, root / "Desktop" / "Codex Windows Status Pet.lnk")
            self.assertNotIn("PYTHONPATH", boundary.environment)

    def test_direct_use_exit_preserves_settings_without_installed_state(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            boundary = smoke.zip_direct_use_boundary(root)
            boundary.settings_file.parent.mkdir(parents=True)
            expected = {"schema_version": 1, "x": 30, "y": 120, "language": "zh-CN"}
            boundary.settings_file.write_text('{"schema_version": 1, "x": 30, "y": 120, "language": "zh-CN", "alpha": 0.95}\n', encoding="utf-8")
            smoke.assert_zip_direct_use_exit(boundary, expected)

    def test_source_entrypoint_compile_uses_extracted_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            entrypoint = Path(directory) / "CodexStatusPet" / "scripts" / "codex_status_pet.py"
            entrypoint.parent.mkdir(parents=True)
            entrypoint.write_text("print('ok')\n", encoding="utf-8")
            smoke.source_entrypoint_compile(entrypoint)


if __name__ == "__main__":
    unittest.main()
