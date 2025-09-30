# Contributing Guide

Welcome to the Meta-Repo Seed project! We appreciate your interest in contributing. This guide will help you understand how to contribute effectively to the project.

## 📋 Essential Documentation

Before contributing, please familiarize yourself with our workflow and standards:

**🚨 CRITICAL: Read First**
- **[Creating Issues Guide](./creating-issues.md)** - **MANDATORY TDD requirements** for all code-related issues
- **[Test-Driven Development Guide](../guides/test-driven-development.md)** - **Required reading** for all contributors

**Development Process:**
- **[Issue Management Guide](./issue-management.md)** - Issue types, labels, and backlog management
- **[Workflow Standards](./workflow-standards.md)** - Development process, branches, and releases
- **[GitHub Issue Templates](../../.github/ISSUE_TEMPLATE/)** - Structured templates for creating issues

## 🧪 **Mandatory Test-Driven Development (TDD)**

**EVERY contribution involving code changes MUST follow TDD:**

### **Issue Creation Requirements:**
1. **Include TDD acceptance criteria** - Use issue templates that enforce TDD requirements
2. **Write tests first** - Before any implementation
3. **Document test cycle** - Show test-fail-pass-refactor evidence in PRs
4. **Maintain coverage** - No reduction in test coverage allowed

### **Development Workflow:**
1. **Update develop branch**: `git checkout develop && git pull origin develop`
2. **Create feature branch**: `git checkout -b feature/issue-[number]-description`
3. **Write failing tests FIRST** - Before any implementation code
4. **Implement minimal code** - Make tests pass
5. **Refactor** - Clean up implementation
6. **Update documentation** - Guides, roadmap, changelog, AI context

**📖 Detailed TDD Guide: [Test-Driven Development](../guides/test-driven-development.md)**

---

## 🎯 Ways to Contribute

### 🐛 Bug Reports
- Report bugs through [GitHub Issues](https://github.com/your-org/meta-repo-seed/issues)
- **Use the bug report template** - Includes mandatory TDD acceptance criteria
- Provide detailed reproduction steps
- Include environment information
- **Include TDD fix criteria** - How the bug will be tested and verified

### 💡 Feature Requests
- Suggest new features through [GitHub Issues](https://github.com/your-org/meta-repo-seed/issues)
- **Use the feature request template** - Includes comprehensive TDD requirements
- Explain the use case and benefits
- Provide examples when possible
- **Include test strategy** - How the feature will be tested

### 📝 Documentation
- Improve existing documentation
- Add new guides and examples
- Fix typos and unclear explanations
- Translate documentation (future)

### 🔧 Code Contributions
- Fix bugs and implement features
- Improve performance and code quality
- Add new templates
- Expand test coverage

### 🧪 Testing
- Report test failures
- Add new test cases
- Improve test coverage
- Test on different platforms

## 🚀 Getting Started

### Prerequisites

**Required Tools:**
- Python 3.8 or higher
- Git
- GitHub CLI (for GitHub integration features)
- Text editor or IDE (VS Code recommended)

**Optional Tools:**
- Docker (for containerized testing)
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Fork and Clone**
   ```bash
   # Fork the repository on GitHub
   # Then clone your fork
   git clone https://github.com/your-username/meta-repo-seed.git
   cd meta-repo-seed
   ```

2. **Set Up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements-dev.txt
   ```

3. **Configure Git**
   ```bash
   # Set up upstream remote
   git remote add upstream https://github.com/original-org/meta-repo-seed.git
   
   # Configure your git info
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

4. **Verify Setup**
   ```bash
   # Run tests to ensure everything works
   python -m pytest tests/
   
   # Run the seeding script
   python seeding.py --help
   ```

## 🔄 Development Workflow

### Branch Strategy

We use a feature branch workflow:

- **`main`** - Stable, production-ready code
- **`develop`** - Integration branch for features
- **`feature/issue-{number}-{description}`** - Feature development
- **`bugfix/issue-{number}-{description}`** - Bug fixes
- **`hotfix/{description}`** - Critical production fixes

### Making Changes

1. **Create Feature Branch**
   ```bash
   # Update develop branch
   git checkout develop
   git pull upstream develop
   
   # Create feature branch
   git checkout -b feature/issue-123-add-new-template
   ```

2. **Make Changes**
   ```bash
   # Edit files
   # Add new features or fix bugs
   
   # Test your changes
   python -m pytest tests/
   python seeding.py --dry-run --verbose
   ```

3. **Commit Changes**
   ```bash
   # Add files
   git add .
   
   # Commit with descriptive message
   git commit -m "Add new React Native template
   
   - Add React Native project template
   - Include mobile-specific .gitignore patterns
   - Add Expo and Metro bundler configurations
   - Update template documentation
   
   Closes #123"
   ```

4. **Push and Create Pull Request**
   ```bash
   # Push feature branch
   git push origin feature/issue-123-add-new-template
   
   # Create pull request on GitHub
   # Use the pull request template
   # Link to related issues
   ```

### Code Style Guidelines

#### Python Code Style

We follow PEP 8 with some project-specific conventions:

```python
# Good: Descriptive function names
def create_directory_structure(target_dir: str) -> None:
    """Create the basic directory structure for a project."""
    pass

# Good: Type hints
def process_template(template_path: str, variables: Dict[str, str]) -> str:
    """Process template file with variable substitution."""
    pass

# Good: Docstrings
class Configuration:
    """Manages project configuration settings.
    
    This class handles loading, saving, and merging configuration
    files in YAML or JSON format.
    """
    pass
```

#### Documentation Style

```markdown
# Good: Clear headings and structure
## Feature Overview

Brief description of the feature.

### Usage Example

```bash
python seeding.py --new-feature
```

### Parameters

- `--parameter` - Description of parameter
- `--another-param` - Description with example: `--another-param value`
```

#### Template Style

```yaml
# Good: Template with clear variable names
project:
  name: "{{PROJECT_NAME}}"
  description: "{{PROJECT_DESCRIPTION|default:'A project created with meta-repo-seed'}}"
  
# Good: Organized sections  
github:
  enabled: {{GITHUB_ENABLED|default:true}}
  username: "{{GITHUB_USERNAME}}"
```

### Testing Guidelines

#### Writing Tests

```python
# tests/test_new_feature.py
import pytest
from seeding import RepoSeeder, Configuration

class TestNewFeature:
    """Test cases for the new feature."""
    
    def test_feature_basic_functionality(self):
        """Test basic functionality works correctly."""
        config = Configuration()
        config.set("new_feature.enabled", True)
        
        seeder = RepoSeeder(config=config, dry_run=True)
        result = seeder.new_feature_method()
        
        assert result is True
    
    def test_feature_with_invalid_input(self):
        """Test feature handles invalid input gracefully."""
        config = Configuration()
        config.set("new_feature.enabled", "invalid")
        
        with pytest.raises(ConfigurationError):
            seeder = RepoSeeder(config=config)
            seeder.new_feature_method()
```

#### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_configuration.py

# Run with coverage
python -m pytest --cov=seeding tests/

# Run tests and generate HTML coverage report
python -m pytest --cov=seeding --cov-report=html tests/
```

### Documentation Guidelines

#### Adding New Documentation

1. **Create the file in appropriate directory:**
   - Guides: `docs/guides/`
   - Reference: `docs/reference/`
   - Examples: `docs/examples/`
   - Development: `docs/development/`

2. **Follow the structure:**
   ```markdown
   # Page Title
   
   Brief overview of the topic.
   
   ## 🎯 Section Title
   
   Content with clear headings and examples.
   
   ### Subsection
   
   More detailed information.
   
   ## 📚 Examples
   
   Practical examples and code snippets.
   
   ---
   
   *Related documentation links at the bottom*
   ```

3. **Update navigation:**
   - Add links in `docs/README.md`
   - Update related pages with cross-references
   - Test all internal links

## 📋 Pull Request Guidelines

### Before Submitting

**Checklist:**
- [ ] Code follows project style guidelines
- [ ] Tests pass locally (`python -m pytest`)
- [ ] New features have tests
- [ ] Documentation updated as needed
- [ ] No merge conflicts with develop branch
- [ ] Commit messages are descriptive

### Pull Request Template

```markdown
## Description

Brief description of changes made in this PR.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)  
- [ ] Breaking change (fix or feature that causes existing functionality to not work)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues

- Closes #123
- Related to #456

## Testing

- [ ] Existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] Cross-platform testing (if applicable)

## Documentation

- [ ] Code is commented appropriately
- [ ] Documentation updated
- [ ] Examples provided for new features
- [ ] CHANGELOG.md updated (if applicable)

## Screenshots/Examples

[If applicable, add screenshots or example output]

## Breaking Changes

[Describe any breaking changes and migration steps]

## Additional Notes

[Any additional information for reviewers]
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs tests
   - Code quality checks
   - Security scans
   - Documentation builds

2. **Manual Review**
   - Code review by maintainers
   - Testing by reviewers
   - Documentation review
   - User experience evaluation

3. **Approval and Merge**
   - Required approvals from CODEOWNERS
   - All checks pass
   - Conflicts resolved
   - Squash and merge to develop

## 🏷️ Issue Guidelines

### Bug Reports

Use the bug report template and include:
- **Environment details** (OS, Python version, etc.)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and stack traces
- **Configuration files** (if relevant)

### Feature Requests

Use the feature request template and include:
- **Problem statement** - what problem does this solve?
- **Proposed solution** - what should the feature do?
- **Use cases** - who would use this and how?
- **Examples** - mockups, code examples, etc.
- **Alternatives considered** - other approaches you thought about

### Issue Labels

We use labels to categorize issues:

**Type Labels:**
- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation improvements
- `question` - Questions about usage
- `help wanted` - Community contributions welcome

**Priority Labels:**
- `priority: high` - Critical issues
- `priority: medium` - Important improvements
- `priority: low` - Nice-to-have features

**Status Labels:**
- `status: triage` - Needs initial review
- `status: approved` - Ready for development
- `status: in-progress` - Currently being worked on
- `status: blocked` - Waiting on dependencies

## 🧪 Testing Strategy

### Test Categories

**Unit Tests** (`tests/unit/`)
- Test individual functions and methods
- Mock external dependencies
- Fast execution, no file system changes

**Integration Tests** (`tests/integration/`)
- Test component interactions
- Use temporary directories
- Test GitHub CLI integration

**End-to-End Tests** (`tests/e2e/`)
- Test complete workflows
- Create actual files and directories
- Validate final output

### Test Environment

```bash
# Set up test environment
export TESTING=true
export GITHUB_TOKEN=fake_token_for_testing

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/e2e/
```

### Writing Good Tests

```python
# Good: Descriptive test names
def test_configuration_loads_yaml_file_correctly():
    """Test that YAML configuration files are loaded without errors."""
    pass

def test_template_processing_replaces_all_variables():
    """Test that all template variables are properly replaced."""
    pass

# Good: Clear test structure
def test_feature_with_valid_input():
    # Arrange
    config = create_test_configuration()
    
    # Act
    result = process_feature(config)
    
    # Assert
    assert result.success is True
    assert result.message == "Expected message"
```

## 📊 Performance Guidelines

### Code Performance

- **Avoid unnecessary file operations** - Use dry-run mode for testing
- **Cache template lookups** - Don't re-read templates repeatedly
- **Use generators** for large data processing
- **Profile performance** for complex operations

### Testing Performance

```bash
# Benchmark test execution time
python -m pytest --benchmark-only tests/

# Profile memory usage
python -m pytest --profile tests/
```

## 🔒 Security Guidelines

### Security Practices

- **Never commit secrets** - Use `.gitignore` for sensitive files
- **Validate user input** - Sanitize template variables and file paths
- **Use secure defaults** - Private repositories, secure permissions
- **Audit dependencies** - Regular security updates

### Security Testing

```bash
# Check for security vulnerabilities
python -m safety check

# Scan for secrets in code
python -m detect-secrets scan --all-files
```

## 🚢 Release Process

### Version Management

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Release Workflow

1. **Prepare Release**
   ```bash
   # Create release branch
   git checkout develop
   git pull upstream develop
   git checkout -b release/v1.2.0
   ```

2. **Update Documentation**
   ```bash
   # Update CHANGELOG.md
   # Update version numbers
   # Update documentation
   ```

3. **Create Release**
   ```bash
   # Merge to main
   git checkout main
   git merge release/v1.2.0
   git tag v1.2.0
   git push upstream main --tags
   ```

4. **Post-Release**
   ```bash
   # Merge back to develop
   git checkout develop
   git merge main
   git push upstream develop
   ```

## 🙋 Getting Help

### Community Support

- **GitHub Discussions** - General questions and discussions
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Comprehensive guides and examples

### Maintainer Contact

- **Primary Maintainer**: @maintainer-username
- **Response Time**: Within 1-2 business days
- **Best Contact**: GitHub issues for public discussions

---

## 📜 Code of Conduct

Please note that this project is released with a [Code of Conduct](../policies/code-of-conduct.md). By participating in this project, you agree to abide by its terms.

Thank you for contributing to Meta-Repo Seed! 🎉