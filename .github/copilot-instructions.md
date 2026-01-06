# GitHub Copilot Instructions for Peyote

## Project Overview

Peyote is a Python package for creating generative computational art. It provides a Processing-like IDE built with PySide6 that allows users to create visual sketches using Python code. The project aims to make generative art creation accessible and visually appealing.

## Tech Stack

- **Language**: Python 3.11+
- **Package Manager**: [uv](https://docs.astral.sh/uv/) (modern Python package manager)
- **CLI Framework**: [Typer](https://typer.tiangolo.com/) for command-line interface
- **GUI Framework**: PySide6 (Qt for Python)
- **Testing**: pytest with pytest-cov and pytest-qt
- **Linting/Formatting**: Ruff (linter and formatter)
- **Type Checking**: ty (Python type checker)
- **Task Runner**: Poe the Poet (poethepoet)
- **Settings Management**: Pydantic Settings
- **Logging**: Loguru
- **Documentation**: MkDocs with mkdocstrings

## Development Workflow

### Environment Setup
```bash
# Install dependencies (do not activate venv manually)
uv sync

# Run tests
uv run pytest

# Run type checks
uv run ty src/peyote

# Run linting
uv run ruff check src tests

# Format code
uv run ruff format src tests
```

### Task Runner
Use `poe` (Poe the Poet) for common tasks:
- `poe test` - Run tests
- `poe ty` - Type check
- `poe ruff` - Lint and format
- `poe check` - Run all code quality tools
- `poe qc` - Run tests and all quality checks
- `poe coverage` - Generate coverage report

### Project Commands
- Always use `uv run` prefix for Python commands
- Main CLI: `uv run peyote --help`
- Run module: `uv run python -m peyote`

## Code Style and Formatting

### General Principles
- Follow Ruff's comprehensive linting rules (configured in pyproject.toml)
- Use automatic fixing: Ruff is configured with `fix = true`
- The project selects ALL Ruff rules with specific ignores

### Specific Style Rules

**Imports**
- Use isort for import ordering
- Imports are automatically sorted by Ruff

**Docstrings**
- Use multi-line docstrings with summary on first line
- Follow D212 style (multi-line summary first line)
- Not required to end docstrings with periods (D400, D415 ignored)
- Do not use imperative mood requirement (D401 ignored)

**Type Hints**
- Use type hints for function parameters and return values
- Run `ty` type checker before committing

**Code Patterns**
- Boolean type hints in function parameters are allowed (FBT001, FBT003 ignored)
- Bare except clauses are allowed (BLE001 ignored)
- Use f-strings for string formatting

### Legacy Code
- Files in `src/peyote/graphics/*` and `src/peyote/util/*` have ALL linting rules ignored
- These are legacy modules being preserved during modernization

## Testing

### Test Framework
- Use pytest for all tests
- Test files should be in the `tests/` directory
- Name test files with `test_*.py` pattern
- Name test functions with `test_*` pattern

### Test Style
- Tests can use assert statements (S101 ignored for tests)
- Tests can use subprocess without shell checks (S603 ignored)
- Use fixtures defined in `conftest.py`
- Example fixture: `project_version` provides the current version

### Running Tests
```bash
# Run all tests
uv run pytest

# Run tests quietly, stop on first failure
uv run pytest -q -x

# Run with coverage
uv run pytest --cov=./src/peyote --cov-report=html
```

### Qt Testing
- Use pytest-qt for PySide6/Qt widget testing
- Tests requiring Qt should use appropriate pytest-qt fixtures

## Architecture and Structure

### Module Organization
```
src/peyote/
├── __main__.py          # CLI entry point
├── settings.py          # Pydantic settings
├── ide_subcommand.py    # IDE subcommand
├── self_subcommand.py   # Self-management subcommand
├── smoke_subcommand.py  # Smoke test subcommand
└── ide/                 # IDE implementation
    ├── ide_window.py    # Main window
    ├── code_editor.py   # Code editor widget
    ├── display_widget.py # Graphics display
    ├── execution_engine.py # Sketch execution
    ├── tab_manager.py   # Tab management
    ├── syntax_highlighter.py # Python syntax highlighting
    ├── package_manager.py # Package installation
    ├── module_loader.py # Dynamic module loading
    ├── logging_setup.py # Logging configuration
    ├── styles.py        # Qt stylesheets
    └── app_dirs.py      # Application directories
```

### CLI Structure
- Main CLI uses Typer for command organization
- Subcommands are organized as separate Typer apps
- Global callback handles settings and logging setup
- Use `ctx.obj` to pass Settings between commands

### Settings
- Use Pydantic Settings with `BaseSettings`
- Environment variables prefixed with `PEYOTE`
- Support `.env-peyote` file for local configuration
- Example: `debug: bool = False`

### Logging
- Use Loguru for all logging
- Logger is configured in CLI global callback
- Enable/disable debug mode with `--debug` or `-D` flag
- Log file: `peyote.log`

## Security Guidelines

### Secrets Management
- Never commit secrets or credentials to the repository
- Use environment variables or .env files for sensitive data
- Add sensitive files to .gitignore

### Input Validation
- Validate user inputs from CLI arguments
- Sanitize code before execution in the IDE
- Be cautious with dynamic code execution

### Dependencies
- Check dependencies for known vulnerabilities
- Keep dependencies updated via dependabot (configured)
- Only add necessary dependencies

## Internal APIs and Libraries

### Preferred Libraries
- **CLI**: Typer (not argparse or click)
- **Logging**: Loguru (not logging module)
- **Settings**: Pydantic Settings (not configparser)
- **GUI**: PySide6 (not PyQt or Tkinter)
- **Graphics**: NumPy for array operations, Pillow for image handling

### Avoid
- Don't add new dependencies without justification
- Don't use `subprocess.run` without proper security checks
- Don't use global state; prefer dependency injection

## Documentation

### Code Documentation
- Document all public APIs with docstrings
- Include parameters, return values, and raises in docstrings
- Keep docstrings concise but complete

### Project Documentation
- Documentation is in `docs/` directory
- Built with MkDocs
- Deploy with `poe docs-deploy`

### Examples
- Example code should be in `examples/` directory
- Include README files for complex examples

## Version Control and Releases

### Git Workflow
- Follow conventional commits when possible
- Keep commits focused and atomic
- Write descriptive commit messages

### Release Process
- Automated via GitHub Actions (see `.github/workflows/release.yaml`)
- Version bumping with Poe tasks:
  - `poe publish_patch` - Patch version
  - `poe publish_minor` - Minor version
  - `poe publish_major` - Major version
- Pushing a version tag triggers CI/CD pipeline

## CI/CD

### GitHub Actions
- Tests run on multiple Python versions
- Publishes to PyPI on version tags
- Deploys documentation to GitHub Pages
- Dependabot keeps dependencies updated

## Additional Notes

### Python Version
- Requires Python 3.11 or higher
- Project uses modern Python features

### Build System
- Uses uv_build as build backend (not setuptools)
- Configured in pyproject.toml

### IDE Features
- Processing-like API for generative art
- Live code execution and visualization
- Integrated package manager
- Syntax highlighting for Python code

## Quick Reference

When writing code for this project:
1. Use `uv run` for all Python commands
2. Run `poe check` before committing
3. Add type hints to all new functions
4. Write tests for new functionality
5. Follow the existing code structure
6. Use Loguru for logging
7. Use Typer for CLI commands
8. Keep security in mind, especially around code execution
