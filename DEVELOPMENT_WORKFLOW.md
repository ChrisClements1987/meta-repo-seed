# Development Workflow Guide

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

## ⚠️ Critical Rules

### ❌ **NEVER DO:**
- Target `main` directly with feature PRs
- Sync develop with main regularly (destroys other devs' work)
- Merge develop→main without UAT and quality verification
- Work directly on develop branch

### ✅ **ALWAYS DO:**
- Branch from latest `develop` for all new work
- Target `develop` with all feature/fix PRs  
- Test features thoroughly before merging to develop
- Create release PRs develop→main only after UAT
- Let develop accumulate features independently from main

## 📋 Current Status

### Active PRs (targeting develop ✅)
- **PR #60** - Sprint 1 Technical Debt → **develop** ✅
- **PR #61** - Sprint 1 Testing Infrastructure → **develop** ✅

### Release PR (develop→main)
- **PR #62** - Release v2.1.0 → **main** ✅

### Next Steps
1. **Merge Sprint 1 PRs** into develop (#60, #61)
2. **Review release PR** for production deployment (#62)
3. **After release**: Continue Sprint 2 from develop (no sync needed)
4. **Future releases**: develop→main only when ready for production

---

*This workflow ensures clean releases and prevents merge conflicts.*
