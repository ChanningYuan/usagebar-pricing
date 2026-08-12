# usagebar-pricing

[usageBar](https://github.com/ChanningYuan/usageBar) 的模型价格表每日镜像。

GitHub Actions 每天（北京时间 03:00）从 [models.dev](https://models.dev) 拉取全量价目，瘦身为 `pricing.json`（providerID → modelID → input/output/cache_read/cache_write 四项单价，$/1M token），供 usagebar.cn 服务器同步分发给客户端。

背景：usagebar.cn 服务器所在机房出口自 2026-07-29 起无法直连 models.dev（域名级网络封锁），故由境外 Actions 代取、服务器再从本仓库回拉。内容有变化才 commit。
