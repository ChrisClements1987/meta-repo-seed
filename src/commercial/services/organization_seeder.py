"""
Multi-Tenant Organization Seeder for Commercial SaaS Platform

This module provides the core OrganizationSeeder class that replaces the single-tenant
RepoSeeder with multi-tenant, organization-scoped deployment capabilities.
"""

import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional, Union, Any
from datetime import datetime

# Import existing utilities from seeding.py
from seeding import (
    sanitize_project_name,
    ensure_directory_exists,
    safe_open_for_write,
    safe_copy_file,
    copy_template_file,
    process_template_content,
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

            # Update organization status
            self.organization.status = OrganizationStatus.CREATING

            # Core deployment steps
            self._create_organization_structure()
            self._setup_meta_repo()
            self._setup_cloud_storage()
            self._create_governance_structure()
            self._create_automation_scripts()
            self._setup_documentation()
            self._create_template_content()
            self._create_infrastructure_templates()
            self._setup_code_formatting()
            self._create_github_repository_settings()
            self._create_audit_management_system()

            # Plan-specific features
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

    def _setup_cloud_storage(self):
        """Set up cloud storage structure for the organization."""
        self.logger.info("Setting up cloud storage structure...")

        # Create cloud storage directories
        cloud_storage_path = self.config.base_path / "cloud-storage"
        ensure_directory_exists(cloud_storage_path)

        # Create strategy and workspace directories
        strategy_path = cloud_storage_path / "strategy"
        workspace_path = cloud_storage_path / "workspace"

        ensure_directory_exists(strategy_path)
        ensure_directory_exists(workspace_path)

        # Create README files
        strategy_readme = strategy_path / "README.md"
        workspace_readme = workspace_path / "README.md"

        if not strategy_readme.exists():
            with safe_open_for_write(strategy_readme, "w") as f:
                f.write(
                    f"# {self.organization.name} - Strategy\n\n"
                    f"Strategic documents and planning for {self.organization.name}.\n\n"
                    f"## Contents\n"
                    f"- Business strategy\n"
                    f"- Product roadmaps\n"
                    f"- Market analysis\n"
                    f"- Competitive intelligence\n"
                )

        if not workspace_readme.exists():
            with safe_open_for_write(workspace_readme, "w") as f:
                f.write(
                    f"# {self.organization.name} - Workspace\n\n"
                    f"Working documents and collaborative space for {self.organization.name}.\n\n"
                    f"## Contents\n"
                    f"- Project documentation\n"
                    f"- Meeting notes\n"
                    f"- Collaborative documents\n"
                    f"- Temporary files\n"
                )

        self.logger.info("Cloud storage structure created successfully")

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

        if self.customer.plan == SubscriptionPlan.ENTERPRISE:
            self._deploy_enterprise_features()
        elif self.customer.plan == SubscriptionPlan.SCALE:
            self._deploy_scale_features()
        elif self.customer.plan == SubscriptionPlan.GROWTH:
            self._deploy_growth_features()
        else:  # STARTUP
            self._deploy_startup_features()

    def _deploy_enterprise_features(self):
        """Deploy enterprise-specific features."""
        self.logger.info("Deploying enterprise features...")

        # SSO configuration
        if self.customer.settings.sso_enabled:
            self._setup_sso_integration()

        # Audit logging
        if self.customer.settings.audit_logging:
            self._setup_audit_logging()

        # White-label branding
        if self.customer.settings.white_label:
            self._setup_white_label_branding()

        # On-premise deployment options
        if self.customer.settings.on_premise:
            self._setup_on_premise_options()

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

    def _deploy_startup_features(self):
        """Deploy startup plan features."""
        self.logger.info("Deploying startup features...")

        # Basic templates and GitHub integration
        self._setup_basic_features()

    # Placeholder methods for plan-specific features
    def _setup_sso_integration(self):
        """Set up SSO integration for enterprise customers."""
        self.logger.info("Setting up SSO integration...")
        # Implementation for SSO setup

    def _setup_audit_logging(self):
        """Set up audit logging for enterprise customers."""
        self.logger.info("Setting up audit logging...")
        # Implementation for audit logging

    def _setup_white_label_branding(self):
        """Set up white-label branding for enterprise customers."""
        self.logger.info("Setting up white-label branding...")
        # Implementation for white-label branding

    def _setup_on_premise_options(self):
        """Set up on-premise deployment options for enterprise customers."""
        self.logger.info("Setting up on-premise options...")
        # Implementation for on-premise options

    def _setup_advanced_analytics(self):
        """Set up advanced analytics for scale customers."""
        self.logger.info("Setting up advanced analytics...")
        # Implementation for advanced analytics

    def _setup_enhanced_monitoring(self):
        """Set up enhanced monitoring for scale customers."""
        self.logger.info("Setting up enhanced monitoring...")
        # Implementation for enhanced monitoring

    def _setup_api_access(self):
        """Set up API access for growth customers."""
        self.logger.info("Setting up API access...")
        # Implementation for API access

    def _setup_webhook_support(self):
        """Set up webhook support for growth customers."""
        self.logger.info("Setting up webhook support...")
        # Implementation for webhook support

    def _setup_basic_features(self):
        """Set up basic features for startup customers."""
        self.logger.info("Setting up basic features...")
        # Implementation for basic features

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
