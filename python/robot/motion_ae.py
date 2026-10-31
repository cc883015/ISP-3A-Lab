"""Exposure vs motion blur. Run this file to compare short and long exposures."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, luma, save_rgb
from common.paths import output_dir
from common.scenes import color_chart
from metrics.snr import patch_snr_db


def motion_blur(rgb: np.ndarray, length: int) -> np.ndarray:
    if length <= 1:
        return rgb
    kernel = np.zeros((1, length), dtype=np.float32)
    kernel[:] = 1.0 / length
    return clip01(cv2.filter2D(rgb, -1, kernel))


if __name__ == "__main__":
    rng = np.random.default_rng(4)
    scene = color_chart() * 0.25
    out = output_dir("robot")
    print(f"{'exp':>6s}  {'blur':>4s}  {'luma':>6s}  {'snr':>6s}")
    for exposure, blur in ((1.0, 1), (2.0, 7), (4.0, 15)):
        frame = clip01(scene * exposure)
        frame = clip01(frame + rng.normal(0, 0.03 / np.sqrt(exposure), frame.shape).astype(np.float32))
        frame = motion_blur(frame, blur)
        save_rgb(out / f"motion_ae_exp{exposure:.0f}.png", frame)
        print(f"{exposure:6.1f}  {blur:4d}  {float(luma(frame).mean()):6.3f}  {patch_snr_db(frame, 20, 20, 30):6.2f}")
    print("longer exposure: brighter, quieter, more smear — robot AE has to pick a side")
