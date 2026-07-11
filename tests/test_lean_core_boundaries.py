import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
API = ROOT / "scripts" / "api"


class LeanCoreBoundaryTests(unittest.TestCase):
    def test_obsolete_compatibility_boundaries_are_absent(self):
        obsolete = [
            API / "models_api.py",
            API / "window_size_api.py",
            API / "resize_session_api.py",
            API / "quota_provider_api.py",
        ]
        self.assertEqual([path.name for path in obsolete if path.exists()], [])

    def test_main_window_uses_the_authoritative_quota_parser_directly(self):
        source = (ROOT / "scripts" / "ui" / "main_window.py").read_text(encoding="utf-8")
        self.assertIn("parse_quota_payload", source)
        self.assertNotIn("normalize_snapshot", source)
        self.assertNotIn("quota_provider_api", source)

    def test_active_api_spec_does_not_advertise_obsolete_boundaries(self):
        source = (ROOT / "docs" / "architecture" / "API_SPEC.md").read_text(encoding="utf-8")
        for name in ("models_api.py", "window_size_api.py", "resize_session_api.py", "quota_provider_api.py"):
            self.assertNotIn(name, source)


if __name__ == "__main__":
    unittest.main()
