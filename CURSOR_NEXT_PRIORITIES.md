# Cursor - Next Priorities After PR #156 Merge

**Status**: PR #156 merged to develop ✅
**Completed**: Commercial bug fixes + docs Phase 1 cleanup
**Focus**: Clean up CI issues, continue commercial infrastructure

---

## 🎯 Immediate Priorities (Next Pull)

### **Priority 1: Fix Import Sorting** ⚡ QUICK WIN
**Type**: Style Fix
**Effort**: 5 minutes
**Impact**: Unblocks future PRs from lint failures
**Priority Score**: 9 (High urgency, low effort)

**Task**:
```bash
# Install isort
pip install isort

# Auto-fix all 44 files
isort seeding.py commercial_cli.py src/ tests/ scripts/ templates/

# Verify
flake8 --select=I seeding.py src/ tests/

# Commit
git checkout -b fix/import-sorting-cleanup
git add -A
git commit -m "style: fix import ordering across codebase

- Run isort on all Python files
- Resolves 44 lint errors from PR #156
- Aligns with flake8-isort standards"

git push origin fix/import-sorting-cleanup
gh pr create --base develop --title "style: Fix import ordering" --body "Quick cleanup from PR #156"
```

**Success**: All lint checks pass, future PRs won't fail on imports ✅

---

### **Priority 2: Fix Database Test Mocks** ⚡
**Type**: Test Fix
**Effort**: 15 minutes
**Impact**: 3 failing tests → all green
**Priority Score**: 8 (Blocks test suite at 100%)

**Task**:
Fix `tests/unit/test_commercial_infrastructure.py` - 3 tests failing:
1. `test_database_manager_initialization_with_url`
2. `test_database_manager_initialization_with_env_var`
3. `test_execute_query_with_pool`

**Problem**: Tests mock `src.commercial.database.SimpleConnectionPool` but should mock `psycopg2.pool.SimpleConnectionPool`

**Fix**:
```python
# In tests/unit/test_commercial_infrastructure.py
# Find all instances of:
with patch("src.commercial.database.SimpleConnectionPool")

# Replace with:
with patch("psycopg2.pool.SimpleConnectionPool")
```

**Commit**:
```bash
git checkout -b fix/database-test-mocking
git add tests/unit/test_commercial_infrastructure.py
git commit -m "test: fix database test mocking for CI compatibility

- Mock psycopg2.pool.SimpleConnectionPool instead of module attribute
- Resolves 3 failing test cases
- Test suite now 100% passing (231/231)"

git push origin fix/database-test-mocking
gh pr create --base develop --title "test: Fix database test mocking"
```

**Success**: All 231 tests pass ✅

---

### **Priority 3: Fix Datetime Defaults (Tech Debt)** ⏰
**Type**: Bug Fix (Low Severity)
**Effort**: 20 minutes
**Impact**: Correct period calculations
**Priority Score**: 6 (Important but not urgent)

**From Oracle review** - the datetime comparison bug in models.

**Task**: See UPDATED_ASSESSMENT.md "Bug 3: Datetime Defaults"

Fix `src/commercial/models/__init__.py`:
- Subscription.current_period_end → Optional[datetime] = None
- UsageMetrics.period_end → Optional[datetime] = None
- Update __post_init__ to check `if is None`

---

## 📋 Kanban Pull Recommendations

### **High Capacity Today (1+ hour)**
Pull all 3 priorities:
1. Import sorting (5 min) ⚡
2. Database tests (15 min) ⚡
3. Datetime defaults (20 min) ⚡

**Total**: 40 minutes → Clean slate ✅

### **Medium Capacity (30-60 min)**
Pull quick wins:
1. Import sorting (5 min) ⚡
2. Database tests (15 min) ⚡

**Total**: 20 minutes → CI clean ✅

### **Low Capacity (<30 min)**
Just the quickest:
1. Import sorting (5 min) ⚡

**Total**: 5 minutes → Lint fixed ✅

---

## 🚀 After CI Cleanup - Bigger Picture

Once CI is green, Cursor should focus on:

### **Week 2-3 Goals** (From WEEK2_FOCUS.md if it exists):
1. **API Testing** - Get coverage from 7% → 80%
2. **PostgreSQL Integration** - Replace in-memory with real DB
3. **Integration Tests** - End-to-end workflow testing
4. **Documentation Phase 2** - Migrate remaining valuable docs

### **ClemNova Preparation**:
- Customer onboarding workflow
- Organization deployment testing
- Performance optimization
- Security audit

---

## 🎯 Recommended Immediate Action

**Tell Cursor**:
> "Great job on the PR! Now let's clean up the CI issues. Start with Priority 1: Run `isort` to fix import ordering (5 min quick win). Create a feature branch, fix imports, commit, and create a small PR. This will make future PRs much cleaner."

**Command for Cursor**:
```bash
git checkout develop
git pull origin develop
git checkout -b fix/import-sorting-cleanup
pip install isort
isort seeding.py commercial_cli.py src/ tests/ scripts/ templates/
git add -A
git commit -m "style: fix import ordering across codebase"
git push origin fix/import-sorting-cleanup
gh pr create --base develop
```

---

## 📊 Current State Summary

**✅ Completed**:
- Commercial SaaS infrastructure foundation
- Production-blocking bugs fixed
- Docs Phase 1 cleanup (60+ files organized)
- PR #156 merged to develop

**⏳ Immediate TODOs**:
- Import sorting (5 min)
- Database test fixes (15 min)
- Datetime defaults (20 min)

**📅 Next Iteration**:
- API test coverage
- PostgreSQL integration
- Docs Phase 2 migration
- Customer workflows

---

**Start with the 5-minute import sorting win! 🚀**
