import sys
import unittest
import io
import json
import subprocess
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

import run_quality_checks
import run_release_candidate_checks


class GateOrchestrationTests(unittest.TestCase):
    def test_quality_has_no_release_readiness_decision(self):
        commands = run_quality_checks.quality_commands("python")
        flattened = repr(commands)
        self.assertNotIn("check_release_readiness", flattened)
        self.assertNotIn("--strict", flattened)

    def test_release_candidate_requires_strict_compatibility(self):
        commands = run_release_candidate_checks.release_candidate_commands("python")
        self.assertEqual(commands["compatibility_strict"][-1], "--strict")
        self.assertIn("run_quality_checks.py", commands["quality"][1])
        self.assertIn("build_release.py", commands["release_build"][1])
        self.assertIn("package_smoke_test.py", commands["package_static"][1])
        self.assertIn("packaged_runtime_smoke.py", commands["package_runtime"][1])
        self.assertIn("release_bootstrap_smoke.py", commands["release_bootstrap"][1])
        self.assertIn("check_readme_screenshots.py", commands["readme_screenshots"][1])

    def test_release_candidate_fails_when_any_child_gate_fails(self):
        with mock.patch.object(
            run_release_candidate_checks,
            "run",
            side_effect=[
                (0, "quality ok"), (0, "build ok"), (0, "package ok"),
                (0, "runtime ok"), (0, "bootstrap ok"), (0, "screenshots ok"), (1, "blocking evidence"), (0, "clean"),
            ],
        ):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(run_release_candidate_checks.main(), 1)

    def test_release_candidate_succeeds_when_every_child_gate_passes(self):
        readiness = json.dumps({"ready": True, "passes": [], "blockers": [], "limitations": [{"area": "DPI"}]})
        with mock.patch.object(
            run_release_candidate_checks,
            "run",
            side_effect=[
                (0, "quality ok"), (0, "build ok"), (0, "package ok"),
                (0, "runtime ok"), (0, "bootstrap ok"), (0, "screenshots ok"), (0, readiness), (0, "clean"),
            ],
        ) as run:
            output = io.StringIO()
            with redirect_stdout(output):
                self.assertEqual(run_release_candidate_checks.main(), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(run.call_count, 8)
        self.assertEqual(result["blockers"], [])
        self.assertEqual(result["limitations"], [{"area": "DPI"}])
        self.assertEqual(
            result["passes"],
            ["quality", "release_build", "package_static", "package_runtime", "release_bootstrap", "readme_screenshots", "compatibility_strict", "whitespace"],
        )

    def test_runner_requests_utf8_replacement_decoding(self):
        completed = mock.Mock(returncode=1, stdout="错误", stderr="")
        with mock.patch.object(run_quality_checks.subprocess, "run", return_value=completed) as subprocess_run:
            self.assertEqual(run_quality_checks.run(["tool"]), (1, "错误"))
        self.assertEqual(subprocess_run.call_args.kwargs["encoding"], "utf-8")
        self.assertEqual(subprocess_run.call_args.kwargs["errors"], "replace")
        self.assertEqual(subprocess_run.call_args.kwargs["env"]["PYTHONIOENCODING"], "utf-8")

    def test_quality_runner_converts_a_stuck_child_into_a_bounded_failure(self):
        timeout = subprocess.TimeoutExpired(["tool"], 300)
        with mock.patch.object(run_quality_checks.subprocess, "run", side_effect=timeout):
            code, output = run_quality_checks.run(["tool"])
        self.assertEqual(code, 124)
        self.assertIn("timed out after 300 seconds", output)

    def test_quality_main_reports_each_check_progress(self):
        progress = io.StringIO()
        with (
            mock.patch.object(run_quality_checks, "quality_commands", return_value={"child": ["tool"]}),
            mock.patch.object(run_quality_checks, "run", return_value=(0, "ok")),
            mock.patch.object(sys, "stderr", progress),
        ):
            self.assertEqual(run_quality_checks.main(), 0)
        self.assertIn("[quality] child: start", progress.getvalue())
        self.assertIn("[quality] child: passed", progress.getvalue())

    def test_quality_json_is_safe_for_a_gbk_parent_console(self):
        raw = io.BytesIO()
        console = io.TextIOWrapper(raw, encoding="gbk")
        with (
            mock.patch.object(run_quality_checks, "quality_commands", return_value={"child": ["tool"]}),
            mock.patch.object(run_quality_checks, "run", return_value=(1, "bad \ufffd output")),
            mock.patch.object(sys, "stdout", console),
        ):
            self.assertEqual(run_quality_checks.main(), 1)
            console.flush()
        self.assertIn(b"\\ufffd", raw.getvalue())


if __name__ == "__main__":
    unittest.main()
