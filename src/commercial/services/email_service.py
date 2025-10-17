"""
Email Service for Commercial SaaS Platform

This module handles email template rendering and sending for customer
communications including welcome emails, notifications, and alerts.
"""

import logging
import os
from typing import Dict, Any, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


class EmailService:
    """
    Service for sending templated emails to customers.
    
    Handles email template rendering using Jinja2 and provides
    methods for sending various types of customer communications.
    """
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize email service with template directory."""
        self.logger = logging.getLogger("email_service")
        
        # Set up template directory
        if template_dir:
            self.template_dir = Path(template_dir)
        else:
            # Default to templates/email/ directory (relative to project root)
            project_root = Path(__file__).parent.parent.parent.parent
            self.template_dir = project_root / "templates" / "email"
        
        # Initialize Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
        
        # Email configuration (in production, this would come from environment variables)
        self.smtp_host = os.getenv("SMTP_HOST", "localhost")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@meta-repo-seed.com")
        self.from_name = os.getenv("FROM_NAME", "Meta-Repo-Seed Team")
        
    def send_template_email(
        self,
        to_email: str,
        template_name: str,
        subject: str,
        data: Dict[str, Any],
        from_email: Optional[str] = None,
        from_name: Optional[str] = None
    ) -> bool:
        """
        Send an email using a Jinja2 template.
        
        Args:
            to_email: Recipient email address
            template_name: Name of the template file (without .html extension)
            subject: Email subject line
            data: Data to pass to the template
            from_email: Sender email (defaults to configured from_email)
            from_name: Sender name (defaults to configured from_name)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            # Load and render template
            template = self.jinja_env.get_template(f"{template_name}.html")
            html_content = template.render(**data)
            
            # Send email
            success = self._send_email(
                to_email=to_email,
                subject=subject,
                html_content=html_content,
                from_email=from_email or self.from_email,
                from_name=from_name or self.from_name
            )
            
            if success:
                self.logger.info(f"Email sent successfully to {to_email}")
            else:
                self.logger.error(f"Failed to send email to {to_email}")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Error sending template email: {e}")
            return False
    
    def send_welcome_email(self, customer_email: str, customer_name: str, trial_days: int = 14) -> bool:
        """Send welcome email to new customer."""
        data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "trial_days": trial_days,
            "dashboard_url": "https://app.meta-repo-seed.com/dashboard",
            "getting_started_url": "https://docs.meta-repo-seed.com/getting-started",
            "support_email": "support@meta-repo-seed.com",
        }
        
        return self.send_template_email(
            to_email=customer_email,
            template_name="welcome",
            subject="Welcome to Meta-Repo-Seed! 🚀",
            data=data
        )
    
    def send_followup_email(self, customer_email: str, customer_name: str) -> bool:
        """Send follow-up email with next steps."""
        data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "dashboard_url": "https://app.meta-repo-seed.com/dashboard",
            "tutorial_url": "https://docs.meta-repo-seed.com/tutorials/first-deployment",
            "support_email": "support@meta-repo-seed.com",
        }
        
        return self.send_template_email(
            to_email=customer_email,
            template_name="getting_started",
            subject="Ready to deploy your first project? 🎯",
            data=data
        )
    
    def send_trial_expiring_email(self, customer_email: str, customer_name: str, days_remaining: int) -> bool:
        """Send trial expiration warning email."""
        data = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "days_remaining": days_remaining,
            "upgrade_url": "https://app.meta-repo-seed.com/billing/upgrade",
            "support_email": "support@meta-repo-seed.com",
        }
        
        return self.send_template_email(
            to_email=customer_email,
            template_name="trial_expiring",
            subject=f"Your trial expires in {days_remaining} days",
            data=data
        )
    
    def _send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        from_email: str,
        from_name: str
    ) -> bool:
        """
        Send email using SMTP.
        
        In production, this would use a real SMTP server or email service
        like SendGrid, AWS SES, or similar.
        """
        try:
            # For development/testing, we'll just log the email
            self.logger.info(f"EMAIL TO: {to_email}")
            self.logger.info(f"SUBJECT: {subject}")
            self.logger.info(f"FROM: {from_name} <{from_email}>")
            self.logger.info(f"CONTENT: {html_content[:200]}...")
            
            # In production, this would be:
            # import smtplib
            # from email.mime.text import MIMEText
            # from email.mime.multipart import MIMEMultipart
            # 
            # msg = MIMEMultipart('alternative')
            # msg['Subject'] = subject
            # msg['From'] = f"{from_name} <{from_email}>"
            # msg['To'] = to_email
            # 
            # html_part = MIMEText(html_content, 'html')
            # msg.attach(html_part)
            # 
            # server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            # server.starttls()
            # server.login(self.smtp_username, self.smtp_password)
            # server.send_message(msg)
            # server.quit()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email: {e}")
            return False
    
    def create_template(self, template_name: str, content: str) -> bool:
        """Create a new email template."""
        try:
            template_path = self.template_dir / f"{template_name}.html"
            
            # Ensure template directory exists
            self.template_dir.mkdir(parents=True, exist_ok=True)
            
            # Write template file
            with open(template_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Created email template: {template_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating template: {e}")
            return False
    
    def get_template(self, template_name: str) -> Optional[str]:
        """Get template content by name."""
        try:
            template_path = self.template_dir / f"{template_name}.html"
            
            if not template_path.exists():
                self.logger.warning(f"Template not found: {template_name}")
                return None
            
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"Error reading template: {e}")
            return None
