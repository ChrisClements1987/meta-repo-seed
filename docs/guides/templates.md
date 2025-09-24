# Template System Guide

The Meta-Repo Seed template system provides a powerful, flexible way to generate consistent project structures and content. This guide covers everything you need to know about working with templates.

## 🎯 Overview

Templates are pre-defined files with placeholder variables that get replaced during project creation. They ensure consistency across projects while allowing customization for specific needs.

### Key Features
- **Variable Replacement**: Dynamic content using `{{VARIABLE}}` syntax
- **Hierarchical Structure**: Organized template directories for different project aspects
- **Extensible**: Easy to add custom templates
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📁 Template Directory Structure

```
templates/
├── gitignore.template                                    # .gitignore template
├── github/
│   └── workflows/
│       ├── ci.yml.template                              # CI/CD workflow
│       └── readme-docs.yml.template                    # README generation workflow
├── governance/
│   ├── policies/
│   │   ├── contributing.md.template                     # Contributing guidelines
│   │   ├── code-of-conduct.md.template                 # Code of conduct
│   │   ├── privacy-policy.md.template                  # Privacy policy
│   │   ├── security-policy.md.template                 # Security policy
│   │   ├── license.md.template                         # License
│   │   └── terms-of-service.md.template                # Terms of service
│   ├── processes/
│   │   ├── onboarding.md.template                       # Onboarding process
│   │   ├── offboarding.md.template                     # Offboarding process
│   │   ├── code-review.md.template                     # Code review process
│   │   ├── issue-management.md.template                # Issue management
│   │   ├── release-management.md.template              # Release management
│   │   └── security-management.md.template             # Security management
│   ├── standards/
│   │   ├── coding-standards.md.template                 # Coding standards
│   │   ├── documentation-standards.md.template         # Documentation standards
│   │   ├── testing-standards.md.template               # Testing standards
│   │   ├── security-standards.md.template              # Security standards
│   │   └── access-control-standards.md.template        # Access control standards
│   └── shared-resources/
│       └── templates/
│           ├── pull-request-template.md.template        # PR template
│           ├── issue-template.md.template               # Issue template
│           └── architecture-decision-record-template.md.template # ADR template
├── cloud-storage/
│   ├── strategy/
│   │   ├── vision.md.template                          # Vision document
│   │   ├── mission.md.template                         # Mission statement
│   │   └── strategic-roadmap.md.template               # Strategic roadmap
│   └── architecture/
│       └── principles/
│           └── principles.md.template                   # Architecture principles
├── documentation/
│   ├── guides/
│   │   └── getting-started.md.template                 # Getting started guide
│   └── shared-resources/
│       ├── templates.md.template                        # Templates documentation
│       ├── glossary.md.template                        # Glossary
│       └── faq.md.template                             # FAQ
├── automation/
│   └── scripts/
│       ├── initialise_repo.py.template                  # Initialization script
│       ├── enforce_structure.py.template               # Structure enforcement
│       └── generate_readmes.py.template                # README generation
└── structure/
    ├── structure.json.template                          # Structure definition
    └── meta-repo-schema.json.template                  # Schema definition
```

## 🔧 Built-in Template Variables

### Core Variables
- `{{PROJECT_NAME}}` - The project name (auto-detected or specified)
- `{{GITHUB_USERNAME}}` - The GitHub username (from git config or specified)
- `{{CURRENT_DATE}}` - Current date in YYYY-MM-DD format
- `{{CURRENT_YEAR}}` - Current year (e.g., 2025)

### Decision Record Variables
- `{{DECISION_NUMBER}}` - Decision number for ADRs (e.g., 001)
- `{{DECISION_TITLE}}` - Decision title for ADRs
- `{{STATUS}}` - Status for ADRs (Proposed, Accepted, Deprecated, etc.)
- `{{ALTERNATIVE_NAME}}` - Alternative name for ADRs

### Project-Specific Variables
- `{{PROJECT_DESCRIPTION}}` - Project description
- `{{AUTHOR_NAME}}` - Author name
- `{{AUTHOR_EMAIL}}` - Author email
- `{{LICENSE_TYPE}}` - License type (MIT, Apache, etc.)
- `{{ORGANIZATION_NAME}}` - Organization name

## ✨ Working with Templates

### Using Existing Templates

```bash
# Use all default templates
python seeding.py

# Use specific templates only
python seeding.py --templates gitignore,github_workflows,governance

# Use templates with custom variables
python seeding.py --variables "ORGANIZATION_NAME=My Company,LICENSE_TYPE=Apache-2.0"
```

### Template Selection Categories

**Core Templates**
- `gitignore` - Comprehensive .gitignore files
- `github_workflows` - GitHub Actions CI/CD pipelines
- `governance` - Project governance and policies

**Documentation Templates**
- `documentation` - Getting started guides and documentation structure
- `readme` - Professional README.md files

**Infrastructure Templates**  
- `cloud_storage` - Cloud storage configurations (AWS, Azure, GCP)
- `automation` - Automation scripts and tooling

### Creating Custom Templates

#### 1. Create Template File
```bash
# Create a new template file
mkdir -p templates/custom
touch templates/custom/my-template.md.template
```

#### 2. Add Template Content
```markdown
# {{PROJECT_NAME}} Custom Documentation

Welcome to {{PROJECT_NAME}}! This project was created on {{CURRENT_DATE}} by {{AUTHOR_NAME}}.

## Project Information
- **Organization**: {{ORGANIZATION_NAME}}
- **License**: {{LICENSE_TYPE}}
- **Contact**: {{AUTHOR_EMAIL}}

## Getting Started
[Add your custom content here]
```

#### 3. Register Template (Optional)
Add your template to the seeding script's template registry or use custom template paths in configuration files.

### Advanced Template Features

#### Conditional Content
```markdown
# {{PROJECT_NAME}}

{{#if INCLUDE_CI}}
## CI/CD Pipeline
This project includes automated CI/CD with GitHub Actions.
{{/if}}

{{#if PRIVATE_REPO}}
> **Note**: This is a private repository.
{{/if}}
```

#### Template Inheritance
```yaml
# Base template
base_template: "standard-project.template"

# Custom overrides
overrides:
  PROJECT_TYPE: "Web Application"
  ADDITIONAL_DEPS: "React, TypeScript"
```

#### Multi-File Templates
```
templates/
├── web-app/
│   ├── package.json.template
│   ├── src/
│   │   ├── index.js.template
│   │   └── App.js.template
│   └── public/
│       └── index.html.template
```

## 🎨 Template Best Practices

### Naming Conventions
- Use `.template` extension for template files
- Mirror the final file structure in template directories
- Use descriptive, hierarchical directory names

### Variable Usage
```markdown
<!-- Good: Descriptive variable names -->
{{PROJECT_NAME}}
{{AUTHOR_EMAIL}}
{{DEPLOYMENT_ENVIRONMENT}}

<!-- Avoid: Generic or unclear names -->
{{VAR1}}
{{TEMP}}
{{DATA}}
```

### Documentation
```markdown
<!-- Template: my-template.md.template -->
<!-- Variables: PROJECT_NAME, AUTHOR_NAME, CURRENT_DATE -->
<!-- Description: Creates project overview documentation -->

# {{PROJECT_NAME}}
Created by {{AUTHOR_NAME}} on {{CURRENT_DATE}}
```

### Error Handling
```markdown
<!-- Provide defaults for optional variables -->
{{PROJECT_NAME|default:"Unnamed Project"}}
{{AUTHOR_NAME|default:"Unknown Author"}}

<!-- Include validation hints -->
<!-- Required variables: PROJECT_NAME, GITHUB_USERNAME -->
<!-- Optional variables: ORGANIZATION_NAME, LICENSE_TYPE -->
```

## 🔧 Advanced Configuration

### Custom Template Paths
```yaml
# Configuration file
templates:
  custom_template_paths:
    - "./custom-templates"
    - "../shared-templates"
    - "/path/to/organization-templates"
```

### Template-Specific Variables
```yaml
templates:
  github_workflows:
    variables:
      NODE_VERSION: "18"
      PYTHON_VERSION: "3.9"
  
  documentation:
    variables:
      DOCS_THEME: "mkdocs-material"
      API_DOCS: "true"
```

### Environment-Specific Templates
```yaml
environments:
  development:
    templates:
      - "gitignore"
      - "github_workflows"
      - "documentation"
    variables:
      DEBUG_MODE: "true"
  
  production:
    templates:
      - "gitignore"
      - "github_workflows"
      - "governance"
      - "cloud_storage"
    variables:
      DEBUG_MODE: "false"
      MONITORING: "enabled"
```

## 🐛 Troubleshooting

### Common Issues

**Template not found**
```
Error: Template 'custom-template' not found
```
Solutions:
- Check template path and filename
- Ensure template has `.template` extension
- Verify custom template paths in configuration

**Variable not replaced**
```
Warning: Variable {{UNDEFINED_VAR}} not found in template
```
Solutions:
- Add variable to configuration file
- Provide variable via command line
- Add default value in template: `{{UNDEFINED_VAR|default:"Default Value"}}`

**Invalid template syntax**
```
Error: Invalid template syntax in file 'template.md.template'
```
Solutions:
- Check for malformed `{{}}` brackets
- Validate YAML/JSON in template frontmatter
- Ensure proper escaping of special characters

### Debugging Templates

#### Dry Run Mode
```bash
# Preview template output without creating files
python seeding.py --dry-run --verbose --templates my-template
```

#### Variable Inspection
```bash
# Show all available variables
python seeding.py --show-variables

# Show variables for specific template
python seeding.py --show-variables --templates github_workflows
```

#### Template Validation
```bash
# Validate template syntax
python seeding.py --validate-templates

# Validate specific template
python seeding.py --validate-templates --templates custom-template
```

## 📚 Template Examples

### Simple Configuration Template
```yaml
# templates/config/app.yml.template
app:
  name: "{{PROJECT_NAME}}"
  version: "1.0.0"
  author: "{{AUTHOR_NAME}}"
  environment: "{{ENVIRONMENT|default:'development'}}"

database:
  host: "{{DB_HOST|default:'localhost'}}"
  port: {{DB_PORT|default:5432}}
  name: "{{PROJECT_NAME|lower}}_{{ENVIRONMENT|default:'dev'}}"
```

### GitHub Actions Template
```yaml
# templates/github/workflows/deploy.yml.template
name: Deploy {{PROJECT_NAME}}

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup {{RUNTIME|default:'Node.js'}}
        uses: actions/setup-node@v3
        with:
          node-version: '{{NODE_VERSION|default:'18'}}'
          
      - name: Deploy to {{DEPLOYMENT_TARGET|default:'production'}}
        run: |
          echo "Deploying {{PROJECT_NAME}} to {{DEPLOYMENT_TARGET}}"
```

### Documentation Template
```markdown
<!-- templates/docs/api.md.template -->
# {{PROJECT_NAME}} API Documentation

## Overview
{{PROJECT_DESCRIPTION|default:'API documentation for ' + PROJECT_NAME}}

## Base URL
```
{{API_BASE_URL|default:'https://api.example.com'}}
```

## Authentication
{{#if REQUIRES_AUTH}}
This API requires authentication. Include your API key in the `Authorization` header.
{{else}}
This API does not require authentication.
{{/if}}

## Endpoints

{{#each API_ENDPOINTS}}
### {{method}} {{path}}
{{description}}

{{#if parameters}}
#### Parameters
{{#each parameters}}
- `{{name}}` ({{type}}) - {{description}}
{{/each}}
{{/if}}
{{/each}}
```

## 🚀 Future Enhancements

### Planned Template Features
- **Dynamic Template Discovery**: Automatic template detection and loading
- **Template Marketplace**: Community-contributed template repository
- **Live Preview**: Real-time template preview during editing
- **Template Testing**: Automated template validation and testing
- **Multi-Language Support**: Templates for different programming languages
- **IDE Integration**: Template editing and preview in VS Code

---

*For more information, see the [Configuration Guide](./configuration.md) and [CLI Reference](../reference/cli.md).*