"""Job track: embodied AI. Perceive → act until the blob is centered."""

from pathlib import Path
import runpy
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("=== demo 07 embodied loop ===")
    runpy.run_path(str(_PY / "embodied" / "loop.py"), run_name="__main__")
