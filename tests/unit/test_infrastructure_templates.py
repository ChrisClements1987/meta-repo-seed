"""
Tests for Infrastructure as Code template generation.

Test-Driven Development for Issue #97:
CRITICAL: Add Infrastructure as Code templates for true 10-minute deployment

This test file implements the TDD approach by defining failing tests FIRST,
before implementing the Infrastructure as Code functionality.
"""
import pytest
import os
import tempfile
import shutil
from pathlib import Path
from seeding import RepoSeeder


class TestInfrastructureTemplates:
    """Test Infrastructure as Code template generation functionality."""

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

    def test_creates_infrastructure_directory_structure(self):
        """Test that Infrastructure as Code directory structure is created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run seeding with infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Infrastructure directories are created
        expected_dirs = [
            project_path / "meta-repo" / "infrastructure",
            project_path / "meta-repo" / "infrastructure" / "terraform",
            project_path / "meta-repo" / "infrastructure" / "kubernetes",
            project_path / "meta-repo" / "infrastructure" / "docker",
            project_path / "meta-repo" / "infrastructure" / "environments",
        ]
        
        for expected_dir in expected_dirs:
            assert expected_dir.exists(), f"Directory {expected_dir} should be created"
            assert expected_dir.is_dir(), f"{expected_dir} should be a directory"

    def test_creates_terraform_provider_templates(self):
        """Test that Terraform provider-specific templates are generated."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Terraform provider templates exist
        terraform_path = project_path / "meta-repo" / "infrastructure" / "terraform"
        expected_files = [
            terraform_path / "main.tf",
            terraform_path / "variables.tf", 
            terraform_path / "outputs.tf",
            terraform_path / "providers.tf",
            terraform_path / "aws" / "main.tf",
            terraform_path / "azure" / "main.tf",
            terraform_path / "gcp" / "main.tf",
        ]
        
        for expected_file in expected_files:
            assert expected_file.exists(), f"Terraform template {expected_file} should be created"
            assert expected_file.is_file(), f"{expected_file} should be a file"

    def test_creates_kubernetes_manifest_templates(self):
        """Test that Kubernetes manifest templates are generated."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Kubernetes manifests exist
        k8s_path = project_path / "meta-repo" / "infrastructure" / "kubernetes"
        expected_files = [
            k8s_path / "namespace.yaml",
            k8s_path / "deployment.yaml",
            k8s_path / "service.yaml",
            k8s_path / "ingress.yaml",
            k8s_path / "configmap.yaml",
            k8s_path / "secret.yaml",
        ]
        
        for expected_file in expected_files:
            assert expected_file.exists(), f"Kubernetes template {expected_file} should be created"
            assert expected_file.is_file(), f"{expected_file} should be a file"

    def test_creates_docker_templates(self):
        """Test that Docker containerization templates are generated."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Docker templates exist
        docker_path = project_path / "meta-repo" / "infrastructure" / "docker"
        expected_files = [
            docker_path / "Dockerfile.template",
            docker_path / "docker-compose.yml",
            docker_path / "docker-compose.prod.yml",
            docker_path / ".dockerignore",
        ]
        
        for expected_file in expected_files:
            assert expected_file.exists(), f"Docker template {expected_file} should be created"
            assert expected_file.is_file(), f"{expected_file} should be a file"

    def test_creates_environment_specific_configs(self):
        """Test that environment-specific configuration files are generated."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Environment configs exist
        env_path = project_path / "meta-repo" / "infrastructure" / "environments"
        expected_dirs = [
            env_path / "dev",
            env_path / "staging", 
            env_path / "production",
        ]
        
        for env_dir in expected_dirs:
            assert env_dir.exists(), f"Environment directory {env_dir} should be created"
            # Each environment should have terraform and kubernetes configs
            assert (env_dir / "terraform.tfvars").exists()
            assert (env_dir / "kubernetes.yaml").exists()

    def test_template_variable_replacement(self):
        """Test that Infrastructure templates properly replace project variables."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Templates contain replaced variables
        main_tf = project_path / "meta-repo" / "infrastructure" / "terraform" / "main.tf"
        content = main_tf.read_text()
        
        # Should contain project-specific values, not template variables
        assert "test-project" in content, "Project name should be replaced in terraform templates"
        assert "testuser" in content, "GitHub username should be replaced in terraform templates"
        assert "{{PROJECT_NAME}}" not in content, "Template variables should be replaced"
        assert "{{GITHUB_USERNAME}}" not in content, "Template variables should be replaced"

    def test_infrastructure_templates_integration_with_main_seeding(self):
        """Test that infrastructure templates integrate with main seeding process."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run full seeding process
        self.seeder.run()
        
        # ASSERT: Infrastructure is created as part of full seeding
        assert (project_path / "meta-repo" / "infrastructure").exists()
        
        # ASSERT: Infrastructure templates are integrated with other templates
        assert (project_path / "meta-repo").exists()
        assert (project_path / "meta-repo" / ".github").exists()
        assert (project_path / "meta-repo" / "infrastructure").exists()

    def test_infrastructure_templates_idempotent(self):
        """Test that infrastructure template creation is idempotent (safe to run multiple times)."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run infrastructure template creation twice
        self.seeder.create_infrastructure_templates()
        initial_file_count = len(list((project_path / "meta-repo" / "infrastructure").rglob("*")))
        
        self.seeder.create_infrastructure_templates()  # Run again
        final_file_count = len(list((project_path / "meta-repo" / "infrastructure").rglob("*")))
        
        # ASSERT: No duplicate files created, same structure maintained
        assert initial_file_count == final_file_count, "Infrastructure template creation should be idempotent"

    def test_cross_platform_infrastructure_templates(self):
        """Test that infrastructure templates work across different platforms."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Generate infrastructure templates
        self.seeder.create_infrastructure_templates()
        
        # ASSERT: Infrastructure templates use cross-platform paths
        terraform_main = project_path / "meta-repo" / "infrastructure" / "terraform" / "main.tf"
        assert terraform_main.exists(), "Infrastructure templates should use cross-platform Path objects"
        
        # File should be readable across platforms
        content = terraform_main.read_text()
        assert len(content) > 0, "Infrastructure template content should be generated correctly"
