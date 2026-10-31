"""Auto exposure. Run this file to converge a dark interior + bright window."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.imageio import clip01, luma, save_rgb
from common.paths import output_dir
from common.scenes import highlight_interior


@dataclass
class AeState:
    exposure: float = 1.0
    gain: float = 1.0


def apply_exposure(rgb: np.ndarray, state: AeState) -> np.ndarray:
    return clip01(rgb * (state.exposure * state.gain))


def ae_step(rgb: np.ndarray, state: AeState, target: float = 0.36, damp: float = 0.7,
            min_exp: float = 0.05, max_exp: float = 8.0) -> AeState:
    current = float(luma(rgb).mean())
    if current < 1e-6:
        return AeState(exposure=max_exp, gain=state.gain)
    ratio = (target / current) ** damp
    exposure = float(np.clip(state.exposure * ratio, min_exp, max_exp))
    return AeState(exposure=exposure, gain=state.gain)


if __name__ == "__main__":
    scene = highlight_interior()
    state = AeState(exposure=0.35)
    out = output_dir("aaa")
    save_rgb(out / "ae_start.png", apply_exposure(scene, state))
    print("frame  exposure  luma")
    for i in range(8):
        frame = apply_exposure(scene, state)
        y = float(luma(frame).mean())
        print(f"{i:5d}  {state.exposure:8.3f}  {y:.3f}")
        state = ae_step(frame, state, target=0.36)
    path = save_rgb(out / "ae_converged.png", apply_exposure(scene, state))
    print(f"final exposure={state.exposure:.3f} luma={float(luma(apply_exposure(scene, state)).mean()):.3f}")
    print(f"wrote {path}")
