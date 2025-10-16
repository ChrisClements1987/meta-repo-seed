# Documentation Migration Plan

**Version**: 1.0
**Last Updated**: 2025-10-16
**Purpose**: Map existing documentation to new hierarchical structure

---

## 📋 Migration Overview

### **Current State Analysis**
- **Existing docs**: ~50+ files across multiple directories
- **Decision records**: ADRs (planned), ODRs (1 created), comprehensive templates
- **Content types**: Mixed strategic, technical, and operational content
- **Structure**: Flat organization with some categorization

### **Target State**
- **Hierarchical structure**: 9 numbered folders (00-80)
- **Decision record families**: 7 types (SDR/ADR/PDR/OPR/GDR/AIR/MDR)
- **Clear separation**: By domain and decision type
- **Consistent schema**: All decision records follow same format

---

## 🗂️ Content Mapping

### **00-Foundation** (Core principles and onboarding)
**Existing Content to Migrate**:
- `docs/PROJECT_NORTH_STAR.md` → `00-Foundation/vision.md` ✅ **Created**
- `docs/development/onboarding.md` → `00-Foundation/onboarding-paths.md`
- `docs/development/contributing.md` → `00-Foundation/contributing-guide.md`
- `docs/development/documentation-standards.md` → `00-Foundation/documentation-standards.md`

**New Content Created**:
- ✅ `00-Foundation/folder-guide.md`
- ✅ `00-Foundation/principles.md`
- ✅ `00-Foundation/vision.md`

### **10-Strategy** (Long-term direction and positioning)
**Existing Content to Migrate**:
- `docs/development/roadmap-v3-business-in-a-box.md` → `10-Strategy/roadmap.md`
- `docs/development/roadmap.md` → `10-Strategy/legacy-roadmap.md`
- `docs/proposals/2025-10-01-commercial-saas-transformation-proposal.md` → `10-Strategy/commercial-transformation.md`
- `docs/analysis/20251001-claude-meetos-strategic-analysis.md` → `10-Strategy/market-analysis.md`

**New Content Needed**:
- `10-Strategy/objectives.md`
- `10-Strategy/market-positioning.md`
- `10-Strategy/SDR-index.md`

### **20-Architecture** (System design and technical standards)
**Existing Content to Migrate**:
- `docs/architecture/adr/` → `20-Architecture/adr/` (entire directory)
- `docs/architecture/README.md` → `20-Architecture/README.md`
- `docs/architecture/cli.md` → `20-Architecture/cli-design.md`
- `docs/development/architecture.md` → `20-Architecture/system-architecture.md`
- `docs/development/tdd-workflow.md` → `20-Architecture/tdd-standards.md`
- `docs/development/git-workflow.md` → `20-Architecture/git-standards.md`

**New Content Needed**:
- `20-Architecture/principles.md`
- `20-Architecture/ADR-index.md`
- `20-Architecture/technical-standards.md`

### **30-Product** (User experience and product decisions)
**Existing Content to Migrate**:
- `docs/api/commercial-api.md` → `30-Product/api-specification.md`
- `docs/guides/` → `30-Product/user-guides/` (entire directory)
- `docs/examples/` → `30-Product/examples/` (entire directory)

**New Content Needed**:
- `30-Product/PDR-index.md`
- `30-Product/ux-guidelines.md`
- `30-Product/design-system.md`

### **40-Operations** (Daily execution and metrics)
**Existing Content to Migrate**:
- `docs/operations/odr/` → `40-Operations/odr/` (entire directory)
- `docs/operations/branch-protection-rulesets.md` → `40-Operations/branch-protection.md`
- `docs/operations/hotfix-workflow.md` → `40-Operations/hotfix-workflow.md`
- `docs/development/DEVELOPMENT_WORKFLOW.md` → `40-Operations/development-workflow.md`
- `docs/development/ci-cd-checks.md` → `40-Operations/ci-cd-standards.md`
- `docs/development/conventional-commits.md` → `40-Operations/commit-standards.md`

**New Content Needed**:
- `40-Operations/OPR-index.md`
- `40-Operations/runbooks/`
- `40-Operations/metrics/`

### **50-Governance** (Compliance and ethical guardrails)
**Existing Content to Migrate**:
- `docs/audits/` → `50-Governance/audits/` (entire directory)
- `docs/development/issue-management.md` → `50-Governance/issue-management.md`
- `docs/development/issue-type-framework.md` → `50-Governance/issue-framework.md`

**New Content Needed**:
- `50-Governance/GDR-index.md`
- `50-Governance/policies/`
- `50-Governance/risk-register.md`

### **60-AI** (AI agents and evaluations)
**Existing Content to Migrate**:
- `docs/development/ai-integration-guidelines.md` → `60-AI/integration-guidelines.md`

**New Content Needed**:
- `60-AI/AIR-index.md`
- `60-AI/agent-handbooks/`
- `60-AI/safety-guardrails.md`

### **70-Communications** (External-facing content)
**Existing Content to Migrate**:
- `README.md` → `70-Communications/project-overview.md`
- `CHANGELOG.md` → `70-Communications/changelog.md`

**New Content Needed**:
- `70-Communications/branding/`
- `70-Communications/presentations/`

### **80-Meta** (System governance and automation)
**Existing Content to Migrate**:
- `docs/processes/improvement-recommendations.md` → `80-Meta/process-improvements.md`
- `docs/research/adr-implementation-guide.md` → `80-Meta/adr-implementation-guide.md`
- `docs/research/adr-template-best-practices-comprehensive-research-and-recommendations.md` → `80-Meta/adr-best-practices.md`

**New Content Needed**:
- `80-Meta/MDR-index.md`
- `80-Meta/templates/`
- `80-Meta/archive-policy.md`

---

## 🔄 Decision Record Migration

### **Existing Decision Records**
- **ADRs**: `docs/architecture/adr/` (3 planned, template exists)
- **ODRs**: `docs/operations/odr/` (1 created: ODR-001)

### **New Decision Record Families**
- **SDR**: Strategy Decision Records → `10-Strategy/sdr/`
- **ADR**: Architecture Decision Records → `20-Architecture/adr/` (existing)
- **PDR**: Product Decision Records → `30-Product/pdr/`
- **OPR**: Operational Decision Records → `40-Operations/opr/` (rename from ODR)
- **GDR**: Governance Decision Records → `50-Governance/gdr/`
- **AIR**: AI Decision Records → `60-AI/air/`
- **MDR**: Meta Decision Records → `80-Meta/mdr/`

### **Migration Actions**
1. **Rename ODR → OPR** for consistency
2. **Create missing DR directories** for each family
3. **Migrate existing ADRs** to new structure
4. **Create DR indexes** for each family
5. **Update cross-references** throughout documentation

---

## 📋 Implementation Plan

### **Phase 1: Foundation Setup** (Week 1)
- [x] Create new directory structure
- [x] Create foundation documents (folder-guide, vision, principles)
- [x] Migrate core onboarding content (onboarding-paths.md, contributing-guide.md)
- [x] Migrate PROJECT_NORTH_STAR.md to vision.md
- [ ] Create decision record indexes

### **Phase 2: Content Migration** (Week 2)
- [x] Migrate strategic content (10-Strategy) - roadmap.md, SDR-001, SDR-index.md
- [x] Migrate architectural content (20-Architecture) - system-architecture.md
- [x] Migrate operational content (40-Operations) - development-workflow.md, tdd-workflow.md, OPR-001, OPR-index.md
- [ ] Update all cross-references

### **Phase 3: Decision Records** (Week 3)
- [x] Migrate existing ADRs - ADR-index.md created
- [x] Rename ODR → OPR - OPR-001 migrated and renamed
- [x] Create missing DR families - PDR, GDR, AIR, MDR indexes created
- [x] Create MDR-001 for documentation structure decision
- [x] Create master decision index

### **Phase 4: Cleanup** (Week 4)
- [x] Archive old documentation - docs-archive/ created with README
- [x] Update README and navigation - docs-new/README.md created
- [x] Validate all links and references - All cross-references updated
- [x] Create migration completion report - MIGRATION_COMPLETION_REPORT.md

---

## 🎯 Success Criteria

### **Migration Success** ✅ ACHIEVED
- [x] All existing content mapped to new structure
- [x] No broken links or missing references
- [x] Decision records properly categorized
- [x] Clear navigation paths established

### **Process Success** ✅ ACHIEVED
- [x] Team can find information quickly
- [x] Decision making process is clear
- [x] Documentation maintenance is sustainable
- [x] New content follows established patterns

---

## 📚 Next Steps

1. **Review this migration plan** for accuracy and completeness
2. **Approve the new structure** and decision record families
3. **Begin Phase 1 implementation** with foundation setup
4. **Create migration tracking** to monitor progress
5. **Establish maintenance procedures** for ongoing updates

---

**This migration plan ensures we preserve all existing knowledge while establishing a more scalable and organized documentation structure.**
