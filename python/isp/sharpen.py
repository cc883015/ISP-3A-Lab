"""Unsharp mask. Run this file on a slightly blurred chart."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, save_rgb
from common.paths import output_dir
from common.scenes import color_chart


def sharpen_unsharp(rgb: np.ndarray, amount: float = 0.7, sigma: float = 1.0) -> np.ndarray:
    blur = cv2.GaussianBlur(rgb, (0, 0), sigma)
    return clip01(rgb + amount * (rgb - blur))


if __name__ == "__main__":
    src = color_chart()
    soft = cv2.GaussianBlur(src, (0, 0), 1.2)
    sharp = sharpen_unsharp(soft, 0.9, 1.0)
    out = output_dir("isp")
    save_rgb(out / "sharpen_soft.png", soft)
    path = save_rgb(out / "sharpen_result.png", sharp)
    print(f"soft mean={float(soft.mean()):.3f}  sharp mean={float(sharp.mean()):.3f}")
    print(f"wrote {path}")
