# AGENTS.md - Context Management & Architecture Overview

**Purpose**: Maintain comprehensive context while optimizing for AI agent efficiency
**Last Updated**: October 16, 2025
**Status**: Unified Kanban Development - Variable Capacity
**Current Focus**: Process hardening + commercial infrastructure
**Framework**: ODR-001 Unified Kanban Workflow

---

## 🎯 Executive Summary

**Project**: meta-repo-seed → Business-in-a-Box Commercial SaaS Platform
**Timeline**: Kanban development with variable capacity
**Current Phase**: Process hardening + commercial infrastructure completion
**Commercial Readiness**: 85% (up from 70% in Week 2)

**ClemNova Context**:
- Customer ID: `cf6965da-bf6e-4995-95e4-3729c1ad12f2`
- Organization ID: `00d184d2-8a78-45fb-8a5d-10bc46ce51b6`
- Plan: Growth (upgraded from Startup)
- Bootstrap Timeline: 2 months from now

---

## 🏗️ Architecture Overview

### **Multi-Tenant Commercial Architecture**
```
organizations/{org_id}/
├── meta-repo/           # Governance & automation
├── cloud-storage/       # Strategy & workspace
├── core-services/       # Shared platforms
├── saas-products/       # Individual products
└── partner-products/    # Collaborations
```

### **Core Components**
- **OrganizationSeeder**: Multi-tenant deployment engine
- **CustomerManager**: Customer lifecycle & subscription management
- **CommercialAPI**: REST API for programmatic access
- **Models**: Customer, Organization, Subscription, UsageMetrics

### **Subscription Plans**
- **Startup**: 1 product, 5 team, basic templates
- **Growth**: 5 products, 20 team, API access, webhooks
- **Scale**: 20 products, 100 team, analytics, monitoring
- **Enterprise**: Unlimited, SSO, audit logs, white-label

---

## 📋 2-Month Transformation Plan

### **✅ Week 1 Complete (Oct 1-7)**
- Multi-tenant architecture implemented
- Customer management system functional
- OrganizationSeeder replacing RepoSeeder
- REST API infrastructure ready
- Plan-based feature gating working
- Commercial CLI operational

### **🚀 Week 2 Current (Oct 8-14)**
**Goal**: Database persistence + API testing
- Implement PostgreSQL database schema
- Replace placeholder methods in CustomerManager
- Add comprehensive API tests (7% → 80% coverage)
- Build customer onboarding workflow

### **📅 Week 3-4 (Oct 15-28)**
**Goal**: ClemNova integration + validation
- ClemNova-specific configuration
- End-to-end deployment testing
- Performance optimization
- Security audit

### **📅 Month 2 (Nov-Dec)**
**Goal**: Commercial features + polish
- Billing integration
- Customer portal
- Enterprise features
- Market readiness

---

## 🎯 Current Unified Kanban Focus

### **Today's Capacity Assessment**
**Available Time**: Variable (adapts to daily availability)
**Current Priority**: Process hardening + infrastructure completion
**WIP Limit**: 2 items maximum
**Framework**: ODR-001 Unified Kanban Workflow

### **Ready to Pull** (Priority Score: 8+)
1. **Fix OrganizationSeeder NoneType error** (30 min) - **Score: 9** (Bug)
2. **Add API endpoint tests** (45 min) - **Score: 8** (Testing Task)

### **In Progress**
- Process hardening implementation (TDD + Git standards) - **Score: 7**

### **Recently Completed**
- ✅ Install pre-commit hooks (Score: 8) - Infrastructure Task
- ✅ Comprehensive test suite (21 tests, 40% coverage) - Testing Task
- ✅ Documentation structure update - Documentation Task
- ✅ Process improvement recommendations - Process Improvement

---

## 📊 Key Metrics & Status

### **Test Coverage**
- **Overall**: 56% (down from 61% due to new code)
- **Commercial**: 34% (needs improvement)
- **API**: 7% (critical priority)
- **Models**: 72% (good foundation)

### **Commercial Readiness**
- **Multi-tenancy**: ✅ 100% complete
- **Customer Management**: ✅ 80% complete
- **API Infrastructure**: ⚠️ 20% complete
- **Database Persistence**: ❌ 0% complete
- **Billing Integration**: ❌ 0% complete

### **ClemNova Readiness**
- **Customer Account**: ✅ Created
- **Organization**: ✅ Created
- **Deployment**: ⚠️ Needs database
- **Testing**: ❌ Needs comprehensive tests

---

## 🔧 Active Development Files

### **Core Commercial Infrastructure**
- `src/commercial/models/__init__.py` - Data models (72% coverage)
- `src/commercial/services/customer_manager.py` - Customer management (21% coverage)
- `src/commercial/services/organization_seeder.py` - Deployment engine (38% coverage)
- `src/commercial/api/__init__.py` - REST API (7% coverage)

### **Testing & Validation**
- `commercial_cli.py` - CLI for testing
- `WEEK2_FOCUS.md` - Current sprint goals

### **Architecture Reference**
- `seeding.py` - Original single-tenant implementation (80% coverage)
- `src/automation/business_operations.py` - Business automation (77% coverage)

---

## 🚨 Critical Path & Dependencies

### **Week 2 Blockers**
1. **Database Schema** - Required for customer persistence
2. **API Testing** - Required for production readiness
3. **Customer Onboarding** - Required for ClemNova bootstrap

### **ClemNova Dependencies**
1. **Production Database** - PostgreSQL with customer data
2. **Tested API** - 80%+ coverage for reliability
3. **Onboarding Workflow** - Guided setup process
4. **Performance Validation** - 10-minute deployment promise

---

## 🎯 Success Criteria

### **Week 2 Success**
- ✅ PostgreSQL database implemented
- ✅ API coverage 80%+
- ✅ Customer onboarding workflow complete
- ✅ ClemNova integration ready

### **ClemNova Bootstrap Success**
- ✅ Complete organization deployment in <10 minutes
- ✅ All commercial features functional
- ✅ Production-ready infrastructure
- ✅ Comprehensive test coverage

### **Commercial Launch Success**
- ✅ Multi-tenant SaaS platform
- ✅ Customer management system
- ✅ Billing & subscription management
- ✅ Enterprise features available

---

## 📚 Context Management Notes

**For AI Agents**: This document provides comprehensive context while maintaining focus on current priorities. Use this as the primary reference for:
- Overall project status and timeline
- Architecture decisions and rationale
- Current week priorities and blockers
- ClemNova-specific requirements and context

**Active Context**: Focus on Week 2 files and priorities. Reference this document for big picture context.

**Archived Context**: Week 1 deliverables are complete and committed to git. Reference this document for historical context.

---

*This document serves as the single source of truth for project context and should be updated as work progresses.*
