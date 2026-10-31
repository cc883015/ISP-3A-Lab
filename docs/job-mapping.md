# Job mapping

One repo, four ways to talk about it. Point interviewers at the files, not the whole tree.

## ISP tuning

- `python/metrics/*` — SNR, ΔE, simplified SFR, shading, one-page report
- `python/aaa/af.py` — focus curve
- `docs/principles/metrics.md`, `docs/principles/af.md`

Talk about: same chart, change one parameter, numbers move. That is the Imatest habit without the vendor GUI.

## Image-driven / 3A

- `python/isp/pipeline.py` and the modules it calls
- `python/aaa/ae.py`, `awb.py`, `af.py`
- `c/src/aaa`, `c/src/isp`

Talk about: module order, AE target / clamp, gray-world vs white-patch, contrast AF. C is there because production ISP is not a notebook.

## Robot vision

- `python/robot/calib.py`, `undistort.py`, `motion_ae.py`, `latency.py`
- `docs/principles/robot.md`

Talk about: camera must be a calibrated, timed sensor. Indoor/outdoor AE and motion blur are the same problems as road-test cameras.

## Embodied AI

- `python/embodied/perceive.py`, `act.py`, `loop.py`
- `docs/principles/embodied.md`

Talk about: vision is inside the control loop. Over-exposed frame → AE command; blob off-center → turn command. Not a VLA model.

## What this repo is not

- Not MediaTek / Sony / Qualcomm firmware
- Not a claim that generic gray-world is a shippable AWB
- Not a substitute for lab instruments
