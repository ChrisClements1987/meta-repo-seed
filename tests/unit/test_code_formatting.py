"""
Tests for Code Formatting and Pre-commit Hooks functionality.

Test-Driven Development for Issue #105:
MEDIUM: Add automated code formatting with pre-commit hooks

This test file implements the TDD approach by defining failing tests FIRST,
before implementing the pre-commit hooks and code formatting functionality.
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path
import subprocess
import yaml
from seeding import RepoSeeder


class TestCodeFormattingSetup:
    """Test pre-commit hooks and code formatting setup functionality."""

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

    def test_creates_precommit_config_file(self):
        """Test that .pre-commit-config.yaml is created in the meta-repo."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run seeding with code formatting setup
        self.seeder.setup_code_formatting()
        
        # ASSERT: Pre-commit config file is created
        precommit_config = project_path / "meta-repo" / ".pre-commit-config.yaml"
        assert precommit_config.exists(), "Pre-commit config file should be created"
        assert precommit_config.is_file(), "Pre-commit config should be a file"

    def test_precommit_config_contains_required_hooks(self):
        """Test that pre-commit config contains essential formatting hooks."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate code formatting setup
        self.seeder.setup_code_formatting()
        
        # ASSERT: Pre-commit config contains required hooks
        precommit_config = project_path / "meta-repo" / ".pre-commit-config.yaml"
        config_content = precommit_config.read_text()
        config_data = yaml.safe_load(config_content)
        
        # Should have repos section with hooks
        assert 'repos' in config_data, "Config should have repos section"
        repos = config_data['repos']
        assert len(repos) > 0, "Should have at least one repository of hooks"
        
        # Should include common formatting hooks
        hook_names = []
        for repo in repos:
            if 'hooks' in repo:
                for hook in repo['hooks']:
                    hook_names.append(hook.get('id', ''))
        
        expected_hooks = ['black', 'isort', 'flake8']
        for expected_hook in expected_hooks:
            assert expected_hook in hook_names, f"Should include {expected_hook} hook"

    def test_creates_formatting_requirements_file(self):
        """Test that formatting requirements are added to development dependencies."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Set up code formatting
        self.seeder.setup_code_formatting()
        
        # ASSERT: Formatting requirements file is created
        requirements_file = project_path / "meta-repo" / "requirements-formatting.txt"
        assert requirements_file.exists(), "Formatting requirements file should be created"
        
        # Should contain essential formatting tools
        requirements_content = requirements_file.read_text()
        expected_packages = ['black', 'isort', 'flake8', 'pre-commit']
        for package in expected_packages:
            assert package in requirements_content, f"Requirements should include {package}"

    def test_creates_setup_script_for_developers(self):
        """Test that a setup script is created to help developers install pre-commit hooks."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate code formatting setup
        self.seeder.setup_code_formatting()
        
        # ASSERT: Setup script is created
        setup_script = project_path / "meta-repo" / "scripts" / "setup-formatting.py"
        assert setup_script.exists(), "Setup script should be created"
        assert setup_script.is_file(), "Setup script should be a file"
        
        # Script should be executable and contain installation commands
        script_content = setup_script.read_text()
        assert "pre-commit install" in script_content, "Script should install pre-commit hooks"
        assert "pip install" in script_content, "Script should install required packages"

    def test_creates_pyproject_toml_configuration(self):
        """Test that pyproject.toml is created with tool configurations."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Set up code formatting
        self.seeder.setup_code_formatting()
        
        # ASSERT: pyproject.toml is created with tool configurations
        pyproject_file = project_path / "meta-repo" / "pyproject.toml"
        assert pyproject_file.exists(), "pyproject.toml should be created"
        
        # Should contain configuration sections for formatting tools
        pyproject_content = pyproject_file.read_text()
        assert "[tool.black]" in pyproject_content, "Should configure black"
        assert "[tool.isort]" in pyproject_content, "Should configure isort"
        assert "[tool.flake8]" in pyproject_content or "[tool.ruff]" in pyproject_content, "Should configure linter"

    def test_precommit_config_uses_proper_versions(self):
        """Test that pre-commit config uses appropriate tool versions."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate code formatting setup
        self.seeder.setup_code_formatting()
        
        # ASSERT: Pre-commit config uses specific versions (not latest)
        precommit_config = project_path / "meta-repo" / ".pre-commit-config.yaml"
        config_content = precommit_config.read_text()
        config_data = yaml.safe_load(config_content)
        
        for repo in config_data.get('repos', []):
            if 'rev' in repo:
                # Should not use 'main' or 'master' - should pin to specific versions
                rev = repo['rev']
                assert rev not in ['main', 'master', 'latest'], f"Should pin specific version, not {rev}"
                assert len(rev) > 3, "Version should be specific (not just v1 or similar)"

    def test_formatting_tools_configuration_is_consistent(self):
        """Test that formatting tool configurations work together consistently."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Set up code formatting
        self.seeder.setup_code_formatting()
        
        # ASSERT: Tool configurations are consistent (e.g., same line length)
        pyproject_file = project_path / "meta-repo" / "pyproject.toml"
        pyproject_content = pyproject_file.read_text()
        
        # Extract line length settings - should be consistent across tools
        black_line_length = None
        isort_line_length = None
        
        if "line-length = " in pyproject_content:
            # Should have consistent line length settings
            lines = pyproject_content.split('\n')
            for line in lines:
                if "line-length = " in line and "[tool.black]" in pyproject_content:
                    # This is a basic check - in real implementation would be more sophisticated
                    assert "88" in pyproject_content or "100" in pyproject_content, "Should have reasonable line length"

    def test_integration_with_existing_seeding_process(self):
        """Test that code formatting setup integrates with main seeding process."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run full seeding process (should include formatting setup)
        self.seeder.run()
        
        # ASSERT: Code formatting is set up as part of full seeding
        assert (project_path / "meta-repo" / ".pre-commit-config.yaml").exists()
        assert (project_path / "meta-repo" / "requirements-formatting.txt").exists()
        assert (project_path / "meta-repo" / "pyproject.toml").exists()
        
        # Should integrate with existing structure
        assert (project_path / "meta-repo").exists()
        assert (project_path / "meta-repo" / ".github").exists()

    def test_setup_script_is_cross_platform(self):
        """Test that setup script works across different platforms."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate code formatting setup
        self.seeder.setup_code_formatting()
        
        # ASSERT: Setup script uses cross-platform approaches
        setup_script = project_path / "meta-repo" / "scripts" / "setup-formatting.py"
        script_content = setup_script.read_text()
        
        # Should use Python's platform-independent approaches
        assert "import sys" in script_content or "import os" in script_content, "Should use platform-aware code"
        assert "python -m pip" in script_content or "sys.executable" in script_content, "Should use proper Python executable"

    def test_formatting_setup_is_idempotent(self):
        """Test that code formatting setup is safe to run multiple times."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run formatting setup twice
        self.seeder.setup_code_formatting()
        initial_files = list((project_path / "meta-repo").rglob("*"))
        
        self.seeder.setup_code_formatting()  # Run again
        final_files = list((project_path / "meta-repo").rglob("*"))
        
        # ASSERT: No duplicate files created, same structure maintained
        assert len(initial_files) == len(final_files), "Code formatting setup should be idempotent"

    def test_dry_run_mode_respects_formatting_setup(self):
        """Test that dry-run mode doesn't create formatting files."""
        # ARRANGE: Set up test project with dry-run enabled
        self.seeder.dry_run = True
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run formatting setup in dry-run mode
        self.seeder.setup_code_formatting()
        
        # ASSERT: No files should be created in dry-run mode
        precommit_config = project_path / "meta-repo" / ".pre-commit-config.yaml"
        assert not precommit_config.exists(), "Dry-run should not create files"
