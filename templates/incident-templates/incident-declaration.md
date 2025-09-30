# Production Incident Declaration Template

Copy and paste this template into your team communication channel when declaring a hotfix incident:

```
🚨 HOTFIX IN PROGRESS
Issue: [Brief description of the problem]
Impact: [Who/what is affected - e.g., "All new user deployments blocked"]
Severity: [CRITICAL/HIGH - use criteria from hotfix-workflow.md]
ETA: [Realistic time estimate for resolution]
Owner: @[incident-commander-github-handle]
Branch: hotfix/v[version]-[brief-description]
Status: [INVESTIGATING/FIXING/TESTING/DEPLOYING]

Updates: Will provide updates every 30 minutes or on status change
Documentation: Following docs/operations/hotfix-workflow.md
```

## Status Update Template

Use this for periodic updates during the incident:

```
🔄 INCIDENT UPDATE - [HH:MM timestamp]
Status: [INVESTIGATING/FIXING/TESTING/DEPLOYING/MONITORING]
Progress: [What has been completed]
Next: [What is happening next]
ETA: [Updated time estimate if changed]
Issues: [Any blockers or complications encountered]
```

## Resolution Template

Use this when the incident is resolved:

```
✅ INCIDENT RESOLVED - [HH:MM timestamp]
Issue: [Brief description of what was fixed]
Duration: [Total incident time from declaration to resolution]
Resolution: [What fixed the issue]
Impact: [Final assessment of who/what was affected]
Follow-up: Post-incident review scheduled for [date within 1 week]
```

## Example Usage

```
🚨 HOTFIX IN PROGRESS
Issue: Business deployment CLI failing with template processing error
Impact: All new startup deployments failing - affects new user onboarding
Severity: CRITICAL
ETA: 2 hours
Owner: @developer
Branch: hotfix/v1.2.1-startup-template-fix
Status: INVESTIGATING

Updates: Will provide updates every 30 minutes or on status change
Documentation: Following docs/operations/hotfix-workflow.md
```
