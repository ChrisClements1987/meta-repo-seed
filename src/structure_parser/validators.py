"""
Schema validation functionality for structure.json files.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import jsonschema
from jsonschema import ValidationError as JsonSchemaValidationError

from .exceptions import SchemaError
from .models import ValidationError, ValidationResult


class SchemaValidator:
    """Validates structure.json files against JSON schema."""
    
    def __init__(self, schema_path: Optional[Path] = None):
        """Initialize validator with schema.
        
        Args:
            schema_path: Path to JSON schema file. If None, uses built-in schema.
        """
        self.schema_path = schema_path or self._get_default_schema_path()
        self.schema = self._load_schema()
        self.validator = jsonschema.Draft7Validator(self.schema)
    
    def _get_default_schema_path(self) -> Path:
        """Get path to default schema file."""
        # Look for schema relative to this package
        current_dir = Path(__file__).parent.parent.parent
        schema_path = current_dir / "schemas" / "structure-v2.json"
        
        if not schema_path.exists():
            raise SchemaError(f"Default schema not found at {schema_path}")
        
        return schema_path
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load JSON schema from file."""
        if not self.schema_path.exists():
            raise SchemaError(f"Schema file not found: {self.schema_path}")
        
        try:
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema = json.load(f)
            return schema
        except json.JSONDecodeError as e:
            raise SchemaError(f"Invalid JSON in schema file: {e}")
        except Exception as e:
            raise SchemaError(f"Error loading schema: {e}")
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Validate structure data against schema.
        
        Args:
            data: Parsed structure.json data
            
        Returns:
            ValidationResult with validation outcome
        """
        result = ValidationResult(is_valid=True)
        
        # Get schema version from data or schema
        schema_version = data.get('version', self.schema.get('version', 'unknown'))
        result.schema_version = schema_version
        
        try:
            # Validate against schema
            errors = sorted(self.validator.iter_errors(data), key=lambda e: e.path)
            
            for error in errors:
                path = ".".join(str(p) for p in error.path) if error.path else "root"
                result.add_error(
                    message=error.message,
                    path=path,
                    error_code="SCHEMA_VALIDATION_ERROR"
                )
            
            # Custom validation rules
            self._validate_custom_rules(data, result)
            
        except Exception as e:
            result.add_error(
                message=f"Schema validation failed: {e}",
                error_code="SCHEMA_ERROR"
            )
        
        return result
    
    def _validate_custom_rules(self, data: Dict[str, Any], result: ValidationResult):
        """Apply custom validation rules beyond basic schema validation."""
        
        # Get metadata from v2 format or fall back to root level for v1
        metadata = data.get('metadata', data)
        
        # Validate project name format
        project_name = metadata.get('project_name', '')
        if not project_name:
            path = "metadata.project_name" if 'metadata' in data else "project_name"
            result.add_error("Project name is required", path, "MISSING_FIELD")
        elif not self._is_valid_project_name(project_name):
            path = "metadata.project_name" if 'metadata' in data else "project_name"
            result.add_error(
                "Project name should be lowercase with hyphens (kebab-case)",
                path,
                "INVALID_FORMAT"
            )
        
        # Validate GitHub username
        github_username = metadata.get('github_username', '')
        if not github_username:
            path = "metadata.github_username" if 'metadata' in data else "github_username"
            result.add_error("GitHub username is required", path, "MISSING_FIELD")
        elif not self._is_valid_github_username(github_username):
            path = "metadata.github_username" if 'metadata' in data else "github_username"
            result.add_warning(
                "GitHub username format may be invalid",
                path,
                "SUSPICIOUS_FORMAT"
            )
        
        # Validate structure completeness
        structure = data.get('structure', {})
        if not structure:
            result.add_error("Structure definition is required", "structure", "MISSING_FIELD")
        else:
            self._validate_structure_completeness(structure, result)
        
        # Validate version format
        version = metadata.get('version', '')
        if version and not self._is_valid_version(version):
            path = "metadata.version" if 'metadata' in data else "version"
            result.add_warning(
                "Version should follow semantic versioning (e.g., 1.0.0)",
                path,
                "INVALID_VERSION_FORMAT"
            )
    
    def _is_valid_project_name(self, name: str) -> bool:
        """Check if project name follows kebab-case convention."""
        import re
        return bool(re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name))
    
    def _is_valid_github_username(self, username: str) -> bool:
        """Check if GitHub username format is valid."""
        import re

        # GitHub username rules: may contain alphanumeric chars and hyphens
        # Cannot start/end with hyphen, cannot contain consecutive hyphens
        return bool(re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', username))
    
    def _is_valid_version(self, version: str) -> bool:
        """Check if version follows semantic versioning."""
        import re
        semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
        return bool(re.match(semver_pattern, version))
    
    def _validate_structure_completeness(self, structure: Dict[str, Any], result: ValidationResult):
        """Validate that structure contains expected sections."""
        
        # Check for required top-level sections
        required_sections = ['meta-repo']  # At minimum, meta-repo is required
        
        for section in required_sections:
            if section not in structure:
                result.add_error(
                    f"Required section '{section}' is missing from structure",
                    f"structure.{section}",
                    "MISSING_REQUIRED_SECTION"
                )
        
        # Validate meta-repo structure
        if 'meta-repo' in structure:
            meta_repo = structure['meta-repo']
            if not isinstance(meta_repo, dict):
                result.add_error(
                    "meta-repo section must be an object",
                    "structure.meta-repo",
                    "INVALID_TYPE"
                )
            else:
                self._validate_meta_repo_structure(meta_repo, result)
    
    def _validate_meta_repo_structure(self, meta_repo: Dict[str, Any], result: ValidationResult):
        """Validate meta-repo section structure."""
        
        # Check for recommended subsections
        recommended_sections = ['governance', 'automation', 'documentation']
        
        for section in recommended_sections:
            if section not in meta_repo:
                result.add_warning(
                    f"Recommended section '{section}' is missing from meta-repo",
                    f"structure.meta-repo.{section}",
                    "MISSING_RECOMMENDED_SECTION"
                )
        
        # Validate governance structure if present
        if 'governance' in meta_repo:
            governance = meta_repo['governance']
            if isinstance(governance, dict):
                governance_sections = ['structure', 'policies', 'processes']
                for section in governance_sections:
                    if section not in governance:
                        result.add_warning(
                            f"Recommended governance section '{section}' is missing",
                            f"structure.meta-repo.governance.{section}",
                            "MISSING_RECOMMENDED_SECTION"
                        )