# 国赛数学建模知识库总览

## 待审核知识

```dataview
TABLE tier, category, code_status, source_status
FROM "10-Models"
WHERE status = "seeded" OR status = "pending"
SORT tier ASC, category ASC, file.name ASC
```

## 已批准模型

```dataview
TABLE tier, category, use_cases
FROM "10-Models"
WHERE status = "approved"
SORT category ASC, file.name ASC
```

## 论文审核队列

```dataview
TABLE year, venue, reproduction_status, review_status
FROM "30-Papers"
WHERE review_status != "approved"
SORT file.mtime DESC
```
