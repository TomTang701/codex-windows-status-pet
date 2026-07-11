import gc
import sys
import tkinter as tk
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_rows_api import ROW_IDS
from ui.status_rows import StatusRows


class StatusRowsUiTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.rows = StatusRows(
            self.root,
            text="activity\nprogress\n5h\nweekly\nreset",
            font=("Segoe UI", 10),
            fg="#ffffff",
            bg="#000000",
            wraplength=260,
        )

    def tearDown(self):
        self.rows.destroy()
        self.root.update_idletasks()
        self.root.destroy()
        del self.rows
        del self.root
        gc.collect()

    def test_exactly_five_stable_labels_and_event_widgets(self):
        self.assertEqual(tuple(self.rows.labels), ROW_IDS)
        self.assertEqual(len(self.rows.labels), 5)
        self.assertEqual(len(self.rows.event_widgets), 6)

    def test_one_row_updates_without_recreating_or_shifting_siblings(self):
        identities = {key: str(label) for key, label in self.rows.labels.items()}
        before = self.rows.row_values()
        self.rows.configure_rows(rows={"weekly": "周 80% / 20:00 7/12"})
        self.assertEqual({key: str(label) for key, label in self.rows.labels.items()}, identities)
        self.assertEqual(self.rows.row_values()["weekly"], "周 80% / 20:00 7/12")
        for row_id in ("activity", "progress", "primary_5h", "reset_credit"):
            self.assertEqual(self.rows.row_values()[row_id], before[row_id])

    def test_style_updates_propagate_to_every_row(self):
        self.rows.configure_rows(fg="#123456", bg="#654321", wraplength=240)
        for label in self.rows.labels.values():
            self.assertEqual(label.cget("fg"), "#123456")
            self.assertEqual(label.cget("bg"), "#654321")
            self.assertEqual(label.cget("wraplength"), 240)


if __name__ == "__main__":
    unittest.main()
