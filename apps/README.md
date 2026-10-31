# apps/

面试或工作里打开的计算服务放这里。算法库仍在 `python/` 和 `c/`。展示站在 `web/`。  
Compute services for interviews live here. Algorithm libraries stay in `python/` and `c/`. The showcase UI is `web/`.

## 放哪里 / Where it goes

| 你做的东西 / What you built | 路径 / Path | 例子 / Example |
|---|---|---|
| 展示网页 | `web/` | 工具卡片、路由 |
| IQ / 调试 API | `apps/<tool>/` | `apps/iq_lab/server.py` 调用 ΔE / SNR |
| 某家平台的调试 API | `apps/<vendor>_<tool>/` | `apps/sony_iq/` |
| 从文档抽出的通用算法 | `python/isp/` `python/aaa/` `python/metrics/` | 灰世界 AWB、块 SNR |
| 某家 3A / ISP | `python/*/platforms/<vendor>/` | `python/aaa/platforms/sony/ae.py` |
| 原理笔记 | `docs/principles/` | CIE76、块 SNR |

当前 IQ 实验室：

```text
apps/iq_lab/server.py     FastAPI，只转调 python/metrics/analyze.py
web/src/pages/IqLab.tsx   上传与展示
```

不要用 Streamlit 做展示站：它绑在 Python 进程上，Cloudflare Pages / 阿里云 OSS 不好迁。  
Do not use Streamlit for the showcase. It is tied to a Python process and is a poor fit for Cloudflare Pages or Aliyun OSS.

不要在 `apps/` 或 `web/` 里重写 ΔE / SNR。  
Do not reimplement ΔE / SNR in `apps/` or `web/`.
