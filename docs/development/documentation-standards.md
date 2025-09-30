# Documentation Standards Guide

**Last Updated:** 2025-09-30  
**Version:** 1.0  

## Overview

This guide outlines our 3-category documentation system that ensures comprehensive coverage while maintaining flexibility for different types of work.

## 3-Category Documentation System

### 👤 User Documentation
**When Required:** User-facing changes, new features, API changes, configuration changes  
**Purpose:** Help end-users effectively use the system

#### Required Components:
- **User Guides/Manuals** (`docs/guides/user/`)
  - Step-by-step instructions for new functionality
  - Getting Started guides for new users
  - Usage examples and common workflows
  
- **FAQ Updates** (`docs/guides/faq.md`)
  - Common scenarios and how to handle them
  - Troubleshooting steps for new features
  - Known limitations and workarounds
  
- **Release Notes** (`CHANGELOG.md`)
  - User-facing changes described in business terms
  - Breaking changes clearly highlighted
  - Migration steps for major version changes

#### Example - Adding New Business Profile:
```markdown
# User Guide: Charity-Nonprofit Business Profile

## Overview
The charity-nonprofit profile provides pre-configured templates for 
charitable organizations including fundraising tools, donor management,
and compliance reporting.

## Quick Start
1. Run: `python -m src.cli.business_commands deploy-business --profile=charity-nonprofit`
2. Configure your organization details in the generated config
3. Your charity infrastructure will be ready in under 10 minutes

## Features Included
- Donor management system
- Fundraising campaign tools
- Financial reporting dashboard
- Compliance monitoring
```

### 👨‍💻 Developer Documentation  
**When Required:** Technical changes, refactoring, architecture changes, development process changes  
**Purpose:** Help developers understand, maintain, and extend the system

#### Required Components:
- **API Reference/OpenAPI Specs** (`docs/api/`)
  - Endpoint documentation with request/response examples
  - Error codes and handling
  - Authentication and rate limiting details

- **Architecture Documentation** (`docs/architecture/`)
  - Architecture Decision Records (ADRs) for design choices
  - System diagrams and component relationships  
  - Data flow and integration patterns

- **Code Documentation**
  - Inline comments for complex business logic
  - Comprehensive docstrings for all functions/classes
  - Type hints for all Python code

- **README Updates** (if setup/installation changed)
  - Installation instructions
  - Development environment setup
  - Dependency management

#### Example - New API Endpoint:
```python
def deploy_business(profile: str, dry_run: bool = False) -> DeploymentResult:
    """Deploy a complete business infrastructure using specified profile.
    
    Args:
        profile: Business profile identifier (startup-basic, charity-nonprofit, etc.)
        dry_run: If True, validate configuration without actual deployment
        
    Returns:
        DeploymentResult containing status, deployed services, and metadata
        
    Raises:
        InvalidProfileError: Profile not found or invalid
        DeploymentError: Deployment failed due to infrastructure issues
        
    Example:
        >>> result = deploy_business('startup-basic', dry_run=True)
        >>> print(f"Would deploy {len(result.services)} services")
    """
```

### ⚙️ Operations Documentation
**When Required:** Deployment changes, configuration changes, infrastructure updates  
**Purpose:** Help operators deploy, configure, and maintain the system

#### Required Components:
- **Installation & Deployment Guide** (`docs/operations/deployment.md`)
  - System requirements and dependencies
  - Step-by-step deployment procedures
  - Environment-specific configuration notes

- **Configuration Guide** (`docs/operations/configuration.md`)
  - All configuration options documented
  - Environment variables with examples
  - Security considerations for production

- **Migration Guide** (for breaking changes)
  - Version upgrade procedures
  - Breaking change impact assessment
  - Rollback procedures if needed

- **Monitoring & Troubleshooting** (`docs/operations/troubleshooting.md`)
  - Common issues and solutions
  - Log analysis and debugging
  - Performance monitoring guidelines

#### Example - Configuration Change:
```yaml
# Configuration Documentation Update
business_profiles:
  startup_basic:
    description: "Essential tools for early-stage startups"
    deployment_time: "8-10 minutes"
    services:
      - accounting_system
      - crm_basic  
      - project_management
    environment_variables:
      STARTUP_SCALE: "small|medium|large" # Default: small
      ENABLE_ANALYTICS: "true|false"      # Default: true
```

### 📋 Process/Research Documentation
**When Required:** Analysis, research, audits, internal process documentation  
**Purpose:** Capture internal work, decisions, and institutional knowledge

#### Flexible Requirements:
- **Analysis/Research Documents** (`docs/analysis/`, `docs/research/`)
  - Executive summary of findings
  - Methodology and scope
  - Recommendations with rationale
  - Implementation roadmap if applicable

- **Audit Documentation** (`docs/audits/`)
  - Audit scope and approach
  - Issues identified with severity levels
  - Remediation recommendations
  - Follow-up tracking

- **Process Documentation** (`docs/development/`)
  - New workflows with examples
  - Integration with existing processes
  - Success criteria and measurement

#### Example - Gap Analysis:
```markdown
# GitFlow Development Workflow Gap Analysis

## Executive Summary
Analysis of GitFlow v3.1 research against current implementation reveals 
12 gaps requiring implementation, with 4 critical priorities.

## Key Findings
- Missing CI/CD status checks in rulesets
- No structured documentation standards
- Missing hotfix workflow for emergencies

## Recommendations
1. Implement critical infrastructure gaps (Week 1)
2. Process enhancements (Weeks 2-3)  
3. Automation optimization (Month 2)
```

## Smart Categorization Logic

### How to Determine Documentation Requirements:

**🚀 User-Facing Changes:**
- New commands or CLI options
- API endpoint changes
- Configuration file changes
- UI/UX modifications
- Feature additions/removals

**🛠️ Technical Changes:**
- Code refactoring or restructuring
- Architecture pattern changes
- Development process updates
- Performance optimizations
- Security implementations

**📋 Process/Research:**
- Gap analyses and research
- Audit findings and reports
- Process improvement documentation
- Internal tooling and workflows

**🐛 Bug Fixes:**
- Minimal documentation requirements
- Focus on changelog if user-visible
- No full 3-category requirements

## Integration with PR Process

### PR Template Workflow:
1. **Select Change Category** - Choose from 4 options in PR template
2. **Follow Applicable Standards** - Complete relevant documentation sections
3. **Skip Non-Applicable Sections** - Clear guidance on what to skip
4. **Validate Completeness** - Use checklist to ensure coverage

### Review Process:
- **Reviewers verify** documentation matches change category
- **Documentation quality** becomes part of approval criteria  
- **Flexible enforcement** for internal/research work

## Benefits of This System

### For User-Facing Changes:
- **Consistent user experience** through comprehensive guides
- **Smooth adoption** via clear documentation
- **Reduced support burden** through good FAQs

### For Technical Changes:  
- **Developer onboarding** accelerated with clear architecture docs
- **Maintainability** improved through code documentation
- **Knowledge preservation** via ADRs and design decisions

### For Operations:
- **Reliable deployments** through clear operational guides
- **Reduced downtime** via troubleshooting documentation
- **Consistent configuration** across environments

### For Research/Process:
- **Institutional knowledge** captured effectively
- **Decision tracking** for future reference
- **Flexible standards** that don't impede internal work

## Exemptions and Flexibility

### Automatic Exemptions:
- **Research documents** in `docs/research/`
- **Analysis documents** in `docs/analysis/`
- **Audit reports** in `docs/audits/`
- **Internal process docs** in `docs/development/`

### Conditional Requirements:
- **Bug fixes** → Only changelog if user-visible
- **Security patches** → Focus on operations documentation
- **Performance improvements** → Developer documentation for implementation details

## Success Metrics

### Documentation Quality:
- All user-facing changes have complete user documentation
- All technical changes include developer documentation  
- All deployment changes include operations documentation
- Research/analysis follows structured format

### Developer Experience:
- Clear guidance on what documentation is required
- Flexible requirements don't impede internal work
- PR template provides helpful structure
- Review process focuses on documentation quality

This system ensures comprehensive documentation for user-facing work while maintaining the flexibility needed for our research, analysis, and audit processes.
