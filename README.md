# isp-3a-lab

ISP pipeline + 3A + IQ lab, from RAW to a control loop.

Same repo covers four job tracks:

| Track | Look at |
|---|---|
| ISP tuning | `python/metrics`, `python/aaa/af.py`, `docs/principles` |
| Image-driven / 3A | `python/isp`, `python/aaa`, `c/src` |
| Robot vision | `python/robot` |
| Embodied AI | `python/embodied` |

Python is the experiment and interview layer. C is the vendor-style core. Algorithm notes live in `docs/principles` and stay language-agnostic. Vendor 3A / ISP (Sony, MTK, Qualcomm, …) goes under each module’s `platforms/` folder later — those folders are extension points, not implementations yet.

This is not vendor ISP source. It is a reproducible lab that matches how those pipelines are reasoned about.

---

## Layout

```text
docs/principles/     algorithm notes (fill / expand anytime)
python/isp/          generic ISP, plus platforms/ for vendor hooks
python/aaa/          generic AE / AWB / AF, plus platforms/
python/metrics/      image-quality tests (separate from 3A)
python/robot/        calibration, undistort, motion AE, latency
python/embodied/     perceive → act loop
c/                   C99 library + small demos for ISP / 3A / SNR
data/                drop real RAW / charts later; demos synthesize data
output/              generated images and reports (gitignored)
```

---

## Run Python

From the repo root, every `python/**/*.py` file can run on its own:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# examples
python python/isp/demosaic.py
python python/aaa/awb.py
python python/metrics/report.py
python python/robot/calib.py
python python/embodied/loop.py
```

Or run the full smoke list:

```bash
bash scripts/smoke_python.sh
```

Outputs land in `output/<module>/`.

---

## Build C

C covers the bits that production camera code usually ships in C: Bayer, demosaic, AE, AWB, AF, SNR.

```bash
make -C c
./c/bin/demo_pipeline
./c/bin/demo_ae
```

Robot calibration and the embodied loop stay Python-only for now (OpenCV). The algorithm notes still apply.

---

## Add a vendor later (Sony / MTK / …)

Do not edit the generic `ae.py` / `awb.py` / `af.py` into vendor code.

1. Put debug notes in `docs/principles/` or `python/aaa/platforms/<vendor>/NOTES.md`
2. Add `python/aaa/platforms/<vendor>/ae.py` (same for AWB / AF)
3. Implement the same function names as the generic files
4. Mirror headers under `c/src/platforms/<vendor>/` if you have a C dump

See `docs/platforms.md`.

---

## Job mapping

See `docs/job-mapping.md`.
