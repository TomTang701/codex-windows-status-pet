"""Release README screenshot evidence must be complete, authentic-file shaped, and localized."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_readme_screenshots import check


PNG = b"\x89PNG\r\n\x1a\n"


class ReadmeScreenshotTests(unittest.TestCase):
    def write_evidence(self, root):
        paths = []
        for language in ("en", "zh-CN"):
            for name in ("main-overlay", "context-menu", "settings"):
                path = root / "docs" / "assets" / "readme" / language / f"{name}.png"
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(PNG)
                paths.append(path.relative_to(root).as_posix())
        (root / "README.md").write_text("\n".join(paths[:3]), encoding="utf-8")
        (root / "README.zh-CN.md").write_text("\n".join(paths[3:]), encoding="utf-8")

    def test_exact_language_matched_six_pngs_are_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_evidence(root)
            self.assertEqual(check(root), [])

    def test_missing_or_cross_language_screenshot_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_evidence(root)
            (root / "docs" / "assets" / "readme" / "zh-CN" / "settings.png").unlink()
            (root / "README.md").write_text(
                "docs/assets/readme/zh-CN/main-overlay.png", encoding="utf-8"
            )
            errors = check(root)
        self.assertTrue(any("missing screenshot" in error for error in errors))
        self.assertTrue(any("README.md" in error and "zh-CN" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
