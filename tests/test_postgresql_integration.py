#!/usr/bin/env python3
"""
Test PostgreSQL Database Integration

This script tests the PostgreSQL database integration for the commercial
infrastructure, verifying that customer management works with persistent storage.
"""

import os
import sys
import logging
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from commercial import CustomerManager, SubscriptionPlan, CustomerStatus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_postgresql_integration():
    """Test PostgreSQL database integration."""
    logger.info("Testing PostgreSQL database integration...")

    # Initialize customer manager
    customer_manager = CustomerManager()

    # Test customer creation
    try:
        customer = customer_manager.create_customer(
            email="test@clemnova.com",
            company_name="ClemNova Test",
            plan=SubscriptionPlan.GROWTH,
            trial_days=30,
        )

        logger.info(f"✅ Customer created: {customer.customer_id}")
        logger.info(f"   Email: {customer.email}")
        logger.info(f"   Company: {customer.company_name}")
        logger.info(f"   Status: {customer.status}")

        # Test customer retrieval
        retrieved_customer = customer_manager.get_customer_by_email("test@clemnova.com")
        if retrieved_customer:
            logger.info(f"✅ Customer retrieved: {retrieved_customer.customer_id}")
            logger.info(f"   Email: {retrieved_customer.email}")
            logger.info(f"   Company: {retrieved_customer.company_name}")
        else:
            logger.error("❌ Failed to retrieve customer")
            return False

        # Test duplicate customer creation
        try:
            duplicate_customer = customer_manager.create_customer(
                email="test@clemnova.com",
                company_name="Duplicate Test",
                plan=SubscriptionPlan.STARTUP,
            )
            logger.error("❌ Should not have created duplicate customer")
            return False
        except ValueError as e:
            logger.info(f"✅ Correctly prevented duplicate customer: {e}")

        logger.info("✅ PostgreSQL integration test passed!")
        return True

    except Exception as e:
        logger.error(f"❌ PostgreSQL integration test failed: {e}")
        return False


def test_in_memory_fallback():
    """Test in-memory fallback when PostgreSQL is not available."""
    logger.info("Testing in-memory fallback...")

    # Set environment to force in-memory mode
    os.environ.pop("DATABASE_URL", None)

    customer_manager = CustomerManager()

    try:
        customer = customer_manager.create_customer(
            email="fallback@test.com",
            company_name="Fallback Test",
            plan=SubscriptionPlan.STARTUP,
        )

        logger.info(f"✅ In-memory fallback worked: {customer.customer_id}")
        return True

    except Exception as e:
        logger.error(f"❌ In-memory fallback failed: {e}")
        return False


if __name__ == "__main__":
    logger.info("Starting PostgreSQL integration tests...")

    # Test PostgreSQL integration
    postgresql_success = test_postgresql_integration()

    # Test in-memory fallback
    fallback_success = test_in_memory_fallback()

    if postgresql_success and fallback_success:
        logger.info("🎉 All tests passed! PostgreSQL integration is working.")
        sys.exit(0)
    else:
        logger.error("💥 Some tests failed. Check the logs above.")
        sys.exit(1)
