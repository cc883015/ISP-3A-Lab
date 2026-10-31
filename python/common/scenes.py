"""Synthetic scenes for every demo. Run this file to dump the scene pack."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, save_rgb
from common.paths import output_dir


def color_chart(height: int = 240, width: int = 360) -> np.ndarray:
    """6x4 saturated patches, similar in spirit to a ColorChecker."""
    colors = np.array(
        [
            [0.46, 0.33, 0.26],
            [0.77, 0.58, 0.50],
            [0.36, 0.48, 0.61],
            [0.35, 0.45, 0.26],
            [0.50, 0.47, 0.67],
            [0.35, 0.61, 0.56],
            [0.86, 0.48, 0.18],
            [0.28, 0.36, 0.65],
            [0.76, 0.33, 0.38],
            [0.36, 0.23, 0.42],
            [0.62, 0.73, 0.25],
            [0.90, 0.63, 0.10],
            [0.16, 0.24, 0.53],
            [0.22, 0.57, 0.27],
            [0.69, 0.16, 0.16],
            [0.93, 0.80, 0.08],
            [0.73, 0.33, 0.60],
            [0.00, 0.53, 0.66],
            [0.96, 0.96, 0.96],
            [0.63, 0.63, 0.63],
            [0.38, 0.38, 0.38],
            [0.20, 0.20, 0.20],
            [0.10, 0.10, 0.10],
            [0.05, 0.05, 0.05],
        ],
        dtype=np.float32,
    )
    rows, cols = 4, 6
    img = np.zeros((height, width, 3), dtype=np.float32)
    ph, pw = height // rows, width // cols
    for i, color in enumerate(colors):
        r, c = divmod(i, cols)
        img[r * ph : (r + 1) * ph, c * pw : (c + 1) * pw] = color
    return img


def apply_vignette(rgb: np.ndarray, strength: float = 0.65) -> np.ndarray:
    h, w = rgb.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cy, cx = (h - 1) / 2.0, (w - 1) / 2.0
    rr = np.sqrt(((yy - cy) / cy) ** 2 + ((xx - cx) / cx) ** 2)
    gain = 1.0 - strength * np.clip(rr, 0.0, 1.0) ** 2
    return clip01(rgb * gain[..., None])


def garage_split(height: int = 240, width: int = 360) -> np.ndarray:
    """Cool left / warm right — two illuminants, AWB stress case."""
    img = color_chart(height, width)
    mid = width // 2
    cool = np.array([0.75, 0.85, 1.15], dtype=np.float32)
    warm = np.array([1.25, 0.95, 0.65], dtype=np.float32)
    img[:, :mid] = clip01(img[:, :mid] * cool)
    img[:, mid:] = clip01(img[:, mid:] * warm)
    return img


def highlight_interior(height: int = 240, width: int = 360) -> np.ndarray:
    """Dark room + bright window for AE."""
    img = np.full((height, width, 3), 0.08, dtype=np.float32)
    img[height // 6 : height // 2, width // 2 :] = 0.95
    img[height // 2 :, : width // 2] = np.array([0.18, 0.16, 0.12], dtype=np.float32)
    img[20:70, 20:90] = np.array([0.55, 0.22, 0.18], dtype=np.float32)
    return img


def slanted_edge(height: int = 200, width: int = 280, angle_deg: float = 5.0) -> np.ndarray:
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    theta = np.deg2rad(angle_deg)
    line = (xx - width * 0.45) * np.cos(theta) + (yy - height * 0.5) * np.sin(theta)
    edge = 0.08 + 0.84 * (1.0 / (1.0 + np.exp(np.clip(-line * 6.0, -40.0, 40.0))))
    return np.repeat(edge[..., None], 3, axis=2).astype(np.float32)


def chessboard(squares: int = 7, square: int = 28) -> np.ndarray:
    n = squares * square
    img = np.zeros((n, n, 3), dtype=np.float32)
    for y in range(squares):
        for x in range(squares):
            if (x + y) % 2 == 0:
                img[y * square : (y + 1) * square, x * square : (x + 1) * square] = 0.92
            else:
                img[y * square : (y + 1) * square, x * square : (x + 1) * square] = 0.08
    return img


def red_blob_scene(height: int = 240, width: int = 320, cx: float = 0.28, cy: float = 0.40, radius: float = 22.0) -> np.ndarray:
    img = np.full((height, width, 3), 0.22, dtype=np.float32)
    yy, xx = np.mgrid[0:height, 0:width].astype(np.float32)
    px, py = cx * (width - 1), cy * (height - 1)
    mask = (xx - px) ** 2 + (yy - py) ** 2 <= radius**2
    img[mask] = np.array([0.85, 0.12, 0.10], dtype=np.float32)
    return img


if __name__ == "__main__":
    out = output_dir("scenes")
    pack = {
        "color_chart.png": color_chart(),
        "vignette.png": apply_vignette(color_chart()),
        "garage_split.png": garage_split(),
        "highlight_interior.png": highlight_interior(),
        "slanted_edge.png": slanted_edge(),
        "chessboard.png": chessboard(),
        "red_blob.png": red_blob_scene(),
    }
    for name, image in pack.items():
        path = save_rgb(out / name, image)
        print(f"wrote {path}")
