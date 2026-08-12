#!/usr/bin/env python3
# 把 models.dev 的全量 api.json 瘦身成 usageBar 用的 pricing.json：
# providerID → modelID → input/output/cache_read/cache_write 四项单价（$/1M token）。
# 输出格式与火山服务器旧版 sync 脚本逐字节一致（separators/sort_keys/ensure_ascii），
# 保证「内容无变化 → 字节不变 → nginx ETag 不变 → 客户端 304 零流量」的链路不被破坏。
# 结构哨兵直接内置：厂商数、claude/gpt 关键模型不在位就非零退出，绝不产出残表。
import json, sys

src, dst = sys.argv[1], sys.argv[2]
data = json.load(open(src))
slim = {}
for pid, p in data.items():
    models = {}
    for mid, m in (p.get("models") or {}).items():
        c = m.get("cost") or {}
        r = {k: c[k] for k in ("input", "output", "cache_read", "cache_write") if isinstance(c.get(k), (int, float))}
        if r:
            models[mid] = r
    if models:
        slim[pid] = models

assert len(slim) >= 50, f"providers too few: {len(slim)}"
assert any("claude" in m for m in slim.get("anthropic", {})), "anthropic/claude missing"
assert any("gpt" in m for m in slim.get("openai", {})), "openai/gpt missing"

json.dump({"providers": slim}, open(dst, "w"), separators=(",", ":"), ensure_ascii=False, sort_keys=True)
print(f"{len(slim)} providers, {sum(len(v) for v in slim.values())} models")
