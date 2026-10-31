"""Bilinear demosaic for RGGB. Run this file and compare to the source RGB."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import color_chart
from isp.bayer import rgb_to_bayer_rggb

_R_KERNEL = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=np.float32) / 4.0
_G_KERNEL = np.array([[0, 1, 0], [1, 4, 1], [0, 1, 0]], dtype=np.float32) / 4.0


def _conv(channel: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    return cv2.filter2D(channel, -1, kernel, borderType=cv2.BORDER_REPLICATE)


def demosaic_bilinear_rggb(raw: np.ndarray) -> np.ndarray:
    raw = raw.astype(np.float32)
    r_mask = np.zeros_like(raw)
    g_mask = np.zeros_like(raw)
    b_mask = np.zeros_like(raw)
    r_mask[0::2, 0::2] = 1.0
    g_mask[0::2, 1::2] = 1.0
    g_mask[1::2, 0::2] = 1.0
    b_mask[1::2, 1::2] = 1.0
    r = _conv(raw * r_mask, _R_KERNEL)
    g = _conv(raw * g_mask, _G_KERNEL)
    b = _conv(raw * b_mask, _R_KERNEL)
    r[r_mask > 0] = raw[r_mask > 0]
    g[g_mask > 0] = raw[g_mask > 0]
    b[b_mask > 0] = raw[b_mask > 0]
    return np.clip(np.stack([r, g, b], axis=-1), 0.0, 1.0)


if __name__ == "__main__":
    src = color_chart()
    raw = rgb_to_bayer_rggb(src)
    rgb = demosaic_bilinear_rggb(raw)
    mae = float(np.mean(np.abs(rgb - src)))
    out = output_dir("isp")
    save_rgb(out / "demosaic_source.png", src)
    path = save_rgb(out / "demosaic_result.png", rgb)
    print(f"mean abs error vs source RGB = {mae:.4f}")
    print(f"wrote {path}")
