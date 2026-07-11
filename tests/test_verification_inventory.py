import copy
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from check_verification_inventory import validate_inventory


VALID = {
    "schema_version": 1,
    "items": [
        {
            "id": "quality.tests",
            "classification": "AUTOMATED",
            "disposition": "pass",
            "fact": "Core and UI tests pass",
            "authority": "python scripts/run_quality_checks.py",
        }
    ],
}


class VerificationInventoryTests(unittest.TestCase):
    def test_minimal_inventory_is_valid(self):
        self.assertEqual(validate_inventory(VALID), [])

    def test_duplicate_ids_are_rejected(self):
        data = copy.deepcopy(VALID)
        data["items"].append(copy.deepcopy(data["items"][0]))
        self.assertIn("duplicate id: quality.tests", validate_inventory(data))

    def test_unknown_classification_is_rejected(self):
        data = copy.deepcopy(VALID)
        data["items"][0]["classification"] = "MANUAL"
        self.assertIn("quality.tests: invalid classification: MANUAL", validate_inventory(data))

    def test_invalid_disposition_is_rejected(self):
        data = copy.deepcopy(VALID)
        data["items"][0]["disposition"] = "deferred"
        self.assertIn("quality.tests: invalid disposition: deferred", validate_inventory(data))

    def test_blank_authority_is_rejected(self):
        data = copy.deepcopy(VALID)
        data["items"][0]["authority"] = "  "
        self.assertIn("quality.tests: authority must be a non-empty string", validate_inventory(data))

    def test_duplicate_requires_existing_replacement(self):
        data = copy.deepcopy(VALID)
        data["items"].append(
            {
                "id": "release.standalone-quality",
                "classification": "DUPLICATE",
                "disposition": "excluded",
                "fact": "Standalone Quality before RC repeats the RC child",
                "authority": "release procedure",
                "replacement": "release.rc",
            }
        )
        self.assertIn(
            "release.standalone-quality: replacement does not exist: release.rc",
            validate_inventory(data),
        )

    def test_physical_only_fact_cannot_be_a_machine_pass(self):
        data = copy.deepcopy(VALID)
        data["items"][0]["classification"] = "PHYSICAL-ONLY"
        self.assertIn(
            "quality.tests: PHYSICAL-ONLY disposition must be limitation or blocker",
            validate_inventory(data),
        )


if __name__ == "__main__":
    unittest.main()
