import copy
from datetime import date
import json
from pathlib import Path
import unittest
from aiegateway.contracts import Denied
from tools.validate_governance import validate


class GovernanceCases(unittest.TestCase):
    def setUp(self):
        self.pack = json.loads((Path(__file__).resolve().parents[1] / "examples/governance-pack.json").read_text())
    def rejected(self, code):
        with self.assertRaises(Denied) as result:
            validate(self.pack, date(2026, 11, 19))
        self.assertEqual(result.exception.code, code)

    def test_complete_synthetic_governance_pack(self):
        self.assertTrue(validate(self.pack, date(2026, 11, 19))["valid"])

    def test_missing_governance_owner_denied(self):
        self.pack["use_cases"][0]["owner"] = ""
        self.rejected("missing_governance_text")

    def test_unregistered_governance_model_denied(self):
        self.pack["use_cases"][0]["models"] = ["unknown"]
        self.rejected("governance_model_reference")

    def test_missing_control_evidence_denied(self):
        self.pack["control_evidence"][0]["artifact"] = "missing.py"
        self.rejected("missing_control_artifact")

    def test_expired_exception_denied(self):
        self.pack["exceptions"][0]["expires"] = "2026-11-18"
        self.rejected("expired_governance_exception")

    def test_example_cannot_be_labelled_production(self):
        self.pack["stage"] = "production_certified"
        self.rejected("example_stage_required")

    def test_same_person_cannot_approve_exception(self):
        self.pack["exceptions"][0]["approver"] = self.pack["exceptions"][0]["owner"]
        self.rejected("independent_exception_approver")
