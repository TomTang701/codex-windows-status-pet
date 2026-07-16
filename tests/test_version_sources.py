import runpy
import unittest
import json
from pathlib import Path


class VersionSourceTests(unittest.TestCase):
    def test_version_sources_are_consistent(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_version_sources.py"))
        self.assertEqual(module["check"](), [])

    def test_v091_release_sources_are_declared_before_release(self):
        root = Path(__file__).parents[1]
        manifest = json.loads((root / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertTrue(manifest["version"].startswith("1.0.0+"))


if __name__ == "__main__":
    unittest.main()
