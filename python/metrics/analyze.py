"""One entry for IQ numbers used by apps/iq_lab. Run this file on a synthetic pair."""

from __future__ import annotations

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import luma
from common.scenes import color_chart
from metrics.color_delta_e import delta_e76
from metrics.snr import patch_snr_db

PRINCIPLES = {
    "delta_e": {
        "id": "CIE76",
        "name_zh": "CIE76 ΔE（CIELAB）",
        "name_en": "CIE76 ΔE in CIELAB",
        "doc": "docs/principles/metrics.md",
        "code": "python/metrics/color_delta_e.py",
        "note_zh": "sRGB → 线性 RGB → XYZ → Lab，再算欧氏距离。不是 ΔE2000。",
        "note_en": "sRGB → linear RGB → XYZ → Lab, then Euclidean distance. Not ΔE2000.",
    },
    "snr": {
        "id": "patch-SNR",
        "name_zh": "块 SNR（亮度 μ/σ）",
        "name_en": "Patch SNR (luma μ/σ)",
        "doc": "docs/principles/metrics.md",
        "code": "python/metrics/snr.py",
        "note_zh": "SNR = 20 log10(mean / std)，取画面中心一块。平坦补丁才有意义。",
        "note_en": "SNR = 20 log10(mean / std) on a center patch. Meaningful on a flat field.",
    },
}


def decode_bgr_to_rgb01(data: bytes) -> np.ndarray:
    buf = np.frombuffer(data, dtype=np.uint8)
    bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("could not decode image")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    return rgb


def center_roi(height: int, width: int, frac: float = 0.28) -> tuple[int, int, int]:
    size = max(16, int(min(height, width) * frac))
    y0 = (height - size) // 2
    x0 = (width - size) // 2
    return y0, x0, size


def luma_histogram(rgb: np.ndarray, bins: int = 32) -> list[float]:
    y = luma(rgb)
    hist, _ = np.histogram(y, bins=bins, range=(0.0, 1.0))
    total = float(hist.sum()) or 1.0
    return (hist.astype(np.float64) / total).tolist()


def analyze(test_rgb: np.ndarray, ref_rgb: np.ndarray | None = None) -> dict:
    h, w = test_rgb.shape[:2]
    y0, x0, size = center_roi(h, w)
    out: dict = {
        "width": w,
        "height": h,
        "snr_db": patch_snr_db(test_rgb, y0, x0, size),
        "snr_roi": {"y": y0, "x": x0, "size": size},
        "histogram": luma_histogram(test_rgb),
        "principles": PRINCIPLES,
    }
    if ref_rgb is not None:
        if ref_rgb.shape[:2] != (h, w):
            ref_rgb = cv2.resize(ref_rgb, (w, h), interpolation=cv2.INTER_AREA)
            ref_rgb = np.clip(ref_rgb, 0.0, 1.0).astype(np.float32)
        de = delta_e76(ref_rgb, test_rgb)
        out["delta_e_mean"] = float(de.mean())
        out["delta_e_max"] = float(de.max())
    else:
        out["delta_e_mean"] = None
        out["delta_e_max"] = None
    return out


if __name__ == "__main__":
    ref = color_chart()
    test = np.clip(ref * np.array([1.12, 0.94, 0.86], dtype=np.float32), 0, 1)
    rng = np.random.default_rng(0)
    test = np.clip(test + rng.normal(0, 0.02, test.shape).astype(np.float32), 0, 1)
    result = analyze(test, ref)
    print(
        f"SNR={result['snr_db']:.2f} dB  "
        f"ΔE mean={result['delta_e_mean']:.2f}  "
        f"ΔE max={result['delta_e_max']:.2f}"
    )
    print("principles:", result["principles"]["delta_e"]["id"], result["principles"]["snr"]["id"])
