# GitHub Integration Guide

The Meta-Repo Seed system provides seamless integration with GitHub to automate repository creation, setup branch protection, and configure essential GitHub features. This guide covers all aspects of GitHub integration.

## 🎯 Overview

GitHub integration enables:
- **Automated Repository Creation**: Create repositories directly from the seeding script
- **Branch Protection**: Set up branch protection rules automatically
- **Issue Templates**: Include comprehensive issue and PR templates
- **GitHub Actions**: Pre-configured CI/CD workflows
- **Team Management**: Configure repository settings for team collaboration

## 🚀 Quick Start

### Prerequisites
1. **GitHub CLI**: Install and authenticate with GitHub CLI
2. **Git Configuration**: Ensure git is configured with your GitHub credentials
3. **Repository Access**: Appropriate permissions for repository creation

### Basic GitHub Integration

```bash
# Create repository and seed with GitHub integration
python seeding.py --github-integration

# Create private repository
python seeding.py --github-integration --private

# Create repository in organization
python seeding.py --github-integration --organization "my-org"
```

## ⚙️ Configuration Options

### Command Line Options

```bash
# Basic GitHub options
python seeding.py \
  --github-integration \
  --github-username "your-username" \
  --private \
  --create-repo

# Advanced GitHub options  
python seeding.py \
  --github-integration \
  --github-username "your-username" \
  --organization "your-org" \
  --private \
  --branch-protection \
  --create-repo \
  --setup-teams
```

### Configuration File Integration

```yaml
# github-config.yml
github:
  enabled: true
  username: "your-github-username"
  organization: "your-organization"  # Optional
  create_repo: true
  private: false
  branch_protection: true
  
  # Repository settings
  repository:
    description: "Project created with meta-repo-seed"
    homepage: "https://your-project-site.com"
    topics: ["meta-repo", "automation", "github"]
    has_issues: true
    has_projects: true
    has_wiki: false
    
  # Branch protection settings
  branch_protection:
    branch: "main"
    required_reviews: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
    required_status_checks:
      - "ci/build"
      - "ci/test"
    restrict_pushes: true
    allowed_push_users: ["admin-user"]
    
  # Team management
  teams:
    - name: "developers"
      permission: "push"
    - name: "maintainers"  
      permission: "admin"
```

## 🔒 Repository Security Setup

### Branch Protection Rules

The system automatically configures branch protection with:

```yaml
branch_protection:
  # Require pull request reviews
  required_reviews: 2
  dismiss_stale_reviews: true
  require_code_owner_reviews: true
  
  # Require status checks
  required_status_checks:
    - "continuous-integration"
    - "security-scan"
    - "quality-gate"
    
  # Restrict direct pushes
  restrict_pushes: true
  allowed_push_users: []  # Only admins can push directly
  
  # Additional protections
  allow_force_pushes: false
  allow_deletions: false
  required_linear_history: true
```

### Security Policies

Automatically includes:
- **Security Policy** (`SECURITY.md`)
- **Code of Conduct** (`CODE_OF_CONDUCT.md`)
- **Contributing Guidelines** (`CONTRIBUTING.md`)
- **Issue Templates** (Bug reports, feature requests)
- **Pull Request Templates**

## 🔄 GitHub Actions Integration

### Included Workflows

**Continuous Integration (`ci.yml`)**
```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Environment
        # Setup based on project type
      - name: Run Tests
        # Project-specific testing
      - name: Security Scan
        # Automated security scanning
```

**Documentation Update (`readme-docs.yml`)**
```yaml  
name: Update Documentation
on:
  push:
    paths: ['docs/**', 'README.md']

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Documentation
        # Automated doc generation
      - name: Update README
        # Keep README.md synchronized
```

### Custom Workflow Integration

```yaml
# In configuration file
github:
  workflows:
    custom_workflows:
      - path: ".github/workflows/custom-deploy.yml"
        template: "deploy-workflow.yml.template"
        variables:
          DEPLOY_TARGET: "production"
          NOTIFICATION_CHANNEL: "#deployments"
```

## 👥 Team and Collaboration Setup

### Team Management

```yaml
github:
  teams:
    - name: "core-developers"
      permission: "admin"
      members:
        - "lead-dev"
        - "senior-dev"
    
    - name: "contributors"
      permission: "push" 
      members:
        - "contributor1"
        - "contributor2"
        
    - name: "reviewers"
      permission: "triage"
      members:
        - "external-reviewer"
```

### Code Owners Configuration

```yaml
# Automatic CODEOWNERS generation
github:
  code_owners:
    global: ["@team-leads"]
    patterns:
      - path: "src/**"
        owners: ["@core-developers"]
      - path: "docs/**"
        owners: ["@documentation-team"] 
      - path: ".github/**"
        owners: ["@devops-team"]
```

## 📋 Issue and PR Templates

### Issue Templates

**Bug Report Template**
```markdown
---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Bug Description
A clear and concise description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
A clear description of what you expected to happen.

## Actual Behavior
A clear description of what actually happened.

## Environment
- OS: [e.g. Windows, macOS, Linux]
- Version: [e.g. 1.0.0]
- Browser: [if applicable]

## Additional Context
Add any other context about the problem here.
```

**Feature Request Template**
```markdown
---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## Feature Description
A clear and concise description of what you want to happen.

## Problem Statement
A clear description of what the problem is. Ex. I'm always frustrated when [...]

## Proposed Solution
A clear description of what you want to happen.

## Alternative Solutions
A clear description of any alternative solutions you've considered.

## Additional Context
Add any other context or screenshots about the feature request here.
```

### Pull Request Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly in hard-to-understand areas
- [ ] Documentation updated as needed
- [ ] No new warnings introduced

## Related Issues
Closes #(issue_number)
```

## 🔧 Advanced Configuration

### Repository Secrets Management

```yaml
github:
  secrets:
    - name: "API_KEY"
      description: "API key for external service"
    - name: "DATABASE_URL"
      description: "Database connection string"
    - name: "DEPLOY_TOKEN"
      description: "Deployment token"
```

### Webhook Configuration

```yaml
github:
  webhooks:
    - url: "https://your-service.com/webhook"
      events: ["push", "pull_request", "issues"]
      secret: "webhook-secret"
      active: true
```

### Repository Visibility and Access

```yaml
github:
  repository:
    private: true
    visibility: "private"  # public, private, internal
    
    # Access control
    permissions:
      issues: "enabled"
      projects: "enabled" 
      wiki: "disabled"
      downloads: "enabled"
      
    # Merge settings
    merge_settings:
      allow_merge_commit: true
      allow_squash_merge: true
      allow_rebase_merge: false
      delete_branch_on_merge: true
```

## 🐛 Troubleshooting

### Common Issues

**GitHub CLI not authenticated**
```bash
Error: GitHub CLI not authenticated
```
Solution:
```bash
# Login to GitHub CLI
gh auth login

# Verify authentication
gh auth status
```

**Insufficient permissions**
```bash
Error: Insufficient permissions to create repository
```
Solutions:
- Ensure GitHub token has `repo` scope
- Verify organization membership and permissions
- Check if repository name conflicts with existing repo

**Branch protection setup failed**
```bash
Warning: Failed to set up branch protection rules
```
Solutions:
- Ensure repository has at least one commit
- Verify admin permissions on repository
- Check if branch exists before setting protection

### Debug Commands

```bash
# Test GitHub integration without creating files
python seeding.py --github-integration --dry-run --verbose

# Verify GitHub CLI setup
gh auth status
gh repo list

# Test repository creation
gh repo create test-repo --private --confirm
gh repo delete test-repo --confirm
```

### Recovery Procedures

**Repository Creation Failed**
```bash
# Clean up failed repository
gh repo delete failed-repo --confirm

# Retry with different settings
python seeding.py --github-integration --project-name "new-name"
```

**Branch Protection Issues**
```bash
# Reset branch protection
gh api repos/:owner/:repo/branches/main/protection -X DELETE

# Reapply protection rules
python seeding.py --update-github-settings
```

## 📊 Monitoring and Analytics

### Repository Insights

The system can optionally set up:
- **Traffic Analytics**: Monitor repository views and clones
- **Contributor Insights**: Track contributor activity
- **Security Advisories**: Monitor security alerts
- **Dependency Insights**: Track dependency updates

### Integration Health Checks

```yaml
github:
  monitoring:
    health_checks:
      - workflow_runs: true
      - branch_protection: true
      - security_alerts: true
      - dependency_updates: true
      
    notifications:
      slack_webhook: "https://hooks.slack.com/services/..."
      email: "team@example.com"
```

## 🚀 Best Practices

### Repository Naming
- Use kebab-case for repository names
- Include organization prefix for team projects
- Keep names descriptive but concise

### Branch Strategy
- Use `main` as the default branch
- Implement feature branch workflow
- Set up branch protection on `main` and `develop`

### Security
- Enable branch protection rules
- Require code reviews for all changes
- Set up automated security scanning
- Use repository secrets for sensitive data

### Documentation
- Include comprehensive README.md
- Add clear contributing guidelines
- Maintain up-to-date issue templates
- Document deployment and setup procedures

---

*For more information, see the [Configuration Guide](./configuration.md) and [CLI Reference](../reference/cli.md).*