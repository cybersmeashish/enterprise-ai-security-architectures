import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = ("aiegateway", "tools", "tests", "examples", "requirements.lock", "Dockerfile")


def manifest():
    paths = []
    for name in INPUTS:
        path = ROOT / name
        paths.extend([path] if path.is_file() else
                     [f for f in path.rglob("*") if f.is_file() and "__pycache__" not in f.parts
                      and f.suffix not in (".pyc", ".pyo")])
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}
