# Our Development Workflow: A Complete Gitflow Guide

## 1. Philosophy & Guiding Principles

This document outlines our Gitflow methodology and development lifecycle. Our goal is to maintain a predictable, high-quality, and stable codebase. Every process described here is in service of these four principles:

* **🛡️ Stability:** The `main` branch is always in a production-ready state. It is our unbreakable source of truth.
* **🚀 Quality:** Quality is not an afterthought; it is built into every step through mandatory testing, automated checks, and peer review.
* **🤝 Clarity:** The state of the project, the history of changes, and the purpose of all work-in-progress is always transparent.
* **💨 Velocity:** By creating a safe and predictable process, we empower developers to work efficiently and confidently on isolated features.

### Our AI-Augmented Workflow

We leverage AI agents (Claude, GitHub Copilot, Cursor, etc.) throughout our development lifecycle. This workflow is designed to make both human developers and AI assistants maximally effective by:
- Providing explicit context in issues and documentation
- Maintaining clear, machine-readable commit history
- Ensuring all code context is discoverable and well-documented

---

## 2. The Branching Strategy

We use a core branching model based on Gitflow, with two main long-lived branches and several supporting, short-lived branches.

### Main Branches

#### `main`
* **Purpose:** Contains production-ready code. This branch represents the official release history.
* **Rules:**
    * Code in `main` **must** be deployable at all times.
    * Direct commits are **strictly forbidden**.
    * Code only gets into `main` by merging from a `release/*` or a `hotfix/*` branch.
    * Each merge to `main` **must** be tagged with a version number (e.g., `v1.2.0`).
    * **⚙️ VARIABLE:** Branch protection rules should be configured to require:
        * ✅ **RECOMMENDED:** At least 1 approval (2+ for larger teams)
        * ✅ **RECOMMENDED:** All CI checks must pass
        * ✅ **REQUIRED:** No direct pushes (even from admins)

#### `develop`
* **Purpose:** The primary integration branch. It contains the latest delivered development changes for the next release. This can be considered the "nightly build."
* **Rules:**
    * While generally stable, it may contain features that are not yet complete or fully tested in an integrated environment.
    * Direct commits are **forbidden**.
    * Code only gets into `develop` by merging from a `feature/*` branch.
    * **⚙️ VARIABLE:** Branch protection rules should require:
        * ✅ **RECOMMENDED:** At least 1 approval
        * ✅ **REQUIRED:** All CI checks must pass

### Supporting Branches

#### `feature/*`
* **Purpose:** For developing new features or non-critical bug fixes.
* **Branches From:** `develop`
* **Merges To:** `develop`
* **Naming Convention:** `feature/issue-123-short-description` (e.g., `feature/gh-42-user-login-form`)
* **⚙️ VARIABLE: Maximum Lifespan:** 
    * ✅ **RECOMMENDED:** 3-5 business days before merging
    * **Rationale:** Longer-lived branches increase merge conflicts and reduce collaboration. If a feature takes longer, consider breaking it into smaller pieces or using feature flags.
* **Deletion:** Automatically deleted after merge (configure in GitHub/GitLab settings)

#### `release/*`
* **Purpose:** To prepare for a new production release. This branch is for final testing, documentation generation, and minor bug fixes. No new features are added here.
* **Branches From:** `develop`
* **Merges To:** `main` (for release) AND `develop` (to incorporate bug fixes)
* **Naming Convention:** `release/v1.2.0`
* **⚙️ VARIABLE: Lifespan:**
    * ✅ **RECOMMENDED:** 1-2 days maximum
    * **Rationale:** Releases should stabilize quickly. Extended release branches indicate insufficient testing in develop or oversized releases.

#### `hotfix/*`
* **Purpose:** To address a critical bug in the current production version (`main`). This is the only branch that can be created directly from `main`.
* **Branches From:** `main`
* **Merges To:** `main` AND `develop` (or current `release/*` if one exists)
* **Naming Convention:** `hotfix/v1.2.1-critical-auth-bug` or `hotfix/issue-124-critical-auth-bug`
* **⚙️ VARIABLE: Definition of "Critical":**
    * ✅ **RECOMMENDED:** Use hotfixes only for:
        * Security vulnerabilities
        * Data loss or corruption bugs
        * Complete system unavailability
        * Critical business function failures
    * **Rationale:** Overusing hotfixes bypasses quality gates. Most bugs can wait for the next regular release.

### Branch Flow Diagram

```
main      ─────●────────────────●─────────●──────
               ↑                ↑         ↑
               │(merge)         │         │
release        └──●─────●───────┘         │
                  ↑     ↑                 │
                  │     │(bug fixes)      │
                  │     ↓                 │
develop   ──●─────●─────●──●──●──●───────●───●──
            ↑           ↑  ↑  ↑           ↑
            │           │  │  │           │
feature     └──●──●─────┘  │  └──●──●─────┘
                           │
hotfix                     └─────────────────────┘
                           (emergency only)
```

---

## 3. The Feature Development Lifecycle (Step-by-Step)

This is the standard workflow for any new feature, improvement, or non-critical bug fix.

### Phase 1: Preparation

**1. Select an Issue**
Find an issue in the backlog that meets the **Definition of Ready** (see Section 8.C). This ensures the task is well-defined with clear acceptance criteria and has all necessary context for both human developers and AI assistants.

**2. Review Context & Architecture**
Before writing code, review all materials linked in the issue:
- Architecture diagrams and design documents
- Relevant code files and modules
- API specifications and data schemas
- Related existing features or similar implementations

**💡 AI Tip:** Share these context documents with your AI assistant at the start of your session to ensure it understands the system architecture and coding patterns.

**3. Sync Local Repository**
Ensure your local `develop` branch is perfectly in sync with the remote.
```bash
git checkout develop
git pull origin develop
```

**4. Create a Feature Branch**
Create your new branch from the up-to-date `develop` branch.
```bash
git checkout -b feature/gh-42-user-login-form
```

### Phase 2: Development

**5. Push Initial Branch & Open Draft PR**
Immediately push your new branch and open a **Draft Pull Request** on GitHub/GitLab.
```bash
git push -u origin feature/gh-42-user-login-form
```
**Rationale:** Early visibility allows the CI pipeline to run against your initial commits and lets teammates know what you're working on. It also creates a place for early feedback and questions.

**6. The TDD Loop (Red-Green-Refactor)**
* **Write a Failing Test:** Before writing implementation code, write an automated test that defines the new functionality.
* **Confirm It Fails:** Run the test suite and confirm your new test fails for the correct reason.
* **Write the Code:** Write the simplest possible code to make the test pass.
* **Confirm It Passes:** Run the test suite again to confirm your new test (and all others) passes.
* **Refactor:** Clean up your code, improve its structure, and ensure it adheres to our style guides.

**💡 AI Tip:** AI assistants excel at generating test cases. Describe the feature requirements and ask your AI to generate comprehensive test scenarios, including edge cases.

**⚙️ VARIABLE: Testing Requirements**
* ✅ **RECOMMENDED MINIMUM:**
    * Unit test coverage: 80%+ for new code
    * Integration tests for API endpoints
    * E2E tests for critical user flows
* **Rationale:** Balance between quality and velocity. 100% coverage has diminishing returns; focus on business-critical paths.

**7. Commit Your Work**
Make small, logical commits using the **Conventional Commits** standard (see Section 8.A).
```bash
git add .
git commit -m "feat(auth): add email and password validation"
```

**⚙️ VARIABLE: Commit Frequency**
* ✅ **RECOMMENDED:** Commit every 30-60 minutes of focused work, or whenever a logical unit is complete
* **Rationale:** Frequent commits make it easier to revert specific changes and understand the evolution of the code.

**8. Keep Your Branch Updated**
Periodically (at least daily), rebase your branch on the latest `develop` to incorporate changes from other developers.
```bash
git pull --rebase origin develop
```
**Rationale:** Frequent rebasing prevents massive conflicts at PR time and ensures your feature works with the latest code.

### Phase 3: Code Review

**9. Finalize & Submit for Review**

* **Run Full Test Suite Locally:** Ensure all tests pass on your machine.
* **Update All Relevant Documentation:** This is **mandatory**. Review the documentation checklist:
  
  **📚 User Documentation** (if user-facing changes):
  - [ ] User Guides / User Manuals
  - [ ] Getting Started / Tutorials
  - [ ] FAQs
  - [ ] Release Notes (draft)
  
  **👨‍💻 Developer Documentation** (if technical changes):
  - [ ] API Reference / OpenAPI specs
  - [ ] Architecture diagrams
  - [ ] Code comments for complex logic
  - [ ] README.md (if setup changes)
  
  **⚙️ Administrator/Operations Documentation** (if deployment/config changes):
  - [ ] Installation & Deployment Guide
  - [ ] Configuration Guide
  - [ ] Troubleshooting Guide
  - [ ] Monitoring & Alerting setup

* **Clean Up History:** Use interactive rebase to squash minor "fixup" or "wip" commits into logical, well-described commits.
    ```bash
    git rebase -i origin/develop
    ```
* **Self-Review:** Review your own PR as if you were the reviewer. Check for:
    * Debugging statements left in code
    * TODO comments that should be addressed
    * Unnecessary commented-out code
    * Sensitive data (API keys, passwords)
    * Adherence to project conventions

* **Mark as Ready:** Change the Pull Request from "Draft" to "Ready for Review."

* **Complete the PR Template:** Fill out our standardized PR template (see Section 15.B) completely. A well-written PR description significantly speeds up review.

**10. The Review Process**

* **Automated Checks (CI):** The PR will be blocked from merging until all CI checks pass:
    * Unit and integration tests
    * Linting and code formatting
    * Security vulnerability scanning
    * Build verification
    * **⚙️ VARIABLE:** Code coverage check (recommended: no decrease in overall coverage)

* **Human Review:** 
    * **⚙️ VARIABLE: Number of Approvals Required:**
        * ✅ **RECOMMENDED:** 1 approval for teams <10 developers
        * ✅ **RECOMMENDED:** 2 approvals for teams 10+ or critical systems
    * **⚙️ VARIABLE: Auto-Assignment:**
        * Use a `CODEOWNERS` file to automatically assign reviewers based on changed files
        * **Rationale:** Ensures domain experts review their areas
    * **⚙️ VARIABLE: Review Turnaround SLA:**
        * ✅ **RECOMMENDED:** First response within 4 business hours
        * ✅ **RECOMMENDED:** Full review within 24 business hours
        * **Rationale:** Slow reviews block progress and discourage small PRs

* **What Reviewers Check:**
    * Logic correctness and edge cases
    * Code readability and maintainability
    * Adherence to project patterns and conventions
    * Security concerns
    * Performance implications
    * Test quality and coverage
    * **Documentation completeness**

* **Address Feedback:** The author is responsible for addressing all comments by pushing new commits to the feature branch. Use:
    ```bash
    git commit -m "fix: address review feedback - handle null case"
    ```

**💡 AI Tip:** When addressing review feedback, you can share the reviewer's comments with your AI assistant to get suggestions for improvements or alternative approaches.

**11. Approval & Merge**

* Once the reviewer(s) approve and all checks pass, **the author** merges the PR into `develop`.
* **⚙️ VARIABLE: Who Can Merge:**
    * ✅ **RECOMMENDED:** Authors merge their own PRs after approval
    * **Rationale:** Empowers developers and reduces bottlenecks. Reviewers shouldn't need to merge.
* **⚙️ VARIABLE: Merge Strategy:**
    * ✅ **RECOMMENDED:** Squash and merge for feature branches
    * **Rationale:** Keeps `develop` history clean with one commit per feature
    * ❌ **AVOID:** Basic merge (creates messy history)
* The feature branch should be deleted automatically upon merging (configure in repo settings).
* The associated issue is automatically closed (use "Closes #123" in PR description).

---

## 4. The Release Process

**⚙️ VARIABLE: Release Cadence**
* ✅ **RECOMMENDED OPTIONS:**
    * **Sprint-based:** Every 2 weeks (predictable, good for stakeholder planning)
    * **Continuous:** Release when enough features are ready (flexible, faster feedback)
    * **Scheduled:** Weekly on specific day (balanced approach)
* **Rationale:** Choose based on your deployment complexity and business needs. Frequent releases reduce risk per release.

### Step-by-Step Release Workflow

**1. Decide to Cut a Release**
* **⚙️ VARIABLE: Who Decides:**
    * ✅ **RECOMMENDED:** Product Owner + Tech Lead consensus
    * Check that `develop` has:
        * Sufficient features to justify a release
        * No known critical bugs
        * All planned features for this sprint/cycle

**2. Create Release Branch**
```bash
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0
git push -u origin release/v1.2.0
```

**3. Bump Version Number**
Update version in all relevant files:
* `package.json` (Node.js)
* `pyproject.toml` or `setup.py` (Python)
* `pom.xml` (Java)
* `Cargo.toml` (Rust)
* Any version constants in code

**How to Choose Version Number (SemVer):**
* **MAJOR (1.x.x → 2.0.0):** Breaking changes, incompatible API changes
* **MINOR (1.2.x → 1.3.0):** New features, backwards-compatible
* **PATCH (1.2.0 → 1.2.1):** Bug fixes, backwards-compatible

```bash
# Example for Node.js
npm version minor  # Automatically updates package.json and creates commit
git push
```

**4. Stabilization Period**
On the release branch:
* ✅ **ALLOWED:** Bug fixes
* ✅ **ALLOWED:** Documentation improvements
* ✅ **ALLOWED:** Release notes preparation
* ✅ **ALLOWED:** Configuration tweaks
* ❌ **FORBIDDEN:** New features
* ❌ **FORBIDDEN:** Refactoring

**⚙️ VARIABLE: Stabilization Activities**
* Run full regression test suite
* Perform manual QA testing
* Deploy to staging environment
* **OPTIONAL:** Deploy to canary environment (for large systems)
* **OPTIONAL:** Run performance/load tests
* Generate or update CHANGELOG.md
* Prepare release announcement

**5. Merge to `main`**
```bash
git checkout main
git pull origin main
git merge --no-ff release/v1.2.0
git push origin main
```
**Note:** The `--no-ff` flag creates a merge commit, preserving the release branch history.

**6. Tag the Release**
```bash
git tag -a v1.2.0 -m "Release version 1.2.0 - User authentication & dashboard improvements"
git push origin v1.2.0
```
**⚙️ VARIABLE: Tag Annotation**
* ✅ **RECOMMENDED:** Include high-level summary of changes in tag message
* **Rationale:** Makes `git tag -n` output useful

**7. Merge Back to `develop`**
Ensure any bug fixes made during stabilization are incorporated into future development.
```bash
git checkout develop
git pull origin develop
git merge --no-ff release/v1.2.0
git push origin develop
```

**8. Delete Release Branch**
```bash
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

**9. Deploy to Production**
**⚙️ VARIABLE: Deployment Trigger**
* ✅ **RECOMMENDED:** Automatic deployment triggered by new tag on `main`
* **Alternative:** Manual deployment with approval gate
* **Rationale:** Automation reduces human error and enables rapid rollback

Your CI/CD pipeline should:
1. Detect the new tag
2. Build production artifacts
3. Run deployment smoke tests
4. Deploy to production
5. Run post-deployment health checks
6. Send notifications to team

**10. Monitor & Announce**
* Monitor error rates, performance metrics, and user feedback
* Announce release to stakeholders
* Update project management tools (Jira, Linear, etc.)

---

## 5. The Hotfix Lifecycle

**IMPORTANT:** Hotfixes bypass normal quality gates and should be used sparingly.

### When to Use Hotfix vs Regular Fix

**Use Hotfix When:**
* Production is down or severely degraded
* Security vulnerability is actively being exploited
* Data is being lost or corrupted
* Critical business function is completely broken
* Financial impact is immediate and severe

**Use Regular Feature Branch When:**
* Bug affects only some users
* Workaround exists
* Impact is moderate or low
* Can wait for next scheduled release (even if just a few days)

### Step-by-Step Hotfix Workflow

**1. Assess & Communicate**
```bash
# Announce in team chat:
# "🚨 HOTFIX IN PROGRESS: Critical auth bug allowing unauthorized access.
# Working on hotfix/v1.2.1-fix-auth-bypass. ETA: 2 hours"
```

**2. Create Hotfix Branch from `main`**
```bash
git checkout main
git pull origin main
git checkout -b hotfix/v1.2.1-fix-auth-bypass
git push -u origin hotfix/v1.2.1-fix-auth-bypass
```

**3. Fix the Bug**
* Make the minimal change necessary to fix the issue
* Add a test that would have caught this bug
* **DO NOT** include unrelated improvements or refactoring

```bash
git commit -m "fix(auth): prevent authorization bypass in JWT validation"
```

**💡 AI Tip:** When debugging critical issues, AI assistants can help analyze logs, suggest root causes, and generate test cases that reproduce the bug.

**4. Test Thoroughly**
* All existing tests must pass
* New test(s) must demonstrate the fix
* **⚙️ VARIABLE:** Consider requiring manual QA approval for hotfixes
* **OPTIONAL:** Deploy to staging for verification

**5. Expedited Review**
* Open PR immediately (not draft)
* Tag reviewers explicitly
* **⚙️ VARIABLE: Hotfix Review Requirements:**
    * ✅ **RECOMMENDED:** 1 approval (even for teams that normally require 2)
    * ✅ **RECOMMENDED:** Can be approved by any senior developer
    * **Rationale:** Speed is critical, but we still need a second pair of eyes

**6. Merge to `main`**
```bash
git checkout main
git merge --no-ff hotfix/v1.2.1-fix-auth-bypass
git push origin main
```

**7. Tag with Patch Version**
```bash
git tag -a v1.2.1 -m "Hotfix: Fix authentication bypass vulnerability"
git push origin v1.2.1
```

**8. Merge to `develop` (or current release branch)**
```bash
# If a release branch exists, merge to both:
git checkout release/v1.3.0  # if it exists
git merge --no-ff hotfix/v1.2.1-fix-auth-bypass

# Always merge to develop:
git checkout develop
git merge --no-ff hotfix/v1.2.1-fix-auth-bypass
git push origin develop
```

**9. Delete Hotfix Branch**
```bash
git branch -d hotfix/v1.2.1-fix-auth-bypass
git push origin --delete hotfix/v1.2.1-fix-auth-bypass
```

**10. Deploy & Monitor**
* CI/CD should auto-deploy the new tag
* Monitor closely for 1-2 hours
* Prepare rollback plan (see Section 9)

**11. Post-Mortem**
**⚙️ VARIABLE: Post-Incident Review**
* ✅ **RECOMMENDED:** Required for all hotfixes
* Schedule within 48 hours
* Focus on:
    * Root cause analysis
    * Why wasn't this caught earlier?
    * What process improvements prevent recurrence?
* **NO BLAME CULTURE** - focus on systems, not individuals

---

## 6. Conflict Resolution

Merge conflicts are inevitable. Here's how to handle them professionally.

### During Rebase (Most Common)

**Scenario:** You run `git pull --rebase origin develop` and hit conflicts.

```bash
# Git will pause and show which files have conflicts
git status

# Open conflicted files and resolve them manually
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# After resolving each file:
git add path/to/resolved-file.js

# Continue the rebase:
git rebase --continue

# If you get stuck or make a mistake:
git rebase --abort  # starts over from before rebase
```

**💡 AI Tip:** When resolving complex conflicts, share both versions with your AI assistant and ask it to help reconcile the changes while preserving functionality from both sides.

**Best Practices:**
* Resolve conflicts in small chunks, don't try to do everything at once
* Run tests after resolving to ensure nothing broke
* When in doubt, ask the author of the conflicting code

### During PR Merge

**Scenario:** GitHub/GitLab shows "This branch has conflicts that must be resolved."

**Option 1: Rebase Your Branch (Preferred)**
```bash
git checkout feature/your-branch
git pull --rebase origin develop
# Resolve conflicts as above
git push --force-with-lease origin feature/your-branch
```

**Option 2: Merge develop into Your Branch**
```bash
git checkout feature/your-branch
git merge origin/develop
# Resolve conflicts
git commit
git push origin feature/your-branch
```

**⚙️ VARIABLE: Conflict Resolution Strategy**
* ✅ **RECOMMENDED:** Option 1 (rebase) - keeps history cleaner
* **ACCEPTABLE:** Option 2 (merge) - easier for beginners, but creates merge commits
* **Rationale:** Rebasing maintains linear history but requires force-push (safe with `--force-with-lease`)

### When Multiple Features Conflict

**Scenario:** Two developers' features both change the same file significantly.

**Process:**
1. First feature to be reviewed gets merged normally
2. Second feature author rebases on updated `develop`
3. Second author resolves conflicts with knowledge of first feature
4. **OPTIONAL:** Brief sync call between both developers to discuss resolution
5. Second feature proceeds through normal review

**⚙️ VARIABLE: Large Conflict Prevention**
* ✅ **RECOMMENDED:** Hold daily 5-minute standups where devs mention which files they're touching
* ✅ **RECOMMENDED:** Use feature flags to merge incomplete features early
* **Rationale:** Prevention is better than resolution

---

## 7. Rollback & Emergency Procedures

### When to Rollback

**Immediate rollback if:**
* Application is completely down
* Data corruption is occurring
* Security breach is active
* Critical business function is broken for all users

**Monitor and decide if:**
* Increased error rate (e.g., 2x normal)
* Performance degradation (e.g., 50% slower)
* Affecting subset of users

### Rollback Process

**Option 1: Deploy Previous Version (Fastest)**
```bash
# Find the previous working tag
git tag --sort=-creatordate | head -n 5

# Deploy that tag through your CI/CD
# Example for manual deployment:
git checkout v1.2.0  # the last known good version
./deploy.sh production
```

**Option 2: Revert Commit**
```bash
git checkout main
git revert <commit-hash>  # creates new commit that undoes changes
git tag -a v1.2.2 -m "Revert v1.2.1 due to critical bug"
git push origin main --tags
```

**Option 3: Emergency Hotfix**
If you know the fix and it's quick (< 30 minutes), follow the hotfix process (Section 5).

**⚙️ VARIABLE: Rollback Authority**
* ✅ **RECOMMENDED:** On-call engineer can initiate rollback without approval
* ✅ **RECOMMENDED:** Must notify team immediately in #incidents channel
* **Rationale:** Speed is critical; trust your on-call engineers

### Post-Rollback

1. Investigate root cause
2. Create issue to track proper fix
3. Schedule post-mortem (mandatory)
4. Update runbooks if process could be improved

---

## 8. Supporting Principles & Definitions

### A. Conventional Commits

We use the Conventional Commits specification to create an explicit and machine-readable commit history.

**Format:** `type(scope): subject`

**Types:**
* **`feat`:** A new feature
* **`fix`:** A bug fix
* **`docs`:** Documentation only changes
* **`style`:** Code style changes (formatting, missing semicolons, etc.)
* **`refactor`:** A code change that neither fixes a bug nor adds a feature
* **`perf`:** A code change that improves performance
* **`test`:** Adding missing tests or correcting existing tests
* **`build`:** Changes to build system or dependencies
* **`ci`:** Changes to CI configuration files and scripts
* **`chore`:** Other changes that don't modify src or test files

**Examples:**
```bash
feat(auth): add OAuth2 login support
fix(api): handle null response in user endpoint
docs(readme): update installation instructions
refactor(utils): simplify date formatting logic
test(auth): add unit tests for password validation
```

**⚙️ VARIABLE: Enforcement**
* ✅ **RECOMMENDED:** Use a git hook (commitlint) to enforce format
* **OPTIONAL:** Require conventional commit format in PR title
* **Rationale:** Consistency enables automated CHANGELOG generation and helps both humans and AI understand code history

### B. Semantic Versioning (SemVer)

All tags on `main` must follow SemVer: `MAJOR.MINOR.PATCH`

* **MAJOR (1.x.x → 2.0.0):** Incompatible API changes, breaking changes
* **MINOR (1.2.x → 1.3.0):** New features, backwards-compatible functionality
* **PATCH (1.2.3 → 1.2.4):** Bug fixes, backwards-compatible fixes

**Pre-release versions:**
* `1.3.0-alpha.1` - early testing
* `1.3.0-beta.2` - feature complete, testing phase
* `1.3.0-rc.1` - release candidate

**⚙️ VARIABLE: Version Zero (0.x.x)**
* During initial development, you can use `0.x.x` versions
* In 0.x.x, MINOR acts like MAJOR (breaking changes allowed)
* Move to 1.0.0 when API is stable enough for public use

### C. Definition of Ready (DoR)

An issue is "Ready" when:
- [ ] It has a clear, descriptive title
- [ ] The user story follows format: "As a [role], I want [feature], so that [benefit]"
- [ ] Acceptance criteria are well-defined and testable
- [ ] **Context for AI Agents & Developers is provided** (see template in Section 15.A):
  - [ ] Links to relevant architecture docs
  - [ ] Key code files that will be affected
  - [ ] API schemas or data models
  - [ ] Design mockups or wireframes (for UI work)
- [ ] Any required design mockups or technical specifications are attached
- [ ] Dependencies on other issues are documented
- [ ] It is small enough to be completed within **⚙️ VARIABLE:** 3-5 days
- [ ] Technical approach has been discussed (for complex tasks)

**⚙️ VARIABLE: Size Threshold**
* ✅ **RECOMMENDED:** Story points: 1-5 (if using points), or max 3-5 days of work
* **Rationale:** Smaller issues reduce risk and enable faster feedback. They're also easier for AI assistants to reason about completely.

### D. Definition of Done (DoD)

A feature is "Done" when:
- [ ] All acceptance criteria have been met
- [ ] Code has been merged into the `develop` branch
- [ ] All automated CI checks (tests, linting, security) have passed
- [ ] **⚙️ VARIABLE:** Code coverage is at or above **X%** (recommend: 80%)
- [ ] **All relevant documentation has been updated:**
  - [ ] User Documentation (if user-facing changes)
  - [ ] Developer Documentation (if technical/API changes)
  - [ ] Administrator/Ops Documentation (if deployment/config changes)
- [ ] Code has been successfully deployed to staging environment
- [ ] **⚙️ VARIABLE:** Manual QA testing has been performed (if required)
- [ ] **⚙️ VARIABLE:** Product Owner has accepted the feature (if required)
- [ ] No known bugs or regressions introduced

### E. CODEOWNERS

The `CODEOWNERS` file automatically assigns reviewers based on which files changed.

**Example `.github/CODEOWNERS`:**
```
# Default owners for everything
* @team-leads

# Frontend code
/src/components/** @frontend-team @jane-doe
/src/styles/** @frontend-team

# Backend API
/src/api/** @backend-team @john-smith
/src/database/** @backend-team @dba-team

# Infrastructure
/.github/workflows/** @devops-team
/docker/** @devops-team
/terraform/** @devops-team

# Documentation
/docs/** @tech-writers @product-team
README.md @tech-writers
```

**Rationale:** Ensures domain experts review relevant changes automatically.

### F. Environments

**⚙️ VARIABLE: Environment Strategy**

We maintain the following environments:

1. **Local Development**
   * Each developer's machine
   * Uses local database/mock services
   * Fast iteration, no deployment process

2. **Staging**
   * Mirrors production configuration
   * Automatically deployed from `develop` branch
   * Used for QA, integration testing, and demos
   * **⚙️ VARIABLE:** Deploy on every merge to `develop` OR nightly

3. **Production**
   * Customer-facing environment
   * Deployed only from tagged releases on `main`
   * Monitored 24/7

**OPTIONAL:**
4. **Preview/PR Environments**
   * Ephemeral environment per PR
   * Allows testing features in isolation
   * Automatically destroyed when PR is merged/closed

5. **Canary**
   * Receives production traffic gradually (e.g., 5% of users)
   * Used to validate releases before full rollout
   * Only for high-scale systems

---

## 9. Troubleshooting & Common Scenarios

### "I accidentally committed to `develop` directly"

**If you haven't pushed yet:**
```bash
# Move your commit(s) to a new feature branch
git branch feature/my-accidental-work
git reset --hard origin/develop
git checkout feature/my-accidental-work
# Now open a PR normally
```

**If you already pushed:**
```bash
# This requires admin privileges to force-push to develop
# Contact a team lead immediately
# They will:
git checkout develop
git reset --hard origin/develop~1  # undo last commit
git push --force
# Then you create proper feature branch from your work
```

### "My feature branch is 100+ commits behind `develop`"

```bash
git checkout feature/my-branch
git pull --rebase origin develop
# Likely many conflicts - resolve them carefully
# Consider pair programming with another dev for this

# Alternative if rebase is too painful:
git checkout develop
git pull
git checkout -b feature/my-branch-rebased
git merge --squash feature/my-branch
git commit -m "feat: complete feature description"
# Open new PR, close old one
```

**Prevention:** Rebase at least daily.

### "CI passes locally but fails in CI/CD"

Common causes:
1. **Different Node/Python/etc. versions**
   * Solution: Use version managers (nvm, pyenv) to match CI version
2. **Environment variables missing**
   * Solution: Check `.env.example`, ensure all vars are in CI secrets
3. **Tests depend on local state**
   * Solution: Ensure tests clean up after themselves, use fresh test DB
4. **Timezone differences**
   * Solution: Use UTC in tests, mock time consistently

**Debug process:**
```bash
# Run tests exactly as CI does:
docker run -it node:18 bash
# Clone repo, install deps, run tests
# This replicates CI environment locally
```

**💡 AI Tip:** Share CI logs with your AI assistant to help diagnose failures faster.

### "I need to abandon this feature branch"

```bash
git checkout develop
git branch -D feature/abandoned-feature  # local delete
git push origin --delete feature/abandoned-feature  # remote delete
# Close the PR with explanation
# Move issue back to backlog or close it
```

### "Two developers need to work on one feature"

**Approach 1: Pair Programming (Preferred)**
* Both devs work together on one machine (or screen share)
* One types, one thinks/reviews
* Switch roles every 30 minutes
* **Works great with AI:** One person prompts the AI, the other reviews its suggestions

**Approach 2: Shared Feature Branch**
```bash
# Dev 1 creates the branch
git checkout -b feature/shared-feature

# Dev 2 checks it out
git fetch
git checkout feature/shared-feature

# Both devs:
# - Pull frequently: git pull --rebase
# - Communicate about which files they're editing
# - Commit frequently to avoid conflicts
# - Push frequently so partner sees changes
```

**Approach 3: Sub-branches (Complex Features)**
```bash
# Main feature branch
git checkout -b feature/large-feature

# Dev 1 creates sub-branch
git checkout -b feature/large-feature-part1

# Dev 2 creates sub-branch
git checkout -b feature/large-feature-part2

# Sub-branches merge to feature/large-feature
# Main feature branch merges to develop
```

### "My reviewer is unresponsive"

**After 24 business hours:**
1. Politely ping in PR comments: "@reviewer friendly reminder on this PR"
2. Message them directly in Slack/Teams
3. After 48 hours, request different reviewer in team channel
4. **⚙️ VARIABLE:** Team policy:
   * ✅ **RECOMMENDED:** Any senior dev can step in as backup reviewer after 48 hours
   * **Rationale:** Prevents single point of failure

### "CI is taking forever / timing out"

**Short-term:**
* Retry the job (might be transient infrastructure issue)
* Check if tests can be run in parallel
* Consider splitting test suites

**Long-term:**
* **⚙️ VARIABLE: Test Suite Timeout:** 15 minutes max (recommended)
* If tests take longer:
  * Run unit tests on every commit
  * Run integration/E2E tests nightly or on `develop` only
  * Use test sharding

---

## 10. Process Exceptions

You **MAY SKIP** the full PR process for:

### Minor Documentation Changes
* Typos in comments or markdown
* Formatting fixes
* Broken links
* **⚙️ VARIABLE:** Still require 1 approval OR allow direct commit to a `docs` branch
* **Recommendation:** Still use PRs; they're fast for docs and provide history

### Emergency Security Patches
* Follow hotfix process but may skip approval if:
  * Vulnerability is actively being exploited
  * Senior engineer reviews after merge
* **Document exception in commit message**

### Automated Dependency Updates
* Dependabot/Renovate PRs for patch updates
* **⚙️ VARIABLE:** Auto-merge if:
  * CI passes
  * Only patch version bumps (not minor/major)
  * From trusted sources
* **Recommendation:** Still manually review minor/major updates

### Reverts
* If a merged PR breaks something, you may immediately revert
```bash
git revert <commit-hash>
git push
```
* Open revert PR, can be merged with just 1 approval
* Still must follow hotfix process for the proper fix

**NEVER SKIP PROCESS FOR:**
* Code changes
* Dependency major/minor upgrades
* Configuration changes affecting production
* Database migrations
* API changes

---

## 11. Quick Reference

### Starting New Feature
```bash
git checkout develop && git pull
git checkout -b feature/gh-123-short-name
git push -u origin feature/gh-123-short-name
# Open Draft PR immediately
```

### Daily Updates
```bash
git pull --rebase origin develop
git push --force-with-lease
```

### Before Submitting PR
```bash
# Clean up history
git rebase -i origin/develop

# Run full test suite
npm test  # or pytest, cargo test, etc.

# Check for issues
npm run lint
npm run type-check

# Mark PR as ready for review
```

### Merge After Approval
```bash
# Use GitHub/GitLab UI: "Squash and merge"
# Or manually:
git checkout develop
git merge --squash feature/gh-123-short-name
git commit
git push
git branch -d feature/gh-123-short-name
git push origin --delete feature/gh-123-short-name
```

### Hotfix
```bash
git checkout main && git pull
git checkout -b hotfix/v1.2.1-description
# Make minimal fix + test
git commit -m "fix: critical issue description"
# Open PR, expedited review
git checkout main && git merge --no-ff hotfix/...
git tag -a v1.2.1 -m "Hotfix description"
git push --tags
git checkout develop && git merge --no-ff hotfix/...
```

### Release
```bash
git checkout develop && git pull
git checkout -b release/v1.3.0
# Bump version in package.json, etc.
# Stabilize, test, prepare docs
git checkout main && git merge --no-ff release/v1.3.0
git tag -a v1.3.0 -m "Release notes summary"
git push origin main --tags
git checkout develop && git merge --no-ff release/v1.3.0
```

---

## 12. Tooling Recommendations

### Required Tools
* **Git:** Obviously
* **GitHub/GitLab/Bitbucket:** For PR reviews and CI/CD
* **CI/CD Pipeline:** GitHub Actions, GitLab CI, Jenkins, CircleCI
* **Branch Protection:** Configure on `main` and `develop`

### Recommended Tools

**Code Quality:**
* **Linter:** ESLint, Pylint, RuboCop, etc.
* **Formatter:** Prettier, Black, rustfmt
* **Type Checker:** TypeScript, mypy, flow

**Git Hooks (via Husky or pre-commit):**
* `pre-commit`: Run linter and formatter
* `commit-msg`: Enforce conventional commits (commitlint)
* `pre-push`: Run unit tests

**Security:**
* **Dependency Scanning:** Dependabot, Renovate, Snyk
* **Secret Scanning:** GitGuardian, TruffleHog
* **SAST:** SonarQube, CodeQL

**Automation:**
* **Auto-labeling:** Add labels to PRs based on changed files
* **Auto-assignment:** CODEOWNERS for reviewer assignment
* **Auto-merge:** Dependabot minor updates (with caution)
* **CHANGELOG Generation:** conventional-changelog, release-please

**AI Development Tools:**
* **AI Code Assistants:** GitHub Copilot, Cursor, Continue, Cody
* **AI Chat Interfaces:** Claude, ChatGPT, or team-specific AI setups
* **Code Review AI:** PR-Agent, CodeRabbit (supplementary to human review)

---

## 13. Metrics & Continuous Improvement

**⚙️ VARIABLE: Track These Metrics**

✅ **RECOMMENDED:**
* **Cycle Time:** Time from branch creation to merge (target: < 5 days)
* **PR Size:** Lines of code changed (target: < 400 lines)
* **Review Time:** Time from "ready for review" to approval (target: < 24 hours)
* **Deployment Frequency:** How often you release (target: at least weekly)
* **Change Failure Rate:** % of deployments causing issues (target: < 15%)
* **Time to Restore:** Time to fix broken production (target: < 1 hour)

**Use these metrics to identify bottlenecks, not to punish individuals.**

### Regular Process Reviews

**⚙️ VARIABLE: Review Cadence**
* ✅ **RECOMMENDED:** Quarterly retrospective on development process
* Questions to ask:
  * What's working well?
  * Where are we struggling?
  * Are our policies helping or hindering?
  * How effective are our AI tools?
  * What would we change?
* Update this document based on team feedback

---

## 14. Getting Help

**If you're stuck:**
1. Check this document
2. Ask in team chat: #engineering-help
3. Use your AI assistant for technical questions
4. Reach out to a senior developer for process questions
5. Schedule pairing session

**If you find a gap in this document:**
1. Open an issue: "Workflow docs don't cover X"
2. Suggest improvement in #process-improvement
3. Submit PR to improve these docs

**Remember:** This process serves us, not the other way around. If something doesn't make sense or is blocking you, speak up. We'll adapt.

---

## 15. Templates

### A. Issue Template (Feature Request)

Save as `.github/ISSUE_TEMPLATE/feature_request.md`:

```markdown
---
name: Feature Request
about: Suggest a new feature for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## User Story
As a [type of user], I want [goal], so that [benefit/value].

## Problem Statement
A clear and concise description of what the problem is.
Ex. "Users are frustrated when..."

## Proposed Solution
A clear and concise description of what you want to happen.

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Context for AI Agents & Developers 🤖
*Provide direct links to files, data schemas, architectural diagrams, or relevant code snippets that are essential for understanding this task. This context helps both AI assistants and human developers quickly understand the technical landscape.*

### Architecture & Design
- **System Architecture:** [Link to architecture diagram/doc]
- **Design Mockups:** [Link to Figma/design tool]
- **Technical Spec:** [Link to detailed technical specification]

### Code References
- **Key Files to Modify:**
  - `src/api/users/controller.js` - User CRUD operations
  - `src/auth/middleware.js` - Authentication logic
- **Related Features:** [Link to similar feature implementation]
- **Existing Patterns:** [Link to code that follows similar patterns]

### Data & APIs
- **Database Schema:**
  - `User` model: `id`, `email`, `role`, `createdAt`
  - `Session` model: `id`, `userId`, `token`, `expiresAt`
- **API Endpoints Involved:**
  - `POST /api/auth/login`
  - `GET /api/users/:id`
- **OpenAPI/Swagger Spec:** [Link to API documentation]

### Dependencies
- **Related Issues:** #123, #456
- **Blocked By:** #789
- **External Dependencies:** New OAuth2 provider integration

## Additional Context
Add any other context, screenshots, or examples about the feature request here.

## Definition of Ready Checklist
- [ ] User story is clear
- [ ] Acceptance criteria are testable
- [ ] Context and code references provided
- [ ] Dependencies documented
- [ ] Estimated to be completable in 3-5 days
```

### B. Pull Request Template

Save as `.github/pull_request_template.md`:

```markdown
## Title: [Use Conventional Commit Format]
<!-- Example: feat(auth): add OAuth2 login support -->
<!-- Example: fix(api): handle null user in profile endpoint -->
<!-- Example: docs(readme): update installation instructions -->

**Related Issue:** Closes #<issue_number>

---

## Summary of Changes

*Provide a clear and concise description of what you changed and why. What problem does this solve? How does it work?*

---

## Type of Change
<!-- Check all that apply -->
- [ ] 🆕 New feature (non-breaking change which adds functionality)
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation update
- [ ] 🎨 Code refactoring (no functional changes)
- [ ] ⚡ Performance improvement
- [ ] ✅ Test updates

---

## PR Checklist: Definition of Done

*Please check the boxes that apply. This PR will not be reviewed until all relevant boxes are checked.*

### Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors
- [ ] I have removed any debugging code, console.logs, or commented-out code

### Testing
- [ ] I have added new automated tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass locally with my changes
- [ ] I have tested edge cases and error scenarios
- [ ] **⚙️ Variable:** Code coverage has not decreased

### Documentation (Check all that apply)

#### 📚 User Documentation
- [ ] User Guides / User Manuals updated
- [ ] Getting Started / Tutorials updated
- [ ] FAQs updated
- [ ] Release notes drafted (for significant changes)
- [ ] N/A - No user-facing changes

#### 👨‍💻 Developer Documentation
- [ ] API Reference / OpenAPI specs updated
- [ ] Architecture diagrams updated
- [ ] Code comments added for complex logic
- [ ] README.md updated (if setup/build process changed)
- [ ] N/A - No developer documentation changes needed

#### ⚙️ Administrator/Operations Documentation
- [ ] Installation & Deployment Guide updated
- [ ] Configuration Guide updated
- [ ] Environment variables documented
- [ ] Migration guide created (for breaking changes)
- [ ] N/A - No deployment/configuration changes

---

## How to Test

*Provide step-by-step instructions on how the reviewer can test your changes. Include any setup steps or specific scenarios.*

1. Check out this branch: `git checkout feature/branch-name`
2. Install dependencies: `npm install` (if needed)
3. Run the application: `npm start`
4. Navigate to: [URL or specific page]
5. Perform action: [specific steps]
6. Expected result: [what should happen]

### Test Credentials (if applicable)
- Test user: `test@example.com` / `password123`
- Admin user: `admin@example.com` / `admin456`

---

## Screenshots or GIFs (if applicable)

*If you made any UI changes, please provide screenshots or a GIF/video to demonstrate them.*

### Before
[Screenshot of old behavior]

### After
[Screenshot of new behavior]

---

## Breaking Changes (if applicable)

*If this PR introduces breaking changes, please describe:*
- What breaks
- Migration path for existing users
- Deprecation timeline (if applicable)

---

## Performance Impact (if applicable)

*If this PR has performance implications, please describe:*
- [ ] Performance improves
- [ ] No significant performance impact
- [ ] Performance degrades (with justification)
- [ ] Load testing performed

---

## Security Considerations (if applicable)

*If this PR has security implications, please describe:*
- [ ] No sensitive data exposed
- [ ] Authentication/authorization properly implemented
- [ ] Input validation added
- [ ] Security scan passed

---

## Additional Context

*Add any other context about the pull request here. Links to related PRs, design decisions, alternative approaches considered, etc.*

---

## Reviewer Notes

*Anything specific you want reviewers to focus on?*

---

## Post-Merge Checklist
<!-- To be completed by author after merge -->
- [ ] Issue closed automatically (via "Closes #X")
- [ ] Feature branch deleted
- [ ] Staging deployment verified
- [ ] Stakeholders notified (if needed)
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
A clear and concise description of what the bug is.

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
A clear and concise description of what you expected to happen.

## Actual Behavior
A clear and concise description of what actually happened.

## Screenshots or Error Messages
If applicable, add screenshots or paste error messages to help explain your problem.

```
[Paste error logs here]
```

## Environment
- **OS:** [e.g., macOS 13.0, Windows 11, Ubuntu 22.04]
- **Browser:** [e.g., Chrome 120, Firefox 121, Safari 17]
- **App Version:** [e.g., v1.2.3]
- **Environment:** [e.g., Production, Staging, Local Development]

## Context for Developers & AI Agents 🤖
- **Affected Files/Modules:** [e.g., src/auth/login.js]
- **Related Code:** [Link to GitHub line/file if known]
- **Recent Changes:** [Link to recent PRs that might be related]

## Additional Context
Add any other context about the problem here.

## Severity
- [ ] 🔴 Critical - System down / Data loss
- [ ] 🟠 High - Major feature broken
- [ ] 🟡 Medium - Feature partially working
- [ ] 🟢 Low - Minor issue / Cosmetic
```

---

## 16. AI Workflow Best Practices

Since we leverage AI throughout our development lifecycle, here are specific best practices:

### Context Sharing with AI

**At the Start of Each Session:**
1. Share the issue you're working on with its full context
2. Reference relevant architectural decisions and patterns
3. Point AI to CODEOWNERS and related code sections
4. Share any relevant previous conversations or decisions

**During Development:**
1. Ask AI to explain complex code sections before modifying
2. Have AI generate test cases based on acceptance criteria
3. Use AI for code review suggestions before human review
4. Ask AI to check for edge cases you might have missed

### AI Code Review Checklist

Before submitting for human review, use AI to check:
- [ ] Are there any obvious bugs or edge cases missed?
- [ ] Does this code follow project conventions?
- [ ] Are there any security vulnerabilities?
- [ ] Could this code be simplified?
- [ ] Are error messages clear and actionable?
- [ ] Is the code well-commented where needed?

### When NOT to Trust AI

AI assistants are powerful but not infallible. Always verify:
- **Security-critical code** - Have a human security expert review
- **Algorithm correctness** - Test thoroughly, don't assume AI is correct
- **Business logic** - AI doesn't understand your specific business rules
- **Performance implications** - AI may not optimize for your scale
- **Compliance requirements** - AI may not know your regulatory constraints

### Documentation for AI Context

When writing documentation, keep in mind that AI will read it:
- Use clear, structured formats (markdown with headers)
- Include code examples
- Be explicit about patterns and anti-patterns
- Link to related concepts
- Use conventional terminology

---

## Appendix: Rationale Summary

This workflow is designed around these core beliefs:

1. **Small, frequent changes are safer than large, infrequent ones**
   * Short-lived feature branches reduce merge conflicts
   * Frequent releases reduce the blast radius of bugs

2. **Automation catches more issues than manual processes**
   * CI checks are consistent and fast
   * Humans are better at creative problem-solving than rote checking
   * AI assists with pattern recognition and boilerplate

3. **Peer review improves quality and spreads knowledge**
   * Two people understanding code is better than one
   * Reviews catch bugs and teach best practices
   * AI can supplement but not replace human review

4. **Clear process reduces anxiety and increases velocity**
   * Developers know what's expected
   * Less time wasted on "what do I do now?"
   * AI can work effectively with well-defined processes

5. **Main branch protection is non-negotiable**
   * Production stability is paramount
   * It's easier to prevent problems than fix them

6. **Context is king for both humans and AI**
   * Well-documented issues save time
   * Clear architecture documentation enables faster onboarding
   * AI assistants are exponentially more effective with good context

**Adapt this document to your team's needs, but keep these principles intact.**

---

**Document Version:** 2.0.0  
**Last Updated:** 29/09/2025  
**Maintained By:** Clem and ClaudeAI  
**Questions?** Open an issue or ask in #engineering

---

**Changelog:**
- v2.0.0: Added AI workflow integration, comprehensive templates, explicit documentation categories
- v1.0.0: Initial Gitflow documentation