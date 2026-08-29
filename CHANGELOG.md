# Changelog

本项目所有重要变更记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循语义化版本。

## [1.4.0] - 2026-08-28

### Fixed

- **`check_demand_card.py`：`--allow` 不再放行硬性词（P0）**。此前 `--allow 接口` 可把硬性 FAIL 变成退出码 0「可以发布」，绕过阶段 1 机械闸——现 `--allow` 仅对软性词生效，硬性词传入时忽略并提示"必须改写"。
- **`check_demand_card.py`：补 HTTP 方法动词（P0）**。新增大小写敏感的 `GET / POST / PUT / PATCH / DELETE` 硬性词（大写敏感是为不误伤"get 到"这类口语）；`spring boot` 正则放宽为兼容 "SpringBoot" / "spring-boot"；补 uvicorn / gunicorn / sqlite / mysql / postgres / redis / mongodb / docker 高频词。
- **`check_demand_card.py`：编号列表误判（P1）**。验收标准条目计数此前只认 `-` / `*` 项目符号，`1. / 1、 / 1)` 编号会被误判为"0 条"；现兼容编号列表。
- **`check_demand_card.py`：标题后缀误判（P1）**。章节标题此前要求整行精确等于「背景」等，`## 背景：为什么要做` 会误报缺失；现允许冒号 / 空格 / 括号后缀。
- **`check_demand_card.py`：软性词重复告警（P2）**。中文词按最长匹配占位，「配置文件」不再同时报「文件」+「配置文件」两条告警。
- **统一"懂了"分流口径（P1）**。guidance-ethics 梯度递进规则（"懂了"→跳出）与 SKILL.md 阶段 3 门禁（"懂了"→升级或跳出）此前矛盾，且与 example-session 样本（"懂思路了但不知道语法"→升一级）不一致；现统一为：懂了且能推进 → 跳出（拿不准用"装懂"话术追问验证）；懂了但明确做不出来 → 升一级。
- **`draft-card.md` 写入权矛盾（P2）**。阶段 1 硬性步骤要求把草稿写入 `.junior-sprint/draft-card.md`，但 Constraints"唯一例外"只列了 state.md；现例外扩为 `.junior-sprint/` 目录过程文件，并明确草稿发布后删除。
- **`selftest.sh`：解释器探测（P2）**。Windows 上 `python3` 可能是 Microsoft Store 占位别名——在 PATH 中存在但执行即失败（实测退出码 49），旧逻辑只检查"是否存在"导致自测入口静默挂掉；现用 `"$PY" -c ""` 实测可用性，失败自动回退 `python`。
- **触发词章节自相矛盾（P2）**。"技术栈非 Python/Java"原列在"不适用场景（拒绝）"下但处置是"仍可侦察"；现移入新增的"受限场景（可用，但先说明局限）"。

### Changed

- **验收结论与五维评分解耦（P2）**。"某维度 <3 触发打回"取消——评分只进复盘与下轮换档，打回仅由业务级缺陷触发（工程硬伤如回归已由逐条核对第 4 条按业务缺陷拦截），消除"沟通 2 分也要业务打回但无缺陷可指"的矛盾。
- SKILL.md 软性词示例去掉「类」（词表刻意不收，避免 类型 / 分类 大面积误报），与脚本实现对齐。
- 复盘报告补「沟通」叙述章（模板 + 验收参考清单 + example-session 样本对齐），样本报告补齐 Sprint ID 字段、跨轮对比细化与「下轮建议（AI 主动）」章节，与模板结构一致。

### Added

- `test_check_demand_card.py` 用例 7 → 14：新增 HTTP 动词拦截与小写 get 不误报 / 编号列表计数 / 冒号标题 / 无后缀标题恰好 3 条不吞行 / 长词去重 / SpringBoot 无空格 / `--allow` 硬性词忽略 / `--allow` 软性词放行。

## [1.3.0] - 2026-08-27

### Fixed

- **修复核心原则冲突（P0）**：防一键退出条款原允许"接管完成本轮交付"，与核心原则 #1「绝不代写完整代码」直接矛盾。现改为退出时 AI 只给【结构化实现清单 + 梯度第 6 级关键片段（≤10 行，逐行注释）】，绝不输出完整成品代码。
- **统一 `SPRINT-RETRO.md` 写入权（P1）**：消除"AI 写入 SPRINT-RETRO.md"与"AI 不代写该文件"的矛盾——统一为 AI 生成带标注的复盘稿，**请学习者追加**，AI 不代写。
- **`interface.yaml` 去重（P1）**：明确 `interface.yaml` 为元数据单一真源，`agents/openai.yaml` 改为其自动镜像并给出 `cp` 重建命令，消除手动双写同步负担。
- **客户口吻禁词歧义（P1）**：阶段 1 发布前自检补充说明脚本两级扫描（硬性 FAIL / 软性 WARN），并强调脚本只是机械闸、上表禁用词仍须严格遵守。
- **`check_demand_card.py` Sprint ID 正则**：由 `S-YYYYMMDD-NN`（强制 2 位）放宽为 `S-YYYYMMDD-N`（N ≥1 位），避免单数字序号被误判缺失。

### Added

- **`check_demand_card.py` 自测（P1）**：新增 `test_check_demand_card.py`（7 用例：合法通过 / 技术词拦截 / 缺章节 / 缺 Sprint ID / `--allow` 放行 / `--strict` 软性词 / 单数字 ID）与 `selftest.sh` 入口，回归验证 `Ran 7 tests ... OK`。
- **三阶段门禁（P1）**：Validation 由扁平清单重构为【阶段 1 / 阶段 3 / 阶段 4 门禁】，并在对应阶段末尾加硬步骤指针，绑定防模型漂移。
- **首触发 orientation（P2）**：学习者首次唤醒时 AI 先给 3 行流程预告，降低陌生感。
- **L3 架构权衡样本（P2）**：example-session 新增「L3 架构卡点（梯度第 3 级架构例外）」对话样本。
- **测试命令泛化（P2）**：阶段 4 与 README 的"跑 `pytest`"泛化为 `pytest` / `mvn test` / `gradle test`，与 Java 训练栈对齐。
- **`references/sprint-state.md` 改名（P2）**：更名为 `references/state-persistence.md`，避免与 `assets/templates/sprint-state.md` 同名混淆；同步更新全部引用。

## [1.2.0] - 2026-08-23

### Fixed

- 修正 SKILL.md Constraints 中"装懂"条款的歧义病句：学习者答错不当场纠正，"装懂"（口头说懂但追问答不上来）是唯一允许当场追问验证的例外
- 修复阶段 2 中"状态持久化"条目误嵌套在"一次不超过 3 句"之下的格式错位

### Added

- 验收运行副作用防护：可能产生不可逆外部影响（外发请求 / 写远端数据库 / 删文件 / 付费 API）时先征得学习者确认；启动长驻服务验收设超时、验证完即停止进程
- `assets/scripts/check_demand_card.py`：需求卡发布前自检脚本（三要素 / Sprint ID / 技术词两级扫描，支持 `--strict` 与 `--allow`），阶段 1 设为硬性步骤
- example-session 新增反例片段集：身份撕裂 / 跳级 / 打回泄改法 / 装懂放行 / 中途退出五种失败模式的「错误 → 正确」对照
- 需求卡模板增加 Sprint ID 字段，与复盘报告、state 文件跨轮可追溯
- CHANGELOG.md（本文件）

### Changed

- "首次加载必读"改为"每次触发必读"（无状态 agent 没有"首次"记忆）
- interface.yaml 与 agents/openai.yaml 顶部声明同步义务；default_prompt 去除 "Use $junior-sprint:" 指令前缀，改为纯用户话术
- 署名统一为 WeatherCore（LICENSE、SKILL.md frontmatter author）

## [1.1.0] - 2026-08-21

### Added

- 跨轮成长闭环：阶段 0 读取 `SPRINT-RETRO.md` 上轮复盘，AI 基于上轮"自主排错"分数主动换档（≥4 升档 / =3 保持 / ≤2 降档）
- Sprint 状态持久化：AI 主动写入 `.junior-sprint/state.md`，含防失忆最小集
- 验收打回 3 轮仍未通过时可例外进入卡点指导模式
- 复盘评分新增"沟通"维度（五维雷达），另附"职场视角"叙述章
- 敏感信息脱敏约束、验收运行边界约束
- Description.md 与 agents/openai.yaml 元数据

### Changed

- 状态文件写入口径调整：state.md 由 AI 主动维护，SPRINT-RETRO.md 由学习者确认追加
- skill 目录从 `junior-sprint-v1.0.0/` 迁移到 `skills/junior-sprint/`（skills CLI 标准布局）
- README 全面重写

## [1.0.0] - 2026-08-20

首个版本。

- 5 阶段教练式闭环工作流（侦察 / 需求发布 / 自我攻坚 / 卡点指导 / 交付验收）
- 4 身份语言隔离、三段式求助判定、渐进梯度 6 级指导
- 五维评分复盘、Python / Java 需求种子库、3 个输出模板与 6 篇方法论 references
