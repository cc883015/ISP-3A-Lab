"""Job track: ISP tuning. One-page IQ report."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 05 IQ report ===")
    runpy.run_path(str(_PY / "metrics" / "report.py"), run_name="__main__")
