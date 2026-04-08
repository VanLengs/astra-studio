---
name: generate-tech-designs
description: Generate five technical infrastructure design documents for an industry AI model platform — data warehouse (Kimball dimensional modeling), data collection pipeline, knowledge graph ontology, ML model portfolio, and RAG retrieval system. Each document provides production-ready architectural specifications derived from planning artifacts.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Agent
user-invocable: true
---

# Generate Technical Design Documents

## Overview

The technical design documents define the data and AI infrastructure that powers the platform's intelligent agents. They translate the business capabilities documented in brainmap and agent-mapping into concrete technical specifications. This is **Step 3** of the platform documentation pipeline.

Five documents are produced:

| Document | Focus |
|----------|-------|
| `data-warehouse-design.md` | Kimball dimensional modeling — ODS → DWD → DWS → DM → ADS |
| `data-collection-design.md` | Edge-cloud ingestion pipelines, IoT protocols, quality framework |
| `knowledge-graph-design.md` | Ontology design, sub-graphs, extraction pipelines, reasoning |
| `ml-models-design.md` | Model portfolio, model cards, coverage matrix, MLOps |
| `rag-system-design.md` | Knowledge bases, hybrid retrieval, prompt engineering |

## Inputs Required

1. **Brainmap documents**: `brainmap-index.md` + `brainmap-module-*.md` (for agent capabilities and dependencies)
2. **Agent-plugin mapping**: `agent-plugin-mapping.md` (for coverage and feature matrix)
3. **Domain workspace**: `event-storm.md`, `domain-map.md`, personas, journeys, processes
4. **Plugin workspaces**: `skill-map.md`, `brief.md` (per plugin)
5. **Implementation files**: `skills/*/SKILL.md` (for detailed data requirements)
6. **Platform configuration**: platform name, industry domain, scale estimates

## Workflow

### Step 1: Analyze Data Requirements

Scan all SKILL.md files and agent definitions to extract:

- **Data entities** mentioned (people, organizations, activities, assessments, etc.)
- **Data operations** (CRUD, aggregation, trend analysis, prediction)
- **External data sources** needed (IoT devices, business systems, government systems)
- **Knowledge domains** referenced (policies, standards, professional knowledge)
- **ML/AI capabilities** used (NLP, CV, prediction, recommendation, optimization)

Use Glob to discover all relevant files, then Grep/Read to extract data references.

### Step 2: Generate data-warehouse-design.md

Write `{output_dir}/data-warehouse-design.md` with the following structure:

```markdown
# {industry}行业大模型 — 数仓设计文档

## 1. 设计概述
Brief: Kimball dimensional modeling approach, industry context, scale estimates.

## 2. 整体架构
Multi-layer data warehouse architecture (ASCII diagram):

ADS (Application Data Service) — dashboards, reports, API
  ↑
DM (Data Mart) — domain-specific analytical cubes
  ↑
DWS (Data Warehouse Summary) — aggregated indicators
  ↑
DWD (Data Warehouse Detail) — cleaned & standardized facts
  ↑
DIM (Dimension) — shared dimension tables
  ↑
ODS (Operational Data Store) — raw operational data

## 3. 维度表设计
For each dimension (typically 8-15):
### DIM_{entity_name}
| 字段名 | 数据类型 | 说明 | 示例 |
|--------|---------|------|------|
| {field} | {type} | {desc} | {example} |

Standard dimensions to consider:
- 人员维度 (person/individual)
- 机构/组织维度 (organization)
- 时间维度 (time)
- 地理维度 (geography)
- 服务类型维度 (service type)
- 设备维度 (device/equipment)
- Plus domain-specific dimensions

## 4. 事实表设计
For each fact table (typically 15-25):
### FACT_{event_name}
| 字段名 | 数据类型 | 说明 | 关联维度 |
|--------|---------|------|---------|
| {field} | {type} | {desc} | DIM_{ref} |

Fact tables should map to key business events from event-storm.

## 5. 汇总层设计 (DWS)
For each summary table (typically 3-6):
### DWS_{summary_name}
Aggregation logic, refresh frequency, key indicators.

## 6. 总线矩阵
Cross-reference fact tables × dimensions:
| 事实表 | DIM_时间 | DIM_人员 | DIM_机构 | ... |
|--------|:-------:|:-------:|:-------:|:---:|
| FACT_X | ✓       | ✓       | —       | ... |

## 7. ETL 流程设计
Data flow from source → ODS → DWD → DWS → DM → ADS.

## 8. 数据质量规则
Quality checks per layer.

## 9. 容量规划
Estimated data volumes, growth rates, storage requirements.
```

### Step 3: Generate data-collection-design.md

Write `{output_dir}/data-collection-design.md` with the following structure:

```markdown
# {industry}行业大模型 — 数据采集设计文档

## 1. 数据源全景
Categorize all data sources:
- IoT/传感器数据 (IoT/sensor data) — list device types, data formats, frequencies
- 业务系统数据 (business system data) — list systems, APIs, sync methods
- 政府/监管数据 (government/regulatory data) — list systems, formats
- 用户交互数据 (user interaction data) — app events, feedback, queries
- 外部知识数据 (external knowledge data) — policies, standards, research
- 第三方数据 (third-party data) — weather, demographics, market data

For each source:
| 数据源 | 类型 | 格式 | 频率 | 协议 | 数据量/日 |
|--------|------|------|------|------|----------|

## 2. 采集架构
Edge-cloud architecture with:
- 边缘层 (edge layer) — local data collection and preprocessing
- 传输层 (transport layer) — protocols (MQTT, HTTP, gRPC)
- 接入层 (ingestion layer) — Kafka, Flink, API gateway
- 处理层 (processing layer) — real-time + batch processing
- 存储层 (storage layer) — time-series DB, RDBMS, object storage

## 3. IoT设备接入规范 (if applicable)
Device specifications per type.

## 4. 数据处理流水线
Real-time stream processing + batch processing pipelines.

## 5. 数据质量框架
6-dimension quality framework: completeness, accuracy, timeliness, consistency, uniqueness, validity.

## 6. 隐私合规设计
Data anonymization, consent management, data lifecycle, compliance standards.

## 7. 监控告警
Data pipeline monitoring, anomaly detection, SLA tracking.
```

### Step 4: Generate knowledge-graph-design.md

Write `{output_dir}/knowledge-graph-design.md` with the following structure:

```markdown
# {industry}行业大模型 — 知识图谱设计文档

## 1. 本体设计
### 实体类型 (typically 15-25)
| 实体类型 | 英文标识 | 属性数 | 说明 | 数据来源 |
|---------|---------|:------:|------|---------|

### 关系类型 (typically 20-30)
| 关系 | 源实体 | 目标实体 | 属性 | 说明 |
|------|--------|---------|------|------|

## 2. 子图设计 (typically 4-7 sub-graphs)
For each sub-graph:
### 子图{N}: {name}子图
- Entities involved
- Key relations
- Cypher/SPARQL query examples
- Use cases

## 3. 知识抽取管道
- 结构化数据导入 (structured data import)
- 非结构化文本抽取 (unstructured text extraction)
- 规则引擎 (rule engine)
- 人工审核 (human review)

## 4. 知识推理
Inference rules, path queries, pattern matching.

## 5. 存储与索引
Neo4j (graph), Milvus (vectors), StarRocks (analytics).

## 6. 规模估算
Entity count, relation count, total triples.

## 7. 实施计划
Phase-by-phase graph construction.
```

### Step 5: Generate ml-models-design.md

Write `{output_dir}/ml-models-design.md` with the following structure:

```markdown
# {industry}行业大模型 — ML模型设计文档

## 1. 模型全景
Categorize models by function (typically 5-7 categories, 15-25 models total):
- A类: 预测/分类模型 (prediction/classification)
- B类: 时序分析模型 (time series analysis)
- C类: 计算机视觉模型 (computer vision)
- D类: NLP/语音模型 (NLP/speech)
- E类: 优化/推荐模型 (optimization/recommendation)
- F类: 图分析模型 (graph analysis)
- G类: 领域专用模型 (domain-specific)

## 2. 模型卡片 (per model)
### 模型 {category}{num}: {model_name}
| 属性 | 说明 |
|------|------|
| 模型类型 | {type} |
| 核心算法 | {algorithm} |
| 训练数据 | {training_data} |
| 输入特征 | {features} |
| 输出 | {output} |
| 评估指标 | {metrics} |
| 服务智能体 | #{agent_nums} |
| 更新频率 | {frequency} |

## 3. 模型覆盖矩阵
| 模型 | Agent-1 | Agent-2 | ... |
|------|:-------:|:-------:|:---:|

## 4. MLOps 流水线
Training → validation → deployment → monitoring → retraining.

## 5. 算力需求
GPU/CPU requirements, inference latency targets.

## 6. 模型治理
Version control, A/B testing, model cards, bias detection.
```

### Step 6: Generate rag-system-design.md

Write `{output_dir}/rag-system-design.md` with the following structure:

```markdown
# {industry}行业大模型 — RAG系统设计文档

## 1. 知识库全景
List all knowledge bases (typically 12-25):
| 知识库 | 文档类型 | 预估文档数 | 预估Chunk数 | 关联智能体 | 更新频率 |
|--------|---------|:--------:|:---------:|----------|---------|

Categories:
- 政策法规库 (policies & regulations)
- 行业标准库 (industry standards)
- 专业指南库 (professional guidelines)
- 评估工具库 (assessment tools)
- 培训教材库 (training materials)
- 案例库 (case studies)
- Plus domain-specific knowledge bases

## 2. 文档处理管道
Ingestion → parsing → chunking → embedding → indexing.
- Chunking strategies: semantic, fixed-size, hierarchical
- Embedding models: text-embedding-ada-002, BGE, etc.

## 3. 检索架构
Multi-stage hybrid retrieval:
- 语义检索 (semantic) — Milvus vector search
- 关键词检索 (keyword) — BM25 / Elasticsearch
- 图检索 (graph) — Neo4j path queries
- 结构化检索 (structured) — SQL queries

## 4. 检索增强策略
Query rewriting, hypothetical document embedding, reranking, context compression.

## 5. 提示词工程
Prompt templates for different agent roles.

## 6. 评估与优化
Retrieval metrics (Recall@K, MRR, NDCG), generation quality metrics.

## 7. 缓存与性能
Query caching, embedding caching, latency optimization.
```

### Parallelization Strategy

The 5 documents can be generated in parallel since they share input data but produce independent outputs. Use the Agent tool to split work:

- **Agent A** — data-warehouse-design.md + data-collection-design.md (data layer, shared context)
- **Agent B** — knowledge-graph-design.md + ml-models-design.md + rag-system-design.md (AI layer, shared context)

Provide each agent with the full set of extracted data requirements from Step 1 so they can work independently.

## Quality Checks

After all 5 documents are generated, verify:

1. All agents from brainmap are referenced in at least one design document
2. Data entities in DW design are consistent with KG entity types
3. ML models referenced by agents exist in ml-models-design
4. RAG knowledge bases cover all knowledge dependencies from brainmap
5. Data collection sources feed into DW fact tables
6. Scale estimates are internally consistent across documents

## Does NOT

- Generate brainmap documents (that's `generate-brainmap`)
- Generate agent-plugin mapping (that's `generate-agent-mapping`)
- Implement actual data pipelines or models
- Modify planning artifacts
