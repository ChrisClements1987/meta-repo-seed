# Hotfix Workflow for Production Emergencies

**Last Updated:** 2025-09-30  
**Version:** 1.0  
**Authority:** Emergency Production Response Protocol

## ⚠️ IMPORTANT WARNING

**Hotfixes bypass normal quality gates and development workflow.** They are for genuine production emergencies only. Misuse undermines code quality and team processes.

## 🚨 Emergency Criteria

### Use Hotfix Process When:
- **Production deployment completely fails** - New deployments impossible for all users
- **Security vulnerability actively exploited** - Active security breach in progress
- **Data loss or corruption occurring** - User/business data being damaged or lost
- **Critical business function broken for all users** - Core functionality completely unavailable
- **Financial/legal/compliance emergency** - Legal violation or financial system failure

### Use Regular Process When:
- Bug affects only some users or specific scenarios
- Workaround exists and is communicated to users
- Impact is moderate or low severity
- Issue can wait for next regular release (days, not hours)
- Performance degradation (unless severe)
- UI/UX issues (unless blocking core functionality)

## 🚀 Hotfix Workflow

### Step 1: Incident Declaration
**Immediate Actions:**
1. **Assess severity** using criteria above
2. **Declare incident** in team communication
3. **Assign incident commander** (typically person discovering issue)
4. **Estimate impact and ETA** for resolution

**Communication Template:**
```
🚨 HOTFIX IN PROGRESS
Issue: [Brief description of problem]
Impact: [Who/what is affected]
Severity: [Production down/Security breach/Data loss/etc.]
ETA: [Realistic time estimate]
Owner: @[incident-commander]
Branch: hotfix/[version]-[brief-description]
Status: [INVESTIGATING/FIXING/TESTING/DEPLOYING]
```

### Step 2: Create Hotfix Branch
```bash
# Start from production state
git checkout main
git pull origin main

# Create hotfix branch with clear naming
git checkout -b hotfix/v1.2.1-[brief-description]
git push -u origin hotfix/v1.2.1-[brief-description]
```

**Branch Naming Convention:**
- `hotfix/v1.2.1-security-vulnerability-fix`
- `hotfix/v1.2.1-deployment-failure-fix`
- `hotfix/v1.2.1-data-corruption-prevention`

### Step 3: Implement Minimal Fix
**Principles:**
- **Minimal scope** - Fix only the immediate issue
- **No scope creep** - Resist urge to improve or refactor
- **Include test** - Add test that would have caught the issue
- **Document thoroughly** - Clear commit messages explaining urgency

**Hotfix Commit Template:**
```bash
git commit -m "hotfix([scope]): [brief description]

EMERGENCY FIX: [Detailed explanation of issue]
Root Cause: [What caused the problem]
Impact: [Who/what was affected]
Solution: [What the fix does]

Restores: [Specific functionality restored]
Urgency: [Why this couldn't wait for regular process]

Incident: #[incident-tracking-number]"
```

### Step 4: Expedited Testing
**Required Testing:**
- [ ] All existing tests must pass
- [ ] New test demonstrates fix works
- [ ] Manual validation on staging environment (if time permits)
- [ ] Smoke test of core functionality

**Time Constraints:**
- Maximum 30 minutes for testing critical fixes
- Focus on safety over comprehensive testing
- Document what testing was skipped due to urgency

### Step 5: Emergency Review Process
**Review Requirements:**
- **1 approval required** from available senior developer
- **Review focus:** Fix effectiveness and safety, not perfection
- **Time limit:** 1-2 hours maximum for critical fixes
- **Bypass option:** Incident commander can deploy without review if:
  - No reviewer available within 2 hours
  - Production completely down
  - Security actively being exploited

**Reviewer Checklist:**
- [ ] Fix addresses the specific emergency issue
- [ ] No obvious security vulnerabilities introduced
- [ ] Minimal scope maintained (no unnecessary changes)
- [ ] Clear rollback plan if fix fails
- [ ] Tests demonstrate fix works

### Step 6: Emergency Deployment
```bash
# Merge to main with no-fast-forward to preserve hotfix history
git checkout main
git merge --no-ff hotfix/v1.2.1-[description]
git push origin main

# Tag immediately for version tracking
git tag -a v1.2.1 -m "Hotfix v1.2.1: [Brief description]

Emergency fix for: [Issue description]
Impact: [What was restored]
Deployed: $(date)
Incident: #[incident-number]"

git push origin v1.2.1
```

**Deployment Validation:**
- [ ] Verify fix resolves the reported issue
- [ ] Confirm core functionality works
- [ ] Monitor for 30 minutes post-deployment
- [ ] Update incident status to RESOLVED

### Step 7: Sync with Development Branches
```bash
# Merge hotfix back to develop
git checkout develop
git pull origin develop
git merge --no-ff hotfix/v1.2.1-[description]
git push origin develop

# If active release branch exists, merge there too
git checkout release/v1.3.0  # if exists
git merge --no-ff hotfix/v1.2.1-[description]
git push origin release/v1.3.0

# Clean up hotfix branch
git branch -d hotfix/v1.2.1-[description]
git push origin --delete hotfix/v1.2.1-[description]
```

### Step 8: Post-Incident Activities
**Immediate (Within 24 hours):**
- [ ] Update incident status to CLOSED
- [ ] Communicate resolution to stakeholders
- [ ] Document lessons learned
- [ ] Schedule post-incident review

**Post-Incident Review (Within 1 week):**
- [ ] Root cause analysis
- [ ] Process improvement recommendations
- [ ] Prevention measures for future
- [ ] Update monitoring/alerting if needed

## 📋 Incident Communication Templates

### Initial Incident Declaration
```
🚨 PRODUCTION INCIDENT DECLARED
Severity: [CRITICAL/HIGH/MEDIUM]
Issue: [Brief description]
Impact: [Affected users/systems]
Status: INVESTIGATING
ETA: [Initial estimate]
Commander: @[name]
Updates: Every 30 minutes or on status change
```

### Status Update Template
```
🔄 INCIDENT UPDATE - [TIMESTAMP]
Status: [INVESTIGATING/FIXING/TESTING/DEPLOYING/MONITORING]
Progress: [What's been done]
Next: [What's happening next]
ETA: [Updated estimate]
Issues: [Any blockers or complications]
```

### Resolution Communication
```
✅ INCIDENT RESOLVED - [TIMESTAMP]
Issue: [Brief description]
Duration: [Total incident time]
Resolution: [What fixed it]
Impact: [Final impact assessment]
Follow-up: Post-incident review scheduled for [date]
```

## 🛡️ GitHub Integration

### Branch Protection Bypass
For genuine emergencies, repository administrators can:
1. **Temporarily disable** required status checks
2. **Use admin bypass** to merge without reviews
3. **Document bypass usage** in PR description

**Emergency Bypass Template:**
```markdown
## 🚨 EMERGENCY BYPASS JUSTIFICATION

**Incident:** [Link to incident tracking]
**Bypass Reason:** [Why normal process couldn't be followed]
**Risk Assessment:** [What risks are accepted]
**Post-Incident Actions:** [How to address bypassed checks]
**Authorized By:** [Incident commander name]
**Timestamp:** [When bypass was used]
```

### PR Template for Hotfixes
```markdown
## 🚨 HOTFIX - EMERGENCY DEPLOYMENT

**Incident Reference:** #[incident-number]
**Severity:** [CRITICAL/HIGH]
**Emergency Justification:** [Why this couldn't wait]

### Issue Description
[Detailed description of production issue]

### Fix Implementation
[What the fix does and why it works]

### Testing Performed
- [ ] Existing tests pass
- [ ] New test validates fix
- [ ] Manual validation: [describe what was tested]
- [ ] Staging validation: [Y/N with justification]

### Risk Assessment
**Risks Accepted:** [What normal processes were bypassed]
**Rollback Plan:** [How to revert if fix fails]
**Monitoring Plan:** [How success will be verified]

### Post-Deployment Actions
- [ ] Monitor production for 30 minutes
- [ ] Verify issue resolution
- [ ] Schedule post-incident review
- [ ] Address any bypassed quality checks
```

## 🔍 Post-Incident Review Process

### Review Objectives
1. **Root Cause Analysis** - Why did the incident occur?
2. **Response Evaluation** - How well did our process work?
3. **Prevention Planning** - How can we prevent recurrence?
4. **Process Improvement** - What should we change?

### Review Template
```markdown
# Post-Incident Review: [Incident Description]

## Incident Summary
- **Date/Time:** [When incident occurred]
- **Duration:** [Total incident duration]
- **Impact:** [Who/what was affected]
- **Resolution:** [How it was resolved]

## Timeline
- [Time] - Issue first detected
- [Time] - Incident declared
- [Time] - Fix implemented
- [Time] - Resolution deployed
- [Time] - Issue confirmed resolved

## Root Cause Analysis
**Primary Cause:** [Main reason incident occurred]
**Contributing Factors:** [Secondary factors]
**Why Weren't We Protected:** [Why didn't existing measures prevent this]

## Response Evaluation
**What Went Well:**
- [Process successes]

**What Could Improve:**
- [Process gaps or delays]

## Prevention Measures
**Immediate Actions:** [What to implement right away]
**Long-term Improvements:** [Larger changes needed]
**Monitoring Enhancements:** [Better detection needed]

## Action Items
- [ ] [Action item 1] - Owner: [Name] - Due: [Date]
- [ ] [Action item 2] - Owner: [Name] - Due: [Date]
```

## 📊 Hotfix Metrics and Monitoring

### Success Metrics
- **Time to Resolution** - From detection to fix deployed
- **Impact Duration** - How long users were affected
- **Quality Escapes** - Whether hotfix introduced new issues
- **Process Adherence** - How well we followed emergency procedures

### Warning Signs (Review Process if These Occur)
- **Frequent hotfixes** (>1 per month) - May indicate process issues
- **Hotfix-induced issues** - Emergency fixes causing new problems
- **Long resolution times** - Process may be too cumbersome
- **Scope creep** - Hotfixes including non-emergency changes

## 🚧 Governance and Accountability

### Authorization Levels
**Can Declare Incidents:** Any team member detecting genuine emergency
**Can Authorize Bypass:** Repository administrators only
**Can Deploy Hotfixes:** Incident commander + reviewer (or commander alone in extreme emergencies)

### Audit Trail Requirements
All hotfixes must include:
- [ ] Clear incident documentation
- [ ] Justification for emergency process
- [ ] Testing evidence (even if limited)
- [ ] Post-incident review completion

### Misuse Consequences
**Inappropriate hotfix usage includes:**
- Using hotfix process for non-emergency issues
- Including scope beyond the immediate fix
- Skipping post-incident review
- Bypassing review without genuine emergency

**Response to misuse:**
1. Process education and coaching
2. Review and improve emergency criteria
3. Consider additional approval requirements

## 🎯 Summary

This hotfix workflow balances **speed for genuine emergencies** with **quality and process integrity**. Key principles:

- **Clear criteria** for when to use emergency process
- **Minimal scope** to reduce risk of new issues  
- **Rapid but safe** deployment with essential checks
- **Complete documentation** for learning and accountability
- **Post-incident review** to improve prevention

**Remember:** Hotfixes are for genuine production emergencies only. When in doubt, use the regular development process.
