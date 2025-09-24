# Meta-Repo-Seed Template Structure

This document describes the template structure used by the seeding script.

## Template Directory Structure

```
meta-repo-seed/templates/
├── gitignore.template                                    # .gitignore template
├── github/
│   └── workflows/
│       ├── ci.yml.template                              # CI/CD workflow
│       └── readme-docs.yml.template                    # README generation workflow
├── governance/
│   ├── policies/
│   │   ├── contributing.md.template                     # Contributing guidelines
│   │   ├── code-of-conduct.md.template                 # Code of conduct
│   │   ├── privacy-policy.md.template                  # [TODO] Privacy policy
│   │   ├── security-policy.md.template                 # [TODO] Security policy
│   │   ├── license.md.template                         # [TODO] License
│   │   └── terms-of-service.md.template                # [TODO] Terms of service
│   ├── processes/
│   │   ├── onboarding.md.template                       # [TODO] Onboarding process
│   │   ├── offboarding.md.template                     # [TODO] Offboarding process
│   │   ├── code-review.md.template                     # [TODO] Code review process
│   │   ├── issue-management.md.template                # [TODO] Issue management
│   │   ├── release-management.md.template              # [TODO] Release management
│   │   └── security-management.md.template             # [TODO] Security management
│   ├── standards/
│   │   ├── coding-standards.md.template                 # [TODO] Coding standards
│   │   ├── documentation-standards.md.template         # [TODO] Documentation standards
│   │   ├── testing-standards.md.template               # [TODO] Testing standards
│   │   ├── security-standards.md.template              # [TODO] Security standards
│   │   └── access-control-standards.md.template        # [TODO] Access control standards
│   └── shared-resources/
│       └── templates/
│           ├── pull-request-template.md.template        # PR template
│           ├── issue-template.md.template               # Issue template
│           └── architecture-decision-record-template.md.template # ADR template
├── cloud-storage/
│   ├── strategy/
│   │   ├── vision.md.template                          # Vision document
│   │   ├── mission.md.template                         # Mission statement
│   │   └── strategic-roadmap.md.template               # [TODO] Strategic roadmap
│   └── architecture/
│       └── principles/
│           └── principles.md.template                   # [TODO] Architecture principles
├── documentation/
│   ├── guides/
│   │   └── getting-started.md.template                 # Getting started guide
│   └── shared-resources/
│       ├── templates.md.template                        # [TODO] Templates documentation
│       ├── glossary.md.template                        # [TODO] Glossary
│       └── faq.md.template                             # [TODO] FAQ
├── automation/
│   └── scripts/
│       ├── initialise_repo.py.template                  # [TODO] Initialization script
│       ├── enforce_structure.py.template               # [TODO] Structure enforcement
│       └── generate_readmes.py.template                # [TODO] README generation
└── structure/
    ├── structure.json.template                          # [TODO] Structure definition
    └── meta-repo-schema.json.template                  # [TODO] Schema definition
```

## Template Variables

The following variables are automatically replaced in templates:

- `{{PROJECT_NAME}}` - The project name (auto-detected or specified)
- `{{GITHUB_USERNAME}}` - The GitHub username (from git config or specified)
- `{{CURRENT_DATE}}` - Current date (2025-09-24)
- `{{DECISION_NUMBER}}` - Decision number for ADRs (001)
- `{{DECISION_TITLE}}` - Decision title for ADRs
- `{{STATUS}}` - Status for ADRs (Proposed)
- `{{ALTERNATIVE_NAME}}` - Alternative name for ADRs

## Completed Templates ✅

- `gitignore.template` - Comprehensive .gitignore
- `github/workflows/ci.yml.template` - CI workflow
- `github/workflows/readme-docs.yml.template` - README generation
- `governance/policies/contributing.md.template` - Contributing guidelines
- `governance/policies/code-of-conduct.md.template` - Code of conduct
- `governance/shared-resources/templates/pull-request-template.md.template` - PR template
- `governance/shared-resources/templates/issue-template.md.template` - Issue template
- `governance/shared-resources/templates/architecture-decision-record-template.md.template` - ADR template
- `cloud-storage/strategy/vision.md.template` - Vision document
- `cloud-storage/strategy/mission.md.template` - Mission statement
- `documentation/guides/getting-started.md.template` - Getting started guide

## Templates Still Needed [TODO]

See the directory structure above for templates marked with [TODO].

## Usage

The seeding script automatically uses these templates to create structured, professional content for new projects. All templates support variable replacement for customization.

To add a new template:
1. Create the template file in the appropriate directory
2. Use `{{VARIABLE_NAME}}` for replaceable content
3. Update the seeding script to reference the new template
4. Add the variable to the `replacements` dictionary if needed

---

*Last Updated: September 24, 2025*