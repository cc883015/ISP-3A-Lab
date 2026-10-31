"""Find a red blob and read luma. Run this file on a synthetic scene."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma, save_rgb
from common.paths import output_dir
from common.scenes import red_blob_scene


def perceive(rgb: np.ndarray) -> dict:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mask = (r > 0.55) & (r > g + 0.25) & (r > b + 0.25)
    if not np.any(mask):
        return {"found": False, "cx": None, "cy": None, "luma": float(luma(rgb).mean())}
    ys, xs = np.nonzero(mask)
    cx = float(xs.mean() / (rgb.shape[1] - 1))
    cy = float(ys.mean() / (rgb.shape[0] - 1))
    return {"found": True, "cx": cx, "cy": cy, "luma": float(luma(rgb).mean())}


if __name__ == "__main__":
    scene = red_blob_scene(cx=0.28, cy=0.40)
    obs = perceive(scene)
    path = save_rgb(output_dir("embodied") / "perceive.png", scene)
    print(obs)
    print(f"wrote {path}")
