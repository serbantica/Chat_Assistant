# Template System Documentation

## 🎯 Overview

The Business Decision Assistant now features a flexible, file-based template system that allows easy addition of new conversation frameworks without code changes.

## 📁 Directory Structure

```
docs/templates/
├── README.md                    # Template format documentation
├── business_decision.md         # Business strategy framework
├── project_planning.md          # Project management framework
├── market_analysis.md           # Marketing and market research framework
└── [future_templates].md        # Easy to add new templates

src/
├── template_loader.py           # Parses markdown templates
├── templates.py                 # Template registry interface
└── app.py                       # Main application with template selection
```

## 🔧 How It Works

### 1. Template Loading Pipeline
```
Markdown Files → TemplateLoader → TemplateRegistry → ChatHandler → StreamlitUI
```

### 2. Template Structure
Each template is a markdown file with:
- **Metadata**: JSON block with template info
- **Stages**: Structured conversation phases
- **Examples**: Multiple choice options for users
- **Follow-ups**: Clarifying questions
- **JSON Schema**: Data structure for each stage

### 3. Dynamic Features
- **Auto-discovery**: New templates are automatically available
- **Validation**: Built-in template validation and error checking
- **Fallback**: Graceful handling of missing or broken templates
- **Caching**: Template configs are cached for performance

## 🚀 Current Templates

### Business Decision Framework (7 stages)
**Category**: Strategy
**Purpose**: Comprehensive business decision analysis
**Stages**: Problem → Stakeholders → Solution → Resources → Success → Implementation → Risk

### Project Planning Framework (6 stages)
**Category**: Project Management  
**Purpose**: Structured project initialization
**Stages**: Scope → Team → Timeline → Success → Risk → Governance

### Market Analysis Framework (5 stages)
**Category**: Marketing
**Purpose**: Market research and competitive analysis
**Stages**: Market → Customers → Competition → Opportunity → Strategy

## 📊 Features Delivered

### ✅ Multi-Template Support
- Template selection UI at startup
- Each template has distinct conversation flow
- Dynamic stage progression tracking

### ✅ Save/Load Functionality
- Save conversation state to JSON files
- Load previous configurations
- Download/upload configuration files
- Auto-timestamped file naming

### ✅ Progress Tracking
- Visual progress bar in sidebar
- Stage completion indicators
- Real-time progress updates
- Completed stages overview

### ✅ JSON Configuration Export
- Progressive JSON building through conversation
- Complete business analysis export
- Structured data for further processing
- Template-specific data schemas

### ✅ Template Management
- File-based template system
- Easy addition of new templates
- Template validation and error checking
- Automatic template discovery

## 🔮 Future Extensions

### Easy Template Addition
Adding a new template requires only:
1. Create new `.md` file in `docs/templates/`
2. Follow the documented format
3. Template is automatically available in UI

### Potential New Templates
- **Financial Planning Framework**
- **Risk Assessment Framework** 
- **Team Performance Analysis**
- **Customer Journey Mapping**
- **Product Launch Planning**
- **Competitive Intelligence**
- **Process Optimization**

## 🛠️ Technical Implementation

### Key Components

1. **TemplateLoader** (`template_loader.py`)
   - Parses markdown template files
   - Validates template structure
   - Provides caching for performance
   - Handles error conditions gracefully

2. **TemplateRegistry** (`templates.py`)
   - Interface layer for template access
   - Fallback handling for missing templates
   - Template validation and listing

3. **ChatHandler** (`chat_handler.py`)
   - Template-aware conversation management
   - Stage progression tracking
   - JSON configuration building
   - Context-aware AI prompting

4. **StreamlitUI** (`app.py`)
   - Template selection interface
   - Progress tracking displays
   - Save/load functionality
   - JSON preview and export

### Data Flow

1. **Startup**: Load available templates from markdown files
2. **Selection**: User chooses framework from available options
3. **Conversation**: AI guides user through template stages
4. **Progress**: Track completion and build JSON configuration
5. **Export**: Save complete analysis as structured data

## 🎯 Business Value

### For Users
- **Structured Decision Making**: Clear frameworks guide thinking
- **Consistent Analysis**: Repeatable process across decisions
- **Progress Tracking**: Visual feedback on completion
- **Data Export**: Structured output for documentation
- **Template Variety**: Different frameworks for different needs

### For Development
- **Easy Extension**: Add new templates without code changes
- **Maintainable**: Clear separation of content and logic
- **Scalable**: Template system grows with business needs
- **Testable**: Validation ensures template quality
- **Flexible**: Support for various conversation patterns

## 📈 Success Metrics

The template system delivers:
- ✅ **3 working templates** with comprehensive coverage
- ✅ **Zero-code template addition** process
- ✅ **Complete conversation state** persistence
- ✅ **Structured JSON export** for business decisions
- ✅ **Visual progress tracking** for user engagement
- ✅ **Template validation** ensuring quality

Your Business Decision Assistant is now a powerful, extensible platform for structured business analysis! 🎉
