"""Gaussian denoise. Run this file on a noisy chart."""

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


def denoise_gaussian(rgb: np.ndarray, sigma: float = 1.1) -> np.ndarray:
    k = max(3, int(round(sigma * 4)) | 1)
    out = cv2.GaussianBlur(rgb, (k, k), sigma)
    return clip01(out)


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    src = color_chart()
    noisy = clip01(src + rng.normal(0, 0.08, src.shape).astype(np.float32))
    clean = denoise_gaussian(noisy, 1.1)
    out = output_dir("isp")
    save_rgb(out / "denoise_noisy.png", noisy)
    path = save_rgb(out / "denoise_result.png", clean)
    print(f"noisy std={float(noisy.std()):.3f}  denoised std={float(clean.std()):.3f}")
    print(f"wrote {path}")
