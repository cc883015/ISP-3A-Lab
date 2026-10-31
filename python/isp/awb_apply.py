"""Apply AWB gains to RGB. Run this file with gray-world gains."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, save_rgb
from common.paths import output_dir
from common.scenes import garage_split


def apply_gains(rgb: np.ndarray, r_gain: float, g_gain: float = 1.0, b_gain: float = 1.0) -> np.ndarray:
    gains = np.array([r_gain, g_gain, b_gain], dtype=np.float32)
    return clip01(rgb * gains)


if __name__ == "__main__":
    src = garage_split()
    mean = src.reshape(-1, 3).mean(axis=0)
    r_gain = float(mean[1] / max(mean[0], 1e-6))
    b_gain = float(mean[1] / max(mean[2], 1e-6))
    out = apply_gains(src, r_gain, 1.0, b_gain)
    folder = output_dir("isp")
    save_rgb(folder / "awb_apply_before.png", src)
    path = save_rgb(folder / "awb_apply_after.png", out)
    print(f"gains R={r_gain:.3f} G=1.000 B={b_gain:.3f}")
    print(f"wrote {path}")
