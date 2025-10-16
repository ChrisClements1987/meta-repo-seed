# MDR-001: Documentation Structure and Decision Framework

**Date**: 2025-10-16
**Status**: Accepted
**Review Date**: 2026-01-16

---

## Context

The existing documentation structure was flat and disorganized, making it difficult to find information and maintain consistency. We needed a comprehensive framework that would:

- **Organize content by domain** rather than by file type
- **Establish clear decision-making processes** with consistent schemas
- **Support scalable growth** as the platform evolves
- **Enable efficient navigation** for different user types
- **Maintain consistency** across all documentation

**Current State**:
- Flat documentation structure with mixed content types
- No consistent decision-making framework
- Difficult to find relevant information
- No clear separation between different domains
- Inconsistent documentation formats

**Requirements**:
- Hierarchical organization by domain
- Consistent decision record schemas
- Clear navigation paths
- Scalable structure for growth
- Role-based access to information

---

## Decision

**Implement a hierarchical documentation structure with numbered folders (00-80) and decision record families (SDR, ADR, PDR, OPR, GDR, AIR, MDR) sharing a consistent schema.**

### **Documentation Structure**

| Folder | Description | Key Contents | Decision Records |
|--------|-------------|--------------|------------------|
| **00-Foundation** | Core principles and onboarding | Vision, principles, onboarding paths | - |
| **10-Strategy** | Strategic direction | Objectives, roadmaps, market analysis | **SDR** |
| **20-Architecture** | Technical design | System design, standards, technical docs | **ADR** |
| **30-Product** | User experience | UX guidelines, user guides, examples | **PDR** |
| **40-Operations** | Process and procedures | Workflows, runbooks, metrics | **OPR** |
| **50-Governance** | Compliance and ethics | Policies, risk management, standards | **GDR** |
| **60-AI** | AI integration | Agent handbooks, safety guidelines | **AIR** |
| **70-Communications** | External content | Branding, presentations, public docs | - |
| **80-Meta** | System governance | Templates, processes, automation | **MDR** |

### **Decision Record Families**

All decision records follow a consistent schema:
- **Context** - What issue is motivating this decision?
- **Decision** - What change are we proposing?
- **Consequences** - What becomes easier or more difficult?
- **Alternatives Considered** - What other options were evaluated?
- **Implementation Notes** - How will this be implemented?
- **Review Date** - When should this be reviewed?

### **Decision Record Types**
- **SDR** - Strategy Decision Record (10-Strategy)
- **ADR** - Architecture Decision Record (20-Architecture)
- **PDR** - Product Decision Record (30-Product)
- **OPR** - Operational Decision Record (40-Operations)
- **GDR** - Governance Decision Record (50-Governance)
- **AIR** - AI Decision Record (60-AI)
- **MDR** - Meta Decision Record (80-Meta)

---

## Consequences

### **Positive Impacts**
- **Clear Organization**: Content organized by domain rather than file type
- **Consistent Decision Making**: All decisions follow the same schema
- **Scalable Structure**: Easy to add new content and decision records
- **Role-Based Navigation**: Different users can find relevant information quickly
- **Maintainable Framework**: Clear processes for maintaining documentation

### **Risks and Mitigations**
- **Migration Complexity**: Moving existing content to new structure → Mitigation: Phased migration approach
- **Learning Curve**: Team needs to adapt to new structure → Mitigation: Comprehensive documentation and training
- **Maintenance Overhead**: More structured approach requires more effort → Mitigation: Automated tools and processes

### **Resource Requirements**
- **Migration Time**: 2-3 weeks for complete migration
- **Training**: Team education on new structure and processes
- **Tools**: Documentation tools and templates
- **Ongoing Maintenance**: Regular review and update processes

---

## Alternatives Considered

### **Alternative 1: Flat Structure with Better Indexing**
- **Pros**: Simpler migration, familiar structure
- **Cons**: Still difficult to navigate, no domain separation, hard to scale
- **Decision**: Rejected - doesn't solve fundamental organization issues

### **Alternative 2: Single Decision Record Type**
- **Pros**: Simpler framework, less complexity
- **Cons**: No domain-specific guidance, harder to find relevant decisions
- **Decision**: Rejected - loses domain-specific context and guidance

### **Alternative 3: External Documentation Platform**
- **Pros**: Professional tools, better collaboration features
- **Cons**: Vendor lock-in, additional costs, migration complexity
- **Decision**: Rejected - prefer to maintain control and avoid external dependencies

---

## Implementation Notes

### **Phase 1: Foundation Setup (Week 1)**
- Create new directory structure (00-80)
- Create foundation documents (vision, principles, onboarding)
- Establish decision record templates and schemas

### **Phase 2: Content Migration (Week 2)**
- Migrate existing content to appropriate domains
- Create decision record indexes for each family
- Update cross-references and navigation

### **Phase 3: Decision Records (Week 3)**
- Migrate existing decision records to new structure
- Create missing decision record families
- Establish review and maintenance processes

### **Phase 4: Cleanup and Validation (Week 4)**
- Archive old documentation
- Validate all links and references
- Create migration completion report

### **Success Metrics**
- **Navigation Efficiency**: Users can find information in < 3 clicks
- **Decision Consistency**: All decisions follow consistent schema
- **Content Organization**: 100% of content properly categorized
- **Team Adoption**: Team successfully uses new structure

---

## Review Date

**Next Review**: 2026-01-16 (3 months after implementation)

**Review Triggers**:
- Team feedback on navigation and usability
- Content organization challenges
- Decision-making process effectiveness
- Scalability requirements changes

---

**Decision Makers**: User (Project Owner), AI Assistant (Implementation Partner)
**Consulted**: Project team, existing documentation
**Informed**: All stakeholders in the meta-repo-seed project

*This MDR follows the Meta-Repo-Seed Meta decision framework.*
