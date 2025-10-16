"""
REST API for Commercial SaaS Platform

This module provides the FastAPI-based REST API for programmatic access
to the commercial platform, including organization management, deployment
status tracking, and usage metrics.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr

from ..models import (
    Customer, Organization, Subscription, UsageMetrics,
    CustomerStatus, SubscriptionPlan, OrganizationStatus
)
from ..services.customer_manager import CustomerManager
from ..services.organization_seeder import OrganizationSeeder


# Pydantic models for API requests/responses
class CustomerCreateRequest(BaseModel):
    email: EmailStr
    company_name: str
    plan: SubscriptionPlan = SubscriptionPlan.STARTUP
    trial_days: int = 14


class CustomerResponse(BaseModel):
    customer_id: str
    email: str
    company_name: str
    status: CustomerStatus
    plan: SubscriptionPlan
    created_at: datetime
    trial_ends_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class OrganizationCreateRequest(BaseModel):
    name: str
    description: str = ""
    github_username: str = ""
    github_org: Optional[str] = None


class OrganizationResponse(BaseModel):
    org_id: str
    customer_id: str
    name: str
    description: str
    status: OrganizationStatus
    github_username: str
    github_org: Optional[str]
    created_at: datetime
    deployed_at: Optional[datetime]
    health_status: str
    
    class Config:
        from_attributes = True


class DeploymentStatusResponse(BaseModel):
    org_id: str
    status: OrganizationStatus
    health_status: str
    deployed_at: Optional[datetime]
    last_health_check: Optional[datetime]
    progress_percentage: int = 0
    current_step: str = ""
    estimated_completion: Optional[datetime] = None


class UsageMetricsResponse(BaseModel):
    org_id: str
    customer_id: str
    period_start: datetime
    period_end: datetime
    deployments_count: int
    api_calls_count: int
    storage_used_mb: int
    team_members_count: int
    products_count: int
    webhook_calls_count: int
    
    class Config:
        from_attributes = True


class SubscriptionUpgradeRequest(BaseModel):
    new_plan: SubscriptionPlan


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


# Initialize FastAPI app
app = FastAPI(
    title="Meta-Repo-Seed Commercial API",
    description="REST API for the Business-in-a-Box commercial platform",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Security
security = HTTPBearer()

# Initialize services
customer_manager = CustomerManager()


# Authentication dependency
async def get_current_customer(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Customer:
    """
    Get current customer from JWT token.
    
    In a real implementation, this would validate the JWT token and
    return the authenticated customer.
    """
    # Placeholder implementation - in reality would validate JWT
    token = credentials.credentials
    
    # For now, return a mock customer for testing
    # In production, this would decode the JWT and fetch the customer
    customer = Customer(
        email="test@example.com",
        company_name="Test Company",
        status=CustomerStatus.ACTIVE,
        plan=SubscriptionPlan.STARTUP
    )
    
    return customer


# API Routes

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "2.0.0"
    }


# Customer Management Endpoints

@app.post("/api/v1/customers", response_model=CustomerResponse, tags=["Customers"])
async def create_customer(request: CustomerCreateRequest):
    """Create a new customer account."""
    try:
        customer = customer_manager.create_customer(
            email=request.email,
            company_name=request.company_name,
            plan=request.plan,
            trial_days=request.trial_days
        )
        
        return CustomerResponse.from_orm(customer)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create customer: {str(e)}"
        )


@app.get("/api/v1/customers/{customer_id}", response_model=CustomerResponse, tags=["Customers"])
async def get_customer(customer_id: str):
    """Get customer by ID."""
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return CustomerResponse.from_orm(customer)


@app.put("/api/v1/customers/{customer_id}/subscription", tags=["Customers"])
async def upgrade_subscription(
    customer_id: str,
    request: SubscriptionUpgradeRequest,
    current_customer: Customer = Depends(get_current_customer)
):
    """Upgrade customer subscription."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = customer_manager.upgrade_subscription(customer_id, request.new_plan)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to upgrade subscription"
        )
    
    return {"message": "Subscription upgraded successfully"}


@app.delete("/api/v1/customers/{customer_id}/subscription", tags=["Customers"])
async def cancel_subscription(
    customer_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Cancel customer subscription."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    success = customer_manager.cancel_subscription(customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel subscription"
        )
    
    return {"message": "Subscription cancelled successfully"}


# Organization Management Endpoints

@app.post("/api/v1/customers/{customer_id}/organizations", response_model=OrganizationResponse, tags=["Organizations"])
async def create_organization(
    customer_id: str,
    request: OrganizationCreateRequest,
    current_customer: Customer = Depends(get_current_customer)
):
    """Create a new organization for a customer."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    organization = customer_manager.create_organization(
        customer_id=customer_id,
        name=request.name,
        description=request.description,
        github_username=request.github_username,
        github_org=request.github_org
    )
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create organization"
        )
    
    return OrganizationResponse.from_orm(organization)


@app.get("/api/v1/customers/{customer_id}/organizations", response_model=List[OrganizationResponse], tags=["Organizations"])
async def get_customer_organizations(
    customer_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Get all organizations for a customer."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    organizations = customer_manager.get_customer_organizations(customer_id)
    return [OrganizationResponse.from_orm(org) for org in organizations]


@app.get("/api/v1/organizations/{org_id}", response_model=OrganizationResponse, tags=["Organizations"])
async def get_organization(org_id: str):
    """Get organization by ID."""
    organization = customer_manager.get_organization(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationResponse.from_orm(organization)


@app.post("/api/v1/organizations/{org_id}/deploy", tags=["Deployment"])
async def deploy_organization(
    org_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Deploy organization infrastructure."""
    organization = customer_manager.get_organization(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Verify customer owns this organization
    if organization.customer_id != current_customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        # Create organization seeder
        seeder = OrganizationSeeder(
            org_id=org_id,
            customer=current_customer,
            organization=organization,
            dry_run=False
        )
        
        # Deploy organization
        success = seeder.deploy_organization()
        
        if success:
            # Track deployment usage
            customer_manager.track_usage(org_id, "deployments", 1)
            
            return {"message": "Organization deployment initiated successfully"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Organization deployment failed"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deployment failed: {str(e)}"
        )


@app.get("/api/v1/organizations/{org_id}/status", response_model=DeploymentStatusResponse, tags=["Deployment"])
async def get_deployment_status(org_id: str):
    """Get organization deployment status."""
    organization = customer_manager.get_organization(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Calculate progress percentage based on status
    progress_map = {
        OrganizationStatus.CREATING: 25,
        OrganizationStatus.ACTIVE: 100,
        OrganizationStatus.SUSPENDED: 0,
        OrganizationStatus.ARCHIVED: 0
    }
    
    progress_percentage = progress_map.get(organization.status, 0)
    
    return DeploymentStatusResponse(
        org_id=org_id,
        status=organization.status,
        health_status=organization.health_status,
        deployed_at=organization.deployed_at,
        last_health_check=organization.last_health_check,
        progress_percentage=progress_percentage,
        current_step=f"Status: {organization.status.value}",
        estimated_completion=organization.deployed_at
    )


# Usage Metrics Endpoints

@app.get("/api/v1/organizations/{org_id}/usage", response_model=UsageMetricsResponse, tags=["Usage"])
async def get_usage_metrics(
    org_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Get usage metrics for an organization."""
    organization = customer_manager.get_organization(org_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Verify customer owns this organization
    if organization.customer_id != current_customer.customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    usage = customer_manager.get_usage_metrics(org_id)
    if not usage:
        # Return empty usage metrics if none exist
        usage = UsageMetrics(org_id=org_id, customer_id=organization.customer_id)
    
    return UsageMetricsResponse.from_orm(usage)


@app.get("/api/v1/customers/{customer_id}/usage", tags=["Usage"])
async def get_customer_usage_summary(
    customer_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Get usage summary for all customer organizations."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    usage_summary = customer_manager.get_customer_usage_summary(customer_id)
    return usage_summary


# Trial Management Endpoints

@app.get("/api/v1/customers/{customer_id}/trial", tags=["Trial"])
async def get_trial_status(
    customer_id: str,
    current_customer: Customer = Depends(get_current_customer)
):
    """Get trial status for a customer."""
    # Verify customer owns this account
    if current_customer.customer_id != customer_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    customer = customer_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    return {
        "is_trial_active": customer.is_trial_active(),
        "trial_ends_at": customer.trial_ends_at,
        "days_remaining": customer_manager.get_trial_days_remaining(customer_id),
        "status": customer.status.value
    }


# Webhook Endpoints

@app.post("/api/v1/webhooks/deployment", tags=["Webhooks"])
async def deployment_webhook(payload: Dict[str, Any]):
    """Webhook endpoint for deployment events."""
    # This would handle webhook events from external services
    # For now, just log the payload
    logging.info(f"Deployment webhook received: {payload}")
    
    return {"message": "Webhook received successfully"}


@app.post("/api/v1/webhooks/billing", tags=["Webhooks"])
async def billing_webhook(payload: Dict[str, Any]):
    """Webhook endpoint for billing events."""
    # This would handle billing webhook events
    # For now, just log the payload
    logging.info(f"Billing webhook received: {payload}")
    
    return {"message": "Billing webhook received successfully"}


# Error handlers

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return {
        "error": "HTTP Error",
        "message": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status_code": 500
    }
