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

---

## 🧪 Test-Driven Development Compliance

### ✅ **Test Coverage Requirements**
- [ ] **Tests written first (TDD)** OR **comprehensive diff coverage provided** 
- [ ] **All new/changed functionality is covered by tests** (unit and/or integration)
- [ ] **All existing tests pass** OR **failing tests are marked xfail/skip with linked issues**
- [ ] **Diff coverage on changed lines >= 80%** (paste coverage report below)
- [ ] **Global coverage not reduced by more than 0.5%**

### 📊 **Test Evidence**
```bash
# Paste test run results here showing:
# 1. Tests covering new/changed functionality
# 2. Diff coverage percentage on changed lines
# 3. Overall test success rate
```

**Test Files Modified/Added:**
- [ ] `tests/unit/test_*.py` - Unit tests added/modified
- [ ] `tests/integration/test_*.py` - Integration tests added/modified
- [ ] `tests/conftest.py` - Test configuration updated if needed
- [ ] N/A - No test files needed for this change

### 🔄 **Legacy Debt Exception**
If TDD or full test coverage isn't feasible:
- [ ] **Linked tech debt issue**: #[issue-number]
- [ ] **Risk assessment**: [describe impact of reduced test coverage]
- [ ] **Follow-up timeline**: [milestone or target date]

---

## 📚 Documentation Updates

### ✅ **Core Documentation Updates** *(Required if applicable)*
- [ ] **README.md** - Updated if user-facing changes or new features
- [ ] **CHANGELOG.md** - Entry added describing changes for users
- [ ] **docs/development/roadmap.md** - Updated if this affects planned features
- [ ] **N/A** - No core documentation updates needed because: _______________

### 📖 **Guides and Architecture Documentation** *(Required if applicable)*
- [ ] **User Guides** - Created/updated if new user functionality
  - [ ] `docs/guides/` - New guide created for complex features
  - [ ] Existing guides updated for changed functionality
- [ ] **Architecture Documentation** - Updated if system design changed
  - [ ] `docs/architecture/` - Architecture decision records (ADRs) added
  - [ ] System diagrams updated if architectural changes made
  - [ ] API documentation updated if interfaces changed
- [ ] **N/A** - No guides/architecture updates needed because: _______________

### 🔧 **Developer Documentation**
- [ ] **Code Comments** - Complex logic explained inline
- [ ] **Docstrings** - All new functions/classes documented
- [ ] **Type Hints** - Added to all new Python code

---

## 🤖 AI Context Maintenance

### ✅ **AI Context Files Updated** *(Required if applicable)*
- [ ] **AGENTS.md** - Updated if new AI workflows or context needed
- [ ] **Project Context Files** - Updated with new patterns, decisions, or architectural changes
- [ ] **Code Examples** - Updated in documentation if implementation patterns changed
- [ ] **N/A** - No AI context updates needed because: _______________

### 🧠 **Context Quality Check**
- [ ] **New patterns documented** - Any new coding patterns explained for AI assistance
- [ ] **Decision rationale captured** - Why choices were made, documented for future AI context
- [ ] **Breaking changes flagged** - Any changes that affect AI understanding of the codebase

---

## 🔍 Code Quality Checklist

### 🧹 **Code Standards**
- [ ] **Linting passes** - `flake8` (current) OR `ruff check` if configured
- [ ] **Type checking** - `mypy` clean if configured in CI
- [ ] **Formatting applied** - `black` or current formatter applied (mark N/A if none configured)
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

## 🔄 Legacy Debt Impact
*Complete this section if you cannot meet standard requirements due to legacy constraints*

**Legacy Debt Items:**
- [ ] **N/A** - All standard requirements met
- [ ] **Linked tech debt issue(s)**: #[issue-number] 
- [ ] **Risk assessment**: [describe impact of any unmet requirements]
- [ ] **Follow-up timeline**: [milestone/target date for addressing debt]

---

**🚫 MERGE BLOCKER:** This PR cannot be merged until:
1. ✅ All tests pass OR failing tests marked xfail/skip with linked issues during stabilization
2. ✅ Diff coverage >= 80% on changed lines and global coverage not reduced >0.5%
3. ✅ Documentation updates complete for applicable changes
4. ✅ AI context updated for applicable changes
5. ✅ Code review approved
6. ✅ Any legacy debt items properly documented with follow-up

---

*This template enforces our commitment to test-driven development, comprehensive documentation, and maintaining AI context for sustainable development practices.*