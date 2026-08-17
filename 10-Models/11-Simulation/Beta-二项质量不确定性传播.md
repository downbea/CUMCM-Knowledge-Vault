---
id: model-beta-binomial-quality-uncertainty
title: Beta-二项质量不确定性传播
english_name: Beta-Binomial Quality Uncertainty Propagation
aliases: [Beta-Binomial, Beta-Bernoulli质量决策, 次品率后验]
tier: high-frequency
type: model_card
status: approved
decision: approved_by_user_2026-07-29
category: 贝叶斯决策
tags: [模型, 贝叶斯, 二项分布, 不确定性传播, 质量控制]
use_cases: [次品率后验估计, 后验预测, 策略稳定性, 信息价值]
code_status: passed_in_build_environment
code_example: "[[40-Code-Examples/production-decision-audit/README|生产决策审计示例]]"
last_validated: 2026-07-29
---

# Beta-二项质量不确定性传播

## 一句话定位

把抽检得到的次品率从点估计提升为后验分布，再将不确定性传递到利润、策略频率与后悔值。

## 数学骨架

若 (p\sim Beta(a,b))，观察 (k\) 个次品和 (n-k\) 个合格品，则

\[
p\mid k,n\sim Beta(a+k,b+n-k),\qquad E[p\mid k,n]=\frac{a+k}{a+b+n}.
\]

对策略 (s) 的利润 (g_s(\boldsymbol p))，应比较

\[
E[g_s(\boldsymbol p)\mid data],\quad
P\{s=\arg\max_j g_j(\boldsymbol p)\mid data\},
\]

以及下分位数、CVaR 或相对逐情景最优策略的期望后悔。

## 适用条件、优缺点

适用于各节点有实际 (n,k)，且批内次品率稳定。共轭计算简单，能直接生成可信区间和后验预测。独立 Beta 假设不能表达同供应商、同批次或共同工艺冲击；质量漂移时应使用分层或动态模型。

## 常见错误与改进

- 不能先用同一数据拟合先验、再把数据更新一次；
- 不能用标称率乘任意样本量冒充观测次品数；
- 区间两端代入不等于联合稳健性；
- 均值、众数和 MAP 不得混称。

改进为：记录每个节点真实 (n,k)，联合后验抽样，每次重新选优，报告策略选择概率、利润区间和信息价值。

## 证据

- [[2024B-P01-多阶段模拟仿真生产决策-审计笔记]]：PDF 18–21 页，§5.4，图10–11；正文有重复计数矛盾，代码只扰动部分节点。
- [[2024B-P03-生产过程决策优化-审计笔记]]：PDF 18–22 页，§8–9、表7–9、图2–3；后验公式正确，但代码以 (np) 代替观测且未重跑 DP。
- 网络补充：W06、W09。
- 本地示例：[[40-Code-Examples/production-decision-audit/README|可运行示例]]中的后验策略频率、利润区间和后悔值。
