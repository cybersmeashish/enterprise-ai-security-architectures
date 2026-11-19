"""Ed25519 policy admission with externally supplied trust anchors."""
import base64
import copy
from dataclasses import dataclass
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from .contracts import Denied, canonical, classification, digest, fields, identifier, integer


@dataclass(frozen=True)
class VerifiedPolicy:
    value: dict
    sha256: str


def sign_policy(policy, signer_id, private_key):
    return {"policy": policy, "signer_id": signer_id,
            "signature": base64.b64encode(private_key.sign(canonical(policy))).decode()}


def admit_policy(envelope, trust, expected_site, minimum_revision, now):
    fields(envelope, ("policy", "signer_id", "signature"))
    identifier(envelope["signer_id"])
    key = trust.get(envelope["signer_id"])
    if key is None:
        raise Denied("untrusted_policy_signer")
    if not isinstance(envelope["signature"], str) or len(envelope["signature"]) != 88:
        raise Denied("invalid_policy_signature")
    try:
        Ed25519PublicKey.from_public_bytes(key).verify(
            base64.b64decode(envelope["signature"], validate=True), canonical(envelope["policy"]))
    except (ValueError, TypeError, InvalidSignature):
        raise Denied("invalid_policy_signature") from None
    policy = copy.deepcopy(envelope["policy"])
    validate_policy(policy)
    if policy["site"] != expected_site:
        raise Denied("wrong_policy_site")
    if policy["revision"] < minimum_revision:
        raise Denied("policy_rollback")
    if not policy["issued_at"] <= now < policy["expires_at"]:
        raise Denied("policy_not_current")
    return VerifiedPolicy(policy, digest(policy))


def validate_policy(p):
    fields(p, ("site", "revision", "issued_at", "expires_at", "owner", "models", "use_cases", "tenants"))
    identifier(p["site"])
    identifier(p["owner"])
    integer(p["revision"], 1, 10**9)
    integer(p["issued_at"], 0, 10**12)
    integer(p["expires_at"], p["issued_at"] + 1, 10**12)
    for collection in ("models", "use_cases", "tenants"):
        if not isinstance(p[collection], dict) or not 1 <= len(p[collection]) <= 100:
            raise Denied("invalid_policy_collection", 400)
        for key in p[collection]:
            identifier(key)
    for model in p["models"].values():
        fields(model, ("region", "classes", "state", "review_expires", "owner", "credit_per_byte",
                       "endpoint_ref", "evaluation_ref", "version"))
        identifier(model["region"])
        identifier(model["owner"])
        identifier(model["endpoint_ref"])
        identifier(model["version"])
        if model["state"] not in ("approved", "suspended", "retired"):
            raise Denied("invalid_model_state", 400)
        if not isinstance(model["classes"], list) or not model["classes"]:
            raise Denied("invalid_model_classes", 400)
        for item in model["classes"]:
            classification(item)
        integer(model["credit_per_byte"], 1, 1000)
        integer(model["review_expires"], 0, 10**12)
        identifier(model["evaluation_ref"])
    for case in p["use_cases"].values():
        fields(case, ("owner", "state", "review_expires", "minimum_classification", "regions",
                      "models", "tools", "max_output_bytes", "risk", "evidence_ref"))
        identifier(case["owner"])
        identifier(case["evidence_ref"])
        classification(case["minimum_classification"])
        if case["state"] not in ("approved", "suspended", "proposed"):
            raise Denied("invalid_use_case_state", 400)
        if case["risk"] not in ("low", "medium", "high"):
            raise Denied("invalid_risk", 400)
        integer(case["review_expires"], 0, 10**12)
        integer(case["max_output_bytes"], 1, 4096)
        if not isinstance(case["regions"], list) or not case["regions"]:
            raise Denied("invalid_regions", 400)
        for region in case["regions"]:
            identifier(region)
        if (not isinstance(case["models"], list) or not case["models"]
                or any(not isinstance(m, str) or m not in p["models"] for m in case["models"])):
            raise Denied("invalid_model_reference", 400)
        if not isinstance(case["tools"], list) or any(t != "maintenance.schedule" for t in case["tools"]):
            raise Denied("invalid_tool_reference", 400)
    for tenant in p["tenants"].values():
        fields(tenant, ("budget_credits", "requests_per_minute"))
        integer(tenant["budget_credits"], 1, 10**12)
        integer(tenant["requests_per_minute"], 1, 10**6)
