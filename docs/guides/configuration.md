# Configuration System Guide

The Meta-Repo Seed configuration system allows you to save, load, and reuse project settings across multiple repositories. This guide covers everything you need to know about working with configuration files.

## 🎯 Overview

The configuration system supports two formats:
- **YAML** (`.yml` or `.yaml`) - Human-readable, great for version control
- **JSON** (`.json`) - Structured data format, good for programmatic use

Configuration files can store all project settings including templates, variables, and GitHub integration options.

## 📁 Configuration File Structure

### Basic Structure
```yaml
# Project metadata
project:
  name: "my-awesome-project"
  description: "An awesome project created with meta-repo-seed"
  author: "Your Name"

# GitHub integration
github:
  enabled: true
  username: "your-github-username"
  create_repo: true
  private: false

# Template settings
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
  
# Custom variables
variables:
  ORGANIZATION_NAME: "My Organization"
  CONTACT_EMAIL: "contact@example.com"
  LICENSE_TYPE: "MIT"

# Seeding options
options:
  dry_run: false
  verbose: true
  backup_existing: true
```

### Advanced Configuration
```yaml
project:
  name: "enterprise-web-app"
  type: "web-application"
  framework: "react-typescript"
  
github:
  enabled: true
  username: "enterprise-org"
  organization: "enterprise-org"
  create_repo: true
  private: true
  branch_protection: true
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows" 
    - "governance"
    - "documentation"
    - "cloud_storage"
  custom_template_paths:
    - "./custom-templates"
    - "../shared-templates"
    
variables:
  PROJECT_TYPE: "Enterprise Web Application"
  TECH_STACK: "React, TypeScript, Node.js"
  DEPLOYMENT_TARGET: "AWS ECS"
  MONITORING_SERVICE: "DataDog"
  
options:
  dry_run: false
  verbose: true
  create_structure: true
  setup_git: true
  install_dependencies: false
```

## 💾 Saving Configurations

### Automatic Save
When you run the seeding script, you can automatically save the configuration:

```bash
# Save configuration after seeding
python seeding.py --save-config ./configs/my-project.yml

# Save configuration without running seeding (dry-run)
python seeding.py --dry-run --save-config ./configs/template.yml
```

### Manual Creation
Create configuration files manually using your preferred text editor:

```bash
# Create a new configuration directory
mkdir configs

# Create a YAML configuration
touch configs/web-app-template.yml
```

## 📂 Loading Configurations

### Command Line Usage
```bash
# Load configuration from file
python seeding.py --config ./configs/my-project.yml

# Load configuration and override specific values
python seeding.py --config ./configs/base.yml --project-name "custom-name"

# Load configuration and modify GitHub settings
python seeding.py --config ./configs/base.yml --github-username "different-user"
```

### Configuration Priority
When loading configurations, settings are applied in this order (later overrides earlier):

1. **Default values** (built into the script)
2. **Configuration file** (loaded with `--config`)
3. **Command line arguments** (highest priority)

```bash
# Example: Config file sets verbose=false, but command line overrides it
python seeding.py --config quiet-config.yml --verbose
```

## 🏗️ Pre-built Configuration Templates

### Web Application Template
```yaml
# configs/web-app-template.yml
project:
  type: "web-application"
  
github:
  enabled: true
  create_repo: true
  private: false
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance" 
    - "documentation"
    
variables:
  PROJECT_TYPE: "Web Application"
  TECH_STACK: "Modern Web Technologies"
```

### Data Science Template  
```yaml
# configs/data-science-template.yml
project:
  type: "data-science"
  
github:
  enabled: true
  create_repo: true
  private: false
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  PROJECT_TYPE: "Data Science Project"
  TECH_STACK: "Python, Jupyter, Pandas"
  DATA_SOURCE: "To be determined"
```

### Enterprise Template
```yaml
# configs/enterprise-template.yml
project:
  type: "enterprise-application"
  
github:
  enabled: true
  create_repo: true
  private: true
  branch_protection: true
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
variables:
  PROJECT_TYPE: "Enterprise Application"
  COMPLIANCE_LEVEL: "SOC2 Type II"
  SECURITY_TIER: "High"
```

## 🔧 Advanced Features

### Environment-Specific Configurations
```yaml
# Base configuration
project:
  name: "my-project"

# Development environment overrides  
development:
  github:
    private: false
  options:
    verbose: true

# Production environment overrides
production:
  github:
    private: true
    branch_protection: true
  options:
    verbose: false
    backup_existing: true
```

### Template Inheritance
```yaml
# Inherit from another configuration
inherit_from: "./configs/base-template.yml"

# Override specific settings
project:
  name: "specialized-project"
  
variables:
  SPECIALIZED_FEATURE: "enabled"
```

### Variable Substitution
```yaml
project:
  name: "{{ENVIRONMENT}}-{{PROJECT_TYPE}}-app"
  
variables:
  ENVIRONMENT: "production"
  PROJECT_TYPE: "web"
  FULL_NAME: "{{project.name}} ({{ENVIRONMENT}})"
```

## 📋 Configuration Schema Reference

### Project Section
- `name` (string): Project name
- `description` (string): Project description  
- `author` (string): Project author
- `type` (string): Project type identifier
- `framework` (string): Framework being used

### GitHub Section
- `enabled` (boolean): Enable GitHub integration
- `username` (string): GitHub username
- `organization` (string): GitHub organization
- `create_repo` (boolean): Create GitHub repository
- `private` (boolean): Make repository private
- `branch_protection` (boolean): Enable branch protection

### Templates Section
- `enabled_templates` (array): List of template names to include
- `custom_template_paths` (array): Additional template search paths
- `template_variables` (object): Template-specific variables

### Variables Section
- Any key-value pairs for template variable replacement
- Supports string interpolation with `{{variable}}` syntax

### Options Section
- `dry_run` (boolean): Run without making changes
- `verbose` (boolean): Enable verbose output
- `backup_existing` (boolean): Backup existing files
- `create_structure` (boolean): Create directory structure
- `setup_git` (boolean): Initialize git repository

## 🔍 Troubleshooting

### Common Issues

**Configuration file not found**
```bash
Error: Configuration file './configs/missing.yml' not found
```
Solution: Check the file path and ensure the file exists.

**Invalid YAML syntax**
```bash
Error: Invalid YAML syntax in configuration file
```
Solution: Validate your YAML using an online validator or text editor with YAML support.

**Missing required variables**
```bash
Warning: Template variable {{PROJECT_NAME}} not found
```
Solution: Add the missing variable to your configuration's `variables` section.

### Validation Commands

```bash
# Validate configuration without running seeding
python seeding.py --config ./configs/test.yml --dry-run --verbose

# Test configuration loading
python -c "from seeding import Configuration; c = Configuration(); c.load_config('./configs/test.yml'); print('Valid!')"
```

## 📚 Examples and Use Cases

### Team Development
Create shared configuration files for consistent project setup across team members:

```yaml
# team-config.yml
project:
  organization: "our-team"
  
github:
  username: "team-lead"
  organization: "our-company"
  private: true
  
templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    
variables:
  TEAM_NAME: "Development Team"
  CODE_REVIEW_REQUIRED: "true"
  SECURITY_SCANNING: "enabled"
```

### Multi-Environment Setup
```bash
# Development
python seeding.py --config base.yml --config dev-overrides.yml

# Staging  
python seeding.py --config base.yml --config staging-overrides.yml

# Production
python seeding.py --config base.yml --config prod-overrides.yml
```

### CI/CD Integration
```yaml
# .github/workflows/create-project.yml
name: Create New Project
on:
  workflow_dispatch:
    inputs:
      project_name:
        description: 'Project name'
        required: true
      config_template:
        description: 'Configuration template'
        required: true
        default: 'web-app-template.yml'
        
jobs:
  create:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8'
      - name: Create project
        run: |
          python seeding.py \
            --config ./configs/${{ github.event.inputs.config_template }} \
            --project-name "${{ github.event.inputs.project_name }}"
```

---

*For more information, see the [CLI Reference](../reference/cli.md) and [API Reference](../reference/api.md).*