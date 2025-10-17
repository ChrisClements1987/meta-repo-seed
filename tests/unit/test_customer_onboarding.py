"""
Tests for Customer Onboarding Workflow

This module tests the automated customer onboarding process including
welcome emails, default organization creation, and profile setup.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from src.commercial.models import (
    Customer,
    Organization,
    CustomerStatus,
    SubscriptionPlan,
    OrganizationStatus,
)
from src.commercial.services.onboarding_manager import (
    OnboardingManager,
    OnboardingStep,
    OnboardingStatus,
)
from src.commercial.services.email_service import EmailService
from src.commercial.services.customer_manager import CustomerManager


class TestOnboardingManager:
    """Test cases for OnboardingManager."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_customer_manager = Mock(spec=CustomerManager)
        self.mock_email_service = Mock(spec=EmailService)
        
        # Create onboarding manager with mocked dependencies
        self.onboarding_manager = OnboardingManager(self.mock_customer_manager)
        self.onboarding_manager.email_service = self.mock_email_service
        
        # Create test customer
        self.test_customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company",
            status=CustomerStatus.TRIAL,
            plan=SubscriptionPlan.STARTUP,
        )
    
    def test_start_onboarding_success(self):
        """Test successful onboarding process start."""
        # Mock successful email sending
        self.mock_email_service.send_template_email.return_value = True
        
        # Mock successful organization creation
        mock_org = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Company-main",
            status=OrganizationStatus.CREATING
        )
        self.mock_customer_manager.create_organization.return_value = mock_org
        
        # Mock scheduling follow-up email
        with patch.object(self.onboarding_manager, '_schedule_followup_email', return_value=True):
            with patch.object(self.onboarding_manager, '_update_onboarding_status'):
                result = self.onboarding_manager.start_onboarding(self.test_customer)
        
        assert result is True
        self.mock_email_service.send_template_email.assert_called_once()
        self.mock_customer_manager.create_organization.assert_called_once()
    
    def test_start_onboarding_email_failure(self):
        """Test onboarding failure when email sending fails."""
        # Mock email sending failure
        self.mock_email_service.send_template_email.return_value = False
        
        result = self.onboarding_manager.start_onboarding(self.test_customer)
        
        assert result is False
        self.mock_email_service.send_template_email.assert_called_once()
        # Organization creation should not be called if email fails
        self.mock_customer_manager.create_organization.assert_not_called()
    
    def test_start_onboarding_organization_creation_failure(self):
        """Test onboarding failure when organization creation fails."""
        # Mock successful email sending
        self.mock_email_service.send_template_email.return_value = True
        
        # Mock organization creation failure
        self.mock_customer_manager.create_organization.return_value = None
        
        result = self.onboarding_manager.start_onboarding(self.test_customer)
        
        assert result is False
        self.mock_email_service.send_template_email.assert_called_once()
        self.mock_customer_manager.create_organization.assert_called_once()
    
    def test_send_welcome_email(self):
        """Test welcome email sending."""
        self.mock_email_service.send_template_email.return_value = True
        
        result = self.onboarding_manager._send_welcome_email(self.test_customer)
        
        assert result is True
        self.mock_email_service.send_template_email.assert_called_once_with(
            to_email="test@example.com",
            template_name="welcome",
            subject="Welcome to Meta-Repo-Seed! 🚀",
            data={
                "customer_name": "Test Company",
                "customer_email": "test@example.com",
                "trial_days": 14,
                "dashboard_url": "https://app.meta-repo-seed.com/dashboard/test-customer-123",
                "getting_started_url": "https://docs.meta-repo-seed.com/getting-started/test-customer-123",
                "support_email": "support@meta-repo-seed.com",
            }
        )
    
    def test_send_welcome_email_without_company_name(self):
        """Test welcome email with customer without company name."""
        customer_no_company = Customer(
            customer_id="test-customer-456",
            email="test2@example.com",
            company_name="",  # No company name
            status=CustomerStatus.TRIAL,
        )
        
        self.mock_email_service.send_template_email.return_value = True
        
        result = self.onboarding_manager._send_welcome_email(customer_no_company)
        
        assert result is True
        call_args = self.mock_email_service.send_template_email.call_args
        assert call_args[1]["data"]["customer_name"] == "there"
    
    def test_create_default_organization(self):
        """Test default organization creation."""
        mock_org = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Company-main",
            status=OrganizationStatus.CREATING
        )
        self.mock_customer_manager.create_organization.return_value = mock_org
        
        with patch.object(self.onboarding_manager, '_update_onboarding_status'):
            result = self.onboarding_manager._create_default_organization(self.test_customer)
        
        assert result == mock_org
        self.mock_customer_manager.create_organization.assert_called_once_with(
            customer_id="test-customer-123",
            name="Test Company-main",
            description="Default organization created during onboarding",
            github_username="",
        )
    
    def test_create_default_organization_without_company_name(self):
        """Test default organization creation without company name."""
        customer_no_company = Customer(
            customer_id="test-customer-456",
            email="test2@example.com",
            company_name="",  # No company name
            status=CustomerStatus.TRIAL,
        )
        
        mock_org = Organization(
            org_id="test-org-456",
            customer_id="test-customer-456",
            name="customer-test-customer-456",
            status=OrganizationStatus.CREATING
        )
        self.mock_customer_manager.create_organization.return_value = mock_org
        
        with patch.object(self.onboarding_manager, '_update_onboarding_status'):
            result = self.onboarding_manager._create_default_organization(customer_no_company)
        
        assert result == mock_org
        call_args = self.mock_customer_manager.create_organization.call_args
        assert call_args[1]["name"] == "customer-test-cus"
    
    def test_send_followup_email(self):
        """Test follow-up email sending."""
        self.mock_email_service.send_template_email.return_value = True
        
        with patch.object(self.onboarding_manager, '_update_onboarding_status'):
            result = self.onboarding_manager.send_followup_email(self.test_customer)
        
        assert result is True
        self.mock_email_service.send_template_email.assert_called_once_with(
            to_email="test@example.com",
            template_name="getting_started",
            subject="Ready to deploy your first project? 🎯",
            data={
                "customer_name": "Test Company",
                "customer_email": "test@example.com",
                "dashboard_url": "https://app.meta-repo-seed.com/dashboard/test-customer-123",
                "tutorial_url": "https://docs.meta-repo-seed.com/tutorials/first-deployment",
                "support_email": "support@meta-repo-seed.com",
            }
        )
    
    def test_complete_profile_setup(self):
        """Test profile setup completion."""
        # Mock customer organizations
        mock_org = Organization(
            org_id="test-org-123",
            customer_id="test-customer-123",
            name="Test Company-main",
            github_username=""
        )
        self.mock_customer_manager.get_customer_organizations.return_value = [mock_org]
        self.mock_customer_manager.update_organization.return_value = True
        
        with patch.object(self.onboarding_manager, '_update_onboarding_status'):
            result = self.onboarding_manager.complete_profile_setup(
                self.test_customer, "testuser"
            )
        
        assert result is True
        assert mock_org.github_username == "testuser"
        self.mock_customer_manager.update_organization.assert_called_once_with(mock_org)
    
    def test_complete_profile_setup_no_organizations(self):
        """Test profile setup completion with no organizations."""
        self.mock_customer_manager.get_customer_organizations.return_value = []
        
        with patch.object(self.onboarding_manager, '_update_onboarding_status'):
            result = self.onboarding_manager.complete_profile_setup(
                self.test_customer, "testuser"
            )
        
        assert result is True
        # Should not try to update organization if none exist
        self.mock_customer_manager.update_organization.assert_not_called()
    
    def test_get_onboarding_status(self):
        """Test getting onboarding status."""
        # Set up customer with onboarding data
        self.test_customer.onboarding_data = {
            "status": "in_progress",
            "current_step": "welcome_email_sent",
            "completed_steps": ["signup_complete", "welcome_email_sent"],
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00"
        }
        
        self.mock_customer_manager.get_customer.return_value = self.test_customer
        
        with patch.object(self.onboarding_manager, '_get_onboarding_data', 
                         return_value=self.test_customer.onboarding_data):
            status = self.onboarding_manager.get_onboarding_status("test-customer-123")
        
        assert status["customer_id"] == "test-customer-123"
        assert status["status"] == "in_progress"
        assert status["current_step"] == "welcome_email_sent"
        assert "signup_complete" in status["completed_steps"]
        assert "welcome_email_sent" in status["completed_steps"]
    
    def test_get_onboarding_status_customer_not_found(self):
        """Test getting onboarding status for non-existent customer."""
        self.mock_customer_manager.get_customer.return_value = None
        
        status = self.onboarding_manager.get_onboarding_status("non-existent")
        
        assert status["status"] == "customer_not_found"
    
    def test_update_onboarding_status(self):
        """Test updating onboarding status."""
        self.mock_customer_manager.update_customer.return_value = True
        
        self.onboarding_manager._update_onboarding_status(
            self.test_customer, OnboardingStep.WELCOME_EMAIL_SENT
        )
        
        # Check that onboarding data was updated
        assert self.test_customer.onboarding_data is not None
        assert self.test_customer.onboarding_data["current_step"] == "welcome_email_sent"
        assert "welcome_email_sent" in self.test_customer.onboarding_data["completed_steps"]
        
        # Check that customer was saved
        self.mock_customer_manager.update_customer.assert_called_once_with(self.test_customer)


class TestEmailService:
    """Test cases for EmailService."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.email_service = EmailService()
    
    def test_send_template_email_success(self):
        """Test successful template email sending."""
        with patch.object(self.email_service, '_send_email', return_value=True):
            result = self.email_service.send_template_email(
                to_email="test@example.com",
                template_name="welcome",
                subject="Test Subject",
                data={"customer_name": "Test User"}
            )
        
        assert result is True
    
    def test_send_template_email_failure(self):
        """Test template email sending failure."""
        with patch.object(self.email_service, '_send_email', return_value=False):
            result = self.email_service.send_template_email(
                to_email="test@example.com",
                template_name="welcome",
                subject="Test Subject",
                data={"customer_name": "Test User"}
            )
        
        assert result is False
    
    def test_send_welcome_email(self):
        """Test welcome email sending."""
        with patch.object(self.email_service, 'send_template_email', return_value=True) as mock_send:
            result = self.email_service.send_welcome_email(
                customer_email="test@example.com",
                customer_name="Test User",
                trial_days=14
            )
        
        assert result is True
        mock_send.assert_called_once_with(
            to_email="test@example.com",
            template_name="welcome",
            subject="Welcome to Meta-Repo-Seed! 🚀",
            data={
                "customer_name": "Test User",
                "customer_email": "test@example.com",
                "trial_days": 14,
                "dashboard_url": "https://app.meta-repo-seed.com/dashboard",
                "getting_started_url": "https://docs.meta-repo-seed.com/getting-started",
                "support_email": "support@meta-repo-seed.com",
            }
        )
    
    def test_send_followup_email(self):
        """Test follow-up email sending."""
        with patch.object(self.email_service, 'send_template_email', return_value=True) as mock_send:
            result = self.email_service.send_followup_email(
                customer_email="test@example.com",
                customer_name="Test User"
            )
        
        assert result is True
        mock_send.assert_called_once_with(
            to_email="test@example.com",
            template_name="getting_started",
            subject="Ready to deploy your first project? 🎯",
            data={
                "customer_name": "Test User",
                "customer_email": "test@example.com",
                "dashboard_url": "https://app.meta-repo-seed.com/dashboard",
                "tutorial_url": "https://docs.meta-repo-seed.com/tutorials/first-deployment",
                "support_email": "support@meta-repo-seed.com",
            }
        )
    
    def test_send_trial_expiring_email(self):
        """Test trial expiration warning email."""
        with patch.object(self.email_service, 'send_template_email', return_value=True) as mock_send:
            result = self.email_service.send_trial_expiring_email(
                customer_email="test@example.com",
                customer_name="Test User",
                days_remaining=3
            )
        
        assert result is True
        mock_send.assert_called_once_with(
            to_email="test@example.com",
            template_name="trial_expiring",
            subject="Your trial expires in 3 days",
            data={
                "customer_name": "Test User",
                "customer_email": "test@example.com",
                "days_remaining": 3,
                "upgrade_url": "https://app.meta-repo-seed.com/billing/upgrade",
                "support_email": "support@meta-repo-seed.com",
            }
        )


class TestCustomerOnboardingIntegration:
    """Integration tests for customer onboarding workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.customer_manager = CustomerManager()
        self.onboarding_manager = OnboardingManager(self.customer_manager)
    
    def test_customer_creation_triggers_onboarding(self):
        """Test that customer creation automatically triggers onboarding."""
        # Mock database operations
        with patch.object(self.customer_manager, 'get_customer_by_email', return_value=None):
            with patch.object(self.customer_manager.db_manager, 'execute_query') as mock_execute:
                # Mock successful customer creation
                mock_execute.return_value = [{
                    "id": "test-customer-123",
                    "email": "test@example.com",
                    "company_name": "Test Company",
                    "status": "trial",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "settings": "{}"
                }]
                
                with patch.object(self.customer_manager, '_create_subscription'):
                    with patch.object(self.customer_manager, '_trigger_onboarding') as mock_trigger:
                        customer = self.customer_manager.create_customer(
                            email="test@example.com",
                            company_name="Test Company"
                        )
        
        # Verify onboarding was triggered
        mock_trigger.assert_called_once()
        
        # Verify customer has onboarding data
        assert customer.onboarding_data is not None
        assert customer.onboarding_data["status"] == "pending"
        assert customer.onboarding_data["current_step"] == "signup_complete"
        assert "signup_complete" in customer.onboarding_data["completed_steps"]


class TestCustomerOnboardingState:
    """Test cases for Customer onboarding state management."""
    
    def test_customer_onboarding_status_methods(self):
        """Test Customer onboarding status methods."""
        customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company"
        )
        
        # Test initial state
        assert customer.get_onboarding_status() == "pending"
        assert customer.get_onboarding_step() == "signup_complete"
        assert not customer.is_onboarding_complete()
        
        # Test updating onboarding step
        customer.update_onboarding_step("welcome_email_sent", "in_progress")
        
        assert customer.get_onboarding_status() == "in_progress"
        assert customer.get_onboarding_step() == "welcome_email_sent"
        assert "welcome_email_sent" in customer.onboarding_data["completed_steps"]
        
        # Test completing onboarding
        customer.update_onboarding_step("onboarding_complete", "completed")
        
        assert customer.get_onboarding_status() == "completed"
        assert customer.get_onboarding_step() == "onboarding_complete"
        assert customer.is_onboarding_complete()
    
    def test_customer_onboarding_data_initialization(self):
        """Test Customer onboarding data initialization."""
        customer = Customer(
            customer_id="test-customer-123",
            email="test@example.com",
            company_name="Test Company"
        )
        
        # Initially no onboarding data
        assert customer.onboarding_data is None
        
        # Update onboarding step should initialize data
        customer.update_onboarding_step("welcome_email_sent")
        
        assert customer.onboarding_data is not None
        assert customer.onboarding_data["current_step"] == "welcome_email_sent"
        assert customer.onboarding_data["status"] == "in_progress"
        assert "welcome_email_sent" in customer.onboarding_data["completed_steps"]
