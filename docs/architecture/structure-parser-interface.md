# Structure Parser Interface Specification

**Related**: Issue #23 - Design Architecture for structure.json Processing  
**Version**: 1.0  
**Date**: 2025-09-24  

## 🎯 Overview

This document defines the detailed interface specifications for the `StructureParser` system that will be shared across all automation scripts in the meta-repo seeding system.

## 🏗️ Core Classes

### StructureParser

The main parser class that handles loading, validating, and parsing structure.json files.

```python
class StructureParser:
    """
    Centralized parser for structure.json files with validation and caching.
    
    Example Usage:
        parser = StructureParser()
        structure = parser.parse_structure_file(Path("structure.json"))
        directories = structure.get_directories()
    """
    
    def __init__(self, 
                 schema_path: Optional[Path] = None,
                 cache_enabled: bool = True,
                 strict_validation: bool = True):
        """
        Initialize the structure parser.
        
        Args:
            schema_path: Path to JSON schema file. If None, uses default.
            cache_enabled: Whether to cache parsed structures
            strict_validation: If True, raise on validation errors
        """
    
    def load_schema(self, schema_path: Optional[Path] = None) -> Dict[str, Any]:
        """
        Load JSON schema for validation.
        
        Returns:
            Parsed JSON schema dictionary
            
        Raises:
            FileNotFoundError: Schema file not found
            json.JSONDecodeError: Invalid JSON in schema
        """
    
    def validate_structure(self, structure_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate structure data against schema.
        
        Args:
            structure_data: Parsed structure.json data
            
        Returns:
            ValidationResult with success status and error details
        """
    
    def parse_structure_file(self, file_path: Path) -> StructureData:
        """
        Parse and validate a structure.json file.
        
        Args:
            file_path: Path to structure.json file
            
        Returns:
            StructureData object with parsed content
            
        Raises:
            FileNotFoundError: Structure file not found
            ValidationError: Structure validation failed (if strict_validation=True)
            json.JSONDecodeError: Invalid JSON format
        """
    
    def parse_structure_dict(self, structure_dict: Dict[str, Any]) -> StructureData:
        """
        Parse and validate structure data from dictionary.
        
        Args:
            structure_dict: Structure data as dictionary
            
        Returns:
            StructureData object with parsed content
        """
    
    def clear_cache(self) -> None:
        """Clear internal structure cache."""
```

### StructureData

Immutable data class representing parsed and validated structure.json content.

```python
class StructureData:
    """
    Immutable representation of a validated structure.json file.
    
    Provides convenient methods to access structure information
    for automation scripts.
    """
    
    def __init__(self, validated_data: Dict[str, Any]):
        """Initialize with pre-validated structure data."""
    
    @property
    def project_name(self) -> str:
        """Get project name from metadata."""
    
    @property
    def github_username(self) -> str:
        """Get GitHub username from metadata."""
    
    @property
    def version(self) -> str:
        """Get structure version from metadata."""
    
    @property
    def created_date(self) -> datetime:
        """Get creation date as datetime object."""
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """Get complete metadata section."""
    
    @property
    def structure(self) -> Dict[str, Any]:
        """Get complete structure section."""
    
    def get_directories(self) -> List[str]:
        """
        Get all directory paths as a flat list.
        
        Returns:
            List of directory paths like ['meta-repo/governance', 'cloud-storage/strategy']
        """
    
    def get_files_for_directory(self, directory_path: str) -> List[str]:
        """
        Get list of files that should exist in the specified directory.
        
        Args:
            directory_path: Directory path (e.g., 'meta-repo/governance/policies')
            
        Returns:
            List of filenames that should exist in that directory
        """
    
    def directory_exists(self, directory_path: str) -> bool:
        """Check if a directory is defined in the structure."""
    
    def get_directory_tree(self) -> Dict[str, Any]:
        """
        Get directory structure as nested dictionary.
        
        Returns:
            Nested dictionary representing directory tree
        """
    
    def to_filesystem_operations(self) -> List[FilesystemOperation]:
        """
        Convert structure to list of filesystem operations.
        
        Returns:
            List of operations needed to create the structure
        """
    
    def validate_against_filesystem(self, base_path: Path) -> ComplianceReport:
        """
        Check if actual filesystem matches structure definition.
        
        Args:
            base_path: Root path to check against
            
        Returns:
            ComplianceReport with missing/extra files and directories
        """
```

### Supporting Classes

```python
class ValidationResult:
    """Result of structure validation."""
    
    def __init__(self, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []
    
    def __bool__(self) -> bool:
        """Allow using ValidationResult in boolean context."""
        return self.is_valid

class FilesystemOperation:
    """Represents a single filesystem operation."""
    
    def __init__(self, operation_type: str, path: Path, content: Optional[str] = None):
        self.operation_type = operation_type  # 'create_directory', 'create_file'
        self.path = path
        self.content = content
    
    def execute(self, base_path: Path, dry_run: bool = False) -> bool:
        """Execute the filesystem operation."""

class ComplianceReport:
    """Report of structure compliance check."""
    
    def __init__(self):
        self.missing_directories: List[str] = []
        self.missing_files: List[str] = []
        self.extra_directories: List[str] = []
        self.extra_files: List[str] = []
        self.compliant: bool = True
    
    def add_missing_directory(self, path: str) -> None:
        """Add missing directory to report."""
    
    def add_missing_file(self, directory: str, filename: str) -> None:
        """Add missing file to report."""
    
    def is_compliant(self) -> bool:
        """Check if structure is fully compliant."""
        return len(self.missing_directories) == 0 and len(self.missing_files) == 0

class ValidationError(Exception):
    """Raised when structure validation fails."""
    
    def __init__(self, message: str, errors: List[str] = None):
        super().__init__(message)
        self.errors = errors or []
```

## 🔧 Usage Examples

### Basic Structure Parsing

```python
from structure_parser import StructureParser

# Basic usage
parser = StructureParser()
structure = parser.parse_structure_file(Path("governance/structure/structure.json"))

print(f"Project: {structure.project_name}")
print(f"Directories: {len(structure.get_directories())}")

# Get files for specific directory
governance_files = structure.get_files_for_directory("meta-repo/governance/policies")
print(f"Policy files: {governance_files}")
```

### Validation and Error Handling

```python
try:
    parser = StructureParser(strict_validation=True)
    structure = parser.parse_structure_file(Path("structure.json"))
except ValidationError as e:
    print(f"Validation failed: {e}")
    for error in e.errors:
        print(f"  - {error}")
except FileNotFoundError:
    print("Structure file not found")
```

### Structure Compliance Checking

```python
# Check if actual filesystem matches structure
parser = StructureParser()
structure = parser.parse_structure_file(Path("structure.json"))

report = structure.validate_against_filesystem(Path("."))
if not report.is_compliant():
    print("Structure compliance issues:")
    for missing_dir in report.missing_directories:
        print(f"  Missing directory: {missing_dir}")
    for missing_file in report.missing_files:
        print(f"  Missing file: {missing_file}")
```

### Creating Filesystem Structure

```python
# Generate filesystem operations and execute them
parser = StructureParser()
structure = parser.parse_structure_file(Path("structure.json"))

operations = structure.to_filesystem_operations()
for op in operations:
    print(f"Executing: {op.operation_type} {op.path}")
    op.execute(base_path=Path("."))
```

## 🔌 Integration Points

### For initialize_repo.py

```python
#!/usr/bin/env python3
"""Initialize repository structure based on structure.json."""

from pathlib import Path
from structure_parser import StructureParser

def main():
    parser = StructureParser()
    structure = parser.parse_structure_file(Path("governance/structure/structure.json"))
    
    # Create all directories and files
    operations = structure.to_filesystem_operations()
    for op in operations:
        if op.operation_type == 'create_directory':
            op.path.mkdir(parents=True, exist_ok=True)
        elif op.operation_type == 'create_file' and not op.path.exists():
            op.path.touch()
    
    print(f"Repository structure initialized for {structure.project_name}")
```

### For enforce_structure.py

```python
#!/usr/bin/env python3
"""Enforce repository structure compliance."""

from pathlib import Path
from structure_parser import StructureParser

def main():
    parser = StructureParser()
    structure = parser.parse_structure_file(Path("governance/structure/structure.json"))
    
    # Check compliance
    report = structure.validate_against_filesystem(Path("."))
    
    if report.is_compliant():
        print("✅ Repository structure is compliant")
    else:
        print("❌ Repository structure compliance issues found:")
        # Fix missing directories and files
        operations = structure.to_filesystem_operations()
        for op in operations:
            op.execute(base_path=Path("."))
        print("Structure compliance enforced")
```

### For generate_readmes.py

```python
#!/usr/bin/env python3
"""Generate README files based on structure."""

from pathlib import Path
from structure_parser import StructureParser

def main():
    parser = StructureParser()
    structure = parser.parse_structure_file(Path("governance/structure/structure.json"))
    
    # Generate README for each directory
    for directory_path in structure.get_directories():
        readme_path = Path(directory_path) / "README.md"
        if not readme_path.exists():
            files_in_dir = structure.get_files_for_directory(directory_path)
            generate_readme(readme_path, directory_path, files_in_dir)
    
    print(f"README files generated for {structure.project_name}")
```

## 🎯 Design Principles

1. **Single Responsibility**: Each class has a clear, focused purpose
2. **Immutability**: StructureData is immutable once created
3. **Fail Fast**: Validation errors are caught early and reported clearly
4. **Extensibility**: Easy to add new validation rules and operations
5. **Testability**: All methods are pure functions where possible
6. **Performance**: Caching prevents repeated parsing of same files

## ✅ Implementation Checklist

- [ ] Create core `StructureParser` class
- [ ] Implement `StructureData` immutable data class
- [ ] Add comprehensive JSON schema validation
- [ ] Create filesystem operation abstraction
- [ ] Implement compliance checking functionality
- [ ] Add caching mechanism for performance
- [ ] Create comprehensive error handling
- [ ] Write unit tests for all methods
- [ ] Add integration tests with actual structure.json files
- [ ] Create API documentation with examples

---

**Next**: This specification will guide the implementation of the structure parser system in subsequent development issues.