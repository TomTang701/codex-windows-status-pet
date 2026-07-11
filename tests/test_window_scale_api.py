import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.window_scale_api import (
    DEFAULT_WINDOW_SCALE_PERCENT,
    MAX_WINDOW_SCALE_PERCENT,
    MIN_WINDOW_SCALE_PERCENT,
    derive_window_metrics,
    infer_scale_percent,
    quantize_scale_percent,
)


class WindowScaleApiTests(unittest.TestCase):
    def test_100_percent_returns_canonical_metrics(self):
        metrics = derive_window_metrics(100)
        self.assertEqual((metrics.width, metrics.height), (330, 138))
        self.assertEqual((metrics.text_font_size, metrics.face_font_size), (10, 28))
        self.assertEqual(metrics.wraplength, 260)

    def test_bounds_and_half_up_quantization_are_deterministic(self):
        self.assertEqual(quantize_scale_percent(79), MIN_WINDOW_SCALE_PERCENT)
        self.assertEqual(quantize_scale_percent(82.5), 85)
        self.assertEqual(quantize_scale_percent(198), 200)
        self.assertEqual(quantize_scale_percent(999), MAX_WINDOW_SCALE_PERCENT)
        self.assertEqual(quantize_scale_percent("bad"), DEFAULT_WINDOW_SCALE_PERCENT)

    def test_supported_steps_preserve_ratio_and_monotonic_visual_metrics(self):
        previous = None
        for percent in range(80, 201, 5):
            metrics = derive_window_metrics(percent)
            self.assertLessEqual(abs(metrics.width / metrics.height - 330 / 138), 0.01)
            if previous is not None:
                self.assertGreaterEqual(metrics.width, previous.width)
                self.assertGreaterEqual(metrics.height, previous.height)
                self.assertGreaterEqual(metrics.text_font_size, previous.text_font_size)
                self.assertGreaterEqual(metrics.face_font_size, previous.face_font_size)
                self.assertGreaterEqual(metrics.wraplength, previous.wraplength)
            self.assertEqual(metrics, derive_window_metrics(percent))
            previous = metrics

    def test_legacy_geometry_inference_uses_area_and_clamps(self):
        self.assertEqual(infer_scale_percent(330, 138), 100)
        self.assertEqual(infer_scale_percent(660, 276), 200)
        self.assertEqual(infer_scale_percent(264, 110), 80)
        self.assertEqual(infer_scale_percent(660, 138), 140)
        self.assertEqual(infer_scale_percent(1, 1), 80)
        self.assertEqual(infer_scale_percent("bad", 138), 100)
        self.assertEqual(infer_scale_percent(-1, 138), 100)


if __name__ == "__main__":
    unittest.main()
