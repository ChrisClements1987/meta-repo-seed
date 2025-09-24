# Structure.json Migration Guide

**Version**: v1.0 → v2.0  
**Related**: Issue #23 - Design Architecture for structure.json Processing  
**Date**: 2025-09-24  

## 🎯 Overview

This guide explains how to migrate existing `structure.json` files from the current format (v1.0) to the enhanced v2.0 format that supports the new `StructureParser` architecture.

## 📋 Migration Changes

### 1. Metadata Restructuring

**Before (v1.0):**
```json
{
  "project_name": "quantum",
  "github_username": "Chris Clements",
  "created_date": "2025-09-24",
  "version": "1.0.0",
  "structure": { ... }
}
```

**After (v2.0):**
```json
{
  "metadata": {
    "project_name": "quantum",
    "github_username": "Chris Clements",
    "created_date": "2025-09-24",
    "updated_date": "2025-09-24",
    "version": "1.0.0",
    "schema_version": "2.0.0"
  },
  "structure": { ... }
}
```

### 2. Required Fields

**New Required Fields:**
- `metadata.schema_version`: Must be "2.0.0"
- `metadata.updated_date`: Automatically set during migration

**Field Validation:**
- `metadata.project_name`: Must match pattern `^[a-zA-Z][a-zA-Z0-9-_]*$`
- `metadata.version`: Must follow semantic versioning pattern
- File names: Must match pattern `^[a-zA-Z0-9][a-zA-Z0-9.-_]*\\.[a-zA-Z0-9]+$`

## 🔧 Automated Migration

### Using the Migration Script

```python
# Example migration script usage
from structure_migration import migrate_structure_file

# Migrate existing file
migrate_structure_file(
    input_path=Path("governance/structure/structure.json"),
    output_path=Path("governance/structure/structure.json"),  # Can overwrite
    backup=True  # Creates structure.json.backup
)
```

### Migration Script Implementation

```python
#!/usr/bin/env python3
"""
Migration script for structure.json v1.0 → v2.0
"""

import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

def migrate_structure_file(input_path: Path, output_path: Path, backup: bool = True) -> None:
    """
    Migrate structure.json from v1.0 to v2.0 format.
    
    Args:
        input_path: Path to existing structure.json
        output_path: Path for migrated file (can be same as input)
        backup: Whether to create backup of original file
    """
    
    # Load existing structure
    with open(input_path, 'r', encoding='utf-8') as f:
        old_structure = json.load(f)
    
    # Create backup if requested
    if backup and input_path == output_path:
        backup_path = input_path.with_suffix('.json.backup')
        shutil.copy2(input_path, backup_path)
        print(f"Backup created: {backup_path}")
    
    # Migrate to v2.0 format
    new_structure = migrate_structure_data(old_structure)
    
    # Save migrated structure
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(new_structure, f, indent=2, ensure_ascii=False)
    
    print(f"Migrated {input_path} → {output_path}")

def migrate_structure_data(old_data: Dict[str, Any]) -> Dict[str, Any]:
    """Convert v1.0 structure data to v2.0 format."""
    
    # Extract metadata from root level
    metadata = {
        "project_name": old_data.get("project_name", ""),
        "github_username": old_data.get("github_username", ""),
        "version": old_data.get("version", "1.0.0"),
        "schema_version": "2.0.0"
    }
    
    # Add dates
    if "created_date" in old_data:
        metadata["created_date"] = old_data["created_date"]
    else:
        metadata["created_date"] = datetime.now().strftime("%Y-%m-%d")
    
    metadata["updated_date"] = datetime.now().strftime("%Y-%m-%d")
    
    # Structure remains the same
    structure = old_data.get("structure", {})
    
    return {
        "metadata": metadata,
        "structure": structure
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python migrate_structure.py <structure.json>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    migrate_structure_file(input_file, input_file, backup=True)
```

## 🔍 Validation

### Schema Validation

After migration, validate the new structure:

```python
import json
import jsonschema
from pathlib import Path

# Load schema and structure
with open("schemas/structure-v2.json", "r") as f:
    schema = json.load(f)

with open("governance/structure/structure.json", "r") as f:
    structure = json.load(f)

# Validate
try:
    jsonschema.validate(structure, schema)
    print("✅ Structure is valid v2.0 format")
except jsonschema.ValidationError as e:
    print(f"❌ Validation error: {e.message}")
```

### Manual Validation Checklist

- [ ] `metadata` section exists and contains all required fields
- [ ] `metadata.schema_version` is set to "2.0.0"  
- [ ] `metadata.project_name` follows naming pattern
- [ ] `metadata.version` follows semantic versioning
- [ ] `structure` section is unchanged from original
- [ ] All file names have valid extensions
- [ ] JSON is properly formatted and valid

## 🔄 Backwards Compatibility

The new `StructureParser` will automatically detect and migrate v1.0 structures:

```python
class StructureParser:
    def parse_structure_file(self, file_path: Path) -> StructureData:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Auto-detect version and migrate if needed
        if not data.get('metadata', {}).get('schema_version'):
            # v1.0 format detected - auto-migrate
            data = migrate_structure_data(data)
            print(f"Auto-migrated {file_path} from v1.0 to v2.0")
        
        return StructureData(data)
```

## 📝 Example Migration

### Before (Current seeding.py output):

```json
{
  "project_name": "quantum",
  "github_username": "Chris Clements", 
  "created_date": "2025-09-24",
  "version": "1.0.0",
  "structure": {
    "cloud-storage": {
      "strategy": ["vision.md", "mission.md", "strategic-roadmap.md"]
    },
    "meta-repo": {
      "governance": {
        "structure": ["structure.json", "meta-repo-schema.json"]
      }
    }
  }
}
```

### After (v2.0 format):

```json
{
  "metadata": {
    "project_name": "quantum",
    "github_username": "Chris Clements",
    "created_date": "2025-09-24", 
    "updated_date": "2025-09-24",
    "version": "1.0.0",
    "schema_version": "2.0.0"
  },
  "structure": {
    "cloud-storage": {
      "strategy": ["vision.md", "mission.md", "strategic-roadmap.md"]
    },
    "meta-repo": {
      "governance": {
        "structure": ["structure.json", "meta-repo-schema.json"]
      }
    }
  }
}
```

## ⚠️ Breaking Changes

### Validation Changes
- Project names must start with letter and contain only alphanumeric, hyphens, underscores
- File names must have valid extensions  
- Semantic versioning required for version field

### API Changes  
- Direct access to root-level metadata fields will break
- Use `structure_data.metadata.project_name` instead of `structure_data.project_name`

### Migration Required For
- All existing `structure.json` files
- Any scripts that directly access metadata fields
- Templates that generate structure.json files

## ✅ Migration Checklist

### For Existing Projects
- [ ] Backup existing structure.json files
- [ ] Run migration script on all structure.json files
- [ ] Validate migrated files against v2.0 schema
- [ ] Test automation scripts with migrated structures
- [ ] Update any custom scripts that access metadata

### For Development  
- [ ] Update seeding.py to generate v2.0 format
- [ ] Update structure templates
- [ ] Update documentation examples
- [ ] Add migration script to repository
- [ ] Update automation scripts to use new parser

---

**Next Steps**: Run migration on existing structure.json files and update seeding.py to generate v2.0 format.