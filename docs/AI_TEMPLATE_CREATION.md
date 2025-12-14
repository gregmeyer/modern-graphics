# AI-Assisted Template Creation

The `modern_graphics` package includes an AI-powered interview system to help you create custom templates through conversation.

## How It Works

### 1. Prompt Library (`prompts/`)

The prompt library contains:
- **System prompts**: Instructions for the AI assistant
- **User prompts**: Initial questions to start the conversation
- **Generation prompts**: Instructions for creating the final template JSON
- **Parsing utilities**: Extract JSON from AI responses

### 2. Interview Flow

```
User: "I want to create a template"
  ↓
AI: Asks about colors, style, use case, fonts
  ↓
User: Answers questions
  ↓
AI: Asks follow-up questions
  ↓
User: Types "done"
  ↓
AI: Generates template JSON
  ↓
System: Parses JSON → Creates StyleTemplate → Registers it
```

### 3. Two Modes

#### Quick Mode
Generate from a single description:
```python
template = quick_template_from_description(
    "dark professional theme with blue accents"
)
```

#### Interactive Mode
Have a conversation:
```python
template = interview_for_template()
# AI asks questions, you answer, type "done" when ready
```

## Usage Examples

### Python API

```python
from modern_graphics import (
    interview_for_template,
    quick_template_from_description,
    register_template,
    ModernGraphicsGenerator
)

# Quick mode
template = quick_template_from_description(
    "modern, playful theme with bright colors"
)
register_template(template)

# Use it
generator = ModernGraphicsGenerator("My Diagram", template=template)
html = generator.generate_cycle_diagram([...])
```

### CLI

```bash
# Interactive interview
python -m modern_graphics.cli_interview

# Quick generation
python -m modern_graphics.cli_interview \
  --quick "dark professional theme" \
  --register \
  --save my_template.json
```

## Prompt Structure

The AI uses structured prompts to:
1. **Understand** your design preferences
2. **Ask clarifying questions** about colors, style, fonts
3. **Generate** a complete template specification in JSON
4. **Parse** the JSON into a `StyleTemplate` object

## Customization

You can customize the prompts by modifying:
- `prompts/template_prompts.py` - Change interview style, questions, output format
- `template_interview.py` - Adjust conversation flow, add validation

## Requirements

- OpenAI API key in `.env` file
- `openai` package: `pip install openai` or `pip install -e ".[ai]"`
