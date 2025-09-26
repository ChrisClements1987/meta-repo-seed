# Agent Instructions for Meta-Repo Seeding System

## Commands
- **Test**: `python -m pytest` (all tests), `python -m pytest tests/unit/test_filename.py::TestClass::test_method` (single test)
- **Coverage**: `python -m pytest --cov=seeding --cov=src --cov-report=term-missing`
- **Diff Coverage**: `pytest --cov=seeding --cov=src --cov-report=xml && diff-cover coverage.xml` (for PR validation)
- **Main Script**: `python seeding.py --dry-run --verbose` (preview), `python seeding.py` (execute)
- **Linting**: `flake8` (current) or `ruff check` (planned future), `python -m pytest --flake8` (if plugin available)
- **Type Checking**: `mypy` (planned, not currently enforced)
- **Formatting**: `black` (planned, not currently enforced)

## Architecture
- **Main Entry**: `seeding.py` - Core seeding script with `RepoSeeder` class for idempotent project structure creation
- **Modules**: `src/structure_parser/` (JSON schema validation), `src/automation/` (automation scripts), `src/meta_repo_seed/` (core package)
- **Templates**: `templates/` directory with Jinja2-style variable replacement ({{PROJECT_NAME}}, {{GITHUB_USERNAME}})
- **Config**: Supports YAML/JSON config files for reusable project configurations
- **Testing**: pytest with coverage, markers for unit/integration/github/slow/network tests

## Code Style
- **Python**: PEP 8 style, type hints required (typing module imports), comprehensive docstrings
- **Error Handling**: Use specific exceptions, input validation/sanitization for security (path traversal protection)
- **Imports**: Standard library first, third-party second, local imports last
- **Logging**: Use `logging` module with proper levels, structured error messages
- **Security**: Sanitize all user inputs, validate project names with regex, prevent path traversal attacks
- **Functions**: Pure functions preferred, idempotent operations, clear separation of concerns

## Development Notes  
- Project uses branch protection (develop→main workflow), idempotent design allows safe re-runs
- Test markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.github`, `@pytest.mark.slow`, `@pytest.mark.network`
- **PR Standards**: Use diff coverage (>=80% on changed lines), conditional documentation updates, legacy debt tracking
- **Quality Gates**: Tests must pass OR be marked xfail/skip with linked issues during stabilization phase
- **CLI Contract**: Defined in `docs/architecture/cli.md` - use `--project`, `--username`, `--dry-run`, `--verbose`
