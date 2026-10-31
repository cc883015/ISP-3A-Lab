# Python and C

Industry camera stacks are mostly C (sometimes C++). Python is how you try ideas and make plots. This repo keeps both, on purpose.

## Split

| Layer | Language | Why |
|---|---|---|
| Principle notes | Markdown | Same math for both implementations |
| Experiment, plots, OpenCV, interview demos | Python | Fast to change, every file has a `__main__` |
| Bayer / demosaic / AE / AWB / AF / SNR | C99 + Python | Matches vendor-style code; numbers should agree in spirit |
| Calib / undistort / embodied loop | Python only (v1) | Needs OpenCV; C port later if needed |
| Vendor 3A | later, both | Drop under `platforms/<vendor>/` |

Do not wrap C with Python bindings in v1. Two readable implementations beat one clever ABI.

## How to keep them honest

1. Change the formula in `docs/principles/<topic>.md` first
2. Update Python
3. Update C
4. Run both demos on the same synthetic pattern and compare the printed numbers

## C style here

- C99, no OpenCV
- `float` images, RGB interleaved or single-channel
- Each `c/demos/demo_*.c` is a small `main`
- Vendor folders stay empty until you add a dump
