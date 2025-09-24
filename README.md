# Meta-Repo Seeding System

An idempotent, cross-platform script for creating standardized project structures with comprehensive governance, automation, and documentation frameworks.

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

4. **Or specify custom parameters**
   ```bash
   python seeding.py --project myproject --username myusername
   ```

### Command Options

| Option | Description |
|--------|-------------|
| `--project PROJECT` | Specify project name (default: auto-detect from directory) |
| `--username USERNAME` | Specify GitHub username (default: from git config) |
| `--dry-run` | Preview changes without making them |
| `--verbose, -v` | Enable detailed logging |
| `--help, -h` | Show help message and examples |

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

- [`TEMPLATES.md`](TEMPLATES.md) - Complete template structure and status
- Generated documentation in your project's `meta-repo/documentation/`
- Governance policies in `meta-repo/governance/policies/`

## 🔧 Development

### Project Structure
```
meta-repo-seed/
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

## 🆘 Support

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the generated documentation in your project

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