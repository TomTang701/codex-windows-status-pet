import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.resize_session_api import ResizeSession


class ResizeSessionTests(unittest.TestCase):
    def test_plus_then_minus_returns_to_exact_base_dimensions(self):
        session = ResizeSession(330, 138)
        original = session.dimensions()
        self.assertEqual(session.step(10), (363, 152))
        self.assertEqual(session.step(-10), original)

    def test_buttons_always_scale_both_dimensions(self):
        session = ResizeSession(330, 138)
        self.assertEqual(session.step(-10), (297, 124))

    def test_dimensions_remain_bounded(self):
        session = ResizeSession(1000, 700)
        session.set_scale(200)
        self.assertEqual(session.dimensions(), (1200, 800))
