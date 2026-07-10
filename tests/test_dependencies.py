import runpy
import unittest
from pathlib import Path


class DependencyTests(unittest.TestCase):
    def test_declared_dependencies_are_installed_and_importable(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_dependencies.py"))
        self.assertEqual(module["check"](), [])


if __name__ == "__main__":
    unittest.main()
