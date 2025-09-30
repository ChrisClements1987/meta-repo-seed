"""
Tests for GitHub Repository Settings as Code functionality.

Test-Driven Development for Issue #100:
HIGH: Add GitHub Repository Settings as Code for automated governance

This test file implements the TDD approach by defining failing tests FIRST,
before implementing the GitHub repository settings automation functionality.
"""
import pytest
import os
import tempfile
import shutil
import json
from pathlib import Path
from seeding import RepoSeeder


class TestGitHubRepositorySettings:
    """Test GitHub Repository Settings as Code functionality."""

    def setup_method(self):
        """Set up test environment for each test."""
        self.test_dir = tempfile.mkdtemp()
        self.seeder = RepoSeeder(
            project_name="test-project",
            github_username="testuser",
            dry_run=False
        )
        # Override base_path to use our test directory
        self.seeder.base_path = Path(self.test_dir)
        self.seeder.project_root = self.seeder.base_path / "test-project"
        self.seeder.meta_repo_path = self.seeder.project_root / 'meta-repo'

    def teardown_method(self):
        """Clean up test environment after each test."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_creates_repository_settings_config(self):
        """Test that repository settings configuration file is created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run seeding with GitHub settings automation
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Repository settings config file is created
        settings_config = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        assert settings_config.exists(), "Repository settings config should be created"
        assert settings_config.is_file(), "Repository settings should be a file"

    def test_repository_settings_contains_required_sections(self):
        """Test that repository settings contain essential governance configurations."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Settings contain required sections
        settings_file = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        settings_content = settings_file.read_text()
        
        # Should include key governance settings
        required_sections = [
            'name:',
            'description:',
            'homepage:',
            'private:',
            'has_issues:',
            'has_projects:',
            'has_wiki:',
            'default_branch:',
            'delete_branch_on_merge:',
            'allow_squash_merge:',
            'allow_merge_commit:',
            'allow_rebase_merge:'
        ]
        
        for section in required_sections:
            assert section in settings_content, f"Settings should include {section}"

    def test_creates_branch_protection_rules(self):
        """Test that branch protection rules are configured."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Branch protection configuration exists
        settings_file = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        settings_content = settings_file.read_text()
        
        # Should include branch protection rules
        protection_keywords = [
            'branches:',
            'protection:',
            'required_status_checks:',
            'enforce_admins:',
            'required_pull_request_reviews:',
            'dismiss_stale_reviews:',
            'require_code_owner_reviews:'
        ]
        
        for keyword in protection_keywords:
            assert keyword in settings_content, f"Should include branch protection: {keyword}"

    def test_creates_repository_labels_config(self):
        """Test that standardized repository labels are configured."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Labels configuration exists
        labels_file = project_path / "meta-repo" / ".github" / "labels.yml"
        assert labels_file.exists(), "Labels configuration should be created"
        
        # Should contain standard labels
        labels_content = labels_file.read_text()
        expected_labels = [
            'priority: high',
            'priority: medium', 
            'priority: low',
            'effort: small',
            'effort: medium',
            'effort: large',
            'infrastructure',
            'operations',
            'business-operations'
        ]
        
        for label in expected_labels:
            assert label in labels_content, f"Should include label: {label}"

    def test_creates_github_settings_automation_script(self):
        """Test that automation script for applying settings is created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Automation script is created
        automation_script = project_path / "meta-repo" / "scripts" / "apply-github-settings.py"
        assert automation_script.exists(), "GitHub settings automation script should be created"
        assert automation_script.is_file(), "Automation script should be a file"
        
        # Script should contain GitHub CLI commands
        script_content = automation_script.read_text()
        assert "gh repo edit" in script_content, "Script should use GitHub CLI for repository settings"
        assert "gh api" in script_content, "Script should use GitHub API for advanced settings"

    def test_repository_settings_use_template_variables(self):
        """Test that repository settings properly replace project variables."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Settings contain replaced variables
        settings_file = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        settings_content = settings_file.read_text()
        
        # Should contain project-specific values, not template variables
        assert "test-project" in settings_content, "Project name should be replaced"
        assert "testuser" in settings_content, "GitHub username should be replaced"
        assert "{{PROJECT_NAME}}" not in settings_content, "Template variables should be replaced"
        assert "{{GITHUB_USERNAME}}" not in settings_content, "Template variables should be replaced"

    def test_creates_github_workflow_for_settings_automation(self):
        """Test that GitHub Actions workflow is created for automated settings application."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: GitHub Actions workflow exists
        workflow_file = project_path / "meta-repo" / ".github" / "workflows" / "repository-settings.yml"
        assert workflow_file.exists(), "Repository settings workflow should be created"
        
        # Workflow should automate settings application
        workflow_content = workflow_file.read_text()
        assert "repository-settings" in workflow_content, "Workflow should handle repository settings"
        assert "gh" in workflow_content, "Workflow should use GitHub CLI"

    def test_settings_include_security_configurations(self):
        """Test that repository settings include security best practices."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate GitHub settings
        self.seeder.create_github_repository_settings()
        
        # ASSERT: Security settings are configured
        settings_file = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        settings_content = settings_file.read_text()
        
        # Should include security-focused settings
        security_settings = [
            'allow_force_pushes: false',
            'allow_deletions: false',
            'required_status_checks',
            'enforce_admins: true',
            'required_pull_request_reviews'
        ]
        
        for setting in security_settings:
            assert setting in settings_content, f"Should include security setting: {setting}"

    def test_integration_with_existing_seeding_process(self):
        """Test that GitHub settings integrate with main seeding process."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run full seeding process
        self.seeder.run()
        
        # ASSERT: GitHub settings are created as part of full seeding
        assert (project_path / "meta-repo" / ".github" / "repository-settings.yml").exists()
        assert (project_path / "meta-repo" / ".github" / "labels.yml").exists()
        assert (project_path / "meta-repo" / "scripts" / "apply-github-settings.py").exists()
        
        # Should integrate with existing GitHub structure
        assert (project_path / "meta-repo" / ".github").exists()
        assert (project_path / "meta-repo" / ".github" / "workflows").exists()

    def test_github_settings_are_idempotent(self):
        """Test that GitHub settings creation is idempotent (safe to run multiple times)."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run GitHub settings creation twice
        self.seeder.create_github_repository_settings()
        initial_files = list((project_path / "meta-repo" / ".github").rglob("*"))
        
        self.seeder.create_github_repository_settings()  # Run again
        final_files = list((project_path / "meta-repo" / ".github").rglob("*"))
        
        # ASSERT: No duplicate files created, same structure maintained
        assert len(initial_files) == len(final_files), "GitHub settings creation should be idempotent"

    def test_dry_run_mode_respects_github_settings(self):
        """Test that dry-run mode doesn't create GitHub settings files."""
        # ARRANGE: Set up test project with dry-run enabled
        self.seeder.dry_run = True
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run GitHub settings creation in dry-run mode
        self.seeder.create_github_repository_settings()
        
        # ASSERT: No files should be created in dry-run mode
        settings_file = project_path / "meta-repo" / ".github" / "repository-settings.yml"
        assert not settings_file.exists(), "Dry-run should not create files"
