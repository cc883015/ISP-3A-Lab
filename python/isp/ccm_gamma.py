"""Color correction matrix and gamma. Run this file to apply both."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, save_rgb
from common.paths import output_dir
from common.scenes import color_chart

# Mild camera-to-display matrix (teaching default, not a measured CCM).
DEFAULT_CCM = np.array(
    [
        [1.15, -0.10, -0.05],
        [-0.08, 1.18, -0.10],
        [-0.04, -0.16, 1.20],
    ],
    dtype=np.float32,
)


def apply_ccm(rgb: np.ndarray, ccm: np.ndarray = DEFAULT_CCM) -> np.ndarray:
    flat = rgb.reshape(-1, 3)
    return clip01(flat.dot(ccm.T).reshape(rgb.shape))


def apply_gamma(rgb: np.ndarray, gamma: float = 2.2) -> np.ndarray:
    return clip01(np.power(np.clip(rgb, 0.0, 1.0), 1.0 / gamma))


if __name__ == "__main__":
    src = color_chart() * 0.55
    ccm = apply_ccm(src)
    out = apply_gamma(ccm, 2.2)
    folder = output_dir("isp")
    save_rgb(folder / "ccm_linear.png", src)
    save_rgb(folder / "ccm_after_matrix.png", ccm)
    path = save_rgb(folder / "ccm_gamma.png", out)
    print(f"input mean={src.mean():.3f}  after CCM+gamma mean={out.mean():.3f}")
    print(f"wrote {path}")
