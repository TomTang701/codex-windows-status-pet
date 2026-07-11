import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_doc_governance import check


class DocumentGovernanceTests(unittest.TestCase):
    def fixture(self, root: Path):
        goal = root / "Goal"
        archive = root / "docs" / "archive" / "plans"
        archive.mkdir(parents=True)
        goal.mkdir()
        (goal / "ACTIVE_GOAL.md").write_text("# Active\n", encoding="utf-8")
        (goal / "ACTIVE_VERSION_BRIEF.md").write_text("# Brief\n", encoding="utf-8")
        (goal / "README.md").write_text("# Rules\n", encoding="utf-8")
        (archive / "old.md").write_text(
            "---\nstatus: archived\nnormative: false\nsuperseded_by: ../../../Goal/ACTIVE_GOAL.md\n---\n# Old\n",
            encoding="utf-8",
        )
        (root / "docs" / "document_manifest.json").write_text(
            json.dumps({"documents": []}), encoding="utf-8"
        )

    def test_approved_goal_and_archived_plan_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            self.assertEqual(check(root), [])

    def test_unapproved_or_duplicate_goal_files_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "Goal" / "ACTIVE_GOAL_copy.md").write_text("duplicate", encoding="utf-8")
            (root / "Goal" / "v0.3.0.md").write_text("version goal", encoding="utf-8")
            errors = check(root)
            self.assertTrue(any("ACTIVE_GOAL_copy" in item for item in errors))
            self.assertTrue(any("v0.3.0" in item for item in errors))

    def test_missing_active_goal_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            (root / "Goal" / "ACTIVE_GOAL.md").unlink()
            self.assertIn("Goal/ACTIVE_GOAL.md is required", check(root))

    def test_archived_plan_metadata_and_target_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            plan = root / "docs" / "archive" / "plans" / "old.md"
            plan.write_text(
                "---\nstatus: active\nnormative: true\nsuperseded_by: missing.md\n---\n",
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("status must be archived" in item for item in errors))
            self.assertTrue(any("normative must be false" in item for item in errors))
            self.assertTrue(any("target is missing" in item for item in errors))

    def test_archived_manifest_entry_cannot_block_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.fixture(root)
            manifest = root / "docs" / "document_manifest.json"
            manifest.write_text(json.dumps({"documents": [{
                "canonical": "docs/archive/plans/old.md",
                "required_for_release": True,
            }]}), encoding="utf-8")
            self.assertTrue(any("cannot be required" in item for item in check(root)))


if __name__ == "__main__":
    unittest.main()
