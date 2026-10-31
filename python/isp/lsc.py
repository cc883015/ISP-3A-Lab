"""Lens shading correction. Run this file to flatten a vignetted chart."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, luma, save_rgb
from common.paths import output_dir
from common.scenes import apply_vignette, color_chart


def shading_gain(height: int, width: int, strength: float = 0.65) -> np.ndarray:
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    cy, cx = (height - 1) / 2.0, (width - 1) / 2.0
    rr = np.sqrt(((yy - cy) / cy) ** 2 + ((xx - cx) / cx) ** 2)
    return (1.0 / np.clip(1.0 - strength * np.clip(rr, 0.0, 1.0) ** 2, 0.15, 1.0)).astype(np.float32)


def apply_lsc(rgb: np.ndarray, strength: float = 0.65) -> np.ndarray:
    gain = shading_gain(rgb.shape[0], rgb.shape[1], strength)
    return clip01(rgb * gain[..., None])


if __name__ == "__main__":
    src = color_chart()
    shaded = apply_vignette(src, 0.65)
    fixed = apply_lsc(shaded, 0.65)
    out = output_dir("isp")
    save_rgb(out / "lsc_shaded.png", shaded)
    path = save_rgb(out / "lsc_corrected.png", fixed)
    print(f"center luma shaded={float(luma(shaded)[120, 180]):.3f}  corrected={float(luma(fixed)[120, 180]):.3f}")
    print(f"corner luma shaded={float(luma(shaded)[10, 10]):.3f}  corrected={float(luma(fixed)[10, 10]):.3f}")
    print(f"wrote {path}")
