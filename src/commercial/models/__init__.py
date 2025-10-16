"""
Customer and Organization Models for Commercial SaaS Platform

This module defines the core data models for the multi-tenant commercial platform,
including customers, organizations, subscriptions, and billing.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from uuid import uuid4


class SubscriptionPlan(Enum):
    """Subscription plan tiers for the commercial platform."""

    STARTUP = "startup"  # $500/month - 1 product, 5 team members
    GROWTH = "growth"  # $2,000/month - 5 products, 20 team members
    SCALE = "scale"  # $5,000/month - 20 products, 100 team members
    ENTERPRISE = "enterprise"  # Custom - Unlimited, white-label, on-premise


class OrganizationStatus(Enum):
    """Status of organization deployment and health."""

    CREATING = "creating"  # Initial deployment in progress
    ACTIVE = "active"  # Fully deployed and operational
    SUSPENDED = "suspended"  # Temporarily suspended (billing issues)
    ARCHIVED = "archived"  # Permanently deactivated


class CustomerStatus(Enum):
    """Customer account status."""

    TRIAL = "trial"  # Free trial period
    ACTIVE = "active"  # Paid subscription active
    SUSPENDED = "suspended"  # Payment issues, suspended
    CANCELLED = "cancelled"  # Subscription cancelled


@dataclass
class CustomerSettings:
    """Customer-specific configuration and preferences."""

    plan: SubscriptionPlan
    max_products: int
    max_team_members: int
    features_enabled: List[str] = field(default_factory=list)
    custom_branding: bool = False
    white_label: bool = False
    on_premise: bool = False
    sso_enabled: bool = False
    audit_logging: bool = False

    def __post_init__(self):
        """Set plan-specific limits and features."""
        if self.plan == SubscriptionPlan.STARTUP:
            self.max_products = 1
            self.max_team_members = 5
            self.features_enabled = ["basic_templates", "github_integration"]
        elif self.plan == SubscriptionPlan.GROWTH:
            self.max_products = 5
            self.max_team_members = 20
            self.features_enabled = [
                "basic_templates",
                "github_integration",
                "api_access",
                "webhooks",
            ]
        elif self.plan == SubscriptionPlan.SCALE:
            self.max_products = 20
            self.max_team_members = 100
            self.features_enabled = [
                "all_templates",
                "github_integration",
                "api_access",
                "webhooks",
                "analytics",
            ]
        elif self.plan == SubscriptionPlan.ENTERPRISE:
            self.max_products = -1  # Unlimited
            self.max_team_members = -1  # Unlimited
            self.features_enabled = ["all_features"]
            self.custom_branding = True
            self.white_label = True
            self.on_premise = True
            self.sso_enabled = True
            self.audit_logging = True


@dataclass
class Customer:
    """Customer account for the commercial platform."""

    customer_id: str = field(default_factory=lambda: str(uuid4()))
    email: str = ""
    company_name: str = ""
    status: CustomerStatus = CustomerStatus.TRIAL
    plan: SubscriptionPlan = SubscriptionPlan.STARTUP
    settings: CustomerSettings = field(
        default_factory=lambda: CustomerSettings(SubscriptionPlan.STARTUP, 1, 5)
    )
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    trial_ends_at: Optional[datetime] = None
    billing_email: Optional[str] = None
    billing_address: Optional[Dict[str, str]] = None

    def __post_init__(self):
        """Initialize settings based on plan."""
        if not hasattr(self, "settings") or self.settings is None:
            self.settings = CustomerSettings(self.plan, 1, 5)
        else:
            # Update existing settings based on plan
            self.settings.plan = self.plan
            self.settings.__post_init__()

        # Set trial period for new customers
        if self.status == CustomerStatus.TRIAL and self.trial_ends_at is None:
            from datetime import timedelta

            self.trial_ends_at = self.created_at + timedelta(days=14)  # 14-day trial

    def is_trial_active(self) -> bool:
        """Check if customer is in active trial period."""
        if self.status != CustomerStatus.TRIAL:
            return False
        return self.trial_ends_at and datetime.now() < self.trial_ends_at

    def can_create_product(self, current_count: int) -> bool:
        """Check if customer can create another product."""
        if self.settings.max_products == -1:  # Unlimited
            return True
        return current_count < self.settings.max_products

    def can_add_team_member(self, current_count: int) -> bool:
        """Check if customer can add another team member."""
        if self.settings.max_team_members == -1:  # Unlimited
            return True
        return current_count < self.settings.max_team_members


@dataclass
class Organization:
    """Organization deployment within a customer account."""

    org_id: str = field(default_factory=lambda: str(uuid4()))
    customer_id: str = ""
    name: str = ""
    description: str = ""
    status: OrganizationStatus = OrganizationStatus.CREATING
    github_username: str = ""
    github_org: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    deployed_at: Optional[datetime] = None
    last_health_check: Optional[datetime] = None
    health_status: str = "unknown"
    configuration: Dict[str, Any] = field(default_factory=dict)

    def is_deployed(self) -> bool:
        """Check if organization is fully deployed."""
        return self.status == OrganizationStatus.ACTIVE and self.deployed_at is not None

    def get_base_path(self) -> str:
        """Get the base path for this organization's resources."""
        return f"organizations/{self.org_id}"

    def get_meta_repo_path(self) -> str:
        """Get the path to the organization's meta-repo."""
        return f"{self.get_base_path()}/meta-repo"

    def get_cloud_storage_path(self) -> str:
        """Get the path to the organization's cloud storage."""
        return f"{self.get_base_path()}/cloud-storage"


@dataclass
class Subscription:
    """Subscription details for billing and usage tracking."""

    subscription_id: str = field(default_factory=lambda: str(uuid4()))
    customer_id: str = ""
    plan: SubscriptionPlan = SubscriptionPlan.STARTUP
    status: str = "active"
    current_period_start: datetime = field(default_factory=datetime.now)
    current_period_end: datetime = field(default_factory=lambda: datetime.now())
    cancel_at_period_end: bool = False
    trial_end: Optional[datetime] = None
    usage_this_period: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        """Set period end date."""
        if self.current_period_end == datetime.now():
            from datetime import timedelta

            self.current_period_end = self.current_period_start + timedelta(
                days=30
            )  # Monthly billing

    def is_active(self) -> bool:
        """Check if subscription is currently active."""
        return self.status == "active" and datetime.now() < self.current_period_end

    def days_remaining(self) -> int:
        """Get days remaining in current billing period."""
        if not self.is_active():
            return 0
        delta = self.current_period_end - datetime.now()
        return max(0, delta.days)


@dataclass
class UsageMetrics:
    """Usage metrics for billing and analytics."""

    org_id: str = ""
    customer_id: str = ""
    period_start: datetime = field(default_factory=datetime.now)
    period_end: datetime = field(default_factory=lambda: datetime.now())
    deployments_count: int = 0
    api_calls_count: int = 0
    storage_used_mb: int = 0
    team_members_count: int = 0
    products_count: int = 0
    webhook_calls_count: int = 0

    def __post_init__(self):
        """Set period end date."""
        if self.period_end == datetime.now():
            from datetime import timedelta

            self.period_end = self.period_start + timedelta(days=30)  # Monthly period

    def get_total_usage_cost(self, plan: SubscriptionPlan) -> float:
        """Calculate total usage cost based on plan pricing."""
        # Base pricing per plan
        base_costs = {
            SubscriptionPlan.STARTUP: 500.0,
            SubscriptionPlan.GROWTH: 2000.0,
            SubscriptionPlan.SCALE: 5000.0,
            SubscriptionPlan.ENTERPRISE: 0.0,  # Custom pricing
        }

        base_cost = base_costs.get(plan, 500.0)

        # Add overage costs if applicable
        overage_cost = 0.0
        if plan != SubscriptionPlan.ENTERPRISE:
            # Example overage pricing
            if self.api_calls_count > 10000:  # 10K calls included
                overage_cost += (self.api_calls_count - 10000) * 0.01  # $0.01 per call
            if self.storage_used_mb > 1000:  # 1GB included
                overage_cost += (self.storage_used_mb - 1000) * 0.10  # $0.10 per MB

        return base_cost + overage_cost
