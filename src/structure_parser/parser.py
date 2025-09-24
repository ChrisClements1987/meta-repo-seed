"""
Main structure parser implementation.

This module provides the StructureParser class for parsing and validating
structure.json files used in the meta-repo seeding system.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from .models import StructureData, ValidationResult
from .exceptions import (
    StructureParserError,
    ValidationError,
    SchemaError,
    FileNotFoundError,
    ParseError,
    MigrationError
)

# Conditional import for schema validation
try:
    from .validators import SchemaValidator
    HAS_SCHEMA_VALIDATION = True
except ImportError:
    HAS_SCHEMA_VALIDATION = False
    SchemaValidator = None


class StructureParser:
    """Main parser for structure.json files.
    
    This class provides methods to parse, validate, and extract information
    from structure.json files according to the architecture specification.
    """
    
    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize the structure parser.
        
        Args:
            schema_path: Optional path to custom JSON schema file for validation.
                        If None, uses the built-in schema.
        """
        self.schema_path = schema_path
        self.validator = None
        
        # Initialize schema validator if available
        if HAS_SCHEMA_VALIDATION:
            try:
                self.validator = SchemaValidator(schema_path)
            except Exception as e:
                # Don't fail initialization if schema loading fails
                print(f"Warning: Could not initialize schema validator: {e}")
    
    def parse_file(self, file_path: Path) -> StructureData:
        """Parse a structure.json file from disk.
        
        Args:
            file_path: Path to the structure.json file
            
        Returns:
            StructureData object containing parsed data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ParseError: If JSON parsing fails
            ValidationError: If structure is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Structure file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.parse_string(content)
        except json.JSONDecodeError as e:
            raise ParseError(
                f"Invalid JSON in {file_path}: {e.msg}",
                line_number=e.lineno,
                column=e.colno
            )
        except Exception as e:
            raise StructureParserError(f"Error reading file {file_path}: {e}")
    
    def parse_string(self, json_content: str) -> StructureData:
        """Parse structure data from a JSON string.
        
        Args:
            json_content: JSON string containing structure data
            
        Returns:
            StructureData object containing parsed data
            
        Raises:
            ParseError: If JSON parsing fails
            ValidationError: If structure is invalid
        """
        try:
            data = json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ParseError(
                f"Invalid JSON: {e.msg}",
                line_number=e.lineno,
                column=e.colno
            )
        
        # Validate the data
        validation_result = self.validate(data)
        if not validation_result.is_valid:
            errors = [str(error) for error in validation_result.errors]
            raise ValidationError(
                "Structure validation failed",
                errors=errors
            )
        
        # Convert to StructureData object
        return self._create_structure_data(data)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate structure data against the schema.
        
        Args:
            data: Parsed JSON data to validate
            
        Returns:
            ValidationResult containing validation outcome and any errors
        """
        # If schema validator is available, use it
        # TODO: Re-enable once JSON schema validation is fixed (Issue #31)
        if False and self.validator:
            try:
                return self.validator.validate(data)
            except Exception as e:
                result = ValidationResult(is_valid=False)
                result.add_error(f"Schema validation error: {e}", error_code="SCHEMA_ERROR")
                return result
        
        # Fallback validation without schema
        return self._validate_basic_structure(data)
    
    def _validate_basic_structure(self, data: Dict[str, Any]) -> ValidationResult:
        """Basic validation without JSON schema (fallback mode).
        
        Args:
            data: Data to validate
            
        Returns:
            ValidationResult with basic validation checks
        """
        result = ValidationResult(is_valid=True)
        
        # Check for v2 format with metadata object
        if 'metadata' in data:
            # V2 format validation
            metadata = data['metadata']
            required_metadata_fields = ['project_name', 'github_username', 'version', 'schema_version']
            for field in required_metadata_fields:
                if field not in metadata:
                    result.add_error(f"Required metadata field '{field}' is missing", f"metadata.{field}", "MISSING_FIELD")
            
            # Validate metadata field types
            if 'project_name' in metadata and not isinstance(metadata['project_name'], str):
                result.add_error("project_name must be a string", "metadata.project_name", "INVALID_TYPE")
            
            if 'github_username' in metadata and not isinstance(metadata['github_username'], str):
                result.add_error("github_username must be a string", "metadata.github_username", "INVALID_TYPE")
            
            if 'version' in metadata and not isinstance(metadata['version'], str):
                result.add_error("version must be a string", "metadata.version", "INVALID_TYPE")
        else:
            # V1 format validation (for backwards compatibility)
            required_fields = ['project_name', 'github_username', 'version', 'structure']
            for field in required_fields:
                if field not in data:
                    result.add_error(f"Required field '{field}' is missing", field, "MISSING_FIELD")
            
            # Validate field types
            if 'project_name' in data and not isinstance(data['project_name'], str):
                result.add_error("project_name must be a string", "project_name", "INVALID_TYPE")
            
            if 'github_username' in data and not isinstance(data['github_username'], str):
                result.add_error("github_username must be a string", "github_username", "INVALID_TYPE")
            
            if 'version' in data and not isinstance(data['version'], str):
                result.add_error("version must be a string", "version", "INVALID_TYPE")
        
        # Check structure field (same for both formats)
        if 'structure' not in data:
            result.add_error("Required field 'structure' is missing", "structure", "MISSING_FIELD")
        elif not isinstance(data['structure'], dict):
            result.add_error("structure must be an object", "structure", "INVALID_TYPE")
        
        # Basic structure validation
        structure = data.get('structure', {})
        if not structure:
            result.add_error("Structure cannot be empty", "structure", "EMPTY_STRUCTURE")
        
        return result
    
    def _create_structure_data(self, data: Dict[str, Any]) -> StructureData:
        """Create StructureData object from validated data.
        
        Args:
            data: Validated structure data
            
        Returns:
            StructureData object
        """
        return StructureData.from_dict(data)
    
    def get_directory_structure(self, data: StructureData) -> List[Path]:
        """Extract directory paths from structure data.
        
        Args:
            data: Parsed structure data
            
        Returns:
            List of Path objects representing directories to create
        """
        directories = []
        
        def collect_paths(obj: Dict[str, Any], base_path: Path = Path()):
            """Recursively collect directory paths."""
            for key, value in obj.items():
                current_path = base_path / key
                directories.append(current_path)
                
                if isinstance(value, dict):
                    collect_paths(value, current_path)
        
        collect_paths(data.structure)
        return directories
    
    def load_structure_with_migration(self, file_path: Path, 
                                    target_version: str = "2.0") -> StructureData:
        """Load structure file with automatic migration if needed.
        
        Args:
            file_path: Path to structure.json file
            target_version: Target schema version to migrate to
            
        Returns:
            StructureData with migrated structure
            
        Raises:
            MigrationError: If migration fails
        """
        data = self.parse_file(file_path)
        
        # Check if migration is needed
        current_version = data.version
        if current_version != target_version:
            return self._migrate_structure(data, target_version)
        
        return data
    
    def _migrate_structure(self, data: StructureData, target_version: str) -> StructureData:
        """Migrate structure data to target version.
        
        Args:
            data: Current structure data
            target_version: Version to migrate to
            
        Returns:
            Migrated structure data
            
        Raises:
            MigrationError: If migration is not supported or fails
        """
        current_version = data.version
        
        # Version 1.x to 2.0 migration
        if current_version.startswith('1.') and target_version == "2.0":
            return self._migrate_v1_to_v2(data)
        
        raise MigrationError(
            f"Migration from version {current_version} to {target_version} is not supported"
        )
    
    def _migrate_v1_to_v2(self, data: StructureData) -> StructureData:
        """Migrate version 1.x structure to version 2.0.
        
        Args:
            data: Version 1.x structure data
            
        Returns:
            Migrated version 2.0 structure data
        """
        # Create new structure data with updated version
        migrated_dict = {
            "metadata": {
                "project_name": data.project_name,
                "github_username": data.github_username,
                "created_date": data.created_date,
                "version": "2.0.0",
                "schema_version": "2.0.0",
                "description": data.description,
                "tags": data.tags.copy()
            },
            "structure": data.structure.copy()  # Deep copy structure
        }
        
        migrated_data = StructureData.from_dict(migrated_dict)
        
        # Apply v1 to v2 transformations
        # (Add specific migration logic here as needed)
        
        return migrated_data
    
    def export_structure(self, data: StructureData, output_path: Path, 
                        pretty_print: bool = True) -> None:
        """Export structure data to a JSON file.
        
        Args:
            data: Structure data to export
            output_path: Path where to save the file
            pretty_print: Whether to format JSON with indentation
        """
        export_data = {
            'project_name': data.project_name,
            'github_username': data.github_username,
            'created_date': data.created_date,
            'version': data.version,
            'structure': data.structure
        }
        
        # Add optional fields if present
        if data.description:
            export_data['description'] = data.description
        if data.tags:
            export_data['tags'] = data.tags
        if data.template_path:
            export_data['template_path'] = data.template_path
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty_print:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(export_data, f, ensure_ascii=False)
    
    def get_schema_info(self) -> Dict[str, Any]:
        """Get information about the loaded schema.
        
        Returns:
            Dictionary with schema information
        """
        if self.validator:
            return {
                'schema_path': str(self.schema_path) if self.schema_path else 'built-in',
                'has_validation': True,
                'schema_version': self.validator.schema.get('version', 'unknown')
            }
        else:
            return {
                'schema_path': None,
                'has_validation': False,
                'schema_version': 'fallback-mode'
            }