# Market Analysis Framework Template

## Template Metadata
```json
{
  "template_id": "market_analysis",
  "name": "📊 Market Analysis Framework",
  "description": "Deep dive into market opportunities and competitive landscape",
  "category": "Marketing",
  "version": "1.0",
  "author": "Business Assistant AI",
  "stages_count": 5
}
```

## Template Configuration

### Stage 1: Market Overview
**Key**: `market_overview`
**Title**: Market Overview
**Prompt**: Let's start with understanding your market. What market or industry are you analyzing?

**Examples**:
- 🛍️ E-commerce and online retail
- 🏥 Healthcare and medical services
- 💼 B2B software and services
- 🎓 Education and e-learning
- 🏦 Financial services and fintech
- 🏠 Real estate and property management
- 🚗 Transportation and logistics
- 🍔 Food and beverage industry
- 🎮 Gaming and entertainment
- 🌱 Sustainability and green technology

**Follow-up Questions**:
- What specific segment within this market?
- What geographic regions are you considering?
- What's driving your interest in this market?

**JSON Structure**:
```json
{
  "industry": "string",
  "market_segment": "string",
  "geographic_scope": ["string"],
  "market_interest_driver": "string",
  "market_size_estimate": "string"
}
```

### Stage 2: Target Customer Analysis
**Key**: `target_customers`
**Title**: Target Customer Analysis
**Prompt**: Who are your target customers and what are their characteristics?

**Examples**:
- 👥 Demographics (age, income, location, education)
- 🎯 Psychographics (values, interests, lifestyle)
- 💼 Business characteristics (company size, industry, role)
- 🛒 Buying behavior and decision-making process
- 📱 Technology adoption and preferences
- 💰 Budget and spending patterns
- 😊 Pain points and unmet needs

**Follow-up Questions**:
- What's the primary customer segment you're targeting?
- How do they currently solve the problem you're addressing?
- What influences their purchasing decisions?

**JSON Structure**:
```json
{
  "primary_segment": "string",
  "customer_demographics": ["string"],
  "customer_psychographics": ["string"],
  "pain_points": ["string"],
  "buying_behavior": "string",
  "decision_influencers": ["string"]
}
```

### Stage 3: Competitive Landscape
**Key**: `competitive_analysis`
**Title**: Competitive Landscape
**Prompt**: Who are your main competitors and how do you compare?

**Examples**:
- 🏢 Direct competitors (same product/service)
- 🔄 Indirect competitors (alternative solutions)
- 🆕 New entrants and emerging threats
- 💪 Competitor strengths and advantages
- 🔍 Competitor weaknesses and gaps
- 💰 Pricing strategies and models
- 📈 Market share and positioning

**Follow-up Questions**:
- Who do you see as your biggest competitive threat?
- What differentiates you from competitors?
- How do competitors price their offerings?

**JSON Structure**:
```json
{
  "direct_competitors": ["string"],
  "indirect_competitors": ["string"],
  "competitive_advantages": ["string"],
  "competitor_weaknesses": ["string"],
  "pricing_comparison": ["string"],
  "differentiation_factors": ["string"]
}
```

### Stage 4: Market Opportunity Assessment
**Key**: `market_opportunity`
**Title**: Market Opportunity Assessment
**Prompt**: What's the size and potential of this market opportunity?

**Examples**:
- 📊 Total Addressable Market (TAM)
- 🎯 Serviceable Addressable Market (SAM)
- 🔍 Serviceable Obtainable Market (SOM)
- 📈 Market growth rate and trends
- 🌟 Emerging opportunities and gaps
- 🚀 Technology trends enabling growth
- 📅 Market timing and seasonality

**Follow-up Questions**:
- What's your realistic market share goal?
- What trends are driving market growth?
- Are there any regulatory or economic factors to consider?

**JSON Structure**:
```json
{
  "market_size_tam": "string",
  "market_size_sam": "string",
  "market_size_som": "string",
  "growth_rate": "string",
  "market_trends": ["string"],
  "opportunity_gaps": ["string"]
}
```

### Stage 5: Go-to-Market Strategy
**Key**: `gtm_strategy`
**Title**: Go-to-Market Strategy
**Prompt**: How will you enter and compete in this market?

**Examples**:
- 🎯 Market entry strategy (direct, partnerships, acquisition)
- 💰 Pricing strategy and revenue model
- 📢 Marketing and promotion channels
- 🤝 Sales strategy and distribution channels
- 🚀 Launch timeline and rollout plan
- 📈 Scaling and expansion strategy
- 💡 Unique value proposition

**Follow-up Questions**:
- What's your primary route to market?
- How will you acquire your first customers?
- What's your competitive positioning strategy?

**JSON Structure**:
```json
{
  "entry_strategy": "string",
  "pricing_model": "string",
  "marketing_channels": ["string"],
  "sales_channels": ["string"],
  "value_proposition": "string",
  "launch_timeline": "string",
  "scaling_plan": "string"
}
```
