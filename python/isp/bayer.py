"""RGB ↔ Bayer RGGB. Run this file to mosaic a color chart."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import color_chart


def rgb_to_bayer_rggb(rgb: np.ndarray) -> np.ndarray:
    """Keep one color per pixel. Pattern: R G / G B."""
    raw = np.zeros(rgb.shape[:2], dtype=np.float32)
    raw[0::2, 0::2] = rgb[0::2, 0::2, 0]
    raw[0::2, 1::2] = rgb[0::2, 1::2, 1]
    raw[1::2, 0::2] = rgb[1::2, 0::2, 1]
    raw[1::2, 1::2] = rgb[1::2, 1::2, 2]
    return raw


def bayer_preview(raw: np.ndarray) -> np.ndarray:
    """False-color view of the mosaic (not a demosaic)."""
    rgb = np.zeros(raw.shape + (3,), dtype=np.float32)
    rgb[0::2, 0::2, 0] = raw[0::2, 0::2]
    rgb[0::2, 1::2, 1] = raw[0::2, 1::2]
    rgb[1::2, 0::2, 1] = raw[1::2, 0::2]
    rgb[1::2, 1::2, 2] = raw[1::2, 1::2]
    return rgb


if __name__ == "__main__":
    rgb = color_chart()
    raw = rgb_to_bayer_rggb(rgb)
    preview = bayer_preview(raw)
    out = output_dir("isp")
    save_rgb(out / "bayer_source.png", rgb)
    path = save_rgb(out / "bayer_preview.png", preview)
    print(f"raw shape={raw.shape} mean={float(raw.mean()):.3f}")
    print(f"wrote {path}")
