import gc
import sys
import tkinter as tk
from tkinter import font as tkfont
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_rows_api import ROW_IDS
from ui.status_rows import StatusRows


class StatusRowsUiTests(unittest.TestCase):
    def _visible_ids(self):
        return tuple(
            row_id
            for row_id, label in self.rows.labels.items()
            if label.winfo_ismapped()
        )

    def _visible_centers_x2(self):
        return tuple(
            2 * label.winfo_y() + label.winfo_height()
            for label in self.rows.labels.values()
            if label.winfo_ismapped()
        )

    def test_hiding_weekly_removes_only_its_persistent_label_from_layout(self):
        self.rows.pack(fill="both", expand=True)
        self.root.deiconify()
        self.root.geometry("300x200")
        self.root.update_idletasks()
        self.rows.set_visible_rows({"show_primary_5h": True, "show_weekly": False, "show_reset_credit": True})
        self.root.update_idletasks()
        self.assertEqual(tuple(self.rows.labels), ROW_IDS)
        self.assertFalse(self.rows.labels["weekly"].winfo_ismapped())
        self.assertTrue(all(self.rows.labels[row_id].winfo_ismapped() for row_id in ("activity", "progress", "primary_5h", "reset_credit")))

    def test_hiding_weekly_evenly_redistributes_the_same_text_region(self):
        self.rows.pack(fill="both", expand=True)
        self.root.deiconify()
        self.root.geometry("300x200")
        self.root.update()
        before = (self.rows.winfo_width(), self.rows.winfo_height())
        self.rows.set_visible_rows({"show_weekly": False})
        self.root.update_idletasks()
        centers = self._visible_centers_x2()
        self.assertEqual(
            self._visible_ids(),
            ("activity", "progress", "primary_5h", "reset_credit"),
        )
        self.assertEqual((self.rows.winfo_width(), self.rows.winfo_height()), before)
        self.assertEqual(len(centers), 4)
        self.assertEqual(len(set(right - left for left, right in zip(centers, centers[1:]))), 1)

    def test_quota_divider_stays_between_progress_and_first_quota_row(self):
        self.rows.pack(fill="both", expand=True)
        self.root.deiconify()
        self.root.geometry("300x200")
        self.root.update()
        self.rows.set_visible_rows({})
        self.root.update_idletasks()
        divider = self.rows.quota_divider
        progress = self.rows.labels["progress"]
        primary = self.rows.labels["primary_5h"]
        self.assertTrue(divider.winfo_ismapped())
        self.assertEqual(divider.cget("bg"), "#26354d")
        self.assertLessEqual(progress.winfo_y() + progress.winfo_height(), divider.winfo_y() + 1)
        self.assertLessEqual(divider.winfo_y() + divider.winfo_height(), primary.winfo_y())
        self.rows.set_visible_rows({"show_primary_5h": False})
        self.root.update_idletasks()
        weekly = self.rows.labels["weekly"]
        self.assertLessEqual(divider.winfo_y() + divider.winfo_height(), weekly.winfo_y())

    def test_quota_divider_has_a_small_group_label(self):
        self.rows.pack(fill="both", expand=True)
        self.root.deiconify()
        self.root.geometry("300x200")
        self.root.update()
        self.rows.set_visible_rows({})
        self.root.update_idletasks()
        self.assertEqual(self.rows.quota_label.cget("text"), "QUOTA")
        self.assertTrue(self.rows.quota_label.winfo_ismapped())
        self.assertEqual(self.rows.quota_label.cget("fg"), "#94a3b8")
        label_center = self.rows.quota_label.winfo_y() + self.rows.quota_label.winfo_height() // 2
        self.assertLessEqual(abs(label_center - self.rows.quota_divider.winfo_y()), 2)

    def test_quota_group_label_scales_with_status_font(self):
        initial_font = self.rows.quota_label.cget("font")
        self.rows.configure_rows(font=("Segoe UI", -20))
        self.assertNotEqual(self.rows.quota_label.cget("font"), initial_font)
        self.assertEqual(
            tkfont.Font(root=self.root, font=self.rows.quota_label.cget("font")).actual("family"),
            "Segoe UI",
        )

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
        self.assertEqual(len(self.rows.event_widgets), 7)

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
        self.assertEqual(self.rows.quota_divider.cget("bg"), "#26354d")
        self.assertEqual(self.rows.quota_label.cget("bg"), "#654321")


if __name__ == "__main__":
    unittest.main()
