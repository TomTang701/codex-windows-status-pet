import runpy
import unittest
from pathlib import Path


class VersionSourceTests(unittest.TestCase):
    def test_version_sources_are_consistent(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_version_sources.py"))
        self.assertEqual(module["check"](), [])


if __name__ == "__main__":
    unittest.main()
