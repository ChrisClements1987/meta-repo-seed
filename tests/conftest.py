"""
Pytest configuration and fixtures for Meta-Repo Seed tests.

This module provides shared fixtures and configuration for all tests.
"""

import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing that gets cleaned up after the test."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def mock_templates_dir():
    """Create a mock templates directory with sample template files."""
    temp_path = Path(tempfile.mkdtemp())
    
    # Create mock template structure
    templates_dir = temp_path / "templates"
    templates_dir.mkdir(parents=True)
    
    # Create sample template files
    (templates_dir / "gitignore.template").write_text("# {{PROJECT_NAME}} .gitignore\n*.log\n")
    
    # GitHub workflows
    workflows_dir = templates_dir / "github" / "workflows"
    workflows_dir.mkdir(parents=True)
    (workflows_dir / "ci.yml.template").write_text("""
name: CI for {{PROJECT_NAME}}
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test {{PROJECT_NAME}}
        run: echo "Testing {{PROJECT_NAME}}"
""")
    
    # Governance templates
    governance_dir = templates_dir / "governance" / "policies"
    governance_dir.mkdir(parents=True)
    (governance_dir / "contributing.md.template").write_text("""
# Contributing to {{PROJECT_NAME}}

Welcome to {{PROJECT_NAME}}! Created by {{GITHUB_USERNAME}} on {{CURRENT_DATE}}.
""")
    
    yield templates_dir
    
    # Cleanup
    if temp_path.exists():
        shutil.rmtree(temp_path)


@pytest.fixture
def sample_replacements():
    """Provide sample template replacement variables."""
    return {
        'PROJECT_NAME': 'test-project',
        'GITHUB_USERNAME': 'test-user',
        'CURRENT_DATE': '2025-09-24',
        'DECISION_NUMBER': '001',
        'DECISION_TITLE': 'Test Decision',
        'STATUS': 'Accepted',
        'ALTERNATIVE_NAME': 'Test Alternative'
    }


@pytest.fixture
def mock_git_config():
    """Mock git configuration for testing."""
    with patch('subprocess.run') as mock_run:
        # Mock git config responses
        mock_run.return_value.stdout = 'test-user'
        mock_run.return_value.returncode = 0
        yield mock_run


@pytest.fixture
def mock_github_cli():
    """Mock GitHub CLI commands for testing."""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = 'success'
        yield mock_run


@pytest.fixture
def sample_config_dict():
    """Provide a sample configuration dictionary."""
    return {
        'project': {
            'name': 'test-project',
            'description': 'A test project',
            'author': 'Test Author',
            'type': 'web-application'
        },
        'github': {
            'enabled': True,
            'username': 'test-user',
            'create_repo': False,
            'private': False
        },
        'templates': {
            'enabled_templates': ['gitignore', 'github_workflows', 'governance']
        },
        'variables': {
            'ORGANIZATION_NAME': 'Test Organization',
            'LICENSE_TYPE': 'MIT'
        },
        'options': {
            'verbose': True,
            'dry_run': False,
            'backup_existing': True
        }
    }


@pytest.fixture
def sample_yaml_config(temp_dir, sample_config_dict):
    """Create a sample YAML configuration file."""
    import yaml
    
    config_file = temp_dir / "test_config.yml"
    with open(config_file, 'w') as f:
        yaml.dump(sample_config_dict, f)
    
    return config_file


@pytest.fixture
def sample_json_config(temp_dir, sample_config_dict):
    """Create a sample JSON configuration file."""
    import json
    
    config_file = temp_dir / "test_config.json"
    with open(config_file, 'w') as f:
        json.dump(sample_config_dict, f, indent=2)
    
    return config_file


@pytest.fixture(autouse=True)
def mock_logging():
    """Mock logging to reduce test output noise."""
    with patch('seeding.logger') as mock_logger:
        yield mock_logger


@pytest.fixture
def no_git_repo(temp_dir, monkeypatch):
    """Run test in directory without git repository."""
    monkeypatch.chdir(temp_dir)
    yield temp_dir


@pytest.fixture
def mock_file_operations():
    """Mock file system operations for isolated testing."""
    with patch('pathlib.Path.mkdir') as mock_mkdir, \
         patch('pathlib.Path.write_text') as mock_write, \
         patch('pathlib.Path.exists') as mock_exists:
        
        mock_exists.return_value = False  # Files don't exist by default
        yield {
            'mkdir': mock_mkdir,
            'write_text': mock_write,
            'exists': mock_exists
        }


class MockPath:
    """Mock Path object for testing path operations."""
    
    def __init__(self, path_str):
        self.path_str = str(path_str)
        
    def __str__(self):
        return self.path_str
        
    def __truediv__(self, other):
        return MockPath(f"{self.path_str}/{other}")
        
    def exists(self):
        return False
        
    def is_dir(self):
        return False
        
    def mkdir(self, parents=True, exist_ok=True):
        pass
        
    @property
    def parent(self):
        return MockPath("/".join(self.path_str.split("/")[:-1]))


@pytest.fixture 
def mock_paths():
    """Provide mock path objects for testing."""
    return MockPath


# Test markers
pytest.fixture(scope="session")
def pytest_configure():
    """Configure pytest markers."""
    pytest.main.addoption = Mock()


# Custom assertions for common test patterns
def assert_file_created(temp_dir, filename, content_contains=None):
    """Assert that a file was created with optional content check."""
    file_path = temp_dir / filename
    assert file_path.exists(), f"File {filename} was not created"
    
    if content_contains:
        content = file_path.read_text()
        assert content_contains in content, f"File {filename} does not contain expected content"


def assert_directory_created(temp_dir, dirname):
    """Assert that a directory was created."""
    dir_path = temp_dir / dirname
    assert dir_path.exists(), f"Directory {dirname} was not created"
    assert dir_path.is_dir(), f"Path {dirname} exists but is not a directory"


# Make assertions available to all tests
pytest.assert_file_created = assert_file_created
pytest.assert_directory_created = assert_directory_created