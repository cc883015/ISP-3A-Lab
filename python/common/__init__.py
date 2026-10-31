"""Shared helpers. Run this file to print repo paths."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.paths import output_dir, repo_root  # noqa: E402
from common.imageio import luma, save_rgb, to_u8  # noqa: E402

if __name__ == "__main__":
    print(f"repo_root  = {repo_root()}")
    print(f"output_dir = {output_dir('common')}")
    print("helpers: luma, save_rgb, to_u8")
