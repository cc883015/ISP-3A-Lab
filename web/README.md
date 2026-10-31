# web/

展示站。静态构建后可以放到 Cloudflare Pages 或阿里云 OSS。  
Showcase site. The static build can go to Cloudflare Pages or Aliyun OSS.

新工具：在 `src/tools/registry.ts` 加一张卡片，再加一条路由。计算仍走 `apps/` → `python/`。  
To add a tool: register a card in `src/tools/registry.ts` and add a route. Compute still goes `apps/` → `python/`.

```bash
npm install
npm run dev      # http://127.0.0.1:5173  （/api 代理到 8788）
npm run build    # dist/ 可上传到任意静态托管
```
