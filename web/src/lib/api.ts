export type Principle = {
  id: string;
  name_zh: string;
  name_en: string;
  doc: string;
  code: string;
  note_zh: string;
  note_en: string;
};

export type AnalyzeResult = {
  width: number;
  height: number;
  snr_db: number;
  snr_roi: { y: number; x: number; size: number };
  histogram: number[];
  delta_e_mean: number | null;
  delta_e_max: number | null;
  principles: {
    delta_e: Principle;
    snr: Principle;
  };
};

export async function analyzeImages(image: File, reference?: File | null): Promise<AnalyzeResult> {
  const body = new FormData();
  body.append("image", image);
  if (reference) {
    body.append("reference", reference);
  }
  const res = await fetch("/api/iq/analyze", { method: "POST", body });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `analyze ${res.status}`);
  }
  return res.json();
}
