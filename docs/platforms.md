# Platform extension

Generic files stay generic. Vendor logic goes under `platforms/`.

Sony is the first planned drop (phone / car debug docs → `aaa/platforms/sony/`). The folder is **not** created yet. Add it when you have notes or a binary dump you can talk about in public.

## Contract

Every vendor AE module should expose the same idea as `python/aaa/ae.py`:

```text
ae_step(rgb, state, target_luma) -> new_state
```

Same for AWB (`estimate_gains`) and AF (`focus_score`).

Suggested tree when you add Sony (or MTK, Qualcomm, OmniVision):

```text
python/aaa/platforms/sony/
  NOTES.md          # pasted / rewritten debug notes
  ae.py
  awb.py
  af.py
c/src/platforms/sony/
  ae.c
  awb.c
  af.c
  NOTES.md
```

ISP vendor hooks (LSC tables, CCM presets, tonemap LUTs) go in `python/isp/platforms/<vendor>/`.
IQ test presets (chart ROI, Imatest-like scripts) go in `python/metrics/platforms/<vendor>/`.

## Rules

- Do not copy customer or NDA logs into git
- Rewrite debug notes in your own words
- Keep a one-line comment: which generic algorithm this vendor path replaces
