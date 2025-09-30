"""
Tests for Audit Management System functionality.

Test-Driven Development for Audit Management System:
Comprehensive audit coordination and tracking system for multiple AI agents

This test file implements the TDD approach by defining failing tests FIRST,
before implementing the audit management and AI agent coordination functionality.
"""
import pytest
import os
import tempfile
import shutil
import json
import yaml
from pathlib import Path
from datetime import datetime
from seeding import RepoSeeder


class TestAuditManagementSystem:
    """Test audit management and AI agent coordination functionality."""

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

    def test_creates_audit_management_structure(self):
        """Test that audit management directory structure is created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Audit directories are created
        expected_dirs = [
            project_path / "meta-repo" / "audits",
            project_path / "meta-repo" / "audits" / "reports",
            project_path / "meta-repo" / "audits" / "templates",
            project_path / "meta-repo" / "audits" / "tracking",
            project_path / "meta-repo" / "audits" / "agents"
        ]
        
        for expected_dir in expected_dirs:
            assert expected_dir.exists(), f"Directory {expected_dir} should be created"
            assert expected_dir.is_dir(), f"{expected_dir} should be a directory"

    def test_creates_audit_registry_file(self):
        """Test that audit registry file is created for tracking audit status."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Audit registry exists
        registry_file = project_path / "meta-repo" / "audits" / "audit-registry.yaml"
        assert registry_file.exists(), "Audit registry should be created"
        
        # Should contain proper structure
        registry_content = yaml.safe_load(registry_file.read_text())
        assert 'audits' in registry_content, "Registry should have audits section"
        assert 'agents' in registry_content, "Registry should have agents section"
        assert 'metadata' in registry_content, "Registry should have metadata section"

    def test_creates_ai_agent_coordination_configs(self):
        """Test that AI agent coordination configurations are created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Agent configurations exist
        agents_dir = project_path / "meta-repo" / "audits" / "agents"
        expected_configs = [
            agents_dir / "security-agent.yaml",
            agents_dir / "code-quality-agent.yaml",
            agents_dir / "architecture-agent.yaml",
            agents_dir / "business-agent.yaml"
        ]
        
        for config_file in expected_configs:
            assert config_file.exists(), f"Agent config {config_file} should be created"
            
            # Should contain agent-specific configuration
            config_content = yaml.safe_load(config_file.read_text())
            assert 'agent_name' in config_content, "Agent config should have name"
            assert 'audit_domains' in config_content, "Agent config should specify domains"
            assert 'prompt_template' in config_content, "Agent config should have prompt template"

    def test_creates_audit_template_files(self):
        """Test that standardized audit templates are created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Audit templates exist
        templates_dir = project_path / "meta-repo" / "audits" / "templates"
        expected_templates = [
            templates_dir / "security-audit-template.md",
            templates_dir / "code-quality-audit-template.md",
            templates_dir / "architecture-audit-template.md",
            templates_dir / "business-audit-template.md",
            templates_dir / "comprehensive-audit-template.md"
        ]
        
        for template_file in expected_templates:
            assert template_file.exists(), f"Audit template {template_file} should be created"
            
            # Should contain template structure
            template_content = template_file.read_text()
            assert "## AUDIT SUMMARY" in template_content, "Template should have summary section"
            assert "## FINDINGS" in template_content, "Template should have findings section"
            assert "## RECOMMENDATIONS" in template_content, "Template should have recommendations"

    def test_creates_audit_automation_scripts(self):
        """Test that audit automation scripts are created."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Automation scripts exist
        scripts_dir = project_path / "meta-repo" / "scripts"
        expected_scripts = [
            scripts_dir / "audit-manager.py",
            scripts_dir / "audit-coordinator.py",
            scripts_dir / "audit-to-issues.py"
        ]
        
        for script_file in expected_scripts:
            assert script_file.exists(), f"Audit script {script_file} should be created"
            assert script_file.is_file(), f"{script_file} should be a file"
            
            # Should contain automation functionality
            script_content = script_file.read_text()
            assert "if __name__ == \"__main__\":" in script_content, "Script should be executable"

    def test_audit_registry_tracks_audit_lifecycle(self):
        """Test that audit registry properly tracks audit status and lifecycle."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Registry tracks audit lifecycle
        registry_file = project_path / "meta-repo" / "audits" / "audit-registry.yaml"
        registry_content = yaml.safe_load(registry_file.read_text())
        
        # Should have audit tracking structure
        assert 'audits' in registry_content
        audits = registry_content['audits']
        
        # Should include status tracking fields
        if len(audits) > 0:
            sample_audit = list(audits.values())[0]
            expected_fields = ['status', 'created_date', 'agent', 'findings_count', 'issues_created']
            for field in expected_fields:
                assert field in sample_audit, f"Audit entry should track {field}"

    def test_creates_github_issues_from_audit_findings(self):
        """Test that audit findings can be converted to GitHub issues."""
        # ARRANGE: Set up test project and audit system
        project_path = Path(self.test_dir) / "test-project"
        self.seeder.create_audit_management_system()
        
        # ACT: Test audit-to-issues conversion (simulated)
        scripts_dir = project_path / "meta-repo" / "scripts"
        audit_to_issues_script = scripts_dir / "audit-to-issues.py"
        
        # ASSERT: Script exists and has GitHub issue creation functionality
        script_content = audit_to_issues_script.read_text()
        assert "gh issue create" in script_content, "Script should create GitHub issues"
        assert "audit-finding" in script_content, "Script should handle audit findings"
        assert "--label" in script_content, "Script should apply appropriate labels"

    def test_audit_agent_coordination_system(self):
        """Test that multiple AI agents can be coordinated for different audit domains."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Agent coordination system exists
        coordinator_script = project_path / "meta-repo" / "scripts" / "audit-coordinator.py"
        coordinator_content = coordinator_script.read_text()
        
        # Should coordinate multiple agents
        assert "security-agent" in coordinator_content, "Should coordinate security agent"
        assert "code-quality-agent" in coordinator_content, "Should coordinate code quality agent"
        assert "architecture-agent" in coordinator_content, "Should coordinate architecture agent"
        assert "business-agent" in coordinator_content, "Should coordinate business agent"

    def test_audit_tracking_prevents_duplicates(self):
        """Test that audit tracking system prevents duplicate work."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Create audit management system
        self.seeder.create_audit_management_system()
        
        # ASSERT: Tracking system includes duplicate prevention
        tracking_dir = project_path / "meta-repo" / "audits" / "tracking"
        
        # Should have tracking mechanisms
        expected_tracking_files = [
            tracking_dir / "audit-history.json",
            tracking_dir / "implementation-status.yaml"
        ]
        
        for tracking_file in expected_tracking_files:
            assert tracking_file.exists(), f"Tracking file {tracking_file} should be created"

    def test_integration_with_existing_seeding_process(self):
        """Test that audit management integrates with main seeding process."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run full seeding process
        self.seeder.run()
        
        # ASSERT: Audit management is created as part of full seeding
        assert (project_path / "meta-repo" / "audits").exists()
        assert (project_path / "meta-repo" / "audits" / "audit-registry.yaml").exists()
        assert (project_path / "meta-repo" / "scripts" / "audit-manager.py").exists()
        
        # Should integrate with existing structure
        assert (project_path / "meta-repo" / ".github").exists()
        assert (project_path / "meta-repo" / "scripts").exists()

    def test_audit_system_is_idempotent(self):
        """Test that audit management creation is idempotent (safe to run multiple times)."""
        # ARRANGE: Set up test project
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run audit system creation twice
        self.seeder.create_audit_management_system()
        initial_files = list((project_path / "meta-repo" / "audits").rglob("*"))
        
        self.seeder.create_audit_management_system()  # Run again
        final_files = list((project_path / "meta-repo" / "audits").rglob("*"))
        
        # ASSERT: No duplicate files created, same structure maintained
        assert len(initial_files) == len(final_files), "Audit system creation should be idempotent"

    def test_dry_run_mode_respects_audit_system(self):
        """Test that dry-run mode doesn't create audit management files."""
        # ARRANGE: Set up test project with dry-run enabled
        self.seeder.dry_run = True
        project_path = Path(self.test_dir) / "test-project"
        
        # ACT: Run audit system creation in dry-run mode
        self.seeder.create_audit_management_system()
        
        # ASSERT: No files should be created in dry-run mode
        audit_registry = project_path / "meta-repo" / "audits" / "audit-registry.yaml"
        assert not audit_registry.exists(), "Dry-run should not create files"
