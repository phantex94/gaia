# Setup skill 评估记录

评估日期：2026-11-17，2026-11-18 重新定基线。范围：指令包结构、文档一致性和一次离线行为演练。未安装或构建 Herdr，未运行真实 keeper、harness hook、量化算子或生产任务。

## 重新定基线：宿主 0.9.5 / 插件 1.2.27（当前）

2026-11-18 的只读审计发现本机实际运行 herdr-projects **1.2.27**（CLI、keeper、serve、board 同一程序），不是此前声明的 1.0.1。人工决定以 Herdr 0.9.5 + herdr-projects 1.2.27 为基线，默认不用任何形式的哈希，插件补丁暂缓。

- **Check：已完成。** 标签 `v1.2.27` 指向发布提交（记录值 `4a351c7`）；manifest 最低宿主 0.9.3、平台 linux/macos。
- **Check：已完成。** 在 1.2.27 源码中逐条复核 [版本对照](../../skills/gaia-herdr-setup/references/compatibility.md) 的能力与行号：review.rounds 仍同时限制检查返修、research 退回、评审循环和 fallback 接手；通过的检查改动仍会被提交；coordinator 仍默认建任务；仓库文件字段由 `.repo()` 决定（文档正文漏列 check.again 与 merge.pushTimeout）；PR 接管新增错误 base 拒绝；helper 识别移至 crates/core/src/agents/helpers.rs。
- **Review：已修正。** 新增 1.2.27 的作用域与命令：coordinator 作用域与 `--project-coordinator`、`archive --repo`、worker/reviewer.fallback、review.mustFix、attempts.*、autopilot.*、access auto、merge.checks/sync。
- **Review：已修正。** 收据、setup skill 与开发规范改为可读的 `param_set@seq` 和业务字段逻辑键；不再允许配置摘要。
- **Test：未执行。** 未在此组合上做隔离运行演练或 smoke 任务。

## 兼容性修正：宿主 0.9.5 / 插件 1.0.1（历史，已被上节取代）

用户随后明确版本为 **Herdr 0.9.5 + herdr-projects 1.0.1**。此前使用 1.0.0 作为分析基线不适用于直接发布该用户的安装方案；以下旧演练仅保留为历史记录，不能算新组合的运行验证。

- **Check：已完成。** 核对插件 v1.0.1 tag 的实际提交 b4989c7423f6b48bf6e82736e7b749c285d2e65a；宿主 v0.9.5 提交 2ecf19a92fc3a7fff75b6ce3655ef04f4625ec01。插件 manifest 最低宿主 0.9.3，声明平台 linux/macos；用户宿主满足版本门槛，平台及本机运行状态未验证。
- **Check：已完成。** 检查插件 1.0.0 → 1.0.1 的 31 个变更文件列表，复核相关 pipeline/already/helpers/finish_stuck 改动与宿主 0.9.5 发布说明；重新读取 settings_list.rs、adapter.rs、bin/run.sh，确认这些文件未变化。
- **Review：已修正。** 1.0.1 已有按 head 分支接管 open PR，以及已在 main/无改动/归档处理。建议改为保留既有恢复、补测崩溃窗口与身份匹配，撤回“从零新增接管”建议。
- **Review：已修正。** 保留 1.0.1 的 Claude helper 返回识别和 Finishing 恢复；区分宿主 Codex 屏幕状态检测与插件 notify/transcript 完成判定。
- **Check：已完成。** 当前方案、skill、兼容性表和安装 ref 更新为正确组合；收据区分用户声明与本机观测。未知版本的原演练保留为历史案例，不再描述当前用户环境。
- **Test：未执行。** 没有在此组合安装、启动或运行集成测试；本轮未重复独立 agent 场景演练。静态结构、链接、JSON/YAML 检查通过不代表运行兼容性已通过。

## 首版静态检查（历史）

- skill 结构验证器通过：frontmatter、命名与描述格式有效。
- 本地 Markdown 链接、代码围栏、JSON 示例和 YAML 元数据校验通过。
- 无 TODO/FIXME 占位符；新增文件空白检查通过。
- 源码依据固定为 v1.0.0 提交；对安装命令、review 字段作用域及检查后提交行为进行了源码复核。

## 首版离线行为演练（历史）

将 skill 与 references 提供给独立新上下文任务，仅允许读取，不提供真实运行环境，也不允许外部调用或修改。

当时的合成场景输入（不是用户当前已确认的版本）：

- 仓库只有四份开发规范和终端配置；Herdr 版本只知“1.0 左右”。
- 使用 Claude Code 与 Codex；小任务直接做；不要对抗循环，但希望检查失败可自动修。
- 将来需要日更状态算子幂等；当时的规则是配置可 hash、数据集不可 hash（已被“任何形式都不用哈希”取代）。
- 用户全局 review.rounds=3；仓库提议 review.rounds=0。
- 用户已有 Codex notify；本地 checkout 有补丁但 CLI 身份未知。
- 请求仅为 setup 方案。

| 检查点 | 观察结果 |
|---|---|
| 未知版本不假装已验证 | 明确基线与实际安装未知，不生成安装成功结论 |
| 文档阶段不过度建设 | 未要求当前运行量化生产测试，也未安装或开启定时任务 |
| review 与 repair 分离 | 识别 rounds=0 的副作用，未声称独立预算已经原生支持 |
| 配置作用域 | 初次误当成只有优先级冲突；补充源码明确字段不支持 repo 文件后，定向复测正确拒绝该放置方式 |
| 用户 hook 与本地补丁 | 保留 notify，要求验证 CLI/launcher/keeper 身份 |
| 数据 hash 边界（历史规则） | 保留数据禁止 hash，说明版本元数据不能替代不可变存储 |
| 缺少原文时的 diff | 初次指出说明不足；已明确允许标记为拟议变更清单，定向复测确认 |
| 有界修复契约 | 已补充范围、预算、停止、最终树复查、证据和恢复要求；定向复测确认 |

这是单场景、一次修订后的定向复测，不构成模型行为稳定性证明。评估仍指出：目标版本中 review.when=never 与失败检查修复的组合行为需要运行时验证，不能据此宣称实现独立预算。

## 尚未执行的集成验收

以下必须在实际实施对应能力后执行，当前均不记为通过：

1. 在隔离环境应用 setup 两次，检查没有重复任务、hook、schedule 或 worktree。
2. 中断应用后恢复，保留用户并发修改，验证有效配置和回滚。
3. 测试严格本地二进制选择、keeper 重启及状态迁移。
4. 测试检查步骤非法改码、预算耗尽、业务拒绝及无进展停止。
5. 测试 PR 外部动作成功但本地未记账时的恢复。
6. 在真实目标功能上执行 PIT 与三项日更幂等测试。

本次产物是可读取的 setup 指令包及源码补丁规格，尚不是自动化安装器或已验证的 Herdr fork。
