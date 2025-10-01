# Issue Type Framework for Meta-Repo Structure

**Document Type:** Development Reference  
**Last Updated:** 2025-09-30  
**Context:** Meta-repo structure with cross-cutting concerns and multi-domain architecture

## Overview

This document defines the issue type framework for meta-repo-seed, designed to handle work across multiple repositories and capture cross-cutting concerns in a Business-in-a-Box ecosystem spanning Strategy, Enterprise Architecture, Product Management, Development, and Operations domains.

## Current Challenge

Traditional issue types designed for single repositories don't adequately capture:
- **Cross-repo concerns** affecting multiple components
- **Process and workflow issues** that aren't code changes
- **Meta-structure changes** affecting the repository organization itself
- **Domain-spanning work** that touches business strategy, technical architecture, and implementation

## Recommended Issue Type Framework

### Core Work Types (What kind of work?)

| Type | Description | Usage Examples |
|------|-------------|-----------------|
| `feat` | New functionality | Adding new template generation, implementing integrated workflow |
| `fix` | Bug fixes | Correcting broken links, fixing template generation errors |
| `docs` | Documentation only | README updates, adding architectural decision records |
| `refactor` | Code restructuring without behavior change | Reorganizing template structure, improving code organization |
| `test` | Test additions/modifications | Adding unit tests, integration test improvements |
| `perf` | Performance improvements | Optimizing template generation, improving CLI response time |

### Cross-Cutting Scope Types (Where does this apply?)

| Type | Description | Usage Examples |
|------|-------------|-----------------|
| `process` | Workflow, methodology, how we work | GitFlow improvements, TDD process updates, PR template fixes |
| `infra` | Infrastructure, CI/CD, tooling, automation | GitHub Actions, deployment pipelines, automation scripts |
| `dx` | Developer experience improvements | CLI usability, development environment setup |
| `security` | Security-related changes | Dependency updates, vulnerability fixes, access control |

### Meta-Repo Specific Types

| Type | Description | Usage Examples |
|------|-------------|-----------------|
| `meta` | Changes affecting multiple repos or meta structure | Cross-repo testing, meta-repo organization changes |
| `config` | Configuration changes across repos | Linting rules, TypeScript config, formatting standards |
| `deps` | Dependency updates across repos | Package updates, version synchronization |

### Maintenance Types

| Type | Description | Usage Examples |
|------|-------------|-----------------|
| `chore` | Miscellaneous maintenance | File cleanup, minor updates, routine tasks |

## Implementation Options

### Option 1: Extended Conventional Commits (Recommended)
Use existing conventional commit types plus new meta-repo specific types:

```
feat(strategy): add business plan template generation
fix(cicd): correct deployment pipeline for multi-repo structure  
process(docs): fix documentation generation workflow
meta(testing): add cross-repo integration testing
config(formatting): update prettier configuration across all repos
```

### Option 2: Hierarchical GitHub Labels
Combine type and scope labels on GitHub issues:

**Type Labels:**
- `type: feat`
- `type: fix` 
- `type: process`
- `type: meta`

**Scope Labels:**
- `scope: strategy`
- `scope: architecture` 
- `scope: product`
- `scope: development`
- `scope: operations`

**Domain Labels:**
- `domain: business`
- `domain: technical`
- `domain: integration`

### Option 3: Minimal Addition (Quick Win)
Add `process` type to existing conventional commit types to address immediate workflow/methodology issues.

## Usage Guidelines

### When to Use `process`
- Workflow improvements (GitFlow, TDD process changes)
- Methodology updates (documentation standards, review processes)
- Process automation (workflow triggers, automation improvements)
- Template or guideline updates for how work gets done

### When to Use `meta`
- Changes affecting multiple repositories simultaneously
- Meta-repository structure modifications
- Cross-repo dependency or integration work
- Architecture changes spanning multiple domains

### When to Use Domain Scopes
Use five-domain scopes when work is specific to business domains:
- `(strategy)` - Business planning, market analysis, financial models
- `(architecture)` - System design, architectural decisions, technical principles  
- `(product)` - Product management, roadmaps, requirements
- `(development)` - Code implementation, testing, development tooling
- `(operations)` - Deployment, monitoring, infrastructure management

## Integration with Existing Systems

### Conventional Commits Compatibility
All issue types align with conventional commit standards and support automated changelog generation and semantic versioning.

### GitHub Integration
Issue types can be enforced through:
- GitHub issue templates requiring type selection
- PR template validation checking conventional commit compliance
- Automated labeling based on commit message parsing

### Project Management
Issue types support filtering and reporting for:
- Sprint planning by work type
- Cross-repo dependency tracking
- Domain-specific work allocation
- Process improvement initiatives

## Migration Strategy

### Phase 1: Immediate Addition (Current)
Add `process` type to address workflow and methodology issues affecting current documentation and development processes.

### Phase 2: Full Framework Implementation (30 days)
- Update GitHub issue templates to include new types
- Add PR template validation for extended conventional commits
- Update CONTRIBUTING.md with new framework
- Train team on new issue type usage

### Phase 3: Tooling Integration (60 days)
- Implement automated labeling based on commit message parsing
- Create dashboard views filtered by issue type
- Add cross-repo dependency tracking

## Examples in Context

### Business-in-a-Box Development
```
feat(strategy): implement business plan template with financial projections
feat(architecture): add architectural decision record templates  
feat(product): create product roadmap integration with GitHub projects
meta(workflow): establish integrated strategy-to-code traceability
process(docs): implement three-category documentation standards
config(formatting): standardize markdown formatting across all domains
```

### Meta-Repo Management
```
meta(structure): reorganize audit documentation for better discoverability
deps(security): update dependencies across all sub-repositories  
infra(cicd): implement cross-repo testing pipeline
dx(cli): add business-oriented CLI commands for company setup
```

## Future Considerations

As the meta-repo structure evolves to support the full Business-in-a-Box vision, issue types may need expansion to handle:
- **Partnership integration** work with fractional CTOs and accelerators  
- **Template ecosystem** contributions from community
- **Compliance and certification** work (TOGAF alignment, security certifications)
- **Market validation** and user research activities

---

## References

1. Conventional Commits Specification: https://www.conventionalcommits.org/
2. Meta-Repo-Seed Contributing Guidelines: `CONTRIBUTING.md`
3. GitFlow Workflow Documentation: `docs/development/gitflow-workflow.md`
4. External Audit Analysis: `docs/analysis/20250930-gemini-external-audit-analysis.md`
