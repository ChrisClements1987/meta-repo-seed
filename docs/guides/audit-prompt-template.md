# Comprehensive AI Agent Audit Prompt Template

## Universal Audit Prompt for Any Software Project

Use this prompt to generate thorough, actionable audit reports for any software repository:

---

**AUDIT REQUEST PROMPT:**

```
Please conduct a comprehensive, professional-grade audit of this software repository. Analyze the codebase, documentation, processes, and infrastructure to identify improvements and risks.

## AUDIT SCOPE & METHODOLOGY

Perform analysis across ALL of these domains:

### 1. **SECURITY AUDIT**
- **Dependencies**: Run dependency vulnerability scanning (pip-audit, npm audit, etc.)
- **Secrets**: Scan for hardcoded secrets, API keys, passwords, tokens
- **Static Analysis**: Use security linters (bandit, eslint-security, etc.) 
- **CI/CD Security**: Review pipeline security, secret management, permissions
- **Input Validation**: Check for injection vulnerabilities, path traversal
- **Authentication/Authorization**: Review access controls and security patterns

### 2. **CODE QUALITY AUDIT** 
- **Linting**: Run language-specific linters (pylint, eslint, rubocop, etc.)
- **Complexity**: Measure cyclomatic complexity (radon, etc.)
- **Duplication**: Identify code duplication and repetitive patterns
- **Architecture**: Review code organization, separation of concerns
- **Error Handling**: Assess exception handling patterns and robustness
- **Code Smells**: Identify maintainability issues and technical debt

### 3. **TESTING AUDIT**
- **Coverage Analysis**: Measure test coverage by module/function
- **Test Quality**: Review test structure, assertions, and reliability  
- **Test Types**: Assess unit, integration, e2e test distribution
- **CI Integration**: Verify automated testing and quality gates
- **Test Maintenance**: Check for flaky, slow, or outdated tests

### 4. **DOCUMENTATION AUDIT**
- **README Quality**: Assess clarity, completeness, and structure
- **API Documentation**: Review inline docs, docstrings, API specs
- **User Guides**: Evaluate onboarding and usage documentation
- **Architecture Docs**: Check design decisions and technical documentation
- **Link Validation**: Verify all links work and content is current

### 5. **PERFORMANCE AUDIT**
- **Runtime Performance**: Profile application execution and bottlenecks
- **Resource Usage**: Check memory, CPU, and I/O efficiency
- **Scalability**: Assess performance under load and growth scenarios
- **Optimization Opportunities**: Identify areas for improvement
- **Benchmarking**: Establish performance baselines

### 6. **CONFIGURATION AUDIT**
- **Config Management**: Review configuration files and environment setup
- **CI/CD Configuration**: Assess workflow efficiency and best practices
- **Environment Consistency**: Check dev/staging/prod alignment
- **Secret Management**: Review how sensitive configuration is handled

### 7. **DEPENDENCY AUDIT**
- **Vulnerability Scanning**: Check for known security issues
- **License Compliance**: Verify license compatibility and legal requirements
- **Dependency Health**: Assess maintenance status and update frequency
- **Version Management**: Review pinning strategy and update policies

### 8. **PROCESS AUDIT**
- **Development Workflow**: Review branching, PR, and release processes
- **Quality Gates**: Assess automated and manual quality controls
- **Governance**: Review policies, standards, and compliance
- **Automation**: Identify manual processes that could be automated

## REPORT FORMAT REQUIREMENTS

Structure your findings using this exact format:

### **DOMAIN**: [Security/Code Quality/Testing/etc.]

#### **FINDINGS**
- **Issue**: [Specific finding]
  - **Severity**: Critical | High | Medium | Low
  - **Evidence**: [Tool output, file references, specific examples]
  - **Business Impact**: [How this affects operations, users, or business goals]
  - **Technical Risk**: [Potential consequences if not addressed]

#### **RECOMMENDATIONS**  
- **Action**: [Specific action to take]
  - **Priority**: Immediate | Short-term | Long-term
  - **Effort**: Small (hours) | Medium (days) | Large (weeks)
  - **Tools Required**: [Specific tools/commands to implement fix]
  - **Success Criteria**: [How to measure successful resolution]
  - **Implementation Steps**: [Concrete steps to implement]

#### **METRICS & MEASUREMENT**
- **Current State**: [Baseline measurements]
- **Target State**: [Desired outcome metrics]  
- **Monitoring**: [How to track ongoing compliance]

## BUSINESS CONTEXT ANALYSIS

For each finding, consider:
- **User Impact**: How does this affect end users?
- **Developer Experience**: How does this affect team productivity?
- **Business Risk**: What are the business consequences?
- **Competitive Advantage**: How does fixing this improve market position?
- **Compliance**: Does this affect regulatory or industry standards?

## TOOL RECOMMENDATIONS

For each domain, specify:
- **Primary Tools**: [Best-in-class tools for this analysis]
- **Commands Used**: [Exact commands run for reproducibility]
- **Alternative Tools**: [Other options teams might prefer]
- **Integration**: [How to integrate into CI/CD or regular workflows]

## IMPLEMENTATION ROADMAP

Provide a prioritized implementation plan:

### **CRITICAL (Fix Immediately)**
Issues that pose security risks, legal problems, or prevent core functionality

### **HIGH PRIORITY (Fix Within 1-2 Weeks)**  
Issues that significantly impact quality, performance, or user experience

### **MEDIUM PRIORITY (Fix Within 1-2 Months)**
Issues that improve maintainability, developer experience, or future scalability

### **LOW PRIORITY (Fix When Time Permits)**
Issues that are nice-to-have improvements or cosmetic fixes

## QUALITY STANDARDS

Ensure your audit meets these standards:
- **Actionable**: Every finding has specific, implementable recommendations
- **Evidence-Based**: Include tool output, metrics, and concrete examples
- **Business-Focused**: Connect technical findings to business impact
- **Comprehensive**: Cover all requested domains thoroughly
- **Prioritized**: Clear severity and priority assessment
- **Reproducible**: Include exact commands and tools used
- **Professional**: Structure suitable for stakeholder review

## FINAL DELIVERABLES

Your audit report should include:
1. **Executive Summary** (2-3 paragraphs)
2. **Domain-by-Domain Analysis** (following format above)
3. **Prioritized Issue List** with effort estimates
4. **Implementation Roadmap** with timelines
5. **Recommended Tools and Processes** for ongoing quality assurance
6. **Success Metrics** for measuring improvement

Remember: Focus on findings that genuinely improve security, quality, performance, or user experience. Avoid nitpicking that doesn't add business value.
```

---

## EXAMPLE USAGE

**For any project:**
```
[Paste the audit prompt above]

PROJECT CONTEXT:
- Name: [Project Name]
- Purpose: [What the project does]
- Technology Stack: [Languages, frameworks, tools]
- Target Users: [Who uses this]
- Business Goals: [Key objectives]
- Critical Requirements: [Security, performance, compliance needs]

Please audit this repository and provide recommendations.
```

**For Business-in-a-Box specific audits:**
```
[Paste the audit prompt above]

BUSINESS-IN-A-BOX CONTEXT:
This project supports the Business-in-a-Box mission: enabling startups, charities, non-profits, and SMBs to deploy professional organizational infrastructure in under 10 minutes. Focus on:

- Professional Standards: Enterprise-grade quality that builds credibility
- Self-Governing Systems: Automation that reduces manual oversight needs
- Target Market Support: Works for resource-constrained organizations
- 10-Minute Deployment: Changes don't slow core deployment functionality
- Scalable Growth: Supports growth from solo founder to multi-tier organization

Prioritize findings that serve these business objectives.
```
