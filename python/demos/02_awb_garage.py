"""Job track: tuning + 3A. Two-illuminant garage entrance."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 02 AWB garage (two illuminants) ===")
    runpy.run_path(str(_PY / "aaa" / "awb.py"), run_name="__main__")
