"""Repo paths. Run this file to create output/common and print locations."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def python_root() -> Path:
    return Path(__file__).resolve().parents[1]


def output_dir(name: str) -> Path:
    path = repo_root() / "output" / name
    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    out = output_dir("common")
    marker = out / "paths.txt"
    marker.write_text(f"repo={repo_root()}\npython={python_root()}\n", encoding="utf-8")
    print(f"wrote {marker}")
