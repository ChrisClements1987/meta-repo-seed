# Systematic Issue Development Workflow

## 🎯 Overview

This document defines the **mandatory workflow for all issue development** to ensure professional standards, test-driven development, and comprehensive documentation maintenance for Business-in-a-Box infrastructure.

## 📋 **MANDATORY: Pre-Work Checklist**

Before starting ANY issue, complete these steps:

### ✅ **1. Environment Preparation**
```bash
# Update local develop branch
git checkout develop
git pull origin develop

# Create appropriate feature branch
git checkout -b [type]/issue-[number]-[description]
# Examples:
# git checkout -b feat/issue-97-infrastructure-as-code
# git checkout -b fix/issue-92-test-coverage-improvement  
# git checkout -b docs/issue-83-readme-cleanup
```

### ✅ **2. Issue Analysis and Planning**
- [ ] **Read issue completely** and understand acceptance criteria
- [ ] **Identify affected components** (code, docs, tests, guides)
- [ ] **Plan test-first approach** (if applicable)
- [ ] **Note AI context impacts** (AGENTS.md, patterns, workflows)

### ✅ **3. Pre-Work Validation**
```bash
# Verify clean starting state
python -m pytest  # All tests should pass
python seeding.py --dry-run --verbose  # Core functionality works
git status  # Clean working tree
```

---

## 🧪 **MANDATORY: Test-Driven Development Steps**

For ANY issue involving code changes, follow this exact sequence:

### **Step 1: Write Failing Tests FIRST**
```bash
# Create test file if needed
touch tests/unit/test_[component].py
# OR
touch tests/integration/test_[workflow].py

# Write tests that FAIL initially
python -m pytest tests/[new_test_file].py -v
# Expected: Tests fail because feature not implemented
```

### **Step 2: Verify Test Failure**
```bash
# Document failing test output
python -m pytest tests/[new_test_file].py -v > test-failure-evidence.txt

# Commit failing tests
git add tests/
git commit -m "test: Add failing tests for issue #[number] - [description]

Tests written before implementation to follow TDD approach.
Expected to fail until implementation is complete."
```

### **Step 3: Implement Minimum Code**
```bash
# Implement ONLY enough code to make tests pass
# No more, no less - follow TDD discipline

# Verify tests now pass
python -m pytest tests/[new_test_file].py -v
```

### **Step 4: Refactor and Improve**
```bash
# Improve implementation while keeping tests green
# Add error handling, edge cases, documentation

# Run full test suite to ensure no regressions
python -m pytest
```

---

## 📚 **MANDATORY: Documentation and Guide Updates**

### **For ANY UX/User-Facing Changes**

#### **Update User Guides**
- [ ] **README.md** - If commands, installation, or basic usage changed
- [ ] **docs/development/onboarding.md** - If developer setup changed
- [ ] **docs/guides/[relevant-guide].md** - If workflows or procedures changed
- [ ] **docs/reference/cli.md** - If CLI commands or options changed

#### **Create New Documentation If Needed**
```bash
# For significant features
touch docs/guides/[feature-name].md

# For new workflows  
touch docs/development/[workflow-name].md

# For architecture changes
touch docs/architecture/adr/[number]-[decision].md
```

### **For Infrastructure/Automation Changes**

#### **Update System Documentation**
- [ ] **AGENTS.md** - If new commands, patterns, or workflows added
- [ ] **docs/architecture/[relevant-doc].md** - If system design changed
- [ ] **docs/development/dependency-management.md** - If dependencies changed

---

## 📊 **MANDATORY: Roadmap and Changelog Maintenance**

### **During Development**
```bash
# Update changelog with work in progress
# Add entry to [Unreleased] section
echo "- [WIP] Working on issue #[number]: [description]" >> CHANGELOG.md
```

### **Upon Completion**
```bash
# Update changelog with completion
# Move from [WIP] to proper category (Added/Changed/Fixed)

# Update roadmap if needed
# Mark items complete, adjust priorities based on learnings
```

---

## 🤖 **MANDATORY: AI Context Management**

### **Before Starting Work**
- [ ] **Review AGENTS.md** to understand current AI patterns
- [ ] **Check existing AI context** for similar work
- [ ] **Plan AI context updates** needed for this change

### **During Development**  
- [ ] **Document new patterns** as they emerge
- [ ] **Note decision rationale** for future AI understanding
- [ ] **Update command examples** if procedures change

### **After Completion**
- [ ] **Update AGENTS.md** with new patterns, commands, or workflows
- [ ] **Document integration points** and how changes fit with existing context
- [ ] **Add examples** of new functionality for AI reference

---

## 🔍 **Issue-Specific Workflows**

### **For Code Enhancement Issues**
```bash
# 1. Pre-work checklist ✅
# 2. Write failing tests ✅
# 3. Implement feature ✅
# 4. Update AGENTS.md with new patterns ✅
# 5. Update relevant user guides ✅
# 6. Update changelog ✅
```

### **For Documentation Issues**
```bash
# 1. Pre-work checklist ✅
# 2. Update/create documentation ✅
# 3. Verify all links work ✅
# 4. Update navigation/cross-references ✅
# 5. Update changelog ✅
# 6. No AI context update needed (mark N/A)
```

### **For Infrastructure Issues**  
```bash
# 1. Pre-work checklist ✅
# 2. Write infrastructure tests ✅
# 3. Implement infrastructure code ✅
# 4. Update deployment guides ✅
# 5. Update AGENTS.md with new commands ✅
# 6. Update roadmap with infrastructure progress ✅
```

### **For Research/Analysis Issues**
```bash
# 1. Pre-work checklist ✅
# 2. Conduct research and analysis ✅
# 3. Document findings comprehensively ✅
# 4. Create implementation recommendations ✅
# 5. Generate follow-up issues if needed ✅
# 6. Update roadmap with research outcomes ✅
```

---

## ✅ **MANDATORY: Completion Checklist**

Before closing ANY issue, verify:

### **Code Quality**
- [ ] All tests pass (including new tests)
- [ ] Code follows project standards (linting, formatting)
- [ ] No regressions introduced
- [ ] Performance impact assessed

### **Documentation**
- [ ] All relevant documentation updated
- [ ] New documentation created if needed
- [ ] Links verified and working
- [ ] Cross-references updated

### **AI Context**
- [ ] AGENTS.md updated with new patterns (or marked N/A)
- [ ] Examples provided for new functionality
- [ ] Integration guidance documented

### **Project Management**
- [ ] Changelog updated with completion
- [ ] Roadmap updated if priorities changed
- [ ] Related issues linked or updated
- [ ] Milestone progress tracked

### **Business-in-a-Box Alignment**
- [ ] Changes serve 10-minute deployment goal
- [ ] Professional standards maintained
- [ ] Self-governing systems preserved/enhanced
- [ ] Target market needs addressed

---

## 🚨 **CRITICAL: Issue Template Updates Required**

All existing and future issues need **explicit TDD requirements** in acceptance criteria. Let me update current high-priority issues.

---

**This workflow ensures every issue delivers professional value aligned with Business-in-a-Box mission while maintaining comprehensive quality standards.**
