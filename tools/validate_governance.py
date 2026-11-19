"""Validate the ORIGINAL example record contract, not a regulatory certification."""
import argparse
from datetime import date
import json
from pathlib import Path
from aiegateway.contracts import Denied, fields, identifier, parse_json

ROOT = Path(__file__).resolve().parents[1]


def text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 3000:
        raise Denied("missing_governance_text", 400)


def validate(pack, as_of=None):
    as_of = as_of or date.today()
    fields(pack, ("stage", "use_cases", "models", "risks", "exceptions",
                  "control_evidence", "operating_model", "evaluation_plan"))
    if pack["stage"] != "synthetic_reference":
        raise Denied("example_stage_required", 400)
    model_ids = set()
    for model in pack["models"]:
        fields(model, ("id", "owner", "supplier", "version", "location_declaration",
                      "intended_use", "evaluation_ref", "exit_plan", "status"))
        identifier(model["id"])
        if model["id"] in model_ids:
            raise Denied("duplicate_model_record", 400)
        model_ids.add(model["id"])
        for value in model.values():
            text(value)
    case_ids = set()
    for case in pack["use_cases"]:
        fields(case, ("id", "owner", "purpose", "prohibited_uses", "classification",
                     "permitted_regions", "models", "human_oversight", "retention",
                     "risk_review", "evaluation_ref", "status"))
        identifier(case["id"])
        if case["id"] in case_ids:
            raise Denied("duplicate_use_case_record", 400)
        case_ids.add(case["id"])
        if not isinstance(case["models"], list) or not case["models"] or any(m not in model_ids for m in case["models"]):
            raise Denied("governance_model_reference", 400)
        for key, value in case.items():
            if key != "models":
                text(value)
    if not case_ids or not model_ids or not pack["risks"] or not pack["control_evidence"]:
        raise Denied("incomplete_governance_inventory", 400)
    for risk in pack["risks"]:
        fields(risk, ("id", "scenario", "owner", "control", "residual_risk", "next_gate"))
        for value in risk.values():
            text(value)
    for exception in pack["exceptions"]:
        fields(exception, ("id", "owner", "approver", "expires", "scope", "compensating_control"))
        for value in exception.values():
            text(value)
        if exception["owner"] == exception["approver"]:
            raise Denied("independent_exception_approver", 400)
        try:
            expiry = date.fromisoformat(exception["expires"])
        except ValueError:
            raise Denied("invalid_exception_date", 400) from None
        if expiry <= as_of:
            raise Denied("expired_governance_exception", 400)
    for control in pack["control_evidence"]:
        fields(control, ("id", "owner", "artifact", "test", "gap"))
        for value in control.values():
            text(value)
        artifact = (ROOT / control["artifact"]).resolve()
        if not artifact.is_relative_to(ROOT) or not artifact.is_file():
            raise Denied("missing_control_artifact", 400)
        if control["test"] not in (ROOT / "tests/test_gateway.py").read_text():
            raise Denied("missing_control_test", 400)
    fields(pack["operating_model"], ("accountable", "security", "governance", "platform", "sre", "finops",
                                     "review_cadence", "incident_owner"))
    for value in pack["operating_model"].values():
        text(value)
    fields(pack["evaluation_plan"], ("scope", "dataset", "security_gate", "quality_gate", "privacy_gate",
                                     "fairness_gate", "reviewer", "production_gate"))
    for value in pack["evaluation_plan"].values():
        text(value)
    return {"valid": True, "stage": pack["stage"], "use_cases": len(case_ids), "models": len(model_ids),
            "risks": len(pack["risks"]), "control_links": len(pack["control_evidence"]),
            "exceptions": len(pack["exceptions"]), "as_of": as_of.isoformat(),
            "assurance": "example schema and artifact traceability only"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args()
    print(json.dumps(validate(parse_json(Path(args.path).read_bytes())), indent=2))


if __name__ == "__main__":
    main()
