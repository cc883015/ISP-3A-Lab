# Auto focus (AF)

## Idea

A sharp image has more high-frequency energy. Sweep focus (or blur a synthetic lens) and pick the peak.

**Tenengrad.** Mean of `Gx² + Gy²` after Sobel.

**Laplacian variance.** Variance of a Laplacian response.

## Production notes (fill from Huaqin-style work)

- Objective curve vs subjective peeking
- Hysteresis so AF does not hunt
- Latency / power of the AF thread
- PDAF / laser vs contrast AF

## Expand later

- [ ] Fine vs coarse search
- [ ] ROI (face, object)
- [ ] Vendor contrast / PDAF confidence
