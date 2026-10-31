"""Corner / center shading. Run this file on a vignetted gray field."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma, save_rgb
from common.paths import output_dir
from common.scenes import apply_vignette


def shading_ratio(rgb: np.ndarray, patch: int = 16) -> float:
    y = luma(rgb)
    h, w = y.shape
    center = float(y[h // 2 - patch : h // 2 + patch, w // 2 - patch : w // 2 + patch].mean())
    corners = [
        float(y[:patch, :patch].mean()),
        float(y[:patch, -patch:].mean()),
        float(y[-patch:, :patch].mean()),
        float(y[-patch:, -patch:].mean()),
    ]
    return float(np.mean(corners) / max(center, 1e-6))


if __name__ == "__main__":
    flat = np.full((200, 260, 3), 0.55, dtype=np.float32)
    vignette = apply_vignette(flat, 0.7)
    out = output_dir("metrics")
    save_rgb(out / "shading_flat.png", flat)
    save_rgb(out / "shading_vignette.png", vignette)
    print(f"flat corner/center     = {shading_ratio(flat):.3f}")
    print(f"vignette corner/center = {shading_ratio(vignette):.3f}")
