#!/usr/bin/env python3
"""
Commercial CLI for Meta-Repo-Seed SaaS Platform

This script provides command-line access to the commercial platform,
enabling customers to manage their organizations and deployments.
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from commercial import (
    CustomerManager,
    OrganizationSeeder,
    Customer,
    Organization,
    SubscriptionPlan,
    CustomerStatus,
)


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def create_customer_command(args):
    """Create a new customer account."""
    logger = logging.getLogger(__name__)

    customer_manager = CustomerManager()

    logger.info(f"Creating customer: {args.email} ({args.company})")

    try:
        customer = customer_manager.create_customer(
            email=args.email,
            company_name=args.company,
            plan=SubscriptionPlan(args.plan),
            trial_days=args.trial_days,
        )

        print(f"✅ Customer created successfully!")
        print(f"   Customer ID: {customer.customer_id}")
        print(f"   Email: {customer.email}")
        print(f"   Company: {customer.company_name}")
        print(f"   Plan: {customer.plan.value}")
        print(f"   Status: {customer.status.value}")
        print(f"   Trial ends: {customer.trial_ends_at}")

        return 0

    except Exception as e:
        logger.error(f"Failed to create customer: {e}")
        return 1


def create_organization_command(args):
    """Create a new organization for a customer."""
    logger = logging.getLogger(__name__)

    customer_manager = CustomerManager()

    logger.info(f"Creating organization '{args.name}' for customer {args.customer_id}")

    try:
        # Get customer first
        customer = customer_manager.get_customer(args.customer_id)
        if not customer:
            logger.error(f"Customer not found: {args.customer_id}")
            return 1

        organization = customer_manager.create_organization(
            customer_id=args.customer_id,
            name=args.name,
            description=args.description,
            github_username=args.github_username,
            github_org=args.github_org,
        )

        if not organization:
            logger.error("Failed to create organization")
            return 1

        print(f"✅ Organization created successfully!")
        print(f"   Organization ID: {organization.org_id}")
        print(f"   Name: {organization.name}")
        print(f"   Customer ID: {organization.customer_id}")
        print(f"   GitHub Username: {organization.github_username}")
        print(f"   Status: {organization.status.value}")

        return 0

    except Exception as e:
        logger.error(f"Failed to create organization: {e}")
        return 1


def deploy_organization_command(args):
    """Deploy organization infrastructure."""
    logger = logging.getLogger(__name__)

    customer_manager = CustomerManager()

    logger.info(f"Deploying organization {args.org_id}")

    try:
        # Get organization and customer
        organization = customer_manager.get_organization(args.org_id)
        if not organization:
            logger.error(f"Organization not found: {args.org_id}")
            return 1

        customer = customer_manager.get_customer(organization.customer_id)
        if not customer:
            logger.error(f"Customer not found: {organization.customer_id}")
            return 1

        # Create organization seeder
        seeder = OrganizationSeeder(
            org_id=args.org_id,
            customer=customer,
            organization=organization,
            dry_run=args.dry_run,
        )

        # Deploy organization
        success = seeder.deploy_organization()

        if success:
            print(f"✅ Organization deployed successfully!")
            print(f"   Organization ID: {args.org_id}")
            print(f"   Status: {organization.status.value}")
            print(f"   Health: {organization.health_status}")

            # Track usage
            customer_manager.track_usage(args.org_id, "deployments", 1)

            return 0
        else:
            logger.error("Organization deployment failed")
            return 1

    except Exception as e:
        logger.error(f"Failed to deploy organization: {e}")
        return 1


def upgrade_subscription_command(args):
    """Upgrade customer subscription."""
    logger = logging.getLogger(__name__)

    customer_manager = CustomerManager()

    logger.info(f"Upgrading customer {args.customer_id} to {args.plan}")

    try:
        success = customer_manager.upgrade_subscription(
            customer_id=args.customer_id, new_plan=SubscriptionPlan(args.plan)
        )

        if success:
            print(f"✅ Subscription upgraded successfully!")
            print(f"   Customer ID: {args.customer_id}")
            print(f"   New Plan: {args.plan}")

            return 0
        else:
            logger.error("Failed to upgrade subscription")
            return 1

    except Exception as e:
        logger.error(f"Failed to upgrade subscription: {e}")
        return 1


def get_usage_command(args):
    """Get usage metrics for organization or customer."""
    logger = logging.getLogger(__name__)

    customer_manager = CustomerManager()

    if args.org_id:
        logger.info(f"Getting usage metrics for organization {args.org_id}")

        usage = customer_manager.get_usage_metrics(args.org_id)
        if not usage:
            print("No usage metrics found for this organization")
            return 0

        print(f"📊 Usage Metrics for Organization {args.org_id}")
        print(f"   Deployments: {usage.deployments_count}")
        print(f"   API Calls: {usage.api_calls_count}")
        print(f"   Storage Used: {usage.storage_used_mb} MB")
        print(f"   Team Members: {usage.team_members_count}")
        print(f"   Products: {usage.products_count}")
        print(f"   Webhook Calls: {usage.webhook_calls_count}")

    elif args.customer_id:
        logger.info(f"Getting usage summary for customer {args.customer_id}")

        usage_summary = customer_manager.get_customer_usage_summary(args.customer_id)

        print(f"📊 Usage Summary for Customer {args.customer_id}")
        for metric, value in usage_summary.items():
            print(f"   {metric.replace('_', ' ').title()}: {value}")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Commercial CLI for Meta-Repo-Seed SaaS Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a new customer
  python commercial_cli.py create-customer --email user@company.com --company "My Company" --plan startup

  # Create an organization
  python commercial_cli.py create-org --customer-id CUSTOMER_ID --name "My Org" --github-username myuser

  # Deploy organization
  python commercial_cli.py deploy --org-id ORG_ID

  # Upgrade subscription
  python commercial_cli.py upgrade --customer-id CUSTOMER_ID --plan growth

  # Get usage metrics
  python commercial_cli.py usage --org-id ORG_ID
        """,
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create customer command
    create_customer_parser = subparsers.add_parser(
        "create-customer", help="Create a new customer"
    )
    create_customer_parser.add_argument("--email", required=True, help="Customer email")
    create_customer_parser.add_argument("--company", required=True, help="Company name")
    create_customer_parser.add_argument(
        "--plan",
        choices=["startup", "growth", "scale", "enterprise"],
        default="startup",
        help="Subscription plan",
    )
    create_customer_parser.add_argument(
        "--trial-days", type=int, default=14, help="Trial period in days"
    )

    # Create organization command
    create_org_parser = subparsers.add_parser(
        "create-org", help="Create a new organization"
    )
    create_org_parser.add_argument("--customer-id", required=True, help="Customer ID")
    create_org_parser.add_argument("--name", required=True, help="Organization name")
    create_org_parser.add_argument(
        "--description", default="", help="Organization description"
    )
    create_org_parser.add_argument(
        "--github-username", default="", help="GitHub username"
    )
    create_org_parser.add_argument("--github-org", help="GitHub organization")

    # Deploy organization command
    deploy_parser = subparsers.add_parser(
        "deploy", help="Deploy organization infrastructure"
    )
    deploy_parser.add_argument("--org-id", required=True, help="Organization ID")
    deploy_parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without making them"
    )

    # Upgrade subscription command
    upgrade_parser = subparsers.add_parser(
        "upgrade", help="Upgrade customer subscription"
    )
    upgrade_parser.add_argument("--customer-id", required=True, help="Customer ID")
    upgrade_parser.add_argument(
        "--plan",
        choices=["startup", "growth", "scale", "enterprise"],
        required=True,
        help="New subscription plan",
    )

    # Usage metrics command
    usage_parser = subparsers.add_parser("usage", help="Get usage metrics")
    usage_group = usage_parser.add_mutually_exclusive_group(required=True)
    usage_group.add_argument("--org-id", help="Organization ID")
    usage_group.add_argument("--customer-id", help="Customer ID")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Set up logging
    logger = setup_logging(args.verbose)

    # Execute command
    try:
        if args.command == "create-customer":
            return create_customer_command(args)
        elif args.command == "create-org":
            return create_organization_command(args)
        elif args.command == "deploy":
            return deploy_organization_command(args)
        elif args.command == "upgrade":
            return upgrade_subscription_command(args)
        elif args.command == "usage":
            return get_usage_command(args)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
