# Business-in-a-Box Development Workflow: GitFlow Guide v3.1

## 1. Philosophy & Guiding Principles

This document outlines our GitFlow methodology and development lifecycle, specifically tailored for Business-in-a-Box - a startup infrastructure automation platform designed for rapid deployment, maintainability, and professional standards.

Our workflow is built on four core principles:

* **🛡️ Stability:** The `main` branch is always production-ready and deployable. It represents our unbreakable source of truth.
* **🚀 Quality:** Quality is built into every step through automated testing, security scanning, and business validation - ensuring our 10-minute deployment promise.
* **🤝 Clarity:** Project state, change history, and work-in-progress are always transparent to support both human developers and AI assistance tools.
* **💨 Velocity:** By creating predictable, safe processes, we enable rapid iteration while maintaining professional standards.

### Project Context

This workflow specifically supports:
- **10-minute deployment promise** for complete business infrastructure
- **Single maintainer with contributors** model rather than large teams
- **Target markets:** Startups, charities, and SMBs requiring streamlined processes
- **Professional standards** that inspire confidence for enterprise adoption
- **AI-assisted development** where appropriate, with realistic expectations

### AI Integration Philosophy

We use AI tools (Claude, GitHub Copilot, Cursor, etc.) as supplementary development aids, not primary drivers.

**AI Strengths - Use For:**
- Code completion and boilerplate generation
- Test case suggestions for well-defined requirements
- Documentation writing assistance
- Code review supplementation (never replacement)
- Pattern recognition for common issues

**AI Limitations - Human Required:**
- Domain-specific business logic and architectural decisions
- Security vulnerability assessment and performance optimization
- Understanding project-specific constraints and market positioning
- Business partnership decisions and strategic direction

**Our Approach:**
- AI assists, humans decide
- Always validate AI suggestions against business requirements
- Maintain human review for all business-critical decisions
- Leverage AI for documentation and routine coding tasks

---

## 2. The Branching Strategy

We use a simplified GitFlow model optimized for small teams with rapid iteration cycles.

### Main Branches

#### `main`
* **Purpose:** Production-ready code for customer deployments. Official release history.
* **Rules:**
    * Code must be deployable within 10 minutes
    * Direct commits **strictly forbidden**
    * Code enters only through release merges or hotfixes
    * Each merge **must** be tagged with semantic version (e.g., `v1.2.0`)
    * **Branch Protection:**
        * ✅ At least 1 approval (appropriate for small teams)
        * ✅ All CI checks must pass (including business validation)
        * ✅ No direct pushes (even from maintainers)

#### `develop`
* **Purpose:** Integration branch containing latest development changes for next release.
* **Rules:**
    * Generally stable, may contain incomplete features
    * Direct commits **forbidden**
    * Code enters through feature branch merges only
    * **Branch Protection:**
        * ✅ At least 1 approval
        * ✅ All CI checks must pass

### Supporting Branches

#### `feature/*`
* **Purpose:** Developing new features or non-critical improvements
* **Branches From:** `develop`
* **Merges To:** `develop`
* **Naming Convention:** `feature/issue-123-short-description` (e.g., `feature/issue-42-business-profile-templates`)
* **Maximum Lifespan:** 3-5 days for rapid iteration
* **Deletion:** Automatic after squash merge

#### `release/*`
* **Purpose:** Prepare releases with final testing and stabilization
* **Branches From:** `develop`
* **Merges To:** `main` (for release) AND `develop` (to incorporate fixes)
* **Naming Convention:** `release/v1.2.0`
* **Lifespan:** 1-2 days maximum
* **Activities:** Business validation testing, documentation finalization, version bumping

#### `hotfix/*`
* **Purpose:** Critical fixes for production deployments
* **Branches From:** `main`
* **Merges To:** `main` AND `develop`
* **Naming Convention:** `hotfix/v1.2.1-critical-deployment-fix`
* **Criteria:**
    * Production deployment completely broken
    * Security vulnerabilities in deployed infrastructure
    * Data loss or corruption in business templates
    * Critical functionality failures affecting all users

### Branch Flow Diagram

```
main      ─────●────────────────●─────────●──────
               ↑                ↑         ↑
               │(release)       │         │(hotfix)
release        └──●─────●───────┘         │
                  ↑     ↑                 │
                  │     │(bug fixes)      │
                  │     ↓                 │
develop   ──●─────●─────●──●──●──●───────●───●──
            ↑           ↑  ↑  ↑           ↑
            │           │  │  │           │
feature     └──●──●─────┘  │  └──●──●─────┘
                           │
                           └─────────────────────┘
                           (emergency only)
```

---

## 3. The Feature Development Lifecycle

### Phase 1: Preparation

**1. Select an Issue**
Choose issues that meet the **Definition of Ready** (Section 8.C) and support project goals: startup infrastructure, charity tools, SMB automation, or core platform improvements.

**2. Review Context & Requirements**
Before implementation, review:
- Architecture diagrams and design documents
- Relevant code files and modules
- API specifications and data schemas
- Performance impact on deployment speed
- Integration with existing business profiles

**💡 AI Tip:** Share these context documents with your AI assistant at session start. Provide the issue details, relevant architecture docs, and coding patterns for more accurate assistance.

**3. Sync and Branch**
```bash
git checkout develop
git pull origin develop
git checkout -b feature/issue-42-business-profile-templates
```

### Phase 2: Development

**4. Early Visibility**
Push branch and create Draft PR immediately for transparency:
```bash
git push -u origin feature/issue-42-business-profile-templates
# Create Draft PR on GitHub/GitLab targeting develop
```
**Rationale:** Early CI feedback, team visibility, and collaborative opportunities.

**5. Test-Driven Development**
* **Write Failing Test:** Define functionality with a test before implementation
* **Confirm Failure:** Verify test fails for the right reason
* **Implement Code:** Write simplest code to pass the test
* **Confirm Success:** All tests pass
* **Refactor:** Clean up and ensure adherence to style guides

**💡 AI Tip:** AI excels at generating test cases. Describe requirements and ask for comprehensive test scenarios including edge cases. Example prompt: "Generate pytest test cases for a business profile validator that checks required fields, validates formats, and handles missing data."

**Testing Requirements:**
* ✅ Unit test coverage: 80%+ for new code
* ✅ Integration tests for API endpoints
* ✅ E2E tests for critical user flows
* ✅ Business validation tests for deployment scenarios

**6. Commit Standards**
Use **Conventional Commits** (Section 8.A) with clear descriptions:
```bash
# Good commits with business context:
git commit -m "feat(business): add startup-basic profile template

Enables rapid deployment for early-stage startups with
pre-configured accounting, CRM, and project management.

Maintains 10-minute deployment goal through optimized template.

Fixes #42"

git commit -m "fix(deploy): optimize template processing for speed"
git commit -m "docs(smb): update configuration guide for small businesses"
```

**💡 AI Tip:** Ask AI to review commit messages for clarity and conventional commit compliance. "Review this commit message and suggest improvements for clarity and convention adherence."

**7. Stay Current**
Daily rebase to minimize conflicts:
```bash
git pull --rebase origin develop
```

### Phase 3: Code Review & Validation

**8. Finalize & Submit**

**Pre-Submission Checklist:**
- [ ] All tests pass locally
- [ ] Code self-reviewed thoroughly
- [ ] History cleaned up (interactive rebase if needed)
- [ ] All relevant documentation updated

**Documentation Update Requirements:**

**📚 User Documentation** (if user-facing changes):
- [ ] User Guides / User Manuals updated
- [ ] Getting Started / Tutorials updated  
- [ ] FAQs updated with common scenarios
- [ ] Release notes drafted (for significant features)
- [ ] N/A - No user-facing changes

**👨‍💻 Developer Documentation** (if technical changes):
- [ ] API Reference / OpenAPI specs updated
- [ ] Architecture diagrams updated
- [ ] Code comments added for complex logic
- [ ] README.md updated (if setup changes)
- [ ] N/A - No developer documentation needed

**⚙️ Administrator/Operations Documentation** (if deployment/config changes):
- [ ] Installation & Deployment Guide updated
- [ ] Configuration Guide updated
- [ ] Environment variables documented
- [ ] Migration guide created (for breaking changes)
- [ ] N/A - No ops documentation needed

**Self-Review Checklist:**
- [ ] No debugging statements left in code
- [ ] TODO comments addressed or tracked
- [ ] Commented-out code removed
- [ ] No sensitive data (API keys, passwords)
- [ ] Follows project conventions and patterns

**💡 AI Tip:** Before human review, ask AI to review your code for common issues. "Review this code for bugs, security issues, and adherence to Python best practices. Check for edge cases I might have missed."

**Mark PR as Ready:**
- Change from Draft to Ready for Review
- Complete PR template thoroughly (Section 15.B)
- Link related issue (use "Closes #123")
- Provide clear testing instructions

**9. The Review Process**

**Automated Checks (CI):**
- Unit and integration tests
- Linting and code formatting
- Security vulnerability scanning
- Build verification
- Code coverage check (no decrease in coverage)
- Business validation tests (deployment speed, profile functionality)

**Human Review:**
* **Approvals Required:** 1 approval (appropriate for small teams)
* **Auto-Assignment:** Uses `CODEOWNERS` for domain expertise (Section 8.E)
* **Review SLA:**
    * First response: 4 business hours
    * Full review: 24 business hours
    * **Rationale:** Fast reviews prevent blocking, encourage small PRs

**What Reviewers Check:**
- Logic correctness and edge cases
- Code readability and maintainability
- Adherence to project patterns and conventions
- Security concerns and performance implications
- Test quality and coverage
- **Documentation completeness** (all three categories)
- **Business impact:** Maintains deployment speed, serves target market

**Address Feedback:**
Push new commits addressing review comments:
```bash
git commit -m "fix: address review feedback - handle null case"
```

**💡 AI Tip:** Share reviewer comments with AI for improvement suggestions. "A reviewer suggested I handle the edge case where X is null. What's the best approach while maintaining performance?"

**10. Approval & Merge**

* **Who Merges:** Author merges own PR after approval
* **Merge Strategy:** **Squash and merge** for clean history
* **Rationale:** Keeps `develop` history clean with one commit per feature, empowers developers
* **Cleanup:** Feature branch deleted automatically
* **Issue:** Closed automatically via "Closes #123" in PR

---

## 4. The Release Process

**Release Cadence Options:**

**🎯 Recommended: Sprint-Based (2 weeks)**
- Predictable for stakeholder planning
- Allows time for business validation
- Reduces cognitive load for small teams

**Alternative: Feature-Driven**
- Release when significant value ready
- Faster market feedback
- More flexible for rapid iteration

### Step-by-Step Release Workflow

**1. Release Decision**
**Decision Makers:** Product Owner (business) + Tech Lead (technical)

**Release Readiness:**
- [ ] Sufficient business value for target market
- [ ] All business validation tests pass
- [ ] No critical bugs affecting core functionality
- [ ] Documentation complete for new features
- [ ] Performance benchmarks met (deployment speed maintained)

**2. Create Release Branch**
```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.3.0
git push -u origin release/v1.3.0
```

**3. Version Bump**
Update version in project files:
```bash
# Python projects
# Update __version__ in __init__.py or seeding.py
# Update pyproject.toml version

# Project-specific
# Update version in business profile templates
# Update deployment documentation
# Update API documentation
```

**Semantic Versioning (SemVer):**
- **MAJOR (1.x.x → 2.0.0):** Breaking changes affecting existing deployments
- **MINOR (1.2.x → 1.3.0):** New features, backward-compatible functionality
- **PATCH (1.2.0 → 1.2.1):** Bug fixes, security patches, backward-compatible

**4. Stabilization Period (1-2 days max)**

**✅ Allowed on release branch:**
- Business validation testing
- Performance optimization
- Documentation improvements
- Bug fixes
- Configuration tweaks

**❌ Forbidden on release branch:**
- New features
- Major refactoring
- Breaking changes

**Business Validation Checklist:**
- [ ] Deployment speed test with all business profiles (< 10 min)
- [ ] Startup scenario testing
- [ ] Charity/nonprofit workflow validation
- [ ] SMB deployment verification
- [ ] Cross-platform compatibility (Windows/macOS/Linux)
- [ ] Professional presentation standards check

**5. Merge to `main`**
```bash
git checkout main
git pull origin main
git merge --no-ff release/v1.3.0
git push origin main
```
**Note:** `--no-ff` creates merge commit, preserving release history.

**6. Tag the Release**
```bash
git tag -a v1.3.0 -m "Release v1.3.0: Enhanced Business Profiles

Key Features:
- New charity-nonprofit business profile
- Improved deployment speed (8.5 minutes avg)
- Enhanced SMB security templates
- Cross-platform compatibility improvements

Business Impact: Enables faster nonprofit infrastructure deployment
with professional governance and compliance templates."

git push origin v1.3.0
```

**7. Merge Back to `develop`**
```bash
git checkout develop
git pull origin develop
git merge --no-ff release/v1.3.0
git push origin develop
```

**8. Delete Release Branch**
```bash
git branch -d release/v1.3.0
git push origin --delete release/v1.3.0
```

**9. Automated Deployment**
CI/CD automatically:
1. Detects new tag on `main`
2. Runs full validation suite
3. Builds production artifacts
4. Deploys to production
5. Runs post-deployment health checks
6. Notifies team

**10. Communicate**
- Update project website/documentation
- Announce to target market communities
- Update roadmap and metrics
- Gather early adopter feedback

---

## 5. The Hotfix Lifecycle

**IMPORTANT:** Hotfixes bypass normal quality gates. Use sparingly.

### When to Use Hotfix vs Regular Fix

**🚨 Use Hotfix When:**
- Production deployment completely fails
- Security vulnerability actively exploited
- Data loss or corruption occurring
- Critical business function broken for all users
- Financial/legal/compliance emergency

**📅 Use Regular Process When:**
- Bug affects only some users or scenarios
- Workaround exists
- Impact moderate or low
- Can wait for next release (days, not hours)

### Step-by-Step Hotfix Workflow

**1. Incident Declaration**
```bash
# Team communication example:
"🚨 HOTFIX IN PROGRESS: Production deployment failing for all new users
Branch: hotfix/v1.2.1-startup-template-fix
ETA: 2 hours
Impact: All new business deployments blocked
Owner: @developer"
```

**2. Create Hotfix Branch**
```bash
git checkout main
git pull origin main
git checkout -b hotfix/v1.2.1-startup-template-fix
git push -u origin hotfix/v1.2.1-startup-template-fix
```

**3. Implement Minimal Fix**
- **Focus:** Minimal change to restore functionality
- **Avoid:** Unrelated improvements or refactoring
- **Include:** Test that would have caught the issue

**💡 AI Tip:** When debugging critical issues, AI can help analyze logs and suggest root causes. "Here's the error log [paste]. What are the most likely causes and how should I fix it while minimizing risk?"

```bash
git commit -m "fix(startup): resolve template processing error

Critical fix for startup profile deployment failure.
Template variable replacement failing due to encoding issue
affecting Windows deployment environments.

Restores deployment capability for startup profiles.

Fixes critical production blocking issue."
```

**4. Expedited Testing**
- All existing tests must pass
- New test demonstrates fix
- Manual validation on staging (if time permits)
- Focus on safety over perfection

**5. Expedited Review**
- **Approval:** 1 approval from senior developer
- **Focus:** Fix effectiveness and safety
- **Speed:** Review within 1-2 hours if possible
- **Rationale:** Speed critical, but second pair of eyes essential

**6. Emergency Deployment**
```bash
# Merge to main
git checkout main
git merge --no-ff hotfix/v1.2.1-startup-template-fix
git push origin main

# Tag immediately
git tag -a v1.2.1 -m "Hotfix v1.2.1: Critical startup deployment fix"
git push origin v1.2.1
```

**7. Sync with Development**
```bash
# Merge to develop and any active release branches
git checkout develop
git merge --no-ff hotfix/v1.2.1-startup-template-fix
git push origin develop

# If release branch exists:
git checkout release/v1.3.0
git merge --no-ff hotfix/v1.2.1-startup-template-fix

# Cleanup
git branch -d hotfix/v1.2.1-startup-template-fix
git push origin --delete hotfix/v1.2.1-startup-template-fix
```

**8. Post-Incident Review (Required within 48 hours)**
- [ ] Post-mortem scheduled
- [ ] Root cause analysis documented
- [ ] Process improvements identified
- [ ] Testing updated to catch similar issues
- [ ] Communication to affected stakeholders
- [ ] **NO BLAME CULTURE** - focus on system improvements

---

## 6. Conflict Resolution

### During Feature Development Rebase

```bash
# Daily rebase encounters conflicts
git pull --rebase origin develop

# Git pauses, showing conflicted files
git status

# Resolve each file manually
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# Stage resolved files
git add path/to/resolved-file.py

# Continue rebase
git rebase --continue

# If confused or stuck
git rebase --abort  # Start over
```

**💡 AI Tip:** For complex conflicts, share both versions with AI. "Help me resolve this conflict while preserving functionality from both sides: [paste conflict]." Always test after resolution.

**Best Practices:**
- Resolve conflicts in small chunks
- Run tests after resolution
- When in doubt, ask the author of conflicting code
- Preserve business logic functionality over style preferences

### During PR Merge

**Scenario:** GitHub shows "This branch has conflicts that must be resolved."

**Option 1: Rebase (Preferred)**
```bash
git checkout feature/your-branch
git pull --rebase origin develop
# Resolve conflicts
git push --force-with-lease origin feature/your-branch
```

**Option 2: Merge develop into branch**
```bash
git checkout feature/your-branch
git merge origin/develop
# Resolve conflicts
git commit
git push origin feature/your-branch
```

**Recommendation:** Option 1 (rebase) keeps history cleaner, though requires force-push (safe with `--force-with-lease`).

### Conflict Prevention

**For Small Teams:**
- Daily 5-minute standups mentioning which files being touched
- Modular design keeping features separated
- Feature flags for merging incomplete work
- Coordinate when multiple people need same files

---

## 7. Rollback & Emergency Procedures

### Rollback Decision Matrix

**🔴 Immediate Rollback:**
- System completely down
- Data corruption occurring
- Security breach active
- Critical function broken for all users

**🟡 Monitor and Decide:**
- One feature/profile affected
- Performance degradation (not critical)
- Subset of users affected
- Non-critical feature issues

### Rollback Process

**Option 1: Deploy Previous Version (Fastest)**
```bash
# Find last known good version
git tag --sort=-version:refname | head -5

# Deploy specific version
git checkout v1.2.0
./scripts/deploy-production.sh
```

**Option 2: Revert and Re-release**
```bash
git checkout main
git revert <commit-hash>  # Creates new commit undoing changes
git tag -a v1.2.2 -m "Revert v1.2.1: Stability fix"
git push origin main --tags
```

**Option 3: Emergency Hotfix**
If fix is quick (< 30 min), follow hotfix process.

**Rollback Authority:**
- ✅ On-call engineer can initiate without approval
- ✅ Must notify team immediately in incident channel
- **Rationale:** Speed critical in emergencies; trust your engineers

### Post-Rollback

1. Investigate root cause
2. Create issue for proper fix
3. Schedule post-mortem (mandatory)
4. Update runbooks and testing

---

## 8. Supporting Principles & Definitions

### A. Conventional Commits

**Format:** `type(scope): subject`

**Types:**
* **`feat`:** New feature
* **`fix`:** Bug fix
* **`docs`:** Documentation only
* **`style`:** Code style (formatting, semicolons)
* **`refactor`:** Code change that neither fixes bug nor adds feature
* **`perf`:** Performance improvement
* **`test`:** Adding or correcting tests
* **`build`:** Build system or dependency changes
* **`ci`:** CI configuration changes
* **`chore`:** Other changes not modifying src or test

**Examples:**
```bash
feat(auth): add OAuth2 login support
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
test(auth): add unit tests for password validation
perf(templates): optimize business profile loading
```

**Enforcement:**
* ✅ Use git hook (commitlint) to enforce format
* **Rationale:** Enables automated CHANGELOG generation, helps AI understand code history

### B. Semantic Versioning (SemVer)

`MAJOR.MINOR.PATCH`

* **MAJOR (1.x.x → 2.0.0):** Breaking changes, incompatible API changes
* **MINOR (1.2.x → 1.3.0):** New features, backward-compatible
* **PATCH (1.2.3 → 1.2.4):** Bug fixes, backward-compatible

**Pre-release versions:**
* `1.3.0-alpha.1` - early testing
* `1.3.0-beta.2` - feature complete, testing
* `1.3.0-rc.1` - release candidate

**Version Zero (0.x.x):**
* During initial development, use `0.x.x`
* In 0.x.x, MINOR acts like MAJOR (breaking changes allowed)
* Move to 1.0.0 when API stable for public use

### C. Definition of Ready (DoR)

An issue is ready for development when:

**Business Requirements:**
- [ ] Clear value proposition for target market
- [ ] Impact on deployment speed/performance assessed
- [ ] User story: "As a [role], I want [feature], so that [benefit]"
- [ ] Success criteria include business validation metrics

**Technical Requirements:**
- [ ] Acceptance criteria testable
- [ ] Dependencies documented
- [ ] Performance impact estimated
- [ ] Security implications considered
- [ ] Estimated 3-5 days maximum

**Context for Development:**
- [ ] Links to relevant architecture/design docs
- [ ] Related code files identified
- [ ] API/data model changes specified
- [ ] Business validation scenarios defined

**AI Context Provided:**
- [ ] Key files and modules listed
- [ ] Existing patterns/similar features referenced
- [ ] Technical constraints documented
- [ ] Integration points identified

### D. Definition of Done (DoD)

A feature is done when:

**Code Quality:**
- [ ] All acceptance criteria met
- [ ] Code merged to `develop`
- [ ] All automated CI checks pass
- [ ] Code coverage maintained (80%+ for new code)
- [ ] Security scans clean
- [ ] Performance benchmarks met

**Documentation (All Three Categories):**
- [ ] **User Documentation** updated (if user-facing)
- [ ] **Developer Documentation** updated (if technical/API changes)
- [ ] **Admin/Ops Documentation** updated (if deployment/config changes)

**Testing & Validation:**
- [ ] Unit, integration, and business validation tests pass
- [ ] Successfully deployed to staging
- [ ] Manual QA performed (if applicable)
- [ ] Cross-platform compatibility verified (if applicable)

**Integration:**
- [ ] No regressions in existing functionality
- [ ] Integrates cleanly with existing features
- [ ] Deployment automation updated (if needed)
- [ ] Product Owner acceptance (if required)

### E. CODEOWNERS

Automatically assigns reviewers based on changed files.

**Example `.github/CODEOWNERS`:**
```
# Default owners
* @tech-lead

# Frontend code
/src/ui/** @frontend-team
/templates/** @frontend-team

# Backend API
/src/api/** @backend-team
/src/services/** @backend-team

# Infrastructure
/.github/workflows/** @devops-team
/docker/** @devops-team
/terraform/** @devops-team

# Business profiles
/profiles/** @business-team @product-owner

# Documentation
/docs/** @tech-writers
README.md @tech-writers
```

**Rationale:** Domain experts automatically review their areas.

### F. Environments

**1. Local Development**
   * Developer machines
   * Local database/mock services
   * Fast iteration

**2. Staging**
   * Mirrors production configuration
   * Auto-deployed from `develop` (or nightly)
   * Used for QA, integration testing, demos

**3. Production**
   * Customer-facing environment
   * Deployed only from tagged `main` releases
   * Monitored 24/7

**Optional:**
**4. Preview/PR Environments**
   * Ephemeral per-PR
   * Test features in isolation
   * Auto-destroyed on merge/close

**5. Canary**
   * Gradual production traffic (5% of users)
   * Validate before full rollout
   * For high-scale systems only

---

## 9. Troubleshooting & Common Scenarios

### Business-Specific Issues

**"Deployment exceeds 10-minute goal"**
```bash
# Profile performance issue
# 1. Run benchmarks
python scripts/benchmark_deployment.py

# 2. Profile bottlenecks
python -m cProfile -o profile.stats seeding.py --profile startup

# 3. Analyze results
python -m pstats profile.stats
# Use 'sort cumtime' and 'stats 20' to find slowest functions

# 4. Optimize critical path (template processing, file I/O, network)

# 5. Re-test
time python seeding.py --profile startup --dry-run
```

**"Business profile fails for specific scenario"**
```bash
# Debug specific profile
# 1. Test with verbose output
python seeding.py --profile charity-nonprofit --verbose --dry-run

# 2. Validate templates
python scripts/validate_templates.py charity-nonprofit

# 3. Check logs for errors
tail -f logs/deployment.log

# 4. Test with minimal config to isolate issue
```

**💡 AI Tip:** Share error logs with AI for diagnosis. "Here's the deployment error log [paste]. What's the root cause and how do I fix it?"

### Standard Git Issues

**"Accidentally committed to `develop` directly"**
```bash
# If not pushed yet
git branch feature/accidental-work
git reset --hard origin/develop
git checkout feature/accidental-work
# Create proper PR

# If already pushed (requires maintainer)
# Contact maintainer for force-push permission
```

**"Feature branch 100+ commits behind `develop`"**
```bash
# Option 1: Rebase (preferred)
git checkout feature/my-branch
git pull --rebase origin develop
# Resolve conflicts carefully
# Consider pairing with another dev

# Option 2: Fresh start if too complex
git checkout develop
git pull
git checkout -b feature/my-branch-v2
git cherry-pick <select commits from original>
# Open new PR, close old one
```

**"CI passes locally but fails remotely"**
Common causes:
1. **Different versions** - Match Node/Python version with CI
2. **Environment variables** - Check CI secrets configuration
3. **Test dependencies** - Ensure clean state, fresh test DB
4. **Timing/platform** - CI slower, adjust timeouts; test cross-platform

**Debug:**
```bash
# Replicate CI environment locally
docker run -it python:3.9 bash
# Clone repo, install deps, run tests
```

**💡 AI Tip:** Share CI logs with AI. "CI is failing with this error [paste log]. It passes locally. What could cause this difference?"

**"Reviewer unresponsive for 24+ hours"**
1. Polite ping in PR: "@reviewer friendly reminder"
2. Direct message in team chat
3. After 48 hours: Request different reviewer
4. **Policy:** Any senior dev can step in after 48 hours

**"Need to abandon feature branch"**
```bash
git checkout develop
git branch -D feature/abandoned  # Local delete
git push origin --delete feature/abandoned  # Remote delete
# Close PR with explanation
# Move issue back to backlog
```

**"Two developers on one feature"**

**Preferred: Pair Programming**
* Work together on one machine/screen
* One types, one thinks/reviews
* Switch every 30 minutes
* Works great with AI: one prompts, one reviews

**Alternative: Shared Branch**
```bash
# Dev 1 creates branch
git checkout -b feature/shared-feature

# Dev 2 checks out
git fetch
git checkout feature/shared-feature

# Both devs:
git pull --rebase  # Frequently
# Communicate about files
# Commit and push frequently
```

---

## 10. Process Exceptions

**MAY SKIP full PR process for:**

### Minor Documentation Changes
* Typo fixes in markdown
* Formatting corrections
* Broken link repairs
* **Still requires:** 1 approval OR use docs branch
* **Rationale:** Documentation quality crucial for adoption

### Emergency Security Patches
* **Criteria:** Active vulnerability affecting deployments
* **Process:** Follow hotfix, review after if time-critical
* **Documentation:** Explain exception in commit message

### Automated Dependency Updates
* **Scope:** Patch versions from trusted sources
* **Requirements:** CI passes, security scans clean
* **Manual review:** Minor/major updates always

**NEVER SKIP FOR:**
* Code changes
* New features or business logic
* Configuration affecting deployment
* API changes
* Database migrations
* Integration with external services

---

## 11. Quick Reference

### Start Feature
```bash
git checkout develop && git pull
git checkout -b feature/issue-123-description
git push -u origin feature/issue-123-description
# Open Draft PR immediately
```

### Daily Development
```bash
# Update branch daily
git pull --rebase origin develop
git push --force-with-lease

# Before submitting PR
git rebase -i origin/develop  # Clean history
pytest  # All tests
flake8 && black . && isort .  # Code quality
```

### Merge After Approval
```bash
# Use GitHub UI: "Squash and merge"
# Or manually:
git checkout develop
git merge --squash feature/issue-123
git commit -m "feat(scope): clear description"
git push
git branch -D feature/issue-123
git push origin --delete feature/issue-123
```

### Release
```bash
git checkout develop && git pull
git checkout -b release/v1.3.0
# Bump version, stabilize, test
git checkout main && git merge --no-ff release/v1.3.0
git tag -a v1.3.0 -m "Release notes"
git push origin main --tags
git checkout develop && git merge --no-ff release/v1.3.0
```

### Hotfix
```bash
git checkout main && git pull
git checkout -b hotfix/v1.2.1-description
# Minimal fix + test
git commit -m "fix: critical issue"
# Open PR, expedited review
git checkout main && git merge --no-ff hotfix/v1.2.1
git tag -a v1.2.1 -m "Hotfix description"
git push origin main --tags
git checkout develop && git merge --no-ff hotfix/v1.2.1
```

---

## 12. Tooling & Automation

### Required Tools
* **Git** - Version control
* **GitHub/GitLab** - PR reviews and CI/CD
* **Python 3.8+** - Runtime
* **pytest** - Testing framework
* **CI/CD** - GitHub Actions, GitLab CI, etc.

### Code Quality Tools
* **Linter:** flake8, pylint
* **Formatter:** black, isort
* **Type Checker:** mypy, pyright

### Git Hooks (Husky or pre-commit)
```yaml
# .pre-commit-config.yaml example
repos:
  - repo: local
    hooks:
      - id: commitlint
        name: Conventional Commits
        entry: commitlint
        language: node
        stages: [commit-msg]
      
      - id: pytest
        name: Run tests
        entry: pytest
        language: python
        stages: [pre-push]
      
      - id: black
        name: Format with black
        entry: black
        language: python
        stages: [pre-commit]
```

### Security Tools
* **Dependency Scanning:** Dependabot, Renovate, Safety
* **Secret Scanning:** GitGuardian, TruffleHog
* **SAST:** Bandit, Semgrep, CodeQL

### CI/CD Automation
* **Auto-labeling** - Add labels based on changed files
* **Auto-assignment** - CODEOWNERS assigns reviewers
* **Auto-merge** - Dependabot patches (with caution)
* **CHANGELOG** - conventional-changelog, release-please

### AI Development Tools
* **GitHub Copilot** - Code completion
* **Cursor** - AI-assisted editing
* **Claude/ChatGPT** - Documentation, analysis
* **Continue** - VS Code AI integration

### Project-Specific Tools
* **Business Validator** - `scripts/validate_business_profiles.py`
* **Deployment Benchmark** - `scripts/benchmark_deployment.py`
* **Cross-Platform Tester** - `scripts/test_cross_platform.py`

---

## 13. Metrics & Continuous Improvement

### Track These Metrics

**Development Velocity:**
* **Cycle Time:** Branch creation to merge (target: < 5 days)
* **PR Size:** Lines changed (target: < 400 lines)
* **Review Time:** Ready to approval (target: < 24 hours)
* **Deployment Frequency:** Release cadence (target: weekly+)

**Quality Metrics:**
* **Change Failure Rate:** % deployments causing issues (target: < 15%)
* **Time to Restore:** Fix production issues (target: < 1 hour)
* **Test Coverage:** % code covered by tests (target: 80%+)
* **Bug Escape Rate:** Bugs reaching production (track trend)

**Business Metrics:**
* **Deployment Speed:** Time to working infrastructure (target: < 10 min)
* **Profile Success Rate:** % successful deployments by type
* **User Adoption:** Usage by target market segments
* **Professional Standards:** Enterprise adoption indicators

**Use metrics to identify bottlenecks, NOT to punish individuals.**

### Regular Process Reviews

**Quarterly Retrospective:**
- What's working well?
- Where are we struggling?
- Are policies helping or hindering?
- How effective are AI tools?
- What should we change?

**Update this document** based on team feedback and evolving needs.

---

## 14. Getting Help

**If stuck:**
1. Check this document
2. Ask in team chat: #engineering-help
3. Use AI assistant for technical questions
4. Reach out to senior developer for process questions
5. Schedule pairing session

**If document has gaps:**
1. Open issue: "Workflow docs don't cover X"
2. Suggest improvement in #process-feedback
3. Submit PR to improve documentation

**Remember:** This process serves us, not the other way around. If something doesn't make sense or blocks progress, speak up. We'll adapt.

---

## 15. Ready-to-Use Templates

### A. Issue Template: Feature Request

Save as `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature Request
about: Suggest a new feature or improvement
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## User Story
As a [type of user], I want [goal], so that [benefit/value].

## Business Value
How does this feature support our target markets (startups, charities, SMBs)?

## Problem Statement
A clear description of the problem this solves.
Ex. "Users are frustrated when..."

## Proposed Solution
A clear description of what you want to happen.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Context for AI Agents & Developers 🤖
*Provide direct links and references to help both AI tools and human developers quickly understand the technical landscape.*

### Architecture & Design
- **System Architecture:** [Link to architecture doc/diagram]
- **Design Mockups:** [Link to Figma/design files]
- **Technical Spec:** [Link to detailed specification]

### Code References
- **Key Files to Modify:**
  - `src/api/profiles/controller.py` - Profile CRUD operations
  - `src/services/deployment.py` - Deployment logic
- **Related Features:** [Link to similar implementation]
- **Existing Patterns:** [Link to code following similar patterns]

### Data & APIs
- **Database Schema:**
  - `BusinessProfile` model: `id`, `name`, `type`, `config`
  - `Template` model: `id`, `profile_id`, `content`, `version`
- **API Endpoints:**
  - `POST /api/profiles`
  - `GET /api/profiles/:id`
- **OpenAPI Spec:** [Link to API documentation]

### Performance & Business Impact
- **10-Minute Goal Impact:** How does this affect deployment speed?
- **Target Market:** Which business types benefit: [ ] Startup [ ] Charity [ ] SMB [ ] All
- **Professional Standards:** How does this maintain enterprise quality?

### Dependencies
- **Related Issues:** #123, #456
- **Blocked By:** #789
- **External Dependencies:** [List external services/APIs]

## Additional Context
Screenshots, examples, or other relevant information.

## Definition of Ready Checklist
- [ ] User story clear with business value
- [ ] Acceptance criteria testable
- [ ] Context and code references provided
- [ ] Performance impact assessed
- [ ] Dependencies documented
- [ ] Estimated 3-5 days or less
```

### B. Pull Request Template

Save as `.github/pull_request_template.md`:

```markdown
## Title: [Use Conventional Commit Format]
<!-- Examples:
feat(profiles): add charity-nonprofit business template
fix(deploy): optimize template processing for speed
docs(setup): update installation guide for Windows
-->

**Related Issue:** Closes #<issue_number>

---

## Summary of Changes

*Provide clear description of what changed and why. What problem does this solve? How does it work?*

---

## Type of Change
<!-- Check all that apply -->
- [ ] 🆕 New feature (non-breaking change adding functionality)
- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] 💥 Breaking change (fix or feature breaking existing functionality)
- [ ] 📝 Documentation update
- [ ] 🎨 Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test updates
- [ ] 🔧 Configuration/build changes

---

## Business Impact
<!-- Check relevant items -->
- [ ] Maintains 10-minute deployment goal
- [ ] Improves deployment speed
- [ ] Affects target market: [ ] Startups [ ] Charities [ ] SMBs [ ] All
- [ ] Maintains professional standards
- [ ] No business impact (technical/internal only)

**Deployment Speed Impact:** [e.g., "No change - 9.2 min avg" or "Improved to 8.5 min"]

---

## PR Checklist: Definition of Done

*Check all relevant boxes. PR will not be reviewed until complete.*

### Code Quality
- [ ] My code follows project style guidelines
- [ ] I have performed self-review of my code
- [ ] I have commented complex/non-obvious code
- [ ] My changes generate no new warnings or errors
- [ ] I have removed debugging code, console.logs, commented code

### Testing
- [ ] I have added tests proving my fix works or feature functions
- [ ] All new and existing tests pass locally
- [ ] I have tested edge cases and error scenarios
- [ ] Code coverage has not decreased
- [ ] Business validation tests pass (if applicable)

### Documentation (Check all that apply)

#### 📚 User Documentation
- [ ] User Guides/Manuals updated
- [ ] Getting Started/Tutorials updated
- [ ] FAQs updated with new scenarios
- [ ] Release notes drafted (significant changes)
- [ ] N/A - No user-facing changes

#### 👨‍💻 Developer Documentation
- [ ] API Reference/OpenAPI specs updated
- [ ] Architecture diagrams updated
- [ ] Code comments added for complex logic
- [ ] README.md updated (setup/build changes)
- [ ] N/A - No developer doc changes

#### ⚙️ Administrator/Operations Documentation
- [ ] Installation & Deployment Guide updated
- [ ] Configuration Guide updated
- [ ] Environment variables documented
- [ ] Migration guide created (breaking changes)
- [ ] N/A - No ops doc changes

---

## How to Test

*Provide step-by-step instructions for reviewer to test your changes.*

1. Check out this branch: `git checkout feature/branch-name`
2. Install dependencies: `pip install -r requirements.txt` (if needed)
3. Run the application: `python seeding.py --profile startup`
4. Expected result: [what should happen]

### Test Scenarios
- **Happy path:** [describe]
- **Edge case:** [describe]
- **Error handling:** [describe]

### Test Credentials (if applicable)
- Test user: `test@example.com` / `password123`
- Admin: `admin@example.com` / `admin456`

---

## Screenshots or GIFs (if applicable)

*For UI changes, provide visual evidence.*

### Before
[Screenshot]

### After
[Screenshot]

---

## Performance Impact (if applicable)

- [ ] Performance improves
- [ ] No significant performance impact
- [ ] Performance degrades (with justification)

**Benchmark Results:**
```
Before: [metric]
After: [metric]
Change: [percentage]
```

---

## Breaking Changes (if applicable)

*If this PR introduces breaking changes, describe:*
- What breaks and why
- Migration path for existing users
- Deprecation timeline (if applicable)
- Backward compatibility considerations

---

## Security Considerations (if applicable)

- [ ] No sensitive data exposed
- [ ] Authentication/authorization properly implemented
- [ ] Input validation added
- [ ] Security scans pass
- [ ] No new vulnerabilities introduced

---

## AI-Assisted Development

*If you used AI tools for this PR (optional):*
- [ ] AI helped with code generation
- [ ] AI helped with test case generation
- [ ] AI helped with documentation
- [ ] All AI suggestions validated by human review

---

## Additional Context

*Links to related PRs, design decisions, alternative approaches considered, technical debt notes, etc.*

---

## Reviewer Notes

*Anything specific you want reviewers to focus on?*

---

## Post-Merge Checklist
<!-- Author completes after merge -->
- [ ] Issue closed automatically
- [ ] Feature branch deleted
- [ ] Staging deployment verified
- [ ] Stakeholders notified (if applicable)
```

### C. Bug Report Template

Save as `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
---
name: Bug Report
about: Report a bug or unexpected behavior
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Execute '...'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Screenshots or Error Messages
If applicable, add screenshots or paste error messages.

```
[Paste full error log/stack trace here]
```

## Environment
- **OS:** [e.g., macOS 13.0, Windows 11, Ubuntu 22.04]
- **Browser:** [e.g., Chrome 120, Firefox 121] (if web-based)
- **Python Version:** [e.g., 3.9.7]
- **App Version:** [e.g., v1.2.3]
- **Environment:** [ ] Production [ ] Staging [ ] Local Development

## Business Impact
- **Severity:** [ ] 🔴 Critical [ ] 🟠 High [ ] 🟡 Medium [ ] 🟢 Low
- **Users Affected:** [ ] All users [ ] Specific segment [ ] Single user
- **Workaround Available:** [ ] Yes [ ] No
- **Target Market Affected:** [ ] Startups [ ] Charities [ ] SMBs [ ] All

**Impact Description:**
[How does this affect users? Business operations? Deployment speed?]

## Context for Developers & AI 🤖
- **Affected Files/Modules:** [e.g., src/services/deployment.py]
- **Related Code:** [Link to GitHub line/file if known]
- **Recent Changes:** [Link to recent PRs that might be related]
- **Business Profile Affected:** [e.g., startup-basic, charity-nonprofit]

## Additional Context
Any other relevant information, configuration details, etc.

## Possible Solution (optional)
If you have ideas on how to fix this.
```

### D. Hotfix Documentation Template

Save as `.github/ISSUE_TEMPLATE/hotfix.md`:

```markdown
---
name: Hotfix Request
about: Critical production issue requiring emergency fix
title: '[HOTFIX] '
labels: 'hotfix, critical'
assignees: ''
---

## 🚨 CRITICAL ISSUE

**Severity:** [ ] System Down [ ] Data Loss [ ] Security Breach [ ] Critical Function Broken

**Impact:**
- **Users Affected:** [All users / Specific segment / Number affected]
- **Business Impact:** [Financial / Operational / Reputational]
- **Time Sensitive:** [How urgent is this?]

## Issue Description
Clear description of the critical issue.

## Steps to Reproduce (if applicable)
1. ...
2. ...

## Error Messages/Logs
```
[Paste relevant error logs]
```

## Root Cause (if known)
[What caused this issue?]

## Proposed Fix
[Minimal change required to resolve issue]

## Testing Plan
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Regression testing plan

## Rollback Plan
[How to rollback if fix doesn't work]

## Communication Plan
- [ ] Stakeholders notified
- [ ] Users informed
- [ ] Team alerted
- [ ] Post-mortem scheduled

## Post-Hotfix Requirements
- [ ] Root cause analysis within 48 hours
- [ ] Process improvements identified
- [ ] Testing updated to catch similar issues
```

---

## 16. AI Workflow Best Practices

### Effective AI Usage Throughout Development

**Context Sharing:**
At session start, provide AI with:
- Issue description and acceptance criteria
- Relevant architecture docs and code files
- Project patterns and conventions
- Business constraints (deployment speed, target market)

**Example AI Prompts:**

**For Implementation:**
```
"I'm implementing [feature] for our business deployment platform.
Context: This is for [startup/charity/SMB] users who need [need].
Here's the existing architecture: [paste relevant structure]
Generate [specific component] that integrates with this system
while maintaining our 10-minute deployment goal."
```

**For Testing:**
```
"Generate comprehensive pytest test cases for this feature: [paste code]
Include:
- Happy path scenarios
- Edge cases for [specific business scenarios]
- Error handling
- Performance considerations for deployment speed"
```

**For Documentation:**
```
"Create user documentation for this feature: [describe feature]
Target audience: [startup founders/charity directors/SMB owners]
Include:
- Setup instructions
- Business examples
- Troubleshooting common issues
- Best practices"
```

**For Debugging:**
```
"Here's a deployment error log: [paste log]
Context: This occurs during [specific business profile] deployment
What are the most likely causes and how should I fix it
while minimizing risk to production?"
```

### AI Pre-Review Checklist

Before human review, ask AI to check:
- [ ] Are there obvious bugs or edge cases missed?
- [ ] Does code follow project conventions?
- [ ] Any security vulnerabilities?
- [ ] Could this be simplified?
- [ ] Are error messages clear?
- [ ] Is complex code well-commented?
- [ ] Performance implications for deployment speed?

### When NOT to Trust AI

Always require human validation for:
- **Security architecture** - Humans must review auth/authz flows
- **Business logic** - Domain expertise required
- **Performance optimization** - Context-specific tuning needed
- **Complex algorithms** - Test thoroughly, verify correctness
- **Compliance requirements** - Legal/regulatory needs human judgment
- **Strategic decisions** - Market positioning, partnerships, direction

### Maintain AI Context

**Keep Updated:**
- `AGENTS.md` - AI integration patterns and context
- Architecture documentation for AI reference
- Code pattern examples
- Common business scenarios

**Update When:**
- New features added
- Architecture changes
- Business requirements evolve
- Development patterns established

---

## 17. Conclusion & Evolution

This workflow is specifically designed for small team development with rapid iteration, balancing speed with professional quality standards.

### Key Adaptations

**From Standard GitFlow:**
- Simplified for single maintainer + contributors
- Realistic AI integration (assists, doesn't drive)
- Business-focused validation throughout
- Performance requirements embedded in process
- Professional standards at every checkpoint

### Success Factors

1. **Business focus** in all development decisions
2. **Streamlined processes** for velocity
3. **AI as supplement** not replacement
4. **Complete documentation** for transparency
5. **Continuous improvement** based on metrics

### Document Evolution

This is a living document:
- Review quarterly for relevance
- Update based on team feedback
- Adapt to changing business needs
- Incorporate lessons learned
- Maintain practical utility

**Remember:** Process serves the team and users, not vice versa. If something blocks progress or doesn't make sense, speak up. We'll adapt together.

---

**Document Version:** 3.1.0  
**Last Updated:** September 30, 2025  
**Maintained By:** Clem and ClaudeAI Sonnet 4  
**Context:** Business-in-a-Box with realistic AI integration  
**Questions?** Open an issue or ask in #engineering

---

**Changelog:**
- v3.1.0: Merged v3 business context with v2 practical templates; added embedded AI tips; restored documentation categories; comprehensive tooling section; complete ready-to-use templates
- v3.0.0: Tailored for project context, realistic AI integration
- v2.0.0: Added AI workflow integration, templates, documentation categories  
- v1.0.0: Initial GitFlow documentation