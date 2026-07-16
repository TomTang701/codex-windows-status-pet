import runpy
import unittest
import json
from pathlib import Path


class VersionSourceTests(unittest.TestCase):
    def test_version_sources_are_consistent(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_version_sources.py"))
        self.assertEqual(module["check"](), [])

    def test_v102_release_sources_are_declared_before_release(self):
        root = Path(__file__).parents[1]
        manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["version"].startswith("1.0.2+"))

    def test_readmes_document_both_supported_installation_paths(self):
        root = Path(__file__).parents[1]
        for name in ("README.md", "README.zh-CN.md"):
            text = (root / name).read_text(encoding="utf-8")
            self.assertIn("CodexStatusPet-v1.0.2-win11-x64.zip", text)
            self.assertIn("launch.cmd", text)
            self.assertIn("CodexStatusPet-bootstrap.ps1", text)


if __name__ == "__main__":
    unittest.main()
