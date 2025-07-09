# Business Decision Assistant

An AI-powered Streamlit application that guides users through structured business decision-making processes using conversation templates and OpenAI integration.

## Features

### Core Functionality
- **Template-Driven Conversations**: Multiple business frameworks for different scenarios
- **Staged Dialog Process**: Step-by-step guided conversations with examples
- **OpenAI Integration**: Intelligent AI responses and recommendations
- **Progress Tracking**: Visual progress indicators and stage completion tracking
- **JSON Configuration Building**: Automatically builds structured business configs

### Advanced Features
- **Save/Load Sessions**: Export and import conversation progress as JSON
- **Dynamic Template Loading**: File-based template system for easy extensibility
- **Multiple Frameworks**: Business decisions, project planning, market analysis, and more
- **Example-Driven UX**: Curated examples for each conversation stage
- **Context Preservation**: Maintains conversation context across stages

## Available Templates

- **🏢 Business Decision Framework**: Comprehensive analysis for strategic business decisions (7 stages)
- **📋 Project Planning Framework**: Structured approach for project initialization (6 stages)  
- **📊 Market Analysis Framework**: Deep dive into market opportunities and competitive landscape (5 stages)

## Setup

1. Install uv (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone and navigate to the project:
   ```bash
   git clone <your-repo-url>
   cd Chat_assistant
   ```

3. Create and activate a virtual environment with uv:
   ```bash
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   ```

4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your OpenAI API key.

6. Run the application:
   ```bash
   streamlit run src/app.py
   ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)

## Usage

### Getting Started
1. Open the application in your browser (typically http://localhost:8501)
2. Select a business framework template from the sidebar
3. Follow the guided conversation through each stage
4. Use provided examples or enter custom responses
5. Save your progress or export the final JSON configuration

### Template System
- **Auto-Discovery**: Templates are automatically loaded from `docs/templates/`
- **Extensible**: Add new templates by creating markdown files following the standard format
- **Validation**: Built-in template validation ensures consistency
- **Easy Maintenance**: Templates are version-controlled and editable as text files

### Session Management
- **Save Progress**: Download your conversation state as JSON
- **Load Sessions**: Upload previously saved sessions to continue
- **Quick Access**: Recently saved sessions appear in the sidebar for quick loading

## Project Structure

```
Chat_assistant/
├── src/
│   ├── app.py              # Main Streamlit application
│   ├── chat_handler.py     # Conversation flow and session management
│   ├── templates.py        # Template registry and management
│   ├── template_loader.py  # Template parsing and validation
│   └── utils.py            # Utility functions
├── docs/
│   ├── templates/          # Business framework templates (markdown)
│   │   ├── business_decision.md
│   │   ├── project_planning.md
│   │   ├── market_analysis.md
│   │   └── README.md       # Template format documentation
│   └── TEMPLATE_SYSTEM.md  # Template system documentation
├── tests/
│   └── test_chat.py        # Tests
├── validate_templates.py   # Template validation script
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore file
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Adding New Templates

To add a new business framework:

1. Create a new markdown file in `docs/templates/` (e.g., `risk_management.md`)
2. Follow the template format documented in `docs/templates/README.md`
3. Include metadata, stages, examples, and JSON structures
4. Run `python validate_templates.py` to verify the template
5. The template will automatically appear in the application

## Template Format

Each template includes:
- **Metadata**: Name, description, category, version info
- **Stages**: Step-by-step conversation flow
- **Examples**: Curated response options for each stage
- **Follow-up Questions**: AI prompts for deeper exploration
- **JSON Schema**: Structure for the final configuration

See `docs/templates/README.md` for detailed format specifications.

## License

MIT License
