# Issue Management Guide

This document defines our issue management workflow, label system, and standards for maintaining a healthy project backlog.

## 🎯 Issue Types

> **Note**: GitHub Issues is the single source of truth for all work items. Use structured labels (`type:`, `priority:`, `area:`, `status:`) for consistent tracking.

### 🚀 Feature Issues
**Format**: `[FEATURE] Feature Name`
**Purpose**: New functionality or enhancements to existing features

**Required Sections**:
```markdown
## 🎯 Feature Description
Clear description of the feature and its purpose

## 💡 Problem/Use Case
What problem this solves or use case it enables

## 🏗️ Proposed Solution
High-level approach to implementing the feature

## 📋 Acceptance Criteria
- [ ] Specific, testable criteria
- [ ] Documentation updated with examples
- [ ] Tests written for new functionality
- [ ] Feature works cross-platform

## 🔧 Implementation Considerations
Technical notes, dependencies, performance implications
```

**Labels**: `enhancement`, `priority: [level]`, relevant category labels

### 🏗️ Epic Issues
**Format**: `[EPIC] Epic Name`
**Purpose**: Large features that need to be broken down into smaller issues

**Required Sections**:
```markdown
## 🎯 Description
**EPIC**: High-level description of the large feature

## 🔄 Next Steps - Break Down Required
Clear statement that this needs decomposition

## 📋 Proposed Breakdown
Suggested smaller issues with brief descriptions

## ⚠️ Impact Analysis
Business impact and priority rationale

## 💡 Priority Recommendation
Suggested priority with justification
```

**Labels**: `epic`, `enhancement`, `priority: [level]`

### 🔍 Analysis Issues
**Format**: `[ANALYSIS] Analysis Topic`
**Purpose**: Research, design, and architectural analysis before implementation

**Required Sections**:
```markdown
## 🎯 Description
**Parent Epic/Issue**: Link to related work

## 🔍 Analysis Required
Key questions to answer and areas to research

## 📋 Deliverables
- [ ] Specific analysis outputs
- [ ] Documentation or design artifacts
- [ ] Implementation recommendations

## ✅ Definition of Done
Clear criteria for when analysis is complete
```

**Labels**: `analysis`, `architecture` (if applicable), `priority: [level]`

### 🔧 Technical Debt Issues
**Format**: `[TECHNICAL DEBT] Description`
**Purpose**: Code improvements, refactoring, TODO items, and maintenance

**Required Sections**:
```markdown
## 🎯 Description
Clear description of the technical debt

## 📍 Current State
What exists now (code location, current implementation)

## 🎯 Desired State
What should be improved and why

## 📊 Impact
How this debt affects development, performance, or maintainability

## 🔧 Proposed Solution
Approach to addressing the debt
```

**Labels**: `technical-debt`, `priority: [level]`, relevant category labels

### 📝 Documentation Issues
**Format**: `[DOCUMENTATION] Documentation Topic`
**Purpose**: Missing or outdated documentation

**Required Sections**:
```markdown
## 🎯 Description
What documentation is missing or needs updates

## 📝 Missing Documentation
Specific documentation gaps with file locations

## 📋 Acceptance Criteria
- [ ] Specific documentation deliverables
- [ ] Updated cross-references
- [ ] Examples and usage patterns included
```

**Labels**: `documentation`, `priority: [level]`

### 🐛 Bug Issues
**Format**: `[BUG] Bug Description`
**Purpose**: Defects, errors, and unexpected behavior

**Required Sections**:
```markdown
## 🐛 Bug Description
Clear description of the issue

## 🔄 Reproduction Steps
1. Step one
2. Step two
3. Issue occurs

## 💻 Environment
- OS:
- Python version:
- Branch/commit:

## 📊 Expected vs Actual
- Expected: What should happen
- Actual: What actually happens

## 🔧 Proposed Fix (if known)
Suggested solution or investigation direction
```

**Labels**: `type: bug`, `priority: [level]`, `area: [relevant]`

### 🧪 Testing Issues
**Format**: `[TEST] Testing Task Description`
**Purpose**: Testing tasks including unit, integration, E2E, performance, and security testing

**Labels**: `type: testing`, `priority: [level]`, `area: [relevant]`

### 🔧 CI/CD Issues
**Format**: `[CI/CD] Pipeline/Automation Task`
**Purpose**: CI/CD pipelines, build automation, deployment automation

**Labels**: `type: ci-cd`, `priority: [level]`, `area: tooling`

### 🔒 Security Issues
**Format**: `[SECURITY] Security Task Description`
**Purpose**: Security hardening, vulnerability fixes, security scanning setup

**Labels**: `type: security`, `priority: [level]`, `area: [relevant]`

### 🏗️ Infrastructure Issues
**Format**: `[INFRA] Infrastructure Task`
**Purpose**: Infrastructure setup, DevOps, environment configuration, IaC

**Labels**: `type: infra`, `priority: [level]`, `area: [relevant]`

## 🏷️ Label System

### Structured Label Taxonomy

All issues should use **structured prefixed labels** for consistency:

#### Type Labels (Required - exactly one)
- **`type: epic`** - Large features requiring breakdown
- **`type: feature`** - New features and enhancements
- **`type: bug`** - Defects and unexpected behavior
- **`type: tech-debt`** - Code quality, refactoring, TODO items
- **`type: testing`** - Testing tasks and test infrastructure
- **`type: docs`** - Documentation creation and updates
- **`type: ci-cd`** - CI/CD pipelines and automation
- **`type: security`** - Security tasks and hardening
- **`type: infra`** - Infrastructure and DevOps tasks
- **`type: process`** - Process improvement tasks
- **`type: analysis`** - Research and analysis tasks

#### Priority Labels (Required - exactly one)
- **`priority: high`** - Blocking current work, security issues, critical bugs
- **`priority: medium`** - Important features, non-blocking improvements
- **`priority: low`** - Nice-to-have features, minor improvements

#### Area Labels (Optional - one or more)
- **`area: api`** - API related work
- **`area: backend`** - Backend implementation
- **`area: tooling`** - Tools and automation
- Additional areas as needed

#### Status Labels (Optional)
- **`status: ready`** - Ready to pull into work
- **`blocked`** - Cannot proceed due to dependencies
- **`in-progress`** - Currently being worked on

### Legacy Labels (Compatibility)

These labels remain for compatibility but prefer structured equivalents:
- **`enhancement`** → use `type: feature`
- **`technical-debt`** → use `type: tech-debt`
- **`documentation`** → use `type: docs`
- **`bug`** → use `type: bug`
- **`epic`** → use `type: epic`
- **`analysis`** → use `type: analysis`
- **`automation`** → use `area: tooling` + appropriate type
- **`testing`** → use `type: testing`
- **`architecture`** → use type + `architecture` label
- **`workflow`** → use `type: process`
- **`roadmap`** - Items from the original roadmap (legacy)

### Special Labels

- **`good-first-issue`** - Suitable for new contributors
- **`help-wanted`** - Community assistance requested

## 📊 Backlog Management

### Priority Assignment Criteria

**High Priority (`priority: high`)**:
- Blocks current development work
- Security vulnerabilities
- Critical bugs affecting core functionality
- Foundational work needed by other features
- Process/workflow improvements for team efficiency

**Medium Priority (`priority: medium`)**:
- Important features for user experience
- Technical debt with moderate impact
- Documentation for existing features
- Non-critical bugs
- Performance improvements

**Low Priority (`priority: low`)**:
- Nice-to-have features
- Minor UI/UX improvements
- Optional documentation
- Cosmetic issues

### Epic Breakdown Process

1. **Create Epic Issue** with broad scope and requirements
2. **Add `epic` label** and appropriate priority
3. **Analysis Phase**: Create analysis issues for complex epics
4. **Decomposition**: Break into focused, implementable issues
5. **Link Child Issues**: Reference parent epic in child issues
6. **Track Progress**: Update epic with completion status

### Issue Lifecycle

```
📝 Created → 🔍 Triaged → 📋 Backlog → 🚧 In Progress → 👀 Review → ✅ Done
```

**States**:
- **Created**: New issue, needs triage
- **Triaged**: Labeled and prioritized
- **Backlog**: Ready for development
- **In Progress**: Actively being worked (`in-progress` label)
- **Review**: PR submitted, under review
- **Done**: Merged, deployed, issue closed

## ✅ Definition of Done

Every issue must meet these criteria before closing:

### Code Requirements
- [ ] Feature implemented according to acceptance criteria
- [ ] Code follows project coding standards
- [ ] No new linting errors or warnings
- [ ] Cross-platform compatibility verified

### Testing Requirements
- [ ] Unit tests written and passing
- [ ] Integration tests updated if needed
- [ ] Manual testing completed
- [ ] No regressions introduced

### Documentation Requirements
- [ ] **API documentation** updated if public interfaces changed
- [ ] **User documentation** updated with examples
- [ ] **README** updated if workflow or features changed
- [ ] **Changelog** entry added for user-facing changes

### Review Requirements
- [ ] Code reviewed by team member
- [ ] PR template completed
- [ ] All CI checks passing
- [ ] Branch up to date with target branch

### Release Requirements
- [ ] Changes tested in integration environment
- [ ] Documentation deployed and accessible
- [ ] Feature verified in production-like environment

## 🔄 Workflow Integration

### Branch Naming
- Feature: `feature/issue-{number}-{brief-description}`
- Bugfix: `bugfix/issue-{number}-{brief-description}`
- Documentation: `docs/issue-{number}-{brief-description}`

### Commit Messages
```
type(scope): brief description

Detailed description if needed.

Fixes #issue-number
```

### Pull Request Requirements
- Link to related issue
- Complete PR template
- All Definition of Done criteria met
- Passing CI checks

## 📈 Backlog Health Metrics

### Healthy Backlog Indicators
- **Age Distribution**: Most issues < 30 days old
- **Priority Balance**: ~20% high, ~60% medium, ~20% low
- **Epic Ratio**: <25% of open issues should be epics
- **Documentation Debt**: <10% of issues should be documentation debt

### Warning Signs
- Issues open >90 days without progress
- >50% of backlog is high priority
- Multiple epics without breakdown progress
- Growing documentation debt

### Regular Maintenance
- **Weekly**: Triage new issues, update priorities
- **Monthly**: Review old issues, close stale items
- **Quarterly**: Epic breakdown planning, backlog cleanup

---

*This document is maintained by the development team. For questions or suggestions, please open an issue with the `workflow` label.*
