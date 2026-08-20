# Junior Sprint — 企业需求交付训练

模拟企业真实开发需求交付闭环的 AI Skill。AI 扮演客户，基于学习者的 Python/Java 项目提出业务需求，让学习者独立攻坚、卡点再分步指导、最后模拟客户验收并复盘。全程教练式训练，绝不直接给完整成品代码。

## 适用场景

- 训练需求理解、问题拆解与自主排错能力
- 模拟真实职场需求交付流程（接收需求 → 攻坚 → 求助 → 交付验收）
- 面试场景练习（被分到陌生项目快速上手）
- 有项目但不知道练什么的开发者

## 安装

将 `junior-sprint/` 目录放入你的 AI 编程助手的 skills 目录：

```bash
# ZCode
cp -r junior-sprint ~/.zcode/skills/

# Claude Code
cp -r junior-sprint ~/.claude/skills/
```

## 使用方式

触发关键词：`练项目` / `模拟客户` / `跑一轮 sprint` / `junior sprint` / `practice project`

```
给我出个开发任务练手，我的项目在 D:/my-app/
```

之后 AI 会自动走完五阶段流程：侦察项目 → 发布需求 → 你独立攻坚 → 卡点指导 → 客户验收复盘。

## 文件结构

```
junior-sprint/
├── SKILL.md                    # Skill 主文件（入口）
├── interface.yaml              # 平台元数据
├── references/
│   ├── demand-generation.md    # 需求生成方法论（L1/L2/L3）
│   ├── demand-seeds.md         # Python/Java 需求种子库
│   ├── guidance-ethics.md      # 卡点指导渐进梯度
│   ├── acceptance-review.md    # 验收标准与复盘
│   ├── sprint-state.md         # 跨轮持久化机制
│   └── example-session.md      # 完整对话样本
└── assets/templates/
    ├── demand-card.md          # 需求卡模板
    ├── retro-report.md         # 复盘报告模板
    └── sprint-state.md         # 状态文件模板
```

## License

MIT