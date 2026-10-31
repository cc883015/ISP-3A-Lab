"""See → decide → act. Run this file to walk a blob to the image center."""

from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, save_rgb
from common.paths import output_dir
from common.scenes import red_blob_scene
from embodied.act import act
from embodied.perceive import perceive


def step_scene(cx: float, cy: float, exposure: float, cmd: dict) -> tuple[float, float, float, np.ndarray]:
    cx = float(np.clip(cx + 0.45 * cmd["turn_x"], 0.08, 0.92))
    cy = float(np.clip(cy + 0.45 * cmd["turn_y"], 0.08, 0.92))
    exposure = float(np.clip(exposure * cmd["exposure_scale"], 0.4, 2.5))
    frame = clip01(red_blob_scene(cx=cx, cy=cy) * exposure)
    return cx, cy, exposure, frame


if __name__ == "__main__":
    cx, cy, exposure = 0.22, 0.38, 0.7
    out = output_dir("embodied")
    print(f"{'i':>3s}  {'cx':>6s}  {'cy':>6s}  {'luma':>6s}  {'exp':>6s}")
    for i in range(10):
        frame = clip01(red_blob_scene(cx=cx, cy=cy) * exposure)
        obs = perceive(frame)
        cmd = act(obs)
        save_rgb(out / f"loop_{i:02d}.png", frame)
        print(f"{i:3d}  {cx:6.3f}  {cy:6.3f}  {obs['luma']:6.3f}  {exposure:6.3f}")
        if obs["found"] and abs(cx - 0.5) < 0.04 and abs(cy - 0.5) < 0.04:
            print("centered")
            break
        cx, cy, exposure, frame = step_scene(cx, cy, exposure, cmd)
    print(f"wrote frames in {out}")
