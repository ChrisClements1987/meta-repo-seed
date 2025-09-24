# Command Line Interface Reference

Complete reference for all Meta-Repo Seed CLI commands, options, and usage patterns.

## 🚀 Basic Usage

```bash
python seeding.py [OPTIONS] [DIRECTORY]
```

### Arguments

**DIRECTORY** (optional)
- **Description**: Target directory for project creation
- **Default**: Current directory (`.`)
- **Example**: `python seeding.py /path/to/new-project`

## 🔧 Core Options

### Project Configuration

**`--project-name NAME`**
- **Description**: Set the project name
- **Default**: Auto-detected from directory name
- **Example**: `--project-name "my-awesome-project"`

**`--github-username USERNAME`**
- **Description**: GitHub username for templates and repository creation
- **Default**: Auto-detected from git config
- **Example**: `--github-username "john-doe"`

**`--author-name NAME`**
- **Description**: Author name for templates and documentation
- **Default**: Auto-detected from git config
- **Example**: `--author-name "John Doe"`

**`--author-email EMAIL`**
- **Description**: Author email for templates and documentation  
- **Default**: Auto-detected from git config
- **Example**: `--author-email "john@example.com"`

### Output Control

**`--verbose`, `-v`**
- **Description**: Enable verbose output with detailed logging
- **Default**: `false`
- **Example**: `--verbose`

**`--quiet`, `-q`**
- **Description**: Suppress all output except errors
- **Default**: `false`
- **Example**: `--quiet`

**`--dry-run`**
- **Description**: Show what would be done without making changes
- **Default**: `false`
- **Example**: `--dry-run`

### Template Selection

**`--templates TEMPLATE_LIST`**
- **Description**: Comma-separated list of templates to include
- **Default**: All available templates
- **Options**: `gitignore`, `github_workflows`, `governance`, `documentation`, `cloud_storage`, `automation`
- **Example**: `--templates "gitignore,github_workflows,governance"`

**`--exclude-templates TEMPLATE_LIST`**
- **Description**: Comma-separated list of templates to exclude
- **Default**: None
- **Example**: `--exclude-templates "cloud_storage,automation"`

**`--list-templates`**
- **Description**: List all available templates and exit
- **Example**: `--list-templates`

## ⚙️ Configuration Options

### Configuration Files

**`--config CONFIG_FILE`**
- **Description**: Load configuration from YAML or JSON file
- **Format**: Path to `.yml`, `.yaml`, or `.json` file
- **Example**: `--config "./configs/web-app.yml"`

**`--save-config CONFIG_FILE`**
- **Description**: Save current configuration to file after execution
- **Format**: Path to save configuration (`.yml` or `.json`)
- **Example**: `--save-config "./configs/my-project.yml"`

**`--config-format FORMAT`**
- **Description**: Format for saved configuration files
- **Options**: `yaml`, `json`
- **Default**: `yaml`
- **Example**: `--config-format json`

### Variable Overrides

**`--variables VARIABLES`**
- **Description**: Set template variables as key=value pairs
- **Format**: `"KEY1=value1,KEY2=value2"`
- **Example**: `--variables "ORGANIZATION_NAME=My Corp,LICENSE_TYPE=Apache-2.0"`

**`--set VAR=VALUE`**
- **Description**: Set individual template variables (can be used multiple times)
- **Example**: `--set PROJECT_TYPE=webapp --set TECH_STACK=React`

## 🐙 GitHub Integration

### Repository Management

**`--github-integration`**
- **Description**: Enable GitHub integration features
- **Default**: `false`
- **Example**: `--github-integration`

**`--create-repo`**
- **Description**: Create GitHub repository (requires GitHub CLI)
- **Default**: `false`
- **Example**: `--create-repo`

**`--private`**
- **Description**: Create private GitHub repository
- **Default**: `false` (public repository)
- **Example**: `--private`

**`--organization ORG`**
- **Description**: Create repository in specified GitHub organization
- **Example**: `--organization "my-company"`

### Repository Configuration

**`--branch-protection`**
- **Description**: Set up branch protection rules on main branch
- **Default**: `false`
- **Example**: `--branch-protection`

**`--setup-teams`**
- **Description**: Configure repository teams and permissions
- **Default**: `false`
- **Example**: `--setup-teams`

**`--topics TOPICS`**
- **Description**: Comma-separated list of repository topics
- **Example**: `--topics "python,automation,template"`

## 🔍 Information Commands

### Help and Documentation

**`--help`, `-h`**
- **Description**: Show help message and exit
- **Example**: `--help`

**`--version`**
- **Description**: Show version information and exit  
- **Example**: `--version`

### Template Information

**`--list-templates`**
- **Description**: List all available templates with descriptions
- **Example**: `--list-templates`

**`--show-variables`**
- **Description**: Show all available template variables
- **Example**: `--show-variables`

**`--validate-templates`**
- **Description**: Validate all template files for syntax errors
- **Example**: `--validate-templates`

### Configuration Information

**`--show-config`**
- **Description**: Display current configuration (including defaults)
- **Example**: `--show-config`

**`--config-schema`**
- **Description**: Display configuration file schema and validation rules
- **Example**: `--config-schema`

## 📚 Usage Examples

### Basic Project Creation

```bash
# Create project with default settings
python seeding.py

# Create project in specific directory
python seeding.py /path/to/new-project

# Create project with custom name
python seeding.py --project-name "my-web-app"
```

### Configuration-Based Setup

```bash
# Use configuration file
python seeding.py --config "./configs/webapp.yml"

# Load config and override specific values
python seeding.py --config "./configs/base.yml" --project-name "custom-project"

# Save configuration after setup
python seeding.py --project-name "test-project" --save-config "./configs/test.yml"
```

### Template Management

```bash
# Use specific templates only
python seeding.py --templates "gitignore,governance"

# Exclude specific templates
python seeding.py --exclude-templates "cloud_storage"

# List available templates
python seeding.py --list-templates
```

### GitHub Integration

```bash
# Create GitHub repository
python seeding.py --github-integration --create-repo

# Create private repository with branch protection
python seeding.py --github-integration --create-repo --private --branch-protection

# Create organization repository
python seeding.py --github-integration --create-repo --organization "my-org"
```

### Variable Customization

```bash
# Set multiple variables
python seeding.py --variables "COMPANY=ACME Corp,LICENSE=MIT,VERSION=1.0.0"

# Set individual variables
python seeding.py --set COMPANY="ACME Corp" --set LICENSE="Apache-2.0"

# Show available variables
python seeding.py --show-variables
```

### Development and Testing

```bash
# Preview changes without applying
python seeding.py --dry-run --verbose

# Validate templates
python seeding.py --validate-templates

# Show current configuration
python seeding.py --show-config
```

## 🔧 Advanced Usage Patterns

### Environment-Specific Setup

```bash
# Development environment
python seeding.py --config "./configs/base.yml" --set ENVIRONMENT=development --verbose

# Production environment  
python seeding.py --config "./configs/base.yml" --set ENVIRONMENT=production --private
```

### Team Workflows

```bash
# Team lead setup
python seeding.py \
  --config "./team-configs/standard.yml" \
  --github-integration \
  --create-repo \
  --private \
  --branch-protection \
  --setup-teams

# Developer setup (existing repo)
python seeding.py \
  --config "./team-configs/standard.yml" \
  --github-integration \
  --templates "gitignore,governance"
```

### Automated Workflows

```bash
# CI/CD pipeline usage
python seeding.py \
  --config "${CONFIG_PATH}" \
  --project-name "${PROJECT_NAME}" \
  --github-username "${GITHUB_ACTOR}" \
  --quiet \
  --github-integration \
  --create-repo
```

## 🚨 Error Codes

The CLI returns standard exit codes:

- **0**: Success
- **1**: General error (invalid arguments, file errors)
- **2**: Configuration error (invalid config file, missing required values)
- **3**: Template error (template not found, invalid template syntax)
- **4**: GitHub integration error (authentication, API errors)
- **5**: Permission error (insufficient permissions, read-only filesystem)

## 📋 Configuration File Priority

When multiple configuration sources are provided, they are applied in this order (later overrides earlier):

1. **Built-in defaults**
2. **Configuration file** (`--config`)
3. **Environment variables** (if supported)
4. **Command-line arguments** (highest priority)

## 🔍 Debugging and Troubleshooting

### Common Command Combinations

**Debug configuration loading:**
```bash
python seeding.py --config myconfig.yml --show-config --dry-run
```

**Test template processing:**
```bash
python seeding.py --dry-run --verbose --templates "gitignore"
```

**Validate everything before running:**
```bash
python seeding.py --validate-templates --config myconfig.yml --dry-run
```

### Environment Variables

Some CLI options can be set via environment variables:

```bash
export GITHUB_USERNAME="my-username"
export PROJECT_NAME="default-project"
export VERBOSE=true

python seeding.py  # Uses environment variables
```

## 📖 Related Documentation

- [Configuration Guide](../guides/configuration.md) - Detailed configuration file documentation
- [Template System Guide](../guides/templates.md) - Working with templates
- [GitHub Integration Guide](../guides/github-integration.md) - GitHub features and setup
- [API Reference](./api.md) - Python API documentation

---

*For questions or issues with the CLI, please check the [troubleshooting section](../guides/troubleshooting.md) or [open an issue](https://github.com/your-org/meta-repo-seed/issues).*