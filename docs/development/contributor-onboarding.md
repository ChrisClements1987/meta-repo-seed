# Contributor Onboarding Guide

**Last Updated:** 2025-09-30  
**Version:** 1.0  
**Audience:** All contributors (human developers, AI agents, external contributors)

## 🚀 Welcome to Business-in-a-Box Development

This guide ensures all contributors understand our development standards and process requirements **before** making their first contribution.

## 📋 Quick Start Checklist

Before creating your first PR, ensure you understand:

- [ ] **Development Workflow** - GitFlow branching strategy
- [ ] **Documentation Standards** - 3-category system based on change type
- [ ] **Commit Standards** - Conventional commits format
- [ ] **PR Template Requirements** - Automated validation and compliance
- [ ] **Testing Requirements** - TDD methodology and coverage standards

## 🎯 Our Development Philosophy

### Core Principles
1. **🛡️ Quality First** - All changes maintain professional standards
2. **📚 Documentation Required** - Comprehensive docs for all user-facing changes
3. **🧪 Test-Driven Development** - Tests written first, implementation follows
4. **🤝 Process Compliance** - Standards are enforced, not optional
5. **⚡ Rapid Iteration** - Process enables speed through quality

### Target Audience
- **Startups** - Rapid infrastructure deployment (10-minute goal)
- **Charities/Nonprofits** - Specialized business profiles and compliance
- **SMBs** - Professional-grade systems for growing businesses

## 🔄 Development Workflow Overview

### 1. Branch Strategy (GitFlow)
```bash
# Always start from develop
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/issue-123-brief-description

# Work on your changes with TDD
# Write failing tests → Implement → Refactor

# Push and create PR
git push -u origin feature/issue-123-brief-description
gh pr create --base develop
```

**Branch Naming Convention:**
- `feature/issue-[number]-[description]` - New features
- `fix/issue-[number]-[description]` - Bug fixes  
- `docs/[description]` - Documentation-only changes
- `hotfix/v[version]-[description]` - **EMERGENCY ONLY**

### 2. Required Standards

**Every contribution must:**
- ✅ Follow **conventional commit** format
- ✅ Complete **PR template** with appropriate category selection
- ✅ Include **tests** for any code changes (TDD methodology)
- ✅ Update **documentation** based on change category
- ✅ Pass **all CI checks** before merge

## 📚 Documentation Standards (Critical!)

### 🎯 Step 1: Categorize Your Changes

**Select exactly ONE category that best describes your contribution:**

**🚀 User-Facing Changes:**
- New CLI commands or options
- API endpoint changes  
- Configuration file modifications
- New business profile templates
- Feature additions/removals

**🛠️ Technical Changes:**
- Code refactoring or restructuring
- Architecture pattern updates
- Development process improvements
- Performance optimizations
- Internal tooling changes

**📋 Process/Research:**
- Gap analyses and research documents
- Audit findings and reports
- Process documentation updates
- Internal workflow improvements

**🐛 Bug Fixes:**
- Simple fixes with minimal user impact
- Error handling improvements
- Small corrections

### 🎯 Step 2: Complete Required Documentation

Based on your selected category:

**User-Facing Changes → Required:**
- 👤 **User Documentation** - Guides, FAQs, release notes
- 👨‍💻 **Developer Documentation** - API docs, architecture updates
- ⚙️ **Operations Documentation** - Deployment, configuration guides

**Technical Changes → Required:**
- 👨‍💻 **Developer Documentation** - Code docs, architecture updates
- ⚙️ **Operations Documentation** - If deployment/config affected

**Process/Research → Flexible:**
- 📋 **Process Documentation** - Analysis, research, internal docs

**Bug Fixes → Minimal:**
- Changelog entry if user-visible

## ✍️ Commit Message Standards

### Required Format
```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

### Required Types
- `feat` - New feature for users
- `fix` - Bug fix affecting users
- `docs` - Documentation only
- `style` - Code formatting  
- `refactor` - Code restructuring
- `test` - Test changes
- `chore` - Build/tooling
- `perf` - Performance improvements
- `ci` - CI/CD changes
- `hotfix` - **EMERGENCY ONLY**

### Business-in-a-Box Scopes
- `business` - Business profiles and deployment
- `cli` - Command-line interface
- `templates` - Template generation
- `auth` - Authentication systems
- `deploy` - Deployment infrastructure
- `api` - API endpoints
- `config` - Configuration management

### Examples
```bash
feat(business): add charity-nonprofit profile template
fix(deploy): resolve Windows template processing error  
docs(api): update deployment endpoint documentation
chore(deps): update Python security dependencies
```

## 🧪 Testing Requirements (TDD Mandatory)

### Test-Driven Development Process
1. **Write failing test** that defines the desired functionality
2. **Run test** to confirm it fails for the right reason
3. **Write minimal code** to make the test pass
4. **Run all tests** to ensure nothing breaks
5. **Refactor** code while keeping tests passing

### Coverage Requirements
- **80% minimum** diff coverage on changed lines
- **No reduction** in global coverage >0.5%
- **All tests pass** OR marked xfail/skip with linked issues

### Test File Organization
```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Component interaction tests  
├── e2e/           # End-to-end workflow tests
└── conftest.py    # Shared test configuration
```

## 📝 PR Template Compliance (Automated Validation)

### ⚠️ Critical: Template is Enforced

Our PR template validation **will fail your CI** if not completed properly. This is intentional to ensure quality.

### Required PR Template Sections

1. **📋 Change Summary** - Clear description of what changed
2. **Type of Change** - Check at least one box
3. **🎯 Documentation Category Assessment** - Select exactly one
4. **Category-Specific Documentation** - Complete based on selection
5. **🧪 TDD Compliance** - Test evidence and coverage
6. **🔍 Quality Checklist** - Code standards compliance

### Validation Rules (Automated)

**❌ PR will be blocked if:**
- Template sections are missing or incomplete
- No change type selected
- No documentation category selected  
- Multiple documentation categories selected
- Required documentation sections not completed
- Description too short (<100 characters)

**✅ PR validation passes when:**
- All required sections present
- Exactly one change type selected
- Exactly one documentation category selected
- Category-appropriate documentation completed
- Clear description provided

### Getting Help with Template

If validation fails:
1. **Read the error message** - specific guidance provided
2. **Edit your PR description** - use "Edit" button  
3. **Check required boxes** - follow validation guidance
4. **Save changes** - validation re-runs automatically

## 🚨 Emergency Procedures

### Hotfix Process (Use Sparingly!)

**Only for genuine production emergencies:**
- Production completely down
- Security actively exploited
- Data loss occurring
- Critical functionality broken for ALL users

**Hotfix Workflow:**
1. Declare incident with communication template
2. Branch from `main`: `hotfix/v1.2.1-brief-description`
3. Minimal fix only (no scope creep)
4. Expedited review (1-2 hours max)
5. Deploy to main, sync to develop
6. Mandatory post-incident review

**See:** `docs/operations/hotfix-workflow.md` for complete procedures

## 🔧 Development Environment Setup

### Required Tools
```bash
# Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt

# Node.js for commit validation
npm install

# Git hooks (optional but recommended)
npm run prepare  # Installs husky for commit linting
```

### Recommended VS Code Extensions
- **Conventional Commits** - Guided commit messages
- **Python** - Language support and debugging
- **GitLens** - Enhanced git capabilities
- **Markdown All in One** - Documentation editing

### Recommended Development Workflow
1. **Install commitizen** for guided commits: `npm install -g commitizen`
2. **Use guided commits**: `git cz` instead of `git commit`
3. **Run tests locally**: `python -m pytest` before pushing
4. **Check documentation**: Ensure appropriate docs updated

## ❌ Common Mistakes to Avoid

### Process Violations
- ❌ **Blank PR template** - Will fail validation
- ❌ **Wrong documentation category** - Delays review process  
- ❌ **Multiple categories selected** - Validation failure
- ❌ **Missing tests for code changes** - TDD requirement
- ❌ **Non-conventional commits** - CI failure

### Branch Management Issues
- ❌ **Branching from main** - Always branch from develop
- ❌ **Long-lived branches** - Keep feature branches small (3-5 days max)
- ❌ **Merge conflicts** - Rebase regularly: `git pull --rebase origin develop`

### Documentation Issues
- ❌ **User-facing changes without user docs** - Required for features
- ❌ **Architecture changes without dev docs** - Required for technical changes
- ❌ **Config changes without ops docs** - Required for deployment changes

## ✅ Success Patterns

### High-Quality Contributions
- ✅ **Clear change categorization** - Makes review efficient
- ✅ **Comprehensive but appropriate documentation** - Right level for change type
- ✅ **Test-first development** - Demonstrates functionality clearly
- ✅ **Business context in commits** - Explains why, not just what
- ✅ **Small, focused PRs** - Easier to review and merge

### Efficient Workflow
- ✅ **Regular develop syncing** - `git pull --rebase origin develop` daily
- ✅ **Early PR creation** - Draft PRs for early feedback
- ✅ **Self-review before submission** - Catch obvious issues
- ✅ **Clear commit history** - Tell story of development
- ✅ **Responsive to feedback** - Address review comments quickly

## 📖 Additional Resources

### Essential Reading
- [AGENTS.md](../../AGENTS.md) - Complete development workflow
- [Documentation Standards](documentation-standards.md) - Detailed documentation guide
- [Conventional Commits](conventional-commits.md) - Complete commit standards
- [Contributing Guidelines](contributing.md) - High-level contribution overview

### Workflow References
- [GitFlow Workflow](../analysis/gitflow-gap-analysis.md) - Our branching strategy analysis
- [Hotfix Procedures](../operations/hotfix-workflow.md) - Emergency response
- [Branch Protection Rules](../operations/branch-protection-rulesets.md) - Automated quality gates

### Business Context
- [Business-in-a-Box Vision](../development/roadmap.md) - Project goals and target market
- [10-Minute Deployment Promise](../guides/user/) - User experience standards

## 🆘 Getting Help

### When You're Stuck
1. **Check validation error messages** - Usually contain specific guidance  
2. **Review this guide** - Most common issues covered
3. **Look at recent successful PRs** - Examples of proper template completion
4. **Read linked documentation** - Detailed guides for specific areas

### Process Questions
- **Unclear on documentation category?** See [Documentation Standards](documentation-standards.md)
- **Commit message format issues?** See [Conventional Commits](conventional-commits.md)
- **Testing requirements unclear?** See TDD section in [AGENTS.md](../../AGENTS.md)
- **Emergency situation?** See [Hotfix Workflow](../operations/hotfix-workflow.md)

### Quality Standards Questions  
- **Code formatting:** We use `black` and `flake8` - CI will validate
- **Test coverage:** 80% minimum on changed lines
- **Performance impact:** Must maintain 10-minute deployment goal
- **Breaking changes:** Require user documentation and migration guide

## 🎯 Your First Contribution

### Recommended Approach
1. **Find a small, well-defined issue** (look for `good-first-issue` label)
2. **Read this entire guide** - Don't skip sections
3. **Review the related documentation** - Understand context
4. **Follow TDD process** - Write test first
5. **Complete PR template thoroughly** - Expect validation
6. **Be responsive to feedback** - Reviews help maintain quality

### Success Metrics
- ✅ **First PR passes validation** - Shows process understanding
- ✅ **Minimal review iterations** - Quality submission
- ✅ **Documentation matches change scope** - Right level of docs
- ✅ **Tests demonstrate functionality** - Clear test coverage

**Remember:** Our process exists to maintain professional standards while enabling rapid development. Following these guidelines ensures your contributions integrate smoothly and support the Business-in-a-Box mission of empowering startups, charities, and SMBs with professional infrastructure.

Welcome to the team! 🚀
