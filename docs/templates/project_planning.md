# Project Planning Framework Template

## Template Metadata
```json
{
  "template_id": "project_planning",
  "name": "📋 Project Planning Framework",
  "description": "Structured approach for project initialization and planning",
  "category": "Project Management",
  "version": "1.0",
  "author": "Business Assistant AI",
  "stages_count": 6
}
```

## Template Configuration

### Stage 1: Project Scope Definition
**Key**: `project_scope`
**Title**: Project Scope Definition
**Prompt**: Let's define what your project aims to achieve. What is the main goal?

**Examples**:
- 🎯 Develop a new software application
- 🏗️ Implement a new business process
- 📈 Launch a marketing campaign
- 🔧 Upgrade existing technology infrastructure
- 👥 Reorganize team structure
- 📊 Create a data analytics solution
- 🎨 Redesign website or user interface
- 📱 Build a mobile application

**Follow-up Questions**:
- What specific deliverables do you expect?
- What's included and what's explicitly excluded?
- How does this align with broader company goals?

**JSON Structure**:
```json
{
  "main_goal": "string",
  "deliverables": ["string"],
  "inclusions": ["string"],
  "exclusions": ["string"],
  "strategic_alignment": "string"
}
```

### Stage 2: Team and Resources
**Key**: `team_resources`
**Title**: Team and Resources
**Prompt**: What team and resources will be involved in this project?

**Examples**:
- 👥 Internal team (developers, designers, analysts)
- 🤝 External contractors or consultants
- 💰 Budget allocation and financial resources
- 🛠️ Technology and infrastructure requirements
- 📚 Training and skill development needs
- 🏢 Physical space or equipment requirements

**Follow-up Questions**:
- Who will be the project manager or lead?
- What skills are currently available vs. needed?
- What's the total budget available?

**JSON Structure**:
```json
{
  "team_members": ["string"],
  "roles_responsibilities": {"role": "responsibility"},
  "budget_allocation": "string",
  "technology_requirements": ["string"],
  "skill_gaps": ["string"]
}
```

### Stage 3: Timeline and Milestones
**Key**: `timeline_milestones`
**Title**: Timeline and Milestones
**Prompt**: What's your timeline and what are the key milestones?

**Examples**:
- 🚀 Project kickoff and initial setup
- 📋 Requirements gathering and analysis
- 🎨 Design and prototyping phase
- 🔧 Development and implementation
- 🧪 Testing and quality assurance
- 📦 Deployment and launch
- 📈 Post-launch monitoring and optimization

**Follow-up Questions**:
- When does the project need to be completed?
- Are there any fixed deadlines or constraints?
- What are the dependencies between phases?

**JSON Structure**:
```json
{
  "project_duration": "string",
  "key_milestones": [{"milestone": "date"}],
  "critical_deadlines": ["string"],
  "dependencies": ["string"]
}
```

### Stage 4: Success Criteria and KPIs
**Key**: `success_kpis`
**Title**: Success Criteria and KPIs
**Prompt**: How will you measure project success?

**Examples**:
- ✅ On-time delivery within deadline
- 💰 Within budget completion
- 🎯 Meeting all functional requirements
- 😊 User satisfaction and adoption rates
- 📈 Performance improvements achieved
- 🔧 Quality metrics and defect rates
- 📊 Business value delivered

**Follow-up Questions**:
- What would make this project a clear success?
- How will you track progress during the project?
- What metrics will stakeholders care about most?

**JSON Structure**:
```json
{
  "success_criteria": ["string"],
  "kpi_metrics": ["string"],
  "tracking_methods": ["string"],
  "stakeholder_priorities": ["string"]
}
```

### Stage 5: Risk Management
**Key**: `risk_management`
**Title**: Risk Management
**Prompt**: What risks do you anticipate and how will you manage them?

**Examples**:
- ⏰ Schedule delays and timeline risks
- 💸 Budget overruns and cost escalation
- 👥 Team member availability and turnover
- 🔧 Technical challenges and integration issues
- 📋 Scope creep and changing requirements
- 🤝 Stakeholder alignment and communication
- 🛡️ Security and compliance risks

**Follow-up Questions**:
- What's the biggest risk that keeps you up at night?
- How will you monitor and respond to risks?
- What contingency plans do you need?

**JSON Structure**:
```json
{
  "identified_risks": ["string"],
  "risk_impact_probability": {"risk": "impact_level"},
  "mitigation_strategies": ["string"],
  "contingency_plans": ["string"]
}
```

### Stage 6: Communication and Governance
**Key**: `communication_governance`
**Title**: Communication and Governance
**Prompt**: How will you manage communication and project governance?

**Examples**:
- 📅 Regular status meetings and updates
- 📊 Progress reporting and dashboards
- 🤝 Stakeholder engagement plan
- 📝 Documentation and knowledge sharing
- ✅ Decision-making processes and approvals
- 🔄 Change management procedures

**Follow-up Questions**:
- Who are the key stakeholders to keep informed?
- How often will you provide updates?
- What decisions require formal approval?

**JSON Structure**:
```json
{
  "stakeholder_map": ["string"],
  "communication_frequency": "string",
  "reporting_methods": ["string"],
  "decision_authority": ["string"],
  "change_process": "string"
}
```
