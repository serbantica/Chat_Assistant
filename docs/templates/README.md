# Template Format Documentation

This directory contains conversation templates for the Business Decision Assistant. Each template follows a standardized format to ensure consistency and easy integration.

## Template Structure

Each template file should follow this structure:

### 1. Template Metadata
```json
{
  "template_id": "unique_identifier",
  "name": "🎯 Display Name with Emoji",
  "description": "Brief description of what this template covers",
  "category": "Category (Strategy, Marketing, Operations, etc.)",
  "version": "1.0",
  "author": "Template Author",
  "stages_count": 5
}
```

### 2. Stage Configuration
Each stage should include:

```markdown
### Stage X: Stage Title
**Key**: `json_key_name`
**Title**: Human-readable stage title
**Prompt**: Main question or prompt for this stage

**Examples**:
- 🎯 Example option 1
- 📊 Example option 2
- 💡 Example option 3
- (etc.)

**Follow-up Questions**:
- Clarifying question 1
- Clarifying question 2
- Clarifying question 3

**JSON Structure**:
```json
{
  "field1": "data_type",
  "field2": ["array_type"],
  "field3": {"object": "type"}
}
```

## Template Guidelines

### Naming Conventions
- **File names**: Use lowercase with underscores (e.g., `market_analysis.md`)
- **Template IDs**: Match file name without extension
- **Stage keys**: Use snake_case (e.g., `market_overview`)

### Content Guidelines
- **Emojis**: Use relevant emojis in examples and template names
- **Examples**: Provide 6-10 diverse, actionable examples per stage
- **Follow-ups**: Include 3-4 clarifying questions per stage
- **JSON Structure**: Define clear data structure for each stage

### Categories
Current categories include:
- **Strategy**: High-level business decisions
- **Marketing**: Market analysis and go-to-market
- **Project Management**: Project planning and execution
- **Operations**: Process improvement and efficiency
- **Finance**: Financial planning and analysis
- **HR**: Human resources and team management

## Available Templates

| Template | Category | Stages | Description |
|----------|----------|--------|-------------|
| [business_decision.md](business_decision.md) | Strategy | 7 | Comprehensive business decision framework |
| [project_planning.md](project_planning.md) | Project Management | 6 | Project initialization and planning |
| [market_analysis.md](market_analysis.md) | Marketing | 5 | Market research and competitive analysis |

## Creating New Templates

1. **Choose a Category**: Select from existing categories or propose a new one
2. **Define Stages**: Plan 4-8 logical stages that build upon each other
3. **Write Examples**: Create diverse, realistic examples for each stage
4. **Test Structure**: Ensure JSON structure supports the conversation flow
5. **Follow Format**: Use the exact format shown above

## Integration

Templates are automatically loaded by the `TemplateLoader` class in the application. The system:

1. Scans this directory for `.md` files
2. Parses the metadata and stage configuration
3. Makes templates available in the UI
4. Guides conversations using the stage structure

## Template Validation

Each template should:
- [ ] Have valid metadata with all required fields
- [ ] Include 4-8 stages with complete information
- [ ] Provide diverse examples for user selection
- [ ] Define clear JSON structure for data collection
- [ ] Follow naming conventions
- [ ] Include relevant follow-up questions
