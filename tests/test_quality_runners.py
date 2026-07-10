import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from run_quality_checks import quality_commands
import run_release_candidate_checks as candidate


class QualityRunnerTests(unittest.TestCase):
    def test_compile_gate_recursively_covers_scripts(self):
        command = quality_commands("python")["compile"]
        self.assertEqual(command[:4], ["python", "-m", "compileall", "-q"])
        self.assertTrue(Path(command[4]).name == "scripts")

    def test_quality_includes_package_and_non_strict_readiness(self):
        commands = quality_commands("python")
        self.assertIn("package_smoke", commands)
        self.assertNotIn("--strict", commands["release_readiness_report"])

    def test_release_candidate_uses_strict_readiness(self):
        source = Path(candidate.__file__).read_text(encoding="utf-8")
        self.assertIn('"--strict"', source)

    def test_tag_must_match_canonical_version(self):
        with patch.dict(os.environ, {"GITHUB_REF_TYPE": "tag", "GITHUB_REF_NAME": "v9.9.9"}, clear=False):
            code, output = candidate._release_metadata_check()
        self.assertEqual(code, 1)
        self.assertIn("does not match", output)

    def test_artifact_check_writes_sha256(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build = root / ".build"
            build.mkdir()
            artifact = build / "codex-windows-status-pet-smoke.zip"
            artifact.write_bytes(b"artifact")
            with patch.object(candidate, "ROOT", root):
                code, output = candidate._artifact_check()
            self.assertEqual(code, 0)
            self.assertIn("sha256=", output)
            self.assertTrue(artifact.with_suffix(".zip.sha256").is_file())

