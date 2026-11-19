"""Connected preparation only; binary-only hash-locked downloads before isolated builds."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--architecture", choices=("arm64", "amd64"), required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    platform = "manylinux_2_28_aarch64" if args.architecture == "arm64" else "manylinux_2_28_x86_64"
    fallback = "manylinux2014_aarch64" if args.architecture == "arm64" else "manylinux2014_x86_64"
    target = root / "vendor/wheels"
    if target.exists() and any(target.glob("*.whl")):
        raise SystemExit("Wheel directory already populated; use an empty task-owned directory")
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, "-m", "pip", "download", "--disable-pip-version-check", "--no-cache-dir",
                    "--require-hashes", "--only-binary=:all:", "--implementation", "cp",
                    "--python-version", "312", "--abi", "cp312", "--abi", "abi3", "--abi", "none",
                    "--platform", platform, "--platform", fallback, "--dest", str(target),
                    "-r", str(root / "requirements.lock")], check=True)


if __name__ == "__main__":
    main()
