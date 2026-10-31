"""Barrel distortion and undistort. Run this file to write before/after."""

from pathlib import Path
import sys

import cv2
import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import save_rgb
from common.paths import output_dir
from common.scenes import chessboard


def distort_barrel(rgb: np.ndarray, k1: float = -0.22) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h, w = rgb.shape[:2]
    k = np.array([[w * 0.9, 0, w / 2], [0, w * 0.9, h / 2], [0, 0, 1]], dtype=np.float32)
    dist = np.array([k1, 0, 0, 0, 0], dtype=np.float32)
    u8 = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    add = np.array([-k1, 0, 0, 0, 0], dtype=np.float32)
    map1, map2 = cv2.initUndistortRectifyMap(k, add, None, k, (w, h), cv2.CV_32FC1)
    barrel = cv2.remap(u8, map1, map2, cv2.INTER_LINEAR, borderValue=40)
    return barrel.astype(np.float32) / 255.0, k, dist


def undistort(rgb: np.ndarray, k: np.ndarray, dist: np.ndarray) -> np.ndarray:
    u8 = (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    fixed = cv2.undistort(u8, k, dist)
    return fixed.astype(np.float32) / 255.0


if __name__ == "__main__":
    src = chessboard()
    barrel, k, dist = distort_barrel(src, -0.22)
    # The map above applied add=[-k1]=[0.22], so undistort with dist=[0.22,...]
    dist_used = np.array([0.22, 0, 0, 0, 0], dtype=np.float32)
    fixed = undistort(barrel, k, dist_used)
    out = output_dir("robot")
    save_rgb(out / "undistort_src.png", src)
    save_rgb(out / "undistort_barrel.png", barrel)
    path = save_rgb(out / "undistort_fixed.png", fixed)
    print("K =\n", np.round(k, 1))
    print("applied k1=0.22 then undistorted")
    print(f"wrote {path}")
