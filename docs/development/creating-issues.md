# Creating Issues: TDD and Quality Requirements

## 🎯 Overview

**ALL issues that involve code changes MUST include Test-Driven Development (TDD) acceptance criteria.** This ensures our rigorous development process is self-sustaining and prevents quality regressions.

## 📋 Issue Creation Checklist

Before creating any issue, ensure:

### ✅ **1. Use Proper Issue Template**
- **Feature requests**: Use [feature request template](.github/ISSUE_TEMPLATE/feature-request.yml) 
- **Bug reports**: Use [bug report template](.github/ISSUE_TEMPLATE/bug-report.yml)
- **Technical debt**: Use [technical debt template](.github/ISSUE_TEMPLATE/technical-debt.yml)
- **Documentation**: Use [documentation template](.github/ISSUE_TEMPLATE/documentation.yml)

### ✅ **2. Include TDD Acceptance Criteria (MANDATORY for Code Changes)**

**Every issue involving code changes MUST include:**

```markdown
## 🧪 Test-Driven Development (TDD) Requirements:
- [ ] **Tests written FIRST** - Before any implementation code
- [ ] **Test-fail-pass-refactor cycle documented** - Evidence of TDD process  
- [ ] **Test coverage maintained** - No reduction in overall test coverage
- [ ] **All tests passing** - New functionality fully tested

## 📚 Documentation Requirements:
- [ ] **Documentation updated** - README, guides, changelog as appropriate
- [ ] **UX changes reflected** - User guides updated for interface changes
- [ ] **AI context maintained** - AGENTS.md updated with new patterns

## 🔀 Development Workflow Requirements:
- [ ] **Proper branch workflow** - develop → feature branch → PR → merge
- [ ] **Focused commits** - Clear, logical commit history
- [ ] **PR template compliance** - Use appropriate PR template
```

### ✅ **3. Apply Appropriate Labels**

**Required labels for new issues:**
- **Priority**: `priority: high`, `priority: medium`, `priority: low`
- **Effort**: `effort: small`, `effort: medium`, `effort: large`  
- **Type**: `type: feature`, `type: bug`, `type: documentation`, `type: maintenance`
- **Domain**: `infrastructure`, `operations`, `security`, etc. (as appropriate)

## 🚫 **Common Mistakes to Avoid**

### ❌ **Issues WITHOUT TDD Requirements**
```markdown
❌ BAD ISSUE:
"Add user authentication"

Description: We need user authentication.
Acceptance Criteria: 
- [ ] Users can log in
- [ ] Passwords are secure
```

### ✅ **Issues WITH TDD Requirements**
```markdown
✅ GOOD ISSUE:
"Add user authentication with JWT tokens"

## 🧪 Test-Driven Development (TDD) Requirements:
- [ ] **Authentication tests written FIRST** - Login/logout, token validation
- [ ] **Security tests included** - Password hashing, token expiry, brute force protection
- [ ] **Integration tests** - End-to-end authentication flow
- [ ] **All tests passing** - 100% authentication functionality covered

## 📝 Implementation Requirements:
- [ ] JWT token implementation with secure defaults
- [ ] Password hashing with bcrypt/scrypt
- [ ] Rate limiting for login attempts
- [ ] Session management and logout

## 📚 Documentation Requirements:
- [ ] Authentication guide for developers
- [ ] Security documentation updated
- [ ] API documentation for auth endpoints
```

## 📚 **Self-Sustaining Process Documentation**

### **For Contributors:**
1. **Read this guide** before creating any issue
2. **Use issue templates** - They enforce TDD requirements automatically
3. **Follow TDD acceptance criteria** - Every code change needs tests first
4. **Update documentation** - Keep AI context and user guides current

### **For Maintainers:**
1. **Review issue quality** - Ensure TDD criteria are included
2. **Reject incomplete issues** - Request TDD acceptance criteria if missing
3. **Enforce process** - Don't approve PRs without TDD evidence
4. **Update this guide** - Keep guidance current as process evolves

## 🔄 **Quality Gates**

**Before issue assignment:**
- ✅ Proper template used
- ✅ TDD acceptance criteria included
- ✅ Clear description and examples
- ✅ Appropriate labels applied

**Before implementation:**
- ✅ Tests written first
- ✅ Implementation follows TDD cycle
- ✅ Documentation updated
- ✅ PR template compliance

## 💡 **Examples by Issue Type**

### **Feature Request Example**
- Use feature request template (has TDD requirements built-in)
- Focus on **tests first** approach
- Include user stories and business value

### **Bug Report Example**  
- Write **reproduction test first**
- Minimal fix to make test pass
- Ensure no regressions

### **Technical Debt Example**
- **Refactoring tests first** to ensure no functionality lost
- Incremental improvements with test coverage
- Code quality metrics improvement

---

## 🎯 **Remember: TDD is NOT Optional**

This project follows **mandatory Test-Driven Development**. Every code change starts with tests. This ensures:
- ✅ **Quality is built-in** - Not bolted on later
- ✅ **Confidence in changes** - Tests prove functionality works  
- ✅ **Sustainable development** - Future changes won't break existing features
- ✅ **Professional standards** - Enterprise-grade development practices

**If an issue doesn't include TDD acceptance criteria for code changes, it's incomplete and should be updated before assignment.**
