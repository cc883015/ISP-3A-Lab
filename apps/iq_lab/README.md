# IQ lab API

调用 `python/metrics/analyze.py`，也就是：

- CIE76 ΔE → `python/metrics/color_delta_e.py` → `docs/principles/metrics.md`
- 块 SNR → `python/metrics/snr.py` → `docs/principles/metrics.md`

这里不写第二套公式。  
This process does not own a second copy of the formulas.

```bash
# 仓库根目录 / from repo root
source .venv/bin/activate
pip install -r requirements.txt
uvicorn apps.iq_lab.server:app --app-dir apps/iq_lab --host 127.0.0.1 --port 8788
```

或 / or:

```bash
cd apps/iq_lab && python server.py
```
