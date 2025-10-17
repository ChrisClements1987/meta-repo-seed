"""
Tests for OrganizationSeeder validation and cloud storage functionality.

This module tests the production-ready validation and cloud storage implementation
that replaces the placeholder approach with proper error handling and real functionality.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

from src.commercial.services.organization_seeder import OrganizationSeeder, OrganizationConfig
from src.commercial.models import (
    Customer, Organization, CustomerSettings, SubscriptionPlan, 
    OrganizationStatus, CustomerStatus
)


class TestOrganizationSeederValidation:
    """Test pre-flight validation functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.temp_dir) / "templates"
        self.templates_dir.mkdir(parents=True)
        
        # Create essential templates
        (self.templates_dir / "gitignore.template").write_text("# Git ignore template")
        (self.templates_dir / "github" / "workflows").mkdir(parents=True)
        (self.templates_dir / "github" / "workflows" / "ci.yml.template").write_text("# CI template")
        (self.templates_dir / "github" / "workflows" / "readme-docs.yml.template").write_text("# Docs template")
        
        # Create test customer and organization
        self.customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.STARTUP,
            settings=CustomerSettings(
                plan=SubscriptionPlan.STARTUP,
                max_products=1,
                max_team_members=5,
                features_enabled=["basic_templates"]
            )
        )
        
        self.organization = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
            github_username="testuser"
        )
        
        self.seeder = OrganizationSeeder(
            org_id="test-org-123",
            customer=self.customer,
            organization=self.organization,
            dry_run=True,
            config_data={}
        )
        
        # Override templates directory for testing
        self.seeder.config.templates_dir = self.templates_dir

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_preflight_validate_success(self):
        """Test successful pre-flight validation."""
        result = self.seeder._preflight_validate()
        assert result is True

    def test_preflight_validate_customer_none(self):
        """Test validation failure when customer is None."""
        self.seeder.customer = None
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_customer_email_missing(self):
        """Test validation failure when customer email is missing."""
        self.seeder.customer.email = ""
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_customer_plan_missing(self):
        """Test validation failure when customer plan is missing."""
        self.seeder.customer.plan = None
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_customer_settings_missing(self):
        """Test validation failure when customer settings are missing."""
        self.seeder.customer.settings = None
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_organization_none(self):
        """Test validation failure when organization is None."""
        self.seeder.organization = None
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_organization_name_missing(self):
        """Test validation failure when organization name is missing."""
        self.seeder.organization.name = ""
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_org_id_missing(self):
        """Test validation failure when org_id is missing."""
        self.seeder.org_id = ""
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_templates_missing(self):
        """Test validation failure when templates directory is missing."""
        self.seeder.config.templates_dir = None
        result = self.seeder._preflight_validate()
        assert result is False

    def test_preflight_validate_cloud_path_permission_error(self):
        """Test validation failure when cloud path has permission issues."""
        # On Windows, we'll simulate a permission error differently
        import platform
        
        if platform.system() == "Windows":
            # On Windows, use a path that doesn't exist and can't be created
            invalid_path = Path("Z:/invalid/path/that/cannot/be/created")
            self.seeder.config.cloud_storage_path = invalid_path
            self.seeder.dry_run = False
            
            result = self.seeder._preflight_validate()
            assert result is False
        else:
            # On Unix systems, create a read-only directory
            read_only_dir = Path(self.temp_dir) / "readonly"
            read_only_dir.mkdir()
            read_only_dir.chmod(0o444)  # Read-only
            
            self.seeder.config.cloud_storage_path = read_only_dir
            self.seeder.dry_run = False
            
            result = self.seeder._preflight_validate()
            assert result is False
            
            # Clean up
            read_only_dir.chmod(0o755)

    def test_validate_customer_settings_success(self):
        """Test successful customer settings validation."""
        result = self.seeder._validate_customer_settings()
        assert result is True

    def test_validate_customer_settings_company_name_missing_warning(self):
        """Test customer settings validation with missing company name (warning only)."""
        self.seeder.customer.company_name = ""
        result = self.seeder._validate_customer_settings()
        assert result is True  # Should pass with warning

    def test_validate_cloud_config_success(self):
        """Test successful cloud configuration validation."""
        result = self.seeder._validate_cloud_config()
        assert result is True

    def test_validate_cloud_config_path_none(self):
        """Test cloud configuration validation failure when path is None."""
        self.seeder.config.cloud_storage_path = None
        result = self.seeder._validate_cloud_config()
        assert result is False

    def test_validate_templates_success(self):
        """Test successful template validation."""
        result = self.seeder._validate_templates()
        assert result is True

    def test_validate_templates_directory_missing(self):
        """Test template validation failure when directory is missing."""
        self.seeder.config.templates_dir = Path("/nonexistent/path")
        result = self.seeder._validate_templates()
        assert result is False

    def test_validate_organization_data_success(self):
        """Test successful organization data validation."""
        result = self.seeder._validate_organization_data()
        assert result is True

    def test_validate_organization_data_github_username_missing_warning(self):
        """Test organization data validation with missing GitHub username (warning only)."""
        self.seeder.organization.github_username = ""
        result = self.seeder._validate_organization_data()
        assert result is True  # Should pass with warning


class TestOrganizationSeederCloudStorage:
    """Test cloud storage functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.temp_dir) / "templates"
        self.templates_dir.mkdir(parents=True)
        
        # Create test customer and organization
        self.customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.STARTUP,
            settings=CustomerSettings(
                plan=SubscriptionPlan.STARTUP,
                max_products=1,
                max_team_members=5,
                features_enabled=["basic_templates"]
            )
        )
        
        self.organization = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
            github_username="testuser"
        )
        
        self.seeder = OrganizationSeeder(
            org_id="test-org-123",
            customer=self.customer,
            organization=self.organization,
            dry_run=False,
            config_data={}
        )
        
        # Override paths for testing
        self.seeder.config.cloud_storage_path = Path(self.temp_dir) / "cloud-storage"
        self.seeder.config.org_base_path = Path(self.temp_dir) / "organizations" / "test-org-123"

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_setup_cloud_storage_success(self):
        """Test successful cloud storage setup."""
        result = self.seeder._setup_cloud_storage()
        assert result is True
        
        # Check that directories were created
        cloud_path = self.seeder.config.cloud_storage_path
        assert cloud_path.exists()
        assert (cloud_path / "strategy").exists()
        assert (cloud_path / "workspace").exists()
        assert (cloud_path / "archives").exists()
        assert (cloud_path / "templates").exists()

    def test_setup_cloud_storage_dry_run(self):
        """Test cloud storage setup in dry run mode."""
        self.seeder.dry_run = True
        result = self.seeder._setup_cloud_storage()
        assert result is True
        
        # Check that directories were NOT created in dry run
        cloud_path = self.seeder.config.cloud_storage_path
        assert not cloud_path.exists()

    def test_setup_cloud_storage_exception_handling(self):
        """Test cloud storage setup with exception handling."""
        # Mock ensure_directory_exists to raise an exception
        with patch('src.commercial.services.organization_seeder.ensure_directory_exists') as mock_ensure:
            mock_ensure.side_effect = Exception("Directory creation failed")
            
            result = self.seeder._setup_cloud_storage()
            assert result is False

    def test_create_cloud_storage_readmes(self):
        """Test creation of README files for cloud storage directories."""
        # Create directories first
        cloud_path = self.seeder.config.cloud_storage_path
        cloud_path.mkdir(parents=True)
        
        # Create the subdirectories that the README files will be created in
        (cloud_path / "strategy").mkdir()
        (cloud_path / "workspace").mkdir()
        
        directories = {
            "strategy": "Strategic documents and planning",
            "workspace": "Working documents and collaborative space"
        }
        
        self.seeder._create_cloud_storage_readmes(cloud_path, directories)
        
        # Check that README files were created
        strategy_readme = cloud_path / "strategy" / "README.md"
        workspace_readme = cloud_path / "workspace" / "README.md"
        
        assert strategy_readme.exists()
        assert workspace_readme.exists()
        
        # Check content
        strategy_content = strategy_readme.read_text()
        assert "Test Organization" in strategy_content
        assert "Strategic documents and planning" in strategy_content
        assert "test-org-123" in strategy_content

    def test_detect_cloud_provider_aws(self):
        """Test AWS cloud provider detection."""
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test-key',
            'AWS_SECRET_ACCESS_KEY': 'test-secret'
        }):
            provider = self.seeder._detect_cloud_provider()
            assert provider == "aws"

    def test_detect_cloud_provider_azure(self):
        """Test Azure cloud provider detection."""
        with patch.dict(os.environ, {
            'AZURE_STORAGE_ACCOUNT': 'test-account',
            'AZURE_STORAGE_KEY': 'test-key'
        }):
            provider = self.seeder._detect_cloud_provider()
            assert provider == "azure"

    def test_detect_cloud_provider_gcp(self):
        """Test GCP cloud provider detection."""
        with patch.dict(os.environ, {
            'GOOGLE_APPLICATION_CREDENTIALS': '/path/to/credentials.json'
        }):
            provider = self.seeder._detect_cloud_provider()
            assert provider == "gcp"

    def test_detect_cloud_provider_none(self):
        """Test cloud provider detection when no provider is available."""
        with patch.dict(os.environ, {}, clear=True):
            provider = self.seeder._detect_cloud_provider()
            assert provider is None

    def test_setup_cloud_provider_integration_no_provider(self):
        """Test cloud provider integration when no provider is detected."""
        with patch.object(self.seeder, '_detect_cloud_provider', return_value=None):
            result = self.seeder._setup_cloud_provider_integration(Path("/test"))
            assert result is False

    def test_setup_cloud_provider_integration_aws(self):
        """Test AWS cloud provider integration."""
        with patch.object(self.seeder, '_detect_cloud_provider', return_value="aws"):
            with patch.object(self.seeder, '_setup_aws_s3_integration', return_value=True):
                result = self.seeder._setup_cloud_provider_integration(Path("/test"))
                assert result is True

    def test_setup_cloud_provider_integration_azure(self):
        """Test Azure cloud provider integration."""
        with patch.object(self.seeder, '_detect_cloud_provider', return_value="azure"):
            with patch.object(self.seeder, '_setup_azure_blob_integration', return_value=True):
                result = self.seeder._setup_cloud_provider_integration(Path("/test"))
                assert result is True

    def test_setup_cloud_provider_integration_gcp(self):
        """Test GCP cloud provider integration."""
        with patch.object(self.seeder, '_detect_cloud_provider', return_value="gcp"):
            with patch.object(self.seeder, '_setup_gcp_storage_integration', return_value=True):
                result = self.seeder._setup_cloud_provider_integration(Path("/test"))
                assert result is True

    def test_setup_aws_s3_integration(self):
        """Test AWS S3 integration setup."""
        result = self.seeder._setup_aws_s3_integration(Path("/test"))
        assert result is True

    def test_setup_azure_blob_integration(self):
        """Test Azure Blob integration setup."""
        result = self.seeder._setup_azure_blob_integration(Path("/test"))
        assert result is True

    def test_setup_gcp_storage_integration(self):
        """Test GCP Storage integration setup."""
        result = self.seeder._setup_gcp_storage_integration(Path("/test"))
        assert result is True


class TestOrganizationSeederPlanGating:
    """Test plan-based feature gating functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test customer and organization
        self.customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.STARTUP,
            settings=CustomerSettings(
                plan=SubscriptionPlan.STARTUP,
                max_products=1,
                max_team_members=5,
                features_enabled=["basic_templates"]
            )
        )
        
        self.organization = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
            github_username="testuser"
        )
        
        self.seeder = OrganizationSeeder(
            org_id="test-org-123",
            customer=self.customer,
            organization=self.organization,
            dry_run=True,
            config_data={}
        )

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_deploy_plan_specific_features_startup(self):
        """Test plan-specific feature deployment for startup plan."""
        self.customer.plan = SubscriptionPlan.STARTUP
        
        with patch.object(self.seeder, '_deploy_basic_features') as mock_basic:
            with patch.object(self.seeder, '_log_skipped_features') as mock_log:
                self.seeder._deploy_plan_specific_features()
                
                mock_basic.assert_called_once()
                mock_log.assert_called_once()

    def test_deploy_plan_specific_features_growth(self):
        """Test plan-specific feature deployment for growth plan."""
        self.customer.plan = SubscriptionPlan.GROWTH
        
        with patch.object(self.seeder, '_deploy_basic_features') as mock_basic:
            with patch.object(self.seeder, '_deploy_growth_features') as mock_growth:
                with patch.object(self.seeder, '_log_skipped_features') as mock_log:
                    self.seeder._deploy_plan_specific_features()
                    
                    mock_basic.assert_called_once()
                    mock_growth.assert_called_once()
                    mock_log.assert_called_once()

    def test_deploy_plan_specific_features_scale(self):
        """Test plan-specific feature deployment for scale plan."""
        self.customer.plan = SubscriptionPlan.SCALE
        
        with patch.object(self.seeder, '_deploy_basic_features') as mock_basic:
            with patch.object(self.seeder, '_deploy_scale_features') as mock_scale:
                with patch.object(self.seeder, '_log_skipped_features') as mock_log:
                    self.seeder._deploy_plan_specific_features()
                    
                    mock_basic.assert_called_once()
                    mock_scale.assert_called_once()
                    mock_log.assert_called_once()

    def test_deploy_plan_specific_features_enterprise(self):
        """Test plan-specific feature deployment for enterprise plan."""
        self.customer.plan = SubscriptionPlan.ENTERPRISE
        
        with patch.object(self.seeder, '_deploy_basic_features') as mock_basic:
            with patch.object(self.seeder, '_deploy_enterprise_features') as mock_enterprise:
                with patch.object(self.seeder, '_log_skipped_features') as mock_log:
                    self.seeder._deploy_plan_specific_features()
                    
                    mock_basic.assert_called_once()
                    mock_enterprise.assert_called_once()
                    mock_log.assert_called_once()

    def test_log_skipped_features_startup(self):
        """Test logging of skipped features for startup plan."""
        self.customer.plan = SubscriptionPlan.STARTUP
        
        with patch.object(self.seeder.logger, 'info') as mock_log:
            self.seeder._log_skipped_features()
            
            # Check that appropriate skip messages were logged
            log_calls = [call[0][0] for call in mock_log.call_args_list]
            assert any("requires Growth plan or higher" in msg for msg in log_calls)
            assert any("API access, webhooks" in msg for msg in log_calls)

    def test_log_skipped_features_growth(self):
        """Test logging of skipped features for growth plan."""
        self.customer.plan = SubscriptionPlan.GROWTH
        
        with patch.object(self.seeder.logger, 'info') as mock_log:
            self.seeder._log_skipped_features()
            
            # Check that appropriate skip messages were logged
            log_calls = [call[0][0] for call in mock_log.call_args_list]
            assert any("requires Scale plan or higher" in msg for msg in log_calls)
            assert any("Advanced analytics" in msg for msg in log_calls)

    def test_log_skipped_features_scale(self):
        """Test logging of skipped features for scale plan."""
        self.customer.plan = SubscriptionPlan.SCALE
        
        with patch.object(self.seeder.logger, 'info') as mock_log:
            self.seeder._log_skipped_features()
            
            # Check that appropriate skip messages were logged
            log_calls = [call[0][0] for call in mock_log.call_args_list]
            assert any("requires Enterprise plan" in msg for msg in log_calls)
            assert any("SSO, audit logging" in msg for msg in log_calls)

    def test_log_skipped_features_enterprise(self):
        """Test logging of skipped features for enterprise plan."""
        self.customer.plan = SubscriptionPlan.ENTERPRISE
        
        with patch.object(self.seeder.logger, 'info') as mock_log:
            self.seeder._log_skipped_features()
            
            # Enterprise plan should not log any skipped features
            assert mock_log.call_count == 0


class TestOrganizationSeederDeployment:
    """Test the main deployment functionality with validation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.temp_dir) / "templates"
        self.templates_dir.mkdir(parents=True)
        
        # Create essential templates
        (self.templates_dir / "gitignore.template").write_text("# Git ignore template")
        (self.templates_dir / "github" / "workflows").mkdir(parents=True)
        (self.templates_dir / "github" / "workflows" / "ci.yml.template").write_text("# CI template")
        
        # Create test customer and organization
        self.customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.STARTUP,
            settings=CustomerSettings(
                plan=SubscriptionPlan.STARTUP,
                max_products=1,
                max_team_members=5,
                features_enabled=["basic_templates"]
            )
        )
        
        self.organization = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
            github_username="testuser"
        )
        
        self.seeder = OrganizationSeeder(
            org_id="test-org-123",
            customer=self.customer,
            organization=self.organization,
            dry_run=True,
            config_data={}
        )
        
        # Override paths for testing
        self.seeder.config.templates_dir = self.templates_dir
        self.seeder.config.cloud_storage_path = Path(self.temp_dir) / "cloud-storage"

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_deploy_organization_success(self):
        """Test successful organization deployment."""
        with patch.object(self.seeder, '_preflight_validate', return_value=True):
            with patch.object(self.seeder, '_setup_cloud_storage', return_value=True):
                with patch.object(self.seeder, '_create_organization_structure'):
                    with patch.object(self.seeder, '_setup_meta_repo'):
                        with patch.object(self.seeder, '_deploy_plan_specific_features'):
                            result = self.seeder.deploy_organization()
                            
                            assert result is True
                            assert self.organization.status == OrganizationStatus.ACTIVE
                            assert self.organization.health_status == "healthy"

    def test_deploy_organization_validation_failure(self):
        """Test organization deployment failure due to validation."""
        with patch.object(self.seeder, '_preflight_validate', return_value=False):
            result = self.seeder.deploy_organization()
            
            assert result is False
            assert self.organization.status == OrganizationStatus.SUSPENDED
            assert self.organization.health_status == "validation_failed"

    def test_deploy_organization_cloud_storage_failure(self):
        """Test organization deployment failure due to cloud storage."""
        with patch.object(self.seeder, '_preflight_validate', return_value=True):
            with patch.object(self.seeder, '_setup_cloud_storage', return_value=False):
                result = self.seeder.deploy_organization()
                
                assert result is False
                assert self.organization.status == OrganizationStatus.SUSPENDED
                assert self.organization.health_status == "cloud_storage_failed"

    def test_deploy_organization_exception_handling(self):
        """Test organization deployment exception handling."""
        with patch.object(self.seeder, '_preflight_validate', side_effect=Exception("Test error")):
            result = self.seeder.deploy_organization()
            
            assert result is False
            assert self.organization.status == OrganizationStatus.SUSPENDED
            assert self.organization.health_status == "failed"

    def test_deploy_organization_dry_run_mode(self):
        """Test organization deployment in dry run mode."""
        self.seeder.dry_run = True
        
        with patch.object(self.seeder, '_preflight_validate', return_value=True):
            with patch.object(self.seeder, '_setup_cloud_storage', return_value=True):
                with patch.object(self.seeder, '_create_organization_structure'):
                    with patch.object(self.seeder, '_setup_meta_repo'):
                        with patch.object(self.seeder, '_deploy_plan_specific_features'):
                            result = self.seeder.deploy_organization()
                            
                            assert result is True
                            assert self.organization.status == OrganizationStatus.ACTIVE
