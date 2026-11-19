"""Strict wire contracts; clients never supply authoritative tenant or endpoint data."""
import hashlib
import json
import re

CLASSES = ("public", "internal", "confidential", "restricted")
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")


class Denied(Exception):
    def __init__(self, code, status=403):
        super().__init__(code)
        self.code, self.status = code, status


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
                      allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def parse_json(data):
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise Denied("duplicate_json_key", 400)
            obj[key] = value
        return obj
    try:
        return json.loads(data, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(ValueError()))
    except Denied:
        raise
    except (ValueError, UnicodeError, RecursionError):
        raise Denied("invalid_json", 400) from None


def fields(value, required, optional=()):
    if not isinstance(value, dict) or set(value) - set(required) - set(optional) or set(required) - set(value):
        raise Denied("invalid_fields", 400)


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise Denied("invalid_identifier", 400)
    return value


def integer(value, low, high):
    if type(value) is not int or not low <= value <= high:
        raise Denied("invalid_integer", 400)
    return value


def classification(value):
    if value not in CLASSES:
        raise Denied("invalid_classification", 400)
    return value


def generate_request(value):
    fields(value, ("use_case", "prompt", "max_output_bytes"), ("classification", "document_id"))
    identifier(value["use_case"])
    integer(value["max_output_bytes"], 1, 4096)
    if not isinstance(value["prompt"], str) or not 1 <= len(value["prompt"].encode()) <= 8192:
        raise Denied("invalid_prompt_size", 400)
    classification(value.get("classification", "public"))
    if "document_id" in value:
        identifier(value["document_id"])
    return value


def tool_action(value):
    fields(value, ("use_case", "tool", "arguments"), ("approvals",))
    identifier(value["use_case"])
    if value["tool"] != "maintenance.schedule":
        raise Denied("tool_not_allowed")
    args = value["arguments"]
    fields(args, ("asset", "window"))
    identifier(args["asset"])
    if args["window"] not in ("day", "night"):
        raise Denied("invalid_window", 400)
    approvals = value.get("approvals", [])
    if (not isinstance(approvals, list) or len(approvals) > 2
            or any(not isinstance(a, str) or len(a) != 43 for a in approvals)):
        raise Denied("invalid_approvals", 400)
    return value
