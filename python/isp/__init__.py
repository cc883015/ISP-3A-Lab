"""Generic ISP. Run this file to list the blocks."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("ISP blocks: bayer, demosaic, lsc, awb_apply, ccm_gamma, denoise, sharpen, pipeline")
    print("Vendor hooks: python/isp/platforms/")
