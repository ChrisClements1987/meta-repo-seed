# Management Scripts

This directory contains utility scripts for managing the Meta-Repo Seeding System project.

## 📋 Available Scripts

### `roadmap_manager.py`
**Purpose**: Manage roadmap features and changelog entries

**Usage**:
```bash
# List all roadmap features
python scripts/roadmap_manager.py list

# Add new feature to roadmap
python scripts/roadmap_manager.py add "Feature Name" "Feature description" --section "High Priority"

# Mark feature as completed (moves to changelog)
python scripts/roadmap_manager.py complete "Feature Name" "1.1.0" "Changelog description" --issue 5

# Generate roadmap summary report
python scripts/roadmap_manager.py report
```

**Features**:
- ✅ Add features to roadmap with priority sections
- ✅ Move completed features to changelog
- ✅ Support GitHub issue references
- ✅ Generate summary statistics
- ✅ Automatic roadmap and changelog formatting

### `create_roadmap_issues.py`
**Purpose**: Automatically create GitHub issues from roadmap items

**Usage**:
```bash
# Dry run to see what would be created
python scripts/create_roadmap_issues.py --dry-run --limit 5

# Create issues for high priority features
python scripts/create_roadmap_issues.py --priority high --limit 3

# Create issues for specific section
python scripts/create_roadmap_issues.py --section "Next Release" --limit 5

# Create all issues (use with caution)
python scripts/create_roadmap_issues.py
```

**Requirements**:
- GitHub CLI (`gh`) installed and authenticated
- Repository must be a GitHub repository

**Features**:
- ✅ Parse roadmap and extract features
- ✅ Create properly formatted GitHub issues
- ✅ Apply appropriate labels (`roadmap`, `priority:*`, `enhancement`)
- ✅ Include structured issue templates
- ✅ Filter by section or priority
- ✅ Dry-run mode for testing

### `map_issues_to_roadmap.py`
**Purpose**: Link existing GitHub issues to roadmap items

**Usage**:
```bash
# Dry run to see what would be updated
python scripts/map_issues_to_roadmap.py --dry-run

# Update roadmap with issue references
python scripts/map_issues_to_roadmap.py
```

**Requirements**:
- GitHub CLI (`gh`) installed and authenticated
- Existing GitHub issues with matching feature names

**Features**:
- ✅ Match GitHub issues to roadmap features by name
- ✅ Add clickable issue links to roadmap
- ✅ Maintain roadmap formatting
- ✅ Show preview of changes in dry-run mode

## 🚀 Complete Workflow

Here's how to use these scripts together for complete feature management:

### 1. Initial Setup (Done Once)
```bash
# Create GitHub labels
gh label create "roadmap" --description "Features from the project roadmap" --color "0E8A16"
gh label create "priority: high" --description "High priority items" --color "D73A4A"
gh label create "priority: medium" --description "Medium priority items" --color "FFA500"
gh label create "priority: low" --description "Low priority items" --color "FBCA04"
```

### 2. Adding New Features
```bash
# Add feature to roadmap
python scripts/roadmap_manager.py add "New Feature" "Description of the feature" --section "High Priority"

# Create GitHub issue for the feature
python scripts/create_roadmap_issues.py --section "High Priority" --limit 1

# Link the issue to the roadmap
python scripts/map_issues_to_roadmap.py
```

### 3. Working on Features
```bash
# List current features with issue numbers
python scripts/roadmap_manager.py list

# Create feature branch (example for issue #5)
git checkout -b feature/issue-5-configuration-file-support

# Work on feature...
git commit -m "Add YAML config loading - addresses #5"
```

### 4. Completing Features
```bash
# Mark feature as complete
python scripts/roadmap_manager.py complete "Configuration File Support" "1.1.0" "Users can save and load project configurations" --issue 5

# Feature is automatically moved from roadmap to changelog
```

### 5. Release Management
```bash
# Generate roadmap report before release
python scripts/roadmap_manager.py report

# Review changelog for release notes
cat CHANGELOG.md
```

## 🛠️ Development Tips

### Script Maintenance
- All scripts use the same patterns for file reading/writing
- Error handling includes helpful messages
- Support both dry-run and live modes where applicable
- Follow consistent CLI argument patterns

### Adding New Scripts
When adding new management scripts:
1. **Place in `scripts/` directory**
2. **Add documentation to this README**
3. **Follow existing CLI patterns** (argparse, dry-run support)
4. **Include error handling** with helpful messages
5. **Update main README.md** if script is user-facing

### Testing Scripts
Always test scripts in dry-run mode first:
```bash
python scripts/script_name.py --dry-run
```

## 📚 Dependencies

All scripts require:
- **Python 3.8+**
- **Standard library modules**: `argparse`, `re`, `pathlib`, `json`, `subprocess`

GitHub integration scripts additionally require:
- **GitHub CLI (`gh`)** installed and authenticated
- **Repository permissions** for creating issues and labels

---

*Keep this directory organized and document any new scripts you add!*