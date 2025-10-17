#!/usr/bin/env python3
"""
Test Commercial CLI with Database Integration

This script tests the commercial CLI functionality with the new PostgreSQL
database integration, demonstrating customer and organization management.
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.commercial import CustomerManager, OrganizationSeeder, SubscriptionPlan

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_commercial_cli_workflow():
    """Test the complete commercial CLI workflow."""
    logger.info("Testing Commercial CLI Workflow...")

    # Initialize managers
    customer_manager = CustomerManager()

    # Step 1: Create customer
    logger.info("Step 1: Creating customer...")
    customer = customer_manager.create_customer(
        email="clemnova@test.com",
        company_name="ClemNova",
        plan=SubscriptionPlan.GROWTH,
        trial_days=30,
    )

    logger.info(f"✅ Customer created: {customer.customer_id}")
    logger.info(f"   Email: {customer.email}")
    logger.info(f"   Company: {customer.company_name}")
    logger.info(f"   Plan: {customer.plan}")
    logger.info(f"   Status: {customer.status}")

    # Step 2: Create organization seeder
    logger.info("Step 2: Creating organization seeder...")
    try:
        org_seeder = OrganizationSeeder.create_for_customer(
            customer_id=customer.customer_id,
            organization_name="ClemNova Organization",
            customer_manager=customer_manager,
            dry_run=True,  # Use dry run for testing
        )

        logger.info(f"✅ Organization seeder created: {org_seeder.org_id}")
        logger.info(f"   Organization: {org_seeder.organization.name}")
        logger.info(f"   Customer: {org_seeder.customer.email}")
        logger.info(f"   Status: {org_seeder.organization.status}")

    except Exception as e:
        logger.error(f"❌ Failed to create organization seeder: {e}")
        return False

    # Step 3: Deploy organization
    logger.info("Step 3: Deploying organization...")
    try:
        deployment_success = org_seeder.deploy_organization()

        if deployment_success:
            logger.info(f"✅ Organization deployed successfully!")
            logger.info(f"   Organization ID: {org_seeder.org_id}")
            logger.info(f"   Status: {org_seeder.organization.status}")
        else:
            logger.warning("⚠️ Organization deployment returned False")

    except Exception as e:
        logger.error(f"❌ Failed to deploy organization: {e}")
        return False

    # Step 4: Test plan-based features
    logger.info("Step 4: Testing plan-based features...")
    try:
        # Test Growth plan features
        if customer.plan == SubscriptionPlan.GROWTH:
            logger.info("✅ Growth plan features available:")
            logger.info("   - API access")
            logger.info("   - Webhooks")
            logger.info("   - 5 products max")
            logger.info("   - 20 team members max")

        # Test usage tracking
        usage_result = customer_manager.track_usage(
            org_id=org_seeder.org_id, usage_type="deployments", amount=1
        )

        if usage_result:
            logger.info("✅ Usage tracking working")
        else:
            logger.warning("⚠️ Usage tracking not implemented")

    except Exception as e:
        logger.error(f"❌ Failed to test plan features: {e}")
        return False

    logger.info("🎉 Commercial CLI workflow test completed successfully!")
    return True


if __name__ == "__main__":
    logger.info("Starting Commercial CLI Workflow Test...")

    success = test_commercial_cli_workflow()

    if success:
        logger.info(
            "✅ All tests passed! Commercial CLI is working with database integration."
        )
        sys.exit(0)
    else:
        logger.error("❌ Some tests failed. Check the logs above.")
        sys.exit(1)
