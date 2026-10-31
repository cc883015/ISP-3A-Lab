"""Chessboard intrinsics. Run this file to calibrate from warped synthetic views."""

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


def _warp_views(board: np.ndarray, count: int = 8) -> list[np.ndarray]:
    h, w = board.shape[:2]
    rng = np.random.default_rng(3)
    views = []
    for _ in range(count):
        inset = 18
        src = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
        jitter = rng.uniform(-inset, inset, size=(4, 2)).astype(np.float32)
        dst = src + jitter
        m = cv2.getPerspectiveTransform(src, dst)
        views.append(cv2.warpPerspective(board, m, (w, h), borderValue=(0.2, 0.2, 0.2)))
    return views


def calibrate(views: list[np.ndarray], squares: int = 7, square: int = 28) -> tuple[np.ndarray, np.ndarray]:
    pattern = (squares - 1, squares - 1)
    objp = np.zeros((pattern[0] * pattern[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0 : pattern[0], 0 : pattern[1]].T.reshape(-1, 2)
    objpoints, imgpoints = [], []
    size = None
    for view in views:
        gray = (np.clip(view, 0, 1) * 255).astype(np.uint8)
        if gray.ndim == 3:
            gray = cv2.cvtColor(gray, cv2.COLOR_RGB2GRAY)
        size = gray.shape[::-1]
        flags = (cv2.CALIB_CB_ADAPTIVE_THRESH
                 | cv2.CALIB_CB_NORMALIZE_IMAGE
                 | cv2.CALIB_CB_FILTER_QUADS)
        ok, corners = cv2.findChessboardCorners(gray, pattern, flags)
        if not ok:
            continue
        corners = cv2.cornerSubPix(
            gray, corners, (5, 5), (-1, -1),
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01),
        )
        objpoints.append(objp)
        imgpoints.append(corners)
    if len(objpoints) < 3:
        raise RuntimeError("not enough chessboard detections — try another seed or more views")
    ok, k, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, size, None, None)
    if not ok:
        raise RuntimeError("calibrateCamera failed")
    return k, dist


if __name__ == "__main__":
    board = chessboard()
    views = _warp_views(board)
    k, dist = calibrate(views)
    out = output_dir("robot")
    save_rgb(out / "calib_board.png", board)
    for i, view in enumerate(views[:3]):
        save_rgb(out / f"calib_view_{i}.png", view)
    print("K =\n", np.round(k, 2))
    print("dist =", np.round(dist.ravel(), 4))
    print(f"used {len(views)} synthetic views")
