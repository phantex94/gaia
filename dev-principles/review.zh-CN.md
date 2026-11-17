# 量化研发大脑：中文审阅提纲

英文 [SKILL.md](SKILL.md) 是入口，`references/` 中的英文专题是规范正文。本文帮助你理解结构、审阅取舍，不逐段翻译，也不维护第二套规则。中英文有歧义时，以英文为准；需要改变规则时，先修改负责该规则的英文专题，再更新本提纲。

## 先读核心，再按问题展开

先确认八件事：信息是否在决策当时已经可用；训练与评估是否隔离；数学口径是否明确；模块是否拥有清楚的知识边界；状态能否正确恢复；发布重试是否会重复生效；结果能否复现；agent 的交付是否有真实证据。

这些是审阅方向，完整条件、例外和验收方式分别由下表中的英文文档定义。无需每次通读全部内容。

| 你现在要审什么 | 打开哪份英文文档 | 最值得问的问题 |
|---|---|---|
| 模块边界与接口 | [Architecture](references/architecture.md) | 这项知识归谁？调用方少需要理解了什么？ |
| 数据、时间与评估 | [Data and PIT](references/data-and-pit.md) | 当时真的能看到这些数据和模型吗？ |
| Alpha、算子与状态 | [Computation and state](references/computation-and-state.md) | 保存的是足够继续计算的状态，还是只有上次输出？ |
| 发布、重试与恢复 | [Publication and recovery](references/publication-and-recovery.md) | 远端已成功、本地没记下来时，会不会再执行一次？ |
| 参数、版本与缓存 | [Configuration and identity](references/configuration-and-identity.md) | 能否准确找到原始输入、参数、实现与前序状态？ |
| 开工、性能与上线 | [Delivery and verification](references/delivery-and-verification.md) | 这个阶段需要哪些证据，哪些检查还没真正执行？ |
| coordinator 派工与交接 | [Agent collaboration](references/agent-collaboration.md) | 分工是否减少了总成本，还是增加了协调负担？ |
| 一个具体变更或事故 | [Scenario playbook](references/scenarios.md) | 应读哪项契约、做什么判断、拿什么证据？ |

## 审阅设计时，区分三类要求

领域硬约束不能随意放宽，例如 PIT、split 隔离和历史 As-Traded 不可改写。架构约束体现当前认可的设计，例如公开接口、无环依赖和发布协议。函数长度、目录名称、是否使用注册表等默认做法，则应根据是否降低整体复杂度来判断。

不要因为一条风格规则就把完整的数学过程拆得难以阅读，也不要把错误的第一版设计永久冻结。但改变接口和业务语义时，必须说明兼容性、版本迁移和验收方法。详细判断依据见 [Architecture](references/architecture.md)。

## 用《软件设计的哲学》检查实际调用方

Deep module 的价值是让调用方更容易正确使用能力。例如，PIT 模块内部处理版本选择和可见性，调用方明确 cutoff 与修订政策；发布模块处理原子提交和去重，调用方明确逻辑身份和发布授权。

要隐藏的是实现机制，影响研究结论的政策仍须显式。不要把设计上的犹豫变成一堆配置开关。重要边界先比较两种接口草图，看真实调用代码、错误处理、修改影响和性能是否合理；不用为小改动机械地设计两次。

把新增 Alpha、供应商变化、发布重试作为三个检查例子：是否总要修改同一批无关模块？是否依赖对话里才知道的隐藏规则？这些信号比文件数量、函数行数更有参考价值。相关书籍链接与具体标准放在 [Architecture](references/architecture.md)。

## 量化语义的几个重点

- PIT 不是简单地 `shift(1)`。Event time 和 availability time 不同；一次可用性标准化与可反复执行的 as-of 查询也不同。
- Batch、Backfill、Step 要共享数学与状态契约，不要求写成同一个函数。浮点值接近，也不代表排名、阈值和最终订单相同。
- 修订数据产生新版本。事后重算使用新的 vintage，不能覆盖当时实际发布的 As-Traded 记录。
- 同一天重跑仍是同一个逻辑结果。新的 attempt 不能变成新的发布，输出与状态也不能出现混版。
- 券商超时不代表拒单。本地事务无法单独保证远端恰好执行一次，必须按 adapter 的真实能力对账。
- 数据集禁哈希是本项目要求，不是软件设计的普遍真理。允许的 config digest、Git 版本与禁用的数据内容指纹，边界由 [Configuration and identity](references/configuration-and-identity.md) 统一定义。

以上只提示易误读的地方，不替代对应英文契约。

## 把审阅落到开发过程

探索阶段也要保证 PIT、数据划分、版本和基本独立参考，但不必先建完整部署框架。进入可复用阶段，再要求稳定接口、充分状态、幂等恢复和规模预算。上线前，必须验证真实输出渠道、告警送达、对账、切换和回滚。按 [Delivery](references/delivery-and-verification.md) 判断进入下一阶段的条件。

coordinator 先按完整能力派工，再分配文件。共享语义要有唯一负责人；worker 分支测试通过，不等于最终集成结果正确。全局 `AGENTS.md` 保留共同约束，模块文档保存局部语义，任务记录保存证据。不要通过不断增加全局提示词补偿错误边界。详细流程见 [Agent collaboration](references/agent-collaboration.md)。

## 这次重组如何保存原有内容

原来的两篇英文指导和两篇中文翻译已改为迁移导航。当前权威内容只有英文入口与专题库；原始全文保留在 [Git 重组前版本 6d602a3](https://github.com/phantex94/gaia/tree/6d602a3/dev-principles)，供追溯设计历史，不作为另一套现行规则。

本次只是知识结构与规范编辑。链接检查、skill 格式检查和内容审阅不等于量化平台已经通过 PIT、恢复或实盘验收。这个目录也不会自动安装到全局 skill 目录或修改其他项目的 agent 指令。
