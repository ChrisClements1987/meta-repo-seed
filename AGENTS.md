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

### Git Workflow - REQUIRED PROCESS
- **Start Any Work**: `git checkout develop && git pull origin develop && git checkout -b feature/issue-X-desc`
- **TDD Mandatory**: Write failing tests FIRST, then implement, then refactor
- **Branch Naming**: `feature/issue-[number]-description` or `bugfix/issue-[number]-description`
- **Create PR**: `gh pr create --base develop` (always target develop, never main)  
- **Branch Cleanup**: Automated via GitHub settings, manual via `./scripts/cleanup-branches.sh`

### Test-Driven Development (TDD) Process - MANDATORY
1. **Update develop branch** - `git checkout develop && git pull origin develop`
2. **Create feature branch** - `git checkout -b feature/issue-X-description`
3. **Write failing tests FIRST** - Document test-fail-pass-refactor cycle in PR
4. **Implement minimum code** - Make tests pass
5. **Refactor** - Clean up implementation
6. **Update documentation** - Follow 3-category documentation standards (see below)
7. **Commit with clear messages** - Focused, logical commits

### Documentation Standards - MANDATORY
**3-Category Documentation System:**

**👤 User Documentation (Required for user-facing changes):**
- User guides and manuals in `docs/guides/user/`
- FAQ updates for common scenarios
- Release notes and changelog entries
- Migration guides for breaking changes

**👨‍💻 Developer Documentation (Required for technical changes):**
- API reference and OpenAPI specifications
- Architecture documentation and ADRs in `docs/architecture/`
- Code comments for complex logic
- README updates for setup changes

**⚙️ Operations Documentation (Required for deployment/config changes):**
- Installation and deployment guides
- Configuration documentation
- Environment variable documentation
- Monitoring and troubleshooting guides

**📋 Process/Research Documentation (Internal work - flexible requirements):**
- Analysis and research documents
- Audit documentation with findings
- Process documentation with examples
- Internal documentation following structure standards

**Documentation Category Assessment:**
- 🚀 User-Facing Changes → Require User + Developer + Operations docs as applicable
- 🛠️ Technical Changes → Require Developer + Operations docs as applicable  
- 📋 Process/Research → Use flexible Process/Research documentation standards
- 🐛 Bug Fixes → Minimal documentation, focus on changelog if user-visible

## Architecture
- **Main Entry**: `seeding.py` - Core seeding script with `RepoSeeder` class for idempotent project structure creation
- **Modules**: `src/structure_parser/` (JSON schema validation), `src/automation/` (automation scripts), `src/meta_repo_seed/` (core package)
- **Templates**: `templates/` directory with Jinja2-style variable replacement ({{PROJECT_NAME}}, {{GITHUB_USERNAME}})
  - `templates/infrastructure/` - Infrastructure as Code templates (Terraform, K8s, Docker)
  - `templates/code-formatting/` - Pre-commit hooks and code quality configurations
  - `templates/github-settings/` - Repository governance automation and GitHub settings
  - `templates/audit-management/` - AI agent coordination and audit tracking system
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
