# 画质测试 / Image quality tests

3A 改的是拍摄过程。IQ 评的是画面。所以指标和 3A 不放在同一目录。  
3A changes the capture. IQ judges the picture. Keep the folders apart.

| 指标 / Metric | 在问什么 / Question | 原理 / Principle | 代码 / Code |
|---|---|---|---|
| SNR | 平坦块有多吵？ | 块 SNR：`20 log10(μ/σ)` | `python/metrics/snr.py` |
| ΔE | 颜色离参考多远？ | CIE76，在 CIELAB 里算欧氏距离 | `python/metrics/color_delta_e.py` |
| SFR / MTF | 边缘还剩多少对比度？ | 简化斜边（不是 ISO 12233 全文） | `python/metrics/mtf_sfr.py` |
| Shading | 四角相对中心有多暗？ | 角 / 心亮度比 | `python/metrics/shading.py` |

网页画质实验室只接了前两行，入口是 `python/metrics/analyze.py`。  
The IQ lab page only wires the first two rows, through `python/metrics/analyze.py`.

实验室仪器（Imatest 等）图卡和 ROI 更严。这里是同一类问题，不是替代品。  
Lab instruments (Imatest and friends) are stricter. Same questions, not a replacement.

## CIE76 ΔE

sRGB → 线性 RGB → XYZ → Lab，再对两个 Lab 向量做欧氏距离。  
sRGB → linear RGB → XYZ → Lab, then Euclidean distance.

这是 CIE76，不是 CIEDE2000。ΔE ≈ 2 常当作可控色块上「刚能看出来」的量级。  
This is CIE76, not CIEDE2000. ΔE ≈ 2 is a common just-noticeable ballpark on a controlled patch.

## 块 SNR / Patch SNR

在中心一块上取亮度均值与标准差：`SNR_dB = 20 log10(mean / std)`。  
On a center patch: `SNR_dB = 20 log10(mean / std)`.

只有近似均匀的灰场 / 补丁才有意义。  
Only meaningful on a near-flat field.

## 以后补 / Expand later

- [ ] ColorChecker 24 色块与参考 Lab
- [ ] ISO 12233 斜边 SFR
- [ ] 动态范围（阶梯图）
- [ ] 厂商 SOP 对照
