# Agent Instructions for Meta-Repo Seeding System

## Commands

### Essential Commands
- **Main Script**: `python seeding.py --dry-run --verbose` (preview), `python seeding.py` (execute)
- **All Tests**: `python -m pytest` (run entire test suite)
- **Coverage**: `python -m pytest --cov=seeding --cov=src --cov-report=term-missing`
- **Specific Test**: `python -m pytest tests/unit/test_filename.py::TestClass::test_method`

### Quality Checks  
- **Linting**: `flake8` (current standard), `python -m pytest --flake8` (if plugin available)
- **Diff Coverage**: `pytest --cov=seeding --cov=src --cov-report=xml && diff-cover coverage.xml` (for PR validation)
- **Type Checking**: `mypy` (planned, not enforced yet)
- **Formatting**: `black` (planned, not enforced yet)

### Git Workflow
- **New Feature**: `git checkout develop && git pull origin develop && git checkout -b feature/issue-X-desc`
- **Create PR**: `gh pr create --base develop` (always target develop, never main)  
- **Branch Cleanup**: Automated via GitHub settings, manual via `./scripts/cleanup-branches.sh`

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
- **Dependencies**: Pinned versions in requirements-*.txt files for reproducible builds and security compliance
