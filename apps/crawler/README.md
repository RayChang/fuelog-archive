# Fuelog Crawler

A modern Python data crawler tool built with [typer](https://typer.tiangolo.com/) CLI framework. Features web scraping capabilities with httpx and BeautifulSoup, data validation with Pydantic, and comprehensive development tooling.

## 📁 Project Structure

```
apps/crawler/
├── src/
│   └── fuelog_crawler/     # Main package
│       ├── __init__.py     # Package initialization
│       ├── __main__.py     # Support for python -m execution
│       ├── cli.py          # CLI entry point (Typer app)
│       ├── commands/       # One module per CLI command
│       │   ├── __init__.py         # Registers commands on the app
│       │   ├── config.py           # `fuelog config` sub-commands
│       │   └── get_retail_price.py # `fuelog fetch`
│       ├── config.py       # Persistent configuration with Pydantic
│       ├── exceptions.py   # Custom exception classes
│       └── utils.py        # Date parsing and database config checks
├── tests/
│   ├── __init__.py
│   └── test_basic.py       # Basic tests with improved path handling
├── pyproject.toml          # Project configuration and dependencies
├── package.json            # npm/turbo script configuration
├── uv.lock                 # Dependency lock file
└── README.md               # Project documentation
```

## 🚀 Quick Start

### Install Dependencies

```bash
# Install all dependencies (including dev dependencies)
uv sync

# Install only production dependencies
uv sync --no-dev
```

### Activate the Virtual Environment (Important)

A local virtual environment is created at `.venv/` after `uv sync`.

Two ways to run commands:

1. Activate once, then call the script directly (best for continuous work)
2. Skip activation and prefix each command with `uv run` (best for one‑off calls)

Activate (option 1):

```bash
source .venv/bin/activate  # macOS / Linux
which python               # should point to project/.venv
```

Deactivate later:

```bash
deactivate
```

Skip activating (option 2 – on demand):

```bash
uv run fuelog info
uv run python -m fuelog_crawler info
```

Choose one style; you don't need both at the same time.

### CLI Usage Examples

Activated venv (most convenient during development):

```bash
fuelog info
fuelog info
python -m fuelog_crawler info
```

Without activation (one‑off invocations):

```bash
uv run fuelog info
uv run python -m fuelog_crawler info
```

Helpful introspection:

```bash
fuelog --help
fuelog fetch --help
```

### System Installation

```bash
# Install globally
uv tool install .

# Use the installed command
fuelog info
```

## 🛠️ Development

### Code Quality

```bash
# Lint check
npm run lint

# Auto-fix lint issues
npm run lint:fix

# Type checking
npm run check-types
```

### Testing

```bash
# Run tests
npm run test

# Run failed tests only (useful for TDD)
npm run test:watch
```

### Build

```bash
# Build package
npm run build
```

## 🏗️ Turbo Integration

This project is integrated into the monorepo's turbo workflow:

```bash
# Execute from root directory
pnpm turbo run python:test --filter=crawler
pnpm turbo run python:lint --filter=crawler
pnpm turbo run python:run --filter=crawler
```

## 📦 Tech Stack

### Core Dependencies

- **Python 3.13+** - Runtime environment
- **httpx** - Modern HTTP client for web requests
- **BeautifulSoup4** - HTML/XML parsing
- **Pydantic** - Data validation and configuration management
- **Typer** - CLI framework with type hints

### Development Tools

- **uv** - Fast dependency management and tooling
- **Hatchling** - Modern build backend
- **Ruff** - Fast linting and code formatting
- **MyPy** - Static type checking (with lxml-stubs)
- **pytest** - Testing framework

## 🗑️ Uninstall

```bash
uv tool uninstall fuelog-crawler
```

## 💡 CLI Extension Guide

This tool uses [typer](https://typer.tiangolo.com/) as the CLI framework, making it easy to add new commands:

1. Add a module in `src/fuelog_crawler/commands/` that defines the command function
2. Register it in `register_commands` in `src/fuelog_crawler/commands/__init__.py`

Example:

```python
# src/fuelog_crawler/commands/update_database.py
def update_database(dry_run: bool = False) -> None:
    """Update the fuel price database."""
    print(f"Updating database (dry run: {dry_run})")


# src/fuelog_crawler/commands/__init__.py, inside register_commands
from .update_database import update_database

app.command(name="update")(update_database)
```

## 🔧 Architecture & Development Workflow

### Key Modules

- **`config.py`** - Configuration management using Pydantic models

  ```python
  from fuelog_crawler.config import CrawlerConfig
  config = CrawlerConfig(rate_limit=2.0, timeout=60)
  ```

- **`exceptions.py`** - Custom exception hierarchy
  ```python
  from fuelog_crawler.exceptions import CrawlerError, NetworkError
  ```

### Development Workflow

1. **Add new features**: Create new modules in `src/fuelog_crawler/`
2. **Extend CLI**: Edit `src/fuelog_crawler/cli.py` using typer decorators
3. **Write tests**: Add test files in the `tests/` directory
4. **Update dependencies**: Edit `dependencies` in `pyproject.toml`
5. **Run quality checks**: Use `npm run lint`, `npm run check-types`, and `npm run test`

### Testing Best Practices

- Tests use dynamic path resolution for better portability
- Type checking includes lxml stubs for comprehensive coverage
- Use `npm run test:watch` for TDD workflow (runs only failed tests)

## 📄 License

This project follows the license in the project root directory.
