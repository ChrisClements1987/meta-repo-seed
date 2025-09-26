# Project Structure Guidelines

This document defines the mandatory project structure for the Business-in-a-Box meta-repo-seed project to maintain organization, clarity, and AI context.

## 🎯 Core Principle

**Keep the root directory clean and organized.** Every file should have a clear, logical location that supports both human understanding and AI assistance.

## 📁 Required Directory Structure

```
meta-repo-seed/
├── 📄 README.md                    # Project overview (REQUIRED)
├── 📄 LICENSE                      # License file (REQUIRED)
├── 📄 .gitignore                   # Git ignore patterns
├── 📄 pytest.ini                  # Test configuration
├── 📄 requirements*.txt            # Python dependencies
├── 📄 seeding.py                   # Legacy main script (to be deprecated)
├── 📄 PROJECT_NORTH_STAR.md        # Strategic vision (REQUIRED)
├── 📄 AGENTS.md                    # AI context and workflows (REQUIRED)
│
├── 📁 src/                         # ALL source code
│   ├── meta_repo_seed/             # Main package
│   ├── blueprints/                 # Business blueprint system
│   ├── cli/                        # Command-line interface
│   ├── templates/                  # Template generation
│   └── providers/                  # Cloud platform providers
│
├── 📁 tests/                       # ALL test files
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── conftest.py                 # Test configuration
│
├── 📁 scripts/                     # ALL utility scripts
│   ├── maintenance/                # Maintenance utilities
│   ├── demo/                       # Demo and example scripts  
│   └── roadmap_manager.py          # Development tools
│
├── 📁 docs/                        # ALL documentation
│   ├── guides/                     # User guides
│   ├── architecture/               # Technical architecture
│   ├── development/                # Development process
│   └── research/                   # Analysis and research
│
├── 📁 templates/                   # Template files for seeding
├── 📁 examples/                    # Usage examples
├── 📁 schemas/                     # JSON schemas
├── 📁 configs/                     # Configuration files
│
└── 📁 .github/                     # GitHub workflows and templates
    ├── workflows/                  # CI/CD workflows
    └── PULL_REQUEST_TEMPLATE/      # PR templates
```

## 🚫 What NOT to Put in Root

### ❌ **Forbidden in Root Directory:**
- Ad-hoc markdown files (`BACKLOG_GROOMING_SUMMARY.md`, `DEVELOPMENT_WORKFLOW.md`)
- Implementation summaries (`ISSUE_33_IMPLEMENTATION_SUMMARY.md`)  
- Demo scripts (`demo_parser.py`)
- Maintenance scripts (`sync_structures.py`)
- Analysis directories (`analysis/`)
- Temporary files or directories
- Individual issue documentation
- Process documentation
- Research notes

### ✅ **Exceptions (Only These Allowed):**
- `README.md` - Main project README
- `LICENSE` - Project license
- `PROJECT_NORTH_STAR.md` - Strategic vision document  
- `AGENTS.md` - AI context and development workflows
- `seeding.py` - Legacy main script (temporary, will be moved to src/)
- Standard configuration files (pytest.ini, .gitignore, requirements.txt, etc.)

## 📋 File Placement Rules

### 📚 Documentation Files

| File Type | Examples | Proper Location |
|-----------|----------|-----------------|
| User guides | How-to guides, tutorials | `docs/guides/` |
| Architecture docs | ADRs, system design | `docs/architecture/` |
| Development process | Workflow, contributing | `docs/development/` |
| Issue summaries | Implementation notes | `docs/development/implementation-notes/` |
| Analysis/Research | Analysis reports, research | `docs/research/` |
| Project roadmap | Roadmap, changelog | `docs/development/` |

### 🔧 Script Files

| Script Type | Examples | Proper Location |
|-------------|----------|-----------------|
| Maintenance scripts | Sync, cleanup utilities | `scripts/maintenance/` |
| Demo scripts | Examples, demonstrations | `scripts/demo/` |
| Build/deployment | CI/CD helpers | `scripts/build/` |
| Development tools | Roadmap manager, helpers | `scripts/` |

### 💻 Source Code

| Code Type | Examples | Proper Location |
|-----------|----------|-----------------|
| Main application code | Core modules | `src/meta_repo_seed/` |
| CLI interfaces | Command handlers | `src/cli/` |
| Template systems | Template engines | `src/templates/` |
| Business logic | Blueprint parsers | `src/blueprints/` |

### 🧪 Tests

| Test Type | Examples | Proper Location |
|-----------|----------|-----------------|
| Unit tests | Function/class tests | `tests/unit/` |
| Integration tests | End-to-end tests | `tests/integration/` |
| Test utilities | Test helpers, fixtures | `tests/` |

## 🔍 Automated Enforcement

### GitHub Workflows
- **Structure Compliance Check** - Automatically validates root directory
- **Link Validation** - Ensures documentation links work
- **Roadmap Synchronization** - Validates roadmap updates

### PR Template Requirements
All pull requests must include:
- ✅ **Project Structure Compliance** - Files placed in correct locations
- ✅ **Root Directory Cleanup** - No violations of root directory rules
- ✅ **File Placement Verification** - Proper categorization confirmed

### Cleanup Tools
- **`scripts/maintenance/cleanup_structure.py`** - Identifies and fixes violations
- **Dry-run mode** - Preview changes before applying
- **Auto-move functionality** - Batch fix common violations

## 🎯 Why This Matters

### For Human Developers
- **Quick navigation** - Find files where you expect them
- **Clear ownership** - Each directory has a specific purpose
- **Reduced cognitive load** - Less time hunting for files

### For AI Assistance  
- **Better context** - AI understands project organization
- **Accurate suggestions** - AI knows where to create new files
- **Proper imports** - AI generates correct import paths

### For Business-in-a-Box Vision
- **Professional appearance** - Clean, organized project structure
- **Enterprise standards** - Follows industry best practices  
- **Scalability** - Structure supports growth and complexity

## 🛠️ Migration Guide

### Current Violations (as of September 2025)

Files that need to be moved:

```bash
# Run the cleanup tool to see current violations:
python scripts/maintenance/cleanup_structure.py

# Fix violations automatically:
python scripts/maintenance/cleanup_structure.py --fix

# Or fix with auto-confirmation:
python scripts/maintenance/cleanup_structure.py --fix --auto-yes
```

### Manual Steps After Cleanup

1. **Update imports** - Fix Python import statements for moved modules
2. **Update documentation links** - Fix references to moved files  
3. **Test functionality** - Ensure everything still works
4. **Update .gitignore** - Add patterns to prevent future violations
5. **Document changes** - Update PR with structure compliance checklist

## 📝 Adding New Files

### Before Creating Any File, Ask:
1. **What type of file is this?** (code, docs, script, config, test)
2. **Who is the audience?** (users, developers, AI, systems)  
3. **Where does this logically belong?** (follow the directory structure)
4. **Is this temporary?** (if yes, consider scripts/temp/ or don't commit)

### Decision Tree:
```
Is it source code?     → src/
Is it a test?          → tests/
Is it a script?        → scripts/
Is it documentation?   → docs/
Is it a template?      → templates/
Is it configuration?   → configs/ or root (if build config)
Is it an example?      → examples/
Is it temporary?       → Don't commit it!
```

## ⚠️ Consequences of Violations

### Automated Blocks
- **PR template requires** structure compliance checkbox
- **GitHub workflow fails** if root violations found
- **CI pipeline blocks** merge until fixed

### Development Impact
- **Slowed development** - Time wasted searching for files
- **Broken AI assistance** - AI context becomes confused
- **Reduced professionalism** - Project appears disorganized
- **Technical debt** - Cleanup becomes increasingly difficult

## ✅ Benefits of Compliance

### Immediate Benefits
- **Faster development** - Know exactly where to find/place files
- **Better AI assistance** - AI understands project organization
- **Professional appearance** - Clean, enterprise-grade structure

### Long-term Benefits  
- **Easier onboarding** - New developers understand layout quickly
- **Scalable complexity** - Structure supports project growth
- **Maintainable codebase** - Clear separation of concerns
- **Enterprise readiness** - Meets professional standards

---

## 🎯 Remember: Clean Root = Clear Mind = Better Code

*This structure supports our Business-in-a-Box vision by providing enterprise-grade organization that scales from solo founder to mature technology organization.*