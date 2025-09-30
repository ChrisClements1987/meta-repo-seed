# Feature Implementation PR

## 🎯 Feature Summary
<!-- Clear description of the feature being implemented -->

**Feature Name:** 
**GitHub Issue:** #[issue-number]
**Business Value:** <!-- How does this serve our Business-in-a-Box vision? -->

---

## 🧪 Test-Driven Development

### ✅ **TDD Evidence** *(Preferred for new features)*
- [ ] **Tests written FIRST** - I wrote failing tests before any implementation
- [ ] **Test-fail-pass-refactor cycle documented** below
- [ ] **Alternative: Comprehensive diff coverage** - >= 90% on new code with justification for non-TDD approach

#### 🔄 TDD Cycle Documentation
```bash
# Step 1: Show failing tests (if TDD approach used)
# Paste output of initial failing test run

# Step 2: Show passing tests after implementation  
# Paste output showing tests now pass

# Step 3: Coverage report
# Paste diff coverage report showing >= 90% coverage on new code
```

### 📊 **Test Coverage Requirements**
- [ ] **Unit tests** - All new functions/classes tested
- [ ] **Integration tests** - Feature works end-to-end
- [ ] **Edge cases** - Error conditions and boundary cases tested
- [ ] **Diff coverage >= 90%** for new features

---

## 📚 Documentation - Required for Features

### ✅ **User Documentation**
- [ ] **Feature guide created** - `docs/guides/[feature-name].md`
- [ ] **README updated** - New feature listed and described
- [ ] **Examples provided** - Real usage examples included
- [ ] **N/A** - Internal/developer-only feature because: _______________

### ✅ **Developer Documentation**  
- [ ] **Architecture documented** - How feature fits into system
- [ ] **API documentation** - If new APIs/interfaces added
- [ ] **Code comments** - Complex logic explained

### ✅ **Project Documentation**
- [ ] **Roadmap updated** - Feature marked complete, next items adjusted
- [ ] **Changelog entry** - User-facing description added
- [ ] **Migration guide** - If breaking changes or user action needed

---

## 🤖 AI Context Updates

### ✅ **AI Files Updated** *(Required if applicable)*
- [ ] **AGENTS.md** - New patterns or workflows documented
- [ ] **Feature patterns** - How AI should understand this feature
- [ ] **Integration points** - How this connects to other systems
- [ ] **N/A** - No new AI patterns introduced because: _______________

---

## 🚀 Business-in-a-Box Alignment

### 🎯 **Target Market Impact**
- [ ] **Startups** - How does this help startups launch faster?
- [ ] **Non-profits** - How does this serve resource-constrained organizations?  
- [ ] **SMBs** - How does this enable business focus over infrastructure?

### ⚡ **Performance Requirements**
- [ ] **10-minute deployment preserved** - Feature doesn't slow core deployment
- [ ] **Self-governing maintained** - Automated quality/compliance preserved
- [ ] **Professional standards** - Enterprise-grade quality maintained

---

## 🔍 Implementation Quality

### ✅ **Code Quality**
- [ ] **Follows project patterns** - Consistent with existing architecture
- [ ] **Error handling** - Graceful error handling implemented
- [ ] **Security reviewed** - No security vulnerabilities introduced
- [ ] **Performance optimized** - Efficient implementation

### ✅ **User Experience**
- [ ] **Intuitive interface** - Easy to discover and use
- [ ] **Clear error messages** - Helpful error guidance provided
- [ ] **Progress indicators** - User knows what's happening

---

## 🔄 Legacy Debt Impact
*Complete if standard requirements cannot be met*

**Legacy Debt Items:**
- [ ] **N/A** - All requirements met
- [ ] **Linked tech debt issue(s)**: #[issue-number]
- [ ] **Risk assessment**: [describe any compromises made]
- [ ] **Follow-up timeline**: [milestone for addressing debt]

---

## 🔀 Development Workflow Compliance

### ✅ **Branch Management** *(Required)*
- [ ] **Started from updated develop branch** - `git checkout develop && git pull origin develop`
- [ ] **Feature branch created** - Named `feature/issue-[number]-description`
- [ ] **Tests written FIRST** - TDD cycle documented above
- [ ] **All commits focused** - Clean, logical commit history

---

**🚫 FEATURE MERGE BLOCKER:** Cannot merge until:
1. ✅ **TDD evidence provided** - Tests written first OR diff coverage >= 90%
2. ✅ **Branch workflow followed** - Proper branch management documented
3. ✅ **Documentation complete** - User docs (if user-facing) and AI context updated
4. ✅ **Business alignment demonstrated** - Serves Business-in-a-Box vision
5. ✅ **Quality checks passed** - All automated tests and linting
6. ✅ **Roadmap/changelog updated** - Project documentation maintained
