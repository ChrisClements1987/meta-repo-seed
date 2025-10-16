"""
Customer Management Service for Commercial SaaS Platform

This module provides customer lifecycle management, including onboarding,
subscription management, and customer support functionality.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import json

from ..models import (
    Customer,
    Organization,
    Subscription,
    UsageMetrics,
    CustomerStatus,
    SubscriptionPlan,
    OrganizationStatus,
    CustomerSettings,
)
from ..database import get_db_manager


class CustomerManager:
    """
    Manages customer lifecycle for the commercial SaaS platform.

    Handles customer onboarding, subscription management, organization
    deployment, and customer support operations.
    """

    def __init__(self, database_url: Optional[str] = None):
        """Initialize customer manager."""
        self.db_manager = get_db_manager()
        self.logger = logging.getLogger("customer_manager")

    def create_customer(
        self,
        email: str,
        company_name: str,
        plan: SubscriptionPlan = SubscriptionPlan.STARTUP,
        trial_days: int = 14,
    ) -> Customer:
        """
        Create a new customer account.

        Args:
            email: Customer email address
            company_name: Company name
            plan: Subscription plan (defaults to STARTUP)
            trial_days: Trial period in days (defaults to 14)

        Returns:
            Customer object

        Raises:
            ValueError: If customer already exists
        """
        # Check if customer already exists
        existing_customer = self.get_customer_by_email(email)
        if existing_customer:
            raise ValueError(f"Customer with email {email} already exists")

        # Create customer record
        customer_query = """
        INSERT INTO customers (email, company_name, status, settings)
        VALUES (%s, %s, %s, %s)
        RETURNING id, email, company_name, status, created_at, updated_at, settings
        """

        customer_data = self.db_manager.execute_query(
            customer_query,
            (email, company_name, CustomerStatus.ACTIVE.value, json.dumps({})),
            fetch=True,
        )

        if not customer_data:
            raise RuntimeError("Failed to create customer")

        customer_row = customer_data[0]

        # Parse settings if it's a string
        settings_data = customer_row["settings"]
        if isinstance(settings_data, str):
            settings_data = json.loads(settings_data) if settings_data else {}

        # Create CustomerSettings object
        settings = CustomerSettings(
            plan=plan,
            max_products=settings_data.get("max_products", 1),
            max_team_members=settings_data.get("max_team_members", 5),
            features_enabled=settings_data.get("features_enabled", []),
            custom_branding=settings_data.get("custom_branding", False),
            white_label=settings_data.get("white_label", False),
            on_premise=settings_data.get("on_premise", False),
            sso_enabled=settings_data.get("sso_enabled", False),
            audit_logging=settings_data.get("audit_logging", False),
        )

        customer = Customer(
            customer_id=str(customer_row["id"]),
            email=customer_row["email"],
            company_name=customer_row["company_name"],
            status=CustomerStatus(customer_row["status"]),
            plan=plan,
            created_at=customer_row["created_at"],
            updated_at=customer_row["updated_at"],
            settings=settings,
        )

        # Create subscription
        self._create_subscription(customer.customer_id, plan, trial_days)

        self.logger.info(f"Created customer {customer.customer_id} for {company_name}")
        return customer

    def _create_subscription(
        self, customer_id: str, plan: SubscriptionPlan, trial_days: int
    ):
        """Create a subscription for a customer."""
        end_date = (
            datetime.now() + timedelta(days=trial_days) if trial_days > 0 else None
        )

        subscription_query = """
        INSERT INTO subscriptions (customer_id, plan, status, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        """

        self.db_manager.execute_query(
            subscription_query,
            (customer_id, plan.value, "active", datetime.now(), end_date),
        )

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        query = """
        SELECT id, email, company_name, status, created_at, updated_at, settings
        FROM customers WHERE id = %s
        """

        result = self.db_manager.execute_query(query, (customer_id,), fetch=True)
        if not result:
            return None

        row = result[0]

        # Parse settings if it's a string
        settings_data = row["settings"]
        if isinstance(settings_data, str):
            settings_data = json.loads(settings_data) if settings_data else {}

        # Create CustomerSettings object
        settings = CustomerSettings(
            plan=SubscriptionPlan.STARTUP,  # Default plan
            max_products=settings_data.get("max_products", 1),
            max_team_members=settings_data.get("max_team_members", 5),
            features_enabled=settings_data.get("features_enabled", []),
            custom_branding=settings_data.get("custom_branding", False),
            white_label=settings_data.get("white_label", False),
            on_premise=settings_data.get("on_premise", False),
            sso_enabled=settings_data.get("sso_enabled", False),
            audit_logging=settings_data.get("audit_logging", False),
        )

        return Customer(
            customer_id=str(row["id"]),
            email=row["email"],
            company_name=row["company_name"],
            status=CustomerStatus(row["status"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            settings=settings,
        )

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email address."""
        query = """
        SELECT id, email, company_name, status, created_at, updated_at, settings
        FROM customers WHERE email = %s
        """

        result = self.db_manager.execute_query(query, (email,), fetch=True)
        if not result:
            return None

        row = result[0]

        # Parse settings if it's a string
        settings_data = row["settings"]
        if isinstance(settings_data, str):
            settings_data = json.loads(settings_data) if settings_data else {}

        # Create CustomerSettings object
        settings = CustomerSettings(
            plan=SubscriptionPlan.STARTUP,  # Default plan
            max_products=settings_data.get("max_products", 1),
            max_team_members=settings_data.get("max_team_members", 5),
            features_enabled=settings_data.get("features_enabled", []),
            custom_branding=settings_data.get("custom_branding", False),
            white_label=settings_data.get("white_label", False),
            on_premise=settings_data.get("on_premise", False),
            sso_enabled=settings_data.get("sso_enabled", False),
            audit_logging=settings_data.get("audit_logging", False),
        )

        return Customer(
            customer_id=str(row["id"]),
            email=row["email"],
            company_name=row["company_name"],
            status=CustomerStatus(row["status"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            settings=settings,
        )

    def update_customer(self, customer: Customer) -> bool:
        """Update customer information."""
        try:
            customer.updated_at = datetime.now()
            self._save_customer(customer)
            self.logger.info(f"Customer updated: {customer.customer_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update customer {customer.customer_id}: {e}")
            return False

    def create_organization(
        self,
        customer_id: str,
        name: str,
        description: str = "",
        github_username: str = "",
        github_org: Optional[str] = None,
    ) -> Optional[Organization]:
        """
        Create a new organization for a customer.

        Args:
            customer_id: Customer ID
            name: Organization name
            description: Organization description
            github_username: GitHub username
            github_org: GitHub organization (optional)

        Returns:
            Organization object or None if customer not found
        """
        customer = self.get_customer(customer_id)
        if not customer:
            self.logger.error(f"Customer not found: {customer_id}")
            return None

        # Check if customer can create another organization
        current_orgs = self.get_customer_organizations(customer_id)
        if not customer.can_create_product(len(current_orgs)):
            self.logger.error(f"Customer {customer_id} has reached organization limit")
            return None

        self.logger.info(f"Creating organization '{name}' for customer {customer_id}")

        # Create organization
        organization = Organization(
            customer_id=customer_id,
            name=name,
            description=description,
            github_username=github_username,
            github_org=github_org,
            status=OrganizationStatus.CREATING,
        )

        # Save to database
        self._save_organization(organization)

        self.logger.info(f"Organization created: {organization.org_id}")
        return organization

    def get_customer_organizations(self, customer_id: str) -> List[Organization]:
        """Get all organizations for a customer."""
        # This would query the database in a real implementation
        # For now, return empty list as placeholder
        return []

    def get_organization(self, org_id: str) -> Optional[Organization]:
        """Get organization by ID."""
        return self._load_organization(org_id)

    def update_organization(self, organization: Organization) -> bool:
        """Update organization information."""
        try:
            organization.updated_at = datetime.now()
            self._save_organization(organization)
            self.logger.info(f"Organization updated: {organization.org_id}")
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to update organization {organization.org_id}: {e}"
            )
            return False

    def upgrade_subscription(
        self, customer_id: str, new_plan: SubscriptionPlan
    ) -> bool:
        """
        Upgrade customer subscription to a new plan.

        Args:
            customer_id: Customer ID
            new_plan: New subscription plan

        Returns:
            True if successful, False otherwise
        """
        customer = self.get_customer(customer_id)
        if not customer:
            self.logger.error(f"Customer not found: {customer_id}")
            return False

        old_plan = customer.plan
        self.logger.info(
            f"Upgrading customer {customer_id} from {old_plan.value} to {new_plan.value}"
        )

        # Update customer plan and settings
        customer.plan = new_plan
        customer.settings = customer.settings.__class__(
            new_plan, 1, 5
        )  # Reset with new plan
        customer.status = CustomerStatus.ACTIVE  # Move from trial to active

        # Update subscription
        subscription = self._get_customer_subscription(customer_id)
        if subscription:
            subscription.plan = new_plan
            subscription.status = "active"
            self._save_subscription(subscription)

        # Save customer
        success = self.update_customer(customer)

        if success:
            self.logger.info(f"Subscription upgraded successfully: {customer_id}")
        else:
            self.logger.error(f"Failed to upgrade subscription: {customer_id}")

        return success

    def cancel_subscription(self, customer_id: str) -> bool:
        """Cancel customer subscription."""
        customer = self.get_customer(customer_id)
        if not customer:
            self.logger.error(f"Customer not found: {customer_id}")
            return False

        self.logger.info(f"Cancelling subscription for customer: {customer_id}")

        # Update customer status
        customer.status = CustomerStatus.CANCELLED

        # Update subscription
        subscription = self._get_customer_subscription(customer_id)
        if subscription:
            subscription.cancel_at_period_end = True
            subscription.status = "cancelled"
            self._save_subscription(subscription)

        # Save customer
        success = self.update_customer(customer)

        if success:
            self.logger.info(f"Subscription cancelled: {customer_id}")
        else:
            self.logger.error(f"Failed to cancel subscription: {customer_id}")

        return success

    def track_usage(self, org_id: str, usage_type: str, amount: int = 1) -> bool:
        """
        Track usage metrics for billing.

        Args:
            org_id: Organization ID
            usage_type: Type of usage (deployments, api_calls, etc.)
            amount: Amount to add to usage

        Returns:
            True if successful, False otherwise
        """
        organization = self.get_organization(org_id)
        if not organization:
            self.logger.error(f"Organization not found: {org_id}")
            return False

        customer = self.get_customer(organization.customer_id)
        if not customer:
            self.logger.error(f"Customer not found for org: {org_id}")
            return False

        # Get or create usage metrics for current period
        usage = self._get_usage_metrics(org_id)
        if not usage:
            usage = UsageMetrics(org_id=org_id, customer_id=organization.customer_id)

        # Update usage based on type
        if usage_type == "deployments":
            usage.deployments_count += amount
        elif usage_type == "api_calls":
            usage.api_calls_count += amount
        elif usage_type == "storage":
            usage.storage_used_mb += amount
        elif usage_type == "team_members":
            usage.team_members_count += amount
        elif usage_type == "products":
            usage.products_count += amount
        elif usage_type == "webhook_calls":
            usage.webhook_calls_count += amount

        # Save usage metrics
        self._save_usage_metrics(usage)

        self.logger.debug(f"Usage tracked for {org_id}: {usage_type} += {amount}")
        return True

    def get_usage_metrics(self, org_id: str) -> Optional[UsageMetrics]:
        """Get usage metrics for an organization."""
        return self._get_usage_metrics(org_id)

    def get_customer_usage_summary(self, customer_id: str) -> Dict[str, Any]:
        """Get usage summary for all customer organizations."""
        organizations = self.get_customer_organizations(customer_id)

        total_usage = {
            "deployments_count": 0,
            "api_calls_count": 0,
            "storage_used_mb": 0,
            "team_members_count": 0,
            "products_count": 0,
            "webhook_calls_count": 0,
        }

        for org in organizations:
            usage = self.get_usage_metrics(org.org_id)
            if usage:
                total_usage["deployments_count"] += usage.deployments_count
                total_usage["api_calls_count"] += usage.api_calls_count
                total_usage["storage_used_mb"] += usage.storage_used_mb
                total_usage["team_members_count"] += usage.team_members_count
                total_usage["products_count"] += usage.products_count
                total_usage["webhook_calls_count"] += usage.webhook_calls_count

        return total_usage

    def is_trial_expired(self, customer_id: str) -> bool:
        """Check if customer trial has expired."""
        customer = self.get_customer(customer_id)
        if not customer:
            return True

        return not customer.is_trial_active()

    def get_trial_days_remaining(self, customer_id: str) -> int:
        """Get days remaining in trial period."""
        customer = self.get_customer(customer_id)
        if not customer or not customer.trial_ends_at:
            return 0

        delta = customer.trial_ends_at - datetime.now()
        return max(0, delta.days)

    # Database methods (placeholder implementations)
    def _init_database(self):
        """Initialize database connection and tables."""
        # This would set up the actual database in a real implementation
        # For now, just log that we're initializing
        self.logger.info("Initializing customer database...")

    def _save_customer(self, customer: Customer):
        """Save customer to database."""
        # Placeholder implementation
        self.logger.debug(f"Saving customer: {customer.customer_id}")

    def _load_customer(self, customer_id: str) -> Optional[Customer]:
        """Load customer from database."""
        # Placeholder implementation
        self.logger.debug(f"Loading customer: {customer_id}")
        return None

    def _save_organization(self, organization: Organization):
        """Save organization to database."""
        # Placeholder implementation
        self.logger.debug(f"Saving organization: {organization.org_id}")

    def _load_organization(self, org_id: str) -> Optional[Organization]:
        """Load organization from database."""
        # Placeholder implementation
        self.logger.debug(f"Loading organization: {org_id}")
        return None

    def _get_customer_subscription(self, customer_id: str) -> Optional[Subscription]:
        """Get customer subscription."""
        # Placeholder implementation
        return None

    def _save_subscription(self, subscription: Subscription):
        """Save subscription to database."""
        # Placeholder implementation
        self.logger.debug(f"Saving subscription: {subscription.subscription_id}")

    def _get_usage_metrics(self, org_id: str) -> Optional[UsageMetrics]:
        """Get usage metrics for organization."""
        # Placeholder implementation
        return None

    def _save_usage_metrics(self, usage: UsageMetrics):
        """Save usage metrics to database."""
        # Placeholder implementation
        self.logger.debug(f"Saving usage metrics for org: {usage.org_id}")
