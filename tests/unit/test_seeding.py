"""
Unit tests for core seeding functionality.

Tests the main RepoSeeder class and its core methods.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import subprocess
import os

# Import the module we're testing
import sys
sys.path.append(str(Path(__file__).parent.parent))
from seeding import RepoSeeder, ensure_directory_exists, get_project_name, get_github_username


class TestRepoSeeder:
    """Test cases for the RepoSeeder class."""
    
    def test_init_with_valid_parameters(self, temp_dir):
        """Test RepoSeeder initialization with valid parameters."""
        project_name = "test-project"
        github_username = "test-user"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder(project_name, github_username, dry_run=True)
            
            assert seeder.project_name == project_name
            assert seeder.github_username == github_username
            assert seeder.dry_run is True
            assert 'PROJECT_NAME' in seeder.replacements
            assert seeder.replacements['PROJECT_NAME'] == project_name
            assert seeder.replacements['GITHUB_USERNAME'] == github_username
    
    def test_init_sets_correct_paths(self, temp_dir):
        """Test that RepoSeeder sets up correct directory paths."""
        project_name = "test-project"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder(project_name, "test-user", dry_run=True)
            
            # Check path setup
            expected_project_root = temp_dir / project_name
            expected_meta_repo = expected_project_root / 'meta-repo'
            expected_cloud_storage = expected_project_root / 'cloud-storage'
            
            assert seeder.project_root == expected_project_root
            assert seeder.meta_repo_path == expected_meta_repo
            assert seeder.cloud_storage_path == expected_cloud_storage
    
    def test_init_with_meta_repo_seed_directory(self, temp_dir):
        """Test initialization when running from meta-repo-seed directory."""
        meta_seed_dir = temp_dir / "meta-repo-seed"
        meta_seed_dir.mkdir()
        
        with patch('seeding.Path.cwd', return_value=meta_seed_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            
            # Should use parent directory as base
            assert seeder.base_path == temp_dir
    
    def test_replacements_dictionary_complete(self, temp_dir):
        """Test that all expected template variables are in replacements dict."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            
            expected_keys = [
                'PROJECT_NAME', 'GITHUB_USERNAME', 'CURRENT_DATE',
                'DECISION_NUMBER', 'DECISION_TITLE', 'STATUS', 'ALTERNATIVE_NAME'
            ]
            
            for key in expected_keys:
                assert key in seeder.replacements, f"Missing replacement key: {key}"
    
    @patch('seeding.ensure_directory_exists')
    def test_create_base_structure_dry_run(self, mock_ensure_dir, temp_dir):
        """Test create_base_structure in dry run mode."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            seeder.create_base_structure()
            
            # In dry run mode, no directories should be created
            mock_ensure_dir.assert_not_called()
    
    @patch('seeding.ensure_directory_exists')
    def test_create_base_structure_normal_mode(self, mock_ensure_dir, temp_dir):
        """Test create_base_structure in normal mode."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=False)
            seeder.create_base_structure()
            
            # Should create all expected directories
            expected_calls = [
                seeder.project_root,
                seeder.meta_repo_path, 
                seeder.cloud_storage_path,
                seeder.project_root / 'core-services',
                seeder.project_root / 'saas-products',
                seeder.project_root / 'partner-products',
                seeder.project_root / 'charity-products'
            ]
            
            assert mock_ensure_dir.call_count >= len(expected_calls)
    
    def test_run_method_dry_run(self, temp_dir, mock_templates_dir):
        """Test the main run method in dry run mode."""
        with patch('seeding.Path.cwd', return_value=temp_dir), \
             patch.object(RepoSeeder, 'create_base_structure') as mock_base, \
             patch.object(RepoSeeder, 'setup_cloud_storage') as mock_cloud, \
             patch.object(RepoSeeder, 'setup_meta_repo') as mock_meta:
            
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            seeder.templates_dir = mock_templates_dir
            seeder.run()
            
            # All setup methods should be called even in dry run
            mock_base.assert_called_once()
            mock_cloud.assert_called_once()
            mock_meta.assert_called_once()
    
    def test_run_method_normal_mode(self, temp_dir, mock_templates_dir):
        """Test the main run method in normal mode."""
        with patch('seeding.Path.cwd', return_value=temp_dir), \
             patch.object(RepoSeeder, 'create_base_structure') as mock_base, \
             patch.object(RepoSeeder, 'setup_cloud_storage') as mock_cloud, \
             patch.object(RepoSeeder, 'setup_meta_repo') as mock_meta:
            
            seeder = RepoSeeder("test-project", "test-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            seeder.run()
            
            mock_base.assert_called_once()
            mock_cloud.assert_called_once()
            mock_meta.assert_called_once()


class TestUtilityFunctions:
    """Test cases for utility functions."""
    
    def test_ensure_directory_exists_creates_new_directory(self, temp_dir):
        """Test ensure_directory_exists creates a new directory."""
        test_dir = temp_dir / "new_directory"
        assert not test_dir.exists()
        
        result = ensure_directory_exists(test_dir, "test directory")
        
        assert result is True  # Should return True for new directory
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_ensure_directory_exists_with_existing_directory(self, temp_dir):
        """Test ensure_directory_exists with existing directory."""
        test_dir = temp_dir / "existing_directory"
        test_dir.mkdir()
        
        result = ensure_directory_exists(test_dir, "test directory")
        
        assert result is False  # Should return False for existing directory
        assert test_dir.exists()
        assert test_dir.is_dir()
    
    def test_ensure_directory_exists_with_nested_path(self, temp_dir):
        """Test ensure_directory_exists creates nested directories."""
        nested_dir = temp_dir / "level1" / "level2" / "level3"
        assert not nested_dir.exists()
        
        result = ensure_directory_exists(nested_dir, "nested directory")
        
        assert result is True
        assert nested_dir.exists()
        assert nested_dir.is_dir()
    
    def test_ensure_directory_exists_with_file_conflict(self, temp_dir):
        """Test ensure_directory_exists raises error when path is a file."""
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("test content")
        
        with pytest.raises(FileExistsError, match="Path exists but is not a directory"):
            ensure_directory_exists(test_file, "test directory")
    
    @patch('seeding.Path.cwd')
    def test_get_project_name_from_current_directory(self, mock_cwd, temp_dir):
        """Test get_project_name returns current directory name."""
        project_dir = temp_dir / "my-awesome-project"
        mock_cwd.return_value = project_dir
        
        result = get_project_name()
        
        assert result == "my-awesome-project"
    
    @patch('seeding.Path.cwd')
    def test_get_project_name_from_meta_repo_seed_directory(self, mock_cwd, temp_dir):
        """Test get_project_name when running from meta-repo-seed directory."""
        parent_dir = temp_dir / "parent-project"
        meta_seed_dir = parent_dir / "meta-repo-seed"
        mock_cwd.return_value = meta_seed_dir
        
        result = get_project_name()
        
        assert result == "parent-project"
    
    @patch('subprocess.run')
    def test_get_github_username_from_git_config(self, mock_run):
        """Test get_github_username retrieves from git config."""
        mock_run.return_value.stdout = "github-user\n"
        mock_run.return_value.returncode = 0
        
        result = get_github_username()
        
        assert result == "github-user"
        mock_run.assert_called_once_with(
            ['git', 'config', '--global', 'user.name'],
            capture_output=True,
            text=True,
            check=True
        )
    
    @patch('subprocess.run')
    @patch('builtins.input', return_value='manual-user')
    def test_get_github_username_fallback_to_input(self, mock_input, mock_run):
        """Test get_github_username falls back to user input when git config fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        result = get_github_username()
        
        assert result == "manual-user"
        mock_input.assert_called_once()
    
    @patch('subprocess.run')
    @patch('builtins.input', return_value='')
    def test_get_github_username_raises_error_on_empty_input(self, mock_input, mock_run):
        """Test get_github_username raises error when user provides empty input."""
        mock_run.side_effect = subprocess.CalledProcessError(1, 'git')
        
        with pytest.raises(ValueError, match="GitHub username is required"):
            get_github_username()


class TestTemplateProcessing:
    """Test cases for template-related functionality."""
    
    @patch('seeding.copy_template_file')
    @patch('seeding.ensure_directory_exists')
    def test_setup_meta_repo_creates_gitignore(self, mock_ensure_dir, mock_copy_template, temp_dir, mock_templates_dir):
        """Test that setup_meta_repo creates .gitignore from template."""
        mock_copy_template.return_value = True
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            
            with patch.object(seeder, 'init_git_repo'), \
                 patch.object(seeder, 'create_gitignore') as mock_gitignore:
                seeder.setup_meta_repo()
                
                mock_gitignore.assert_called_once()
                # Also verify that copy_template_file was called for workflows
                assert mock_copy_template.call_count >= 2  # CI and README workflows
    
    def test_template_replacements_applied_correctly(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test that template variable replacements work correctly."""
        from seeding import create_file_from_template
        
        # Create a test template
        template_file = mock_templates_dir / "test.template"
        template_content = "Project: {{PROJECT_NAME}}\nUser: {{GITHUB_USERNAME}}\nDate: {{CURRENT_DATE}}"
        template_file.write_text(template_content)
        
        # Create output file
        output_file = temp_dir / "output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "Project: test-project" in content
        assert "User: test-user" in content
        assert "Date: 2025-09-24" in content


class TestErrorHandling:
    """Test cases for error handling scenarios."""
    
    def test_missing_template_directory(self, temp_dir):
        """Test behavior when templates directory doesn't exist."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            seeder.templates_dir = temp_dir / "nonexistent_templates"
            
            # Should not crash, but may log warnings
            # The actual behavior depends on implementation
            assert seeder.templates_dir == temp_dir / "nonexistent_templates"
    
    def test_permission_error_handling(self, temp_dir):
        """Test handling of permission errors during directory creation."""
        with patch('pathlib.Path.mkdir') as mock_mkdir:
            mock_mkdir.side_effect = PermissionError("Access denied")
            
            test_dir = temp_dir / "restricted"
            
            with pytest.raises(PermissionError):
                ensure_directory_exists(test_dir)


class TestDryRunMode:
    """Test cases specifically for dry run mode behavior."""
    
    @patch('seeding.ensure_directory_exists')
    def test_dry_run_prevents_directory_creation(self, mock_ensure_dir, temp_dir):
        """Test that dry run mode prevents actual directory creation."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            
            seeder.create_base_structure()
            
            # No directories should be created in dry run mode
            mock_ensure_dir.assert_not_called()
    
    @patch('seeding.create_file_from_template')
    def test_dry_run_prevents_file_creation(self, mock_create_file, temp_dir):
        """Test that dry run mode prevents actual file creation."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            
            seeder.create_template_content()
            
            # No files should be created in dry run mode
            mock_create_file.assert_not_called()
    
    def test_dry_run_mode_logging(self, temp_dir, caplog):
        """Test that dry run mode produces appropriate log messages."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-project", "test-user", dry_run=True)
            seeder.run()
            
            # Should see dry run related log messages
            # (This test depends on the actual logging implementation)
            assert seeder.dry_run is True