# Business-in-a-Box: Rapid Infrastructure Deployment System

An idempotent, cross-platform system for deploying complete business infrastructure in under 10 minutes. Supports startups, charities, nonprofits, and SMBs with professional-grade templates and automation.

> **📍 [Project North Star](docs/PROJECT_NORTH_STAR.md)** - Our vision and guiding principles for this tool

> **Note**: This repository uses branch protection rules to ensure code quality and proper review processes.

## 🎯 Overview

This seeding system creates a complete organizational structure for managing multiple repositories, projects, and teams. It establishes governance frameworks, automation pipelines, and documentation standards that scale across your entire organization.

## 🏗️ What It Creates

### Project Structure
```
your-project/
├── 📁 cloud-storage/          # Local file storage synced with cloud providers
│   ├── strategy/              # Vision, mission, strategic roadmap
│   ├── architecture/          # Principles, ADRs, patterns, designs
│   ├── workspace/             # Initiatives, meetings, projects, notes
│   └── documentation/         # Published content from meta-repo
│
├── 📦 meta-repo/              # Central GitHub repository for governance
│   ├── .github/workflows/     # CI/CD automation
│   ├── governance/            # Policies, processes, standards, templates
│   ├── automation/scripts/    # Repository management scripts
│   └── documentation/         # Centralized documentation
│
├── 📦 core-services/          # Shared services and platforms
├── 📦 saas-products/          # Individual SaaS products
├── 📦 partner-products/       # Partner collaborations
└── 📦 charity-products/       # Open-source and charitable projects
```

### Generated Content
- **Infrastructure as Code**: Terraform, Kubernetes, Docker configurations for 10-minute deployment
- **Audit Management System**: AI agent coordination and audit-to-implementation tracking for continuous improvement
- **Repository Governance Automation**: GitHub settings, branch protection, and label management as code
- **Code Quality Automation**: Pre-commit hooks, formatting tools, and quality checks for consistent development
- **Governance Policies**: Contributing guidelines, code of conduct, security policies
- **Process Documentation**: Onboarding, code review, release management
- **Standards**: Coding, documentation, testing, security standards
- **Templates**: PR templates, issue templates, ADR templates
- **Automation**: CI/CD workflows, structure validation, README generation
- **Documentation**: Getting started guides, FAQs, glossaries

## 🚀 Quick Start

> **👨‍💻 New Contributor?** **MANDATORY:** Complete [Contributor Onboarding](docs/development/contributor-onboarding.md) before making any contributions!

### Prerequisites
- **Git** (latest version)
- **Python 3.8+**
- **GitHub account** with appropriate access

### Installation & Usage

1. **Clone this repository**
   ```bash
   git clone <repository-url>
   cd meta-repo-seed
   ```

2. **Preview what will be created** (recommended first step)
   ```bash
   python seeding.py --dry-run --verbose
   ```

3. **Create your project structure**
   ```bash
   python seeding.py
   ```

### ⚙️ Configuration File Support

Save and reuse project configurations for consistent setups:

```bash
# Save current settings to a configuration file
python seeding.py --save-config my-project.yaml --project MyProject --username myusername

# Load configuration from file
python seeding.py --config my-project.yaml

# Override specific values from config
python seeding.py --config my-project.yaml --project DifferentName --dry-run

# List available configurations
python seeding.py --list-configs
```

**Supported formats**: YAML (`.yaml`, `.yml`) and JSON (`.json`)
**Examples**: See [`examples/`](examples/) directory for sample configurations and detailed usage guide.

4. **Or specify custom parameters**
   ```bash
   python seeding.py --project myproject --username myusername
   ```

### 🏢 Business Operations Automation (NEW)

Deploy complete self-governing business operations with minimal ongoing management:

```bash
# Deploy business automation for a startup
python -m src.cli.business_commands start-onboarding \
    --profile startup-basic \
    --automation-level standard \
    --org-name my-startup

# Deploy for a charity with transparency requirements
python -m src.cli.business_commands start-onboarding \
    --profile charity-nonprofit \
    --automation-level standard

# Test automation deployment first (recommended)
python -m src.cli.business_commands start-onboarding \
    --profile smb-standard \
    --automation-level conservative \
    --dry-run --verbose
```

**Business Profiles Available:**
- `startup-basic` - Growth-ready infrastructure with investor focus
- `charity-nonprofit` - Transparency-focused with donor privacy protection
- `smb-standard` - Professional operations with business continuity
- `consulting-firm` - Client confidentiality with partner approval workflows

> **📖 Full Documentation:** [Business Operations Automation Guide](docs/business-operations-automation.md)

### Command Options

| Option | Description |
|--------|-------------|
| `--project PROJECT` | Specify project name (default: auto-detect from directory) |
| `--username USERNAME` | Specify GitHub username (default: from GITHUB_USERNAME env var or git config) |
| `--dry-run` | Preview changes without making them |
| `--verbose, -v` | Enable detailed logging |
| `--help, -h` | Show help message and examples |

### Environment Variables

| Variable | Description | Usage |
|----------|-------------|-------|
| `GITHUB_USERNAME` | GitHub username for authentication | CI/CD pipelines, non-interactive environments |

**CI/CD Example:**
```bash
# GitHub Actions
env:
  GITHUB_USERNAME: ${{ github.actor }}

# Shell
export GITHUB_USERNAME=your-username
python seeding.py --dry-run
```

## ✨ Key Features

### 🔄 Idempotent Design
- **Safe to run multiple times** - won't break existing structures
- **Smart detection** - only creates what's missing
- **Cross-platform** - works on Windows, macOS, Linux

### 📝 Template System
- **Professional templates** for all common documents
- **Variable replacement** - automatically customized for your project
- **Easy maintenance** - templates separate from script logic
- **Extensible** - easy to add new templates

### 🏛️ Governance Framework
- **Comprehensive policies** - contributing, security, privacy
- **Standardized processes** - onboarding, code review, releases
- **Quality standards** - coding, documentation, testing
- **Template resources** - consistent issue/PR templates

### 🤖 Built-in Automation
- **GitHub Actions workflows** - CI/CD, structure validation
- **Repository management scripts** - initialization, enforcement
- **Documentation generation** - automatic README creation
- **Structure validation** - ensures compliance

### 🏢 Business Operations Automation ✨ NEW
- **Self-governing repositories** - automated onboarding, compliance, and maintenance
- **Business profile support** - startup, charity, SMB, consulting firm configurations
- **Automated compliance enforcement** - weekly validation with issue creation
- **Self-healing systems** - 6-hour health cycles with auto-remediation
- **Governance integration** - CODEOWNERS, branch protection, PR review automation

### 🔒 Security Features
- **Path traversal protection** - Project names are sanitized to prevent directory traversal attacks
- **Input validation** - All user inputs are validated against safe character sets
- **Safe file operations** - File creation operations include security checks
- **No privilege escalation** - Script runs with user permissions only

> **Security Note**: Project names are restricted to letters, numbers, hyphens, underscores, and periods. Path separators, parent directory references (`..`), and absolute paths are rejected to prevent security vulnerabilities.

## 📋 Template Variables

Templates automatically replace these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{PROJECT_NAME}}` | Project name | `quantum` |
| `{{GITHUB_USERNAME}}` | GitHub username | `johndoe` |
| `{{CURRENT_DATE}}` | Current date | `2025-09-24` |
| `{{DECISION_NUMBER}}` | ADR decision number | `001` |
| `{{STATUS}}` | ADR status | `Proposed` |

## 🎨 Customization

### Adding New Templates
1. Create template file in `templates/` directory
2. Use `{{VARIABLE_NAME}}` for replaceable content
3. Update seeding script to reference new template
4. Add variables to `replacements` dictionary if needed

### Modifying Existing Templates
Templates are stored in `templates/` directory - modify them directly to customize generated content.

## 📚 Documentation

The project includes comprehensive documentation organized in the `docs/` directory for easy navigation:

> **📖 [Complete Documentation Index](docs/README.md)** - All documentation with organized structure

### Quick Links
- **[Contributor Onboarding](docs/development/contributor-onboarding.md)** - **REQUIRED** for all contributors
- **[Contributing Guide](docs/development/contributing.md)** - High-level contribution overview
- **[Documentation Standards](docs/development/documentation-standards.md)** - 3-category documentation system
- **[Conventional Commits](docs/development/conventional-commits.md)** - Commit message standards
- **[Project Vision](docs/PROJECT_NORTH_STAR.md)** - Business-in-a-Box vision and strategy

## 🔧 Development

### Project Structure
```
meta-repo-seed/
├── scripts/               # Management and utility scripts
│   ├── roadmap_manager.py     # Roadmap and changelog management
│   ├── create_roadmap_issues.py # GitHub issue creation
│   ├── map_issues_to_roadmap.py # Issue-roadmap linking
│   └── README.md              # Scripts documentation
├── templates/             # All template files for project generation
│   ├── github/workflows/  # GitHub Actions templates
│   ├── governance/        # Governance document templates
│   ├── cloud-storage/     # Strategy and architecture templates
│   └── documentation/     # Documentation templates
├── TEMPLATES.md           # Template documentation (see docs/30-Product/reference/templates.md)
├── seeding.py            # Main seeding script
└── README.md              # This file
```

### Key Functions
- `RepoSeeder` - Main class managing the seeding process
- `create_file_from_template()` - Template processing with variable replacement
- `ensure_directory_exists()` - Idempotent directory creation
- `copy_template_file()` - Template file copying

## 📋 Pull Request Requirements

**ALL PULL REQUESTS MUST:**

### 🧪 **Test-Driven Development (TDD)**
- ✅ **Tests written FIRST** - Before any implementation code
- ✅ **Evidence provided** - Show test-fail-pass-refactor cycle
- ✅ **Coverage maintained** - No reduction in test coverage
- ✅ **TDD compliance confirmed** - Explicit confirmation in PR

### 📚 **Documentation Updates**
- ✅ **User documentation** - README, guides, examples updated
- ✅ **Developer documentation** - Architecture, APIs, comments added
- ✅ **Project documentation** - Roadmap, changelog, migration guides updated
- ✅ **AI context files** - AGENTS.md and patterns maintained

### 🤖 **AI Context Maintenance**
- ✅ **AGENTS.md updated** - New patterns, workflows, decisions documented
- ✅ **Context preserved** - Ensure AI can understand changes
- ✅ **Integration guidance** - How changes fit with existing context

### 🎯 **Business-in-a-Box Alignment**
- ✅ **Target market served** - Startups, charities, non-profits, SMBs
- ✅ **Professional standards** - Enterprise-grade quality maintained
- ✅ **Self-governing systems** - Automated compliance preserved

### 📝 **Use PR Templates**
Choose appropriate template:
- **Feature PRs**: `.github/PULL_REQUEST_TEMPLATE/feature.md`
- **Bug Fix PRs**: `.github/PULL_REQUEST_TEMPLATE/bugfix.md`
- **Documentation PRs**: `.github/PULL_REQUEST_TEMPLATE/documentation.md`
- **General PRs**: `.github/pull_request_template.md` (default)

**📖 [Complete PR Template Guide](.github/PULL_REQUEST_TEMPLATE/README.md)**

### 🚫 **Merge Blockers**
PRs **CANNOT** be merged without:
1. ✅ TDD evidence (test-first development proof)
2. ✅ Complete documentation updates
3. ✅ AI context maintenance
4. ✅ Template compliance verification
5. ✅ Automated quality checks passing

*These requirements ensure code quality, maintainability, and team collaboration standards.*

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏷️ Version

Current Version: **1.0.0**

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🚨 **CRITICAL: All Code-Related Issues Must Include TDD Requirements**

**Before creating any issue involving code changes:**
1. **Read**: [Creating Issues Guide](docs/development/creating-issues.md)
2. **Use proper templates** - They enforce mandatory TDD acceptance criteria
3. **Include test strategy** - How changes will be tested and verified

### 💡 Suggesting Features
1. **Check existing issues** and roadmap first
2. **Use our feature request template** - Includes mandatory TDD requirements
3. **Join the discussion** - we value community input on feature design
4. **Include test strategy** - How the feature will be tested

### 🐛 Reporting Bugs
1. **Use our bug report template** - Includes mandatory TDD fix criteria
2. **Include reproduction steps** and environment details
3. **Check for existing reports** to avoid duplicates
4. **Include test requirements** - How the fix will be verified

### 🔧 Development Process
1. **Read the [Contributing Guide](docs/development/contributing.md)** for detailed contribution guidelines
2. **Fork and create feature branches** for your changes
3. **Follow our branch protection rules** - PRs required for main branch
4. **Use our roadmap manager**: `python scripts/roadmap_manager.py --help`

### 📋 Feature Management Tools
```bash
# List current roadmap features
python scripts/roadmap_manager.py list

# Add new feature to roadmap
python scripts/roadmap_manager.py add "Feature Name" "Description"

# Mark feature as completed
python scripts/roadmap_manager.py complete "Feature Name" "1.1.0" "Changelog description"

# Generate roadmap report
python scripts/roadmap_manager.py report
```

## 🆘 Support

- **Issues**: Use [GitHub Issues](https://github.com/ChrisClements1987/meta-repo-seed/issues) with our structured templates
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the [comprehensive documentation](docs/README.md)
- **Development**: See [Issue Management](docs/development/issue-management.md) and [Workflow Standards](docs/development/workflow-standards.md)
- **Contributing**: Review the [Contributing Guide](docs/development/contributing.md) for development process

## ⭐ Features Roadmap

- [ ] Additional template categories
- [ ] Integration with external tools (Slack, Teams)
- [ ] Advanced configuration options
- [ ] Multi-language support
- [ ] Cloud provider integrations
- [ ] Team management features

---

**Created with ❤️ for organizations that value structure, governance, and automation.**

*Made by developers, for developers who want to focus on building great products instead of fighting with project setup.*
