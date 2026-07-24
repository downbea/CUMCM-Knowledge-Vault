# 基础知识种子批量审核

审核规则：逐条检查模型定义、适用边界、代码运行结果、来源和相近模型。可将 `decision` 改为 `approve`、`revise`、`defer` 或 `reject`。Codex 读取本表后同步更新对应知识卡状态并重建索引。

```dataview
TABLE tier, category, code_status, source_status, decision
FROM "10-Models"
WHERE status = "seeded"
SORT tier ASC, category ASC, file.name ASC
```
