# Auto white balance (AWB)

## Idea

Make a neutral surface look neutral. Two teaching estimators:

**Gray world.** Assume the average scene is gray.

```text
r_gain = G_mean / R_mean
b_gain = G_mean / B_mean
g_gain = 1
```

**White patch.** Assume the brightest pixels are a white reflector. Use a high percentile, not the single max (that one is often a light source).

## Failure cases you already know

- Underground garage entrance: two illuminants in one frame
- Strong colored objects (green trees, red walls) break gray world
- Saturated highlights are not a white patch

## Expand later

- [ ] Illuminant estimation / CCT
- [ ] Scene classifier
- [ ] Vendor AWB gain tables
