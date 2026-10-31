"""IQ lab API. Calls python/metrics/analyze.py — no local ΔE / SNR formulas."""

from __future__ import annotations

from pathlib import Path
import sys

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parents[2]
PY = ROOT / "python"
if str(PY) not in sys.path:
    sys.path.insert(0, str(PY))

from metrics.analyze import PRINCIPLES, analyze, decode_bgr_to_rgb01  # noqa: E402

app = FastAPI(title="ISP-3A-Lab IQ API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "service": "iq-lab"}


@app.get("/api/iq/principles")
def principles() -> dict:
    return PRINCIPLES


@app.post("/api/iq/analyze")
async def analyze_upload(
    image: UploadFile = File(...),
    reference: UploadFile | None = File(None),
) -> dict:
    raw = await image.read()
    if not raw:
        raise HTTPException(400, "empty image")
    try:
        test = decode_bgr_to_rgb01(raw)
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc

    ref = None
    if reference is not None:
        ref_raw = await reference.read()
        if ref_raw:
            try:
                ref = decode_bgr_to_rgb01(ref_raw)
            except ValueError as exc:
                raise HTTPException(400, f"reference: {exc}") from exc

    return analyze(test, ref)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8788)
