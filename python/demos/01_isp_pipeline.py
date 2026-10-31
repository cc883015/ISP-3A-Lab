"""Job track: image-driven. Full teaching ISP."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 01 ISP pipeline ===")
    runpy.run_path(str(_PY / "isp" / "pipeline.py"), run_name="__main__")
