# Cursor - Next Focus [Updated Oct 17]

**Current**: PR #157 (formatting cleanup) is open  
**Status**: Clean, ready to merge  
**Next**: Move from cleanup → high-value commercial features

---

## ✅ PR #157 Assessment

**Title**: chore: apply pre-commit hook formatting fixes  
**Type**: Automated cleanup (no logic changes)  
**Files**: 4 files, 195 additions, 5 deletions  
**Quality**: ✅ Good - just whitespace and formatting  
**CI Status**: Only 1 check ran (validate-issue-links: PASSED)

**Recommendation**: This PR is fine. It will likely have same CI issues as #156 (not triggering full test suite), but it's just formatting so safe to merge with bypass.

---

## 🎯 Your Next Step (Chris)

### **Merge PR #157** (30 seconds)

Since it's just formatting cleanup:
```bash
gh pr merge 157 --repo ChrisClements1987/meta-repo-seed --squash --admin
```

Or wait for CI if you prefer, but it's low-risk formatting only.

---

## 🚀 Cursor's Next Focus (After #157)

**Stop doing**: Low-value cleanup (formatting, import sorting, lint chasing)  
**Start doing**: High-value commercial features

### **Priority Queue** (Kanban-Ready)

#### **🔴 High-Value, Quick Wins** (Pull These First)

**Task 1: Fix Unused Imports** (5 min) ⚡
- File: `src/commercial/services/organization_seeder.py`
- Lines: Remove 3 unused imports from line 15
- Impact: Clean up flake8 warnings
- Branch: `fix/commercial-unused-imports`

**Task 2: Fix Database Test Mocks** (15 min) ⚡
- File: `tests/unit/test_commercial_infrastructure.py`
- Fix: Change mock path from `src.commercial.database.SimpleConnectionPool` to `psycopg2.pool.SimpleConnectionPool`
- Impact: 3 tests pass, test suite 100% green
- Branch: `fix/database-test-mocking`

**Task 3: Fix Datetime Defaults** (20 min)
- Files: `src/commercial/models/__init__.py`
- Fix Subscription and UsageMetrics period_end logic
- Impact: Correct period calculations
- Branch: `fix/commercial-datetime-defaults`

**Total Quick Wins**: 40 minutes → Clean codebase ✅

---

#### **🟢 High-Value, Medium Effort** (Main Focus)

**Task 4: API Test Coverage** (2-3 hours) 🎯 **TOP PRIORITY**
- **Current**: 7% coverage (2% in latest)
- **Target**: 80% coverage
- **Files**: `tests/integration/test_commercial_api.py`
- **Impact**: Production-ready API confidence
- **Branch**: `feat/commercial-api-tests`

**What to test**:
- All CRUD endpoints (create, read, update, delete)
- Authentication/authorization flows
- Error handling (404, 403, 500)
- Request/response serialization
- Subscription upgrades
- Usage tracking
- Organization deployment status

---

**Task 5: PostgreSQL Integration** (3-4 hours) 🎯
- **Current**: In-memory fallback only
- **Target**: Full PostgreSQL persistence
- **Files**: `src/commercial/database/__init__.py`, `customer_manager.py`
- **Impact**: Production data persistence
- **Branch**: `feat/postgresql-persistence`

**What to implement**:
- Complete DatabaseManager connection handling
- Full CRUD for customers, organizations, subscriptions
- Migration scripts (Alembic)
- Connection pooling
- Transaction management

---

**Task 6: Docs Phase 2 Migration** (1-2 hours)
- **Current**: 60 files deleted, new structure created
- **Target**: Migrate 35 high-value files to docs-new/
- **Plan**: See `document_assessment_summary.md`
- **Impact**: Complete docs reorganization
- **Branch**: `docs/phase-2-migration`

---

## 🎓 Strategic Guidance for Cursor

### **Kanban Principles**:
1. **Pull based on capacity** - Don't overcommit
2. **Deliver value** - API tests > import sorting
3. **One task at a time** - WIP limit of 2
4. **Test everything** - Maintain 90%+ coverage
5. **Small PRs** - Easier to review and merge

### **What Good Looks Like**:
- Small, focused PRs (1-2 features)
- Clear conventional commit messages
- Tests included with code
- Documentation updated
- CI passing (or bypass justification clear)

### **What to Avoid**:
- Giant refactors (like PR #156 - too big!)
- Chasing lint perfection (diminishing returns)
- Blocked on CI (use bypass when appropriate)
- Low-value cleanup when features needed

---

## 📊 Capacity Assessment

**If Cursor has**:

**High Capacity (3+ hours)**:
- Pull Task 4 (API tests) - highest value

**Medium Capacity (1-2 hours)**:
- Pull Tasks 1-3 (quick wins) → Clean slate
- Then start Task 6 (docs migration)

**Low Capacity (<1 hour)**:
- Pull Tasks 1-2 (import + test fixes)
- Save API work for when more time

---

## ✅ Success Metrics

**This Week's Goal**: Commercial infrastructure production-ready

**Definition of Done**:
- [ ] API test coverage >80%
- [ ] PostgreSQL integration complete
- [ ] All tests passing (231/231)
- [ ] Docs Phase 2 migrated
- [ ] No critical lint issues
- [ ] Ready for ClemNova deployment

**Current Progress**: ~60% complete (foundation done, need tests + DB)

---

## 🎯 Immediate Recommendation

**For Chris**: 
- Merge PR #157 with admin bypass (it's just formatting)
- Tell Cursor: "Focus on API testing next - that's highest value"

**For Cursor**:
- Read this file (CURSOR_NEXT_FOCUS.md)
- Pull Task 4 (API tests) if high capacity
- OR pull Tasks 1-2 (quick cleanup) if medium capacity
- Create feature branch, implement, test, PR

**Don't**: Chase lint issues or spend hours on formatting. Focus on features!

---

**Ready to shift from cleanup → feature development! 🚀**
