# License Policy for Meta-Repo Seed

## Overview

Meta-Repo Seed is distributed under the **MIT License** to ensure maximum compatibility and freedom for Business-in-a-Box users, including startups, charities, non-profits, and SMBs.

## Approved Dependency Licenses

### ✅ **Fully Compatible Licenses**
These licenses are approved for dependencies without restrictions:

- **MIT License** - Maximum compatibility, no restrictions
- **BSD License (2-clause, 3-clause)** - Permissive, attribution required
- **Apache License 2.0** - Permissive, patent protection included
- **ISC License** - Simplified permissive license
- **Unlicense** - Public domain equivalent

### ⚠️ **Compatible with Restrictions**
These licenses are acceptable but require compliance monitoring:

- **LGPL (GNU Lesser General Public License)** 
  - **Allowed**: When used as libraries (dynamic linking)
  - **Required**: Must not modify LGPL code directly
  - **Usage**: Database drivers, networking libraries, utilities
  
- **MPL 2.0 (Mozilla Public License)**
  - **Allowed**: File-level copyleft compatible with MIT
  - **Required**: Changes to MPL files must remain MPL
  - **Usage**: Limited use in utility libraries

### ❌ **Prohibited Licenses**
These licenses are **incompatible** with MIT and **not allowed**:

- **GPL (GNU General Public License)** - Any version
- **AGPL (GNU Affero General Public License)** - Any version  
- **SSPL (Server Side Public License)** - Copyleft for hosted services
- **Commons Clause** - Restricts commercial use
- **BUSL (Business Source License)** - Commercial restrictions

### ❓ **Unknown/Unclear Licenses**
Dependencies with unknown licenses require investigation:
- **Action**: Research actual license terms
- **Timeline**: Must be clarified within 30 days
- **Escalation**: Legal review if terms unclear

## Enforcement Process

### 1. **Automated Checking**
- CI/CD pipeline automatically scans all dependencies
- Build fails if GPL or prohibited licenses detected
- Reports generated for legal review

### 2. **Manual Review Process**
- **Monthly**: Review unknown/unclear licenses
- **Quarterly**: Complete license audit
- **Before Release**: License compliance verification

### 3. **Violation Response**
If prohibited licenses are detected:
1. **Immediate**: Block deployment/release
2. **Research**: Find MIT-compatible alternatives
3. **Replace**: Update dependencies within 48 hours
4. **Document**: Update this policy if needed

## Business Impact

### For Business-in-a-Box Users
- **Commercial Use**: Unrestricted commercial usage rights
- **Distribution**: Can distribute generated projects freely
- **Modification**: Can modify and customize without license conflicts
- **Enterprise**: Meets corporate legal requirements

### For Meta-Repo Seed Development
- **Contribution**: Contributors retain rights while enabling commercial use
- **Integration**: Compatible with proprietary systems
- **Growth**: Supports various business models and monetization

## Current Compliance Status

✅ **GPL Violations Resolved**: All GPL-licensed dependencies removed  
⚠️ **LGPL Dependencies**: 3 libraries (chardet, paramiko, psycopg2-binary) - MIT compatible  
📋 **Unknown Licenses**: Under investigation, documented in LICENSE_AUDIT.md

## Implementation Guidelines

### For Developers
```bash
# Before adding new dependencies
pip install pip-licenses
pip-licenses --fail-on GPL --fail-on GPLv2 --fail-on AGPL

# Check specific package
pip-licenses | grep package-name
```

### For Code Reviews
- [ ] Verify new dependencies have compatible licenses
- [ ] Check transitive dependencies for license issues
- [ ] Update LICENSE_AUDIT.md if new dependencies added
- [ ] Escalate to legal team if uncertain

### For Releases
- [ ] Run complete license audit before release
- [ ] Verify no GPL dependencies present
- [ ] Update compliance documentation
- [ ] Generate license report for stakeholders

## Legal Contacts

**Internal Review**: Development Team  
**Legal Questions**: [Contact legal team when available]  
**Escalation**: Project maintainers

## Policy Updates

**Last Updated**: 2025-09-27  
**Next Review**: 2025-12-27  
**Version**: 1.0  

**Change Process**: Updates require legal review and team approval

---

*This policy ensures Meta-Repo Seed remains freely usable for all Business-in-a-Box deployment scenarios while maintaining legal compliance and professional standards.*
