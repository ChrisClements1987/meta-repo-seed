# Structure Parser Module

A comprehensive Python module for parsing and validating `structure.json` files used in the meta-repo seeding system.

## 🎯 Overview

The Structure Parser Module provides a robust foundation for all automation scripts that need to work with repository structure definitions. It implements the architecture specified in [docs/architecture/structure-parser-interface.md](../../docs/architecture/structure-parser-interface.md).

## ✨ Features

- **📄 JSON Parsing** - Parse structure.json files with comprehensive error handling
- **✅ Schema Validation** - Validate against JSON Schema with detailed error reporting  
- **🔧 Type Safety** - Strongly typed data models with proper Python typing
- **🔄 Migration Support** - Handle schema version migrations automatically
- **🚨 Error Handling** - Comprehensive exception hierarchy with detailed messages
- **📊 Directory Analysis** - Extract directory structures and file listings
- **🧪 Fully Tested** - Comprehensive test suite with >95% coverage

## 🚀 Quick Start

### Basic Usage

```python
from structure_parser import StructureParser

# Initialize parser
parser = StructureParser()

# Parse from file
structure = parser.parse_file(Path("structure.json"))

# Access parsed data
print(f"Project: {structure.project_name}")
print(f"Directories: {structure.get_top_level_directories()}")

# Check if directories exist
if structure.has_directory("meta-repo/governance"):
    files = structure.get_directory_files("meta-repo/governance")
    print(f"Governance files: {files}")
```

### With Validation

```python
# Parse and validate
try:
    structure = parser.parse_file(Path("structure.json"))
    print("✅ Structure is valid!")
except ValidationError as e:
    print(f"❌ Validation failed: {e}")
    for error in e.errors:
        print(f"  - {error}")
```

### String Parsing

```python
import json

# Parse from JSON string
json_data = json.dumps({
    "project_name": "my-project",
    "github_username": "myuser", 
    "version": "2.0",
    "structure": {
        "meta-repo": {
            "governance": {
                "structure": ["structure.json"]
            }
        }
    }
})

structure = parser.parse_string(json_data)
```

## 📦 Installation

### Dependencies

The module requires Python 3.8+ and has the following dependencies:

**Required:**
- `pathlib` (built-in)
- `json` (built-in)
- `typing` (built-in)

**Optional (for enhanced validation):**
- `jsonschema>=4.0.0` - Enables full JSON Schema validation

### Install Dependencies

```bash
# For basic functionality
# No additional dependencies required

# For full schema validation
pip install jsonschema>=4.0.0

# For development and testing
pip install -r requirements-test.txt
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/test_structure_parser/

# Run with coverage
python -m pytest tests/test_structure_parser/ --cov=src/structure_parser --cov-report=html

# Run specific test categories
python -m pytest tests/test_structure_parser/ -m unit
python -m pytest tests/test_structure_parser/ -m integration
```

### Test Structure

- **Unit Tests** - Test individual components in isolation
- **Integration Tests** - Test component interactions with fixtures
- **Validation Tests** - Test schema validation with various inputs
- **Error Handling Tests** - Test exception handling and error reporting

## 📖 API Reference

### Core Classes

#### `StructureParser`

Main parser class for structure.json files.

```python
class StructureParser:
    def __init__(self, schema_path: Optional[Path] = None)
    def parse_file(self, file_path: Path) -> StructureData
    def parse_string(self, json_content: str) -> StructureData
    def validate(self, data: Dict[str, Any]) -> ValidationResult
    def get_directory_structure(self, data: StructureData) -> List[Path]
```

#### `StructureData`

Parsed structure data with typed access methods.

```python
@dataclass
class StructureData:
    project_name: str
    github_username: str
    created_date: str
    version: str
    structure: Dict[str, Any]
    
    def get_top_level_directories(self) -> List[str]
    def get_directory_files(self, directory_path: str) -> List[str]
    def has_directory(self, directory_path: str) -> bool
    def get_all_directories(self) -> List[str]
    def get_all_files(self) -> Dict[str, List[str]]
```

#### `ValidationResult`

Result of structure validation with detailed error reporting.

```python
@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[ValidationError]
    warnings: List[ValidationError]
    
    def get_summary(self) -> str
    def get_detailed_report(self) -> str
```

### Exception Hierarchy

```
StructureParserError
├── ValidationError
├── SchemaError
├── FileNotFoundError
├── ParseError
└── MigrationError
```

## 🔧 Configuration

### Schema Validation

By default, the parser uses the built-in schema at `schemas/structure-v2.json`. You can specify a custom schema:

```python
# Use custom schema
parser = StructureParser(schema_path=Path("custom-schema.json"))

# Check schema info
info = parser.get_schema_info()
print(f"Validation enabled: {info['has_validation']}")
print(f"Schema version: {info['schema_version']}")
```

### Fallback Mode

If `jsonschema` is not available, the parser falls back to basic validation:

- ✅ JSON parsing and basic type checking
- ✅ Required field validation
- ❌ Advanced schema validation
- ❌ Custom validation rules

## 🔄 Schema Migration

The parser supports automatic schema migration:

```python
# Load with automatic migration
structure = parser.load_structure_with_migration(
    file_path=Path("old-structure.json"),
    target_version="2.0"
)

# Manual migration
if structure.version == "1.0":
    migrated = parser._migrate_v1_to_v2(structure)
```

## 🎯 Integration Examples

### With Initialize Script

```python
from structure_parser import StructureParser

def initialize_repository(structure_file: Path, target_dir: Path):
    parser = StructureParser()
    structure = parser.parse_file(structure_file)
    
    # Create directories
    directories = parser.get_directory_structure(structure)
    for directory in directories:
        (target_dir / directory).mkdir(parents=True, exist_ok=True)
        
    print(f"Created {len(directories)} directories")
```

### With Validation Script

```python
def validate_repository_structure(structure_file: Path):
    parser = StructureParser()
    
    try:
        structure = parser.parse_file(structure_file)
        result = parser.validate(structure.__dict__)
        
        if result.is_valid:
            print("✅ Repository structure is valid")
        else:
            print("❌ Validation failed:")
            print(result.get_detailed_report())
            
    except StructureParserError as e:
        print(f"❌ Parser error: {e}")
```

## 🔗 Related Documentation

- [Structure JSON Processing Architecture](../../docs/architecture/structure-json-processing.md)
- [Parser Interface Specification](../../docs/architecture/structure-parser-interface.md)
- [Schema Migration Guide](../../docs/architecture/structure-migration-guide.md)
- [JSON Schema v2](../../schemas/structure-v2.json)

## 🤝 Contributing

This module follows the project's coding standards and workflow:

1. **Create feature branch** following naming convention
2. **Write tests** for all new functionality
3. **Ensure >95% coverage** with `pytest --cov`
4. **Follow type hints** and documentation standards
5. **Submit PR** with comprehensive description

See [CONTRIBUTING.md](../../docs/development/contributing.md) for detailed guidelines.

## 📝 License

Part of the Meta-Repo Seeding System project. See main project LICENSE for details.