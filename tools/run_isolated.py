"""Run the locally prepared image with no external network and constrained privileges."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from .source_manifest import manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="ashish-enterprise-ai-gateway:0.1.0")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    command = ["docker", "run", "--rm", "--network=none", "--read-only", "--cap-drop=ALL",
               "--security-opt=no-new-privileges", "--cpus=1", "--memory=256m", "--pids-limit=96",
               "--tmpfs", "/tmp:rw,noexec,nosuid,size=32m,mode=1777",
               "--tmpfs", "/state:rw,noexec,nosuid,size=32m,mode=1777",
               args.image, "python", "-m", "tools.verify", "--require-isolation", "--output", "/state/report.json"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.with_suffix(".log").write_text(result.stderr)
    if result.returncode:
        raise RuntimeError(f"Isolated verification failed; inspect {target.with_suffix('.log')}")
    report = json.loads(result.stdout)
    if report["source_sha256"] != manifest():
        raise RuntimeError("Container source differs from current repository inputs")
    report["container_constraints"] = {
        "image": args.image, "network": "none", "root_filesystem": "read_only",
        "capabilities": "all_dropped", "no_new_privileges": True, "cpu_limit": 1,
        "memory_bytes": 256 * 1024 * 1024, "pid_limit": 96, "temporary_storage_mib": 64}
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"tests": report["tests"], "isolation": report["isolation"],
                      "scenarios": len(report["scenarios"]), "report": str(target)}, indent=2))


if __name__ == "__main__":
    main()
