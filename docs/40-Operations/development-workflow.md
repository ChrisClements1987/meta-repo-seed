# Development Workflow

**Version**: 2.0
**Last Updated**: 2025-10-16
**Purpose**: Development process and standards for Meta-Repo-Seed platform

---

## 📋 Work Selection Process

> **🚨 MANDATORY**: All development work MUST originate from a GitHub Issue. No exceptions.

### Before Starting Any Work

1. **Check GitHub Issues Backlog**: https://github.com/ChrisClements1987/meta-repo-seed/issues
2. **Select an Issue**: Choose from `status: ready` or high-priority issues matching your capacity
3. **Verify Issue Has**:
   - Clear acceptance criteria
   - Proper labels (`type:`, `priority:`, `area:`)
   - No blocking dependencies
4. **Assign Yourself**: Comment on issue or assign to yourself
5. **Link Issue to Branch**: Use format `feature/issue-{number}-description`

### If No Suitable Issue Exists

**DO NOT** start work without an issue. Instead:

1. **Create GitHub Issue** using appropriate template
2. **Add Required Labels**: `type:`, `priority:`, `area:`
3. **Define Acceptance Criteria**
4. **Get Approval** if high-effort or architectural change
5. **Then** proceed with work

> **Why This Matters**: GitHub Issues is our single source of truth. Ad-hoc work creates drift, duplication, and lost context in multi-agent environments.

---

## 🔄 Git Branching Strategy

### Branch Structure
- **`main`** - Production-ready releases only
- **`develop`** - Integration branch for all development work
- **`feature/*`** - Individual feature/fix branches
- **`sprint-*/*`** - Sprint-specific feature branches

### Workflow Process

#### 1. Start New Work - Branch from latest develop
```bash
git checkout develop
git pull origin develop       # Get latest develop (with other devs' work)
git checkout -b feature/issue-123-feature-name
```

#### 2. Feature Development
```bash
# Work on feature
git add .
git commit -m "feat: implement feature"
git push origin feature/issue-123-feature-name

# Create PR targeting develop (NOT main)
gh pr create --base develop --title "Feature: ..." --body "..."
```

#### 3. Release Process - develop → main (After UAT)
```bash
# When develop is ready for production release
# After User Acceptance Testing and quality verification
gh pr create --head develop --base main --title "🚀 Release v2.x.x: ..." --body "..."

# After release is merged to main, develop continues independently
# (develop accumulates new features while main stays stable)
```

---

## ⚠️ Critical Rules

### ❌ **NEVER DO:**
- Target `main` directly with feature PRs
- Sync develop with main regularly (destroys other devs' work)
- Merge develop→main without UAT and quality verification
- Work directly on develop branch

### ✅ **ALWAYS DO:**
- Branch from latest `develop` for all new work
- Target `develop` with all feature PRs
- Complete UAT before merging to `main`
- Use descriptive branch names: `feature/issue-123-description`

---

## 🧪 Test-Driven Development (TDD)

### **Mandatory TDD Requirements**
**EVERY contribution involving code changes MUST follow TDD:**

#### **Issue Creation Requirements:**
1. **Include TDD acceptance criteria** - Use issue templates that enforce TDD requirements
2. **Write tests first** - Before any implementation
3. **Document test cycle** - Show test-fail-pass-refactor evidence in PRs
4. **Maintain coverage** - No reduction in test coverage allowed

#### **Development Workflow:**
1. **Update develop branch**: `git checkout develop && git pull origin develop`
2. **Create feature branch**: `git checkout -b feature/issue-[number]-description`
3. **Write failing tests FIRST** - Before any implementation code
4. **Implement minimal code** - Make tests pass
5. **Refactor** - Clean up implementation
6. **Update documentation** - Guides, roadmap, changelog, AI context

### **Test Categories**
- **Unit Tests** (`tests/unit/`) - Individual functions and methods
- **Integration Tests** (`tests/integration/`) - Component interactions
- **End-to-End Tests** (`tests/e2e/`) - Complete workflows

### **Coverage Requirements**
- **Diff Coverage**: ≥80% coverage on changed lines required
- **Legacy Friendly**: Can mark failing tests as xfail with linked issues during stabilization
- **Test Types**: Unit, Integration, End-to-End

```bash
# Run specific test types
python -m pytest tests/unit/
python -m pytest tests/integration/

# Check coverage on changes
python -m pytest --cov=src --cov-report=term-missing
```

---

## 📝 Code Quality Standards

### **Code Style Guidelines**

#### **Python Code Style**
- **Follow PEP 8** with project-specific conventions
- **Use type hints** for function parameters and returns
- **Write descriptive docstrings** for all functions and classes
- **Use meaningful variable names** and clear structure

#### **Documentation Style**
- **Use clear headings** and consistent structure
- **Provide practical examples** with code snippets
- **Include parameter descriptions** and usage examples
- **Test all examples** to ensure they work

### **Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.12
        args: [--line-length=88]
```

---

## 🔄 Pull Request Process

### **Before Submitting Checklist**
- [ ] **Code follows style guidelines** and project conventions
- [ ] **Tests pass locally** (`python -m pytest`)
- [ ] **New features have tests** following TDD approach
- [ ] **Documentation updated** as needed
- [ ] **No merge conflicts** with develop branch
- [ ] **Commit messages** are descriptive and follow conventions

### **Pull Request Template**
```markdown
## Description
Brief description of changes made in this PR.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to not work)
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Related Issues
- Closes #123
- Related to #456

## Testing
- [ ] Existing tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed
- [ ] Cross-platform testing (if applicable)

## Documentation
- [ ] Code is commented appropriately
- [ ] Documentation updated
- [ ] Examples provided for new features
- [ ] CHANGELOG.md updated (if applicable)

## Screenshots/Examples
[If applicable, add screenshots or example output]

## Breaking Changes
[Describe any breaking changes and migration steps]

## Additional Notes
[Any additional information for reviewers]
```

### **Review Process**
1. **Automated Checks** - CI/CD pipeline, code quality, security scans
2. **Manual Review** - Code review, testing, documentation review
3. **Approval and Merge** - Required approvals, all checks pass, squash and merge

---

## 🏷️ Issue Management

### **Issue Types**
- **Bug Reports** - Something isn't working
- **Feature Requests** - New feature or improvement
- **Documentation** - Documentation improvements
- **Technical Debt** - Code quality and maintenance improvements

### **Issue Labels**
**Type Labels:**
- `bug` - Something isn't working
- `enhancement` - New feature or improvement
- `documentation` - Documentation improvements
- `question` - Questions about usage
- `help wanted` - Community contributions welcome

**Priority Labels:**
- `priority: high` - Critical issues
- `priority: medium` - Important improvements
- `priority: low` - Nice-to-have features

**Status Labels:**
- `status: triage` - Needs initial review
- `status: approved` - Ready for development
- `status: in-progress` - Currently being worked on
- `status: blocked` - Waiting on dependencies

---

## 🚀 Release Process

### **Version Management**
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR** - Breaking changes
- **MINOR** - New features, backward compatible
- **PATCH** - Bug fixes, backward compatible

### **Release Workflow**
1. **Prepare Release** - Create release branch from develop
2. **Update Documentation** - CHANGELOG.md, version numbers
3. **Create Release** - Merge to main, tag version
4. **Post-Release** - Merge back to develop

---

## 🔒 Security Guidelines

### **Security Practices**
- **Never commit secrets** - Use `.gitignore` for sensitive files
- **Validate user input** - Sanitize template variables and file paths
- **Use secure defaults** - Private repositories, secure permissions
- **Audit dependencies** - Regular security updates

### **Security Testing**
```bash
# Check for security vulnerabilities
python -m safety check

# Scan for secrets in code
python -m detect-secrets scan --all-files
```

---

## 📊 Performance Guidelines

### **Code Performance**
- **Avoid unnecessary file operations** - Use dry-run mode for testing
- **Cache template lookups** - Don't re-read templates repeatedly
- **Use generators** for large data processing
- **Profile performance** for complex operations

### **Testing Performance**
```bash
# Benchmark test execution time
python -m pytest --benchmark-only tests/

# Profile memory usage
python -m pytest --profile tests/
```

---

## 🆘 Getting Help

### **Community Support**
- **GitHub Discussions** - General questions and discussions
- **GitHub Issues** - Bug reports and feature requests
- **Documentation** - Comprehensive guides and examples

### **Quick Reference**
- **Onboarding**: [Onboarding Paths](../00-Foundation/onboarding-paths.md)
- **Contributing**: [Contributing Guide](../00-Foundation/contributing-guide.md)
- **Architecture**: [System Architecture](../20-Architecture/system-architecture.md)
- **Decision Records**: [Decision Indexes](../80-Meta/decision-indexes.md)

---

## ✅ Success Criteria

### **You're Ready to Develop When**
- [ ] **Completed onboarding** for your role
- [ ] **Can run tests** and main script successfully
- [ ] **Understand TDD workflow** and requirements
- [ ] **Know where to find** documentation and help
- [ ] **Can create first contribution** following all guidelines

### **Development Quality Checklist**
- [ ] **Followed TDD** - wrote tests first
- [ ] **Updated documentation** as needed
- [ ] **Used conventional commits** with descriptive messages
- [ ] **Created PR** with completed template
- [ ] **Addressed review feedback** promptly

---

**This development workflow ensures consistent, high-quality development practices across the Meta-Repo-Seed platform.**
