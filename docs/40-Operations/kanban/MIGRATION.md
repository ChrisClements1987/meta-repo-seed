# Kanban to GitHub Issues Migration Playbook

**Status**: Active
**Duration**: 10-15 minutes
**Purpose**: Migrate from file-based Kanban to GitHub Issues as single source of truth

---

## 🎯 Migration Goals

1. **GitHub Issues** becomes single source of truth for all work items
2. **Structured labels** (`type:`, `priority:`, `area:`, `status:`) for consistent tracking
3. **Zero data loss** - all valuable items ("gold") migrated
4. **UNIFIED_KANBAN_BOARD.md** deprecated with historical reference

---

## ✅ Migration Checklist

### Phase 1: Pre-Migration (Completed)
- [x] Create structured label taxonomy in GitHub
- [x] Create missing type labels (`type: testing`, `type: ci-cd`, `type: security`, etc.)
- [x] Create area labels (`area: api`, `area: backend`, `area: tooling`)
- [x] Update documentation with new label structure

### Phase 2: Issue Migration (Completed)
- [x] Identify "gold" items from Kanban not in GitHub Issues
- [x] De-duplicate against existing GitHub issues
- [x] Create GitHub issues for all valuable Kanban items:
  - [x] #165 - Fix OrganizationSeeder NoneType error (Bug, P-high)
  - [x] #161 - Add API endpoint tests (Testing, P-high)
  - [x] #163 - Process hardening implementation (Process, In Progress)
  - [x] #160 - Customer onboarding workflow (Feature, P-medium)
  - [x] #162 - Security testing with OWASP ZAP (Testing/Security, P-medium)
  - [x] #164 - Re-enable flake8 linting (Tech Debt, P-medium)

### Phase 3: Documentation Updates (Completed)
- [x] Update `issue-management.md` with new types and label structure
- [x] Update `work-item-template.md` with comprehensive types
- [x] Create this `MIGRATION.md` playbook
- [ ] Deprecate `UNIFIED_KANBAN_BOARD.md` with banner
- [ ] Update `CURSOR_COMPLETION_GUIDE.md` to reflect completed work

---

## 📋 Migration Process

### For Each Kanban Item

1. **Search GitHub Issues** by title keywords and type
   ```bash
   gh issue list --search "keyword in:title" --limit 10
   ```

2. **If Not Found**, create using Work Item Template:
   ```bash
   gh issue create \
     --title "[TYPE] Description" \
     --body "..." \
     --label "type: [type],priority: [level],area: [relevant]"
   ```

3. **Set Correct Labels**:
   - **Required**: `type:` and `priority:`
   - **Recommended**: `area:` for filtering
   - **Optional**: `status:` if in progress or blocked

4. **Link Related Items**:
   - Reference parent epic if applicable
   - Link to related issues or PRs
   - Add to project board if using GitHub Projects

5. **Mark as Completed** in Kanban with link to GitHub Issue

---

## 🏷️ Label Migration Mapping

### Type Labels
| Kanban Category | GitHub Label | Example |
|----------------|--------------|---------|
| Bug | `type: bug` | #165 OrganizationSeeder |
| Feature | `type: feature` | #160 Customer onboarding |
| Testing Task | `type: testing` | #161 API tests |
| Tech Debt | `type: tech-debt` | #164 flake8 linting |
| Process Improvement | `type: process` | #163 Process hardening |
| Documentation | `type: docs` | Documentation tasks |
| CI/CD | `type: ci-cd` | Pipeline work |
| Security | `type: security` | #162 OWASP ZAP |
| Infrastructure | `type: infra` | DevOps tasks |

### Priority Mapping
| Kanban Score | Priority Label | Rationale |
|-------------|----------------|-----------|
| 8-10 | `priority: high` | Blocking work, critical bugs |
| 5-7 | `priority: medium` | Important features, non-blocking |
| 1-4 | `priority: low` | Nice-to-have, minor improvements |

---

## 🚀 Quick Commands

### Search for Existing Issue
```bash
gh issue list --search "OrganizationSeeder in:title" --limit 5
```

### Create New Issue with Labels
```bash
gh issue create \
  --title "fix: Description of bug" \
  --body "## Description\n...\n\n## Acceptance Criteria\n- [ ] ..." \
  --label "type: bug,priority: high,area: backend"
```

### List All Issues by Type
```bash
gh issue list --label "type: testing" --limit 20
gh issue list --label "priority: high" --limit 20
gh issue list --label "area: api" --limit 20
```

### Update Issue Labels
```bash
gh issue edit 165 --add-label "area: backend"
gh issue edit 165 --remove-label "enhancement"
```

---

## 🎯 Post-Migration Actions

### Immediate (After All Issues Migrated)
1. Add deprecation banner to `UNIFIED_KANBAN_BOARD.md`
2. Update `CURSOR_COMPLETION_GUIDE.md` to reflect completed commercial work
3. Verify all valuable items exist in GitHub Issues
4. Remove or archive Kanban file after confirmation

### Within 1 Week
1. Train team on structured label usage
2. Create saved GitHub searches/filters for common queries
3. Set up GitHub Projects board if needed for visualization
4. Document any lessons learned

### Within 1 Month
1. Review label usage and adjust taxonomy if needed
2. Close any stale or duplicate issues
3. Ensure all team members using GitHub Issues consistently
4. Remove legacy labels if fully migrated

---

## 📊 Success Metrics

- [ ] All Kanban "gold" items exist in GitHub Issues
- [ ] All new issues use structured labels (`type:`, `priority:`, `area:`)
- [ ] Team using GitHub Issues as primary backlog
- [ ] UNIFIED_KANBAN_BOARD.md marked as deprecated
- [ ] Zero valuable work items lost in migration

---

## 🔗 References

- [Issue Management Guide](../development/issue-management.md)
- [Work Item Template](../procedures/work-item-template.md)
- [GitHub Issues](https://github.com/ChrisClements1987/meta-repo-seed/issues)

---

**Migration Completed**: 2025-10-17
**Migrated By**: Amp AI Assistant
**Verified By**: [Pending]
