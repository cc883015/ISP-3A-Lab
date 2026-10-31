"""Simplified slanted-edge contrast / SFR. Run this file on a sharp vs soft edge."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma, save_rgb
from common.paths import output_dir
from common.scenes import slanted_edge


def edge_contrast(rgb: np.ndarray) -> float:
    """10–90% rise width in pixels on the row-averaged profile. Smaller is sharper."""
    profile = luma(rgb).mean(axis=0)
    lo, hi = float(profile.min()), float(profile.max())
    span = hi - lo
    if span < 1e-6:
        return 0.0
    t10, t90 = lo + 0.1 * span, lo + 0.9 * span
    inside = np.where((profile >= t10) & (profile <= t90))[0]
    return float(inside.size)


def simple_sfr_peak(rgb: np.ndarray) -> float:
    """High-frequency share of |FFT(row-mean gradient)| — a teaching SFR, not ISO 12233."""
    profile = luma(rgb).astype(np.float32).mean(axis=0)
    grad = np.diff(profile)
    spec = np.abs(np.fft.rfft(grad))
    if spec.sum() < 1e-8:
        return 0.0
    mid = spec.size // 3
    return float(spec[mid:].sum() / spec.sum())


if __name__ == "__main__":
    sharp = slanted_edge()
    soft = cv2.GaussianBlur(sharp, (0, 0), 1.8)
    out = output_dir("metrics")
    save_rgb(out / "sfr_sharp.png", sharp)
    save_rgb(out / "sfr_soft.png", soft)
    print(f"sharp rise_px={edge_contrast(sharp):.1f}  hf_share={simple_sfr_peak(sharp):.3f}")
    print(f"soft  rise_px={edge_contrast(soft):.1f}  hf_share={simple_sfr_peak(soft):.3f}")
    print("rise_px should grow and hf_share should drop when the edge is blurred")
