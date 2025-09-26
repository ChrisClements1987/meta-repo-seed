# Pull Request Templates Guide

This directory contains specialized PR templates designed to enforce our commitment to **test-driven development**, **comprehensive documentation**, and **AI context maintenance**.

## 📋 Template Selection Guide

### Default Template
**File:** `../pull_request_template.md`
**Use when:** General changes or unsure which specific template to use

### Feature Template  
**File:** `feature.md`
**Use when:** 
- Adding new functionality
- Implementing user-facing features
- Building new capabilities for Business-in-a-Box platform

**URL:** `?template=feature.md`

### Bug Fix Template
**File:** `bugfix.md`  
**Use when:**
- Fixing reported bugs
- Resolving defects or errors
- Addressing user-reported issues

**URL:** `?template=bugfix.md`

### Documentation Template
**File:** `documentation.md`
**Use when:**
- Adding user guides or tutorials
- Updating architecture documentation  
- Creating developer documentation
- Updating AI context files

**URL:** `?template=documentation.md`

## 🚨 Critical Requirements - ALL Templates

### ✅ **Test-Driven Development (TDD)**
Every PR must demonstrate the test-fail-pass-refactor cycle:
1. **Tests written FIRST** - Before any implementation code
2. **Evidence provided** - Show failing tests, then passing tests  
3. **Coverage maintained** - No reduction in test coverage
4. **TDD compliance confirmed** - Explicit confirmation TDD was followed

### 📚 **Documentation Updates**
Every PR must update relevant documentation:
1. **User documentation** - Guides, README, examples
2. **Developer documentation** - Architecture, APIs, code comments
3. **Project documentation** - Roadmap, changelog, migration guides
4. **AI context files** - AGENTS.md, patterns, decision rationale

### 🤖 **AI Context Maintenance**
Every PR must maintain AI assistance context:
1. **AGENTS.md updates** - New patterns, workflows, decisions
2. **Context preservation** - Ensure AI can understand changes
3. **Pattern documentation** - How AI should approach similar work
4. **Integration guidance** - How changes fit with existing AI context

## 🎯 Business-in-a-Box Alignment

All PRs must demonstrate alignment with our core mission:
- **Target market served** - Startups, charities, non-profits, SMBs
- **Complexity reduction** - Makes business operations easier
- **Professional standards** - Maintains enterprise-grade quality
- **Self-governing systems** - Preserves automated compliance

## 🔧 How to Use Templates

### Method 1: URL Parameter
Add `?template=template-name.md` to your PR creation URL:
```
https://github.com/ChrisClements1987/meta-repo-seed/compare/develop...feature-branch?template=feature.md
```

### Method 2: GitHub CLI
```bash
gh pr create --template .github/PULL_REQUEST_TEMPLATE/feature.md
```

### Method 3: Manual Selection
When creating PR through GitHub interface, select template from dropdown.

## 🚫 Merge Blockers

**No PR will be merged without:**
1. ✅ **TDD Evidence** - Proof of test-first development
2. ✅ **Documentation Complete** - All relevant docs updated
3. ✅ **AI Context Current** - Context files maintained
4. ✅ **Quality Standards Met** - Code quality and review complete
5. ✅ **Business Alignment** - Serves Business-in-a-Box mission

## 📊 Template Effectiveness

These templates are designed to prevent:
- ❌ **Implementation without tests** (TDD violations)
- ❌ **Outdated documentation** (Forced doc updates)
- ❌ **Lost AI context** (Mandatory context maintenance)
- ❌ **Feature creep** (Business alignment requirement)
- ❌ **Technical debt** (Quality gate enforcement)

## 🔄 Template Evolution

Templates will evolve based on:
- **Team feedback** - What works, what doesn't
- **Quality metrics** - Measuring effectiveness
- **Process improvements** - Continuous enhancement
- **AI assistance needs** - Better AI context maintenance

---

**Remember:** These templates are quality gates, not bureaucracy. They ensure we maintain the high standards our Business-in-a-Box platform requires while preserving our test-driven, documentation-first, AI-assisted development culture.