"""Interview demos. Run this file to list them."""

from pathlib import Path
import sys

_PY = Path(__file__).resolve().parents[1]
if str(_PY) not in sys.path:
    sys.path.insert(0, str(_PY))

if __name__ == "__main__":
    print("01_isp_pipeline  02_awb_garage  03_ae_highlight  04_af_curve")
    print("05_iq_report     06_robot_calib 07_embodied_loop")
