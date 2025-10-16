"""
Test Suite for Commercial Database Infrastructure

This module provides comprehensive tests for the PostgreSQL database integration,
following TDD principles and ensuring robust commercial infrastructure.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from pathlib import Path

# Import commercial modules
from src.commercial.database import DatabaseManager, get_db_manager
from src.commercial.models import (
    Customer,
    Organization,
    Subscription,
    UsageMetrics,
    CustomerStatus,
    SubscriptionPlan,
    OrganizationStatus,
    CustomerSettings,
)
from src.commercial.services.customer_manager import CustomerManager


class TestDatabaseManager:
    """Test suite for DatabaseManager class."""

    def test_database_manager_initialization_with_url(self):
        """Test DatabaseManager initialization with database URL."""
        with patch("src.commercial.database.SimpleConnectionPool") as mock_pool_class, \
             patch("src.commercial.database.DatabaseManager._create_tables"):
            mock_pool_instance = MagicMock()
            mock_pool_class.return_value = mock_pool_instance
            
            db_manager = DatabaseManager("postgresql://test:test@localhost/test")
            assert db_manager.database_url == "postgresql://test:test@localhost/test"
            assert db_manager.pool is not None

    def test_database_manager_initialization_without_url(self):
        """Test DatabaseManager initialization without database URL."""
        db_manager = DatabaseManager()
        assert db_manager.database_url is None
        assert db_manager.pool is None

    def test_database_manager_initialization_with_env_var(self):
        """Test DatabaseManager initialization with DATABASE_URL env var."""
        with patch.dict(
            "os.environ", {"DATABASE_URL": "postgresql://env:test@localhost/test"}
        ):
            with patch("psycopg2.pool.SimpleConnectionPool") as mock_pool:
                db_manager = DatabaseManager()
                assert db_manager.database_url == "postgresql://env:test@localhost/test"

    def test_execute_query_with_pool(self):
        """Test execute_query with active connection pool."""
        with patch("src.commercial.database.SimpleConnectionPool") as mock_pool_class:
            mock_pool = MagicMock()
            mock_pool_class.return_value = mock_pool

            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_cursor.fetchall.return_value = [{"id": "test", "name": "test"}]
            mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
            mock_pool.getconn.return_value.__enter__.return_value = mock_conn

            db_manager = DatabaseManager("postgresql://test:test@localhost/test")

            # Mock the _create_tables method to avoid table creation
            with patch.object(db_manager, "_create_tables"):
                result = db_manager.execute_query("SELECT * FROM test", fetch=True)

                assert result == [{"id": "test", "name": "test"}]
                # Check that execute was called with our query (not table creation)
                mock_cursor.execute.assert_called_with("SELECT * FROM test", None)

    def test_execute_query_without_pool(self):
        """Test execute_query without connection pool (in-memory fallback)."""
        db_manager = DatabaseManager()

        # Test INSERT query
        result = db_manager.execute_query(
            "INSERT INTO customers (email, company_name, status, settings) VALUES (%s, %s, %s, %s)",
            ("test@example.com", "Test Company", "active", "{}"),
            fetch=True,
        )

        assert len(result) == 1
        assert result[0]["email"] == "test@example.com"
        assert result[0]["company_name"] == "Test Company"

    def test_execute_query_select_customers(self):
        """Test SELECT query for customers."""
        db_manager = DatabaseManager()

        # First insert a customer
        db_manager.execute_query(
            "INSERT INTO customers (email, company_name, status, settings) VALUES (%s, %s, %s, %s)",
            ("test@example.com", "Test Company", "active", "{}"),
        )

        # Then select it
        result = db_manager.execute_query(
            "SELECT id, email, company_name, status, created_at, updated_at, settings FROM customers WHERE email = %s",
            ("test@example.com",),
            fetch=True,
        )

        assert len(result) == 1
        assert result[0]["email"] == "test@example.com"

    def test_execute_query_insert_subscription(self):
        """Test INSERT query for subscriptions."""
        db_manager = DatabaseManager()

        result = db_manager.execute_query(
            "INSERT INTO subscriptions (customer_id, plan, status, start_date, end_date) VALUES (%s, %s, %s, %s, %s)",
            ("cust_1", "growth", "active", datetime.now(), None),
            fetch=True,
        )

        assert len(result) == 1
        assert result[0]["customer_id"] == "cust_1"
        assert result[0]["plan"] == "growth"


class TestCustomerManager:
    """Test suite for CustomerManager class."""

    @pytest.fixture
    def customer_manager(self):
        """Create CustomerManager instance for testing."""
        return CustomerManager()

    def test_create_customer_success(self, customer_manager):
        """Test successful customer creation."""
        customer = customer_manager.create_customer(
            email="test@example.com",
            company_name="Test Company",
            plan=SubscriptionPlan.GROWTH,
            trial_days=30,
        )

        assert customer.email == "test@example.com"
        assert customer.company_name == "Test Company"
        assert customer.status == CustomerStatus.ACTIVE
        assert customer.plan == SubscriptionPlan.GROWTH
        assert isinstance(customer.settings, CustomerSettings)

    def test_create_customer_duplicate_email(self, customer_manager):
        """Test customer creation with duplicate email raises error."""
        # Create first customer
        customer_manager.create_customer(
            email="duplicate@example.com", company_name="First Company"
        )

        # Try to create second customer with same email
        with pytest.raises(ValueError, match="already exists"):
            customer_manager.create_customer(
                email="duplicate@example.com", company_name="Second Company"
            )

    def test_get_customer_by_email_success(self, customer_manager):
        """Test successful customer retrieval by email."""
        # Create customer first
        created_customer = customer_manager.create_customer(
            email="retrieve@example.com", company_name="Retrieve Company"
        )

        # Retrieve customer
        retrieved_customer = customer_manager.get_customer_by_email(
            "retrieve@example.com"
        )

        assert retrieved_customer is not None
        assert retrieved_customer.email == "retrieve@example.com"
        assert retrieved_customer.company_name == "Retrieve Company"
        assert retrieved_customer.customer_id == created_customer.customer_id

    def test_get_customer_by_email_not_found(self, customer_manager):
        """Test customer retrieval with non-existent email."""
        customer = customer_manager.get_customer_by_email("nonexistent@example.com")
        assert customer is None

    def test_get_customer_by_id_success(self, customer_manager):
        """Test successful customer retrieval by ID."""
        # Create customer first
        created_customer = customer_manager.create_customer(
            email="idtest@example.com", company_name="ID Test Company"
        )

        # Retrieve customer by ID
        retrieved_customer = customer_manager.get_customer(created_customer.customer_id)

        assert retrieved_customer is not None
        assert retrieved_customer.customer_id == created_customer.customer_id
        assert retrieved_customer.email == "idtest@example.com"

    def test_get_customer_by_id_not_found(self, customer_manager):
        """Test customer retrieval with non-existent ID."""
        customer = customer_manager.get_customer("nonexistent_id")
        assert customer is None

    def test_create_subscription(self, customer_manager):
        """Test subscription creation."""
        # Create customer first
        customer = customer_manager.create_customer(
            email="subscription@example.com", company_name="Subscription Company"
        )

        # Verify subscription was created (this is called internally)
        # We can test by checking the database directly
        subscriptions = customer_manager.db_manager.execute_query(
            "SELECT * FROM subscriptions WHERE customer_id = %s",
            (customer.customer_id,),
            fetch=True,
        )

        assert len(subscriptions) == 1
        assert subscriptions[0]["customer_id"] == customer.customer_id
        assert subscriptions[0]["plan"] == SubscriptionPlan.STARTUP.value


class TestCommercialModels:
    """Test suite for commercial models."""

    def test_customer_model_creation(self):
        """Test Customer model creation and initialization."""
        customer = Customer(
            email="model@example.com",
            company_name="Model Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.GROWTH,
        )

        assert customer.email == "model@example.com"
        assert customer.company_name == "Model Company"
        assert customer.status == CustomerStatus.ACTIVE
        assert customer.plan == SubscriptionPlan.GROWTH
        assert isinstance(customer.settings, CustomerSettings)
        assert customer.settings.max_products == 5  # Growth plan limit
        assert customer.settings.max_team_members == 20  # Growth plan limit

    def test_customer_settings_startup_plan(self):
        """Test CustomerSettings initialization for STARTUP plan."""
        settings = CustomerSettings(
            plan=SubscriptionPlan.STARTUP, max_products=1, max_team_members=5
        )

        assert settings.plan == SubscriptionPlan.STARTUP
        assert settings.max_products == 1
        assert settings.max_team_members == 5
        assert "basic_templates" in settings.features_enabled
        assert "github_integration" in settings.features_enabled
        assert not settings.custom_branding
        assert not settings.white_label

    def test_customer_settings_enterprise_plan(self):
        """Test CustomerSettings initialization for ENTERPRISE plan."""
        settings = CustomerSettings(
            plan=SubscriptionPlan.ENTERPRISE, max_products=-1, max_team_members=-1
        )

        assert settings.plan == SubscriptionPlan.ENTERPRISE
        assert settings.max_products == -1  # Unlimited
        assert settings.max_team_members == -1  # Unlimited
        assert "all_features" in settings.features_enabled
        assert settings.custom_branding
        assert settings.white_label
        assert settings.on_premise
        assert settings.sso_enabled
        assert settings.audit_logging

    def test_organization_model_creation(self):
        """Test Organization model creation."""
        org = Organization(
            org_id="test_org_123",
            customer_id="cust_123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
        )

        assert org.org_id == "test_org_123"
        assert org.customer_id == "cust_123"
        assert org.name == "Test Organization"
        assert org.status == OrganizationStatus.CREATING
        assert org.get_base_path() == "organizations/test_org_123"
        assert org.get_meta_repo_path() == "organizations/test_org_123/meta-repo"

    def test_organization_is_deployed(self):
        """Test Organization deployment status checking."""
        # Not deployed
        org_creating = Organization(
            org_id="test_org_creating",
            customer_id="cust_123",
            name="Creating Org",
            status=OrganizationStatus.CREATING,
        )
        assert not org_creating.is_deployed()

        # Deployed
        org_deployed = Organization(
            org_id="test_org_deployed",
            customer_id="cust_123",
            name="Deployed Org",
            status=OrganizationStatus.ACTIVE,
            deployed_at=datetime.now(),
        )
        assert org_deployed.is_deployed()


class TestCommercialIntegration:
    """Integration tests for commercial infrastructure."""

    def test_customer_lifecycle_integration(self):
        """Test complete customer lifecycle."""
        customer_manager = CustomerManager()

        # Create customer
        customer = customer_manager.create_customer(
            email="lifecycle@example.com",
            company_name="Lifecycle Company",
            plan=SubscriptionPlan.SCALE,
            trial_days=14,
        )

        # Verify customer exists
        assert customer.customer_id is not None
        assert customer.status == CustomerStatus.ACTIVE

        # Retrieve customer
        retrieved = customer_manager.get_customer_by_email("lifecycle@example.com")
        assert retrieved.customer_id == customer.customer_id

        # Verify subscription exists
        subscriptions = customer_manager.db_manager.execute_query(
            "SELECT * FROM subscriptions WHERE customer_id = %s",
            (customer.customer_id,),
            fetch=True,
        )
        assert len(subscriptions) == 1
        assert subscriptions[0]["plan"] == SubscriptionPlan.SCALE.value

    def test_plan_based_feature_gating(self):
        """Test plan-based feature gating."""
        # Test STARTUP plan
        startup_customer = Customer(
            email="startup@example.com",
            company_name="Startup Company",
            plan=SubscriptionPlan.STARTUP,
        )

        assert startup_customer.settings.max_products == 1
        assert startup_customer.settings.max_team_members == 5
        assert "basic_templates" in startup_customer.settings.features_enabled
        assert "api_access" not in startup_customer.settings.features_enabled

        # Test GROWTH plan
        growth_customer = Customer(
            email="growth@example.com",
            company_name="Growth Company",
            plan=SubscriptionPlan.GROWTH,
        )

        assert growth_customer.settings.max_products == 5
        assert growth_customer.settings.max_team_members == 20
        assert "api_access" in growth_customer.settings.features_enabled
        assert "webhooks" in growth_customer.settings.features_enabled


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
