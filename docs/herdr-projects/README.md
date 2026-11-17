# 让 Herdr Projects 执行 Gaia 开发原则

状态：源码分析、改造设计和 setup skill 已提供；Herdr 补丁、安装与运行时集成测试尚未实施。

## 1. 选择两层交付，保留一个原则来源

采用“标准版 setup + 薄补丁版本”。先用 setup 识别项目状态、生成适用配置和检查入口；遇到标准版无法强制保证的约束，再选择本地补丁版本。两条路径共用同一个 setup，不维护两套合作协议。

以 [量化开发与协作规范](../../dev-principles/quant-development-and-agent-collaboration.zh-CN.md) 和 [项目启动规范](../../dev-principles/new-project-skeleton-efficiency-and-delivery.zh-CN.md) 为约束来源。工具适配留在本目录，不把特定 Herdr 版本的字段写回通用规范。参数和配置允许 hash；原始及衍生数据集、行、分区禁止 hash。Git 源码标识、软件包完整性校验不属于量化数据集 hash。

源码基线为上游 `v1.0.0`，对应提交 `75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0`。原仓库 `eliasstravik/herdr-projects` 已重定向至 [eliasstravik/shepherdr](https://github.com/eliasstravik/shepherdr)。用户实际安装仅知“1.0 左右”；不要直接套用最新主干或旧版 PROJECT.md 配置。详细能力边界见 [版本对照](../../skills/gaia-herdr-setup/references/compatibility.md)。

| 交付方式 | 适用情况 | 能保证什么 | 不能声称什么 |
|---|---|---|---|
| 标准版 + setup skill | 先用已有工具推进项目；能接受部分约束靠人工/检查入口执行 | 识别版本、配置有效值、统一规则、阶段化检查、列出缺口 | 配置不能实现原生不存在的只读隔离、类型化依赖、独立修复预算 |
| 本地薄补丁版 + 同一个 setup | 需要长期无人值守、强依赖与恢复语义 | 用少量源码修改强制关键约束，并验证实际运行版本 | 尚未实现的补丁不能作为已支持能力 |
| 完整重写平台 | 目前不选 | 仅在薄补丁无法满足已验证需求时重新评估 | 不因想用 goal/loop 就先建设通用调度平台 |

**落实：Check** 核对安装版本、有效配置与能力矩阵；**Review** 每个补丁必须说明标准配置为什么不足。

## 2. 按源码落点修改，先修真实缺口

下列链接均固定到上述提交。优先级表示建议实施顺序，不表示补丁已经完成。

| 优先级 / 改动 | 源码观察 | 修改方案 | 验收 |
|---|---|---|---|
| P0：锁定本地运行版本 | [bin/run.sh](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/bin/run.sh) 按本地构建新鲜度、下载版和版本条件选择程序；改源码后可能改选下载版 | 增加严格本地模式；本地构建过期则拒绝启动并给出构建命令。新增构建身份输出，记录上游提交、补丁提交、状态格式、二进制路径。CLI、launcher、keeper 使用同一身份 | **Test** 改源不重建时拒绝；断网时不降级；keeper 重启后身份一致 |
| P0：分离检查修复与评审返修 | [settings_list.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/core/src/store/settings_list.rs) 与 [pipeline.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/finish/pipeline.rs) 共用 review.rounds；设 0 会连带停止自动检查返修 | 独立表示确定性检查修复预算、独立验证策略、业务拒绝。保留已授权范围内的有界修复；禁止多轮对抗辩论。不要通过设置 rounds=0 假装完成解耦 | **Test** 检查失败按预算修复；评审不自动循环；business refusal 独立终止，不当作基础设施失败重试 |
| P0：验证最终提交，禁止检查偷偷改代码 | [pipeline.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/finish/pipeline.rs) 可在检查通过后将工作树改动提交为 Written by the check | 将有意代码生成移到显式步骤；验证步骤对最终代码只读，检测受版本控制文件和影响构建的新增文件；产物只写隔离输出目录。发生代码变化就使原证据失效并重新验证 | **Test** 一个返回 0 但修改源码的检查必须失败；独立生成后重新验证的提交才可通过 |
| P1：原生按任务规模路由 | [coordinator/rules.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/coordinator/rules.rs) 默认建任务；直接做要求用户明确提出 | 增加最小执行模式选择：direct、delegate、persistent。direct 仍需项目 CWD、唯一写者与完成证据；不能直接在 coordinator 数据目录改项目。不要只追加一段与固定规则冲突的提示词 | **Test** 单文件修正不启动整套派工；独立多文件任务可并行；恢复型任务形成持久依赖；同 worktree 不出现双写 |
| P1：依赖边携带交付契约 | [after.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/after.rs)、[after/pass.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/after/pass.rs) 基于 board 完成状态放行 | 保留无环检查，新增代码/报告/数据引用等依赖类型、对应版本和证据。在入队及真正启动时重新核验；报告型依赖无需强行 merge。旧 after 边标明 legacy，不能迁移后冒充严格契约 | **Test** 手动 done 但无要求的产物不能解锁；合法报告能解锁；代码或数据 vintage 变更使旧证据失效 |
| P1：补齐外部副作用恢复 | [turn_ended.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/finish/turn_ended.rs) 已有事件水位、锁、阶段与回合检查；pipeline 创建 PR 后才记入本地状态 | 保留现有去重，增加外部动作意图与结果核对。重启先按任务、head/base 等稳定身份查找已有 PR，再决定是否创建。不要把一次派发等同一次副作用 | **Test** 注入“服务端成功、本地未记账”崩溃；重启找回同一结果。此处是源码推导的恢复风险，尚未复现为重复 PR 缺陷 |
| P2：提供真正独立的验证边界 | [review_brief.rs](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/flow/src/finish/review_brief.rs) 有 commit-pinned verdict，但评审口吻对抗；access 的 ask/full 不是只读权限模型 | 以最终代码、契约和命令为独立任务输入，限定写入隔离临时目录；用操作系统权限或隔离执行器保护源码与凭据。通过新鲜上下文做一次证据验证，必要修复回到有界检查流程 | **Test** 读得到目标产物、写不了受保护仓库/生产状态；PIT/幂等守卫的定向故障注入能被发现。**Review** 不把模型自述“只读”算权限证明 |
| P2：跨 harness 预算与长期任务 | [automations.md](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/docs/automations.md) 已有调度、重叠与循环防护；令牌限制按回合边界检查 | 对实际需要的长任务新增 goal 的完成证据、workflow 依赖、loop 停止条件；统一 board 与 harness 内部 agent 预算。显式记录时区、漏跑与恢复策略 | **Test** 预算计入嵌套代理；达成目标或无进展后停止；重启不重复消费。不要假称这些设计名词是 v1.0.0 原生命令 |

不重做已有 completion hooks、锁、事件水位与循环保护；先对缺口做小补丁。源码当前已区分 hook/transcript、旧回合和阶段，不能把它描述成“屏幕空闲就算完成”。

## 3. 让 setup 先调查，再问少量关键问题

入口为仓库内 [gaia-herdr-setup](../../skills/gaia-herdr-setup/SKILL.md)。这是可供 harness 读取的指令包；当前不包含自动修改 Herdr 的可执行安装器。将整个目录连同 references 安装到所用 harness 支持的技能位置；先检查该版本的发现机制。也可直接要求 harness 读取此文件执行 setup，不依赖自动发现。不要覆盖上游同名 `herdr-projects` 指令包。

示例调用：

> 读取 skills/gaia-herdr-setup/SKILL.md。目标仓库是当前目录，先识别安装版本、原则和功能状态，为目标功能生成方案及 diff；暂不安装或启用定时任务。已有的信息不要再问。

| 阶段 | 输入与输出 | 落实 |
|---|---|---|
| 只读调查 | 原则、当前 diff、实际二进制、插件、检查命令、有效配置、目标功能状态；区分已知和未知 | **Check** 先读文件，避免读取秘密；不要把可能触发 housekeeping 的 board 命令当纯只读 |
| 补问决策 | 目标与验收、未明确的执行权限和预算、是否接受维护补丁；每轮最多三问 | **Review** 不重复已有答案；不擅定交易参数、业务日历、修复次数或部署权限 |
| 选择路线 | 输出 native/configurable/advisory/patch-required/unsupported/unknown 能力矩阵 | **Check** 每项给版本证据和边界；缺补丁时明确阻断相应能力 |
| 生成变更 | 给出确切文件、设置作用域、差异、回滚和每条规则的 Check/Test/Review | **Check** 只生成安装版本支持的键；未实现能力不塞入 Herdr 配置 |
| 应用与恢复 | 在已授权范围内执行；保留自有修改收据，不覆盖用户新增内容 | **Test** 相同输入重跑不新增 hook/task/cron/worktree；中断后核对现状再续跑 |
| 验收报告 | 说明实际改动、有效版本、检查结果、剩余缺口和生产状态 | **Review** 区分 skill 文本评估、运行时 smoke test 和量化验收 |

任务级 → 用户仓库级 → 用户全局 → 仓库文件 → 默认值的优先级，意味着“写好了仓库配置”不等于“已经生效”。instructions 还会累加并受 none 重置影响。尤其 v1.0.0 的 review.rounds、review.when、merge.by、plan.approve 不支持放入仓库设置文件；用户配置里的“仓库条目”是另一作用域。setup 先检验字段能否放在该作用域，再检查生效结果。[查找优先级](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/core/src/store/settings/lookup.rs) 与 [字段定义](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/core/src/store/settings_list.rs) 分别决定这两件事。

## 4. 根据功能状态定制，不按整仓库一刀切

当前读取到的 Gaia 主干主要是四份开发规范和终端配置。此次适用范围是规范与适配方案，不宣称存在可测试的量化生产系统。业务检查只在真实目标仓库有对应功能时接入。

| 目标情形 | 执行选择 | setup 应生成 | 不应生成 |
|---|---|---|---|
| 修改一段规范、修一个局部 CLI 参数 | 直接执行；最低开销 | 相关规则链接、必要检查、变更证据 | 强制多 agent、goal、cron、完整发布架构 |
| 新建可复用 Alpha 算子 | 可独立时按契约分工 | 最小非退化数据案例、PIT/缺失语义、适用幂等与资源检查 | 不存在的生产账户、交易默认值、永远通过的检查 |
| 修改成熟日更链路的状态算子 | 持久任务与严格依赖，隔离写者 | 原状态锚点、数据 vintage、恢复测试、最终提交证据 | 重跑当日再次推进状态、把修订结果覆盖 As-Traded |
| 跨模块迁移或长时开发 | 依赖 DAG；确有等待/周期才调度 | 可恢复步骤、产物交付条件、预算、结束与无进展条件 | 无界循环、嵌套 agent 不计预算、把工程 cron 当交易调度 |

对于量化生产，保留三项核心幂等验收：同日连跑两次、崩溃恢复重跑、全量 Batch 对比分段 Batch + Step（含重跑）。日志只追加，逻辑视图去重；有状态算子只读确认的前一日快照并原子发布新状态。同实现、固定环境按承诺精确比对；不同数值算法允许经论证的容差，并单独核验下游决策。

**落实：Test** 检查以上可观察行为；**Check** 用源、不可变 revision/vintage、截点及 schema 引用数据，不计算数据 hash。引用元数据不等于字节完整性证明；重现性还依赖存储不可变和写入权限控制。

## 5. Claude Code 与 Codex 共用约束，保留各自执行适配

将业务规则和验收放在仓库；保持 AGENTS 为共享入口，并在支持的 Claude 入口引用相同规则。避免两套全文副本漂移。worker/reviewer 使用哪个 harness 是可调整的执行选择，不把“Claude 写、Codex 审”当成质量证明。

保留上游适配器：Claude hook 与用户 hook 共存；Codex 已有 notify 时可能依靠 transcript fallback。不要另装一套抢占完成事件的 hook。将流程完成归属留在一个地方。[adapter 源码](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/crates/core/src/agents/adapter.rs)。

**落实：Check** 核对实际 harness 版本、入口和 hook 所有者；**Test** 单次完成、重复回调、旧回合回调和中断恢复；**Review** 中型任务只在可独立分工、节省总时间时增加 agent。

## 6. 本地优化版本的安装与回退

先取得实际 fork 地址或本地 checkout，不假设已经存在 Gaia Herdr fork。以固定上游提交创建补丁分支；对每个补丁保留独立提交与验收。构建前按实际源码检查工具链与测试入口，构建用 `cargo build --release --locked`。这是一条构建建议，不表示本次已经执行。

按以下顺序实施：

1. **Check** 固定 upstream 与 patch commit，记录状态格式和运行依赖；禁止把当前主干当成 v1.0.0。
2. **Test** 在隔离目录构建并运行补丁验收；隔离仓库、HERDR_PROJECTS_HOME、harness 配置和 Herdr server/socket。只隔离 state home 不足以隔离 install 的全部影响。
3. **Test** 以严格本地 launcher 运行，验证 CLI/keeper/launcher 身份及崩溃恢复；未实现严格选择时不宣称本地补丁版稳定生效。
4. **Check** 按安装版本支持的本地 link/install 流程切换，先停止旧工作者并备份状态。上游文档使用 `herdr plugin link "$PWD"`、`sh bin/run.sh install`；必须确认它们的作用范围后执行。不要在同一 server 并行注册两个冲突插件。
5. **Test** 先在一次性仓库做真实 smoke test，再接入目标仓库；setup 不自动开启生产发布和 cron。
6. **Check** 回退时验证旧二进制能读的状态格式；迁移不可逆时保留新事件、导出或协调后恢复备份，禁止直接用旧二进制读取新格式。

标准版路线可按 [安装文档](https://github.com/eliasstravik/shepherdr/blob/75a7adf866a090050e1d4cd3c0f7d4cadad4c7e0/docs/install.md) 核对固定 ref 的安装。两条路线都要再次确认正在运行的程序，不能以“源码已经改了”作为生效证据。

## 7. 首批实施范围与成功标准

先用 setup 对 Gaia 做方案级演练，再对一个真实功能做隔离试用。首批源码补丁只做 P0：版本锁定、修复/评审预算分离、最终提交验证。随后用一个跨任务依赖案例决定 P1 的必要范围；P2 等真实长任务出现再做。

- **Check** setup 输出能逐条追溯到原则、版本和作用域。
- **Test** setup 两次运行及中断恢复不重复产生副作用。
- **Test** P0 三项补丁分别通过表中故障案例，并保留上游现有恢复行为。
- **Review** 记录直接完成、委派和排队的时间开销，以实测调整路由；不预设多 agent 一定更快。
- **Review** 清楚区分已提供指令包、已实现补丁、已安装版本、已通过生产验收这四种状态。

本次交付的评估记录见 [evaluation.md](evaluation.md)。完整 setup 输出与恢复契约见 [setup-contract.md](../../skills/gaia-herdr-setup/references/setup-contract.md)。
