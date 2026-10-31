"""RAW → RGB teaching pipeline. Run this file to dump every stage."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import apply_vignette, color_chart
from isp.awb_apply import apply_gains
from isp.bayer import bayer_preview, rgb_to_bayer_rggb
from isp.ccm_gamma import apply_ccm, apply_gamma
from isp.demosaic import demosaic_bilinear_rggb
from isp.denoise import denoise_gaussian
from isp.lsc import apply_lsc
from isp.sharpen import sharpen_unsharp


def run_pipeline(rgb_scene: np.ndarray, awb_gains=(1.0, 1.0, 1.0)) -> dict:
    shaded = apply_vignette(rgb_scene, 0.45)
    raw = rgb_to_bayer_rggb(shaded)
    dem = demosaic_bilinear_rggb(raw)
    lsc = apply_lsc(dem, 0.45)
    awb = apply_gains(lsc, *awb_gains)
    ccm = apply_ccm(awb)
    gamma = apply_gamma(ccm, 2.2)
    den = denoise_gaussian(gamma, 0.6)
    sharp = sharpen_unsharp(den, 0.35, 0.8)
    return {
        "scene": rgb_scene,
        "raw_preview": bayer_preview(raw),
        "demosaic": dem,
        "lsc": lsc,
        "awb": awb,
        "gamma": gamma,
        "out": sharp,
    }


if __name__ == "__main__":
    stages = run_pipeline(color_chart())
    out = output_dir("isp")
    last = None
    for name, image in stages.items():
        last = save_rgb(out / f"pipeline_{name}.png", image)
        print(f"{name:12s} mean={float(np.mean(image)):.3f}")
    print(f"wrote {last}")
