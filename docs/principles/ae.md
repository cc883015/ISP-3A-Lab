# Auto exposure (AE)

## Idea

Hold scene luma near a target. If the frame is too dark, raise exposure time and/or analog gain. If it is too bright, lower them.

```text
luma = 0.2126 R + 0.7152 G + 0.0722 B     # BT.709, linear
ratio = target / current_luma
exposure_next = clamp(exposure * ratio^k, min, max)
```

`k < 1` damps oscillation.

## Production notes (fill from your debug docs)

- Pre-frames: how many frames before AE is trusted
- Longest exposure vs motion blur (robot / car)
- Highlight priority vs face priority
- Gain vs exposure split (noise vs blur)

## Expand later

- [ ] Metering: center-weight, spot, histogram
- [ ] Flicker (50/60 Hz) line period
- [ ] Sony / MTK AE stat windows
