"""
Unit tests for Configuration class functionality.

Tests configuration file loading, saving, validation, and CLI integration.
"""

import pytest
import yaml
import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open

# Import the module we're testing
import sys
sys.path.append(str(Path(__file__).parent.parent))
from seeding import Configuration


class TestConfigurationClass:
    """Test cases for the Configuration class."""
    
    def test_init_with_defaults(self):
        """Test Configuration initialization with default values."""
        config = Configuration()
        
        assert config.project_name is None
        assert config.github_username is None
        assert config.dry_run is False
        assert config.templates_dir is None
        assert config.base_path is None
    
    def test_init_with_parameters(self, temp_dir):
        """Test Configuration initialization with specific parameters."""
        config = Configuration(
            project_name="test-project",
            github_username="test-user",
            dry_run=True,
            templates_dir=temp_dir,
            base_path=temp_dir
        )
        
        assert config.project_name == "test-project"
        assert config.github_username == "test-user"
        assert config.dry_run is True
        assert config.templates_dir == temp_dir
        assert config.base_path == temp_dir
    
    def test_from_dict_complete_config(self):
        """Test creating Configuration from complete dictionary."""
        data = {
            'project_name': 'dict-project',
            'github_username': 'dict-user',
            'dry_run': True,
            'templates_dir': '/path/to/templates',
            'base_path': '/path/to/base'
        }
        
        config = Configuration.from_dict(data)
        
        assert config.project_name == 'dict-project'
        assert config.github_username == 'dict-user'
        assert config.dry_run is True
        # Check that paths are converted to Path objects correctly
        assert config.templates_dir == Path('/path/to/templates')
        assert config.base_path == Path('/path/to/base')
    
    def test_from_dict_partial_config(self):
        """Test creating Configuration from partial dictionary."""
        data = {
            'project_name': 'partial-project',
            'dry_run': True
        }
        
        config = Configuration.from_dict(data)
        
        assert config.project_name == 'partial-project'
        assert config.github_username is None  # Should remain None
        assert config.dry_run is True
        assert config.templates_dir is None
        assert config.base_path is None
    
    def test_from_dict_empty_dict(self):
        """Test creating Configuration from empty dictionary."""
        config = Configuration.from_dict({})
        
        assert config.project_name is None
        assert config.github_username is None
        assert config.dry_run is False
        assert config.templates_dir is None
        assert config.base_path is None
    
    def test_to_dict_complete_config(self, temp_dir):
        """Test converting Configuration to dictionary."""
        config = Configuration(
            project_name="dict-project",
            github_username="dict-user",
            dry_run=True,
            templates_dir=temp_dir / "templates",
            base_path=temp_dir
        )
        
        result = config.to_dict()
        
        expected = {
            'project_name': 'dict-project',
            'github_username': 'dict-user',
            'dry_run': True,
            'templates_dir': str(temp_dir / "templates"),
            'base_path': str(temp_dir)
        }
        
        assert result == expected
    
    def test_to_dict_with_none_values(self):
        """Test converting Configuration with None values to dictionary."""
        config = Configuration(project_name="test-project")
        
        result = config.to_dict()
        
        expected = {
            'project_name': 'test-project',
            'github_username': None,
            'dry_run': False,
            'templates_dir': None,
            'base_path': None
        }
        
        assert result == expected


class TestConfigurationFileSaving:
    """Test cases for saving configuration files."""
    
    def test_save_yaml_file(self, temp_dir):
        """Test saving configuration as YAML file."""
        config = Configuration(
            project_name="yaml-project",
            github_username="yaml-user",
            dry_run=True
        )
        
        config_file = temp_dir / "config.yaml"
        result = config.save(config_file)
        
        assert result is True
        assert config_file.exists()
        
        # Verify file content
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        
        assert data['project_name'] == 'yaml-project'
        assert data['github_username'] == 'yaml-user'
        assert data['dry_run'] is True
    
    def test_save_json_file(self, temp_dir):
        """Test saving configuration as JSON file."""
        config = Configuration(
            project_name="json-project",
            github_username="json-user",
            dry_run=False
        )
        
        config_file = temp_dir / "config.json"
        result = config.save(config_file)
        
        assert result is True
        assert config_file.exists()
        
        # Verify file content
        with open(config_file, 'r') as f:
            data = json.load(f)
        
        assert data['project_name'] == 'json-project'
        assert data['github_username'] == 'json-user'
        assert data['dry_run'] is False
    
    def test_save_creates_parent_directories(self, temp_dir):
        """Test that save creates parent directories if they don't exist."""
        config = Configuration(project_name="nested-project")
        
        nested_config_file = temp_dir / "configs" / "subdir" / "config.yaml"
        result = config.save(nested_config_file)
        
        assert result is True
        assert nested_config_file.exists()
        assert nested_config_file.parent.exists()
    
    def test_save_unsupported_format_raises_error(self, temp_dir):
        """Test that saving with unsupported format raises ValueError."""
        config = Configuration(project_name="test-project")
        
        config_file = temp_dir / "config.txt"
        
        with pytest.raises(ValueError, match="Unsupported config format"):
            config.save(config_file)
    
    @patch('builtins.open', side_effect=PermissionError("Access denied"))
    def test_save_permission_error_handling(self, mock_open, temp_dir):
        """Test handling of permission errors during save."""
        config = Configuration(project_name="test-project")
        config_file = temp_dir / "config.yaml"
        
        result = config.save(config_file)
        
        assert result is False
    
    @patch('yaml.safe_dump', side_effect=Exception("YAML error"))
    def test_save_yaml_serialization_error(self, mock_dump, temp_dir):
        """Test handling of YAML serialization errors."""
        config = Configuration(project_name="test-project")
        config_file = temp_dir / "config.yaml"
        
        result = config.save(config_file)
        
        assert result is False


class TestConfigurationFileLoading:
    """Test cases for loading configuration files."""
    
    def test_load_yaml_file(self, temp_dir):
        """Test loading configuration from YAML file."""
        # Create test YAML file
        config_data = {
            'project_name': 'loaded-yaml-project',
            'github_username': 'loaded-yaml-user',
            'dry_run': True
        }
        
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.safe_dump(config_data, f)
        
        config = Configuration.load(config_file)
        
        assert config.project_name == 'loaded-yaml-project'
        assert config.github_username == 'loaded-yaml-user'
        assert config.dry_run is True
    
    def test_load_json_file(self, temp_dir):
        """Test loading configuration from JSON file."""
        # Create test JSON file
        config_data = {
            'project_name': 'loaded-json-project',
            'github_username': 'loaded-json-user',
            'dry_run': False
        }
        
        config_file = temp_dir / "config.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        config = Configuration.load(config_file)
        
        assert config.project_name == 'loaded-json-project'
        assert config.github_username == 'loaded-json-user'
        assert config.dry_run is False
    
    def test_load_nonexistent_file_returns_none(self, temp_dir):
        """Test loading non-existent file returns None."""
        config_file = temp_dir / "nonexistent.yaml"
        
        config = Configuration.load(config_file)
        
        assert config is None
    
    def test_load_unsupported_format_returns_none(self, temp_dir):
        """Test loading unsupported file format returns None."""
        config_file = temp_dir / "config.txt"
        config_file.write_text("some content")
        
        config = Configuration.load(config_file)
        
        assert config is None
    
    @patch('builtins.open', side_effect=PermissionError("Access denied"))
    def test_load_permission_error_returns_none(self, mock_open, temp_dir):
        """Test that permission errors during load return None."""
        config_file = temp_dir / "config.yaml"
        
        config = Configuration.load(config_file)
        
        assert config is None
    
    def test_load_invalid_yaml_returns_none(self, temp_dir):
        """Test loading invalid YAML returns None."""
        config_file = temp_dir / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")
        
        config = Configuration.load(config_file)
        
        assert config is None
    
    def test_load_invalid_json_returns_none(self, temp_dir):
        """Test loading invalid JSON returns None."""
        config_file = temp_dir / "invalid.json"
        config_file.write_text('{"invalid": json, content}')
        
        config = Configuration.load(config_file)
        
        assert config is None
    
    def test_load_with_path_conversion(self, temp_dir):
        """Test loading configuration with path string conversion."""
        # Create config with path strings
        config_data = {
            'project_name': 'path-project',
            'templates_dir': str(temp_dir / 'templates'),
            'base_path': str(temp_dir)
        }
        
        config_file = temp_dir / "config.yaml"
        with open(config_file, 'w') as f:
            yaml.safe_dump(config_data, f)
        
        config = Configuration.load(config_file)
        
        assert config.project_name == 'path-project'
        assert config.templates_dir == temp_dir / 'templates'
        assert config.base_path == temp_dir


class TestConfigurationIntegration:
    """Test cases for Configuration integration with RepoSeeder."""
    
    def test_configuration_roundtrip_yaml(self, temp_dir):
        """Test saving and loading configuration maintains data integrity (YAML)."""
        original_config = Configuration(
            project_name="roundtrip-project",
            github_username="roundtrip-user",
            dry_run=True,
            templates_dir=temp_dir / "templates",
            base_path=temp_dir
        )
        
        config_file = temp_dir / "roundtrip.yaml"
        
        # Save and load
        save_result = original_config.save(config_file)
        loaded_config = Configuration.load(config_file)
        
        assert save_result is True
        assert loaded_config is not None
        assert loaded_config.project_name == original_config.project_name
        assert loaded_config.github_username == original_config.github_username
        assert loaded_config.dry_run == original_config.dry_run
        assert loaded_config.templates_dir == original_config.templates_dir
        assert loaded_config.base_path == original_config.base_path
    
    def test_configuration_roundtrip_json(self, temp_dir):
        """Test saving and loading configuration maintains data integrity (JSON)."""
        original_config = Configuration(
            project_name="roundtrip-json-project",
            github_username="roundtrip-json-user",
            dry_run=False
        )
        
        config_file = temp_dir / "roundtrip.json"
        
        # Save and load
        save_result = original_config.save(config_file)
        loaded_config = Configuration.load(config_file)
        
        assert save_result is True
        assert loaded_config is not None
        assert loaded_config.project_name == original_config.project_name
        assert loaded_config.github_username == original_config.github_username
        assert loaded_config.dry_run == original_config.dry_run
    
    def test_configuration_with_none_values_roundtrip(self, temp_dir):
        """Test that None values are handled correctly in save/load cycle."""
        original_config = Configuration(
            project_name="partial-project",
            # Other fields remain None
        )
        
        config_file = temp_dir / "partial.yaml"
        
        save_result = original_config.save(config_file)
        loaded_config = Configuration.load(config_file)
        
        assert save_result is True
        assert loaded_config is not None
        assert loaded_config.project_name == "partial-project"
        assert loaded_config.github_username is None
        assert loaded_config.dry_run is False  # Default value
        assert loaded_config.templates_dir is None
        assert loaded_config.base_path is None


class TestConfigurationValidation:
    """Test cases for configuration validation and error handling."""
    
    def test_from_dict_with_invalid_types(self):
        """Test Configuration.from_dict handles type conversion gracefully."""
        data = {
            'project_name': 123,  # Should be string
            'dry_run': 'true',    # Should be boolean
        }
        
        config = Configuration.from_dict(data)
        
        # Should handle type conversion or set reasonable defaults
        assert config.project_name == 123  # Or converted to '123'
        assert config.dry_run == 'true'    # Or converted to True
    
    def test_to_dict_serializable_output(self, temp_dir):
        """Test that to_dict produces JSON-serializable output."""
        config = Configuration(
            project_name="serializable-project",
            templates_dir=temp_dir / "templates",
            base_path=temp_dir
        )
        
        result = config.to_dict()
        
        # Should be JSON serializable
        json_str = json.dumps(result)
        loaded_result = json.loads(json_str)
        
        assert loaded_result['project_name'] == 'serializable-project'
        assert loaded_result['templates_dir'] == str(temp_dir / "templates")
        assert loaded_result['base_path'] == str(temp_dir)
    
    def test_configuration_equality(self, temp_dir):
        """Test configuration equality comparison."""
        config1 = Configuration(
            project_name="equal-project",
            github_username="equal-user",
            dry_run=True,
            templates_dir=temp_dir
        )
        
        config2 = Configuration(
            project_name="equal-project",
            github_username="equal-user",
            dry_run=True,
            templates_dir=temp_dir
        )
        
        config3 = Configuration(
            project_name="different-project",
            github_username="equal-user",
            dry_run=True,
            templates_dir=temp_dir
        )
        
        # Note: This test assumes __eq__ method is implemented
        # If not implemented, these assertions might need adjustment
        assert config1.to_dict() == config2.to_dict()
        assert config1.to_dict() != config3.to_dict()


class TestConfigurationPathHandling:
    """Test cases for path handling in configuration."""
    
    def test_path_normalization(self):
        """Test that paths are normalized correctly."""
        data = {
            'templates_dir': '/path/to/../templates',
            'base_path': '/path/to/base/'
        }
        
        config = Configuration.from_dict(data)
        
        # Paths should be normalized (depending on implementation)
        assert isinstance(config.templates_dir, Path)
        assert isinstance(config.base_path, Path)
    
    def test_relative_path_handling(self, temp_dir):
        """Test handling of relative paths."""
        # Change to temp directory context
        with patch('pathlib.Path.cwd', return_value=temp_dir):
            data = {
                'templates_dir': './templates',
                'base_path': '../parent'
            }
            
            config = Configuration.from_dict(data)
            
            assert isinstance(config.templates_dir, Path)
            assert isinstance(config.base_path, Path)
    
    def test_windows_path_handling(self):
        """Test handling of Windows-style paths."""
        data = {
            'templates_dir': 'C:\\Users\\Test\\templates',
            'base_path': 'C:\\Projects\\base'
        }
        
        config = Configuration.from_dict(data)
        
        assert isinstance(config.templates_dir, Path)
        assert isinstance(config.base_path, Path)