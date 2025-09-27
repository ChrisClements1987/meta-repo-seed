# License Compliance Audit Report

**Date**: 2025-09-27  
**Auditor**: Automated scan + manual review  
**Purpose**: Ensure MIT license compatibility for Business-in-a-Box users

## Executive Summary

⚠️ **3 GPL-licensed dependencies** identified that require immediate attention for MIT license compliance. Most are development dependencies not needed for core functionality.

## Critical Issues (GPL License Conflicts)

### 🔴 **pyinstaller (GPLv2)**
- **Version**: 6.16.0
- **License**: GNU General Public License v2 (GPLv2)
- **Special Note**: Has commercial use exception for bundled applications
- **Usage**: Not used in core seeding.py functionality
- **Action**: **REMOVE** - Not needed for meta-repo seeding

### 🔴 **text-unidecode (GPL/Artistic)**
- **Version**: 1.3  
- **License**: Artistic License; GNU General Public License (GPL)
- **Required By**: python-slugify
- **Usage**: Not used in core functionality
- **Action**: **REMOVE** python-slugify dependency

### 🔴 **truffleHogRegexes (GNU)**
- **Version**: 0.0.7
- **License**: GNU (unclear version)
- **Usage**: Likely transitive dependency
- **Action**: **INVESTIGATE** and remove if not essential

## LGPL Dependencies (Require Compliance Review)

### 🟡 **chardet (LGPLv2+)**
- **Version**: 5.2.0
- **License**: GNU Lesser General Public License v2 or later (LGPLv2+)
- **Usage**: Character encoding detection
- **Compliance**: LGPL allows dynamic linking without GPL requirements
- **Action**: **KEEP** - LGPL compatible with MIT when used as library

### 🟡 **paramiko (LGPL)**
- **Version**: 3.5.1
- **License**: GNU Library or Lesser General Public License (LGPL)
- **Usage**: SSH functionality
- **Compliance**: LGPL compatible when used as library
- **Action**: **KEEP** - LGPL compatible with MIT

### 🟡 **psycopg2-binary (LGPL)**
- **Version**: 2.9.10
- **License**: GNU Library or Lesser General Public License (LGPL)
- **Usage**: PostgreSQL adapter
- **Compliance**: LGPL compatible when used as library
- **Action**: **KEEP** - LGPL compatible with MIT

## Unknown/Unclear Licenses (Require Investigation)

### ❓ **High Priority Clarification Needed**
- **CacheControl**: UNKNOWN
- **Flask**: UNKNOWN (should be BSD)
- **alembic**: UNKNOWN (should be MIT)
- **anyio**: UNKNOWN (should be MIT)
- **astroid**: UNKNOWN (should be GPL - part of pylint)
- **attrs**: UNKNOWN (should be MIT)
- **click**: UNKNOWN (should be BSD)
- **jsonschema**: UNKNOWN (should be MIT)
- **pylint**: UNKNOWN (should be GPL)

## Remediation Plan

### Immediate Actions (This Sprint)

1. **Remove GPL Dependencies**
   ```bash
   # Remove pyinstaller (not needed for core functionality)
   pip uninstall pyinstaller pyinstaller-hooks-contrib
   
   # Remove python-slugify and text-unidecode (not used)
   pip uninstall python-slugify text-unidecode
   
   # Remove truffleHogRegexes (investigate first)
   pip uninstall truffleHogRegexes
   ```

2. **Create Clean Requirements Files**
   ```bash
   # Generate current requirements without GPL packages
   pip freeze | grep -v -E "(pyinstaller|text-unidecode|truffleHogRegexes)" > requirements-clean.txt
   ```

3. **Add License Checking to CI/CD**
   ```yaml
   - name: License Compliance Check
     run: |
       pip install pip-licenses
       pip-licenses --fail-on GPL --fail-on "GPLv2" --allow LGPL
   ```

### Short-term Actions (Next Sprint)

1. **Clarify Unknown Licenses**
   - Research each UNKNOWN dependency
   - Contact maintainers for clarification
   - Document findings in this file

2. **Implement License Policy**
   - Document approved licenses
   - Add license checking to PR requirements
   - Train team on license compliance

### Long-term Actions (Next Month)

1. **Regular License Audits**
   - Quarterly dependency license reviews
   - Automated license monitoring
   - Update compliance documentation

## License Compatibility Matrix

| License Type | Compatible with MIT | Action Required |
|--------------|-------------------|-----------------|
| MIT | ✅ Yes | None |
| BSD (2/3-clause) | ✅ Yes | None |
| Apache 2.0 | ✅ Yes | None |
| LGPL | ⚠️ Yes* | Dynamic linking only |
| MPL 2.0 | ⚠️ Yes* | File-level copyleft |
| GPL/GPLv2 | ❌ No | Remove or replace |
| UNKNOWN | ❓ Research | Investigate and clarify |

*Requires compliance with specific terms

## Success Criteria

- [ ] Zero GPL-licensed dependencies in production
- [ ] All UNKNOWN licenses investigated and documented
- [ ] License checking integrated into CI/CD
- [ ] License compliance policy documented
- [ ] Team trained on license requirements

## Compliance Statement

After remediation, this project will be fully MIT-license compliant, enabling Business-in-a-Box users to:
- Use the tool commercially without restrictions
- Distribute generated projects with clear licensing
- Meet enterprise legal requirements
- Integrate with proprietary systems confidently

---

**Next Review Date**: 2025-12-27 (Quarterly)  
**Owner**: Development Team  
**Approval**: Legal Review Required
