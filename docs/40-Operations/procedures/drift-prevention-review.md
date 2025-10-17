# Drift Prevention Review Checkpoint

**Review Schedule**: Every 2 weeks (starting 2025-10-31)
**Duration**: 15-30 minutes
**Purpose**: Evaluate if incremental guardrails prevent work drift, or if stronger enforcement needed

---

## 🎯 Review Objectives

Determine if current drift-prevention measures are sufficient:
1. All work traces to GitHub Issues
2. No ad-hoc branches or PRs
3. Multi-agent coordination effective
4. Minimal process friction

If measures fail, escalate to advanced orchestration (policy engine, containerized agents, etc.)

---

## 📊 Success Metrics

### ✅ Passing Criteria (Keep Current Approach)
- **100%** of branches follow `feature/issue-{number}-*` convention
- **100%** of PRs reference GitHub Issues with auto-close keywords
- **0** ad-hoc work items discovered in retrospective
- **<2** branch naming violations caught by pre-commit hook per week
- **0** work duplication incidents between agents
- Team reports **low friction** with process

### ⚠️ Warning Signs (Monitor Closely)
- **80-99%** branch/PR compliance
- **1-2** ad-hoc work items per 2-week period
- **2-5** branch naming violations per week
- Team reports **moderate friction**
- **1** work duplication incident

### ❌ Failing Criteria (Escalate to Advanced Orchestration)
- **<80%** branch/PR compliance
- **3+** ad-hoc work items per 2-week period
- **>5** branch naming violations per week (hooks ignored/bypassed)
- **2+** work duplication incidents
- Team reports **high friction** or actively bypassing checks
- Evidence of coordination failures between AI agents

---

## 🔍 Review Checklist

### 1. Branch Compliance Audit
```bash
# List all branches and check naming
git branch -a | grep -v "main\|develop" | grep -v "feature/issue-\|bugfix/issue-\|hotfix/"

# Expected: Empty output or only legacy branches
# If non-compliant branches exist, investigate
```

### 2. PR Issue Reference Audit
```bash
# Check recent PRs for issue references
gh pr list --state merged --limit 20 --json number,title,body \
  | jq '.[] | select(.body | test("(close[sd]?|fix(e[sd])?|resolve[sd]?)\\s+#\\d+"; "i") | not) | {number, title}'

# Expected: Empty output
# If PRs without issue references exist, investigate
```

### 3. GitHub Issues Backlog Health
```bash
# Check for issues with proper labels
gh issue list --limit 50 --json number,labels \
  | jq '[.[] | select((.labels | map(.name) | any(startswith("type:"))) and (.labels | map(.name) | any(startswith("priority:"))))] | length'

# Expected: Most issues have type: and priority: labels
```

### 4. Work Duplication Check
- Review closed issues and PRs for overlapping scope
- Check for multiple agents working on same area without coordination
- Identify any rework or throwaway commits

### 5. Hook Effectiveness Check
```bash
# Check git log for commits bypassing hooks (if logs available)
git log --all --oneline --since="2 weeks ago" | wc -l

# Manually sample recent commits to verify TDD cycle followed
```

### 6. Team Friction Assessment
- Review agent/human feedback on process
- Check for complaints about blocked work or bureaucracy
- Assess time spent on process vs. actual development

---

## 📝 Review Template

```markdown
## Drift Prevention Review - [DATE]

### Metrics
- Branch compliance: ___%
- PR issue reference compliance: ___%
- Ad-hoc work items discovered: ___
- Hook violations: ___/week
- Work duplication incidents: ___

### Status
[ ] ✅ Passing - Continue current approach
[ ] ⚠️ Warning - Monitor closely, minor adjustments needed
[ ] ❌ Failing - Escalate to advanced orchestration

### Observations
- [Key finding 1]
- [Key finding 2]
- [Key finding 3]

### Actions
- [ ] Action 1
- [ ] Action 2

### Decision
[Keep current approach | Make adjustments | Escalate to orchestrator]

### Next Review
[Date]
```

---

## 🚀 Escalation Path (If Metrics Fail)

If review determines current measures insufficient, implement in phases:

### Phase 1: Enhanced Enforcement (1-2 weeks)
- Add server-side branch protection rules
- Add GitHub Action to auto-close non-compliant PRs
- Add issue template enforcement
- Add stricter commit message validation

### Phase 2: Policy Engine (2-4 weeks)
- Implement Open Policy Agent (OPA)
- Define policy-as-code for workflows
- Add policy violations dashboard
- Automate issue assignment based on capacity

### Phase 3: Agent Orchestrator (4-8 weeks)
- Design orchestrator architecture (per your framework)
- Implement queue-based issue assignment
- Add closed-loop CI remediation
- Containerize agent execution environments

### Phase 4: Full Autonomy (8+ weeks)
- Self-healing CI failures
- Predictive task routing
- Agent performance analytics
- Automated learning from failures

**Decision Point**: At each phase, reassess if ROI justifies next phase investment.

---

## 📅 Review Schedule

| Review Date | Status | Actions | Next Review |
|-------------|--------|---------|-------------|
| 2025-10-31 | [TBD] | [TBD] | 2025-11-14 |
| 2025-11-14 | [TBD] | [TBD] | 2025-11-28 |
| 2025-11-28 | [TBD] | [TBD] | 2025-12-12 |

---

## 🔗 Related Documentation

- [Development Workflow](../development-workflow.md#-work-selection-process)
- [Issue Management Guide](../development/issue-management.md)
- [AGENTS.md](../../../AGENTS.md#git-workflow---required-process)
- [GitHub Issues Backlog](https://github.com/ChrisClements1987/meta-repo-seed/issues)

---

**First Review Date**: 2025-10-31
**Reviewer**: Project Owner + AI Team Lead
**Escalation Contact**: Project Owner
