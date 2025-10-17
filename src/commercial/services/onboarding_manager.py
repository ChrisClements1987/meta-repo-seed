"""
Customer Onboarding Manager for Commercial SaaS Platform

This module handles automated customer onboarding workflows including
welcome emails, default organization creation, and profile setup.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

from ..models import (
    Customer,
    Organization,
    CustomerStatus,
    OrganizationStatus,
    SubscriptionPlan,
)
from .customer_manager import CustomerManager
from .email_service import EmailService


class OnboardingStep(Enum):
    """Steps in the customer onboarding process."""
    
    SIGNUP_COMPLETE = "signup_complete"
    WELCOME_EMAIL_SENT = "welcome_email_sent"
    DEFAULT_ORG_CREATED = "default_org_created"
    PROFILE_SETUP_STARTED = "profile_setup_started"
    PROFILE_SETUP_COMPLETE = "profile_setup_complete"
    FOLLOWUP_EMAIL_SENT = "followup_email_sent"
    ONBOARDING_COMPLETE = "onboarding_complete"


class OnboardingStatus(Enum):
    """Overall onboarding status."""
    
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class OnboardingManager:
    """
    Manages automated customer onboarding workflows.
    
    Handles the complete onboarding process from signup to first
    successful organization deployment.
    """
    
    def __init__(self, customer_manager: Optional[CustomerManager] = None):
        """Initialize onboarding manager."""
        self.customer_manager = customer_manager or CustomerManager()
        self.email_service = EmailService()
        self.logger = logging.getLogger("onboarding_manager")
        
    def start_onboarding(self, customer: Customer) -> bool:
        """
        Start the automated onboarding process for a new customer.
        
        Args:
            customer: Customer object to onboard
            
        Returns:
            True if onboarding started successfully, False otherwise
        """
        try:
            self.logger.info(f"Starting onboarding for customer {customer.customer_id}")
            
            # Step 1: Send welcome email
            if not self._send_welcome_email(customer):
                self.logger.error(f"Failed to send welcome email for {customer.customer_id}")
                return False
                
            # Step 2: Create default organization
            default_org = self._create_default_organization(customer)
            if not default_org:
                self.logger.error(f"Failed to create default organization for {customer.customer_id}")
                return False
                
            # Step 3: Schedule follow-up email
            self._schedule_followup_email(customer)
            
            # Update customer onboarding status
            self._update_onboarding_status(customer, OnboardingStep.WELCOME_EMAIL_SENT)
            
            self.logger.info(f"Onboarding started successfully for {customer.customer_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start onboarding for {customer.customer_id}: {e}")
            return False
    
    def _send_welcome_email(self, customer: Customer) -> bool:
        """Send welcome email to new customer."""
        try:
            email_data = {
                "customer_name": customer.company_name or "there",
                "customer_email": customer.email,
                "trial_days": 14,
                "dashboard_url": f"https://app.meta-repo-seed.com/dashboard/{customer.customer_id}",
                "getting_started_url": f"https://docs.meta-repo-seed.com/getting-started/{customer.customer_id}",
                "support_email": "support@meta-repo-seed.com",
            }
            
            success = self.email_service.send_template_email(
                to_email=customer.email,
                template_name="welcome",
                subject="Welcome to Meta-Repo-Seed! 🚀",
                data=email_data
            )
            
            if success:
                self.logger.info(f"Welcome email sent to {customer.email}")
            else:
                self.logger.error(f"Failed to send welcome email to {customer.email}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending welcome email: {e}")
            return False
    
    def _create_default_organization(self, customer: Customer) -> Optional[Organization]:
        """Create a default organization for the customer."""
        try:
            # Generate default organization name
            if customer.company_name:
                org_name = f"{customer.company_name}-main"
            else:
                # Use first 8 characters of customer_id for shorter name
                org_name = f"customer-{customer.customer_id[:8]}"
            
            # Create organization
            organization = self.customer_manager.create_organization(
                customer_id=customer.customer_id,
                name=org_name,
                description="Default organization created during onboarding",
                github_username="",  # Will be set during profile setup
            )
            
            if organization:
                self.logger.info(f"Default organization created: {organization.org_id}")
                self._update_onboarding_status(customer, OnboardingStep.DEFAULT_ORG_CREATED)
            else:
                self.logger.error(f"Failed to create default organization for {customer.customer_id}")
                
            return organization
            
        except Exception as e:
            self.logger.error(f"Error creating default organization: {e}")
            return None
    
    def _schedule_followup_email(self, customer: Customer) -> bool:
        """Schedule follow-up email to be sent after 24 hours."""
        try:
            # In a real implementation, this would use a job queue like Celery
            # For now, we'll just log the scheduling
            followup_time = datetime.now() + timedelta(hours=24)
            
            self.logger.info(f"Scheduled follow-up email for {customer.email} at {followup_time}")
            
            # Store the scheduled email in the database or job queue
            self._store_scheduled_email(customer, followup_time)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling follow-up email: {e}")
            return False
    
    def send_followup_email(self, customer: Customer) -> bool:
        """Send follow-up email with next steps."""
        try:
            email_data = {
                "customer_name": customer.company_name or "there",
                "customer_email": customer.email,
                "dashboard_url": f"https://app.meta-repo-seed.com/dashboard/{customer.customer_id}",
                "tutorial_url": f"https://docs.meta-repo-seed.com/tutorials/first-deployment",
                "support_email": "support@meta-repo-seed.com",
            }
            
            success = self.email_service.send_template_email(
                to_email=customer.email,
                template_name="getting_started",
                subject="Ready to deploy your first project? 🎯",
                data=email_data
            )
            
            if success:
                self.logger.info(f"Follow-up email sent to {customer.email}")
                self._update_onboarding_status(customer, OnboardingStep.FOLLOWUP_EMAIL_SENT)
            else:
                self.logger.error(f"Failed to send follow-up email to {customer.email}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending follow-up email: {e}")
            return False
    
    def complete_profile_setup(self, customer: Customer, github_username: str) -> bool:
        """Complete customer profile setup with GitHub integration."""
        try:
            # Update customer with GitHub username
            customer.updated_at = datetime.now()
            
            # Update default organization with GitHub username
            organizations = self.customer_manager.get_customer_organizations(customer.customer_id)
            if organizations:
                default_org = organizations[0]  # First org is the default
                default_org.github_username = github_username
                default_org.updated_at = datetime.now()
                
                if self.customer_manager.update_organization(default_org):
                    self.logger.info(f"Updated default organization with GitHub username: {github_username}")
                else:
                    self.logger.error(f"Failed to update default organization")
                    return False
            
            # Mark profile setup as complete
            self._update_onboarding_status(customer, OnboardingStep.PROFILE_SETUP_COMPLETE)
            
            self.logger.info(f"Profile setup completed for {customer.customer_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error completing profile setup: {e}")
            return False
    
    def get_onboarding_status(self, customer_id: str) -> Dict[str, Any]:
        """Get current onboarding status for a customer."""
        try:
            customer = self.customer_manager.get_customer(customer_id)
            if not customer:
                return {"status": "customer_not_found"}
            
            # Get onboarding data from customer settings or separate table
            onboarding_data = self._get_onboarding_data(customer_id)
            
            return {
                "customer_id": customer_id,
                "status": onboarding_data.get("status", OnboardingStatus.PENDING.value),
                "current_step": onboarding_data.get("current_step", OnboardingStep.SIGNUP_COMPLETE.value),
                "completed_steps": onboarding_data.get("completed_steps", []),
                "created_at": onboarding_data.get("created_at"),
                "updated_at": onboarding_data.get("updated_at"),
            }
            
        except Exception as e:
            self.logger.error(f"Error getting onboarding status: {e}")
            return {"status": "error", "message": str(e)}
    
    def _update_onboarding_status(self, customer: Customer, step: OnboardingStep):
        """Update customer onboarding status."""
        try:
            # Initialize onboarding data if it doesn't exist
            if customer.onboarding_data is None:
                customer.onboarding_data = {
                    "status": "pending",
                    "current_step": "signup_complete",
                    "completed_steps": ["signup_complete"],
                    "created_at": datetime.now().isoformat(),
                }
            
            # Update onboarding data
            onboarding_data = {
                "current_step": step.value,
                "updated_at": datetime.now().isoformat(),
            }
            
            # Add to completed steps if not already there
            completed_steps = customer.onboarding_data.get("completed_steps", [])
            if step.value not in completed_steps:
                completed_steps.append(step.value)
                onboarding_data["completed_steps"] = completed_steps
            
            customer.onboarding_data.update(onboarding_data)
            
            # Save customer with updated onboarding data
            self.customer_manager.update_customer(customer)
            
            self.logger.debug(f"Updated onboarding status for {customer.customer_id}: {step.value}")
            
        except Exception as e:
            self.logger.error(f"Error updating onboarding status: {e}")
    
    def _get_onboarding_data(self, customer_id: str) -> Dict[str, Any]:
        """Get onboarding data for a customer."""
        try:
            customer = self.customer_manager.get_customer(customer_id)
            if not customer:
                return {}
            
            # Return onboarding data from customer object
            return getattr(customer, 'onboarding_data', {})
            
        except Exception as e:
            self.logger.error(f"Error getting onboarding data: {e}")
            return {}
    
    def _store_scheduled_email(self, customer: Customer, scheduled_time: datetime):
        """Store scheduled email in database or job queue."""
        try:
            # In a real implementation, this would store in a database table
            # or add to a job queue like Celery
            self.logger.debug(f"Stored scheduled email for {customer.email} at {scheduled_time}")
            
        except Exception as e:
            self.logger.error(f"Error storing scheduled email: {e}")
