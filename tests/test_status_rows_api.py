import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_rows_api import ROW_IDS, StatusRowsSnapshot, split_status_text


class StatusRowsApiTests(unittest.TestCase):
    def test_stable_row_ids_and_round_trip(self):
        rows = StatusRowsSnapshot("activity", "progress", "5h", "weekly", "reset")
        self.assertEqual(tuple(rows.as_dict()), ROW_IDS)
        self.assertEqual(split_status_text(rows.as_text()), rows)

    def test_missing_lines_are_empty_not_shifted(self):
        rows = split_status_text("activity\nprogress")
        self.assertEqual(rows.activity, "activity")
        self.assertEqual(rows.progress, "progress")
        self.assertEqual(rows.reset_credit, "")

