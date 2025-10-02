# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **CRITICAL: External Audit Analysis & Strategic Transformation** - Comprehensive third-party strategic assessment
  - External audits by Claude AI, Gemini, and GPT-5 assessing Business-in-a-Box positioning
  - Strategic competitive positioning analysis: competing with $200k-1M consulting engagements vs. free dev tools
  - Market opportunity assessment: "Business Infrastructure as Code" category creation for startups/SMBs/non-profits
  - Five-domain architecture framework: Strategy → Enterprise Architecture → Product → Development → Operations
  - Independent strategic assessment and risk analysis with 85% agreement on strategic direction
  - Target audience repositioning: founders/CEOs/entrepreneurs rather than just developers
  - Priority #1 established: World-class README as project manifesto to communicate Business-in-a-Box vision
- **HIGH: Business Operations Automation** - Self-governing organizational infrastructure automation (Priority 2 Complete)
  - KPI tracking and business metrics automation templates
  - Portfolio lifecycle management automation frameworks
  - Self-governing business operations for 10-minute organizational deployment
  - Strategic spike analysis completed for business automation requirements
- **HIGH: Comprehensive Audit Management System** - AI agent coordination and audit-to-implementation tracking
  - Multi-agent audit coordination for security, code quality, architecture, and business domains
  - Central audit registry with lifecycle tracking from findings to implementation
  - Standardized audit templates and automation scripts for consistent reporting
  - GitHub integration for converting audit findings to tracked issues
  - Progress tracking system preventing duplicate work and enabling continuous improvement
- **HIGH: GitHub Repository Settings as Code** - Automated repository governance and security configuration
  - Repository settings automation with branch protection rules and security policies
  - Standardized label system for consistent issue and PR management
  - GitHub Actions workflow for automated settings application
  - Cross-platform automation script using GitHub CLI and API
- **MEDIUM: Pre-commit Hooks & Code Formatting** - Automated code quality and formatting workflow
  - Pre-commit hooks with black, isort, flake8, pydocstyle, and bandit for consistent code quality
  - pyproject.toml configuration with tool settings and project metadata
  - Cross-platform setup script for easy developer environment configuration
  - Requirements file for all formatting and quality dependencies
- **CRITICAL: Infrastructure as Code templates** - Complete infrastructure automation for 10-minute deployment
  - Terraform configurations for AWS, Azure, GCP with production-ready modules
  - Kubernetes manifests with security contexts, resource limits, and monitoring
  - Docker multi-stage builds with development and production configurations
  - Environment-specific configs (dev/staging/production) for scalable deployment
- **TDD Development Process** - Mandatory test-driven development workflow enforcement
  - Enhanced issue templates with explicit TDD acceptance criteria
  - Updated PR templates requiring branch workflow compliance and TDD evidence
  - AGENTS.md documentation of rigorous development process
- **CRITICAL: AI Integration Guidelines** - Comprehensive AI-assisted development framework
  - AI tools as supplementary aids with human oversight requirements
  - Defined AI strengths (code completion, documentation) vs. limitations (business logic)
  - Integration with TDD workflow and security requirements
  - Mandatory human validation for business-critical decisions
- **HIGH: Documentation Reorganization** - Three-category documentation system implementation
  - User Documentation for user-facing changes
  - Developer Documentation for technical changes  
  - Operations Documentation for deployment/config changes
  - Process/Research Documentation for internal work
- Comprehensive audit documentation with 8-domain analysis
- Reusable AI audit prompt template for future quality assessments
- ADR research documentation and implementation guides
- "Everything as Code" audit for tool and generated output
- Backlog management audit and standardization recommendations
- Professional label system with effort estimation and business alignment
- Issue type framework development for strategic project management

### Changed
- **Strategic Transformation**: Repositioned from technical tool to comprehensive business infrastructure platform
- **Target Market Shift**: Primary users now founders/CEOs/entrepreneurs, not just developers
- **Competitive Framework**: Competing with management consulting and fractional CTO services vs. free developer tools
- **Market Category**: Establishing "Business Infrastructure as Code" as new market category
- Updated roadmap to reflect Business-in-a-Box priorities and external audit strategic insights
- Standardized issue labeling with infrastructure, operations, and effort categories
- Aligned backlog with 10-minute deployment and self-governing systems goals
- Documentation standards aligned with three-category system
- AI integration workflow established for human-AI collaboration

### Fixed
- License compliance issues with GPL dependencies (removed pyinstaller, text-unidecode) (#91)
- Integration test failures achieving 100% test success (20/20 passing)
- Dependency security with pinned versions for reproducible builds
- Strategic direction clarity through comprehensive external audit analysis

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
