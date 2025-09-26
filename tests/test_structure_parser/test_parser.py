"""
Tests for the StructureParser class.
"""

import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.structure_parser import (MigrationError, ParseError, StructureData,
                                  StructureFileNotFoundError, StructureParser,
                                  StructureParserError, ValidationError,
                                  ValidationResult)


class TestStructureParser:
    """Test cases for StructureParser class."""
    
    @pytest.fixture
    def parser(self):
        """Create a parser instance for testing."""
        return StructureParser()
    
    @pytest.fixture
    def valid_structure_data(self):
        """Valid structure data for testing."""
        return {
            "metadata": {
                "project_name": "test-project",
                "github_username": "testuser",
                "created_date": "2025-09-24",
                "version": "1.0.0",
                "schema_version": "2.0.0"
            },
            "structure": {
                "meta-repo": {
                    "governance": {
                        "structure": ["structure.json"],
                        "policies": ["contributing.md"]
                    }
                }
            }
        }
    
    @pytest.fixture
    def fixtures_dir(self):
        """Path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"
    
    def test_parser_initialization(self):
        """Test parser initialization."""
        parser = StructureParser()
        assert parser is not None
        
        # Test with custom schema path
        schema_path = Path("custom/schema.json")
        parser_with_schema = StructureParser(schema_path)
        assert parser_with_schema.schema_path == schema_path
    
    def test_parse_string_valid_json(self, parser, valid_structure_data):
        """Test parsing valid JSON string."""
        json_string = json.dumps(valid_structure_data)
        result = parser.parse_string(json_string)
        
        assert isinstance(result, StructureData)
        assert result.project_name == "test-project"
        assert result.github_username == "testuser"
        assert result.version == "1.0.0"
        assert "meta-repo" in result.structure
    
    def test_parse_string_invalid_json(self, parser):
        """Test parsing invalid JSON string."""
        invalid_json = '{"invalid": json,}'
        
        with pytest.raises(ParseError) as exc_info:
            parser.parse_string(invalid_json)
        
        assert "Invalid JSON" in str(exc_info.value)
        assert exc_info.value.line_number is not None
    
    def test_parse_string_validation_failure(self, parser):
        """Test parsing JSON that fails validation."""
        invalid_data = {
            "project_name": "",  # Empty name should fail validation
            "version": "2.0"
            # Missing required fields
        }
        
        with pytest.raises(ValidationError) as exc_info:
            parser.parse_string(json.dumps(invalid_data))
        
        assert "validation failed" in str(exc_info.value).lower()
    
    def test_parse_file_success(self, parser, fixtures_dir):
        """Test parsing valid file."""
        valid_file = fixtures_dir / "valid_structure.json"
        
        if valid_file.exists():
            result = parser.parse_file(valid_file)
            assert isinstance(result, StructureData)
            assert result.project_name == "test-project"
    
    def test_parse_file_not_found(self, parser):
        """Test parsing non-existent file."""
        nonexistent_file = Path("nonexistent.json")
        
        with pytest.raises(StructureFileNotFoundError):
            parser.parse_file(nonexistent_file)
    
    def test_parse_file_invalid_json(self, parser):
        """Test parsing file with invalid JSON."""
        with patch("builtins.open", mock_open(read_data='{"invalid": json,}')):
            with patch.object(Path, "exists", return_value=True):
                with pytest.raises(StructureParserError):
                    parser.parse_file(Path("invalid.json"))
    
    def test_validate_basic_structure(self, parser, valid_structure_data):
        """Test basic validation without schema."""
        result = parser.validate(valid_structure_data)
        
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert result.error_count == 0
    
    def test_validate_missing_required_fields(self, parser):
        """Test validation with missing required fields."""
        incomplete_data = {
            "project_name": "test"
            # Missing other required fields
        }
        
        result = parser.validate(incomplete_data)
        
        assert not result.is_valid
        assert result.error_count > 0
        
        # Check that specific fields are reported as missing
        error_messages = [error.message for error in result.errors]
        assert any("github_username" in msg for msg in error_messages)
        assert any("version" in msg for msg in error_messages)
        assert any("structure" in msg for msg in error_messages)
    
    def test_validate_invalid_field_types(self, parser):
        """Test validation with invalid field types."""
        invalid_data = {
            "project_name": 123,  # Should be string
            "github_username": [],  # Should be string
            "version": {},  # Should be string
            "structure": "not an object"  # Should be object
        }
        
        result = parser.validate(invalid_data)
        
        assert not result.is_valid
        assert result.error_count >= 4  # At least one error per invalid field
    
    def test_get_directory_structure(self, parser, valid_structure_data):
        """Test extracting directory structure."""
        structure_data = StructureData.from_dict(valid_structure_data)
        
        directories = parser.get_directory_structure(structure_data)
        
        assert len(directories) > 0
        assert any("meta-repo" in str(path) for path in directories)
        assert any("governance" in str(path) for path in directories)
    
    def test_export_structure(self, parser, valid_structure_data, tmp_path):
        """Test exporting structure to file."""
        structure_data = StructureData.from_dict(valid_structure_data)
        
        output_file = tmp_path / "exported_structure.json"
        parser.export_structure(structure_data, output_file)
        
        assert output_file.exists()
        
        # Verify exported content
        with open(output_file, 'r') as f:
            exported_data = json.load(f)
        
        assert exported_data["project_name"] == "test-project"
        assert exported_data["version"] == "1.0.0"
        assert "structure" in exported_data
    
    def test_migration_v1_to_v2(self, parser):
        """Test migration from version 1.x to 2.0.""" 
        # Create v1 format data (flat structure)
        v1_data = {
            "project_name": "legacy-project",
            "github_username": "legacyuser", 
            "created_date": "2024-01-01",
            "version": "1.0",
            "structure": {"meta-repo": {"governance": {}}}
        }
        structure_data = StructureData.from_dict(v1_data)
        
        migrated = parser._migrate_v1_to_v2(structure_data)
        
        assert migrated.version == "2.0.0"
        assert migrated.project_name == "legacy-project"
        assert migrated.github_username == "legacyuser"
    
    def test_migration_unsupported_version(self, parser):
        """Test migration with unsupported version combination."""
        # Create v3 format data (hypothetical future version)
        v3_data = {
            "metadata": {
                "project_name": "future-project",
                "github_username": "futureuser",
                "version": "3.0.0",
                "schema_version": "3.0.0"
            },
            "structure": {"meta-repo": {"governance": {}}}
        }
        structure_data = StructureData.from_dict(v3_data)
        
        with pytest.raises(MigrationError) as exc_info:
            parser._migrate_structure(structure_data, "2.0")
        
        assert "not supported" in str(exc_info.value)
    
    def test_get_schema_info(self, parser):
        """Test getting schema information."""
        schema_info = parser.get_schema_info()
        
        assert isinstance(schema_info, dict)
        assert "has_validation" in schema_info
        assert "schema_version" in schema_info
        
        # In fallback mode, validation should be False
        if not parser.validator:
            assert not schema_info["has_validation"]
            assert schema_info["schema_version"] == "fallback-mode"


class TestStructureParserIntegration:
    """Integration tests using fixture files."""
    
    @pytest.fixture
    def parser(self):
        return StructureParser()
    
    @pytest.fixture
    def fixtures_dir(self):
        return Path(__file__).parent / "fixtures"
    
    def test_parse_valid_fixture(self, parser, fixtures_dir):
        """Test parsing the valid structure fixture."""
        valid_file = fixtures_dir / "valid_structure.json"
        
        if valid_file.exists():
            result = parser.parse_file(valid_file)
            
            assert result.project_name == "test-project"
            assert result.github_username == "testuser"
            assert result.version == "1.0.0"
            assert "test" in result.tags
            assert "example" in result.tags
            
            # Test structure access methods
            assert result.has_directory("meta-repo")
            assert result.has_directory("meta-repo/governance")
            assert not result.has_directory("nonexistent")
            
            top_dirs = result.get_top_level_directories()
            assert "cloud-storage" in top_dirs
            assert "meta-repo" in top_dirs
            assert "core-services" in top_dirs
    
    def test_parse_invalid_fixture_handling(self, parser, fixtures_dir):
        """Test graceful handling of invalid fixture."""
        invalid_file = fixtures_dir / "invalid_structure.json"
        
        if invalid_file.exists():
            with pytest.raises((ValidationError, ParseError, StructureParserError)):
                parser.parse_file(invalid_file)
    
    def test_migration_fixture(self, parser, fixtures_dir):
        """Test migration using v1 fixture."""
        v1_file = fixtures_dir / "v1_structure.json"
        
        if v1_file.exists():
            # This should work even with basic validation
            try:
                result = parser.parse_file(v1_file)
                assert result.version == "1.0"
                
                # Test migration
                migrated = parser._migrate_v1_to_v2(result)
                assert migrated.version == "2.0.0"
                assert migrated.project_name == result.project_name
            except ValidationError:
                # Expected in strict validation mode
                pass