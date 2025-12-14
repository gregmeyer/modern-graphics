# Contributing to Modern Graphics Generator

Thank you for your interest in contributing!

## Development Setup

1. Clone the repository
2. Install in editable mode: `pip install -e .`
3. Install development dependencies: `pip install -e ".[dev]"`
4. Set up `.env` file with `OPENAI_API_KEY` (optional, for AI features)

## Project Structure

```
modern_graphics/
├── modern_graphics/          # Main package
│   ├── diagrams/            # Diagram generators
│   ├── templates/           # Template system
│   ├── base.py              # Base generator class
│   ├── generator.py         # Main API
│   └── export.py            # PNG export
├── examples/                # Example scripts
├── docs/                    # Documentation
└── tests/                   # Tests (if added)
```

## Adding New Diagram Types

1. Create a new file in `modern_graphics/diagrams/`
2. Implement a `generate_[diagram_name]_diagram()` function
3. Add it to `modern_graphics/diagrams/__init__.py`
4. Add method to `ModernGraphicsGenerator` in `generator.py`
5. Update README with documentation

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to public functions
- Keep functions focused and small

## Testing

Run example scripts to verify changes:
```bash
python3 scripts/all_diagram_types.py
```

## Submitting Changes

1. Make your changes
2. Test thoroughly
3. Update documentation if needed
4. Submit a pull request
