# Work Item Template

**Work Item ID**: WI-XXX or GitHub Issue #XXX
**Type**: [Epic | Feature | User Story | Bug | Tech Debt | Testing Task | CI/CD Task | Security Task | Infrastructure Task | Process Improvement | Documentation Task | Analysis | Research Project | Spike | Meeting/Ceremony]
**Created**: YYYY-MM-DD
**Priority Score**: [Calculated: Business Value + Urgency - Effort - Risk]
**Labels**: `type: [type]`, `priority: [level]`, `area: [relevant]`

---

## 📋 Basic Information

### **Title**
[Clear, concise title describing the work]

### **Description**
[Detailed description of what needs to be done]

### **Acceptance Criteria**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

### **Definition of Done**
- [ ] Code implemented and tested
- [ ] Tests pass with 90%+ coverage
- [ ] Documentation updated
- [ ] Code reviewed (if applicable)
- [ ] Deployed to staging (if applicable)

---

## 🎯 Prioritization

### **Business Value** (1-5)
- **5**: Critical for business success
- **4**: High business impact
- **3**: Moderate business value
- **2**: Low business impact
- **1**: Minimal business value

**Score**: [1-5]
**Rationale**: [Why this score?]

### **Effort** (1-5)
- **5**: Very high effort (weeks)
- **4**: High effort (days)
- **3**: Medium effort (hours)
- **2**: Low effort (minutes to hours)
- **1**: Minimal effort (minutes)

**Score**: [1-5]
**Estimate**: [Time estimate: e.g., "2 hours", "1 day", "3 weeks"]

### **Urgency** (1-5)
- **5**: Critical - blocking other work
- **4**: High - needed soon
- **3**: Medium - can wait
- **2**: Low - nice to have
- **1**: Minimal - whenever

**Score**: [1-5]
**Deadline**: [If applicable]

### **Risk** (1-5)
- **5**: High risk - could break things
- **4**: Medium-high risk
- **3**: Medium risk
- **2**: Low risk
- **1**: Minimal risk

**Score**: [1-5]
**Risk Description**: [What are the risks?]

### **Priority Score Calculation**
**Formula**: Business Value + Urgency - Effort - Risk
**Score**: [Calculated number]
**Rank**: [Where this fits in priority order]

---

## 🔗 Dependencies & Relationships

### **Dependencies**
- **Blocks**: [What work items does this block?]
- **Blocked By**: [What work items block this?]
- **Depends On**: [What work items must be completed first?]

### **Related Work Items**
- **Parent**: [Epic or larger work item]
- **Children**: [Sub-tasks or smaller work items]
- **Related**: [Other related work items]

---

## 📊 Work Item Type Specifics

### **Epic**
- **Business Objective**: [What business goal does this achieve?]
- **Success Metrics**: [How will we measure success?]
- **Timeline**: [Expected completion date]

### **Feature**
- **User Value**: [What value does this provide to users?]
- **User Stories**: [List of user stories included]
- **Technical Requirements**: [Technical specifications]

### **User Story**
- **As a**: [User type]
- **I want**: [Desired functionality]
- **So that**: [Business value/benefit]
- **Story Points**: [Effort estimate]

### **Tech Debt**
- **Debt Type**: [Code Quality | Performance | Security | Maintainability]
- **Impact**: [What problems does this debt cause?]
- **Refactoring Scope**: [What needs to be refactored?]

### **Bug**
- **Severity**: [Critical | High | Medium | Low]
- **Priority**: [P0 | P1 | P2 | P3]
- **Environment**: [Production | Staging | Development]
- **Steps to Reproduce**: [How to reproduce the bug]

### **Infrastructure Task**
- **Infrastructure Type**: [DevOps | Deployment | Monitoring | Security]
- **Environment**: [Production | Staging | Development]
- **Dependencies**: [System dependencies]

### **Process Improvement**
- **Current Process**: [What process needs improvement?]
- **Proposed Process**: [What is the improved process?]
- **Expected Benefits**: [What improvements will this bring?]

### **Documentation Task**
- **Documentation Type**: [User Docs | Dev Docs | Architecture | API]
- **Audience**: [Who is the target audience?]
- **Format**: [Markdown | PDF | Wiki | etc.]

### **Testing Task**
- **Test Type**: [Unit | Integration | E2E | Performance | Security]
- **Scope**: [What needs to be tested?]
- **Automation**: [Manual | Automated | Semi-automated]

### **CI/CD Task**
- **Pipeline Type**: [Build | Test | Deploy | Release]
- **Scope**: [What pipeline or automation needs work?]
- **Dependencies**: [Required tools or services]

### **Security Task**
- **Security Type**: [Scanning | Hardening | Vulnerability Fix | Policy]
- **Scope**: [What security work needs to be done?]
- **Priority**: [Critical | High | Medium | Low]

### **Research Project**
- **Research Question**: [What are we trying to answer?]
- **Methodology**: [How will we conduct the research?]
- **Deliverables**: [What will be produced?]

### **Spike**
- **Spike Question**: [What technical question needs answering?]
- **Time Box**: [How long is this spike?]
- **Success Criteria**: [What constitutes success?]

### **Project Task/Meeting**
- **Meeting Type**: [Backlog Grooming | Review | Retrospective | Planning]
- **Participants**: [Who needs to attend?]
- **Agenda**: [What will be discussed?]

---

## 📝 Implementation Details

### **Assignee**
**Primary**: [Name]
**Secondary**: [Name if applicable]

### **Capacity Required**
**Minimum**: [Low/Medium/High capacity needed]
**Optimal**: [Best capacity level for this work]

### **Skills Required**
- [ ] Skill 1
- [ ] Skill 2
- [ ] Skill 3

### **Tools & Resources**
- [ ] Tool 1
- [ ] Resource 2
- [ ] Access 3

---

## 📈 Progress Tracking

### **Status**
[Backlog | Ready to Pull | In Progress | Review | Done]

### **Progress Updates**
**Date**: YYYY-MM-DD
**Update**: [Progress made]
**Blockers**: [Any blockers encountered]
**Next Steps**: [What's next?]

### **Time Tracking**
**Estimated**: [Original estimate]
**Actual**: [Time actually spent]
**Remaining**: [Estimated time remaining]

---

## 🔄 Review & Approval

### **Reviewers**
- [ ] Reviewer 1
- [ ] Reviewer 2
- [ ] Reviewer 3

### **Approval**
- [ ] Technical Review
- [ ] Business Review
- [ ] Final Approval

### **Sign-off**
**Completed By**: [Name]
**Date**: YYYY-MM-DD
**Approved By**: [Name]
**Date**: YYYY-MM-DD

---

## 📚 References & Links

- [Related Documentation](link)
- [External Resources](link)
- [Related Issues/PRs](link)
- [Design Documents](link)

---

## 📝 Notes

[Any additional notes, context, or information that doesn't fit elsewhere]

---

**Created By**: [Name]
**Last Updated**: YYYY-MM-DD
**Version**: 1.0
