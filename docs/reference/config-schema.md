# Configuration Schema Reference

Complete reference for Meta-Repo Seed configuration file format and validation rules.

## 📋 Schema Overview

Configuration files use YAML or JSON format with the following top-level sections:

```yaml
project:          # Project metadata and settings
github:           # GitHub integration configuration  
templates:        # Template selection and customization
variables:        # Custom template variables
options:          # Runtime options and behavior
environments:     # Environment-specific overrides (optional)
```

## 🏗️ Project Section

### Basic Project Information

```yaml
project:
  name: string              # Project name (required)
  description: string       # Project description (optional)
  author: string           # Author name (optional)
  type: string             # Project type identifier (optional)
  framework: string        # Framework/technology used (optional)
  version: string          # Project version (optional, default: "1.0.0")
```

#### Field Specifications

**`project.name`** (required)
- **Type**: String
- **Constraints**: 1-100 characters, alphanumeric and hyphens
- **Description**: Name of the project, used for templates and repository creation
- **Example**: `"my-awesome-project"`

**`project.description`** (optional)
- **Type**: String  
- **Constraints**: 0-500 characters
- **Default**: `"A project created with meta-repo-seed"`
- **Description**: Brief project description for README and repository
- **Example**: `"Modern web application with React and TypeScript"`

**`project.author`** (optional)
- **Type**: String
- **Constraints**: 1-100 characters
- **Default**: Auto-detected from git config
- **Description**: Project author name for templates
- **Example**: `"John Doe"`

**`project.type`** (optional)
- **Type**: String
- **Enum**: `web-application`, `api-service`, `library`, `cli-tool`, `data-science`, `mobile-app`, `desktop-app`, `other`
- **Description**: Project type for template selection and customization
- **Example**: `"web-application"`

**`project.framework`** (optional)
- **Type**: String
- **Description**: Primary framework or technology stack
- **Example**: `"react-typescript"`

## 🐙 GitHub Section

### Repository Configuration

```yaml
github:
  enabled: boolean                    # Enable GitHub integration
  username: string                   # GitHub username
  organization: string               # GitHub organization (optional)
  create_repo: boolean              # Create GitHub repository
  private: boolean                  # Make repository private
  branch_protection: boolean        # Enable branch protection
  topics: array<string>            # Repository topics
  
  # Repository settings
  repository:
    description: string             # Repository description
    homepage: string               # Project homepage URL
    has_issues: boolean           # Enable issues
    has_projects: boolean         # Enable projects
    has_wiki: boolean            # Enable wiki
    
  # Branch protection configuration
  branch_protection:
    branch: string                 # Protected branch name
    required_reviews: integer      # Required review count
    dismiss_stale_reviews: boolean # Dismiss stale reviews
    require_code_owner_reviews: boolean # Require code owner reviews
    required_status_checks: array<string> # Required status checks
    restrict_pushes: boolean       # Restrict direct pushes
    allowed_push_users: array<string> # Users allowed to push
    
  # Team management
  teams:
    - name: string                 # Team name
      permission: string           # Permission level
      members: array<string>      # Team members
```

#### GitHub Field Specifications

**`github.enabled`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable GitHub integration features
- **Example**: `true`

**`github.username`** (optional)
- **Type**: String
- **Constraints**: Valid GitHub username
- **Default**: Auto-detected from git config
- **Description**: GitHub username for repository operations
- **Example**: `"john-doe"`

**`github.create_repo`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Automatically create GitHub repository
- **Requires**: GitHub CLI authentication
- **Example**: `true`

**`github.private`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Create private repository (if creating repo)
- **Example**: `true`

**`github.topics`** (optional)
- **Type**: Array of strings
- **Constraints**: Each topic 1-35 characters, lowercase, hyphen-separated
- **Description**: Repository topics for discoverability
- **Example**: `["python", "automation", "template"]`

**`github.branch_protection.required_reviews`** (optional)
- **Type**: Integer
- **Range**: 0-6
- **Default**: `1`
- **Description**: Number of required code reviews
- **Example**: `2`

**`github.teams[].permission`** (required if teams specified)
- **Type**: String
- **Enum**: `pull`, `triage`, `push`, `maintain`, `admin`
- **Description**: Permission level for team members
- **Example**: `"push"`

## 📄 Templates Section

### Template Selection and Configuration

```yaml
templates:
  enabled_templates: array<string>        # Templates to include
  disabled_templates: array<string>      # Templates to exclude
  custom_template_paths: array<string>   # Additional template directories
  
  # Template-specific configuration
  template_config:
    gitignore:
      languages: array<string>          # Programming languages
      frameworks: array<string>        # Frameworks to include
    
    github_workflows:
      ci_enabled: boolean              # Enable CI workflow
      cd_enabled: boolean              # Enable CD workflow
      security_scan: boolean           # Enable security scanning
      
    governance:
      code_of_conduct: boolean         # Include code of conduct
      contributing_guide: boolean      # Include contributing guide
      security_policy: boolean         # Include security policy
```

#### Template Field Specifications

**`templates.enabled_templates`** (optional)
- **Type**: Array of strings
- **Valid Values**: `gitignore`, `github_workflows`, `governance`, `documentation`, `cloud_storage`, `automation`
- **Default**: All available templates
- **Description**: Templates to include in project creation
- **Example**: `["gitignore", "github_workflows", "governance"]`

**`templates.custom_template_paths`** (optional)
- **Type**: Array of strings
- **Constraints**: Valid directory paths
- **Description**: Additional directories to search for templates
- **Example**: `["./custom-templates", "../shared-templates"]`

**`templates.template_config.gitignore.languages`** (optional)
- **Type**: Array of strings
- **Valid Values**: `python`, `javascript`, `java`, `csharp`, `go`, `rust`, etc.
- **Description**: Programming languages to include in .gitignore
- **Example**: `["python", "javascript", "docker"]`

## 🔧 Variables Section

### Custom Template Variables

```yaml
variables:
  # Built-in variables (auto-populated but can be overridden)
  PROJECT_NAME: string              # Project name
  GITHUB_USERNAME: string          # GitHub username  
  CURRENT_DATE: string             # Current date (YYYY-MM-DD)
  CURRENT_YEAR: string             # Current year
  AUTHOR_NAME: string              # Author name
  AUTHOR_EMAIL: string             # Author email
  
  # Custom variables
  ORGANIZATION_NAME: string         # Organization name
  LICENSE_TYPE: string             # License type
  TECH_STACK: string               # Technology stack description
  DEPLOYMENT_TARGET: string        # Deployment target platform
  API_VERSION: string              # API version
  
  # Conditional variables
  INCLUDE_TESTS: boolean           # Include test configuration
  ENABLE_MONITORING: boolean       # Enable monitoring setup
  USE_DOCKER: boolean              # Include Docker configuration
```

#### Variable Types and Constraints

**String Variables**
- **Type**: String
- **Constraints**: No special requirements unless specified
- **Usage**: Direct replacement in templates using `{{VARIABLE_NAME}}`

**Boolean Variables**
- **Type**: Boolean (`true`/`false`)
- **Usage**: Conditional template sections using `{{#if VARIABLE}}`

**Date/Time Variables**
- **Format**: ISO 8601 date format (YYYY-MM-DD)
- **Auto-generated**: `CURRENT_DATE`, `CURRENT_YEAR`
- **Usage**: Timestamps in templates and documentation

## ⚙️ Options Section

### Runtime Behavior Configuration

```yaml
options:
  # Execution options
  dry_run: boolean                 # Preview mode without changes
  verbose: boolean                 # Enable verbose output
  quiet: boolean                  # Suppress non-error output
  
  # File operations
  backup_existing: boolean        # Backup existing files
  overwrite_existing: boolean     # Overwrite existing files
  create_structure: boolean       # Create directory structure
  
  # Git operations  
  setup_git: boolean             # Initialize git repository
  initial_commit: boolean        # Create initial commit
  
  # External integrations
  install_dependencies: boolean  # Install project dependencies
  setup_pre_commit: boolean     # Setup pre-commit hooks
```

#### Options Field Specifications

**`options.dry_run`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Preview changes without creating files
- **CLI Override**: `--dry-run`

**`options.verbose`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable detailed logging output
- **CLI Override**: `--verbose` or `-v`

**`options.backup_existing`** (optional)
- **Type**: Boolean
- **Default**: `false`
- **Description**: Create backups before overwriting existing files
- **Behavior**: Files backed up with `.backup.TIMESTAMP` extension

## 🌍 Environments Section (Advanced)

### Environment-Specific Overrides

```yaml
environments:
  development:
    github:
      private: false
    options:
      verbose: true
      backup_existing: true
    variables:
      ENVIRONMENT: "development"
      DEBUG_MODE: "true"
      
  staging:
    github:
      private: true
    variables:
      ENVIRONMENT: "staging" 
      DEBUG_MODE: "false"
      
  production:
    github:
      private: true
      branch_protection: true
    options:
      verbose: false
    variables:
      ENVIRONMENT: "production"
      DEBUG_MODE: "false"
      MONITORING_ENABLED: "true"
```

#### Environment Usage

```bash
# Use specific environment
python seeding.py --config myconfig.yml --environment production

# Environment overrides base configuration
python seeding.py --config base.yml --environment development
```

## 📐 Schema Validation

### JSON Schema Definition

The configuration schema can be validated against a JSON Schema:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Meta-Repo Seed Configuration",
  "type": "object",
  "properties": {
    "project": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9\\-_]{1,100}$"
        },
        "description": {
          "type": "string",
          "maxLength": 500
        },
        "type": {
          "type": "string",
          "enum": ["web-application", "api-service", "library", "cli-tool", "data-science", "mobile-app", "other"]
        }
      },
      "required": ["name"]
    },
    "github": {
      "type": "object",
      "properties": {
        "enabled": {"type": "boolean"},
        "username": {
          "type": "string",
          "pattern": "^[a-zA-Z0-9\\-]{1,39}$"
        }
      }
    }
  }
}
```

### Validation Commands

```bash
# Validate configuration file
python seeding.py --validate-config ./myconfig.yml

# Show configuration schema
python seeding.py --config-schema

# Validate and show effective configuration
python seeding.py --config ./myconfig.yml --show-config --dry-run
```

## 🔍 Configuration Examples

### Minimal Configuration

```yaml
project:
  name: "simple-project"
```

### Complete Configuration

```yaml
project:
  name: "enterprise-web-app"
  description: "Enterprise web application with full CI/CD"
  author: "Development Team"
  type: "web-application"
  framework: "react-typescript"

github:
  enabled: true
  username: "company-org"
  organization: "enterprise-company"
  create_repo: true
  private: true
  branch_protection: true
  topics: ["react", "typescript", "enterprise"]
  
  repository:
    has_issues: true
    has_projects: true
    has_wiki: false
    
  branch_protection:
    required_reviews: 2
    dismiss_stale_reviews: true
    required_status_checks: ["ci/build", "ci/test"]

templates:
  enabled_templates:
    - "gitignore"
    - "github_workflows"
    - "governance"
    - "documentation"
    - "cloud_storage"
    
  template_config:
    gitignore:
      languages: ["javascript", "typescript", "node"]
    github_workflows:
      ci_enabled: true
      security_scan: true

variables:
  ORGANIZATION_NAME: "Enterprise Company"
  LICENSE_TYPE: "MIT"
  TECH_STACK: "React, TypeScript, Node.js"
  DEPLOYMENT_TARGET: "AWS ECS"
  MONITORING_SERVICE: "DataDog"

options:
  verbose: true
  backup_existing: true
  setup_git: true
  initial_commit: true
```

## ⚠️ Common Validation Errors

### Project Name Validation

```yaml
# ❌ Invalid: Contains spaces
project:
  name: "my project name"

# ✅ Valid: Uses hyphens
project:
  name: "my-project-name"
```

### GitHub Username Validation

```yaml
# ❌ Invalid: Contains underscores
github:
  username: "user_name"

# ✅ Valid: Uses hyphens
github:
  username: "user-name"
```

### Template Names Validation

```yaml
# ❌ Invalid: Unknown template
templates:
  enabled_templates: ["invalid-template"]

# ✅ Valid: Known template names
templates:
  enabled_templates: ["gitignore", "github_workflows"]
```

## 🔧 Advanced Configuration Patterns

### Configuration Inheritance

```yaml
# base-config.yml
project:
  author: "Team Lead"
  type: "web-application"

github:
  enabled: true
  private: true

# Override config
inherit_from: "./base-config.yml"
project:
  name: "specific-project"
variables:
  CUSTOM_VAR: "custom-value"
```

### Variable Interpolation

```yaml
project:
  name: "{{ENVIRONMENT}}-{{PROJECT_TYPE}}-service"

variables:
  ENVIRONMENT: "production"
  PROJECT_TYPE: "api"
  FULL_NAME: "{{project.name}} ({{ENVIRONMENT}})"
  BUILD_TAG: "{{PROJECT_TYPE}}-{{CURRENT_DATE}}"
```

### Conditional Configuration

```yaml
variables:
  ENABLE_FEATURES: true
  FEATURE_FLAGS: "{{#if ENABLE_FEATURES}}advanced-features{{else}}basic-features{{/if}}"
```

---

*For practical configuration examples, see [Configuration Examples](../examples/configurations.md). For CLI usage, see [CLI Reference](./cli.md).*