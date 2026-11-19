import argparse
import json
from pathlib import Path
import sys
import unittest
from .experiment import isolation, run_experiment
from .source_manifest import manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--require-isolation", action="store_true")
    args = parser.parse_args()
    isolated = isolation() if args.require_isolation else None
    if isolated and not (isolated["only_loopback"] and isolated["external_probe_unreachable"] and isolated["uid"] != 0):
        raise RuntimeError("Required non-root external-network isolation is not established")
    suite = unittest.defaultTestLoader.discover("tests")
    result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    report = {"version": "0.1.0", "tests": {"run": result.testsRun, "failures": len(result.failures),
                                         "errors": len(result.errors), "passed": result.wasSuccessful()},
              "isolation": isolated, "source_sha256": manifest(), **run_experiment()}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
