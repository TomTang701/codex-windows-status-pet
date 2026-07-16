import runpy
import tempfile
import unittest
from pathlib import Path


class DependencyTests(unittest.TestCase):
    def test_declared_dependencies_are_installed_and_importable(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_dependencies.py"))
        self.assertEqual(module["check"](), [])

    def test_exact_pins_are_valid_dependency_declarations(self):
        module = runpy.run_path(str(Path(__file__).parents[1] / "scripts" / "check_dependencies.py"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "requirements.txt").write_text("Pillow==12.2.0\n", encoding="utf-8")
            self.assertEqual(module["check"](root), [])


if __name__ == "__main__":
    unittest.main()
