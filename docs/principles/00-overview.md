# Pipeline overview

Fill this file as you read papers, vendor docs, or ask a model to explain a block.

```text
photon → sensor → Bayer RAW
      → black level / LSC
      → demosaic
      → AWB gains
      → CCM + gamma
      → denoise / sharpen
      → AE / AF statistics (often from RAW or pre-gamma)
      → RGB / YUV out
```

On a robot or embodied stack the extra question is: **when is this frame safe to act on?** That is latency, AE settle, and calibration — not a new ISP.

## Expand later

- [ ] Where 3A statistics are tapped on MTK vs Sony
- [ ] Which blocks run before / after AWB on the last project you touched
- [ ] Bit depth: 10 / 12 / 14 bit RAW vs the float32 used here
