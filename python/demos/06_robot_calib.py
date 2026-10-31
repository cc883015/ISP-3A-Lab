"""Job track: robot vision. Intrinsics from synthetic chessboards."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 06 robot calib ===")
    runpy.run_path(str(_PY / "robot" / "calib.py"), run_name="__main__")
    runpy.run_path(str(_PY / "robot" / "undistort.py"), run_name="__main__")
    runpy.run_path(str(_PY / "robot" / "motion_ae.py"), run_name="__main__")
    runpy.run_path(str(_PY / "robot" / "latency.py"), run_name="__main__")
