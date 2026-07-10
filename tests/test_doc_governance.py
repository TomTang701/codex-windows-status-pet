import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_doc_metadata import check as check_metadata
from check_doc_review_age import stale_documents
from check_orphan_documents import check as check_orphans


class DocumentGovernanceTests(unittest.TestCase):
    def _fixture(self, root, version="1.0.0", reviewed="2026-07-10"):
        (root / "docs").mkdir()
        manifest = {
            "schema_version": 1,
            "documents": [{
                "id": "SPEC", "class": "normative", "status": "active",
                "canonical": "SPEC.md", "translations": {"zh-CN": "SPEC.zh-CN.md"},
                "owner": "maintainer", "review_cycle_days": 90, "required_for_release": True,
            }],
        }
        (root / "docs" / "document_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        for path, pair, doc_version in (("SPEC.md", "SPEC.zh-CN.md", "1.0.0"), ("SPEC.zh-CN.md", "SPEC.md", version)):
            (root / path).write_text(
                f"---\ndocument_id: SPEC\nstatus: active\ndocument_version: {doc_version}\n"
                f"canonical_language: en\ntranslation_pair: {pair}\nowner: maintainer\n"
                f"last_reviewed: {reviewed}\nreview_cycle_days: 90\n---\n# Spec\n",
                encoding="utf-8",
            )

    def test_metadata_accepts_matching_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture(root)
            self.assertEqual(check_metadata(root), [])

    def test_metadata_rejects_translation_version_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture(root, version="2.0.0")
            self.assertTrue(any("document_version differs" in error for error in check_metadata(root)))

    def test_review_age_reports_overdue_required_document(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture(root, reviewed="2025-01-01")
            result = stale_documents(root, today=date(2026, 7, 10))
            self.assertEqual(result[0]["id"], "SPEC")
            self.assertTrue(result[0]["required_for_release"])

    def test_orphan_active_front_matter_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._fixture(root)
            (root / "ORPHAN.md").write_text("---\nstatus: active\n---\n# Orphan\n", encoding="utf-8")
            self.assertEqual(check_orphans(root), ["orphan active document: ORPHAN.md"])

