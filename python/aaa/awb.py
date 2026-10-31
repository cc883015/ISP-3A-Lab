"""AWB estimators. Run this file on the garage two-illuminant scene."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import garage_split
from isp.awb_apply import apply_gains


def gray_world(rgb: np.ndarray) -> tuple[float, float, float]:
    mean = rgb.reshape(-1, 3).mean(axis=0)
    g = float(max(mean[1], 1e-6))
    return g / float(max(mean[0], 1e-6)), 1.0, g / float(max(mean[2], 1e-6))


def white_patch(rgb: np.ndarray, percentile: float = 97.0) -> tuple[float, float, float]:
    hi = np.percentile(rgb.reshape(-1, 3), percentile, axis=0)
    g = float(max(hi[1], 1e-6))
    return g / float(max(hi[0], 1e-6)), 1.0, g / float(max(hi[2], 1e-6))


if __name__ == "__main__":
    src = garage_split()
    gw = gray_world(src)
    wp = white_patch(src)
    out = output_dir("aaa")
    save_rgb(out / "awb_garage.png", src)
    save_rgb(out / "awb_gray_world.png", apply_gains(src, *gw))
    path = save_rgb(out / "awb_white_patch.png", apply_gains(src, *wp))
    print(f"gray_world  R={gw[0]:.3f} G={gw[1]:.3f} B={gw[2]:.3f}")
    print(f"white_patch R={wp[0]:.3f} G={wp[1]:.3f} B={wp[2]:.3f}")
    print("two illuminants in one frame: one global gain cannot fix both sides")
    print(f"wrote {path}")
