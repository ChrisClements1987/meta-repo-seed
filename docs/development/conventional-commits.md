# Conventional Commit Standards

**Last Updated:** 2025-09-30  
**Version:** 1.0  
**Based on:** [Conventional Commits Specification v1.0.0](https://www.conventionalcommits.org/)

## Overview

Conventional Commits provide a lightweight convention on top of commit messages that enables automated tooling for changelog generation, semantic versioning, and better change tracking.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Required Elements

**Type:** Communicates the kind of change  
**Description:** Brief summary of the change (50 chars or less)

### Optional Elements

**Scope:** Component/area affected by the change  
**Body:** Detailed explanation of the change  
**Footer:** Breaking changes, issue references, co-authors

## Commit Types

### Primary Types (Required)

**feat** - A new feature for users
```bash
feat(auth): add JWT token validation
feat(business): add charity-nonprofit profile template
```

**fix** - A bug fix that affects users
```bash  
fix(deploy): resolve template processing error on Windows
fix(cli): handle missing configuration file gracefully
```

**docs** - Documentation changes only
```bash
docs(api): update deployment guide with new endpoints
docs: fix broken links in README
```

**style** - Code formatting, missing semicolons, etc (no logic change)
```bash
style: apply black formatting to seeding module
style(templates): fix indentation in Jinja2 templates
```

**refactor** - Code changes that neither fix bugs nor add features
```bash
refactor(parser): extract validation logic to separate module
refactor: simplify template processing pipeline
```

**test** - Adding or modifying tests
```bash
test(business): add integration tests for deployment scenarios
test: increase coverage for template validation
```

**chore** - Build process, tools, dependencies, etc
```bash
chore: update dependencies to latest versions
chore(ci): add Python 3.12 to test matrix
```

### Extended Types (Recommended)

**perf** - Performance improvements
```bash
perf(deploy): optimize template processing speed
perf: reduce memory usage during business profile generation
```

**build** - Build system or external dependencies
```bash
build: add webpack configuration for frontend assets
build(deps): update requirements.txt with security patches
```

**ci** - CI/CD configuration changes
```bash
ci: add automated deployment pipeline
ci(github): update branch protection rules
```

**revert** - Reverting a previous commit
```bash
revert: revert "feat(auth): add OAuth integration"

This reverts commit abc123def456.
Reason: OAuth integration causing deployment failures
```

## Scopes

Scopes provide additional context about which part of the codebase is affected:

### Business-in-a-Box Specific Scopes

**business** - Business profile and deployment functionality
```bash
feat(business): add SMB profile with accounting integration
fix(business): resolve startup profile template errors
```

**cli** - Command-line interface
```bash
feat(cli): add interactive onboarding wizard  
fix(cli): improve error messages for missing dependencies
```

**templates** - Template generation and processing
```bash
feat(templates): add Kubernetes deployment templates
fix(templates): resolve Jinja2 variable substitution issue
```

**auth** - Authentication and authorization
```bash
feat(auth): implement API key management
fix(auth): resolve JWT token expiration handling
```

**deploy** - Deployment and infrastructure
```bash
feat(deploy): add automated SSL certificate generation
perf(deploy): optimize Docker image build process
```

**api** - API endpoints and interfaces
```bash
feat(api): add business profile validation endpoint
docs(api): update OpenAPI specification
```

**config** - Configuration management
```bash
feat(config): add environment-specific configuration
fix(config): resolve YAML parsing for complex structures
```

### Technical Scopes

**ci** - Continuous integration
**deps** - Dependencies
**security** - Security-related changes
**performance** - Performance optimizations
**accessibility** - Accessibility improvements

## Commit Body Guidelines

### When to Include a Body

- **Complex changes** that need explanation
- **Business context** for feature decisions
- **Breaking changes** with migration information
- **Performance impacts** with benchmarks
- **Security considerations** that affect users

### Body Format

- Wrap at 72 characters per line
- Use present tense ("add" not "added")
- Include motivation and contrast with previous behavior
- Reference issues and pull requests when relevant

### Example with Body

```bash
feat(business): add charity-nonprofit profile template

Enables rapid deployment for charitable organizations with
pre-configured fundraising tools, donor management, and
compliance reporting systems.

Maintains 10-minute deployment goal through optimized
template processing and simplified configuration.

Key features:
- Automated donor database setup
- Fundraising campaign management
- Financial reporting dashboard
- Compliance monitoring tools

Addresses user feedback from issue #42 requesting
specialized nonprofit infrastructure support.
```

## Footer Guidelines

### Breaking Changes

Use `BREAKING CHANGE:` footer to indicate breaking changes:

```bash
feat(api): add new authentication flow

BREAKING CHANGE: API endpoints now require JWT authentication.
Migration guide available at docs/migration/v2-auth.md
```

### Issue References

Use footers to close issues or reference related work:

```bash
fix(deploy): resolve template processing on Windows

Fixes #123
Closes #456
Related to #789
```

### Co-authors

Credit additional contributors:

```bash
feat(business): implement SMB profile templates

Co-authored-by: Developer Name <developer@example.com>
Co-authored-by: Designer Name <designer@example.com>
```

## Business Context Examples

### Feature Addition with Business Impact

```bash
feat(business): add startup-basic profile template

Enables rapid infrastructure deployment for early-stage startups
with essential tools including accounting, CRM, and project management.

Business Impact:
- Reduces startup onboarding from days to 8-10 minutes
- Provides professional-grade infrastructure from day one
- Includes growth-ready scaling options
- Maintains cost efficiency for bootstrap budgets

Technical Implementation:
- Optimized template processing pipeline
- Environment-specific configuration management
- Automated service integration and testing
- Comprehensive deployment validation

Supports Business-in-a-Box 10-minute deployment promise
and addresses primary target market needs.

Closes #42
```

### Bug Fix with Production Impact

```bash
fix(deploy): resolve critical template processing error

Critical fix for deployment failure affecting all new startup
profiles on Windows environments. Template variable replacement
was failing due to encoding mismatch between UTF-8 and Windows-1252.

Root Cause:
- Jinja2 template engine defaulting to system encoding
- Windows environments using different default than Linux/Mac
- Variable substitution failing silently in some cases

Solution:
- Explicit UTF-8 encoding specification in template processing
- Enhanced error handling with descriptive messages
- Cross-platform encoding tests added to validation suite

Impact:
- Restores deployment capability for Windows users
- Prevents silent failures in template processing
- Improves error reporting for debugging

Tested on Windows 10, Windows 11, and Windows Server 2019.

Fixes #156
```

## Validation and Tools

### Commitlint Configuration

We use `@commitlint/config-conventional` with custom Business-in-a-Box rules:

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', [
      'business', 'cli', 'templates', 'auth', 'deploy', 
      'api', 'config', 'ci', 'deps', 'security'
    ]],
    'subject-max-length': [2, 'always', 50],
    'body-max-line-length': [2, 'always', 72],
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor', 
      'test', 'chore', 'perf', 'build', 'ci', 'revert'
    ]]
  }
};
```

### Pre-commit Hooks

Automatic validation on every commit:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/conventional-commits/commitlint
    rev: v17.7.1
    hooks:
      - id: commitlint
        stages: [commit-msg]
```

### CI/CD Integration

Commit message validation in GitHub Actions:

```yaml
# .github/workflows/commit-lint.yml
name: Commit Message Lint
on: [push, pull_request]
jobs:
  commitlint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: wagoid/commitlint-github-action@v5
```

## Common Patterns and Examples

### Feature Development Workflow

```bash
# Start feature
feat(business): begin charity-nonprofit profile implementation

# Add specific functionality  
feat(business): add donor management system to charity profile
feat(business): implement fundraising campaign tools
feat(templates): create charity-specific Kubernetes configs

# Bug fixes during development
fix(business): resolve charity profile validation errors
fix(templates): fix nonprofit template variable substitution

# Testing and documentation
test(business): add integration tests for charity deployment
docs(business): document charity-nonprofit profile usage

# Final polish
refactor(business): optimize charity profile deployment speed
perf(business): reduce charity template processing time by 30%
```

### Bug Fix Workflow

```bash
# Initial investigation
fix(deploy): investigate startup profile deployment failures

# Root cause identification  
fix(deploy): identify encoding issue in template processing

# Implementation
fix(deploy): resolve UTF-8 encoding in Windows environments

# Testing and validation
test(deploy): add cross-platform encoding tests
docs(troubleshooting): update Windows deployment guide
```

### Maintenance Workflow

```bash
# Dependencies
chore(deps): update Python dependencies for security patches
build(deps): upgrade Node.js packages to resolve vulnerabilities

# CI/CD improvements
ci: add Python 3.12 to test matrix
ci(github): update branch protection with new status checks

# Documentation maintenance
docs: update README with latest installation instructions
docs(api): sync OpenAPI spec with current implementation
```

## Integration with Development Workflow

### TDD Process Integration

1. **Write failing test** - `test(scope): add test for [feature]`
2. **Implement feature** - `feat(scope): implement [feature]`
3. **Refactor** - `refactor(scope): optimize [area] implementation`
4. **Documentation** - `docs(scope): document [feature] usage`

### Code Review Process

- **Reviewers validate** commit message format during PR review
- **Squash commits** into single conventional commit when merging
- **PR titles** should follow conventional commit format
- **Changelog generation** automated from conventional commits

### Release Process

```bash
# Version calculation based on commits since last release
# feat: commits → minor version bump  
# fix: commits → patch version bump
# BREAKING CHANGE: → major version bump

# Automatic changelog generation
# Categorizes changes by type (Features, Bug Fixes, etc.)
# Includes scope and description for user-friendly reading
```

## Benefits

### For Developers

- **Clear communication** - Intent obvious from commit message
- **Better git history** - Structured, searchable commit log
- **Faster reviews** - Reviewers understand changes quickly
- **Automated tooling** - CI/CD can parse and act on commits

### for Project Management

- **Automatic changelogs** - Generate release notes from commits
- **Semantic versioning** - Calculate version bumps automatically
- **Impact tracking** - Understand scope and type of changes
- **Release planning** - Categorize work by type and impact

### For Business-in-a-Box

- **Professional standards** - Consistent, enterprise-grade practices
- **Deployment tracking** - Clear history of business profile changes
- **User communication** - Auto-generated release notes for customers
- **Quality assurance** - Structured approach to change documentation

## Migration from Current Practice

### Gradual Adoption

1. **Week 1:** Documentation and training
2. **Week 2:** Soft enforcement with reminders
3. **Week 3:** Pre-commit hooks enabled
4. **Week 4:** CI validation required

### Existing Commits

- **No retroactive changes** - Leave existing commit history as-is
- **New standard applies** to all commits after implementation date
- **Squash merge PRs** to ensure main branch follows convention

## Troubleshooting

### Common Issues

**Subject too long:**
```bash
# ❌ Too long
feat(business): implement comprehensive charity-nonprofit profile template with donor management, fundraising tools, and compliance reporting

# ✅ Correct length
feat(business): add charity-nonprofit profile template
```

**Missing type:**
```bash
# ❌ No type
add user authentication system

# ✅ With type  
feat(auth): add user authentication system
```

**Wrong tense:**
```bash
# ❌ Past tense
feat(api): added new user endpoints

# ✅ Present tense
feat(api): add new user endpoints
```

**Invalid scope:**
```bash
# ❌ Invalid scope
feat(user-interface): add login form

# ✅ Valid scope
feat(auth): add login form
```

## Tools and Resources

### Recommended Tools

- **commitlint** - Lint commit messages
- **husky** - Git hooks management
- **conventional-changelog** - Generate changelogs
- **standard-version** - Automate versioning and changelog

### IDE Integration

- **VS Code:** Conventional Commits extension
- **JetBrains:** Conventional Commit plugin
- **Vim:** vim-conventional-commits plugin

### Learning Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [Semantic Versioning](https://semver.org/)

This standard ensures consistent, meaningful commit messages that support automated tooling while maintaining clear communication about project changes.
