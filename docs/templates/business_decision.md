# Business Decision Framework Template

## Template Metadata
```json
{
  "template_id": "business_decision",
  "name": "🏢 Business Decision Framework",
  "description": "Comprehensive analysis for strategic business decisions",
  "category": "Strategy",
  "version": "1.0",
  "author": "Business Assistant AI",
  "stages_count": 7
}
```

## Template Configuration

### Stage 1: Problem Identification
**Key**: `problem_definition`
**Title**: Problem Identification
**Prompt**: Let's start by understanding the core business challenge. What problem are you trying to solve?

**Examples**:
- 📊 Reduce manual reporting time and improve accuracy
- 💰 Cut operational costs while maintaining quality
- 🚀 Scale operations to handle growing demand
- 🎯 Improve customer satisfaction and retention
- 📈 Increase sales conversion rates
- 🔧 Streamline internal processes and workflows
- 💡 Launch a new product or service
- 🔍 Better understand market opportunities

**Follow-up Questions**:
- What's the current pain point costing you in time/money?
- How urgent is solving this problem?
- What happens if this problem isn't solved?

**JSON Structure**:
```json
{
  "primary_problem": "string",
  "pain_points": ["string"],
  "urgency_level": "low|medium|high|critical",
  "cost_of_inaction": "string"
}
```

### Stage 2: Stakeholder Analysis
**Key**: `stakeholders`
**Title**: Stakeholder Analysis
**Prompt**: Who are the key people involved in this decision and its implementation?

**Examples**:
- 👥 Internal team members (employees, managers)
- 🤝 External customers or clients
- 🏢 Business partners or suppliers
- 💼 Investors or board members
- 🎯 Regulatory bodies or compliance teams
- 📊 Data and analytics teams

**Follow-up Questions**:
- Who has the final decision-making authority?
- Who will be most affected by the changes?
- What are their main concerns or requirements?

**JSON Structure**:
```json
{
  "decision_makers": ["string"],
  "affected_parties": ["string"],
  "influencers": ["string"],
  "concerns": ["string"]
}
```

### Stage 3: Solution Approach
**Key**: `solution_approach`
**Title**: Solution Approach
**Prompt**: What type of solution are you considering?

**Examples**:
- 🛠️ Technology implementation (software, automation)
- 📋 Process improvement or restructuring
- 👥 Hiring or team reorganization
- 🤝 Partnership or outsourcing
- 📈 Marketing or sales strategy change
- 💰 Financial restructuring or investment
- 🎓 Training or skill development
- 🔄 Operational efficiency improvements

**Follow-up Questions**:
- Have you tried similar solutions before?
- What's your preferred approach and why?
- Are there any solutions you want to avoid?

**JSON Structure**:
```json
{
  "preferred_type": "string",
  "alternatives_considered": ["string"],
  "past_attempts": ["string"],
  "constraints": ["string"]
}
```

### Stage 4: Resource Requirements
**Key**: `resources`
**Title**: Resource Requirements
**Prompt**: What resources do you have available for this initiative?

**Examples**:
- 💰 Budget: Under €10K | €10K-50K | €50K-100K | €100K+
- ⏰ Timeline: 1-3 months | 3-6 months | 6-12 months | 12+ months
- 👥 Team: Solo | Small team (2-5) | Medium team (5-15) | Large team (15+)
- 🛠️ Technical expertise: None | Basic | Intermediate | Advanced
- 📊 Data availability: Limited | Moderate | Extensive

**Follow-up Questions**:
- What's your maximum budget for this project?
- How much time can you dedicate weekly?
- What skills are missing from your current team?

**JSON Structure**:
```json
{
  "budget_range": "string",
  "timeline": "string",
  "team_size": "string",
  "technical_expertise": "string",
  "data_availability": "string",
  "constraints": ["string"]
}
```

### Stage 5: Success Metrics
**Key**: `success_criteria`
**Title**: Success Metrics
**Prompt**: How will you measure success for this initiative?

**Examples**:
- 💰 Cost reduction (% savings or absolute amount)
- ⏱️ Time savings (hours saved per week/month)
- 📈 Revenue increase (% growth or absolute amount)
- 😊 Customer satisfaction improvement
- 🎯 Quality metrics (error reduction, accuracy improvement)
- 📊 Productivity gains (output per hour/employee)
- 🔄 Process efficiency (cycle time reduction)
- 📋 Compliance or risk reduction

**Follow-up Questions**:
- What's your target improvement percentage?
- When do you expect to see initial results?
- What would make this a clear success?

**JSON Structure**:
```json
{
  "primary_metrics": ["string"],
  "target_improvements": {"metric": "target_value"},
  "timeline_to_results": "string",
  "success_definition": "string"
}
```

### Stage 6: Implementation Plan
**Key**: `implementation`
**Title**: Implementation Plan
**Prompt**: How do you want to approach the implementation?

**Examples**:
- 🚀 Full deployment (all at once)
- 📈 Phased rollout (step by step)
- 🧪 Pilot program first (test with small group)
- 🔄 Iterative approach (continuous improvement)
- 📋 Outsourced implementation
- 🏠 In-house development

**Follow-up Questions**:
- Do you have any fixed deadlines?
- What's your risk tolerance for this project?
- Who will lead the implementation?

**JSON Structure**:
```json
{
  "approach": "string",
  "phases": ["string"],
  "timeline": "string",
  "leadership": "string",
  "dependencies": ["string"]
}
```

### Stage 7: Risk Assessment
**Key**: `risk_management`
**Title**: Risk Assessment
**Prompt**: What risks are you most concerned about?

**Examples**:
- 💸 Budget overruns
- ⏰ Timeline delays
- 👥 Team resistance to change
- 🛡️ Security or compliance issues
- 📊 Data quality problems
- 🔧 Technical integration challenges
- 🏢 Market or business environment changes
- 🤝 Vendor or partner reliability

**Follow-up Questions**:
- What's your biggest fear about this project?
- How would you handle potential setbacks?
- What contingency plans do you need?

**JSON Structure**:
```json
{
  "identified_risks": ["string"],
  "risk_levels": {"risk": "low|medium|high"},
  "mitigation_strategies": ["string"],
  "contingency_plans": ["string"]
}
```
