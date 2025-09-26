# Pull Request: [TITLE]

## 📋 Change Summary
<!-- Provide a clear, concise description of what this PR accomplishes -->

**Type of Change:** 
- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that causes existing functionality to change)
- [ ] 🔧 Refactoring (code changes that neither fix bugs nor add features)
- [ ] 📚 Documentation (changes to documentation only)
- [ ] 🧪 Tests (adding missing tests or correcting existing tests)
- [ ] 🎨 Style (formatting, missing semicolons, etc; no code change)

**Related Issues:** 
<!-- Link related issues: Fixes #123, Closes #456, Related to #789 -->
<!-- REQUIRED: All PRs must reference at least one GitHub issue -->

---

## 🎯 GitHub Issue Management - MANDATORY

### ✅ **Issue Lifecycle Management**
- [ ] **GitHub issue exists** - This PR must reference an existing GitHub issue
- [ ] **Issue is properly labeled** - Issue has correct type/priority/component labels
- [ ] **Issue status updated** - Issue moved to "In Progress" or appropriate column
- [ ] **Issue will be closed** - This PR will close/resolve the referenced issue

### 📋 **Issue Documentation**
- [ ] **Issue acceptance criteria met** - All requirements from issue satisfied
- [ ] **Issue comments updated** - Progress and decisions documented in issue
- [ ] **Related issues linked** - Dependencies/blockers properly cross-referenced
- [ ] **Issue milestone assigned** - Issue assigned to appropriate release milestone

**Issue References:**
- Primary Issue: #___ (this PR closes/fixes this issue)
- Related Issues: #___, #___ (supporting/dependent issues)
- Milestone: _____ (release version this contributes to)

---

## 📊 Project Roadmap Updates - MANDATORY

### ✅ **Roadmap Maintenance**
- [ ] **Roadmap updated** - `docs/development/roadmap.md` reflects this change
- [ ] **Feature status updated** - Completed features moved from planned to done
- [ ] **Priority adjustments** - Related features reprioritized if needed  
- [ ] **Timeline impact** - Release timeline updated if this affects schedule

### 🗺️ **Roadmap Integration**
- [ ] **Feature placement verified** - New features added to appropriate roadmap section
- [ ] **Dependencies mapped** - Prerequisites and blockers documented
- [ ] **Success metrics defined** - How completion will be measured
- [ ] **Business value articulated** - Why this feature matters for Business-in-a-Box vision

---

## 🏗️ Project Structure Compliance - MANDATORY

### ✅ **File Placement Requirements**
**ROOT LEVEL - Only these files allowed:**
- [ ] **Core files only** - README.md, LICENSE, .gitignore, pyproject.toml/requirements.txt
- [ ] **Configuration files** - pytest.ini, .pre-commit-config.yaml, etc.
- [ ] **Main script** - seeding.py (legacy, will be deprecated)
- [ ] **NO ad-hoc files** - No temporary scripts, analysis files, or random documents

### 📁 **Proper Directory Structure**
- [ ] **Documentation** - All docs in `docs/` hierarchy (not root)
  - `docs/guides/` - User guides
  - `docs/architecture/` - Technical architecture
  - `docs/development/` - Development process docs
- [ ] **Scripts** - All scripts in `scripts/` directory
- [ ] **Source code** - All source in `src/` hierarchy
- [ ] **Templates** - All templates in `templates/` or `src/templates/`
- [ ] **Analysis/Research** - In `docs/research/` or `docs/analysis/`

### 🚫 **File Placement Violations**
**Check for these violations and fix them:**
- [ ] **No root-level markdown** - Files like `BACKLOG_GROOMING_SUMMARY.md` must move to `docs/development/`
- [ ] **No root-level scripts** - Files like `demo_parser.py`, `sync_structures.py` must move to `scripts/`
- [ ] **No temporary directories** - `analysis/`, `temp/`, etc. must be cleaned up or properly located
- [ ] **No ad-hoc files** - Issue summaries, workflow docs, etc. belong in `docs/`

### ✅ **File Placement Actions Taken**
```
Files moved in this PR:
FROM: [root]/filename.ext
TO:   [proper-location]/filename.ext

Rationale: [why this placement is correct]
```

---

## 🧹 Root Directory Cleanup - MANDATORY

### ✅ **Current Root Cleanup**
- [ ] **Identified root violations** - Listed all files that don't belong in root
- [ ] **Proper relocation planned** - Each file has a designated proper location
- [ ] **No broken links** - All references updated after moving files
- [ ] **Import paths fixed** - Python imports updated for moved modules

**Root Directory Violations Found:**
```
Files that violate project structure:
- [ ] BACKLOG_GROOMING_SUMMARY.md → docs/development/backlog-grooming.md
- [ ] DEVELOPMENT_WORKFLOW.md → docs/development/workflow.md  
- [ ] ISSUE_33_IMPLEMENTATION_SUMMARY.md → docs/development/implementation-notes/
- [ ] demo_parser.py → scripts/demo/ or remove if temporary
- [ ] sync_structures.py → scripts/maintenance/
- [ ] analysis/ → docs/research/ or remove if outdated
```

### 🎯 **Structure Enforcement**
- [ ] **Future prevention** - Added comments/docs explaining proper structure
- [ ] **Documentation updated** - README or contributing guide explains file placement
- [ ] **.gitignore updated** - Patterns added to prevent future violations
- [ ] **Linting rules** - Pre-commit hooks or CI checks added if possible

## 🧪 Test-Driven Development Compliance

### ✅ **REQUIRED: Tests Written FIRST**
- [ ] **I wrote tests BEFORE implementing the feature/fix** (TDD approach)
- [ ] **All new functionality is covered by tests** (unit and/or integration)
- [ ] **All existing tests continue to pass** (no regressions introduced)
- [ ] **Test coverage maintained or improved** (check with `pytest --cov`)

### 📊 **Test Evidence Required**
```bash
# Paste test run results here showing:
# 1. New tests written and passing
# 2. Overall test success rate
# 3. Coverage percentage
```

**Test Files Modified/Added:**
- [ ] `tests/unit/test_*.py` - Unit tests added/modified
- [ ] `tests/integration/test_*.py` - Integration tests added/modified
- [ ] `tests/conftest.py` - Test configuration updated if needed

### 🚫 **TDD Violation Check**
- [ ] **I confirm I did NOT write implementation code before writing tests**
- [ ] **I can demonstrate the test-fail-pass-refactor cycle was followed**

---

## 📚 Documentation Updates - MANDATORY

### ✅ **Core Documentation Updates**
- [ ] **README.md** - Updated if user-facing changes or new features
- [ ] **CHANGELOG.md** - Entry added describing changes for users
- [ ] **docs/development/roadmap.md** - Updated if this affects planned features

### 📖 **Guides and Architecture Documentation**
- [ ] **User Guides** - Created/updated if new user functionality
  - [ ] `docs/guides/` - New guide created for complex features
  - [ ] Existing guides updated for changed functionality
- [ ] **Architecture Documentation** - Updated if system design changed
  - [ ] `docs/architecture/` - Architecture decision records (ADRs) added
  - [ ] System diagrams updated if architectural changes made
  - [ ] API documentation updated if interfaces changed

### 🔧 **Developer Documentation**
- [ ] **Code Comments** - Complex logic explained inline
- [ ] **Docstrings** - All new functions/classes documented
- [ ] **Type Hints** - Added to all new Python code

---

## 🤖 AI Context Maintenance - MANDATORY

### ✅ **AI Context Files Updated**
- [ ] **AGENTS.md** - Updated if new AI workflows or context needed
- [ ] **Project Context Files** - Updated with new patterns, decisions, or architectural changes
- [ ] **Code Examples** - Updated in documentation if implementation patterns changed

### 🧠 **Context Quality Check**
- [ ] **New patterns documented** - Any new coding patterns explained for AI assistance
- [ ] **Decision rationale captured** - Why choices were made, documented for future AI context
- [ ] **Breaking changes flagged** - Any changes that affect AI understanding of the codebase

---

## 🔍 Code Quality Checklist

### 🧹 **Code Standards**
- [ ] **Linting passes** - `ruff check` and `mypy` clean
- [ ] **Formatting applied** - Code formatted with `black` or equivalent
- [ ] **No debugging code** - Print statements, debugger calls, etc. removed
- [ ] **Security review** - No hardcoded secrets, proper input validation

### 🏗️ **Architecture Compliance**
- [ ] **Follows project patterns** - Consistent with existing codebase structure
- [ ] **Separation of concerns** - Business logic separated from infrastructure
- [ ] **Error handling** - Appropriate exception handling implemented
- [ ] **Performance consideration** - No obvious performance issues introduced

---

## 🚀 Business-in-a-Box Alignment

### 🎯 **North Star Compliance**
- [ ] **Supports target market** - Benefits startups, charities, non-profits, or SMBs
- [ ] **Reduces complexity** - Makes business infrastructure easier, not harder
- [ ] **Maintains automation** - Preserves or enhances self-governing systems
- [ ] **Professional standards** - Maintains enterprise-grade quality

### ⚡ **Performance Impact**
- [ ] **10-minute deployment goal** - Changes don't slow down core deployment speed
- [ ] **Resource efficiency** - Reasonable memory/CPU usage
- [ ] **Scalability maintained** - Works for solo founder to mature organization

---

## 📋 Review Readiness Checklist

### 🔍 **Self-Review Completed**
- [ ] **Code review performed** - I've reviewed my own code changes
- [ ] **Commit messages clear** - Descriptive commits following convention
- [ ] **Branch up to date** - Merged latest develop/main changes
- [ ] **No merge conflicts** - Clean merge possible

### 📊 **Evidence Provided**
- [ ] **Screenshots** - For UI changes (if applicable)
- [ ] **Performance benchmarks** - For performance-critical changes
- [ ] **Migration notes** - For breaking changes requiring user action

---

## 🚨 Blocking Issues Declaration

### ⚠️ **Known Issues**
<!-- List any known issues, limitations, or technical debt introduced -->
- None / [List any issues]

### 🔄 **Follow-up Work Required**
<!-- List any immediate follow-up work needed after this PR -->
- None / [List follow-up items]

---

## 📝 Reviewer Guidelines

### 🎯 **Focus Areas for Review**
- [ ] **Test quality** - Tests actually validate the functionality
- [ ] **Documentation accuracy** - Docs match implementation
- [ ] **Architecture alignment** - Fits with Business-in-a-Box vision
- [ ] **Performance impact** - No significant performance degradation
- [ ] **Security implications** - No security vulnerabilities introduced

### ❓ **Questions for Reviewer**
<!-- Specific questions or areas where you want focused review -->

---

## 🏆 Definition of Done

**This PR is ready to merge when:**
- ✅ All checklist items above are completed
- ✅ All tests pass (including new tests)
- ✅ Documentation is updated and accurate
- ✅ AI context files are current
- ✅ Code review approved by team member
- ✅ No blocking issues remain

---

## 📊 Metrics Impact

### 📈 **Positive Impact**
<!-- What metrics will this improve? -->
- Deployment speed
- User experience
- Code quality
- Documentation coverage
- Test coverage

### ⚠️ **Potential Concerns**
<!-- Any metrics that might be negatively affected? -->
- None identified / [List concerns]

---

**🚫 MERGE BLOCKER:** This PR cannot be merged until:
1. ✅ All tests pass with TDD evidence provided
2. ✅ Documentation updates are complete and accurate
3. ✅ AI context files are updated
4. ✅ Code review is approved
5. ✅ All checklist items are completed

---

*This template enforces our commitment to test-driven development, comprehensive documentation, and maintaining AI context for sustainable development practices.*