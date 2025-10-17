# Customer Onboarding Workflow Procedures

## Overview

This document outlines the automated customer onboarding workflow for the Meta-Repo-Seed commercial SaaS platform. The onboarding process ensures new customers have a smooth experience from signup to their first successful deployment.

## Workflow Steps

### 1. Customer Signup
**Trigger**: Customer completes registration
**Duration**: Immediate
**Status**: `signup_complete`

When a customer signs up:
- Customer record is created in the database
- Default subscription is established (14-day trial)
- Onboarding data is initialized
- Onboarding process is automatically triggered

### 2. Welcome Email
**Trigger**: Automatic (immediately after signup)
**Duration**: < 1 minute
**Status**: `welcome_email_sent`

The system sends a welcome email containing:
- Personalized greeting with company name
- Trial period information (14 days)
- Dashboard access link
- Getting started guide link
- Support contact information

**Email Template**: `templates/email/welcome.html`

### 3. Default Organization Creation
**Trigger**: Automatic (after welcome email sent)
**Duration**: < 2 minutes
**Status**: `default_org_created`

A default organization is automatically created:
- **Name**: `{company_name}-main` or `customer-{customer_id[:8]}`
- **Description**: "Default organization created during onboarding"
- **Status**: `creating`
- **GitHub Integration**: Empty (to be configured during profile setup)

### 4. Follow-up Email Scheduling
**Trigger**: Automatic (after organization creation)
**Duration**: Immediate
**Status**: `followup_email_scheduled`

A follow-up email is scheduled for 24 hours later containing:
- Next steps for first deployment
- Tutorial links
- Support options
- Dashboard access

**Email Template**: `templates/email/getting_started.html`

### 5. Profile Setup (Customer-Initiated)
**Trigger**: Customer action (when they access dashboard)
**Duration**: Variable
**Status**: `profile_setup_complete`

Customer completes profile setup:
- GitHub username integration
- Organization configuration
- Team member invitations
- Project preferences

### 6. Follow-up Email Delivery
**Trigger**: Scheduled (24 hours after signup)
**Duration**: < 1 minute
**Status**: `followup_email_sent`

The scheduled follow-up email is sent with:
- Step-by-step deployment guide
- Video tutorial links
- Community support options
- Pro tips for first-time users

## Technical Implementation

### Components

1. **OnboardingManager** (`src/commercial/services/onboarding_manager.py`)
   - Orchestrates the entire onboarding process
   - Manages onboarding state transitions
   - Handles error recovery

2. **EmailService** (`src/commercial/services/email_service.py`)
   - Renders and sends email templates
   - Manages email scheduling
   - Handles email delivery failures

3. **Customer Model** (`src/commercial/models/__init__.py`)
   - Stores onboarding state and progress
   - Provides onboarding status methods
   - Tracks completed steps

4. **CustomerManager** (`src/commercial/services/customer_manager.py`)
   - Triggers onboarding on customer creation
   - Manages customer lifecycle
   - Handles organization creation

### Database Schema

The onboarding state is stored in the `customers` table:

```sql
-- Onboarding data stored as JSON in customers table
onboarding_data JSONB DEFAULT NULL
```

Example onboarding data:
```json
{
  "status": "in_progress",
  "current_step": "welcome_email_sent",
  "completed_steps": ["signup_complete", "welcome_email_sent"],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

### Email Templates

Templates are stored in `templates/email/` and use Jinja2 syntax:

- **welcome.html**: Initial welcome email
- **getting_started.html**: 24-hour follow-up email
- **trial_expiring.html**: Trial expiration warning

## Error Handling

### Email Delivery Failures
- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback**: Log error and continue with organization creation
- **Monitoring**: Alert if email failure rate > 5%

### Organization Creation Failures
- **Retry Logic**: 2 attempts with 30-second delay
- **Fallback**: Manual organization creation via support
- **Monitoring**: Alert if organization creation failure rate > 2%

### Database Failures
- **Retry Logic**: 3 attempts with exponential backoff
- **Fallback**: Queue for manual processing
- **Monitoring**: Alert on any database connection issues

## Monitoring and Metrics

### Key Metrics
- **Onboarding Completion Rate**: % of customers who complete onboarding
- **Time to First Deployment**: Average time from signup to first deployment
- **Email Delivery Rate**: % of emails successfully delivered
- **Organization Creation Success Rate**: % of default organizations created successfully

### Alerts
- **Critical**: Onboarding failure rate > 10%
- **Warning**: Email delivery failure rate > 5%
- **Warning**: Organization creation failure rate > 2%
- **Info**: Daily onboarding completion rate < 80%

## Testing

### Unit Tests
- `tests/unit/test_customer_onboarding.py`
- Tests all onboarding workflow steps
- Tests error handling scenarios
- Tests email template rendering

### Integration Tests
- End-to-end onboarding workflow
- Database integration
- Email service integration
- Customer manager integration

### Manual Testing Checklist
- [ ] Customer signup triggers onboarding
- [ ] Welcome email is sent immediately
- [ ] Default organization is created
- [ ] Follow-up email is scheduled
- [ ] Profile setup updates organization
- [ ] Follow-up email is delivered after 24 hours

## Troubleshooting

### Common Issues

1. **Welcome Email Not Sent**
   - Check SMTP configuration
   - Verify email service is running
   - Check customer email address validity

2. **Organization Creation Failed**
   - Check database connectivity
   - Verify customer exists
   - Check organization limits

3. **Follow-up Email Not Delivered**
   - Check scheduled job queue
   - Verify customer still exists
   - Check email service status

### Debug Commands

```python
# Check onboarding status
customer = customer_manager.get_customer(customer_id)
print(customer.get_onboarding_status())

# Manually trigger onboarding
onboarding_manager = OnboardingManager(customer_manager)
onboarding_manager.start_onboarding(customer)

# Send follow-up email manually
onboarding_manager.send_followup_email(customer)
```

## Future Enhancements

### Planned Improvements
1. **A/B Testing**: Test different email templates and timing
2. **Personalization**: Customize onboarding based on customer type
3. **Analytics**: Track customer behavior during onboarding
4. **Automation**: Auto-deploy sample project during onboarding
5. **Integration**: Connect with CRM and support systems

### Metrics to Track
- Customer engagement during onboarding
- Time spent on each step
- Drop-off points in the process
- Conversion rate from trial to paid

## Related Documentation

- [Customer Management Service](../services/customer_manager.md)
- [Email Service Configuration](../services/email_service.md)
- [Database Schema](../database/schema.md)
- [Monitoring and Alerting](../monitoring/alerts.md)
