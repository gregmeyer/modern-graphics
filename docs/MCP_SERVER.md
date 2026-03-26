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

The `modern-graphics` image sets **`ENTRYPOINT` to the CLI** (`modern-graphics`). The MCP server must run with **`--entrypoint python`** so the module starts correctly—same pattern as `make mcp` in the repo [Makefile](../Makefile).

Example `docker run` argument list for MCP config (adjust the host volume path; build the image first with `make build` or `docker build -t modern-graphics .`):

```json
{
  "mcpServers": {
    "modern-graphics": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--ipc=host",
        "--init",
        "-v",
        "/path/on/host/output:/app/output",
        "-w",
        "/app",
        "--entrypoint",
        "python",
        "modern-graphics",
        "-m",
        "modern_graphics.mcp_server"
      ]
    }
  }
}
```

Mount your project or a writable output directory into `/app/output` (or set `MODERN_GRAPHICS_OUTPUT_DIR` inside the container). If clients pass **absolute host paths** for `output_path`, set **`HOST_WORKSPACE_ROOT`** and **`CONTAINER_WORKSPACE_ROOT`** so the server can map them (see [Environment variables](#environment-variables)).

## Output paths and session defaults

- **`set_output_root`**: Optional per-session default **directory**. When `output_path` is omitted on `generate_graphic` (and for some wireframe saves), files go under this root as `<layout>.<format>` (or wireframe defaults). Call `set_output_root` once after the server starts if you want a stable folder (e.g. your mounted `/app/output`).
- **`output_path`**: When provided, must be a full path to a file (PNG/HTML/SVG as appropriate). Parent directories are created when possible.
- **Host vs container:** If the MCP process runs in Docker and the client sends **host absolute paths** under `HOST_WORKSPACE_ROOT`, they are rewritten under `CONTAINER_WORKSPACE_ROOT` before writing. Configure both env vars to the same workspace mount pair (host path and in-container path).

## Available tools

Tools are defined in `modern_graphics/mcp_server.py`. Grouped by role:

### Layout discovery and generation

| Tool | What it does |
|------|--------------|
| `suggest_layout` | Recommend a layout from a plain-text description |
| `list_layouts` | List all layouts with required args and examples |
| `generate_graphic` | Generate an HTML or PNG graphic for a given `layout` and `args` |
| `preview_layout` | Validate `args` without writing a file |
| `get_layout_help` | Detailed help for one layout |

### Themes

| Tool | What it does |
|------|--------------|
| `list_themes` | List built-in and registered themes (colors, descriptions) |
| `create_theme` | Register a custom theme from a primary color (and optional accent, background, font) |
| `preview_theme` | Render a sample hero PNG for a theme |
| `save_theme` | Persist a custom theme to JSON (default under `examples/schemes/`) |

### Wireframes

| Tool | What it does |
|------|--------------|
| `generate_wireframe` | Build a wireframe SVG from a preset, `scene_spec`, or description |
| `list_wireframe_elements` | List element types and scene presets |
| `register_wireframe_preset` | Register a custom preset for reuse |

### Utilities

| Tool | What it does |
|------|--------------|
| `set_output_root` | Set session default output directory |
| `composite_image` | Overlay a PNG on another (logos, badges) |

### suggest_layout

Input: `{"description": "compare two approaches side by side"}`

Returns the best-matching layout with confidence score, alternatives, and a ready-to-use CLI command.

### generate_graphic

**Parameters:** `layout` (string), `args` (object), optional `output_path`, `format` (`html` | `png`), `theme`, `transparent`.

**Defaults:** If `output_path` is omitted, the file path is `<session_output_root>/<layout>.<format>`, where `session_output_root` comes from `set_output_root` if set, otherwise `MODERN_GRAPHICS_OUTPUT_DIR` (see below).

`theme` is applied to the rendered HTML before export, including for **`hero-triptych`**.

**Example — simple hero:**

```json
{
  "layout": "hero",
  "args": {"headline": "Execution scales. Judgment does not."},
  "format": "png",
  "theme": "corporate"
}
```

**Example — triptych with theme:**

```json
{
  "layout": "hero-triptych",
  "format": "png",
  "theme": "warm",
  "args": {
    "title": "Deck",
    "headline": "Three pillars",
    "subheadline": "Optional supporting line",
    "eyebrow": "Optional eyebrow",
    "columns": [
      {"title": "Column A", "icon": "manual", "items": ["Point one", "Point two"]},
      {"title": "Column B", "icon": "templates", "items": ["Point one", "Point two"]},
      {"title": "Column C", "icon": "generated", "items": ["Point one", "Point two"]}
    ],
    "stats": [
      {"label": "Before", "value": "After"}
    ]
  }
}
```

Returns JSON including `file_path`, `layout`, `format`. For HTML, `html_content` may be included. Responses may also include `gallery_url` (see `MODERN_GRAPHICS_SITE_PORT`).

PNG export requires Playwright/Chromium in the MCP environment. If unavailable, use `"format": "html"` or run the server in Docker (Playwright image).

### list_layouts

Input: `{}`

Returns all layouts with their names, descriptions, required args, and example commands.

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODERN_GRAPHICS_OUTPUT_DIR` | `./output` at process cwd | Base directory for generated files when `set_output_root` was not used and `output_path` is omitted |
| `HOST_WORKSPACE_ROOT` | (unset) | Absolute path on the **host** for the mounted workspace (used with Docker MCP to rewrite client paths) |
| `CONTAINER_WORKSPACE_ROOT` | (unset) | Path **inside the container** that corresponds to the same mount |
| `MODERN_GRAPHICS_SITE_PORT` | `8484` | Port embedded in `gallery_url` hints returned with generation results |

---

## Read Next

- [Create Command Guide](./CREATE_COMMAND.md) -- CLI recipes and flag reference
- [Quick Start Guide](./QUICKSTART.md) -- first successful graphic in minutes
