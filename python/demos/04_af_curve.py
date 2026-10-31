"""Job track: tuning. Contrast AF curve."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 04 AF curve ===")
    runpy.run_path(str(_PY / "aaa" / "af.py"), run_name="__main__")
