# Changelog

本项目所有重要变更记录于此。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本遵循语义化版本。

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
