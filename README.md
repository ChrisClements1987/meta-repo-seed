# Meta-Repo Seeding System

An idempotent, cross-platform script for creating standardized project structures with comprehensive governance, automation, and documentation frameworks.

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
- **Governance Policies**: Contributing guidelines, code of conduct, security policies
- **Process Documentation**: Onboarding, code review, release management
- **Standards**: Coding, documentation, testing, security standards
- **Templates**: PR templates, issue templates, ADR templates
- **Automation**: CI/CD workflows, structure validation, README generation
- **Documentation**: Getting started guides, FAQs, glossaries

## 🚀 Quick Start

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

The project includes comprehensive documentation organized for easy navigation:

### 🚀 Getting Started
- **[Main Documentation](docs/README.md)** - Complete documentation index
- **[Configuration Guide](docs/guides/configuration.md)** - Setup and configuration options
- **[Template System Guide](docs/guides/templates.md)** - Working with templates
- **[Quick Start Examples](docs/examples/configurations.md)** - Ready-to-use configurations

### 📋 Reference
- **[CLI Reference](docs/reference/cli.md)** - Command-line interface documentation
- **[API Reference](docs/reference/api.md)** - Python API documentation
- **[Template Reference](docs/reference/templates.md)** - Available templates
- **[Configuration Schema](docs/reference/config-schema.md)** - Configuration format specification

### 🔧 Development
- **[Contributing Guide](docs/development/contributing.md)** - How to contribute
- **[Workflow Guide](docs/guides/workflow.md)** - Development workflows and processes
- **[Changelog](docs/development/changelog.md)** - Version history
- **[Roadmap](docs/development/roadmap.md)** - Planned features and priorities

## 🔧 Development

### Project Structure
```
meta-repo-seed/
├── scripts/               # Management and utility scripts
│   ├── roadmap_manager.py     # Roadmap and changelog management
│   ├── create_roadmap_issues.py # GitHub issue creation
│   ├── map_issues_to_roadmap.py # Issue-roadmap linking
│   └── README.md              # Scripts documentation
├── templates/             # Template files for project generation
│   ├── governance/        # Governance templates
│   ├── github/workflows/  # GitHub Actions templates  
│   ├── cloud-storage/     # Cloud integration templates
│   └── documentation/     # Documentation templates
├── TEMPLATES.md           # Template documentation
└── seeding.py            # Main seeding script
├── seeding.py              # Main seeding script
├── templates/              # All template files
│   ├── github/             # GitHub workflow templates
│   ├── governance/         # Governance document templates
│   ├── cloud-storage/      # Strategy and architecture templates
│   └── documentation/      # Documentation templates
├── TEMPLATES.md           # Template documentation
└── README.md              # This file
```

### Key Functions
- `RepoSeeder` - Main class managing the seeding process
- `create_file_from_template()` - Template processing with variable replacement
- `ensure_directory_exists()` - Idempotent directory creation
- `copy_template_file()` - Template file copying

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with clear description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏷️ Version

Current Version: **1.0.0**

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 💡 Suggesting Features
1. **Check existing issues** and roadmap first
2. **Create a feature request** using our GitHub issue template
3. **Join the discussion** - we value community input on feature design

### 🐛 Reporting Bugs  
1. **Use our bug report template** for consistent information
2. **Include reproduction steps** and environment details
3. **Check for existing reports** to avoid duplicates

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