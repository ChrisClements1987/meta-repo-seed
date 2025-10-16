# OPR-001: Unified Kanban Workflow for Project Management

**Date**: 2025-10-16
**Status**: Accepted
**Review Date**: 2026-01-16

---

## Context

We need to establish a unified project management workflow that treats all work items equally while maintaining clear categorization and prioritization. Currently, we have a basic Kanban board but lack a comprehensive framework for managing different types of work items.

The current approach treats technical debt as a separate category, but we recognize that all work items should be prioritized together based on business value, effort, and urgency rather than being siloed by type.

**Current State**:
- Basic Kanban board with limited work item types
- Technical debt treated as separate category
- No unified prioritization framework
- Variable daily capacity not well accommodated

**Requirements**:
- Unified prioritization across all work types
- Clear categorization without silos
- Flexible capacity management
- Comprehensive work item taxonomy

---

## Decision

**Adopt a unified Kanban workflow with comprehensive work item types and standardized prioritization criteria.**

### **Work Item Types**

#### **Product Management**
- **Epics** - Large initiatives spanning multiple sprints
- **Features** - Deliverable functionality for users
- **User Stories** - User-focused requirements with acceptance criteria

#### **Development Work**
- **Tech Debt** - Code quality, refactoring, and maintenance work
- **Bugs** - Defects and issues requiring fixes
- **Infrastructure Tasks** - DevOps, deployment, and system maintenance

#### **Process & Quality**
- **Process Improvement Work** - Workflow optimization and team efficiency
- **Documentation Tasks** - User docs, dev docs, architecture docs
- **Testing Tasks** - Setup, automation, unit tests, integration tests, UAT

#### **Research & Planning**
- **Research Projects** - Investigation and analysis work
- **Spikes** - Time-boxed exploration of technical solutions
- **Project Tasks/Meetings** - Backlog grooming, reviews, retrospectives

### **Prioritization Framework**

All work items prioritized using unified scoring system:

#### **Business Value** (1-5 scale)
- **5**: Critical for business success
- **4**: High business impact
- **3**: Moderate business value
- **2**: Low business impact
- **1**: Minimal business value

#### **Effort** (1-5 scale)
- **5**: Very high effort (weeks)
- **4**: High effort (days)
- **3**: Medium effort (hours)
- **2**: Low effort (minutes to hours)
- **1**: Minimal effort (minutes)

#### **Urgency** (1-5 scale)
- **5**: Critical - blocking other work
- **4**: High - needed soon
- **3**: Medium - can wait
- **2**: Low - nice to have
- **1**: Minimal - whenever

#### **Risk** (1-5 scale)
- **5**: High risk - could break things
- **4**: Medium-high risk
- **3**: Medium risk
- **2**: Low risk
- **1**: Minimal risk

**Priority Score Formula**: `Business Value + Urgency - Effort - Risk`

### **Kanban Board Structure**

#### **Backlog** (Unified)
- All work items regardless of type
- Sorted by priority score
- Tagged with work item type and effort estimate

#### **Ready to Pull**
- Items that meet Definition of Ready
- No dependencies blocking work
- Clear acceptance criteria
- Effort estimate within capacity range

#### **In Progress** (WIP Limits)
- **Development Work**: 2 items maximum
- **Research/Spikes**: 1 item maximum
- **Process Work**: 1 item maximum

#### **Review**
- Completed work awaiting review
- **WIP Limit**: 3 items maximum

#### **Done**
- Completed and accepted work

---

## Consequences

### **Positive Impacts**
- **Unified Prioritization**: All work items evaluated on same criteria
- **Better Resource Allocation**: Clear visibility into all work types
- **Reduced Silos**: No artificial separation between work types
- **Improved Planning**: Better capacity planning across all work
- **Quality Focus**: Tech debt gets appropriate priority alongside features

### **Risks and Mitigations**
- **Initial Complexity**: More detailed categorization required → Mitigation: Comprehensive templates and training
- **Learning Curve**: Team needs to adapt to new prioritization system → Mitigation: Gradual implementation with support
- **Overhead**: More detailed scoring and tagging required → Mitigation: Streamlined tools and processes

### **Resource Requirements**
- **Personnel**: Project team (AI Assistant + User)
- **Tools**: Existing Kanban board (KANBAN_BOARD.md)
- **Time**: 2-3 hours for initial setup, ongoing maintenance

---

## Alternatives Considered

### **Alternative 1: Separate Boards by Work Type**
- **Pros**: Clear separation of concerns, specialized workflows
- **Cons**: Creates silos, difficult cross-type prioritization, resource allocation complexity
- **Decision**: Rejected - creates artificial barriers

### **Alternative 2: Traditional Sprint-Based Approach**
- **Pros**: Well-established methodology, clear time boundaries
- **Cons**: Inflexible for variable capacity, doesn't accommodate diverse work types
- **Decision**: Rejected - doesn't align with variable capacity

### **Alternative 3: Simple Todo List**
- **Pros**: Minimal overhead, easy to understand
- **Cons**: Lacks structure, no clear work item types, poor visibility
- **Decision**: Rejected - too simplistic for diverse requirements

---

## Implementation Notes

### **Phase 1: Framework Design (Week 1)**
- Create comprehensive work item templates
- Design prioritization framework
- Establish Definition of Ready criteria

### **Phase 2: Board Migration (Week 2)**
- Update Kanban board with new structure
- Migrate existing work items to new system
- Train team on prioritization framework

### **Phase 3: Full Implementation (Week 3)**
- Complete implementation and refinement
- Establish work item type guidelines
- Monitor and adjust based on usage

### **Success Metrics**
- **Unified Prioritization**: All work items scored consistently
- **Capacity Management**: Better resource allocation across work types
- **Quality Improvement**: Tech debt addressed appropriately
- **Team Adoption**: Smooth transition to new system

---

## Review Date

**Next Review**: 2026-01-16 (3 months after implementation)

**Review Triggers**:
- Team feedback on prioritization effectiveness
- Capacity management improvements
- Work item categorization challenges
- Process efficiency metrics

---

**Decision Makers**: User (Project Owner), AI Assistant (Implementation Partner)
**Consulted**: Project team, existing process documentation
**Informed**: All stakeholders in the meta-repo-seed project

*This OPR follows the Meta-Repo-Seed Operations decision framework.*
