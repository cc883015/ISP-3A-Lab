# ISP pipeline

## Order used in this repo

1. Bayer mosaic (or load RAW)
2. Demosaic (bilinear)
3. Lens shading correction
4. Apply AWB gains
5. Color correction matrix
6. Gamma
7. Denoise
8. Sharpen

Real silicon reorders some of this (LSC and black level are usually earlier; denoise may be RAW-domain). Write the vendor order here when you add a platform.

## Blocks

**Demosaic.** Each pixel has one color. Missing colors are interpolated. Bilinear is the teaching baseline. Malvar–He–Cutler and AHD are common next steps.

**LSC.** Optics vignette the corners. A radial or tabulated gain flattens the field.

**CCM.** 3×3 maps camera RGB toward a working space. Wrong CCM looks like a hue shift, not an AWB failure.

**Gamma.** `out = in^(1/γ)` for display. Metrics on gamma-encoded vs linear data are not the same thing.

## Expand later

- [ ] Black level / white level
- [ ] Tone mapping / local contrast
- [ ] HDR merge
- [ ] Vendor LUT locations
