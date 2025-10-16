"""
Commercial SaaS Infrastructure for Meta-Repo-Seed

This package provides multi-tenant, commercial-ready infrastructure for the
Business-in-a-Box platform, enabling SaaS deployment and customer management.

Key Components:
- OrganizationSeeder: Multi-tenant organization deployment
- CustomerManager: Customer lifecycle and subscription management
- OrganizationConfig: Per-customer configuration and settings
- CommercialAPI: REST API for programmatic access
- Models: Customer, Organization, Subscription, UsageMetrics

Author: ChrisClements1987
"""

__version__ = "2.0.0"
__author__ = "ChrisClements1987"

# Import main components for easy access
try:
    from .models import (
        Customer,
        Organization,
        Subscription,
        UsageMetrics,
        CustomerStatus,
        SubscriptionPlan,
        OrganizationStatus,
        CustomerSettings,
    )
    from .services.organization_seeder import OrganizationSeeder, OrganizationConfig
    from .services.customer_manager import CustomerManager
    from .api import app as CommercialAPI

    __all__ = [
        "OrganizationSeeder",
        "CustomerManager",
        "Customer",
        "Organization",
        "Subscription",
        "UsageMetrics",
        "CustomerStatus",
        "SubscriptionPlan",
        "OrganizationStatus",
        "CustomerSettings",
        "OrganizationConfig",
        "CommercialAPI",
    ]
except ImportError:
    # Allow package to be imported even if dependencies aren't installed
    __all__ = []
