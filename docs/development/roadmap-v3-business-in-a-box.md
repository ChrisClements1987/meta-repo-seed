# Business-in-a-Box Roadmap (v3.0+)

**Vision**: Deploy complete organizational infrastructures enabling startups, charities, non-profits, and SMBs to launch professional operations in under 10 minutes.

**Architecture Evolution**: Repository scaffolding tool → **Organizational Control Plane**

---

## 🎯 Phase 0: Business-in-a-Box Foundation (Q1 2026)
*Goal: Prove 10-minute business deployment concept*

### **Sprint 1-2: Core Business Deployment (2-3 weeks)**
- [ ] **Organization Blueprint System** 
  - YAML schema for org/portfolio/product/environment/provider definitions
  - Multi-repo orchestration engine (replaces single-repo seeding)
  - Dependency-aware deployment (teams→repos→policies→pipelines)

- [ ] **Platform Repo with Reusable Workflows**
  - Library of GitHub Actions workflows (build/test/scan/deploy) 
  - Pre-approved patterns: Node/Python/Go API, SPA, Worker, Mobile
  - Versioned releases for consumer stability

- [ ] **GitHub App + Minimal Control Plane**
  - Replace PAT with GitHub App for org-wide operations
  - Webhook receiver for compliance enforcement
  - Basic API for CLI commands and state tracking

### **Sprint 3: Fast-Path Product Launch (1-2 weeks)**
- [ ] **10-Minute Product Launch Pipeline**
  - PaaS provider integration (Vercel/Netlify/Cloudflare/Fly.io)
  - Template → Secrets → Deploy → URL automation
  - CLI: `launch-product --stack=nextjs --name=my-app`

- [ ] **Business Deployment Command**
  - CLI: `deploy-business --profile=startup-basic`
  - Seeds: org-meta, platform, templates, teams, rulesets, handbook
  - Automated team permissions and security settings

**Success Metrics**: 
- < 10 minutes: Command to operational business infrastructure
- < 10 minutes: Idea to deployed app with CI/CD
- 95%+ automation (minimal manual configuration)

---

## 🏗️ Phase 1: Organizational Operations (Q2 2026)
*Goal: Self-governing, onboarding, and portfolio management*

### **Sprint 4-5: Post-Seeding Onboarding (2-3 weeks)**
- [ ] **Workflow Engine with Durable State**
  - Resumable workflows stored in Control Plane
  - GitHub Issues/Projects integration for task tracking
  - CLI: `start-onboarding`, `resume-onboarding`

- [ ] **Guided Business Setup Workflows**
  - Domain connection, billing setup, team roles
  - Secret imports, compliance confirmation
  - Company information and localization

- [ ] **Provider Abstraction Layer**
  - Plugin registry for VCS/CI/CD/Cloud/Secrets/PaaS
  - Starting providers: GitHub, Actions, Vercel, GitHub Secrets
  - Configuration-driven provider selection

### **Sprint 6-7: Portfolio Lifecycle Management (2-3 weeks)**
- [ ] **Portfolio Service and Domain Model**
  - Organization, Team, Portfolio, Product, Repository, Environment
  - Lifecycle states: idea→poc→mvp→active→maintained→sunset
  - Environment promotion gates and automation

- [ ] **Multi-Environment Management**
  - Dev/staging/production environment orchestration
  - Promotion pipelines with quality gates
  - Dashboard showing portfolio status across environments

- [ ] **Policy-as-Code Engine**
  - OPA/Conftest policies for compliance checking
  - GitHub Checks API integration
  - Auto-remediation PRs for safe fixes

**Success Metrics**:
- < 30 minutes: Complete onboarding workflow
- 90%+ policy compliance automatically maintained
- Portfolio visibility across all environments and lifecycle stages

---

## 🔄 Phase 2: Migration and Governance (Q3 2026)
*Goal: Integrate existing assets and self-healing systems*

### **Sprint 8-9: Migration and Grandfathering (3-4 weeks)**
- [ ] **Asset Discovery and Assessment**
  - Scan existing organization for repos, settings, compliance
  - Score against policies, generate remediation plans
  - CLI: `scan-compliance`, `migrate-import`

- [ ] **Automated Migration System**
  - Non-breaking adapter PRs to introduce standards
  - Grandfathering model for exceptions with expiry
  - Dry-run and rollback capabilities

- [ ] **Compliance Enforcement Automation**
  - Webhook-triggered policy checks
  - Self-healing governance (auto-fix drift)
  - Exception workflow for unavoidable non-compliance

### **Sprint 10: Advanced Pipeline Generation (2 weeks)**
- [ ] **Enterprise CI/CD Templates**
  - Infrastructure-as-Code modules (Terraform/Pulumi)
  - AWS/GCP/Azure minimal provisioning patterns
  - Security scanning, SBOM, container analysis

- [ ] **Advanced Promotion Engine**
  - Change freeze windows, approval workflows
  - Preview environments for PRs
  - Deployment rollback and monitoring

**Success Metrics**:
- 95%+ existing assets successfully migrated or grandfathered
- Self-healing compliance (automatic drift correction)
- < 15 minutes: Enterprise product launch (with IaC)

---

## 🚀 Phase 3: Business Intelligence and Scale (Q4 2026)
*Goal: Analytics, localization, and enterprise features*

### **Sprint 11-12: Business Intelligence (3-4 weeks)**
- [ ] **Portfolio Analytics Dashboard**
  - Cross-project metrics, deployment frequency
  - Change failure rate, lead time tracking
  - Cost visibility and resource optimization

- [ ] **Audit and Compliance Reporting**
  - Immutable audit logs for all control plane actions
  - Compliance reports for security teams
  - Policy violation tracking and trends

### **Sprint 13: Localization and Business Models (2-3 weeks)**
- [ ] **Localization Framework**
  - Regional policy packs and documentation variants
  - Business model presets: startup, charity, SMB, consulting
  - Industry-specific templates and compliance

- [ ] **Advanced Integrations**
  - SSO providers (Okta, Auth0, Clerk)
  - Observability (Grafana, New Relic, Datadog)
  - Communication (Slack, Teams, Discord)

**Success Metrics**:
- Multi-region deployment support
- Industry-specific business model templates
- Enterprise-grade observability and compliance

---

## 📊 Success Metrics Summary

### **Quantitative Targets**
- **Initial Deployment**: < 10 minutes command to operational business
- **Product Launch**: < 10 minutes idea to deployed app with CI/CD  
- **Onboarding**: < 30 minutes guided setup completion
- **Migration**: 95%+ existing assets integrated
- **Automation**: 95%+ quality gates and compliance automated
- **Professional Completeness**: 100% enterprise-ready governance

### **Qualitative Outcomes**
- **Business Focus**: Companies spend time on core business vs infrastructure
- **Professional Credibility**: External stakeholders see mature organization
- **Operational Readiness**: Immediate client/product/partnership capability
- **Self-Governing**: Compliance and quality maintained automatically
- **Scalable Growth**: Seamless expansion without architecture rewrites

---

## 🔄 Migration from v2.x Roadmap

### **Items to Close** (No longer aligned with Business-in-a-Box)
- #8 Multi-Language Support (generic scaffolding)
- #9 Cloud Integration (too generic)
- #10 Project Scaffolding Intelligence (individual projects vs business systems)
- #11 Team Collaboration Features (generic vs business governance)
- #12 VS Code Extension (tooling vs business deployment)
- #13 Web Interface (nice-to-have vs core business value)
- #14 CLI Enhancements (generic improvements)

### **Items to Reframe** (Align with Business-in-a-Box)
- #4 Update Command → **Business Infrastructure Updates**
- #6 Interactive Setup → **Business Deployment Wizard**  
- #17 Organizational Structure → **Organization Blueprint System** ✅ (Critical)
- #24 Template Library → **Business Model Template Library**

### **Items to Accelerate** (Support core capabilities)
- #22 Automation Scripts → **Reusable Workflow Library** (Phase 0)
- #34 Generate READMEs → **Professional Documentation Automation**
- #47 Security Guide → **Enterprise Security Standards**

---

## 🎯 Immediate Actions (Next 2 Weeks)

### **Architecture Definition**
1. Define organization blueprint YAML schema
2. Design Control Plane API specification
3. Create provider abstraction interfaces
4. Document workflow engine state machine

### **Foundation Implementation**
1. Build platform repo with reusable workflows
2. Create first business deployment profiles
3. Implement GitHub App with webhook receiver
4. Build CLI commands: `deploy-business`, `launch-product`

### **Validation**
1. End-to-end test: 10-minute business deployment
2. End-to-end test: 10-minute product launch
3. Document onboarding workflow requirements
4. Validate with target market (startup/charity/SMB)

---

*This roadmap transforms meta-repo-seed from a repository scaffolding tool into a complete Business-in-a-Box deployment platform, directly serving startups, charities, non-profits, and SMBs with professional organizational infrastructure.*
