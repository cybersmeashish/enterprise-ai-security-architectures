"""Run the bounded demonstration or start an ephemeral local fixture gateway."""
import argparse
import json
import signal
import tempfile
from pathlib import Path
from .fixtures import environment


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true", help="Expose loopback demo until Ctrl-C")
    args = parser.parse_args()
    if not args.serve:
        from tools.experiment import run_experiment
        report = run_experiment(samples=10)
        print(json.dumps({"product": "Enterprise AI Gateway", "version": "0.1.0",
                          "scenarios": [{"id": c["id"], "passed": c["passed"]} for c in report["scenarios"]],
                          "benchmarks": report["benchmarks"], "known_gaps": report["known_gaps"]}, indent=2))
        return
    with tempfile.TemporaryDirectory() as directory:
        with environment(str(Path(directory) / "gateway.sqlite"), start_http=True) as env:
            print("Local synthetic fixture; credentials expire after one hour. No paid provider calls.")
            print(json.dumps({"url": f"http://127.0.0.1:{env['server'].server_port}",
                              "temporary_local_credentials": env["tokens"]}, indent=2), flush=True)
            try:
                while True:
                    signal.pause()
            except KeyboardInterrupt:
                pass


if __name__ == "__main__":
    main()
