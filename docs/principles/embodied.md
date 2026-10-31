# Embodied loop

Embodied vision is not “run a detector then stop”. It is:

```text
sense → decide → act → sense
```

This repo’s loop is deliberately small:

- **perceive:** find a colored blob, read luma
- **act:** turn toward the blob, or ask AE to move
- **loop:** repeat until the blob is centered and luma is near target

A foundation model can replace `perceive` later. The loop shape stays.

## Expand later

- [ ] Depth / stereo
- [ ] Grasp or nav command instead of a 2D nudge
- [ ] When to trust the frame (AE converged, not saturated)
