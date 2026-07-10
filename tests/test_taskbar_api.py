import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.taskbar_api import edge_name


class TaskbarApiTests(unittest.TestCase):
    def test_edge_names_are_stable(self):
        self.assertEqual(edge_name(0), "left")
        self.assertEqual(edge_name(1), "top")
        self.assertEqual(edge_name(2), "right")
        self.assertEqual(edge_name(3), "bottom")
        self.assertEqual(edge_name(99), "unknown")
