"""One-page IQ report. Run this file to compare a clean chart vs a degraded copy."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import apply_vignette, color_chart
from metrics.color_delta_e import delta_e76
from metrics.mtf_sfr import edge_contrast
from metrics.shading import shading_ratio
from metrics.snr import patch_snr_db


def report(ref: np.ndarray, test: np.ndarray) -> dict:
    return {
        "snr_db": patch_snr_db(test, 12, 12, 28),
        "delta_e_mean": float(delta_e76(ref, test).mean()),
        "edge_contrast": edge_contrast(test),
        "shading_ratio": shading_ratio(test),
    }


if __name__ == "__main__":
    ref = color_chart()
    rng = np.random.default_rng(2)
    test = apply_vignette(ref, 0.4)
    test = np.clip(test * np.array([1.08, 0.96, 0.88], np.float32), 0, 1)
    test = np.clip(test + rng.normal(0, 0.02, test.shape).astype(np.float32), 0, 1)
    test = cv2.GaussianBlur(test, (0, 0), 0.7)
    ref_m = report(ref, ref)
    tes_m = report(ref, test)
    out = output_dir("metrics")
    save_rgb(out / "report_ref.png", ref)
    save_rgb(out / "report_test.png", test)
    print(f"{'metric':16s}  {'ref':>8s}  {'test':>8s}")
    for key in ref_m:
        print(f"{key:16s}  {ref_m[key]:8.3f}  {tes_m[key]:8.3f}")
    lines = ["metric,ref,test"] + [f"{k},{ref_m[k]:.4f},{tes_m[k]:.4f}" for k in ref_m]
    csv = out / "report.csv"
    csv.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {csv}")
