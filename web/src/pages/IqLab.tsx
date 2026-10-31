import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { analyzeImages, type AnalyzeResult, type Principle } from "../lib/api";

export function IqLab() {
  const [image, setImage] = useState<File | null>(null);
  const [reference, setReference] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [result, setResult] = useState<AnalyzeResult | null>(null);
  const [principles, setPrinciples] = useState<Record<string, Principle> | null>(null);
  const [error, setError] = useState<string>("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    fetch("/api/iq/principles")
      .then((res) => (res.ok ? res.json() : Promise.reject(new Error("API 未启动 / API is down"))))
      .then(setPrinciples)
      .catch((err: Error) => setError(err.message));
  }, []);

  function onImage(file: File | null) {
    setImage(file);
    setResult(null);
    if (file) {
      setPreview(URL.createObjectURL(file));
    } else {
      setPreview("");
    }
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!image) {
      setError("先选一张测试图 / choose a test image");
      return;
    }
    setBusy(true);
    setError("");
    try {
      setResult(await analyzeImages(image, reference));
    } catch (err) {
      setError(err instanceof Error ? err.message : "analyze failed");
    } finally {
      setBusy(false);
    }
  }

  const shown = result?.principles ?? principles;

  return (
    <div className="page iq">
      <p className="crumb">
        <Link to="/">工具 / Tools</Link> / 画质实验室
      </p>
      <h1>画质实验室 / IQ lab</h1>
      <p className="lede">
        页面不写公式。数字来自 <code>python/metrics/analyze.py</code> → CIE76 ΔE 与块 SNR。
        <br />
        The UI does not own the math. Numbers come from the existing Python metrics.
      </p>

      <div className="split">
        <form className="panel" onSubmit={onSubmit}>
          <label>
            测试图 / Test image
            <input type="file" accept="image/*" onChange={(e) => onImage(e.target.files?.[0] ?? null)} />
          </label>
          <label>
            参考图 / Reference（可选，才算 ΔE）
            <input type="file" accept="image/*" onChange={(e) => setReference(e.target.files?.[0] ?? null)} />
          </label>
          <button className="btn" type="submit" disabled={busy}>
            {busy ? "计算中 / running" : "调用 ΔE / SNR"}
          </button>
          {preview ? <img className="preview" src={preview} alt="test preview" /> : null}
          {error ? <p className="error">{error}</p> : null}
        </form>

        <aside className="panel">
          {result ? (
            <>
              <dl className="metrics">
                <div>
                  <dt>Patch SNR</dt>
                  <dd>{result.snr_db.toFixed(2)} dB</dd>
                </div>
                <div>
                  <dt>CIE76 ΔE mean</dt>
                  <dd>{result.delta_e_mean == null ? "—" : result.delta_e_mean.toFixed(2)}</dd>
                </div>
                <div>
                  <dt>CIE76 ΔE max</dt>
                  <dd>{result.delta_e_max == null ? "—" : result.delta_e_max.toFixed(2)}</dd>
                </div>
              </dl>
              <p className="hint">
                ROI {result.snr_roi.size}×{result.snr_roi.size} @ ({result.snr_roi.x}, {result.snr_roi.y}) · {result.width}×{result.height}
              </p>
              <Histogram values={result.histogram} />
            </>
          ) : (
            <p className="placeholder">结果在右侧 / results land here</p>
          )}

          {shown ? (
            <div className="principle-list">
              <h2>原理 / Principles</h2>
              {Object.values(shown).map((item) => (
                <article key={item.id}>
                  <strong>{item.name_zh}</strong>
                  <span>{item.name_en}</span>
                  <p>{item.note_zh}</p>
                  <p className="en">{item.note_en}</p>
                  <code>{item.code}</code>
                </article>
              ))}
            </div>
          ) : null}
        </aside>
      </div>
    </div>
  );
}

function Histogram({ values }: { values: number[] }) {
  const max = Math.max(...values, 1e-6);
  return (
    <div className="hist" aria-label="luma histogram">
      {values.map((value, i) => (
        <i key={i} style={{ height: `${(value / max) * 100}%` }} />
      ))}
    </div>
  );
}
