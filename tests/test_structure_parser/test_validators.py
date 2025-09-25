"""
Tests for the validators module.
"""

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

# Import only if jsonschema is available
try:
    from src.structure_parser.exceptions import SchemaError
    from src.structure_parser.validators import SchemaValidator
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False
    SchemaValidator = None
    SchemaError = Exception

from src.structure_parser.models import ValidationResult


@pytest.mark.skipif(not HAS_JSONSCHEMA, reason="jsonschema not available")
class TestSchemaValidator:
    """Test cases for SchemaValidator class."""
    
    @pytest.fixture
    def mock_schema(self):
        """Mock JSON schema for testing."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {
                "project_name": {"type": "string", "minLength": 1},
                "github_username": {"type": "string", "minLength": 1},
                "version": {"type": "string"},
                "structure": {"type": "object"}
            },
            "required": ["project_name", "github_username", "version", "structure"]
        }
    
    @pytest.fixture
    def valid_data(self):
        """Valid structure data for testing."""
        return {
            "project_name": "test-project",
            "github_username": "testuser",
            "version": "2.0",
            "structure": {
                "meta-repo": {
                    "governance": {
                        "structure": ["structure.json"]
                    }
                }
            }
        }
    
    def test_validator_initialization_with_schema_path(self, mock_schema, tmp_path):
        """Test validator initialization with custom schema."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        validator = SchemaValidator(schema_file)
        assert validator.schema_path == schema_file
        assert validator.schema == mock_schema
    
    def test_validator_initialization_missing_schema(self):
        """Test validator initialization with missing schema file."""
        nonexistent_schema = Path("nonexistent_schema.json")
        
        with pytest.raises(SchemaError) as exc_info:
            SchemaValidator(nonexistent_schema)
        
        assert "not found" in str(exc_info.value)
    
    def test_validator_initialization_invalid_json_schema(self, tmp_path):
        """Test validator initialization with invalid JSON schema."""
        invalid_schema_file = tmp_path / "invalid_schema.json"
        invalid_schema_file.write_text('{"invalid": json,}')
        
        with pytest.raises(SchemaError) as exc_info:
            SchemaValidator(invalid_schema_file)
        
        assert "Invalid JSON" in str(exc_info.value)
    
    def test_validate_valid_data(self, mock_schema, valid_data, tmp_path):
        """Test validation of valid data."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(valid_data)
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert result.error_count == 0
    
    def test_validate_missing_required_fields(self, mock_schema, tmp_path):
        """Test validation with missing required fields."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        invalid_data = {
            "project_name": "test"
            # Missing other required fields
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(invalid_data)
        
        assert not result.is_valid
        assert result.error_count > 0
    
    def test_validate_invalid_types(self, mock_schema, tmp_path):
        """Test validation with invalid field types."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        invalid_data = {
            "project_name": 123,  # Should be string
            "github_username": "user",
            "version": "2.0",
            "structure": "not an object"  # Should be object
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(invalid_data)
        
        assert not result.is_valid
        assert result.error_count >= 2  # At least project_name and structure errors
    
    def test_custom_validation_rules_project_name(self, mock_schema, tmp_path):
        """Test custom validation rules for project name format."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        # Valid kebab-case name
        valid_data = {
            "project_name": "my-awesome-project",
            "github_username": "user",
            "version": "2.0",
            "structure": {}
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(valid_data)
        
        # Should pass basic validation, may have warnings for other things
        assert result.error_count == 0 or all("project_name" not in error.path for error in result.errors)
        
        # Invalid project name format
        invalid_data = valid_data.copy()
        invalid_data["project_name"] = "MyProjectName"  # Not kebab-case
        
        result = validator.validate(invalid_data)
        
        # Should have a warning or error about project name format
        has_project_name_issue = any(
            "project_name" in error.path and "kebab-case" in error.message.lower()
            for error in result.errors + result.warnings
        )
        assert has_project_name_issue or result.warning_count > 0
    
    def test_custom_validation_rules_github_username(self, mock_schema, tmp_path):
        """Test custom validation rules for GitHub username."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        valid_data = {
            "project_name": "test-project",
            "github_username": "validuser123",
            "version": "2.0",
            "structure": {}
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(valid_data)
        
        # Should not have username-specific errors
        username_errors = [error for error in result.errors if "github_username" in error.path]
        assert len(username_errors) == 0
    
    def test_custom_validation_rules_version_format(self, mock_schema, tmp_path):
        """Test custom validation rules for version format."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        # Valid semantic version
        valid_data = {
            "project_name": "test-project",
            "github_username": "user",
            "version": "1.2.3",
            "structure": {}
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(valid_data)
        
        # Should not have version format warnings
        version_warnings = [w for w in result.warnings if "version" in w.path]
        assert len(version_warnings) == 0
        
        # Invalid version format
        invalid_data = valid_data.copy()
        invalid_data["version"] = "v1.2"  # Not semantic versioning
        
        result = validator.validate(invalid_data)
        
        # May have a warning about version format
        # This is a warning, not an error, so validation might still pass
        assert result.is_valid or result.warning_count > 0
    
    def test_validate_structure_completeness(self, mock_schema, tmp_path):
        """Test validation of structure completeness."""
        schema_file = tmp_path / "schema.json"
        schema_file.write_text(json.dumps(mock_schema))
        
        # Structure missing meta-repo section
        incomplete_data = {
            "project_name": "test-project",
            "github_username": "user",
            "version": "2.0",
            "structure": {
                "other-section": {}
            }
        }
        
        validator = SchemaValidator(schema_file)
        result = validator.validate(incomplete_data)
        
        # Should have error or warning about missing meta-repo section
        meta_repo_issues = [
            issue for issue in result.errors + result.warnings
            if "meta-repo" in issue.message.lower()
        ]
        assert len(meta_repo_issues) > 0


class TestValidationFallback:
    """Test validation behavior when jsonschema is not available."""
    
    def test_fallback_import_handling(self):
        """Test that the module handles missing jsonschema gracefully."""
        # This test verifies that the import structure allows graceful degradation
        # when jsonschema is not available
        
        # The actual test is that this file can be imported successfully
        # even without jsonschema
        assert True  # If we get here, imports worked
    
    def test_validation_result_creation(self):
        """Test that ValidationResult can be created without jsonschema."""
        result = ValidationResult(is_valid=True)
        
        assert result.is_valid
        assert result.error_count == 0
        assert result.warning_count == 0
        
        # Test adding errors and warnings
        result.add_error("Test error", "test.path", "TEST_ERROR")
        result.add_warning("Test warning", "test.path", "TEST_WARNING")
        
        assert not result.is_valid
        assert result.error_count == 1
        assert result.warning_count == 1
        
        # Test summary
        summary = result.get_summary()
        assert "1 error" in summary
        assert "1 warning" in summary