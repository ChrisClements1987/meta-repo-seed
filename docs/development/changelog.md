# Changelog

All notable changes to the Meta-Repo Seeding System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CI/CD status badges and test coverage badges to README for better project visibility
- Project status section with build and coverage information  
- Symlink write protection for template processing (PR #46 - In Review)

## [2.1.0] - 2025-09-24

### Added
- **Configuration File Support** (#5) - YAML/JSON configuration files for project templates
  - Save and load project configurations with `--config` and `--save-config` flags
  - Example configurations for web apps and data science projects
  - Comprehensive documentation with CI/CD integration examples
- **Structure Parser Module** (#31) - Complete parsing foundation for automation scripts
  - Schema validation using structure-v2.json
  - Type-safe dataclasses and models
  - Comprehensive test suite with 95%+ coverage
  - Ready for automation script integration
- **Repository Initialization Automation** (#32) - Automated project setup scripts
  - CLI interface for structure-based repository creation
  - Integration with StructureParser module
  - Cross-platform compatibility
- **Enhanced Documentation System** (#15, #26) - Structured documentation with guides
  - Comprehensive docs/ directory structure
  - Development workflow standards
  - Issue management templates
  - Architecture decision records

### Security
- **Path Traversal Protection** (#35) - Comprehensive input sanitization
  - Project name validation against directory traversal attacks
  - Path separator and absolute path blocking
  - Safe character set restrictions
  - Clear security error messages
- **Non-Interactive Environment Support** (#36) - CI/CD compatibility improvements
  - `GITHUB_USERNAME` environment variable support
  - TTY detection to prevent hanging in automated environments
  - Priority-based username resolution chain
  - GitHub-specific git config preference

### Infrastructure
- **Test Suite Foundation** (#18) - Comprehensive testing framework
  - Unit tests with fixtures and mocking
  - Integration test coverage
  - Cross-platform test compatibility
  - Test configuration with pytest.ini

### Documentation
- **API Reference Documentation** - Complete API and CLI documentation
- **Configuration Schema** - Detailed configuration format specification
- **Template System Guide** - Working with templates and customization
- **CI/CD Integration Examples** - GitHub Actions, GitLab CI, Jenkins examples

## [1.1.0] - 2025-09-24

### Added
- Feature tracking system with CHANGELOG.md and ROADMAP.md

## [1.0.0] - 2025-09-24

### Added
- Initial release of Meta-Repo Seeding System
- Core `seeding.py` script with idempotent project structure creation
- Cross-platform support using pathlib
- Command-line interface with argparse (dry-run and verbose modes)
- Template-based content generation system
- Variable replacement system with {{PROJECT_NAME}}, {{GITHUB_USERNAME}}, {{CURRENT_DATE}} placeholders
- Comprehensive template collection:
  - Governance templates (CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md)
  - GitHub workflow templates (CI/CD, dependency updates, security scanning)
  - Documentation templates (README.md, API documentation)
  - Configuration templates (.gitignore, .editorconfig, pyproject.toml)
  - Cloud storage templates (AWS S3, Azure Blob, GCS configurations)
- MIT License
- Professional README.md with usage examples
- TEMPLATES.md documentation for all available templates
- Repository governance setup:
  - Branch protection rules for main branch
  - CODEOWNERS file for code review enforcement
  - Pull request workflow requirements
  - Administrator bypass capabilities

### Technical Features
- Python 3.8+ compatibility
- Logging system with configurable verbosity
- Error handling and validation
- Cross-platform file path handling
- Template directory organization
- Git integration and workflow setup

### Infrastructure
- GitHub repository with public visibility
- GitHub Actions integration ready
- Branch protection and security rules
- Code review enforcement
- Professional development workflow

---

## Release Tags

- `v1.0.0` - Initial stable release with core functionality and governance framework