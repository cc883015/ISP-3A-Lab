"""Patch SNR. Run this file on a clean vs noisy gray card."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma, save_rgb
from common.paths import output_dir


def patch_snr_db(rgb: np.ndarray, y0: int, x0: int, size: int = 40) -> float:
    patch = luma(rgb)[y0 : y0 + size, x0 : x0 + size]
    mean = float(patch.mean())
    std = float(patch.std())
    if std < 1e-8:
        return 99.0
    return 20.0 * float(np.log10(mean / std))


if __name__ == "__main__":
    rng = np.random.default_rng(1)
    clean = np.full((160, 160, 3), 0.42, dtype=np.float32)
    noisy = np.clip(clean + rng.normal(0, 0.04, clean.shape).astype(np.float32), 0, 1)
    out = output_dir("metrics")
    save_rgb(out / "snr_clean.png", clean)
    save_rgb(out / "snr_noisy.png", noisy)
    print(f"clean SNR = {patch_snr_db(clean, 60, 60):.2f} dB")
    print(f"noisy SNR = {patch_snr_db(noisy, 60, 60):.2f} dB")
