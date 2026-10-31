"""CIE76 ΔE on sRGB patches. Run this file on a shifted chart."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import color_chart


def _srgb_to_linear(srgb: np.ndarray) -> np.ndarray:
    a = 0.055
    return np.where(srgb <= 0.04045, srgb / 12.92, ((srgb + a) / (1 + a)) ** 2.4)


def _linear_to_lab(rgb: np.ndarray) -> np.ndarray:
    m = np.array(
        [[0.4124564, 0.3575761, 0.1804375],
         [0.2126729, 0.7151522, 0.0721750],
         [0.0193339, 0.1191920, 0.9503041]],
        dtype=np.float32,
    )
    xyz = rgb.reshape(-1, 3).dot(m.T)
    w = np.array([0.95047, 1.0, 1.08883], dtype=np.float32)
    t = xyz / w
    delta = 6 / 29
    f = np.where(t > delta**3, np.cbrt(t), t / (3 * delta**2) + 4 / 29)
    L = 116 * f[:, 1] - 16
    a = 500 * (f[:, 0] - f[:, 1])
    b = 200 * (f[:, 1] - f[:, 2])
    return np.stack([L, a, b], axis=1)


def delta_e76(ref_rgb: np.ndarray, test_rgb: np.ndarray) -> np.ndarray:
    lab_r = _linear_to_lab(_srgb_to_linear(np.clip(ref_rgb, 0, 1)))
    lab_t = _linear_to_lab(_srgb_to_linear(np.clip(test_rgb, 0, 1)))
    return np.linalg.norm(lab_r - lab_t, axis=1).reshape(ref_rgb.shape[:2])


if __name__ == "__main__":
    ref = color_chart()
    test = np.clip(ref * np.array([1.15, 0.92, 0.85], dtype=np.float32), 0, 1)
    de = delta_e76(ref, test)
    out = output_dir("metrics")
    save_rgb(out / "delta_e_ref.png", ref)
    save_rgb(out / "delta_e_test.png", test)
    print(f"mean ΔE76 = {float(de.mean()):.2f}  max = {float(de.max()):.2f}")
    print("ΔE ~2 is a common just-noticeable ballpark on a controlled patch")
