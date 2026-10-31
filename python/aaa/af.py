"""Contrast AF scores. Run this file to print a focus curve."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma, save_rgb
from common.paths import output_dir
from common.scenes import color_chart


def tenengrad(rgb: np.ndarray) -> float:
    y = luma(rgb).astype(np.float32)
    gx = cv2.Sobel(y, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(y, cv2.CV_32F, 0, 1, ksize=3)
    return float(np.mean(gx * gx + gy * gy))


def laplacian_var(rgb: np.ndarray) -> float:
    y = luma(rgb).astype(np.float32)
    lap = cv2.Laplacian(y, cv2.CV_32F, ksize=3)
    return float(lap.var())


def blur_at(rgb: np.ndarray, sigma: float) -> np.ndarray:
    if sigma <= 0.05:
        return rgb
    return cv2.GaussianBlur(rgb, (0, 0), sigma)


if __name__ == "__main__":
    sharp = color_chart()
    sigmas = [2.4, 1.6, 1.0, 0.5, 0.15, 0.5, 1.2]
    out = output_dir("aaa")
    print("sigma  tenengrad  laplacian_var")
    scores = []
    for i, sigma in enumerate(sigmas):
        frame = blur_at(sharp, sigma)
        t = tenengrad(frame)
        v = laplacian_var(frame)
        scores.append(t)
        save_rgb(out / f"af_sigma_{sigma:.2f}.png", frame)
        print(f"{sigma:5.2f}  {t:9.4f}  {v:13.4f}")
    peak = sigmas[int(np.argmax(scores))]
    print(f"peak tenengrad at sigma={peak:.2f} (smaller blur = sharper)")
    print(f"wrote {out}")
