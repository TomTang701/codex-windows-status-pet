import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from api.input_validation_api import (
    is_signed_integer_candidate,
    is_unsigned_integer_candidate,
    parse_signed_integer,
    parse_unsigned_integer,
)


class InputValidationTests(unittest.TestCase):
    def test_signed_candidate_allows_typing_negative_value(self):
        self.assertTrue(is_signed_integer_candidate(""))
        self.assertTrue(is_signed_integer_candidate("-"))
        self.assertTrue(is_signed_integer_candidate("-1"))
        self.assertFalse(is_signed_integer_candidate("--1"))
        self.assertFalse(is_signed_integer_candidate("+-1"))
        self.assertFalse(is_signed_integer_candidate("1.2"))

    def test_unsigned_candidate_rejects_symbols(self):
        self.assertTrue(is_unsigned_integer_candidate("123"))
        self.assertTrue(is_unsigned_integer_candidate(""))
        self.assertFalse(is_unsigned_integer_candidate("-1"))
        self.assertFalse(is_unsigned_integer_candidate("1a"))

    def test_submit_requires_complete_integer(self):
        self.assertEqual(parse_signed_integer("-4151"), -4151)
        with self.assertRaises(ValueError):
            parse_signed_integer("-")
        with self.assertRaises(ValueError):
            parse_signed_integer("+-1")

    def test_unsigned_submit_clamps_range(self):
        self.assertEqual(parse_unsigned_integer("0", 1, 10), 1)
        self.assertEqual(parse_unsigned_integer("99", 1, 10), 10)
        with self.assertRaises(ValueError):
            parse_unsigned_integer("")
