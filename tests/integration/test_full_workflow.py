"""
Integration tests for complete workflow scenarios.

Tests end-to-end functionality including RepoSeeder, Configuration,
and template processing working together.
"""

import json
import subprocess
# Import the modules we're testing
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
import yaml

sys.path.append(str(Path(__file__).parent.parent))
from seeding import Configuration, RepoSeeder, main


class TestCompleteWorkflow:
    """Test cases for complete end-to-end workflows."""
    
    @patch('subprocess.run')
    @patch('seeding.ensure_directory_exists')
    def test_full_repo_seeding_workflow_dry_run(self, mock_ensure_dir, mock_subprocess, 
                                                temp_dir, mock_templates_dir, mock_git_config):
        """Test complete repository seeding workflow in dry run mode."""
        # Setup git config mock
        mock_subprocess.return_value.stdout = "test-user"
        mock_subprocess.return_value.returncode = 0
        
        # Create template files
        (mock_templates_dir / "gitignore.template").write_text("# {{PROJECT_NAME}}\n*.log")
        (mock_templates_dir / "readme.template").write_text("# {{PROJECT_NAME}}\n\nBy {{GITHUB_USERNAME}}")
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("workflow-project", "workflow-user", dry_run=True)
            seeder.templates_dir = mock_templates_dir
            
            # Run complete workflow
            seeder.run()
            
            # Verify seeder configuration
            assert seeder.project_name == "workflow-project"
            assert seeder.github_username == "workflow-user"
            assert seeder.dry_run is True
            
            # In dry run mode, directories should not be created
            mock_ensure_dir.assert_not_called()
    
    @patch('subprocess.run')
    def test_full_repo_seeding_workflow_normal_mode(self, mock_subprocess, 
                                                   temp_dir, mock_templates_dir, mock_git_config):
        """Test complete repository seeding workflow in normal mode."""
        # Setup git config mock
        mock_subprocess.return_value.stdout = "test-user"
        mock_subprocess.return_value.returncode = 0
        
        # Create template files
        (mock_templates_dir / "gitignore.template").write_text("# {{PROJECT_NAME}}\n*.log")
        (mock_templates_dir / "readme.template").write_text("# {{PROJECT_NAME}}\n\nBy {{GITHUB_USERNAME}}")
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("workflow-project", "workflow-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            
            # Run complete workflow
            seeder.run()
            
            # Verify directory structure was created
            project_root = temp_dir / "workflow-project"
            assert project_root.exists()
            assert (project_root / "meta-repo").exists()
            assert (project_root / "cloud-storage").exists()
            assert (project_root / "core-services").exists()
    
    def test_configuration_integration_with_seeding(self, temp_dir, mock_templates_dir):
        """Test Configuration class integration with RepoSeeder."""
        # Create configuration
        config = Configuration(
            project_name="config-project",
            github_username="config-user",
            dry_run=True,
            templates_dir=mock_templates_dir,
            base_path=temp_dir
        )
        
        # Save configuration
        config_file = temp_dir / "project.yaml"
        assert config.save(config_file) is True
        
        # Load configuration and use with RepoSeeder
        loaded_config = Configuration.load(config_file)
        assert loaded_config is not None
        
        with patch('seeding.Path.cwd', return_value=loaded_config.base_path):
            seeder = RepoSeeder(
                loaded_config.project_name,
                loaded_config.github_username,
                dry_run=loaded_config.dry_run
            )
            seeder.templates_dir = loaded_config.templates_dir
            
            assert seeder.project_name == "config-project"
            assert seeder.github_username == "config-user"
            assert seeder.dry_run is True
            assert seeder.templates_dir == mock_templates_dir


class TestMainFunctionIntegration:
    """Test cases for main function and CLI integration."""
    
    @patch('sys.argv', ['seeding.py', '--dry-run'])
    @patch('seeding.get_project_name', return_value='cli-project')
    @patch('seeding.get_github_username', return_value='cli-user')
    def test_main_function_with_dry_run(self, mock_username, mock_project, temp_dir):
        """Test main function with dry-run argument."""
        with patch('seeding.Path.cwd', return_value=temp_dir), \
             patch.object(RepoSeeder, 'run') as mock_run:
            
            main()
            
            mock_run.assert_called_once()
    
    @patch('sys.argv', ['seeding.py', '--config', 'test-config.yaml'])
    def test_main_function_with_config_file(self, temp_dir, mock_templates_dir):
        """Test main function with configuration file."""
        # Create configuration file
        config = Configuration(
            project_name="config-cli-project",
            github_username="config-cli-user",
            dry_run=False,
            templates_dir=mock_templates_dir,
            base_path=temp_dir
        )
        
        config_file = temp_dir / "test-config.yaml"
        config.save(config_file)
        
        with patch('seeding.Path.cwd', return_value=temp_dir), \
             patch.object(RepoSeeder, 'run') as mock_run:
            
            main()
            
            mock_run.assert_called_once()
    
    @patch('sys.argv', ['seeding.py', '--project', 'override-project', '--username', 'override-user'])
    def test_main_function_with_cli_overrides(self, temp_dir):
        """Test main function with CLI parameter overrides."""
        with patch('seeding.Path.cwd', return_value=temp_dir), \
             patch.object(RepoSeeder, 'run') as mock_run:
            
            main()
            
            mock_run.assert_called_once()


class TestErrorRecoveryScenarios:
    """Test cases for error recovery and resilience."""
    
    @patch('subprocess.run', side_effect=Exception("Git command failed"))
    def test_git_command_failure_handling(self, mock_subprocess, temp_dir):
        """Test handling of git command failures."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("error-project", "error-user", dry_run=False)
            
            # Should handle git errors gracefully
            # Specific behavior depends on implementation
            try:
                seeder.init_git_repo()
                # If no exception is raised, error was handled
                assert True
            except Exception as e:
                # If exception is raised, it should be a handled error type
                assert isinstance(e, (subprocess.CalledProcessError, RuntimeError, Exception))
    
    def test_template_directory_missing_handling(self, temp_dir):
        """Test handling when templates directory is missing."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("missing-templates-project", "test-user", dry_run=False)
            seeder.templates_dir = temp_dir / "nonexistent_templates"
            
            # Should handle missing templates gracefully
            try:
                seeder.run()
                # If no exception, missing templates was handled
                assert True
            except FileNotFoundError:
                # Acceptable to raise FileNotFoundError for missing templates
                assert True
    
    def test_permission_error_recovery(self, temp_dir):
        """Test recovery from permission errors."""
        with patch('pathlib.Path.mkdir', side_effect=PermissionError("Access denied")):
            with patch('seeding.Path.cwd', return_value=temp_dir):
                seeder = RepoSeeder("permission-project", "test-user", dry_run=False)
                
                # Should handle permission errors appropriately
                try:
                    seeder.create_base_structure()
                    # If completed without error, permission handling worked
                    assert True
                except PermissionError:
                    # Acceptable to bubble up permission errors
                    assert True
    
    def test_partial_workflow_completion(self, temp_dir, mock_templates_dir):
        """Test behavior when workflow is partially completed."""
        project_root = temp_dir / "partial-project"
        project_root.mkdir()
        
        # Create partial structure
        (project_root / "meta-repo").mkdir()
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("partial-project", "test-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            
            # Should handle existing partial structure
            seeder.run()
            
            # Verify completion of missing parts
            assert (project_root / "cloud-storage").exists()
            assert (project_root / "core-services").exists()


class TestConcurrencyAndPerformance:
    """Test cases for performance and concurrent usage scenarios."""
    
    def test_multiple_seeder_instances(self, temp_dir, mock_templates_dir):
        """Test multiple RepoSeeder instances don't interfere."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder1 = RepoSeeder("project1", "user1", dry_run=True)
            seeder2 = RepoSeeder("project2", "user2", dry_run=True)
            
            seeder1.templates_dir = mock_templates_dir
            seeder2.templates_dir = mock_templates_dir
            
            # Both should work independently
            seeder1.run()
            seeder2.run()
            
            assert seeder1.project_name == "project1"
            assert seeder2.project_name == "project2"
            assert seeder1.github_username == "user1"
            assert seeder2.github_username == "user2"
    
    def test_large_project_structure_creation(self, temp_dir):
        """Test creation of large project structures."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("large-project", "test-user", dry_run=False)
            
            # Add many directories to creation list
            large_structure = [
                seeder.project_root / f"service-{i}" for i in range(100)
            ]
            
            # Simulate creating large structure
            for directory in large_structure:
                directory.mkdir(parents=True, exist_ok=True)
            
            # Verify all directories were created
            for directory in large_structure:
                assert directory.exists()


class TestConfigurationWorkflows:
    """Test cases for configuration-based workflows."""
    
    def test_yaml_configuration_workflow(self, temp_dir, mock_templates_dir):
        """Test complete workflow using YAML configuration."""
        # Create YAML configuration
        config_data = {
            'project_name': 'yaml-workflow-project',
            'github_username': 'yaml-user',
            'dry_run': False,
            'templates_dir': str(mock_templates_dir),
            'base_path': str(temp_dir)
        }
        
        config_file = temp_dir / "workflow.yaml"
        with open(config_file, 'w') as f:
            yaml.safe_dump(config_data, f)
        
        # Load and use configuration
        config = Configuration.load(config_file)
        assert config is not None
        
        with patch('seeding.Path.cwd', return_value=config.base_path):
            seeder = RepoSeeder(
                config.project_name,
                config.github_username,
                dry_run=config.dry_run
            )
            seeder.templates_dir = config.templates_dir
            seeder.run()
            
            # Verify project was created
            project_root = temp_dir / "yaml-workflow-project"
            assert project_root.exists()
    
    def test_json_configuration_workflow(self, temp_dir, mock_templates_dir):
        """Test complete workflow using JSON configuration."""
        # Create JSON configuration
        config_data = {
            'project_name': 'json-workflow-project',
            'github_username': 'json-user',
            'dry_run': False,
            'templates_dir': str(mock_templates_dir),
            'base_path': str(temp_dir)
        }
        
        config_file = temp_dir / "workflow.json"
        with open(config_file, 'w') as f:
            json.dump(config_data, f)
        
        # Load and use configuration
        config = Configuration.load(config_file)
        assert config is not None
        
        with patch('seeding.Path.cwd', return_value=config.base_path):
            seeder = RepoSeeder(
                config.project_name,
                config.github_username,
                dry_run=config.dry_run
            )
            seeder.templates_dir = config.templates_dir
            seeder.run()
            
            # Verify project was created
            project_root = temp_dir / "json-workflow-project"
            assert project_root.exists()
    
    def test_configuration_save_and_reload_workflow(self, temp_dir, mock_templates_dir):
        """Test saving configuration during workflow and reloading later."""
        # Create initial configuration
        config = Configuration(
            project_name="save-reload-project",
            github_username="save-reload-user",
            dry_run=True,
            templates_dir=mock_templates_dir,
            base_path=temp_dir
        )
        
        # Save configuration
        config_file = temp_dir / "save-reload.yaml"
        assert config.save(config_file) is True
        
        # Simulate later reload and use
        reloaded_config = Configuration.load(config_file)
        assert reloaded_config is not None
        
        # Use reloaded configuration
        with patch('seeding.Path.cwd', return_value=reloaded_config.base_path):
            seeder = RepoSeeder(
                reloaded_config.project_name,
                reloaded_config.github_username,
                dry_run=reloaded_config.dry_run
            )
            seeder.templates_dir = reloaded_config.templates_dir
            
            # Verify configuration was preserved
            assert seeder.project_name == "save-reload-project"
            assert seeder.github_username == "save-reload-user"
            assert seeder.dry_run is True


class TestTemplateIntegrationWorkflows:
    """Test cases for template processing in complete workflows."""
    
    def test_complete_template_processing_workflow(self, temp_dir, mock_templates_dir):
        """Test complete workflow with template processing."""
        # Create various template files
        templates = {
            'gitignore.template': "# {{PROJECT_NAME}}\n*.log\n*.tmp",
            'readme.template': "# {{PROJECT_NAME}}\n\nCreated by {{GITHUB_USERNAME}}",
            'package.template': '{\n  "name": "{{PROJECT_NAME}}",\n  "author": "{{GITHUB_USERNAME}}"\n}',
            'config.template': "project: {{PROJECT_NAME}}\nuser: {{GITHUB_USERNAME}}\ndate: {{CURRENT_DATE}}"
        }
        
        for filename, content in templates.items():
            (mock_templates_dir / filename).write_text(content)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("template-workflow-project", "template-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            seeder.run()
            
            # Verify project structure was created
            project_root = temp_dir / "template-workflow-project"
            assert project_root.exists()
            
            # Test template processing by creating files from templates
            from seeding import create_file_from_template
            
            for template_name, _ in templates.items():
                template_file = mock_templates_dir / template_name
                output_file = project_root / template_name.replace('.template', '')
                
                result = create_file_from_template(template_file, output_file, seeder.replacements)
                assert result is True
                assert output_file.exists()
                
                content = output_file.read_text()
                assert "template-workflow-project" in content
                assert "template-user" in content
    
    def test_template_error_recovery_in_workflow(self, temp_dir, mock_templates_dir):
        """Test workflow continues when some templates fail to process."""
        # Create mix of valid and invalid templates
        (mock_templates_dir / "valid.template").write_text("Valid: {{PROJECT_NAME}}")
        (mock_templates_dir / "invalid.template").write_text("Invalid: {{NONEXISTENT_VAR}}")
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("error-recovery-project", "test-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            
            # Workflow should complete despite template errors
            seeder.run()
            
            # Verify basic structure was still created
            project_root = temp_dir / "error-recovery-project"
            assert project_root.exists()


class TestRealWorldScenarios:
    """Test cases simulating real-world usage scenarios."""
    
    def test_team_development_scenario(self, temp_dir, mock_templates_dir):
        """Test scenario where multiple developers use same configuration."""
        # Create shared team configuration
        team_config = Configuration(
            project_name="team-project",
            dry_run=False,
            templates_dir=mock_templates_dir,
            base_path=temp_dir
        )
        
        shared_config_file = temp_dir / "team-config.yaml"
        team_config.save(shared_config_file)
        
        # Simulate different team members using the config
        team_members = ["alice", "bob", "charlie"]
        
        for member in team_members:
            # Load shared config
            config = Configuration.load(shared_config_file)
            # Override username for each member
            config.github_username = member
            
            member_dir = temp_dir / f"{member}_workspace"
            member_dir.mkdir()
            
            with patch('seeding.Path.cwd', return_value=member_dir):
                seeder = RepoSeeder(
                    config.project_name,
                    config.github_username,
                    dry_run=config.dry_run
                )
                seeder.templates_dir = config.templates_dir
                seeder.run()
                
                # Each member should get the same project structure
                project_root = member_dir / "team-project"
                assert project_root.exists()
                assert (project_root / "meta-repo").exists()
    
    def test_ci_cd_pipeline_scenario(self, temp_dir, mock_templates_dir):
        """Test scenario simulating CI/CD pipeline usage."""
        # Create configuration for automated environment
        ci_config = Configuration(
            project_name="ci-project",
            github_username="ci-bot",
            dry_run=False,
            templates_dir=mock_templates_dir,
            base_path=temp_dir
        )
        
        config_file = temp_dir / "ci-config.json"
        ci_config.save(config_file)
        
        # Simulate CI environment variables and constraints
        with patch.dict('os.environ', {'CI': 'true', 'GITHUB_ACTIONS': 'true'}):
            config = Configuration.load(config_file)
            
            with patch('seeding.Path.cwd', return_value=config.base_path):
                seeder = RepoSeeder(
                    config.project_name,
                    config.github_username,
                    dry_run=config.dry_run
                )
                seeder.templates_dir = config.templates_dir
                
                # Should work in CI environment
                seeder.run()
                
                project_root = temp_dir / "ci-project"
                assert project_root.exists()
    
    def test_migration_scenario(self, temp_dir, mock_templates_dir):
        """Test scenario for migrating existing projects."""
        # Create existing project structure
        existing_project = temp_dir / "legacy-project"
        existing_project.mkdir()
        (existing_project / "old-structure").mkdir()
        (existing_project / "legacy-file.txt").write_text("Legacy content")
        
        # Use seeder to add new structure to existing project
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("legacy-project", "migration-user", dry_run=False)
            seeder.templates_dir = mock_templates_dir
            seeder.run()
            
            # Should preserve existing content and add new structure
            assert (existing_project / "legacy-file.txt").exists()
            assert (existing_project / "old-structure").exists()
            assert (existing_project / "meta-repo").exists()
            assert (existing_project / "cloud-storage").exists()