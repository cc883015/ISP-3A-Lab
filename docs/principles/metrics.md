# Image quality tests

This folder is separate from 3A on purpose. 3A changes the capture. Metrics judge the picture.

| Metric | What it answers | File |
|---|---|---|
| SNR | How noisy is a flat patch? | `python/metrics/snr.py` |
| ΔE | How far is a color from the reference? | `python/metrics/color_delta_e.py` |
| SFR / MTF (simplified) | How much edge contrast survives? | `python/metrics/mtf_sfr.py` |
| Shading | Corner / center brightness | `python/metrics/shading.py` |

Lab instruments (Imatest and friends) use charts, ROIs, and a lot more care. The code here is the same *questions*, not a replacement.

## Expand later

- [ ] ColorChecker 24 patch layout and reference Lab
- [ ] ISO 12233 slanted-edge SFR
- [ ] Dynamic range from a step chart
- [ ] Vendor test SOP mapping
