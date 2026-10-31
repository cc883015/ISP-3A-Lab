# 部署 / Deploy

仓库分两层，所以换云平台只换托管，不换算法。  
Two layers, so a cloud move changes hosting, not the algorithms.

| 层 / Layer | 产物 / Artifact | Cloudflare | 阿里云 / Aliyun |
|---|---|---|---|
| 展示站 | `web/dist` | Pages | OSS + CDN |
| IQ 计算 | `apps/iq_lab/server.py` | 本地，或以后 Containers | 函数计算 / 轻量 ECS |
| 算法 | `python/` `c/` | 不部署，只在 GitHub 打磨 | 同上 |

## 国外 / Cloudflare

1. `cd web && npm run build`
2. Pages 指向 `web/dist`
3. `public/_redirects` 已写 SPA 回退
4. 纯静态也能打开工具目录。要现场算 ΔE / SNR，本机再开 API，或以后把 Worker/Container 接到同一 `/api`

## 国内 / Aliyun

1. 同一份 `web/dist` 传到 OSS，打开静态网站，404 回 `index.html`
2. API 用函数计算或轻量服务器跑 `uvicorn`
3. 前端把 API 基址换成国内域名（`web/src/lib/api.ts` 只使用相对路径 `/api`，用网关反代即可）

## 本机面试 / Local interview

```bash
bash scripts/dev_showcase.sh
```

打开 http://127.0.0.1:5173
