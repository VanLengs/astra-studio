# 工作机制：迭代式插件开发

本文档详细模拟 Astra Studio 中一次完整的迭代式插件开发流程。

示例领域参考 `course-workshop-plugins`，展示从 `init` 到规划、构建、校验、发布，再到第二轮迭代变更时，工作区是如何演化的。

## 文档范围

本文重点说明：

- `studio/changes/` 在各阶段如何变化
- 域工作区与插件工作区的区别
- `target_dir` 如何作为实现的单一事实源
- 已交付的设计记录如何进入 `studio/archive/`
- `create` 与 `modify` 两类迭代路径的差异

本文也采用当前已经澄清的交互模型：

- 用户只在关键阶段边界进行确认
- 系统自动执行阶段内部步骤
- `skill-creator` 这类内置能力视为系统内部执行步骤，而不是用户手动运行的命令

## 核心模型

### 设计与实现分离

`studio/changes/` 是活跃设计工作区。

其中保存：

- 域级工件，例如 `event-storm.md`、`domain-map.md`、`changelog.md`
- 插件级设计工件，例如 `skill-map.md`、`brief.md`、`plugin.json.draft`、`status.json`

它不保存可执行实现文件。

实现直接保存在各插件的 `target_dir` 中，并且是单一事实源：

- `skills/*/SKILL.md`
- `commands/*.md`
- `scripts/`
- `hooks/`
- `.mcp.json`

当插件具有特定特征（traits）时，`spec-generate` 还会在 `target_dir` 中产出额外脚手架：

- **stateful**：`skills/init-workspace/SKILL.md` + `templates/runtime-config.yaml.tmpl` + `templates/runtime-status.json.tmpl`
- **hil-gated**：相关 SKILL.md 骨架中的 `## Approval Gate` 段落
- **multi-pipeline**：每条流水线的 `commands/{pipeline-name}.md` 编排命令
- **expert-scoped**：`agents/` 目录中的运行时专家定义

### 确认与执行分离

整个流程有阶段确认点，但执行动作由系统完成。

例如：

- 用户在 event-storm 结束后确认领域发现结果
- 用户在 domain-model 结束后确认插件边界
- 用户在 skill-design 结束后确认 skill 拆分
- 用户在进入 build 阶段前确认构建范围

确认之后，系统继续自动执行：

- 生成规格
- 执行 `build-skills`
- 调用 `skill-creator`
- 校验插件
- 发布已通过校验的变更

用户不应该在正常流水线中手动运行这些内部 skill。

## 示例领域

这里模拟一个课程工作坊领域，包含以下插件：

- `workshop-core`
- `workshop-designer`
- `workshop-insight`
- `workshop-quality`
- `workshop-resource`

在第二轮迭代中会新增一个插件：

- `workshop-feedback`

本模拟采用项目根目录插件布局，因此示例中的 `target_dir` 为：

- `workshop-core`
- `workshop-designer`
- `workshop-insight`
- `workshop-quality`
- `workshop-resource`
- `workshop-feedback`

## 场景 0：`/studio-core:init`

用户在项目中初始化 studio。

### 工作区快照

```text
studio/
├── config.yaml
├── changes/
│   └── .gitkeep
├── agents/
│   └── .gitkeep
└── archive/
    └── .gitkeep
```

### 说明

- `changes/` 为空
- `archive/` 为空
- 还没有任何插件工作区

## 场景 1：`/studio-planner:plan "course-workshop"` - event-storm 阶段

系统创建域工作区并生成领域发现产物。

### 工作区快照

```text
studio/
├── config.yaml
├── agents/
│   ├── .gitkeep
│   ├── child-development-psychologist.md
│   ├── early-childhood-curriculum-expert.md
│   └── instructional-designer.md
├── changes/
│   ├── .gitkeep
│   └── course-workshop/
│       ├── event-storm.md
│       ├── changelog.md
│       ├── status.json
│       ├── personas/
│       │   ├── curriculum-director.md
│       │   ├── classroom-teacher.md
│       │   └── principal.md
│       ├── journeys/
│       │   └── curriculum-director-monthly-proposal.md
│       └── processes/
│           ├── activity-design.md
│           └── monthly-proposal-creation.md
└── archive/
    └── .gitkeep
```

### `status.json`

```json
{
  "type": "domain",
  "domain": "course-workshop",
  "iteration": 1,
  "phase": "planning",
  "created_at": "2026-03-28T21:00:00+08:00",
  "updated_at": "2026-03-28T21:00:00+08:00",
  "plugins": []
}
```

### 系统做了什么

- 系统识别并整理了事件、Persona、Journey、Process
- 系统写入 `event-storm.md`
- 系统创建 `changelog.md`
- 域工作区以 iteration 1 初始化

### 阶段确认点

用户确认：

- 领域描述是否准确
- 参与角色是否合理
- 热点排序是否正确

确认后，系统继续进入 domain-model。

## 场景 2：domain-model 阶段

系统将领域聚类为插件候选，并创建插件变更工作区。

识别出的插件候选：

- `workshop-core`
- `workshop-designer`
- `workshop-insight`
- `workshop-quality`
- `workshop-resource`

### 工作区快照

```text
studio/
├── config.yaml
├── agents/
│   └── ...
├── changes/
│   ├── .gitkeep
│   ├── course-workshop/
│   │   ├── event-storm.md
│   │   ├── changelog.md
│   │   ├── status.json
│   │   ├── domain-map.md
│   │   ├── domain-canvas.md
│   │   ├── behavior-matrix.md
│   │   ├── opportunity-brief.md
│   │   ├── personas/
│   │   │   └── ...
│   │   ├── journeys/
│   │   │   └── ...
│   │   └── processes/
│   │       └── ...
│   ├── workshop-core/
│   │   └── status.json
│   ├── workshop-designer/
│   │   └── status.json
│   ├── workshop-insight/
│   │   └── status.json
│   ├── workshop-quality/
│   │   └── status.json
│   └── workshop-resource/
│       └── status.json
└── archive/
    └── .gitkeep

workshop-core/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep

workshop-designer/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep

workshop-insight/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep

workshop-quality/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep

workshop-resource/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep
```

### 插件工作区状态示例

`studio/changes/workshop-designer/status.json`

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "planning",
  "created_at": "2026-03-28T21:30:00+08:00",
  "skills": {}
}
```

### 域状态示例

```json
{
  "type": "domain",
  "domain": "course-workshop",
  "iteration": 1,
  "phase": "planning",
  "created_at": "2026-03-28T21:00:00+08:00",
  "updated_at": "2026-03-28T21:30:00+08:00",
  "plugins": [
    "workshop-core",
    "workshop-designer",
    "workshop-insight",
    "workshop-quality",
    "workshop-resource"
  ]
}
```

### 系统做了什么

- 系统写入了域分析相关文档
- 系统为每个插件候选创建了一个插件工作区
- 每个插件工作区初始都是 `action: "create"`
- 系统在对应 `target_dir` 下建立了空脚手架

### 阶段确认点

用户确认：

- 插件边界是否合理
- 插件职责是否正确
- 整体集合结构是否合理

确认后，系统继续进入 skill-design。

## 场景 3：skill-design 阶段

系统为每个插件设计 skill，并写入 `skill-map.md`。

### 工作区快照

```text
studio/
├── ...
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-core/
│   │   ├── status.json
│   │   └── skill-map.md
│   ├── workshop-designer/
│   │   ├── status.json
│   │   └── skill-map.md
│   ├── workshop-insight/
│   │   ├── status.json
│   │   └── skill-map.md
│   ├── workshop-quality/
│   │   ├── status.json
│   │   └── skill-map.md
│   └── workshop-resource/
│       ├── status.json
│       └── skill-map.md
└── ...
```

### skill-design 后状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "planning",
  "created_at": "2026-03-28T21:30:00+08:00",
  "skills": {
    "driving-question": "draft",
    "network-map": "draft",
    "inquiry-scaffold": "draft",
    "activity-design": "draft",
    "proposal-generate": "draft"
  }
}
```

### 系统做了什么

- 系统检测了每个插件的跨领域特征（traits）：`stateful`、`hil-gated`、`kb-dependent`、`multi-pipeline`、`expert-scoped`
- 系统为每个插件拆分了 skill（特征会影响拆分：HIL 检查点处拆分、不同流水线独立拆分、有状态插件需要 init-workspace skill）
- 系统把设计结果写进 `skill-map.md`（含 `## Plugin Traits` 和 `## Pipelines` 段落）
- `status.json.skills` 开始记录本轮涉及的 skill

### 阶段确认点

用户确认：

- 插件特征检测是否准确
- skill 边界是否合理
- 数据流是否清晰
- 复杂度分层是否合理

确认后，系统继续进入 `spec-generate`。

## 场景 4：spec-generate 阶段

这是设计与实现正式分离的阶段。

`spec-generate` 会把设计输出写入 `studio/changes/`，把实现骨架写入 `target_dir`。

### 工作区快照

```text
studio/
├── ...
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-core/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   ├── workshop-designer/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   ├── workshop-insight/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   ├── workshop-quality/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   └── workshop-resource/
│       ├── status.json
│       ├── skill-map.md
│       ├── brief.md
│       └── plugin.json.draft
└── archive/
    └── .gitkeep
```

### 实现侧快照示例

```text
workshop-designer/
├── skills/
│   ├── driving-question/
│   │   └── SKILL.md
│   ├── network-map/
│   │   └── SKILL.md
│   ├── inquiry-scaffold/
│   │   └── SKILL.md
│   ├── activity-design/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── .gitkeep
│   └── proposal-generate/
│       ├── SKILL.md
│       └── scripts/
│           └── .gitkeep
└── commands/
    ├── driving-question.md
    ├── network-map.md
    ├── inquiry-scaffold.md
    ├── activity-design.md
    └── proposal-generate.md
```

### 插件状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "building",
  "created_at": "2026-03-28T21:30:00+08:00",
  "updated_at": "2026-03-28T22:00:00+08:00",
  "skills": {
    "driving-question": "draft",
    "network-map": "draft",
    "inquiry-scaffold": "draft",
    "activity-design": "draft",
    "proposal-generate": "draft"
  }
}
```

### 系统做了什么

- `brief.md` 与 `plugin.json.draft` 被写入设计工作区
- skill 骨架直接写入 `target_dir`
- command 文件直接写入 `target_dir`
- 如果检测到 `stateful` 特征：生成 `skills/init-workspace/SKILL.md`、`templates/runtime-config.yaml.tmpl`、`templates/runtime-status.json.tmpl`
- 如果检测到 `hil-gated` 特征：在相关 SKILL.md 骨架中注入 `## Approval Gate` 段落
- 如果检测到 `multi-pipeline` 特征：为每条流水线生成 `commands/{pipeline-name}.md` 编排命令
- 如果检测到 `expert-scoped` 特征：在 `agents/` 中生成运行时专家定义
- 插件 phase 从 `planning` 进入 `building`

### 关键规则

用户在这里确认是否进入 build 阶段，但不会手动运行 `skill-creator`。

真正的构建动作由下一阶段完成。

## 场景 5：build-skills 阶段（初始填充）

用户确认进入 build 阶段后，Astra Studio 自动执行 `build-skills`。

`build-skills` 产出**可工作的初稿**，而非完成品。它读取 `studio/changes/{plugin}/` 中的插件工作区，确定本轮哪些 skill 需要处理，然后在 `target_dir` 中自动调用 `skill-creator` 进行初始填充。

> **初始填充 vs 迭代优化**：初稿覆盖核心逻辑和基本流程。边界情况、错误处理、评估用例需要用户后续用 `skill-creator` 迭代优化。

### 工作区快照

```text
studio/
├── ...
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-designer/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   └── ...
└── archive/
    └── .gitkeep

workshop-designer/
├── skills/
│   ├── driving-question/
│   │   └── SKILL.md
│   ├── network-map/
│   │   └── SKILL.md
│   ├── inquiry-scaffold/
│   │   └── SKILL.md
│   ├── activity-design/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── .gitkeep
│   └── proposal-generate/
│       ├── SKILL.md
│       └── scripts/
│           └── .gitkeep
└── commands/
    └── ...
```

### 构建中的状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "building",
  "created_at": "2026-03-28T21:30:00+08:00",
  "updated_at": "2026-03-28T22:20:00+08:00",
  "skills": {
    "driving-question": "built",
    "network-map": "built",
    "inquiry-scaffold": "built",
    "activity-design": "built",
    "proposal-generate": "built"
  }
}
```

### 系统做了什么

- Astra Studio 执行了 `build-skills`（初始填充）
- `build-skills` 在内部调用了 `skill-creator`，产出可工作的初稿
- `target_dir` 中的实现被原地充实
- 插件仍处于 `phase: "building"`
- 各 skill 的状态从 `draft` 推进到 `built`

### 下一步

初始填充完成后，用户应：
1. 用真实输入测试每个技能
2. 用 `skill-creator` 迭代优化（边界情况、错误处理、评估用例）
3. 运行 `/studio-quality:validate` 校验

## 场景 6：validate 通过

此时系统已经完成 `build-skills`，并且通过 `skill-creator` 在 `target_dir` 中补全了实现。

接着系统对 `target_dir` 执行校验，并回写对应插件工作区。

### 工作区快照

```text
studio/
├── ...
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-designer/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   └── ...
└── archive/
    └── .gitkeep

workshop-designer/
├── skills/
│   ├── driving-question/
│   │   └── SKILL.md
│   ├── network-map/
│   │   └── SKILL.md
│   ├── inquiry-scaffold/
│   │   └── SKILL.md
│   ├── activity-design/
│   │   ├── SKILL.md
│   │   └── scripts/
│   │       └── .gitkeep
│   └── proposal-generate/
│       ├── SKILL.md
│       └── scripts/
│           └── .gitkeep
└── commands/
    └── ...
```

### validate 后状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "approved",
  "created_at": "2026-03-28T21:30:00+08:00",
  "updated_at": "2026-03-28T23:00:00+08:00",
  "skills": {
    "driving-question": "tested",
    "network-map": "tested",
    "inquiry-scaffold": "tested",
    "activity-design": "tested",
    "proposal-generate": "tested"
  }
}
```

### 系统做了什么

- 校验是针对 `target_dir` 执行的
- 系统通过插件名找到对应的工作区
- 系统把 in-scope skill 从 `built` 推进为 `tested`
- 插件 phase 被推进到 `approved`

### 阶段确认点

用户确认：

- 是否现在发布
- 是否继续修改后再发布

确认后，系统可以执行 promote。

## 场景 7：promote（版本化里程碑）

promote 创建版本化里程碑，正式化 manifest 并快照设计工作区。

关键行为变化：
- 设计文档被**复制**（不是移动）到 `studio/archive/`
- 活跃工作区保留在 `studio/changes/` 中，供下一轮迭代使用
- 版本号自动递增（v0.1.0 → v0.1.1）
- 实现不会被复制

### Promote `workshop-designer` 后的工作区快照

```text
studio/
├── ...
├── changes/
│   ├── .gitkeep
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-core/
│   │   └── ...
│   ├── workshop-designer/
│   │   ├── status.json          # phase 重置为 planning, iteration++
│   │   ├── skill-map.md         # 保留供下一轮迭代参考
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   ├── workshop-insight/
│   │   └── ...
│   ├── workshop-quality/
│   │   └── ...
│   └── workshop-resource/
│       └── ...
└── archive/
    ├── .gitkeep
    └── workshop-designer/
        └── 2026-03-28-iteration-1/
            ├── skill-map.md
            ├── brief.md
            ├── plugin.json.draft
            └── status.json

workshop-designer/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── ...
└── commands/
    └── ...
```

### 活跃工作区状态（promote 后）

`studio/changes/workshop-designer/status.json`：

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 2,
  "phase": "planning",
  "created_at": "2026-03-28T21:30:00+08:00",
  "updated_at": "2026-03-28T23:10:00+08:00",
  "last_shipped_at": "2026-03-28T23:10:00+08:00",
  "last_shipped_version": "0.1.0",
  "skills": {
    "driving-question": "tested",
    "network-map": "tested",
    "inquiry-scaffold": "tested",
    "activity-design": "tested",
    "proposal-generate": "tested"
  }
}
```

### 归档快照状态

`studio/archive/workshop-designer/2026-03-28-iteration-1/status.json`：

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "create",
  "iteration": 1,
  "phase": "shipped",
  "created_at": "2026-03-28T21:30:00+08:00",
  "updated_at": "2026-03-28T23:10:00+08:00",
  "shipped_at": "2026-03-28T23:10:00+08:00",
  "shipped_version": "0.1.0",
  "archive_path": "studio/archive/workshop-designer/2026-03-28-iteration-1",
  "skills": {
    "driving-question": "tested",
    "network-map": "tested",
    "inquiry-scaffold": "tested",
    "activity-design": "tested",
    "proposal-generate": "tested"
  }
}
```

### 系统做了什么

- 正式 manifest 被写入 `target_dir`，版本号自动递增
- 设计工作区被**复制**（不是移动）到 `studio/archive/`
- 活跃工作区保留在 `studio/changes/`，phase 重置为 `planning`，iteration 递增
- 活跃工作区新增 `last_shipped_at` 和 `last_shipped_version` 字段
- 实现文件没有被复制

> **promote 是里程碑，不是终态**。设计文档保持活跃，供下一轮迭代参考和修改。

iteration 1 中其它插件也会依次经历相同的 promote 流程。

## 场景 8：iteration 2 开始

一个新需求进入：

- 新增家园共育反馈场景
- 修正 proposal 生成里缺失的园长审批摘要

用户运行 `/studio-planner:plan course-workshop`。

### 8a. event-storm 增量模式

由于域工作区已存在，系统进入增量模式，并就地更新域工件。

### 工作区快照

```text
studio/
├── changes/
│   ├── .gitkeep
│   └── course-workshop/
│       ├── event-storm.md
│       ├── changelog.md
│       ├── status.json
│       ├── domain-map.md
│       ├── domain-canvas.md
│       ├── behavior-matrix.md
│       ├── opportunity-brief.md
│       ├── personas/
│       │   ├── curriculum-director.md
│       │   ├── classroom-teacher.md
│       │   ├── principal.md
│       │   └── parent.md
│       ├── journeys/
│       │   ├── curriculum-director-monthly-proposal.md
│       │   └── parent-feedback-cycle.md
│       └── processes/
│           ├── activity-design.md
│           ├── monthly-proposal-creation.md
│           └── home-school-feedback.md
└── archive/
    └── ...
```

### 域状态示例

```json
{
  "type": "domain",
  "domain": "course-workshop",
  "iteration": 2,
  "phase": "planning",
  "created_at": "2026-03-28T21:00:00+08:00",
  "updated_at": "2026-04-10T09:30:00+08:00",
  "plugins": [
    "workshop-core",
    "workshop-designer",
    "workshop-insight",
    "workshop-quality",
    "workshop-resource"
  ]
}
```

### changelog 示例

```markdown
## 2026-04-10

**Summary**: Added a home-school feedback scenario and revised proposal generation to include a principal approval summary.

### Added
- Persona: parent
- Journey: parent-feedback-cycle
- Process: home-school-feedback

### Revised
- Process: monthly-proposal-creation — added principal approval summary output

### Impact on Plugins
- `workshop-designer`: needs modification — proposal output changed
- `workshop-quality`: needs modification — review checklist changed
- `workshop-feedback`: new plugin needed — home-school feedback scenario
- `workshop-core`: no change
- `workshop-insight`: no change
- `workshop-resource`: no change
```

### 阶段确认点

用户确认增量内容：

- 新增了哪些内容
- 修正了哪些流程
- 影响到了哪些插件

确认后，系统继续进入增量 domain-model。

## 场景 8b：domain-model 增量模式

系统只为受影响的插件创建变更工作区：

- `workshop-designer` → `modify`
- `workshop-quality` → `modify`
- `workshop-feedback` → `create`

未受影响、已 shipped 的插件不会重新出现在 `changes/` 中。

### 工作区快照

```text
studio/
├── changes/
│   ├── .gitkeep
│   ├── course-workshop/
│   │   ├── event-storm.md
│   │   ├── changelog.md
│   │   ├── status.json
│   │   ├── domain-map.md
│   │   ├── domain-canvas.md
│   │   ├── behavior-matrix.md
│   │   ├── opportunity-brief.md
│   │   ├── personas/
│   │   │   └── ...
│   │   ├── journeys/
│   │   │   └── ...
│   │   └── processes/
│   │       └── ...
│   ├── workshop-designer/
│   │   └── status.json
│   ├── workshop-quality/
│   │   └── status.json
│   └── workshop-feedback/
│       └── status.json
└── archive/
    ├── workshop-core/
│   │   └── 2026-03-28-iteration-1/
│   ├── workshop-designer/
│   │   └── 2026-03-28-iteration-1/
│   ├── workshop-insight/
│   │   └── 2026-03-28-iteration-1/
│   ├── workshop-quality/
│   │   └── 2026-03-28-iteration-1/
│   └── workshop-resource/
│       └── 2026-03-28-iteration-1/

workshop-feedback/
├── skills/
│   └── .gitkeep
└── commands/
    └── .gitkeep
```

### modify 工作区状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "modify",
  "iteration": 2,
  "phase": "planning",
  "created_at": "2026-04-10T10:00:00+08:00",
  "skills": {}
}
```

### 系统做了什么

- 系统只为受影响插件创建了新一轮变更工作区
- `modify` 工作区只引用已有 `target_dir`
- 只有新插件被建立了新的 target scaffold

### 阶段确认点

用户确认：

- 影响判断是否准确
- 哪些插件属于 `modify`
- 哪些插件属于 `create`

确认后，系统进入增量 skill-design。

## 场景 8c：skill-design 增量模式

在 `modify` 模式下，系统会先读取已有实现，再输出面向本轮变更的 `skill-map.md`。

### 工作区快照

```text
studio/
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-designer/
│   │   ├── status.json
│   │   └── skill-map.md
│   ├── workshop-quality/
│   │   ├── status.json
│   │   └── skill-map.md
│   └── workshop-feedback/
│       ├── status.json
│       └── skill-map.md
└── ...
```

### skill-design 后的 modify 状态示例

```json
{
  "type": "plugin",
  "plugin": "workshop-designer",
  "domain": "course-workshop",
  "target_collection": ".",
  "target_dir": "workshop-designer",
  "action": "modify",
  "iteration": 2,
  "phase": "planning",
  "created_at": "2026-04-10T10:00:00+08:00",
  "skills": {
    "proposal-generate": "draft"
  }
}
```

### 系统做了什么

- 对于 `modify`，只列出本轮真正需要动的 skill
- 未变化的 skill 不会被重新展开描述
- `skill-map.md` 表达的是本轮的设计增量

### 阶段确认点

用户确认：

- 哪些 skill 受影响
- 哪些是新增 skill
- 哪些是修改已有 skill

确认后，系统继续执行增量 `spec-generate`。

## 场景 8d：spec-generate + build-skills（modify 模式）

这是 iteration 2 中最关键的差异点。

`modify` 规则如下：

- `brief.md` 保留原内容，并追加迭代更新说明
- `plugin.json.draft` 只刷新系统生成字段
- 现有 `SKILL.md` 在 `spec-generate` 阶段不会被覆盖
- 现有 command 文件不会被覆盖
- 新 skill 会生成骨架
- 已有 skill 会交给 `build-skills`，由其调用 `skill-creator` 做原地更新

### 工作区快照

```text
studio/
├── changes/
│   ├── course-workshop/
│   │   └── ...
│   ├── workshop-designer/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   ├── workshop-quality/
│   │   ├── status.json
│   │   ├── skill-map.md
│   │   ├── brief.md
│   │   └── plugin.json.draft
│   └── workshop-feedback/
│       ├── status.json
│       ├── skill-map.md
│       ├── brief.md
│       └── plugin.json.draft
└── archive/
    └── ...
```

### 已有插件的实现快照

```text
workshop-designer/
├── skills/
│   ├── driving-question/
│   │   └── SKILL.md
│   ├── network-map/
│   │   └── SKILL.md
│   ├── inquiry-scaffold/
│   │   └── SKILL.md
│   ├── activity-design/
│   │   └── SKILL.md
│   └── proposal-generate/
│       └── SKILL.md
└── commands/
    └── proposal-generate.md
```

### 新插件的实现快照

```text
workshop-feedback/
├── skills/
│   ├── feedback-summary/
│   │   └── SKILL.md
│   └── parent-report/
│       └── SKILL.md
└── commands/
    ├── feedback-summary.md
    └── parent-report.md
```

### 系统做了什么

- `workshop-designer/proposal-generate/SKILL.md` 被保留下来
- `spec-generate` 没有覆盖它
- 系统把它交给 `build-skills`，由 `build-skills` 再调用 `skill-creator` 原地修改
- `workshop-designer/commands/` 中已有命令被保留
- 新插件 `workshop-feedback` 获得了新的 skill 与 command 骨架，并被继续构建

### 重要说明

在 `modify` 模式下，“不覆盖已有 `SKILL.md`”并不等于“用户必须手动去改文件”。

它真正的含义是：

- `spec-generate` 不会用新骨架替换已有文件
- 但系统仍然会通过 `build-skills` 和 `skill-creator` 原地更新这个已有文件

## 场景 9：validate 与 promote（iteration 2）

系统对 iteration 2 中受影响的插件执行校验并发布。

顺序例如：

- 先 promote `workshop-feedback`
- 再 promote `workshop-designer`
- 再 promote `workshop-quality`

### iteration 2 完成后的最终快照

```text
studio/
├── config.yaml
├── agents/
│   └── ...
├── changes/
│   ├── .gitkeep
│   ├── course-workshop/
│   │   ├── event-storm.md
│   │   ├── changelog.md
│   │   ├── domain-map.md
│   │   ├── domain-canvas.md
│   │   ├── behavior-matrix.md
│   │   ├── opportunity-brief.md
│   │   ├── personas/
│   │   ├── journeys/
│   │   ├── processes/
│   │   └── status.json
│   ├── workshop-core/
│   │   └── ...              # 活跃工作区保留
│   ├── workshop-designer/
│   │   └── ...              # 活跃工作区保留
│   ├── workshop-insight/
│   │   └── ...
│   ├── workshop-quality/
│   │   └── ...
│   ├── workshop-resource/
│   │   └── ...
│   └── workshop-feedback/
│       └── ...              # 活跃工作区保留
└── archive/
    ├── workshop-core/
    │   └── 2026-03-28-iteration-1/
    ├── workshop-designer/
    │   ├── 2026-03-28-iteration-1/
    │   └── 2026-04-10-iteration-2/
    ├── workshop-insight/
    │   └── 2026-03-28-iteration-1/
    ├── workshop-quality/
    │   ├── 2026-03-28-iteration-1/
    │   └── 2026-04-10-iteration-2/
    ├── workshop-resource/
    │   └── 2026-03-28-iteration-1/
    └── workshop-feedback/
        └── 2026-04-10-iteration-2/
```

### 实现侧快照

```text
workshop-designer/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── ...
└── commands/
    └── ...

workshop-feedback/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── ...
└── commands/
    └── ...
```

### 系统做了什么

- 设计文档被**复制**到 archive（活跃工作区保留在 changes/ 中）
- 活跃工作区 phase 重置为 `planning`，iteration 递增，版本号自动递增
- 域工作区继续保留并累积领域知识
- 实现继续留在各自的 `target_dir`
- 设计历史按插件与迭代保留在 archive 中

## 场景 10：小的实现改动

用户只想修改某个已有 skill 的输出格式，例如 `proposal-generate`。

这类改动不需要重走完整规划流程。

系统或用户可以直接修改：

```text
workshop-designer/skills/proposal-generate/SKILL.md
```

### 工作区快照

```text
studio/
├── changes/
│   ├── .gitkeep
│   └── course-workshop/
│       └── ...
└── archive/
    └── ...
```

### 系统做了什么

- `studio/changes/` 没有变化
- `studio/archive/` 没有变化
- 变化直接发生在 `target_dir` 的实现文件中
- 这类实现层变更由 git 历史记录

## 总结表

| 阶段 | `studio/changes/` 中的变化 | `target_dir` 中的变化 |
|------|----------------------------|-----------------------|
| `init` | 创建空工作区 | — |
| `event-storm` | 出现域工作区及 `event-storm.md`、`changelog.md`、personas、journeys、processes | — |
| `domain-model` | 出现域分析文档；出现插件工作区 `status.json` | `create` 插件建立 scaffold；`modify` 插件不建立 |
| `skill-design` | 出现 `skill-map.md`（含特征 + 流水线）；skill 进入 `draft` | — |
| `spec-generate` | 生成 `brief.md`、`plugin.json.draft`，插件 phase 进入 `building` | 生成 skill 骨架和 command + 特征条件脚手架 |
| `build-skills` | 除状态更新外无新增设计文档 | `skill-creator` 在 `target_dir` 中产出初稿（初始填充） |
| `validate` | 匹配的工作区 phase 进入 `approved`，skill 进入 `tested` | 校验 `target_dir` 中实现 |
| `promote` | 设计文档**复制**到 `archive/{plugin}/{date}-iteration-{N}`；活跃工作区保留，phase 重置为 `planning`，iteration++ | 写入正式 manifest（版本递增）；实现保留原地 |
| iteration N `event-storm` | 域工件原地更新；`changelog.md` 追加 | — |
| iteration N `domain-model` | 只出现受影响插件的工作区 | `modify` 不建立 scaffold |
| iteration N `spec-generate` | 更新 `brief.md`、`plugin.json.draft`、`status.json` | 只为新 skill 生成骨架；已有文件保留 |
| iteration N `build-skills` | 主要更新状态 | 新 skill 被构建；已有 skill 被原地更新 |
| 小改动 | 无变化 | 直接编辑实现 |

## 最终解释

当前 Astra Studio 的目标模型可以概括为：

- 域知识是持续累积的，保留在 `studio/changes/{domain}`
- 插件工作区是**持续活跃的**变更记录（promote 后保留，不删除）
- 实现始终存在于 `target_dir`
- promote 将设计文档**复制**到 `studio/archive/`（里程碑快照），活跃工作区保留供下一轮迭代
- `build-skills` 产出初稿（初始填充），用户用 `skill-creator` 迭代优化
- `skill-design` 自动检测插件特征（stateful、hil-gated 等），驱动 `spec-generate` 产出条件性脚手架
- 用户负责阶段确认
- 系统负责阶段执行

这个模型的核心价值在于：

- 用户只判断方向
- 系统完成构建（初始填充 + 条件性脚手架）
- 设计过程可追踪（版本化归档）
- 实现始终保持唯一事实源
- 迭代永不停止（promote 是里程碑，不是终点）
