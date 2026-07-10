import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class StatusRowsUiTests(unittest.TestCase):
    def test_reset_credit_row_fits_legacy_330_by_138_window(self):
        code = r'''
import sys
import tkinter as tk
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "scripts"))
from ui.status_rows import StatusRows
root = tk.Tk()
try:
    root.geometry("330x138+0+0")
    face = tk.Label(root, text="🐾", font=("Segoe UI Emoji", 28))
    face.pack(side="left", padx=(12, 5), pady=10)
    rows = StatusRows(
        root,
        text="Codex 输出中\n活动对话 1 个\n5h 10% / 17:23\n周 86% / 12:23 7/17\n重置 5 次 / 18:40 7/12",
        wraplength=248,
        font=("Segoe UI", 10), fg="#ffffff", bg="#aaaaaa",
    )
    rows.pack(side="left", fill="both", expand=True, pady=3)
    root.update_idletasks()
    reset = rows.labels["reset_credit"]
    assert reset.winfo_y() + reset.winfo_height() <= rows.winfo_height()
    assert reset.cget("text") == "重置 5 次 / 18:40 7/12"
finally:
    root.destroy()
'''
        completed = subprocess.run(
            [sys.executable, "-c", code], cwd=ROOT, text=True, capture_output=True, timeout=10
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
