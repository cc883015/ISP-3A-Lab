"""Turn observation into a small command. Run this file with a fake observation."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))


def act(obs: dict, target_luma: float = 0.36) -> dict:
    if not obs.get("found"):
        return {"turn_x": 0.0, "turn_y": 0.0, "exposure_scale": 1.0, "reason": "no target"}
    turn_x = 0.5 - float(obs["cx"])
    turn_y = 0.5 - float(obs["cy"])
    luma_now = float(obs["luma"])
    if luma_now < 1e-6:
        scale = 1.4
    else:
        scale = float(min(1.6, max(0.6, target_luma / luma_now)))
    return {
        "turn_x": turn_x,
        "turn_y": turn_y,
        "exposure_scale": scale,
        "reason": "track + AE",
    }


if __name__ == "__main__":
    fake = {"found": True, "cx": 0.28, "cy": 0.40, "luma": 0.22}
    cmd = act(fake)
    print("obs", fake)
    print("cmd", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in cmd.items()})
    print("positive turn_x means move the camera so the blob slides right toward center")
