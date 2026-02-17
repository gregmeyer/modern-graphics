# Troubleshooting

Common issues and solutions.

## Installation Issues

### Playwright browser not found

```bash
playwright install chromium
```

### Python version error

- Ensure Python 3.8+ is installed: `python3 --version`

## PNG Export Issues

### "playwright not found" error

```bash
pip install playwright
playwright install chromium
```

### Low quality exports

- Increase `device_scale_factor` (default: 2, try 3 or 4)
- Increase `viewport_width` and `viewport_height`

### Cropping issues

- Adjust `padding` parameter if content is cut off: `export_to_png(html, path, padding=40)`

## AI Features Issues

### "OPENAI_API_KEY not found" error

- **You only see this if using prompt-based features** (optional)
- **Solution 1**: Use structured data instead (no OpenAI needed)
  ```python
  # Instead of: generate_cycle_diagram_from_prompt(generator, prompt="...")
  # Use: generator.generate_cycle_diagram([{'text': 'Step 1', 'color': 'blue'}])
  ```
- **Solution 2**: If you want prompt-based generation:
  - Ensure `.env` file exists with `OPENAI_API_KEY=your_key`
  - Or set environment variable: `export OPENAI_API_KEY=your_key`
  - Verify API key is valid and has credits
  - Check OpenAI model availability

### Template generation fails

- Only affects AI-assisted template creation (optional)
- Use existing templates or create templates manually (no OpenAI needed)
- If using AI template creation, verify API key is valid and has credits

## Common Errors

### Import errors

Make sure you're importing from the correct module:

```python
# Correct
from modern_graphics import ModernGraphicsGenerator, Attribution

# Incorrect
from modern_graphics.generator import ModernGraphicsGenerator  # Don't do this
```

### Path errors

Use `Path` objects for file paths:

```python
from pathlib import Path

# Correct
generator.export_to_png(html, Path('output.png'))

# Also works
generator.export_to_png(html, 'output.png')
```

### SVG.js not rendering

Ensure `use_svg_js=True` when creating the generator:

```python
generator = ModernGraphicsGenerator("My Diagram", Attribution(), use_svg_js=True)
```

## Getting Help

- Check [Examples Directory](../examples/) for working examples
- Review [API Reference](API.md) for method signatures
- See [Advanced Topics](ADVANCED.md) for complex use cases
- Check existing [Issues](https://github.com/gregmeyer/modern-graphics/issues) (if applicable)
