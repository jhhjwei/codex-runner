# Opportunity Pipeline Archive

这是全网收入机会的长期、可追溯资料库。当前唯一商业目标：尽快获得首笔真实付费；优先推进 Maven Dependency Doctor 的真实用户验证，而不是扩大搜索和报告数量。

## 核心 KPI（从 2026-08-11 起）

每小时/每日主看 5 个数字：

1. `target_users_found`：新增、正在遭遇 Maven/Java 依赖问题的真实目标用户数。
2. `outreach_sent`：已完成的真实外部触达数（评论、issue 回复、邮件、DM 等）。
3. `replies_received`：真实用户回复数。
4. `projects_submitted`：用户愿意提供用于诊断的真实项目数。
5. `quotes_sent / payments_received`：明确报价数 / 实际到账数。

搜索结果、候选清单、snapshot、health、归档、报告、代码提交均不计入商业进展。

## 当前执行优先级

- P0：寻找最近仍活跃的 Maven/Spring/Java dependency conflict、dependency convergence、version mismatch、upgrade breakage 等真实问题拥有者。
- P0：对合适目标生成针对该项目的 Maven Dependency Doctor 诊断，并完成一次低摩擦触达。
- P0：用户回复后推动其提交真实项目；完成免费初诊后，对完整修复方案或 PR 直接报价。
- P1：已有明确赏金且可直接领取、低竞争、1–4 小时可交付的机会。
- P2：其他机会搜索。

若连续两个小时 `outreach_sent=0`，下一小时禁止继续扩展渠道、health、报告或基础设施，必须优先完成至少一次真实外部触达，除非不存在满足安全与平台规则的目标。

## Maven Dependency Doctor 首单漏斗

`真实 Maven 问题 → 目标用户 → 针对性诊断 → 外部触达 → 回复 → 提交真实项目 → 免费初诊 → $19–39 完整修复/PR 报价 → 付款`

首单前禁止开发非成交必需的新功能。产品是否继续投入，用真实漏斗数据判断，而不是代码完成度判断。

## 数据原则

- **一条机会一个稳定记录**：使用原始页面的 canonical URL 作为主要去重依据。
- **不覆盖历史事实**：状态变化写入 `history`，当前状态写入主记录。
- **聚合器只作线索来源**：Algora、Opire、IssueHunt 等金额必须回到原始页面验真。
- **公开仓库不保存秘密**：不得保存密码、Token、Cookie、验证码、客户代码、客户数据、私密邮件正文、未公开报价或身份材料。
- **真实漏斗**：L1 原始线索 → L2 验真 → L3 可联系 → L4 已验真商业机会 → L5 A1/A2/A3 → L6 已联系/认领 → L7 需求/合同 → L8 交付 → L9 验收/PR → L10 接受/成交 → L11 确认付款 → L12 到账；D 表示淘汰。
- **不把搜索数量当收入进展**：只有目标用户、触达、回复、真实项目、报价、成交、付款和到账才属于核心推进。

## 文件结构

- `opportunities.jsonl`：主机会库；每行一个 JSON 对象，便于脚本、AI 和 Git diff 处理。
- `SCHEMA.md`：字段、状态和去重规范。
- `snapshots/YYYY-MM-DD/HH.md`：每小时扫描与推进快照。
- `archive/YYYY-MM.jsonl`：关闭、失效、已授标、违规或重复机会的归档记录。
- `SUMMARY.md`：当前 Pipeline 汇总和最佳机会索引，由自动化更新。

## 更新流程

1. 首先检查 Maven Dependency Doctor 首单漏斗是否有下一步可执行动作；有则优先执行。
2. 搜索公开的近期真实 Maven/Java 依赖问题，确认问题拥有者和可联系入口。
3. 以 `canonical_url` 去重并更新状态、证据和下一步。
4. 对满足条件的目标完成针对性诊断和外部触达，而不是只保存候选。
5. 每次运行记录核心 KPI；发生状态变化时更新主记录。
6. 只有核心 KPI 无可执行目标时，才扩展其他赏金/商业机会搜索。
7. 淘汰记录保留 `dedup_key`，防止重复计入。
