"""Image quality tests. Run this file to list the metrics."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("metrics: snr, color_delta_e, mtf_sfr, shading, report")
    print("Separate from 3A on purpose — 3A changes capture, metrics judge the picture.")
