export type ToolStatus = "live" | "soon";

export type Tool = {
  id: string;
  path: string;
  status: ToolStatus;
  titleZh: string;
  titleEn: string;
  blurbZh: string;
  blurbEn: string;
  principles: string[];
};

/** Add a card here when a new interview tool is ready. */
export const tools: Tool[] = [
  {
    id: "iq-lab",
    path: "/tools/iq-lab",
    status: "live",
    titleZh: "画质实验室",
    titleEn: "IQ lab",
    blurbZh: "上传图，调用仓库里的 CIE76 ΔE 与块 SNR。",
    blurbEn: "Upload a frame. Calls CIE76 ΔE and patch SNR from python/metrics.",
    principles: ["CIE76 ΔE", "Patch SNR"],
  },
  {
    id: "awb-garage",
    path: "/tools/awb-garage",
    status: "soon",
    titleZh: "地库 AWB",
    titleEn: "Garage AWB",
    blurbZh: "双光源灰世界 / 白点，对应 python/aaa/awb.py。",
    blurbEn: "Two-illuminant gray world / white patch from python/aaa/awb.py.",
    principles: ["AWB"],
  },
  {
    id: "ae-highlight",
    path: "/tools/ae-highlight",
    status: "soon",
    titleZh: "强光 AE",
    titleEn: "Highlight AE",
    blurbZh: "目标亮度与曝光收敛，对应 python/aaa/ae.py。",
    blurbEn: "Target luma and exposure settle from python/aaa/ae.py.",
    principles: ["AE"],
  },
  {
    id: "af-curve",
    path: "/tools/af-curve",
    status: "soon",
    titleZh: "AF 曲线",
    titleEn: "AF curve",
    blurbZh: "Tenengrad 对焦曲线，对应 python/aaa/af.py。",
    blurbEn: "Tenengrad focus curve from python/aaa/af.py.",
    principles: ["AF"],
  },
];
