"""Robot camera helpers. Run this file to list the modules."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("robot: calib, undistort, motion_ae, latency")
