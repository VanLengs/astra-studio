---
name: generate-speech
description: Generate a presentation speech script (迎检话术) for the industry AI model platform — structured around the 4 visualization frames (dashboard, agents, knowledge network, scenarios). Professional tone suitable for government inspection or executive presentations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
user-invocable: true
---

### Overview
The speech script is a structured presentation guide designed for government inspections (迎检) or executive demonstrations. It follows the 4-frame structure of the .pen visualization and provides natural, authoritative talking points. This is Step 6 (final step) of the platform documentation pipeline.

### Inputs Required
1. **All generated docs**: brainmap-index.md, agent-mapping, tech designs, project plan
2. **.pen visualization**: {platform_name}.pen (for frame structure reference)
3. **Platform configuration**: platform name, industry, audience context (government, executive, technical)

### Speech Structure

The speech follows 5 sections corresponding to the presentation flow:

#### Section 1: 开场定位 (Opening Positioning)
- Position the platform as industry infrastructure, not just a software system
- Describe the industry challenges that necessitate an AI platform
- Frame it as: "not a traditional information system, but an industry-specific AI model foundation"
- Length: 2-3 paragraphs

#### Section 2: 全景驾驶舱 (Dashboard Overview — Frame 0)
- Explain the dashboard as the platform's "global capability view"
- Highlight that this is purpose-built for the industry, not a general AI model
- Mention key capabilities: understanding regulations, individual differences, multi-stakeholder analysis
- Length: 2-3 paragraphs

#### Section 3: 角色智能体 (Agent Roster — Frame 1)
- Present total agent count and module coverage
- Emphasize each agent has clear professional boundaries and specialized expertise
- Provide 3-4 concrete examples of agent capabilities
- Highlight the data and knowledge foundation supporting agents
- Mention cross-agent collaboration capabilities
- Length: 3-4 paragraphs (this is the core section)

#### Section 4: 知识网络 (Knowledge Network — Frame 2)
- Explain the knowledge graph as the "professional knowledge foundation"
- List types of knowledge organized: policies, standards, assessment tools, professional guidelines
- Emphasize that platform outputs are grounded in professional standards and policy basis
- Length: 1-2 paragraphs

#### Section 5: 数智场景应用 (Application Scenarios — Frame 3)
- Present scenarios organized by service endpoint (G/B/C or equivalent)
- For each endpoint, give 3-4 concrete application examples
- Conclude with the "complete closed loop" message: understanding → analysis → decision support → implementation
- Length: 2-3 paragraphs

#### Closing: 总结 (Summary)
- Summarize the platform's core value proposition
- Emphasize it as a "growing, collaborative capability system"
- Frame future benefits for the industry
- Length: 1 paragraph

### Tone Guidelines
- Authoritative but accessible (suitable for non-technical government officials)
- Use "我们" (we) for the development team perspective
- Use specific numbers and examples (avoid vague claims)
- Use professional terminology naturally (not excessively technical)
- Each section starts with a frame reference: "请各位领导看..." or "第X部分请看..."
- Four-character phrases (四字短语) used naturally but not excessively

### Output Location
`{output_dir}/迎检话术-{platform_name}.md`

### Quality Checks
1. All statistics match brainmap-index.md (agent count, module count, etc.)
2. Agent examples actually exist in the brainmap
3. Knowledge base references match rag-system-design.md
4. No residual terms from other industry projects
5. Reading length: approximately 5-8 minutes when spoken aloud
6. Professional tone maintained throughout

### Does NOT
- Generate the .pen visualization (that's generate-platform-visual)
- Create PowerPoint or PDF presentations
- Include technical implementation details (this is a business-level presentation)
