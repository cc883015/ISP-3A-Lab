"""Embodied perceive → act loop. Run this file to list the pieces."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("embodied: perceive, act, loop")
    print("swap perceive later; keep the loop")
