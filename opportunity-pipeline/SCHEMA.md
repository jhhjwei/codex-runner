# Opportunity Record Schema

`opportunities.jsonl` 每行保存一个机会对象。

## 必填字段

| 字段 | 含义 |
|---|---|
| `id` | 稳定的人类可读 ID，例如 `github-dokploy-416` |
| `canonical_url` | 原始任务页面；主要去重键 |
| `title` | 原始任务标题 |
| `publisher` | 发布组织或个人 |
| `channel` | GitHub、RFP、公开邮箱、竞赛、白标等 |
| `discovered_at` | 首次发现时间，ISO 8601 |
| `last_checked_at` | 最近底层验真时间 |
| `stage` | L1-L12 或 D |
| `status` | open、verifying、contactable、claimed、delivering、review、accepted、paid、received、rejected 等 |
| `delivery_mode` | A1、A2、A3、unknown |
| `deliverable_types` | code、docx、pdf、pptx、xlsx、research、data、design、maintenance 等数组 |
| `payment_signal` | 原始页面展示的预算、奖金、分成或付费信号原文摘要 |
| `contact_route` | GitHub 评论、公开邮箱、表单、API 等 |
| `verification` | 开放状态、预算、付款、竞争、验收、地区、身份与条款的当前结论 |
| `next_action` | 下一步可执行动作 |
| `upgrade_condition` | 升级到下一漏斗阶段所需条件 |
| `drop_condition` | 淘汰条件 |
| `history` | 状态变化数组 |

## 建议字段

- `discovery_sources`：聚合器、搜索页和交叉来源数组。
- `amount`：结构化金额对象；不确定时保留 `null`，不得猜测。
- `economics`：收入、自有工时、分包、工具、平台、风险预留、毛利和现金流。
- `competition`：认领者、PR、提案或其他竞争证据。
- `acceptance`：交付物、验收标准、期限和修订次数。
- `maintenance`：维护责任、SLA、成本和可收费模式。
- `risks`：法律、许可证、隐私、安全、付款、范围和供应商风险。
- `evidence`：支持当前结论的公开 URL 数组。
- `tags`：技术栈、行业、语言和成果形式。
- `historical_backfill_pending`：历史记录是否仍需重新验真。

## 去重与归并

1. 首选规范化后的 `canonical_url`。
2. GitHub 使用 `owner/repo#issue_number` 或 `owner/repo#pr_number` 作为二级键。
3. 同一任务在多个聚合器出现时不得创建多条记录，来源加入 `discovery_sources`。
4. 标题相似但原始页面不同的任务先保留，待确认是否重复。
5. 已淘汰记录仍保留去重键，避免过期缓存重新进入漏斗。

## 状态要求

- L1-L3 是上游漏斗，可以包含尚未完全验真的线索。
- 只有预算/付费机制、开放状态、验收、付款路径和自主触达能力得到确认后，才进入 L4。
- 进入 L4 后必须填写经济模型。
- Upwork、Freelancer.com 及其他需要用户持续登录/投标且无可用官方连接器的任务不得进入 L4。
- `paid` 不等于 `received`；只有资金实际进入可核验收款账户才是 L12。
