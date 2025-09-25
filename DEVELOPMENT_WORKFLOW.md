# Development Workflow Guide

## 🔄 Git Branching Strategy

### Branch Structure
- **`main`** - Production-ready releases only
- **`develop`** - Integration branch for all development work  
- **`feature/*`** - Individual feature/fix branches
- **`sprint-*/*`** - Sprint-specific feature branches

### Workflow Process

#### 1. Start New Work - ALWAYS sync develop with main first
```bash
git checkout develop
git pull origin main          # Sync develop with latest main
git push origin develop       # Update remote develop
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

#### 3. Sprint Completion - Create Release PR
```bash
# After sprint features are merged into develop
gh pr create --head develop --base main --title "🚀 Release v2.x.x: ..." --body "..."
```

#### 4. Post-Release - Sync develop with main
```bash
git checkout develop  
git pull origin main          # Sync develop with merged release
git push origin develop       # Keep develop current
```

## ⚠️ Critical Rules

### ❌ **NEVER DO:**
- Target `main` directly with feature PRs
- Work on develop without syncing with main first
- Merge develop→main without proper release PR
- Skip the sync step before new development

### ✅ **ALWAYS DO:**
- Sync develop with main before starting new work
- Target `develop` with all feature/fix PRs
- Create proper release PRs from develop→main
- Review and test release PRs thoroughly

## 📋 Current Status

### Active PRs (targeting develop ✅)
- **PR #60** - Sprint 1 Technical Debt → **develop** ✅
- **PR #61** - Sprint 1 Testing Infrastructure → **develop** ✅

### Release PR (develop→main)
- **PR #62** - Release v2.1.0 → **main** ✅

### Next Steps
1. **Merge feature PRs** into develop
2. **Review release PR** for production deployment  
3. **After merge**: Sync develop with main before Sprint 2
4. **Continue Sprint 2** with proper branch management

---

*This workflow ensures clean releases and prevents merge conflicts.*
