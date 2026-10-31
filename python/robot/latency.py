"""Time the teaching ISP pipeline. Run this file to print milliseconds per frame."""

from pathlib import Path
import sys
import time

import numpy as np

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

from common.paths import output_dir
from common.scenes import color_chart
from isp.pipeline import run_pipeline


if __name__ == "__main__":
    scene = color_chart(180, 240)
    run_pipeline(scene)  # warmup
    times = []
    for _ in range(12):
        t0 = time.perf_counter()
        run_pipeline(scene)
        times.append((time.perf_counter() - t0) * 1000.0)
    arr = np.array(times)
    out = output_dir("robot")
    (out / "latency.txt").write_text(
        f"n={len(arr)} mean_ms={arr.mean():.2f} p95_ms={np.percentile(arr, 95):.2f}\n",
        encoding="utf-8",
    )
    print(f"pipeline latency  mean={arr.mean():.2f} ms  p95={np.percentile(arr, 95):.2f} ms")
    print("a robot only gets to act on a frame after this plus capture + 3A settle")
