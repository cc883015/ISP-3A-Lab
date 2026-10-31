"""Generic 3A. Run this file to list the controllers."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("3A: ae.py  awb.py  af.py")
    print("Vendor hooks later: python/aaa/platforms/<vendor>/")
