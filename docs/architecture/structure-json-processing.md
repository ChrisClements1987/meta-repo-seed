# Structure.json Processing Architecture

**Issue**: #23 - Design Architecture for structure.json Processing  
**Parent Epic**: #22 - Complete Automation Script Implementation  
**Status**: Analysis Phase  
**Date**: 2025-09-24  

## 🎯 Executive Summary

This document defines the architecture for parsing, validating, and processing `structure.json` files that define repository structures in the meta-repo seeding system. This analysis is based on the current implementation in `seeding.py` and establishes the foundation for all automation scripts.

## 🔍 Current State Analysis

### Schema Overview (from seeding.py)

Based on the `create_structure_json()` method in `seeding.py`, the current schema includes:

```json
{
  "project_name": "string",
  "github_username": "string", 
  "created_date": "2025-09-24",
  "version": "1.0.0",
  "structure": {
    "cloud-storage": { /* workspace and strategy structure */ },
    "meta-repo": { /* governance, automation, documentation */ },
    "core-services": { /* shared platforms */ },
    "saas-products": { /* individual products */ },
    "partner-products": { /* collaborations */ },
    "charity-products": { /* open-source projects */ }
  }
}
```

### Current Implementation Issues

1. **Hard-coded Structure**: The structure is completely hard-coded in `seeding.py`
2. **No Validation**: No validation against the existing schema file
3. **No Parser Abstraction**: Each script will need to reimplement parsing logic
4. **Static Date**: Created date is hard-coded to "2025-09-24"
5. **No Extension Mechanism**: Cannot customize structure for different project types

## 🏗️ Proposed Architecture

### 1. Schema Definition & Validation

#### Enhanced Schema Structure
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Meta Repository Structure Schema v2.0",
  "type": "object",
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "project_name": {"type": "string", "minLength": 1},
        "github_username": {"type": "string", "minLength": 1},
        "created_date": {"type": "string", "format": "date"},
        "updated_date": {"type": "string", "format": "date"},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "schema_version": {"type": "string", "enum": ["2.0"]}
      },
      "required": ["project_name", "github_username", "version", "schema_version"]
    },
    "structure": {
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z][a-zA-Z0-9-_]*$": {
          "$ref": "#/definitions/directory_node"
        }
      }
    }
  },
  "definitions": {
    "directory_node": {
      "oneOf": [
        {
          "type": "object",
          "patternProperties": {
            "^[a-zA-Z][a-zA-Z0-9-_]*$": {
              "oneOf": [
                {"$ref": "#/definitions/directory_node"},
                {"$ref": "#/definitions/file_list"}
              ]
            }
          }
        },
        {"$ref": "#/definitions/file_list"}
      ]
    },
    "file_list": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[a-zA-Z0-9][a-zA-Z0-9.-_]*\\.[a-zA-Z0-9]+$"
      }
    }
  }
}
```

### 2. Parser Architecture

#### Core Parser Class Design

```python
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json
import jsonschema
from datetime import datetime

class StructureParser:
    """
    Centralized parser for structure.json files with validation,
    caching, and extensibility features.
    """
    
    def __init__(self, schema_path: Optional[Path] = None):
        self.schema_path = schema_path
        self._schema_cache: Optional[Dict] = None
        self._structure_cache: Dict[str, Dict] = {}
    
    def load_schema(self) -> Dict:
        """Load and cache JSON schema for validation."""
        pass
    
    def validate_structure(self, structure_data: Dict) -> List[str]:
        """Validate structure against schema, return error list."""
        pass
    
    def parse_structure_file(self, file_path: Path) -> 'StructureData':
        """Parse structure.json file with validation and caching."""
        pass
    
    def get_directory_structure(self, structure_data: Dict) -> Dict:
        """Extract flat directory structure for file system operations."""
        pass
    
    def get_file_mappings(self, structure_data: Dict) -> Dict[str, List[str]]:
        """Get directory -> file list mappings."""
        pass

class StructureData:
    """
    Immutable data class representing a parsed and validated structure.json
    """
    
    def __init__(self, raw_data: Dict):
        self._data = raw_data
        self._validate()
    
    @property
    def metadata(self) -> Dict:
        """Get metadata section."""
        return self._data.get('metadata', {})
    
    @property
    def structure(self) -> Dict:
        """Get structure section."""
        return self._data.get('structure', {})
    
    def get_directories(self) -> List[str]:
        """Get all directory paths as flat list."""
        pass
    
    def get_files_for_directory(self, directory: str) -> List[str]:
        """Get files that should exist in specified directory."""
        pass
    
    def to_filesystem_operations(self) -> List['FilesystemOperation']:
        """Convert to filesystem operations for automation scripts."""
        pass

class FilesystemOperation:
    """Represents a single filesystem operation."""
    pass
```

### 3. Integration Points

#### Automation Script Integration

```python
# Example usage in initialize_repo.py
from structure_parser import StructureParser, StructureData

def main():
    parser = StructureParser(schema_path=Path("governance/structure/meta-repo-schema.json"))
    structure = parser.parse_structure_file(Path("governance/structure/structure.json"))
    
    # Create directories and files
    operations = structure.to_filesystem_operations()
    for op in operations:
        op.execute()
```

#### Seeding Script Integration

```python
# Updated seeding.py approach
class MetaRepoSeeder:
    def create_structure_json(self, structure_path: Path):
        """Create structure.json using template system."""
        template = self.load_structure_template()
        structure_data = self.customize_structure(template)
        
        parser = StructureParser()
        errors = parser.validate_structure(structure_data)
        if errors:
            raise ValidationError(f"Structure validation failed: {errors}")
        
        # Save validated structure
        self.save_structure_file(structure_path / 'structure.json', structure_data)
```

## 🔧 Implementation Plan

### Phase 1: Core Parser Implementation
- [ ] Create `StructureParser` and `StructureData` classes
- [ ] Implement JSON schema validation
- [ ] Add comprehensive error handling
- [ ] Create unit tests for parser functionality

### Phase 2: Schema Enhancement
- [ ] Update meta-repo-schema.json to v2.0 format
- [ ] Add extensible directory/file pattern matching
- [ ] Implement backwards compatibility layer
- [ ] Add schema migration utilities

### Phase 3: Automation Script Integration
- [ ] Refactor `initialize_repo.py` to use parser
- [ ] Update `enforce_structure.py` with validation
- [ ] Enhance `generate_readmes.py` with structure awareness
- [ ] Add filesystem operation abstraction

### Phase 4: Seeding Script Enhancement
- [ ] Replace hard-coded structure with template system
- [ ] Add structure customization options
- [ ] Implement validation during creation
- [ ] Add structure versioning support

## 🔒 Backwards Compatibility Strategy

### Version Migration
1. **Detect Schema Version**: Check for `schema_version` field
2. **Auto-upgrade**: Convert v1.0 format to v2.0 seamlessly  
3. **Validation Warnings**: Alert users to deprecated patterns
4. **Graceful Degradation**: Support old format with warnings

### API Compatibility
- Maintain existing method signatures where possible
- Add new methods with clear naming conventions
- Use deprecation warnings for old approaches
- Provide migration guides in documentation

## 🚀 Benefits

### For Developers
- **Consistent Parsing**: Single source of truth for structure.json handling
- **Validation**: Catch errors early with comprehensive schema validation
- **Extensibility**: Easy to add new directory structures and file patterns
- **Testing**: Mockable parser interface for unit testing

### for Scripts
- **Reliability**: Robust error handling and validation
- **Performance**: Caching reduces repeated file parsing
- **Flexibility**: Support for different project structure variations
- **Maintainability**: Centralized logic reduces code duplication

### For Operations
- **Validation**: Structure files are validated before use
- **Debugging**: Clear error messages for malformed structures
- **Monitoring**: Ability to audit structure compliance across repositories
- **Evolution**: Schema can evolve without breaking existing implementations

## ✅ Success Criteria

1. **Schema Compliance**: All structure.json files validate against enhanced schema
2. **Parser Integration**: All automation scripts use centralized parser
3. **Test Coverage**: >95% coverage for parser and validation logic
4. **Performance**: Structure parsing <100ms for typical files
5. **Documentation**: Complete API documentation with examples
6. **Backwards Compatibility**: Existing structure.json files work without modification

## 🔗 Related Issues

- **Issue #22**: Complete Automation Script Implementation (Parent Epic)
- **Future Issues**: Individual automation script implementation tasks
- **Future Issues**: Structure template system implementation
- **Future Issues**: Schema migration utilities

---

**Next Steps**: This analysis will be used to create specific implementation issues for each phase of the architecture development.