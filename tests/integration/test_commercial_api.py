"""
Test Suite for Commercial API Infrastructure

This module provides comprehensive tests for the FastAPI-based commercial API,
ensuring all endpoints work correctly and follow REST principles.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime

# Import commercial API
from src.commercial.api import app
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


class TestCommercialAPI:
    """Test suite for Commercial API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client for API."""
        return TestClient(app)

    @pytest.fixture
    def mock_customer_manager(self):
        """Create mock customer manager."""
        manager = Mock(spec=CustomerManager)

        # Mock customer data
        mock_customer = Customer(
            customer_id="test_customer_123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.ACTIVE,
            plan=SubscriptionPlan.GROWTH,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        manager.create_customer.return_value = mock_customer
        manager.get_customer.return_value = mock_customer
        manager.get_customer_by_email.return_value = mock_customer

        return manager

    def test_health_check_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["version"] == "2.0.0"

    def test_create_customer_endpoint(self, client, mock_customer_manager):
        """Test customer creation endpoint."""
        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            customer_data = {
                "email": "newcustomer@example.com",
                "company_name": "New Company",
                "plan": "growth",
                "trial_days": 30,
            }

            response = client.post("/customers", json=customer_data)

            assert response.status_code == 201
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["company_name"] == "Test Company"
            assert data["status"] == "active"
            assert data["plan"] == "growth"

    def test_get_customer_endpoint(self, client, mock_customer_manager):
        """Test customer retrieval endpoint."""
        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/customers/test_customer_123")

            assert response.status_code == 200
            data = response.json()
            assert data["customer_id"] == "test_customer_123"
            assert data["email"] == "test@example.com"
            assert data["company_name"] == "Test Company"

    def test_get_customer_not_found(self, client, mock_customer_manager):
        """Test customer retrieval with non-existent ID."""
        mock_customer_manager.get_customer.return_value = None

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/customers/nonexistent_id")

            assert response.status_code == 404
            data = response.json()
            assert "not found" in data["detail"].lower()

    def test_create_customer_duplicate_email(self, client, mock_customer_manager):
        """Test customer creation with duplicate email."""
        mock_customer_manager.create_customer.side_effect = ValueError(
            "Customer with email test@example.com already exists"
        )

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            customer_data = {
                "email": "test@example.com",
                "company_name": "Duplicate Company",
                "plan": "startup",
            }

            response = client.post("/customers", json=customer_data)

            assert response.status_code == 400
            data = response.json()
            assert "already exists" in data["detail"]

    def test_create_customer_invalid_data(self, client):
        """Test customer creation with invalid data."""
        customer_data = {
            "email": "invalid-email",  # Invalid email format
            "company_name": "",  # Empty company name
            "plan": "invalid_plan",  # Invalid plan
        }

        response = client.post("/customers", json=customer_data)

        assert response.status_code == 422  # Validation error

    def test_list_customers_endpoint(self, client, mock_customer_manager):
        """Test customer listing endpoint."""
        # Mock multiple customers
        customers = [
            Customer(
                customer_id="customer_1",
                email="customer1@example.com",
                company_name="Company 1",
                status=CustomerStatus.ACTIVE,
                plan=SubscriptionPlan.STARTUP,
            ),
            Customer(
                customer_id="customer_2",
                email="customer2@example.com",
                company_name="Company 2",
                status=CustomerStatus.ACTIVE,
                plan=SubscriptionPlan.GROWTH,
            ),
        ]

        mock_customer_manager.list_customers.return_value = customers

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/customers")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["email"] == "customer1@example.com"
            assert data[1]["email"] == "customer2@example.com"

    def test_create_organization_endpoint(self, client, mock_customer_manager):
        """Test organization creation endpoint."""
        mock_organization = Organization(
            org_id="test_org_123",
            customer_id="test_customer_123",
            name="Test Organization",
            status=OrganizationStatus.CREATING,
        )

        mock_customer_manager.create_organization.return_value = mock_organization

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            org_data = {
                "customer_id": "test_customer_123",
                "name": "Test Organization",
                "description": "Test organization description",
            }

            response = client.post("/organizations", json=org_data)

            assert response.status_code == 201
            data = response.json()
            assert data["org_id"] == "test_org_123"
            assert data["customer_id"] == "test_customer_123"
            assert data["name"] == "Test Organization"
            assert data["status"] == "creating"

    def test_get_organization_endpoint(self, client, mock_customer_manager):
        """Test organization retrieval endpoint."""
        mock_organization = Organization(
            org_id="test_org_123",
            customer_id="test_customer_123",
            name="Test Organization",
            status=OrganizationStatus.ACTIVE,
        )

        mock_customer_manager.get_organization.return_value = mock_organization

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/organizations/test_org_123")

            assert response.status_code == 200
            data = response.json()
            assert data["org_id"] == "test_org_123"
            assert data["name"] == "Test Organization"
            assert data["status"] == "active"

    def test_deploy_organization_endpoint(self, client, mock_customer_manager):
        """Test organization deployment endpoint."""
        mock_customer_manager.deploy_organization.return_value = {
            "deployment_id": "deploy_123",
            "status": "success",
            "message": "Organization deployed successfully",
        }

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.post("/organizations/test_org_123/deploy")

            assert response.status_code == 200
            data = response.json()
            assert data["deployment_id"] == "deploy_123"
            assert data["status"] == "success"

    def test_get_usage_metrics_endpoint(self, client, mock_customer_manager):
        """Test usage metrics retrieval endpoint."""
        mock_metrics = [
            UsageMetrics(
                id="metric_1",
                customer_id="test_customer_123",
                organization_id="test_org_123",
                metric_name="deployments",
                metric_value=5.0,
                recorded_at=datetime.now(),
            ),
            UsageMetrics(
                id="metric_2",
                customer_id="test_customer_123",
                organization_id="test_org_123",
                metric_name="api_calls",
                metric_value=100.0,
                recorded_at=datetime.now(),
            ),
        ]

        mock_customer_manager.get_usage_metrics.return_value = mock_metrics

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/customers/test_customer_123/usage")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["metric_name"] == "deployments"
            assert data[0]["metric_value"] == 5.0
            assert data[1]["metric_name"] == "api_calls"
            assert data[1]["metric_value"] == 100.0

    def test_api_error_handling(self, client, mock_customer_manager):
        """Test API error handling."""
        mock_customer_manager.get_customer.side_effect = Exception(
            "Database connection failed"
        )

        with patch(
            "src.commercial.api.CustomerManager", return_value=mock_customer_manager
        ):
            response = client.get("/customers/test_customer_123")

            assert response.status_code == 500
            data = response.json()
            assert "error" in data
            assert "Database connection failed" in data["error"]


class TestAPIIntegration:
    """Integration tests for API with real services."""

    def test_customer_crud_workflow(self):
        """Test complete customer CRUD workflow through API."""
        client = TestClient(app)

        # Create customer
        customer_data = {
            "email": "crud@example.com",
            "company_name": "CRUD Company",
            "plan": "startup",
            "trial_days": 14,
        }

        create_response = client.post("/customers", json=customer_data)
        assert create_response.status_code == 201

        customer_id = create_response.json()["customer_id"]

        # Retrieve customer
        get_response = client.get(f"/customers/{customer_id}")
        assert get_response.status_code == 200

        retrieved_customer = get_response.json()
        assert retrieved_customer["email"] == "crud@example.com"
        assert retrieved_customer["company_name"] == "CRUD Company"

        # List customers
        list_response = client.get("/customers")
        assert list_response.status_code == 200

        customers = list_response.json()
        assert len(customers) >= 1
        assert any(c["customer_id"] == customer_id for c in customers)

    def test_organization_workflow(self):
        """Test organization creation and deployment workflow."""
        client = TestClient(app)

        # First create a customer
        customer_data = {
            "email": "orgworkflow@example.com",
            "company_name": "Org Workflow Company",
            "plan": "growth",
        }

        customer_response = client.post("/customers", json=customer_data)
        assert customer_response.status_code == 201
        customer_id = customer_response.json()["customer_id"]

        # Create organization
        org_data = {
            "customer_id": customer_id,
            "name": "Workflow Organization",
            "description": "Test organization for workflow",
        }

        org_response = client.post("/organizations", json=org_data)
        assert org_response.status_code == 201

        org_id = org_response.json()["org_id"]

        # Deploy organization
        deploy_response = client.post(f"/organizations/{org_id}/deploy")
        assert deploy_response.status_code == 200

        deployment_result = deploy_response.json()
        assert "deployment_id" in deployment_result
        assert deployment_result["status"] in ["success", "in_progress"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
