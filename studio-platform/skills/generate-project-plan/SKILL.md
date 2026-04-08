---
name: generate-project-plan
description: Generate a comprehensive project implementation plan from planning artifacts — parallel development tracks, Gantt chart with Mermaid, milestones, team composition, risk analysis, and deliverable checklist. Adapts to project scale and plugin count.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

### Overview
The project plan translates all planning and design artifacts into an actionable implementation roadmap. It defines parallel development tracks, resource allocation, milestones, and risk mitigation strategies. This is Step 4 of the platform documentation pipeline.

### Inputs Required
1. **All previously generated docs**: brainmap-index.md, agent-plugin-mapping.md, 5 tech design docs
2. **Domain workspace**: domain-map.md (plugin candidates, dependencies, complexity)
3. **Plugin workspaces**: skill-map.md (skill count, complexity tiers), brief.md
4. **Platform configuration**: team size, timeline constraints, technology preferences

### Workflow

#### Step 1: Analyze Scope
- Count plugins, skills, agents, data entities, models, knowledge bases
- Classify skills by complexity tier (from skill-maps)
- Identify critical path dependencies

#### Step 2: Define Development Tracks (typically 6-10)
Parallel work streams, each with clear ownership:
- Track 1: 基础设施与环境 (infrastructure)
- Track 2: 数据管道 (data pipeline — DW + collection)
- Track 3: 知识图谱与RAG (KG + RAG system)
- Track 4: ML模型训练 (ML model training)
- Track 5: 前端与交互 (frontend + UX)
- Track 6-N: 智能体开发 (agent/plugin development — grouped by module)
- Final Track: 集成测试与上线 (integration + launch)

#### Step 3: Generate Gantt Chart
Mermaid gantt chart showing all tracks and milestones:
```mermaid
gantt
    title {platform_name} 实施计划
    dateFormat YYYY-MM-DD
    ...
```

#### Step 4: Define Milestones (typically 5-8)
| 里程碑 | 时间节点 | 交付物 | 验收标准 |
|--------|---------|--------|---------|

#### Step 5: Team Composition
Role-based staffing plan with headcount and responsibilities.

#### Step 6: Risk Analysis
| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|---------|

#### Step 7: Deliverables Checklist
Phase-by-phase deliverable list with acceptance criteria.

### Output Structure
```markdown
# {industry}行业大模型 — 项目实施计划

## 1. 项目概述 (scope summary with key metrics)
## 2. 整体架构 (platform architecture diagram)
## 3. 实施路线 (development tracks with Gantt)
## 4. 里程碑计划 (milestones)
## 5. 团队配置 (team composition)
## 6. 技术选型 (technology stack)
## 7. 风险管理 (risk management)
## 8. 质量保障 (quality assurance)
## 9. 交付物清单 (deliverables)
## 10. 附录 (appendices)
```

### Output Location
`{output_dir}/project-plan.md`

### Quality Checks
1. All plugins appear in at least one development track
2. Dependencies are respected (no task starts before its dependency)
3. Gantt chart renders correctly in Mermaid
4. Team size is realistic for the scope
5. Milestones cover the full project lifecycle
