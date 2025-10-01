"""
Tests for Business Operations Automation

Tests the self-governing business operations automation system to ensure
it properly deploys and manages automation workflows, compliance enforcement,
self-healing capabilities, and governance integration.
"""

import asyncio
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch

# Import the module under test
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "automation"))
from business_operations import (
    BusinessOperationsManager, 
    BusinessOperationsConfig,
    BusinessProfile,
    AutomationLevel,
    deploy_business_operations_automation
)


class TestBusinessOperationsConfig:
    """Test business operations configuration."""
    
    def test_config_creation_with_defaults(self):
        """Test configuration creation with default values."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.STARTUP_BASIC,
            automation_level=AutomationLevel.STANDARD
        )
        
        assert config.business_profile == BusinessProfile.STARTUP_BASIC
        assert config.automation_level == AutomationLevel.STANDARD
        assert config.self_healing_enabled == True
        assert config.compliance_enforcement == True
        assert config.automated_reporting == True
        assert config.notification_channels == ['github-issues', 'workflow-logs']
        assert config.custom_policies == {}
    
    def test_config_creation_with_custom_values(self):
        """Test configuration creation with custom values."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.CHARITY_NONPROFIT,
            automation_level=AutomationLevel.CONSERVATIVE,
            self_healing_enabled=False,
            compliance_enforcement=True,
            notification_channels=['email', 'slack'],
            custom_policies={'transparency': True}
        )
        
        assert config.business_profile == BusinessProfile.CHARITY_NONPROFIT
        assert config.automation_level == AutomationLevel.CONSERVATIVE
        assert config.self_healing_enabled == False
        assert config.notification_channels == ['email', 'slack']
        assert config.custom_policies == {'transparency': True}


class TestBusinessOperationsManager:
    """Test business operations manager."""
    
    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return BusinessOperationsConfig(
            business_profile=BusinessProfile.STARTUP_BASIC,
            automation_level=AutomationLevel.STANDARD
        )
    
    @pytest.fixture
    def manager(self, config):
        """Create test manager."""
        return BusinessOperationsManager(config, dry_run=True)
    
    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)
    
    def test_manager_initialization(self, config):
        """Test manager initialization."""
        manager = BusinessOperationsManager(config, dry_run=True)
        
        assert manager.config == config
        assert manager.dry_run == True
        assert manager.templates_dir.exists()
    
    @pytest.mark.asyncio
    async def test_setup_automated_onboarding(self, manager, temp_dir):
        """Test automated onboarding setup."""
        result = await manager.setup_automated_onboarding(
            target_dir=temp_dir,
            org_name="test-org",
            repo_name="test-repo"
        )
        
        assert result['success'] == True
        assert 'workflows_created' in result
        assert 'governance_files' in result
        assert 'policies_applied' in result
        
        # Check that governance directory would be created
        assert len(result['governance_files']) > 0
    
    @pytest.mark.asyncio
    async def test_setup_compliance_enforcement(self, manager, temp_dir):
        """Test compliance enforcement setup."""
        result = await manager.setup_compliance_enforcement(temp_dir)
        
        assert result['success'] == True
        assert 'workflows_created' in result
        assert 'policies_created' in result
    
    @pytest.mark.asyncio
    async def test_setup_automated_reporting(self, manager, temp_dir):
        """Test automated reporting setup."""
        result = await manager.setup_automated_reporting(
            target_dir=temp_dir,
            org_name="test-org"
        )
        
        assert result['success'] == True
        assert 'workflows_created' in result
        assert 'reports_configured' in result
    
    @pytest.mark.asyncio 
    async def test_setup_self_healing(self, manager, temp_dir):
        """Test self-healing setup."""
        result = await manager.setup_self_healing(temp_dir)
        
        assert result['success'] == True
        assert 'workflows_created' in result
        assert 'remediation_rules' in result
    
    @pytest.mark.asyncio
    async def test_setup_governance_integration(self, manager, temp_dir):
        """Test governance integration setup."""
        result = await manager.setup_governance_integration(
            target_dir=temp_dir,
            org_name="test-org"
        )
        
        assert result['success'] == True
        assert 'governance_files' in result
        assert 'protection_rules' in result
        assert 'CODEOWNERS' in result['governance_files']
    
    @pytest.mark.asyncio
    async def test_deploy_complete_automation(self, manager, temp_dir):
        """Test complete automation deployment."""
        result = await manager.deploy_complete_automation(
            target_dir=temp_dir,
            org_name="test-org", 
            repo_name="test-repo"
        )
        
        assert 'business_profile' in result
        assert 'automation_level' in result
        assert 'components_deployed' in result
        assert 'overall_success' in result
        assert 'deployment_summary' in result
        
        # Check that all expected components are deployed
        expected_components = [
            'automated_onboarding',
            'compliance_enforcement', 
            'automated_reporting',
            'governance_integration',
            'self_healing'
        ]
        
        for component in expected_components:
            assert component in result['components_deployed']


class TestBusinessProfileSpecificBehavior:
    """Test business profile-specific behavior."""
    
    @pytest.mark.asyncio
    async def test_charity_nonprofit_profile(self):
        """Test charity nonprofit profile-specific features."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.CHARITY_NONPROFIT,
            automation_level=AutomationLevel.STANDARD
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            result = await manager.deploy_complete_automation(
                target_dir=temp_path,
                org_name="charity-org",
                repo_name="charity-repo"
            )
            
            assert result['business_profile'] == 'charity-nonprofit'
            
            # Charity-specific features should be included
            # This would be verified by checking the actual file contents
            # in a more comprehensive test
    
    @pytest.mark.asyncio
    async def test_consulting_firm_profile(self):
        """Test consulting firm profile-specific features."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.CONSULTING_FIRM,
            automation_level=AutomationLevel.AGGRESSIVE
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            result = await manager.deploy_complete_automation(
                target_dir=temp_path,
                org_name="consulting-org",
                repo_name="consulting-repo"
            )
            
            assert result['business_profile'] == 'consulting-firm'
            assert result['automation_level'] == 'aggressive'


class TestAutomationLevels:
    """Test different automation levels."""
    
    @pytest.mark.parametrize("automation_level,expected_features", [
        (AutomationLevel.CONSERVATIVE, {'self_healing': True, 'aggressive_updates': False}),
        (AutomationLevel.STANDARD, {'self_healing': True, 'balanced_approach': True}),
        (AutomationLevel.AGGRESSIVE, {'self_healing': True, 'maximum_automation': True}),
    ])
    @pytest.mark.asyncio
    async def test_automation_levels(self, automation_level, expected_features):
        """Test different automation levels produce appropriate configurations."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.SMB_STANDARD,
            automation_level=automation_level
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            result = await manager.deploy_complete_automation(
                target_dir=temp_path,
                org_name="smb-org",
                repo_name="smb-repo"
            )
            
            assert result['automation_level'] == automation_level.value
            # More specific assertions would check the actual configuration files


class TestConvenienceFunction:
    """Test the convenience deployment function."""
    
    @pytest.mark.asyncio
    async def test_deploy_business_operations_automation(self):
        """Test the convenience deployment function."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            result = await deploy_business_operations_automation(
                target_dir=temp_path,
                org_name="test-org",
                repo_name="test-repo", 
                business_profile="startup-basic",
                automation_level="standard",
                dry_run=True
            )
            
            assert 'overall_success' in result
            assert 'deployment_summary' in result
            assert result['business_profile'] == 'startup-basic'
            assert result['automation_level'] == 'standard'
    
    @pytest.mark.asyncio
    async def test_deploy_with_invalid_profile(self):
        """Test deployment with invalid business profile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            with pytest.raises(ValueError):
                await deploy_business_operations_automation(
                    target_dir=temp_path,
                    org_name="test-org",
                    repo_name="test-repo",
                    business_profile="invalid-profile",
                    automation_level="standard",
                    dry_run=True
                )


class TestFileGeneration:
    """Test file generation capabilities."""
    
    def test_codeowners_generation(self):
        """Test CODEOWNERS file generation."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.STARTUP_BASIC,
            automation_level=AutomationLevel.STANDARD
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        codeowners_content = manager._generate_codeowners("test-org")
        
        assert "test-org" in codeowners_content
        assert "core-team" in codeowners_content
        assert "/governance/" in codeowners_content
        assert "/compliance/" in codeowners_content
    
    def test_branch_protection_config_generation(self):
        """Test branch protection configuration generation."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.CONSULTING_FIRM,
            automation_level=AutomationLevel.STANDARD
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        protection_config = manager._generate_branch_protection_config()
        
        assert 'main' in protection_config
        assert protection_config['main']['enforce_admins'] == True  # Consulting firm specific
        assert 'client-data-protection' in protection_config['main']['required_status_checks']['contexts']
    
    def test_compliance_framework_generation(self):
        """Test compliance framework document generation."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.CHARITY_NONPROFIT,
            automation_level=AutomationLevel.STANDARD
        )
        manager = BusinessOperationsManager(config, dry_run=True)
        
        framework_content = manager._generate_compliance_framework()
        
        assert "charity-nonprofit" in framework_content
        assert "Compliance Framework" in framework_content
        assert "standard" in framework_content


class TestErrorHandling:
    """Test error handling and resilience."""
    
    @pytest.mark.asyncio
    async def test_deployment_with_template_missing(self):
        """Test deployment behavior when templates are missing."""
        config = BusinessOperationsConfig(
            business_profile=BusinessProfile.STARTUP_BASIC,
            automation_level=AutomationLevel.STANDARD
        )
        
        # Mock the templates directory to not exist
        with patch.object(Path, 'exists', return_value=False):
            manager = BusinessOperationsManager(config, dry_run=True)
            
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                result = await manager.setup_automated_onboarding(
                    target_dir=temp_path,
                    org_name="test-org",
                    repo_name="test-repo"
                )
                
                # Should still succeed but with limited functionality
                assert result['success'] == True


class TestIntegrationScenarios:
    """Test integration scenarios and workflows."""
    
    @pytest.mark.asyncio
    async def test_full_startup_onboarding_scenario(self):
        """Test complete startup onboarding scenario."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Deploy automation
            result = await deploy_business_operations_automation(
                target_dir=temp_path,
                org_name="startup-inc",
                repo_name="awesome-product",
                business_profile="startup-basic",
                automation_level="standard",
                dry_run=True
            )
            
            assert result['overall_success'] == True
            assert result['business_profile'] == 'startup-basic'
            
            # Verify expected components are present
            summary = result['deployment_summary']
            assert summary['successful_components'] > 0
            assert summary['workflows_created'] > 0
            assert summary['policies_applied'] > 0
            assert summary['governance_files'] > 0
    
    @pytest.mark.asyncio
    async def test_charity_transparency_scenario(self):
        """Test charity organization with transparency requirements."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            result = await deploy_business_operations_automation(
                target_dir=temp_path,
                org_name="helping-hands-charity",
                repo_name="impact-tracker",
                business_profile="charity-nonprofit",
                automation_level="standard",
                dry_run=True
            )
            
            assert result['overall_success'] == True
            assert result['business_profile'] == 'charity-nonprofit'
            
            # Charity-specific validations would go here
            # e.g., transparency policy files, donor privacy measures, etc.


if __name__ == "__main__":
    # Run specific tests for development
    pytest.main([__file__, "-v"])
