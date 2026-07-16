import gc
import sys
import tkinter as tk
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.status_snapshot_api import battery_presentation
from ui.battery_view import BatteryView


class BatteryViewTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.view = BatteryView(self.root, bg="#111827")
        self.view.pack()

    def tearDown(self):
        self.view.destroy()
        self.root.update_idletasks()
        self.root.destroy()
        gc.collect()

    def test_view_has_exactly_ten_visible_cells_in_two_columns_and_five_rows(self):
        self.view.configure_presentation(battery_presentation({"usedPercent": 22}))
        self.root.update_idletasks()
        self.root.update()
        self.assertEqual(len(self.view.cells), 10)
        self.assertEqual({cell.grid_info()["column"] for cell in self.view.cells}, {0, 1})
        self.assertEqual({cell.grid_info()["row"] for cell in self.view.cells}, {1, 2, 3, 4, 5})
        self.assertTrue(all(cell.winfo_ismapped() for cell in self.view.cells))
        self.assertEqual(self.view.value_label.grid_info()["row"], 0)
        self.assertEqual(self.view.value_label.cget("text"), "78%")
        self.assertEqual(self.view.cells[0].cget("bg"), "#ef4444")
        self.assertNotEqual(self.view.cells[6].cget("bg"), self.view.cells[8].cget("bg"))


if __name__ == "__main__":
    unittest.main()
