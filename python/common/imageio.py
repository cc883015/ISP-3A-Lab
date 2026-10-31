"""Save and convert float images. Run this file to write a gradient PNG."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.paths import output_dir


def to_u8(image: np.ndarray) -> np.ndarray:
    arr = np.clip(image, 0.0, 1.0)
    return (arr * 255.0 + 0.5).astype(np.uint8)


def save_rgb(path: Path, image: np.ndarray) -> Path:
    import cv2

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    rgb = image if image.ndim == 3 else np.repeat(image[..., None], 3, axis=2)
    bgr = to_u8(rgb)[:, :, ::-1]
    if not cv2.imwrite(str(path), bgr):
        raise RuntimeError(f"failed to write {path}")
    return path


def luma(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def clip01(image: np.ndarray) -> np.ndarray:
    return np.clip(image, 0.0, 1.0).astype(np.float32)


if __name__ == "__main__":
    h, w = 80, 160
    xs = np.linspace(0, 1, w, dtype=np.float32)
    grad = np.stack([np.tile(xs, (h, 1)), np.zeros((h, w), np.float32), 1.0 - np.tile(xs, (h, 1))], axis=-1)
    path = save_rgb(output_dir("common") / "gradient.png", grad)
    print(f"luma mean={float(luma(grad).mean()):.3f}")
    print(f"wrote {path}")
