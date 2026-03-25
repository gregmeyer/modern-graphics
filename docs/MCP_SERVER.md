# MCP Server

Run modern-graphics as an MCP server so AI clients (Claude Code, Claude Desktop, IDE extensions) can suggest layouts and generate graphics through tool calls.

## Use This Doc When

- You want Claude or another AI to generate graphics for you via tool calls.
- You are integrating modern-graphics into an AI-powered workflow.

For direct CLI usage, see [Create Command Guide](./CREATE_COMMAND.md).

## Setup

Install the MCP dependency:

```bash
pip install modern-graphics-generator[mcp]
```

### Claude Code

Add to your project's `.mcp.json`:

```json
{
  "mcpServers": {
    "modern-graphics": {
      "command": "python",
      "args": ["-m", "modern_graphics.mcp_server"],
      "cwd": "/path/to/modern-graphics"
    }
  }
}
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "modern-graphics": {
      "command": "python",
      "args": ["-m", "modern_graphics.mcp_server"]
    }
  }
}
```

### Docker (for PNG without local Playwright)

```json
{
  "mcpServers": {
    "modern-graphics": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i", "--ipc=host",
        "-v", "/tmp/mg-output:/app/output",
        "modern-graphics",
        "python", "-m", "modern_graphics.mcp_server"
      ]
    }
  }
}
```

## Available Tools

| Tool | What it does |
|------|-------------|
| `suggest_layout` | Recommend a layout from a plain-text description |
| `list_layouts` | List all layouts with required args and examples |
| `generate_graphic` | Generate an HTML or PNG graphic |
| `preview_layout` | Validate inputs and preview what would be generated |
| `get_layout_help` | Get detailed help for a specific layout |

### suggest_layout

Input: `{"description": "compare two approaches side by side"}`

Returns the best-matching layout with confidence score, alternatives, and a ready-to-use CLI command.

### generate_graphic

Input:
```json
{
  "layout": "hero",
  "args": {"headline": "Execution scales. Judgment does not."},
  "format": "png",
  "theme": "corporate"
}
```

Returns: `{"file_path": "./output/hero.png", "format": "png"}`.

For HTML format, also returns `html_content` with the raw HTML string.

PNG export requires Playwright/Chromium. If unavailable, use `"format": "html"` or run the MCP server via Docker.

### list_layouts

Input: `{}`

Returns all layouts with their names, descriptions, required args, and example commands.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODERN_GRAPHICS_OUTPUT_DIR` | `./output` | Where generated files are written |

---

## Read Next

- [Create Command Guide](./CREATE_COMMAND.md) -- CLI recipes and flag reference
- [Quick Start Guide](./QUICKSTART.md) -- first successful graphic in minutes
