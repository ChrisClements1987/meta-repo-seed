# Branch Protection Rulesets

**Last Updated:** 2025-09-30  
**Author:** CI/CD Automation  

## Overview

GitHub rulesets enforce quality gates and prevent code from merging without passing all required checks. This ensures production stability and maintains our professional development standards.

## Protected Branches

### Main Branch (`main`)
**Purpose:** Production-ready code for customer deployments  
**Ruleset ID:** 8381314

**Protection Rules:**
- ❌ **No direct pushes** - all changes via pull requests only
- ❌ **No force pushes** - history preservation required
- ❌ **No branch deletion** - permanent history maintenance
- ✅ **1 approval required** - human code review mandatory
- ✅ **Code owner review required** - domain expertise validation
- ✅ **Require up-to-date branches** - no outdated merges
- ✅ **Dismiss stale reviews** - fresh approval after changes

**Required Status Checks:**
- `test` - All Python versions (3.9, 3.10, 3.11, 3.12)
- `lint` - Code formatting and style validation
- `security` - Security vulnerability scanning
- `business-validation` - 10-minute deployment promise validation
- `license-compliance` - GPL license violation detection

### Develop Branch (`develop`)  
**Purpose:** Integration branch for feature development  
**Ruleset ID:** 8381356

**Protection Rules:**
- ❌ **No direct pushes** - all changes via pull requests only
- ❌ **No force pushes** - history preservation required  
- ❌ **No branch deletion** - permanent integration history
- ✅ **1 approval required** - peer code review mandatory
- ✅ **Require up-to-date branches** - no outdated merges
- ✅ **Dismiss stale reviews** - fresh approval after changes

**Required Status Checks:**
- `test` - All Python versions (3.9, 3.10, 3.11, 3.12)
- `lint` - Code formatting and style validation  
- `security` - Security vulnerability scanning
- `business-validation` - 10-minute deployment promise validation
- `license-compliance` - GPL license violation detection

## CI/CD Workflow Integration

### Status Check Sources
All required status checks come from `.github/workflows/`:

1. **`ci.yml`** - Provides `test`, `lint`, `security`, `business-validation` contexts
2. **`license-check.yml`** - Provides `license-compliance` context

### Bypass Policy
- **Repository administrators** can bypass rules in emergency situations
- **Emergency bypass** should be documented and reviewed post-incident
- **No routine bypassing** - maintain process integrity

## Developer Impact

### Before Merge Requirements
✅ **All CI checks must pass:**
- Unit tests across all Python versions
- Code formatting (black, isort) compliance
- Linting (flake8) without critical issues
- Security scans (bandit, safety) clean
- Business validation (10-minute deployment) successful
- License compliance (no GPL violations) verified

### What This Prevents
❌ **Broken code reaching develop/main:**
- Failing tests cannot be merged
- Improperly formatted code blocked
- Security vulnerabilities caught
- Performance regressions detected
- License compliance violations prevented

### Developer Workflow
1. **Create feature branch** from `develop`
2. **Write tests first** (TDD methodology)
3. **Implement feature** with proper formatting
4. **Run local checks** before push:
   ```bash
   python -m pytest
   black --check .
   flake8 .
   ```
5. **Push and create PR** - CI runs automatically
6. **Address any failures** before requesting review
7. **Get approval** - human review required
8. **Merge** - automated after all gates pass

## Troubleshooting

### Common CI Failures

**Test Failures:**
```bash
# Run specific test
python -m pytest tests/unit/test_filename.py -v

# Run with coverage
python -m pytest --cov=src --cov=seeding
```

**Formatting Issues:**
```bash
# Fix black formatting
black .

# Fix import sorting  
isort .
```

**Linting Issues:**
```bash
# Check specific issues
flake8 . --show-source

# Focus on critical issues
flake8 . --select=E9,F63,F7,F82
```

**Security Issues:**
```bash
# Check security locally
bandit -r . -x tests/

# Check dependencies
safety check
```

**Business Validation Failures:**
- Usually indicates performance regression
- Review deployment speed optimization
- Check for blocking operations in CLI commands

**License Compliance Failures:**
- GPL-licensed dependencies detected
- Replace with MIT/BSD/Apache alternatives
- Review `requirements*.txt` files

## Emergency Procedures

### Hotfix Process
For critical production issues:
1. **Create hotfix branch** from `main`
2. **Implement minimal fix** with test coverage
3. **Use admin bypass** if CI failures are unrelated to fix
4. **Document bypass reasoning** in PR description
5. **Merge to main** and back to develop
6. **Post-incident review** of bypass usage

### Status Check Debugging
If status checks fail to appear:
1. **Verify workflow files** are on the target branch
2. **Check GitHub Actions** tab for workflow runs
3. **Ensure branch names** match workflow triggers
4. **Validate YAML syntax** in workflow files

## Maintenance

### Adding New Status Checks
1. **Create workflow** in `.github/workflows/`
2. **Test workflow** runs successfully
3. **Update rulesets** via GitHub API:
   ```bash
   gh api -X PUT repos/ChrisClements1987/meta-repo-seed/rulesets/RULESET_ID --input ruleset.json
   ```
4. **Update this documentation**

### Removing Status Checks
1. **Remove from rulesets** first
2. **Disable or delete workflow** files
3. **Update documentation**

**Warning:** Never remove status checks during active development - coordinate with team first.

## Related Documentation
- [GitHub Workflows](../../.github/workflows/) - CI/CD pipeline definitions
- [AGENTS.md](../../AGENTS.md) - Development workflow and TDD process
- [GitFlow Gap Analysis](../analysis/gitflow-gap-analysis.md) - Implementation rationale
