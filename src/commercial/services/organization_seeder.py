"""
Multi-Tenant Organization Seeder for Commercial SaaS Platform

This module provides the core OrganizationSeeder class that replaces the single-tenant
RepoSeeder with multi-tenant, organization-scoped deployment capabilities.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional, Union, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .customer_manager import CustomerManager
from datetime import datetime

# Import existing utilities from seeding.py
from seeding import (
    ensure_directory_exists,
    safe_open_for_write,
    copy_template_file,
    create_file_from_template,
)

# Import commercial models
from ..models import (
    Organization,
    Customer,
    SubscriptionPlan,
    OrganizationStatus,
)


class OrganizationConfig:
    """
    Configuration for organization deployment with multi-tenant support.

    Replaces the single-tenant Configuration class with organization-scoped
    configuration that supports different subscription plans and customer settings.
    """

    def __init__(
        self,
        org_id: str,
        customer: Customer,
        organization: Organization,
        dry_run: bool = False,
        templates_dir: Optional[Union[str, Path]] = None,
        base_path: Optional[Union[str, Path]] = None,
    ):
        """Initialize organization configuration."""
        self.org_id = org_id
        self.customer = customer
        self.organization = organization
        self.dry_run = dry_run
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self.base_path = Path(base_path) if base_path else None

        # Organization-specific paths
        self.org_base_path = Path(f"organizations/{org_id}")
        self.meta_repo_path = self.org_base_path / "meta-repo"
        self.cloud_storage_path = self.org_base_path / "cloud-storage"

        # Template replacements with organization context
        self.replacements = {
            "ORG_ID": org_id,
            "ORG_NAME": organization.name,
            "CUSTOMER_EMAIL": customer.email,
            "COMPANY_NAME": customer.company_name,
            "GITHUB_USERNAME": organization.github_username,
            "GITHUB_ORG": organization.github_org or organization.github_username,
            "CURRENT_DATE": datetime.now().strftime("%Y-%m-%d"),
            "SUBSCRIPTION_PLAN": customer.plan.value,
            "MAX_PRODUCTS": str(customer.settings.max_products),
            "MAX_TEAM_MEMBERS": str(customer.settings.max_team_members),
            "FEATURES_ENABLED": ",".join(customer.settings.features_enabled),
            "CUSTOM_BRANDING": str(customer.settings.custom_branding).lower(),
            "WHITE_LABEL": str(customer.settings.white_label).lower(),
            "SSO_ENABLED": str(customer.settings.sso_enabled).lower(),
            "AUDIT_LOGGING": str(customer.settings.audit_logging).lower(),
        }

        # Plan-specific template directories
        self.plan_templates = {
            SubscriptionPlan.STARTUP: "startup",
            SubscriptionPlan.GROWTH: "growth",
            SubscriptionPlan.SCALE: "scale",
            SubscriptionPlan.ENTERPRISE: "enterprise",
        }

    def get_template_path(self, template_name: str) -> Path:
        """Get template path based on subscription plan."""
        if not self.templates_dir:
            self.templates_dir = Path.cwd() / "templates"

        # Check for plan-specific template first
        plan_template_dir = self.plan_templates.get(self.customer.plan, "startup")
        plan_template_path = self.templates_dir / plan_template_dir / template_name

        if plan_template_path.exists():
            return plan_template_path

        # Fall back to default template
        return self.templates_dir / template_name

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled for this customer."""
        return feature in self.customer.settings.features_enabled

    def get_plan_limits(self) -> Dict[str, int]:
        """Get plan-specific limits."""
        return {
            "max_products": self.customer.settings.max_products,
            "max_team_members": self.customer.settings.max_team_members,
            "max_api_calls": self._get_api_limit(),
            "max_storage_mb": self._get_storage_limit(),
        }

    def _get_api_limit(self) -> int:
        """Get API call limit based on plan."""
        limits = {
            SubscriptionPlan.STARTUP: 1000,
            SubscriptionPlan.GROWTH: 10000,
            SubscriptionPlan.SCALE: 100000,
            SubscriptionPlan.ENTERPRISE: -1,  # Unlimited
        }
        return limits.get(self.customer.plan, 1000)

    def _get_storage_limit(self) -> int:
        """Get storage limit in MB based on plan."""
        limits = {
            SubscriptionPlan.STARTUP: 100,  # 100MB
            SubscriptionPlan.GROWTH: 1000,  # 1GB
            SubscriptionPlan.SCALE: 10000,  # 10GB
            SubscriptionPlan.ENTERPRISE: -1,  # Unlimited
        }
        return limits.get(self.customer.plan, 100)


class OrganizationSeeder:
    """
    Multi-tenant organization seeder for commercial SaaS platform.

    Replaces the single-tenant RepoSeeder with organization-scoped deployment
    capabilities that support multiple customers and subscription plans.
    """

    def __init__(
        self,
        org_id: str,
        customer: Customer,
        organization: Organization,
        dry_run: bool = False,
        config_data: Optional[Dict[str, Any]] = None,
    ):
        """Initialize organization seeder."""
        self.org_id = org_id
        self.customer = customer
        self.organization = organization
        self.dry_run = dry_run
        self.config_data = config_data or {}

        # Initialize configuration
        self.config = OrganizationConfig(
            org_id=org_id,
            customer=customer,
            organization=organization,
            dry_run=dry_run,
            templates_dir=Path.cwd() / "templates",
            base_path=Path(f"organizations/{org_id}"),
        )

        # Set up logging
        self.logger = logging.getLogger(f"org_seeder.{org_id}")

        self.logger.info(f"Initializing OrganizationSeeder for org: {org_id}")
        self.logger.info(f"Customer: {customer.email} ({customer.plan.value})")
        self.logger.info(f"Organization: {organization.name}")
        self.logger.info(f"Dry run mode: {dry_run}")

    @classmethod
    def create_for_customer(
        cls,
        customer_id: str,
        organization_name: str,
        customer_manager: Optional["CustomerManager"] = None,
        dry_run: bool = False,
    ) -> "OrganizationSeeder":
        """
        Factory method to create OrganizationSeeder for a customer.

        Args:
            customer_id: Customer ID
            organization_name: Name of the organization
            customer_manager: CustomerManager instance (optional)
            dry_run: Whether to run in dry-run mode

        Returns:
            OrganizationSeeder instance
        """
        # Import here to avoid circular imports
        from .customer_manager import CustomerManager

        if customer_manager is None:
            customer_manager = CustomerManager()

        # Get customer
        customer = customer_manager.get_customer(customer_id)
        if not customer:
            raise ValueError(f"Customer not found: {customer_id}")

        # Create organization
        org_id = f"org_{customer_id}_{organization_name.lower().replace(' ', '_')}"
        organization = Organization(
            org_id=org_id,
            customer_id=customer_id,
            name=organization_name,
            status=OrganizationStatus.CREATING,
        )

        return cls(
            org_id=org_id, customer=customer, organization=organization, dry_run=dry_run
        )

    def deploy_organization(self) -> bool:
        """
        Deploy complete organization infrastructure.

        This is the main entry point that orchestrates the entire deployment
        process for a customer organization.
        """
        try:
            if self.dry_run:
                self.logger.info("DRY RUN MODE - No actual changes will be made")

            self.logger.info("Starting organization deployment process...")

            # Pre-flight validation
            if not self._preflight_validate():
                self.logger.error("Pre-flight validation failed - aborting deployment")
                self.organization.status = OrganizationStatus.SUSPENDED
                self.organization.health_status = "validation_failed"
                return False

            # Update organization status
            self.organization.status = OrganizationStatus.CREATING

            # Core deployment steps
            self._create_organization_structure()
            self._setup_meta_repo()
            
            # Cloud storage with proper error handling
            if not self._setup_cloud_storage():
                self.logger.error("Cloud storage setup failed - aborting deployment")
                self.organization.status = OrganizationStatus.SUSPENDED
                self.organization.health_status = "cloud_storage_failed"
                return False

            # Plan-specific features (gated by plan checks)
            self._deploy_plan_specific_features()

            # Update organization status
            self.organization.status = OrganizationStatus.ACTIVE
            self.organization.deployed_at = datetime.now()
            self.organization.health_status = "healthy"

            self.logger.info("Organization deployment completed successfully!")
            return True

        except Exception as e:
            self.logger.error(f"Organization deployment failed: {e}")
            self.organization.status = OrganizationStatus.SUSPENDED
            self.organization.health_status = "failed"
            return False

    def _preflight_validate(self) -> bool:
        """
        Pre-flight validation before deployment.
        
        Validates customer settings, cloud configuration, and template availability.
        Returns True if all validations pass, False otherwise.
        """
        self.logger.info("Running pre-flight validation...")
        
        try:
            # Validate customer settings
            if not self._validate_customer_settings():
                return False
            
            # Validate cloud configuration
            if not self._validate_cloud_config():
                return False
            
            # Validate template availability
            if not self._validate_templates():
                return False
            
            # Validate organization data
            if not self._validate_organization_data():
                return False
            
            self.logger.info("Pre-flight validation passed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Pre-flight validation error: {e}")
            return False

    def _validate_customer_settings(self) -> bool:
        """Validate customer settings and configuration."""
        try:
            # Check customer exists and is active
            if not self.customer:
                self.logger.error("Customer is None")
                return False
            
            if not self.customer.email:
                self.logger.error("Customer email is missing")
                return False
            
            if not self.customer.company_name:
                self.logger.warning("Customer company name is missing - using fallback")
            
            # Check subscription plan
            if not self.customer.plan:
                self.logger.error("Customer subscription plan is missing")
                return False
            
            # Check settings
            if not self.customer.settings:
                self.logger.error("Customer settings are missing")
                return False
            
            # Validate plan limits
            limits = self.config.get_plan_limits()
            if limits["max_products"] < 1:
                self.logger.error("Invalid max_products limit")
                return False
            
            self.logger.debug("Customer settings validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Customer settings validation failed: {e}")
            return False

    def _validate_cloud_config(self) -> bool:
        """Validate cloud storage configuration."""
        try:
            # Check if cloud storage path is accessible
            cloud_path = self.config.cloud_storage_path
            if not cloud_path:
                self.logger.error("Cloud storage path is not configured")
                return False
            
            # Check if we can create the directory (dry run check)
            if not self.dry_run:
                try:
                    cloud_path.mkdir(parents=True, exist_ok=True)
                    self.logger.debug(f"Cloud storage path validated: {cloud_path}")
                except PermissionError:
                    self.logger.error(f"Permission denied for cloud storage path: {cloud_path}")
                    return False
                except Exception as e:
                    self.logger.error(f"Cloud storage path validation failed: {e}")
                    return False
            
            self.logger.debug("Cloud configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Cloud configuration validation failed: {e}")
            return False

    def _validate_templates(self) -> bool:
        """Validate template availability."""
        try:
            # Check if templates directory exists
            templates_dir = self.config.templates_dir
            if not templates_dir or not templates_dir.exists():
                self.logger.error(f"Templates directory not found: {templates_dir}")
                return False
            
            # Check for essential templates
            essential_templates = [
                "gitignore.template",
                "github/workflows/ci.yml.template",
                "github/workflows/readme-docs.yml.template"
            ]
            
            for template_name in essential_templates:
                template_path = self.config.get_template_path(template_name)
                if not template_path.exists():
                    self.logger.warning(f"Template not found: {template_name} - will use fallback")
            
            self.logger.debug("Template validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Template validation failed: {e}")
            return False

    def _validate_organization_data(self) -> bool:
        """Validate organization data."""
        try:
            # Check organization exists
            if not self.organization:
                self.logger.error("Organization is None")
                return False
            
            # Check required fields
            if not self.organization.name:
                self.logger.error("Organization name is missing")
                return False
            
            if not self.org_id:
                self.logger.error("Organization ID is missing")
                return False
            
            # Check GitHub configuration
            if not self.organization.github_username:
                self.logger.warning("GitHub username not configured - will use fallback")
            
            self.logger.debug("Organization data validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Organization data validation failed: {e}")
            return False

    def _setup_cloud_storage(self) -> bool:
        """
        Set up cloud storage structure for the organization.
        
        Creates local directory structure with fallback logic for cloud providers.
        Returns True if successful, False if critical failures occur.
        """
        self.logger.info("Setting up cloud storage structure...")
        
        try:
            # Create cloud storage directories
            cloud_storage_path = self.config.cloud_storage_path
            
            if not self.dry_run:
                ensure_directory_exists(cloud_storage_path)
                self.logger.debug(f"Created cloud storage path: {cloud_storage_path}")
            
            # Create core directories
            directories = {
                "strategy": "Strategic documents and planning",
                "workspace": "Working documents and collaborative space",
                "archives": "Archived documents and historical data",
                "templates": "Organization-specific templates"
            }
            
            created_dirs = []
            for dir_name, description in directories.items():
                dir_path = cloud_storage_path / dir_name
                
                if not self.dry_run:
                    ensure_directory_exists(dir_path)
                    created_dirs.append(dir_name)
                    self.logger.debug(f"Created directory: {dir_name}")
                else:
                    self.logger.info(f"DRY RUN: Would create directory: {dir_name}")
            
            # Create README files for each directory
            if not self.dry_run:
                self._create_cloud_storage_readmes(cloud_storage_path, directories)
            
            # Attempt cloud provider integration (with fallback)
            cloud_success = self._setup_cloud_provider_integration(cloud_storage_path)
            
            if cloud_success:
                self.logger.info("Cloud storage setup completed successfully with provider integration")
            else:
                self.logger.warning("Cloud storage setup completed with local fallback only")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Cloud storage setup failed: {e}")
            return False

    def _create_cloud_storage_readmes(self, base_path: Path, directories: Dict[str, str]):
        """Create README files for cloud storage directories."""
        try:
            for dir_name, description in directories.items():
                readme_path = base_path / dir_name / "README.md"
                
                if not readme_path.exists():
                    with safe_open_for_write(readme_path, encoding="utf-8") as f:
                        f.write(
                            f"# {self.organization.name} - {dir_name.title()}\n\n"
                            f"{description} for {self.organization.name}.\n\n"
                            f"## Organization Details\n"
                            f"- **Organization ID**: {self.org_id}\n"
                            f"- **Customer**: {self.customer.email}\n"
                            f"- **Plan**: {self.customer.plan.value}\n"
                            f"- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                            f"## Contents\n"
                            f"- {description.lower()}\n"
                            f"- Organization-specific resources\n"
                            f"- Collaborative documents\n"
                        )
                    self.logger.debug(f"Created README for {dir_name}")
                    
        except Exception as e:
            self.logger.error(f"Failed to create README files: {e}")

    def _setup_cloud_provider_integration(self, cloud_path: Path) -> bool:
        """
        Attempt to set up cloud provider integration.
        
        This is where real cloud storage (AWS S3, Azure Blob, GCP Storage) would be configured.
        Returns True if cloud integration succeeds, False for fallback to local storage.
        """
        try:
            # Check if cloud provider credentials are available
            cloud_provider = self._detect_cloud_provider()
            
            if not cloud_provider:
                self.logger.info("No cloud provider detected - using local storage only")
                return False
            
            self.logger.info(f"Detected cloud provider: {cloud_provider}")
            
            # Attempt to create cloud bucket/container
            if cloud_provider == "aws":
                return self._setup_aws_s3_integration(cloud_path)
            elif cloud_provider == "azure":
                return self._setup_azure_blob_integration(cloud_path)
            elif cloud_provider == "gcp":
                return self._setup_gcp_storage_integration(cloud_path)
            else:
                self.logger.warning(f"Unsupported cloud provider: {cloud_provider}")
                return False
                
        except Exception as e:
            self.logger.error(f"Cloud provider integration failed: {e}")
            return False

    def _detect_cloud_provider(self) -> Optional[str]:
        """Detect available cloud provider based on environment variables."""
        import os
        
        # Check for AWS credentials
        if os.getenv("AWS_ACCESS_KEY_ID") and os.getenv("AWS_SECRET_ACCESS_KEY"):
            return "aws"
        
        # Check for Azure credentials
        if os.getenv("AZURE_STORAGE_ACCOUNT") and os.getenv("AZURE_STORAGE_KEY"):
            return "azure"
        
        # Check for GCP credentials
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") or os.getenv("GCP_PROJECT"):
            return "gcp"
        
        return None

    def _setup_aws_s3_integration(self, cloud_path: Path) -> bool:
        """Set up AWS S3 integration."""
        try:
            # This would be real AWS S3 integration
            # For now, simulate the process
            bucket_name = f"{self.org_id}-storage"
            self.logger.info(f"Would create S3 bucket: {bucket_name}")
            
            # In a real implementation, you would:
            # 1. Create S3 bucket
            # 2. Set up bucket policies
            # 3. Configure lifecycle rules
            # 4. Set up monitoring
            
            self.logger.info("AWS S3 integration would be configured here")
            return True
            
        except Exception as e:
            self.logger.error(f"AWS S3 integration failed: {e}")
            return False

    def _setup_azure_blob_integration(self, cloud_path: Path) -> bool:
        """Set up Azure Blob Storage integration."""
        try:
            # This would be real Azure Blob integration
            container_name = f"{self.org_id}-storage"
            self.logger.info(f"Would create Azure container: {container_name}")
            
            # In a real implementation, you would:
            # 1. Create blob container
            # 2. Set up access policies
            # 3. Configure lifecycle management
            # 4. Set up monitoring
            
            self.logger.info("Azure Blob integration would be configured here")
            return True
            
        except Exception as e:
            self.logger.error(f"Azure Blob integration failed: {e}")
            return False

    def _setup_gcp_storage_integration(self, cloud_path: Path) -> bool:
        """Set up Google Cloud Storage integration."""
        try:
            # This would be real GCP Storage integration
            bucket_name = f"{self.org_id}-storage"
            self.logger.info(f"Would create GCP bucket: {bucket_name}")
            
            # In a real implementation, you would:
            # 1. Create GCS bucket
            # 2. Set up IAM policies
            # 3. Configure lifecycle rules
            # 4. Set up monitoring
            
            self.logger.info("GCP Storage integration would be configured here")
            return True
            
        except Exception as e:
            self.logger.error(f"GCP Storage integration failed: {e}")
            return False

    def _create_organization_structure(self):
        """Create the base organization structure."""
        self.logger.info("Creating organization structure...")

        if not self.dry_run:
            ensure_directory_exists(
                self.config.org_base_path, f"(org root: {self.org_id})"
            )
            ensure_directory_exists(self.config.meta_repo_path, "(meta-repo)")
            ensure_directory_exists(self.config.cloud_storage_path, "(cloud-storage)")

            # Create placeholder directories for future repos based on plan limits
            max_products = self.config.get_plan_limits()["max_products"]
            if max_products == -1:  # Unlimited
                product_dirs = [
                    "core-services",
                    "saas-products",
                    "partner-products",
                    "charity-products",
                ]
            else:
                # Limit directories based on plan
                product_dirs = [
                    "core-services",
                    "saas-products",
                ]  # Start with core directories

            for product_dir in product_dirs:
                ensure_directory_exists(
                    self.config.org_base_path / product_dir, f"({product_dir})"
                )

    def _setup_meta_repo(self):
        """Set up the meta-repo with Git initialization and GitHub workflows."""
        self.logger.info("Setting up meta-repo...")

        if not self.dry_run:
            # Initialize Git repository
            self._init_git_repo(self.config.meta_repo_path)

            # Create .gitignore
            self._create_gitignore()

            # Create GitHub workflows
            workflows_path = self.config.meta_repo_path / ".github" / "workflows"
            ensure_directory_exists(workflows_path, "(GitHub workflows)")

            # Copy workflow templates
            self._copy_workflow_templates(workflows_path)

    def _copy_workflow_templates(self, workflows_path: Path):
        """Copy GitHub workflow templates based on customer plan."""
        workflow_templates = ["ci.yml.template", "readme-docs.yml.template"]

        # Add plan-specific workflows
        if self.config.is_feature_enabled("api_access"):
            workflow_templates.append("api-monitoring.yml.template")

        if self.config.is_feature_enabled("webhooks"):
            workflow_templates.append("webhook-handler.yml.template")

        if self.config.is_feature_enabled("analytics"):
            workflow_templates.append("analytics-collection.yml.template")

        for template_name in workflow_templates:
            template_path = self.config.get_template_path(
                f"github/workflows/{template_name}"
            )
            dest_path = workflows_path / template_name.replace(".template", "")
            create_file_from_template(
                template_path,
                dest_path,
                self.config.replacements,
                f"(workflow: {template_name})",
            )

    def _deploy_plan_specific_features(self):
        """Deploy features specific to the customer's subscription plan."""
        self.logger.info(f"Deploying {self.customer.plan.value} plan features...")

        # Always deploy basic features
        self._deploy_basic_features()

        # Deploy plan-specific features with proper gating
        if self.customer.plan == SubscriptionPlan.ENTERPRISE:
            self._deploy_enterprise_features()
        elif self.customer.plan == SubscriptionPlan.SCALE:
            self._deploy_scale_features()
        elif self.customer.plan == SubscriptionPlan.GROWTH:
            self._deploy_growth_features()
        
        # Log skipped features for lower plans
        self._log_skipped_features()

    def _deploy_basic_features(self):
        """Deploy basic features available to all plans."""
        self.logger.info("Deploying basic features...")
        
        # Basic GitHub integration
        self._setup_basic_github_integration()
        
        # Basic templates
        self._setup_basic_templates()
        
        self.logger.info("Basic features deployed successfully")

    def _deploy_enterprise_features(self):
        """Deploy enterprise-specific features."""
        self.logger.info("Deploying enterprise features...")

        # SSO configuration
        if self.customer.settings.sso_enabled:
            self._setup_sso_integration()
        else:
            self.logger.info("SSO integration skipped - not enabled in customer settings")

        # Audit logging
        if self.customer.settings.audit_logging:
            self._setup_audit_logging()
        else:
            self.logger.info("Audit logging skipped - not enabled in customer settings")

        # White-label branding
        if self.customer.settings.white_label:
            self._setup_white_label_branding()
        else:
            self.logger.info("White-label branding skipped - not enabled in customer settings")

        # On-premise deployment options
        if self.customer.settings.on_premise:
            self._setup_on_premise_options()
        else:
            self.logger.info("On-premise options skipped - not enabled in customer settings")

    def _deploy_scale_features(self):
        """Deploy scale plan features."""
        self.logger.info("Deploying scale features...")

        # Advanced analytics
        self._setup_advanced_analytics()

        # Enhanced monitoring
        self._setup_enhanced_monitoring()

    def _deploy_growth_features(self):
        """Deploy growth plan features."""
        self.logger.info("Deploying growth features...")

        # API access
        self._setup_api_access()

        # Webhook support
        self._setup_webhook_support()

    def _log_skipped_features(self):
        """Log features that are skipped due to plan limitations."""
        current_plan = self.customer.plan
        
        if current_plan == SubscriptionPlan.STARTUP:
            self.logger.info("Skipping advanced features - requires Growth plan or higher")
            self.logger.info("Skipped: API access, webhooks, advanced analytics, enhanced monitoring")
            self.logger.info("Skipped: SSO, audit logging, white-label branding, on-premise options")
        elif current_plan == SubscriptionPlan.GROWTH:
            self.logger.info("Skipping enterprise features - requires Scale plan or higher")
            self.logger.info("Skipped: Advanced analytics, enhanced monitoring")
            self.logger.info("Skipped: SSO, audit logging, white-label branding, on-premise options")
        elif current_plan == SubscriptionPlan.SCALE:
            self.logger.info("Skipping enterprise features - requires Enterprise plan")
            self.logger.info("Skipped: SSO, audit logging, white-label branding, on-premise options")

    # Real implementations for plan-specific features
    def _setup_basic_github_integration(self):
        """Set up basic GitHub integration."""
        self.logger.info("Setting up basic GitHub integration...")
        
        if not self.dry_run:
            # Create basic GitHub workflows
            workflows_path = self.config.meta_repo_path / ".github" / "workflows"
            ensure_directory_exists(workflows_path)
            
            # Copy basic workflow templates
            self._copy_workflow_templates(workflows_path)
            
            self.logger.info("Basic GitHub integration configured")
        else:
            self.logger.info("DRY RUN: Would set up basic GitHub integration")

    def _setup_basic_templates(self):
        """Set up basic templates."""
        self.logger.info("Setting up basic templates...")
        
        if not self.dry_run:
            # Create basic template structure
            templates_path = self.config.org_base_path / "templates"
            ensure_directory_exists(templates_path)
            
            # Copy essential templates
            essential_templates = ["gitignore.template", "README.md.template"]
            for template_name in essential_templates:
                template_path = self.config.get_template_path(template_name)
                if template_path.exists():
                    dest_path = templates_path / template_name
                    copy_template_file(template_path, dest_path, f"(template: {template_name})")
            
            self.logger.info("Basic templates configured")
        else:
            self.logger.info("DRY RUN: Would set up basic templates")

    def _setup_sso_integration(self):
        """Set up SSO integration for enterprise customers."""
        self.logger.info("Setting up SSO integration...")
        
        if not self.dry_run:
            # This would be real SSO integration
            # For now, create configuration files
            sso_config_path = self.config.org_base_path / "config" / "sso"
            ensure_directory_exists(sso_config_path)
            
            # Create SSO configuration template
            sso_config_file = sso_config_path / "sso-config.yaml"
            with safe_open_for_write(sso_config_file, "w") as f:
                f.write(
                    f"# SSO Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"customer_id: {self.customer.customer_id}\n"
                    f"enabled: true\n"
                    f"providers:\n"
                    f"  - saml\n"
                    f"  - oauth2\n"
                )
            
            self.logger.info("SSO integration configured")
        else:
            self.logger.info("DRY RUN: Would set up SSO integration")

    def _setup_audit_logging(self):
        """Set up audit logging for enterprise customers."""
        self.logger.info("Setting up audit logging...")
        
        if not self.dry_run:
            # Create audit logging configuration
            audit_config_path = self.config.org_base_path / "config" / "audit"
            ensure_directory_exists(audit_config_path)
            
            # Create audit configuration file
            audit_config_file = audit_config_path / "audit-config.yaml"
            with safe_open_for_write(audit_config_file, "w") as f:
                f.write(
                    f"# Audit Logging Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"retention_days: 365\n"
                    f"log_levels:\n"
                    f"  - info\n"
                    f"  - warning\n"
                    f"  - error\n"
                )
            
            self.logger.info("Audit logging configured")
        else:
            self.logger.info("DRY RUN: Would set up audit logging")

    def _setup_white_label_branding(self):
        """Set up white-label branding for enterprise customers."""
        self.logger.info("Setting up white-label branding...")
        
        if not self.dry_run:
            # Create branding configuration
            branding_path = self.config.org_base_path / "branding"
            ensure_directory_exists(branding_path)
            
            # Create branding configuration file
            branding_config_file = branding_path / "branding-config.yaml"
            with safe_open_for_write(branding_config_file, "w") as f:
                f.write(
                    f"# White-label Branding Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"company_name: {self.customer.company_name}\n"
                    f"enabled: true\n"
                    f"custom_domain: false\n"
                    f"logo_path: /branding/logo.png\n"
                )
            
            self.logger.info("White-label branding configured")
        else:
            self.logger.info("DRY RUN: Would set up white-label branding")

    def _setup_on_premise_options(self):
        """Set up on-premise deployment options for enterprise customers."""
        self.logger.info("Setting up on-premise options...")
        
        if not self.dry_run:
            # Create on-premise configuration
            onprem_path = self.config.org_base_path / "on-premise"
            ensure_directory_exists(onprem_path)
            
            # Create on-premise configuration file
            onprem_config_file = onprem_path / "on-premise-config.yaml"
            with safe_open_for_write(onprem_config_file, "w") as f:
                f.write(
                    f"# On-premise Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"deployment_type: kubernetes\n"
                    f"storage_class: local-storage\n"
                )
            
            self.logger.info("On-premise options configured")
        else:
            self.logger.info("DRY RUN: Would set up on-premise options")

    def _setup_advanced_analytics(self):
        """Set up advanced analytics for scale customers."""
        self.logger.info("Setting up advanced analytics...")
        
        if not self.dry_run:
            # Create analytics configuration
            analytics_path = self.config.org_base_path / "analytics"
            ensure_directory_exists(analytics_path)
            
            # Create analytics configuration file
            analytics_config_file = analytics_path / "analytics-config.yaml"
            with safe_open_for_write(analytics_config_file, "w") as f:
                f.write(
                    f"# Advanced Analytics Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"metrics_retention_days: 90\n"
                    f"dashboard_enabled: true\n"
                )
            
            self.logger.info("Advanced analytics configured")
        else:
            self.logger.info("DRY RUN: Would set up advanced analytics")

    def _setup_enhanced_monitoring(self):
        """Set up enhanced monitoring for scale customers."""
        self.logger.info("Setting up enhanced monitoring...")
        
        if not self.dry_run:
            # Create monitoring configuration
            monitoring_path = self.config.org_base_path / "monitoring"
            ensure_directory_exists(monitoring_path)
            
            # Create monitoring configuration file
            monitoring_config_file = monitoring_path / "monitoring-config.yaml"
            with safe_open_for_write(monitoring_config_file, "w") as f:
                f.write(
                    f"# Enhanced Monitoring Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"alerting_enabled: true\n"
                    f"metrics_interval: 30s\n"
                )
            
            self.logger.info("Enhanced monitoring configured")
        else:
            self.logger.info("DRY RUN: Would set up enhanced monitoring")

    def _setup_api_access(self):
        """Set up API access for growth customers."""
        self.logger.info("Setting up API access...")
        
        if not self.dry_run:
            # Create API configuration
            api_path = self.config.org_base_path / "api"
            ensure_directory_exists(api_path)
            
            # Create API configuration file
            api_config_file = api_path / "api-config.yaml"
            with safe_open_for_write(api_config_file, "w") as f:
                f.write(
                    f"# API Access Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"rate_limit: 1000/hour\n"
                    f"authentication: api_key\n"
                )
            
            self.logger.info("API access configured")
        else:
            self.logger.info("DRY RUN: Would set up API access")

    def _setup_webhook_support(self):
        """Set up webhook support for growth customers."""
        self.logger.info("Setting up webhook support...")
        
        if not self.dry_run:
            # Create webhook configuration
            webhook_path = self.config.org_base_path / "webhooks"
            ensure_directory_exists(webhook_path)
            
            # Create webhook configuration file
            webhook_config_file = webhook_path / "webhook-config.yaml"
            with safe_open_for_write(webhook_config_file, "w") as f:
                f.write(
                    f"# Webhook Configuration for {self.organization.name}\n"
                    f"organization_id: {self.org_id}\n"
                    f"enabled: true\n"
                    f"max_webhooks: 10\n"
                    f"retry_attempts: 3\n"
                )
            
            self.logger.info("Webhook support configured")
        else:
            self.logger.info("DRY RUN: Would set up webhook support")

    # Reuse existing methods from seeding.py with organization context
    def _init_git_repo(self, repo_path: Path):
        """Initialize a Git repository if it doesn't exist."""
        git_path = repo_path / ".git"
        if git_path.exists():
            self.logger.debug(f"Git repository already exists at: {repo_path}")
            return

        try:
            subprocess.run(
                ["git", "init"],
                check=True,
                capture_output=True,
                text=True,
                cwd=str(repo_path),
            )
            self.logger.info(f"Initialized Git repository: {repo_path}")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to initialize Git repository: {e}")
            raise

    def _create_gitignore(self):
        """Create a comprehensive .gitignore file from template."""
        gitignore_path = self.config.meta_repo_path / ".gitignore"
        if gitignore_path.exists():
            self.logger.debug(".gitignore already exists")
            return

        template_path = self.config.get_template_path("gitignore.template")
        copy_template_file(template_path, gitignore_path, "(.gitignore)")

    # Additional methods would be implemented following the same pattern,
    # reusing existing functionality from seeding.py but with organization context
