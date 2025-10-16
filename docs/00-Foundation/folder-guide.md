# Documentation Folder Guide

**Version**: 1.0
**Last Updated**: 2025-10-16
**Purpose**: Guide to the hierarchical documentation structure

---

## 📁 Folder Overview

| Folder | Description | Key Contents |
|--------|-------------|--------------|
| **00-Foundation** | Core principles, glossary, and onboarding guides | vision.md, principles.md, folder-guide.md, onboarding-paths.md |
| **10-Strategy** | Long-term direction and positioning | SDRs, objectives, market analysis, roadmaps |
| **20-Architecture** | System design, platforms, and technical standards | ADRs, diagrams, standards, developer-docs, how-to |
| **30-Product** | User experience and product decisions | PDRs, UX guidelines, design-system |
| **40-Operations** | Daily execution, runbooks, and metrics | OPRs, runbooks, troubleshooting, metrics |
| **50-Governance** | Compliance, risk, and ethical guardrails | GDRs, policies, risk-register, standards |
| **60-AI** | AI agents, prompt patterns, and evaluations | AIRs, agent-handbooks, safety-guardrails |
| **70-Communications** | External-facing content and branding | blog-posts, external-docs, presentations, branding |
| **80-Meta** | System governance and automation | MDRs, templates, indexes, archive-policy.md |

---

## 🔄 Decision Record Families

| Code | Domain | Description |
|------|--------|-------------|
| **SDR** | Strategy Decision Record | Guides market focus, goals, and strategic positioning |
| **ADR** | Architecture Decision Record | Defines technical and system-level choices |
| **PDR** | Product Decision Record | Captures product features, UX, and user needs |
| **OPR** | Operational Decision Record | Documents process and workflow standards |
| **GDR** | Governance Decision Record | Establishes compliance and ethical principles |
| **AIR** | AI Decision Record | Governs AI agent behaviour, autonomy, and safeguards |
| **MDR** | Meta Decision Record | Defines rules for how decisions themselves are made |

### Decision Record Schema

All decision records share a consistent schema:

1. **Context** → What is the issue motivating this decision?
2. **Decision** → What change are we proposing?
3. **Consequences** → What becomes easier/difficult?
4. **Alternatives** → What other options were considered?
5. **Implementation Notes** → How will this be implemented?
6. **Review Date** → When should this be reviewed?

---

## 📋 Navigation Patterns

### **By Role**
- **New Team Members**: Start with 00-Foundation
- **Product Managers**: Focus on 10-Strategy, 30-Product
- **Developers**: Focus on 20-Architecture, 40-Operations
- **AI Agents**: Focus on 60-AI, 80-Meta
- **Stakeholders**: Focus on 70-Communications

### **By Task**
- **Strategic Planning**: 10-Strategy
- **Technical Decisions**: 20-Architecture
- **Product Features**: 30-Product
- **Daily Operations**: 40-Operations
- **Compliance**: 50-Governance
- **AI Integration**: 60-AI
- **External Communication**: 70-Communications
- **Process Automation**: 80-Meta

### **By Decision Type**
- **Strategic**: SDR-XXX files
- **Architectural**: ADR-XXX files
- **Product**: PDR-XXX files
- **Operational**: OPR-XXX files
- **Governance**: GDR-XXX files
- **AI**: AIR-XXX files
- **Meta**: MDR-XXX files

---

## 🔧 Usage Guidelines

### **Creating New Documents**
1. **Identify the appropriate folder** based on content type
2. **Use consistent naming** conventions
3. **Include metadata** (version, date, purpose)
4. **Cross-reference** related documents
5. **Update indexes** when adding new content

### **Decision Record Creation**
1. **Choose the appropriate DR type** (SDR/ADR/PDR/OPR/GDR/AIR/MDR)
2. **Use the standard schema** (Context → Decision → Consequences → Alternatives → Implementation → Review)
3. **Number sequentially** within each type
4. **Include status** (Proposed/Accepted/Rejected/Deprecated/Superseded)
5. **Set review dates** for regular evaluation

### **Maintenance**
- **Regular reviews** of decision records
- **Archive outdated** content to 80-Meta
- **Update cross-references** when documents change
- **Maintain indexes** for easy navigation

---

## 📚 Quick Reference

### **Foundation Documents**
- [Vision](vision.md) - Project vision and mission
- [Principles](principles.md) - Core principles and values
- [Onboarding Paths](onboarding-paths.md) - Role-specific onboarding

### **Decision Record Indexes**
- [Strategy Decisions](../10-Strategy/SDR-index.md)
- [Architecture Decisions](../20-Architecture/ADR-index.md)
- [Product Decisions](../30-Product/PDR-index.md)
- [Operational Decisions](../40-Operations/OPR-index.md)
- [Governance Decisions](../50-Governance/GDR-index.md)
- [AI Decisions](../60-AI/AIR-index.md)
- [Meta Decisions](../80-Meta/MDR-index.md)

### **Key Processes**
- [Documentation Standards](../80-Meta/documentation-standards.md)
- [Decision Making Process](../80-Meta/decision-making-process.md)
- [Review and Archive Policy](../80-Meta/archive-policy.md)

---

## 🎯 Success Metrics

- **Navigation Efficiency**: Time to find relevant information
- **Decision Traceability**: Clear audit trail of decisions
- **Onboarding Speed**: Time for new team members to become productive
- **Maintenance Overhead**: Effort required to keep documentation current

---

**This folder guide is a living document that should be updated as the documentation structure evolves.**
