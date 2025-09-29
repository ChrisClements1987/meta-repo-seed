# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CRITICAL: Infrastructure as Code templates** - Complete infrastructure automation for 10-minute deployment
  - Terraform configurations for AWS, Azure, GCP with production-ready modules
  - Kubernetes manifests with security contexts, resource limits, and monitoring
  - Docker multi-stage builds with development and production configurations
  - Environment-specific configs (dev/staging/production) for scalable deployment
- **TDD Development Process** - Mandatory test-driven development workflow enforcement
  - Enhanced issue templates with explicit TDD acceptance criteria
  - Updated PR templates requiring branch workflow compliance and TDD evidence
  - AGENTS.md documentation of rigorous development process
- Comprehensive audit documentation with 8-domain analysis
- Reusable AI audit prompt template for future quality assessments
- ADR research documentation and implementation guides
- "Everything as Code" audit for tool and generated output
- Backlog management audit and standardization recommendations
- Professional label system with effort estimation and business alignment
- 10 new GitHub issues from comprehensive audit findings

### Changed
- Updated roadmap to reflect Business-in-a-Box priorities and audit findings
- Standardized issue labeling with infrastructure, operations, and effort categories
- Aligned backlog with 10-minute deployment and self-governing systems goals

### Fixed
- License compliance issues with GPL dependencies (removed pyinstaller, text-unidecode)
- Integration test failures achieving 100% test success (20/20 passing)
- Dependency security with pinned versions for reproducible builds

## [1.1.0] - 2025-09-26

### Added
- Realistic PR template system with conditional requirements
- Legacy debt management for incremental compliance
- Specialized PR templates for features, bug fixes, and documentation
- Developer Onboarding Guide with 5-minute setup process
- Branch cleanup automation script
- Comprehensive documentation organization in docs/ directory
- CLI contract specification and architecture documentation

### Changed
- Updated PR templates to use diff coverage instead of global coverage requirements
- Made documentation and AI context updates conditional based on change type
- Aligned code quality checks with current tooling (flake8 vs ruff)
- Moved all documentation to organized docs/ structure
- Streamlined main README with proper documentation references
- Organized AGENTS.md commands by category for better AI assistance

### Fixed
- PR template compliance gaps that blocked development on legacy codebase
- Documentation scattered across repository root
- Missing developer onboarding process

### Moved
- PROJECT_NORTH_STAR.md → docs/PROJECT_NORTH_STAR.md
- DEVELOPMENT_WORKFLOW.md → docs/development/DEVELOPMENT_WORKFLOW.md  
- Various development docs to docs/development/ directory

## [1.0.0] - 2025-09-26

### Added
- Initial meta-repo seeding system
- Business-in-a-Box organizational infrastructure deployment
- Comprehensive PR template system
- 10-minute product launch pipeline
- Complete governance framework
- AI context maintenance system

### Features
- Idempotent project structure creation
- Cross-platform support (Windows, macOS, Linux)
- Template variable replacement system
- Configuration file support (YAML/JSON)
- GitHub Actions automation
- Security-hardened file operations
- Branch protection workflows

### Documentation
- Comprehensive user guides
- Architecture decision records
- Developer onboarding documentation
- AI context maintenance (AGENTS.md)
- Template system documentation
