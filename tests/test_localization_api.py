import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.localization_api import SUPPORTED_LANGUAGES, normalize_language, translate


class LocalizationApiTests(unittest.TestCase):
    def test_supported_languages_normalize_and_translate(self):
        self.assertEqual(SUPPORTED_LANGUAGES, ("en", "zh-CN"))
        self.assertEqual(normalize_language(None), ("en", None))
        self.assertEqual(normalize_language("zh-CN"), ("zh-CN", None))
        self.assertEqual(normalize_language("fr"), ("en", "language is invalid; English retained"))
        self.assertEqual(translate("en", "idle"), "Idle")
        self.assertEqual(translate("en", "loading"), "Loading")
        self.assertEqual(
            translate("en", "existing_instance"),
            "Codex Windows Status Pet is already running.\nClose the existing instance before launching this copy.",
        )
        self.assertTrue(translate("zh-CN", "existing_instance").startswith("Codex "))
        self.assertEqual(translate("zh-CN", "idle"), "空闲")
        self.assertEqual(translate("zh-CN", "loading"), "\\u52a0\\u8f7d\\u4e2d")

    def test_key_and_placeholder_contract_is_visible(self):
        self.assertEqual(translate("en", "activity", detail="Running"), "Codex Running")
        self.assertEqual(translate("en", "reset_credit", count=5), "Reset 5 times")
        self.assertEqual(translate("zh-CN", "activity", detail="运行中"), "Codex 运行中")
        with self.assertRaises(KeyError):
            translate("en", "missing-key")


if __name__ == "__main__":
    unittest.main()
