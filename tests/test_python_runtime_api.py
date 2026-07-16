import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.python_runtime_api import RuntimeProbe, choose_runtime


class PythonRuntimeTests(unittest.TestCase):
    def test_codex_runtime_is_selected_before_py_and_path(self):
        probes = {
            "codex": RuntimeProbe(Path("codex-python"), "codex", (3, 12), 64, True, True, Path("pythonw.exe")),
            "py": RuntimeProbe(Path("py-python"), "py", (3, 11), 64, True, True, Path("pythonw.exe")),
            "path": RuntimeProbe(Path("path-python"), "path", (3, 10), 64, True, True, Path("pythonw.exe")),
        }
        with mock.patch("api.python_runtime_api.probe_runtime", side_effect=probes.values()):
            selected = choose_runtime(["codex", "py", "path"])
        self.assertEqual(selected.source, "codex")

    def test_invalid_candidates_are_rejected_until_valid_fallback(self):
        probes = [
            RuntimeProbe(Path("old"), "codex", (3, 9), 64, True, True, Path("pythonw.exe")),
            RuntimeProbe(Path("no-tk"), "py", (3, 11), 64, False, True, Path("pythonw.exe")),
            RuntimeProbe(Path("valid"), "path", (3, 11), 64, True, True, Path("pythonw.exe")),
        ]
        with mock.patch("api.python_runtime_api.probe_runtime", side_effect=probes):
            selected = choose_runtime(["codex", "py", "path"])
        self.assertEqual(selected.path, Path("valid"))

    def test_no_compatible_runtime_fails_with_actionable_error(self):
        probe = RuntimeProbe(Path("bad"), "path", (3, 9), 32, False, False, None)
        with mock.patch("api.python_runtime_api.probe_runtime", return_value=probe):
            with self.assertRaisesRegex(RuntimeError, r"Python 3.10\+"):
                choose_runtime(["path"])


if __name__ == "__main__":
    unittest.main()
