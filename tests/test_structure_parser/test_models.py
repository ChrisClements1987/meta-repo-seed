"""
Tests for data models.
"""

import pytest
from pathlib import Path

from src.structure_parser.models import StructureData, ValidationResult, ValidationError


class TestStructureData:
    """Test cases for StructureData class."""
    
    @pytest.fixture
    def sample_structure_data(self):
        """Create sample structure data for testing."""
        data = {
            "metadata": {
                "project_name": "test-project",
                "github_username": "testuser",
                "created_date": "2025-09-24",
                "version": "1.0.0",
                "schema_version": "2.0.0"
            },
            "structure": {
                "cloud-storage": {
                    "strategy": ["vision.md", "mission.md"],
                    "architecture": {
                        "principles": ["principles.md"],
                        "adr": []
                    }
                },
                "meta-repo": {
                    "governance": {
                        "structure": ["structure.json"],
                        "policies": ["contributing.md", "code-of-conduct.md"]
                    },
                    "automation": {
                        "scripts": ["initialize-repo.py"]
                    }
                },
                "core-services": {
                    "service1": ["main.py", "config.py"],
                    "service2": {
                        "src": ["app.py"],
                        "tests": ["test-app.py"]
                    }
                }
            }
        }
        return StructureData.from_dict(data)
    
    def test_structure_data_initialization(self, sample_structure_data):
        """Test basic StructureData initialization."""
        data = sample_structure_data
        
        assert data.project_name == "test-project"
        assert data.github_username == "testuser"
        assert data.version == "1.0.0"
        assert data.schema_version == "2.0.0"
    
    def test_get_top_level_directories(self, sample_structure_data):
        """Test getting top-level directory names."""
        directories = sample_structure_data.get_top_level_directories()
        
        assert "cloud-storage" in directories
        assert "meta-repo" in directories
        assert "core-services" in directories
        assert len(directories) == 3
    
    def test_get_directory_files(self, sample_structure_data):
        """Test getting files for specific directories."""
        # Test getting files from a list directory
        strategy_files = sample_structure_data.get_directory_files("cloud-storage/strategy")
        assert "vision.md" in strategy_files
        assert "mission.md" in strategy_files
        
        # Test getting files from a dict directory (should collect all list values)
        governance_files = sample_structure_data.get_directory_files("meta-repo/governance")
        assert "structure.json" in governance_files
        assert "contributing.md" in governance_files
        assert "code-of-conduct.md" in governance_files
        
        # Test non-existent directory
        nonexistent_files = sample_structure_data.get_directory_files("nonexistent/path")
        assert nonexistent_files == []
    
    def test_has_directory(self, sample_structure_data):
        """Test checking if directories exist."""
        assert sample_structure_data.has_directory("cloud-storage")
        assert sample_structure_data.has_directory("cloud-storage/strategy")
        assert sample_structure_data.has_directory("meta-repo/governance")
        assert sample_structure_data.has_directory("core-services/service1")
        
        assert not sample_structure_data.has_directory("nonexistent")
        assert not sample_structure_data.has_directory("cloud-storage/nonexistent")
    
    def test_get_all_directories(self, sample_structure_data):
        """Test getting all directory paths."""
        all_directories = sample_structure_data.get_all_directories()
        
        expected_directories = [
            "cloud-storage",
            "cloud-storage/strategy",
            "cloud-storage/architecture",
            "cloud-storage/architecture/principles",
            "cloud-storage/architecture/adr",
            "meta-repo",
            "meta-repo/governance",
            "meta-repo/governance/structure",
            "meta-repo/governance/policies",
            "meta-repo/automation",
            "meta-repo/automation/scripts",
            "core-services",
            "core-services/service1",
            "core-services/service2",
            "core-services/service2/src",
            "core-services/service2/tests"
        ]
        
        for directory in expected_directories:
            assert directory in all_directories
    
    def test_get_all_files(self, sample_structure_data):
        """Test getting all files organized by directory."""
        files_by_dir = sample_structure_data.get_all_files()
        
        # Check that file lists are correctly associated with directories
        assert "vision.md" in files_by_dir["cloud-storage/strategy"]
        assert "mission.md" in files_by_dir["cloud-storage/strategy"]
        assert "principles.md" in files_by_dir["cloud-storage/architecture/principles"]
        assert "structure.json" in files_by_dir["meta-repo/governance/structure"]
        assert "initialize-repo.py" in files_by_dir["meta-repo/automation/scripts"]
        assert "main.py" in files_by_dir["core-services/service1"]
        assert "app.py" in files_by_dir["core-services/service2/src"]


class TestValidationError:
    """Test cases for ValidationError class."""
    
    def test_validation_error_initialization(self):
        """Test ValidationError initialization."""
        error = ValidationError(
            message="Test error message",
            path="test.path",
            error_code="TEST_ERROR",
            line_number=10
        )
        
        assert error.message == "Test error message"
        assert error.path == "test.path"
        assert error.error_code == "TEST_ERROR"
        assert error.line_number == 10
    
    def test_validation_error_string_representation(self):
        """Test ValidationError string conversion."""
        error = ValidationError(
            message="Test error",
            path="test.field",
            error_code="VALIDATION_ERROR",
            line_number=5
        )
        
        error_str = str(error)
        assert "VALIDATION_ERROR" in error_str
        assert "Test error" in error_str
        assert "test.field" in error_str
        assert "(line 5)" in error_str
    
    def test_validation_error_without_line_number(self):
        """Test ValidationError without line number."""
        error = ValidationError(
            message="Test error",
            path="test.field",
            error_code="ERROR"
        )
        
        error_str = str(error)
        assert "ERROR" in error_str
        assert "Test error" in error_str
        assert "test.field" in error_str
        assert "(line" not in error_str


class TestValidationResult:
    """Test cases for ValidationResult class."""
    
    def test_validation_result_initialization(self):
        """Test ValidationResult initialization."""
        result = ValidationResult(is_valid=True)
        
        assert result.is_valid
        assert result.error_count == 0
        assert result.warning_count == 0
        assert not result.has_errors
        assert not result.has_warnings
    
    def test_add_error(self):
        """Test adding validation errors."""
        result = ValidationResult(is_valid=True)
        
        result.add_error("Test error", "test.path", "TEST_ERROR", line_number=10)
        
        assert not result.is_valid  # Should become invalid when error is added
        assert result.error_count == 1
        assert result.has_errors
        
        error = result.errors[0]
        assert error.message == "Test error"
        assert error.path == "test.path"
        assert error.error_code == "TEST_ERROR"
        assert error.line_number == 10
    
    def test_add_warning(self):
        """Test adding validation warnings."""
        result = ValidationResult(is_valid=True)
        
        result.add_warning("Test warning", "test.path", "TEST_WARNING", line_number=5)
        
        assert result.is_valid  # Should remain valid when only warning is added
        assert result.warning_count == 1
        assert result.has_warnings
        
        warning = result.warnings[0]
        assert warning.message == "Test warning"
        assert warning.path == "test.path"
        assert warning.error_code == "TEST_WARNING"
        assert warning.line_number == 5
    
    def test_get_summary(self):
        """Test validation result summary."""
        result = ValidationResult(is_valid=True)
        
        # Valid with no issues
        assert result.get_summary() == "Valid"
        
        # Valid with warnings
        result.add_warning("Warning", "path", "WARN")
        assert "Valid with 1 warning" in result.get_summary()
        
        # Invalid with errors
        result.add_error("Error", "path", "ERROR")
        summary = result.get_summary()
        assert "Invalid" in summary
        assert "1 error" in summary
        assert "1 warning" in summary
    
    def test_get_detailed_report(self):
        """Test detailed validation report."""
        result = ValidationResult(is_valid=True, schema_version="2.0")
        
        result.add_error("Test error", "error.path", "ERROR")
        result.add_warning("Test warning", "warning.path", "WARNING")
        
        report = result.get_detailed_report()
        
        assert "Validation Result:" in report
        assert "Schema Version: 2.0" in report
        assert "Errors:" in report
        assert "ERROR: Test error" in report
        assert "Warnings:" in report
        assert "WARNING: Test warning" in report
    
    def test_multiple_errors_and_warnings(self):
        """Test handling multiple errors and warnings."""
        result = ValidationResult(is_valid=True)
        
        # Add multiple errors
        result.add_error("Error 1", "path1", "ERROR1")
        result.add_error("Error 2", "path2", "ERROR2")
        
        # Add multiple warnings
        result.add_warning("Warning 1", "path3", "WARN1")
        result.add_warning("Warning 2", "path4", "WARN2")
        
        assert not result.is_valid
        assert result.error_count == 2
        assert result.warning_count == 2
        assert result.has_errors
        assert result.has_warnings
        
        # Check that all errors and warnings are present
        error_messages = [error.message for error in result.errors]
        warning_messages = [warning.message for warning in result.warnings]
        
        assert "Error 1" in error_messages
        assert "Error 2" in error_messages
        assert "Warning 1" in warning_messages
        assert "Warning 2" in warning_messages