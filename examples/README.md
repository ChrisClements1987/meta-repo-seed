# Configuration File Examples

This directory contains example configuration files for the Meta-Repo Seeding System.

## 📋 Available Examples

### `web-app-project.yaml`
**Purpose**: Configuration for web application projects  
**Format**: YAML  
**Features**:
- Custom decision title for frontend framework choice
- Accepted status for architectural decisions
- Tailored for web development workflows

**Usage**:
```bash
python seeding.py --config examples/web-app-project.yaml
```

### `data-science-project.json`
**Purpose**: Configuration for data science projects  
**Format**: JSON  
**Features**:
- ML framework decision template
- Data science focused project structure
- Proposed status for new decisions

**Usage**:
```bash
python seeding.py --config examples/data-science-project.json
```

## 🛠️ Creating Your Own Configuration

### 1. Save Current Settings
```bash
# Save your current project settings
python seeding.py --save-config my-project.yaml --project MyProject --username myusername

# Or in JSON format
python seeding.py --save-config my-project.json --project MyProject --username myusername
```

### 2. Customize Configuration
Edit the generated file to customize:
- **Project-specific replacements**: Update template variables
- **Decision templates**: Modify decision titles and statuses  
- **Alternative names**: Set context-appropriate alternatives

### 3. Use Configuration
```bash
# Load and use your configuration
python seeding.py --config my-project.yaml

# Override specific values while using config
python seeding.py --config my-project.yaml --project DifferentName --dry-run
```

## 📖 Configuration File Structure

### YAML Format
```yaml
project_name: my-awesome-project
github_username: myusername
created_at: '2025-09-24T18:40:00.000000'
version: 1.1.0
template_path: null  # Optional: custom template directory
replacements:
  PROJECT_NAME: my-awesome-project
  GITHUB_USERNAME: myusername
  CURRENT_DATE: '2025-09-24'
  DECISION_NUMBER: '001'
  DECISION_TITLE: Your Custom Decision Title
  STATUS: Proposed  # or Accepted, Rejected, etc.
  ALTERNATIVE_NAME: Your Alternative Option Name
```

### JSON Format  
```json
{
  "project_name": "my-awesome-project",
  "github_username": "myusername", 
  "created_at": "2025-09-24T18:40:00.000000",
  "version": "1.1.0",
  "template_path": null,
  "replacements": {
    "PROJECT_NAME": "my-awesome-project",
    "GITHUB_USERNAME": "myusername",
    "CURRENT_DATE": "2025-09-24",
    "DECISION_NUMBER": "001", 
    "DECISION_TITLE": "Your Custom Decision Title",
    "STATUS": "Proposed",
    "ALTERNATIVE_NAME": "Your Alternative Option Name"
  }
}
```

## 🎯 Best Practices

### Configuration Management
- **Version Control**: Store configurations in git for team sharing
- **Environment-Specific**: Create separate configs for dev/staging/prod
- **Template Reuse**: Use common configurations as starting points
- **Documentation**: Comment YAML configs for team understanding

### Template Customization
- **Project-Specific Decisions**: Customize DECISION_TITLE for your domain
- **Status Tracking**: Use STATUS to reflect current decision states
- **Meaningful Alternatives**: Set ALTERNATIVE_NAME to relevant options
- **Date Consistency**: Keep CURRENT_DATE updated for document accuracy

### Team Workflows
```bash
# Team lead creates base configuration
python seeding.py --save-config team-template.yaml --project base-project --username team

# Team members customize for their projects  
python seeding.py --config team-template.yaml --project member-project --username member

# Share configurations through git
git add *.yaml *.json
git commit -m "Add project configurations"
```

---

*These examples demonstrate the flexibility of configuration files for different project types and team workflows.*