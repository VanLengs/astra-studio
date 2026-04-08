---
name: generate-brainmap
description: Generate platform brainmap documentation — a master index with Mermaid mindmap plus per-module agent detail documents. Each agent is documented with skill inventory, data/knowledge dependencies, and model/tool dependencies. Works for any industry vertical (elderly care, education, healthcare, etc.).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
user-invocable: true
---

# generate-brainmap

## Overview

The brainmap is the core intellectual map of an industry AI model platform. It organizes all AI agents by functional module, documents their capabilities, and maps their technical dependencies. This is Step 1 of the platform documentation pipeline.

## Inputs Required

1. **Domain workspace** (`studio/changes/{domain}/`):
   - `event-storm.md` — business events, user journeys, pain points
   - `domain-map.md` — domain analysis with plugin candidates
   - `personas/` — persona cards
   - `journeys/` — journey maps
   - `processes/` — process flows
2. **Plugin workspaces** (`studio/changes/{plugin-name}/`):
   - `skill-map.md` — skill breakdown for each plugin
   - `brief.md` — business context
3. **Implementation files** (target directories):
   - `skills/*/SKILL.md` — built skill definitions (for detailed capability extraction)
   - `agents/*.md` — agent role definitions (if any exist)
4. **Platform configuration** (gathered from user or inferred):
   - Platform name (e.g., "幼教行业大模型", "康养行业大模型")
   - Industry domain (e.g., "early education", "elderly care")
   - Service model (e.g., G-B-C, B2B, B2C)
   - Target audience description

## Workflow

### Step 1: Gather Context

- Read domain workspace: `event-storm.md`, `domain-map.md`
- Read all plugin skill-maps from `studio/changes/*/skill-map.md`
- Read all built SKILL.md files from target directories
- Read existing agent definitions if any
- If `$ARGUMENTS` contains a platform name, use it; otherwise ask

### Step 2: Define Module Structure

Analyze the domain-map and skill-maps to organize plugins into functional modules. Each module groups related plugins that serve the same business function area. Typical module count: 5–10.

For each module, define:
- Module number and name (in Chinese, descriptive of the functional area)
- Which plugins belong to this module
- How many agents this module needs (typically 3–10 per module)

### Step 3: Define Agents per Module

For each module, define AI agents. Each agent represents a specialized AI role with:
- Agent number (global sequential, e.g., #1, #2, …)
- Agent name (Chinese, descriptive role title, e.g., "幼儿行为观察AI助手")
- English slug (e.g., "Behavior-Observation-AI")
- Associated plugin and skills
- Core capability description (1–2 sentences)

Agent count per module should reflect the complexity and scope of skills in that module. Typically each agent covers 2–5 related skills.

### Step 4: Generate brainmap-index.md

Write `{output_dir}/brainmap-index.md` with the following structure:

```markdown
# {emoji} {industry}智能体全景脑图 — 总索引

> {platform_name}
> {total_agents} 个专业智能体 · {module_count} 大模块 · {plugin_count} 个 Plugin · {skill_count} 个 Skill
> 覆盖 {service_model} 三端

---

## 模块总览

| 模块 | 智能体数 | 关联 Plugin | 详细文档 |
|------|:--------:|-------------|----------|
| 模块一：{name} | {n} | {plugins} | [brainmap-module-1.md](brainmap-module-1.md) |
| … | … | … | … |

---

## 全景脑图 (Mermaid)

​```mermaid
mindmap
  root(({platform_name}))
    {module_1_name}
      {agent_1}
      {agent_2}
      …
    {module_2_name}
      …
​```

---

## 智能体主索引

| # | 智能体名称 | 所属模块 | 关联 Plugin | 核心技能数 |
|:-:|-----------|---------|-------------|:----------:|
| 1 | {agent_name} | {module} | {plugin} | {skill_count} |
| … | … | … | … | … |

---

## 跨模块协同场景

List 4–6 cross-module collaboration scenarios showing how agents from different modules work together.

---

## 数据资产概览

Summary of data assets: total data items, policy/regulation count, assessment tool count, knowledge docs count, etc.
```

### Step 5: Generate brainmap-module-N.md (one per module)

For each module, write `{output_dir}/brainmap-module-{N}.md` with the following structure:

```markdown
# 模块{N}：{module_name}类智能体（{agent_count}个）

> {module_description}
> 关联 Plugin：{plugin_list}

---

## 智能体 #{global_num}：{agent_name}（{english_slug}）

> {capability_description}

### 1. 技能清单

| 技能名称 | 所属 Plugin | 功能描述 | 关键输出 |
|----------|-----------|---------|---------|
| {skill} | {plugin} | {description} | {output} |

### 2. 数据与知识依赖

| 类别 | 数据项 | 来源 | 更新频率 | 用途 |
|------|-------|------|---------|------|

Categories (9 standard categories, select applicable):

1. 个体基础数据 (individual base data)
2. 健康/评估数据 (health/assessment data)
3. 行为/活动数据 (behavior/activity data)
4. 环境/设施数据 (environment/facility data)
5. 政策法规 (policies and regulations)
6. 行业标准/规范 (industry standards)
7. 专业知识库 (professional knowledge base)
8. 历史档案数据 (historical records)
9. 外部参考数据 (external reference data)

### 3. 模型与工具依赖

| 类别 | 名称 | 用途 | 输入 → 输出 |
|------|------|------|------------|

Categories (7 standard categories, select applicable):

1. NLP/LLM 模型 (natural language models)
2. 计算机视觉模型 (computer vision)
3. 预测/分类模型 (prediction/classification)
4. 时序分析模型 (time series)
5. 推荐/优化模型 (recommendation/optimization)
6. 知识图谱工具 (knowledge graph tools)
7. 数据分析工具 (data analysis tools)

### 4. 典型应用场景

Describe 2–3 concrete usage scenarios showing this agent in action.

---

(repeat for each agent in this module)

---

## 模块小结

| 指标 | 数值 |
|------|------|
| 智能体数 | {count} |
| 覆盖技能数 | {count} |
| 数据依赖项 | {count} |
| 模型依赖项 | {count} |
```

### Step 6: Parallelization Strategy

When generating, use parallel generation for speed:

- **Agent A**: `brainmap-index.md`
- **Agent B**: modules 1–2 (if ≤ 8 modules)
- **Agent C**: modules 3–4
- **Agent D**: remaining modules

Use the Agent tool to spawn sub-agents for parallel module generation.

## Output Location

Default: `{project_root}/docs/`

Can be overridden via `$ARGUMENTS` (e.g., `generate-brainmap output=./platform-docs/`).

## Quality Checks

1. All plugins from domain-map are covered by at least one agent
2. All skills from skill-maps are referenced in at least one agent's skill inventory
3. Agent numbering is globally sequential with no gaps
4. Module boundaries are clean — no skill appears in two modules unless explicitly cross-cutting
5. Mermaid mindmap renders without syntax errors
6. Internal links between index and module files are consistent

## Does NOT

- Generate tech design documents (that's `generate-tech-designs`)
- Generate the agent-plugin mapping (that's `generate-agent-mapping`)
- Create implementation code or SKILL.md files
- Modify planning artifacts
