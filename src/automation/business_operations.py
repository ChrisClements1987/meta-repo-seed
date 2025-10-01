"""
Business Operations Automation

Implements self-governing business operations automation for the meta-repo-seed system.
This module provides the core automation capabilities that enable repositories to 
operate with minimal manual intervention while maintaining compliance and governance.
"""

import asyncio
import json
import logging
import os
import shutil
import yaml
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Add the root directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class BusinessProfile(Enum):
    """Business deployment profiles with specific automation requirements."""
    STARTUP_BASIC = "startup-basic"
    CHARITY_NONPROFIT = "charity-nonprofit"
    SMB_STANDARD = "smb-standard"
    CONSULTING_FIRM = "consulting-firm"


class AutomationLevel(Enum):
    """Levels of business operations automation."""
    CONSERVATIVE = "conservative"  # Minimal automation, manual oversight
    STANDARD = "standard"         # Balanced automation with some manual steps
    AGGRESSIVE = "aggressive"     # Maximum automation, minimal manual intervention


@dataclass
class BusinessOperationsConfig:
    """Configuration for business operations automation."""
    business_profile: BusinessProfile
    automation_level: AutomationLevel
    self_healing_enabled: bool = True
    compliance_enforcement: bool = True
    automated_reporting: bool = True
    notification_channels: List[str] = None
    custom_policies: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.notification_channels is None:
            self.notification_channels = ['github-issues', 'workflow-logs']
        if self.custom_policies is None:
            self.custom_policies = {}


class BusinessOperationsManager:
    """
    Central manager for business operations automation.
    
    This class orchestrates the various automation components to create
    self-governing repository systems with minimal manual intervention.
    """
    
    def __init__(self, config: BusinessOperationsConfig, dry_run: bool = False):
        """
        Initialize business operations manager.
        
        Args:
            config: Business operations configuration
            dry_run: If True, simulate operations without making changes
        """
        self.config = config
        self.dry_run = dry_run
        self.logger = logging.getLogger(f"{__name__}.BusinessOperationsManager")
        
        # Template directories
        self.templates_dir = Path(__file__).parent.parent.parent / "templates"
        self.business_ops_templates = self.templates_dir / "business-operations"
    
    async def setup_automated_onboarding(self, target_dir: Path, org_name: str, repo_name: str) -> Dict[str, Any]:
        """
        Set up automated onboarding workflows for a new repository.
        
        Args:
            target_dir: Target repository directory
            org_name: GitHub organization name
            repo_name: Repository name
            
        Returns:
            Dictionary with setup results
        """
        self.logger.info(f"Setting up automated onboarding for {org_name}/{repo_name}")
        
        results = {
            'workflows_created': [],
            'governance_files': [],
            'policies_applied': [],
            'success': True,
            'errors': []
        }
        
        try:
            # Create .github/workflows directory
            workflows_dir = target_dir / ".github" / "workflows"
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy onboarding workflow template
            onboarding_workflow = self.business_ops_templates / "workflows" / "automated-onboarding.yml"
            if onboarding_workflow.exists():
                target_workflow = workflows_dir / "automated-onboarding.yml"
                
                if not self.dry_run:
                    shutil.copy2(onboarding_workflow, target_workflow)
                    self.logger.info(f"✅ Copied onboarding workflow to {target_workflow}")
                else:
                    self.logger.info(f"🔍 DRY RUN: Would copy onboarding workflow to {target_workflow}")
                
                results['workflows_created'].append('automated-onboarding.yml')
            
            # Create governance structure
            governance_dir = target_dir / "governance"
            governance_dir.mkdir(exist_ok=True)
            (governance_dir / "policies").mkdir(exist_ok=True)
            
            # Create business profile configuration
            business_profile_config = governance_dir / "business-profile.yml"
            profile_data = {
                'profile': self.config.business_profile.value,
                'automation_level': self.config.automation_level.value,
                'organization': org_name,
                'repository': repo_name,
                'self_healing_enabled': self.config.self_healing_enabled,
                'compliance_enforcement': self.config.compliance_enforcement,
                'automated_reporting': self.config.automated_reporting,
                'created_at': str(Path().cwd()),  # timestamp placeholder
                'managed_by': 'business-operations-automation'
            }
            
            if not self.dry_run:
                with open(business_profile_config, 'w') as f:
                    yaml.dump(profile_data, f, default_flow_style=False)
                self.logger.info(f"✅ Created business profile config: {business_profile_config}")
            else:
                self.logger.info(f"🔍 DRY RUN: Would create business profile config")
            
            results['governance_files'].append('business-profile.yml')
            
            # Apply profile-specific policies
            await self._apply_profile_policies(target_dir, results)
            
            # Set up CODEOWNERS
            await self._setup_codeowners(target_dir, org_name, results)
            
            # Create compliance directory structure
            compliance_dir = target_dir / "compliance"
            compliance_dir.mkdir(exist_ok=True)
            (compliance_dir / "reports").mkdir(exist_ok=True)
            (compliance_dir / "audits").mkdir(exist_ok=True)
            
        except Exception as e:
            self.logger.error(f"Error setting up automated onboarding: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    async def setup_compliance_enforcement(self, target_dir: Path) -> Dict[str, Any]:
        """
        Set up automated compliance enforcement workflows.
        
        Args:
            target_dir: Target repository directory
            
        Returns:
            Dictionary with setup results
        """
        self.logger.info(f"Setting up compliance enforcement for {self.config.business_profile.value}")
        
        results = {
            'workflows_created': [],
            'policies_created': [],
            'success': True,
            'errors': []
        }
        
        try:
            workflows_dir = target_dir / ".github" / "workflows"
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy compliance enforcement workflow
            compliance_workflow = self.business_ops_templates / "workflows" / "compliance-enforcement.yml"
            if compliance_workflow.exists():
                target_workflow = workflows_dir / "compliance-enforcement.yml"
                
                if not self.dry_run:
                    shutil.copy2(compliance_workflow, target_workflow)
                    self.logger.info(f"✅ Copied compliance workflow to {target_workflow}")
                else:
                    self.logger.info(f"🔍 DRY RUN: Would copy compliance workflow")
                
                results['workflows_created'].append('compliance-enforcement.yml')
            
            # Create profile-specific compliance policies
            await self._create_compliance_policies(target_dir, results)
            
        except Exception as e:
            self.logger.error(f"Error setting up compliance enforcement: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    async def setup_automated_reporting(self, target_dir: Path, org_name: str) -> Dict[str, Any]:
        """
        Set up automated reporting workflows and dashboards.
        
        Args:
            target_dir: Target repository directory
            org_name: Organization name
            
        Returns:
            Dictionary with setup results
        """
        self.logger.info("Setting up automated reporting")
        
        results = {
            'workflows_created': [],
            'reports_configured': [],
            'success': True,
            'errors': []
        }
        
        try:
            workflows_dir = target_dir / ".github" / "workflows"
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Create business reporting workflow
            reporting_workflow = workflows_dir / "business-reporting.yml"
            
            reporting_content = self._generate_reporting_workflow(org_name)
            
            if not self.dry_run:
                with open(reporting_workflow, 'w') as f:
                    f.write(reporting_content)
                self.logger.info(f"✅ Created business reporting workflow")
            else:
                self.logger.info(f"🔍 DRY RUN: Would create business reporting workflow")
            
            results['workflows_created'].append('business-reporting.yml')
            
            # Set up reports directory structure
            reports_dir = target_dir / "reports"
            reports_dir.mkdir(exist_ok=True)
            
            for report_type in ['compliance', 'business-metrics', 'audit-logs']:
                (reports_dir / report_type).mkdir(exist_ok=True)
                results['reports_configured'].append(report_type)
            
            # Create dashboard configuration
            await self._setup_dashboard_config(target_dir, results)
            
        except Exception as e:
            self.logger.error(f"Error setting up automated reporting: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    async def setup_self_healing(self, target_dir: Path) -> Dict[str, Any]:
        """
        Set up self-healing and auto-remediation workflows.
        
        Args:
            target_dir: Target repository directory
            
        Returns:
            Dictionary with setup results
        """
        self.logger.info("Setting up self-healing automation")
        
        results = {
            'workflows_created': [],
            'remediation_rules': [],
            'success': True,
            'errors': []
        }
        
        try:
            workflows_dir = target_dir / ".github" / "workflows"
            workflows_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy self-healing workflow
            self_healing_workflow = self.business_ops_templates / "workflows" / "self-healing.yml"
            if self_healing_workflow.exists():
                target_workflow = workflows_dir / "self-healing.yml"
                
                if not self.dry_run:
                    shutil.copy2(self_healing_workflow, target_workflow)
                    self.logger.info(f"✅ Copied self-healing workflow to {target_workflow}")
                else:
                    self.logger.info(f"🔍 DRY RUN: Would copy self-healing workflow")
                
                results['workflows_created'].append('self-healing.yml')
            
            # Create remediation configuration
            await self._create_remediation_config(target_dir, results)
            
        except Exception as e:
            self.logger.error(f"Error setting up self-healing: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    async def setup_governance_integration(self, target_dir: Path, org_name: str) -> Dict[str, Any]:
        """
        Set up governance integration with CODEOWNERS, branch protection, and PR rules.
        
        Args:
            target_dir: Target repository directory
            org_name: Organization name
            
        Returns:
            Dictionary with setup results
        """
        self.logger.info("Setting up governance integration")
        
        results = {
            'governance_files': [],
            'protection_rules': [],
            'success': True,
            'errors': []
        }
        
        try:
            github_dir = target_dir / ".github"
            github_dir.mkdir(exist_ok=True)
            
            # Create CODEOWNERS file
            codeowners_content = self._generate_codeowners(org_name)
            codeowners_file = github_dir / "CODEOWNERS"
            
            if not self.dry_run:
                with open(codeowners_file, 'w') as f:
                    f.write(codeowners_content)
                self.logger.info(f"✅ Created CODEOWNERS file")
            else:
                self.logger.info(f"🔍 DRY RUN: Would create CODEOWNERS file")
            
            results['governance_files'].append('CODEOWNERS')
            
            # Create branch protection configuration
            protection_config = self._generate_branch_protection_config()
            protection_file = github_dir / "branch-protection.yml"
            
            if not self.dry_run:
                with open(protection_file, 'w') as f:
                    yaml.dump(protection_config, f, default_flow_style=False)
                self.logger.info(f"✅ Created branch protection config")
            else:
                self.logger.info(f"🔍 DRY RUN: Would create branch protection config")
            
            results['governance_files'].append('branch-protection.yml')
            results['protection_rules'] = list(protection_config.keys())
            
        except Exception as e:
            self.logger.error(f"Error setting up governance integration: {e}")
            results['success'] = False
            results['errors'].append(str(e))
        
        return results
    
    async def deploy_complete_automation(self, target_dir: Path, org_name: str, repo_name: str) -> Dict[str, Any]:
        """
        Deploy complete business operations automation suite.
        
        Args:
            target_dir: Target repository directory  
            org_name: GitHub organization name
            repo_name: Repository name
            
        Returns:
            Dictionary with complete deployment results
        """
        self.logger.info(f"Deploying complete business operations automation for {org_name}/{repo_name}")
        
        # Overall results
        deployment_results = {
            'business_profile': self.config.business_profile.value,
            'automation_level': self.config.automation_level.value,
            'components_deployed': {},
            'overall_success': True,
            'deployment_summary': {},
            'errors': []
        }
        
        components = [
            ('automated_onboarding', self.setup_automated_onboarding, (target_dir, org_name, repo_name)),
            ('compliance_enforcement', self.setup_compliance_enforcement, (target_dir,)),
            ('automated_reporting', self.setup_automated_reporting, (target_dir, org_name)),
            ('governance_integration', self.setup_governance_integration, (target_dir, org_name))
        ]
        
        # Add self-healing if enabled
        if self.config.self_healing_enabled:
            components.append(('self_healing', self.setup_self_healing, (target_dir,)))
        
        # Deploy each component
        for component_name, setup_func, args in components:
            try:
                self.logger.info(f"🚀 Deploying {component_name}")
                result = await setup_func(*args)
                deployment_results['components_deployed'][component_name] = result
                
                if not result['success']:
                    deployment_results['overall_success'] = False
                    deployment_results['errors'].extend(result.get('errors', []))
                
            except Exception as e:
                self.logger.error(f"Failed to deploy {component_name}: {e}")
                deployment_results['overall_success'] = False
                deployment_results['errors'].append(f"{component_name}: {str(e)}")
                deployment_results['components_deployed'][component_name] = {
                    'success': False,
                    'error': str(e)
                }
        
        # Generate deployment summary
        deployment_results['deployment_summary'] = self._generate_deployment_summary(deployment_results)
        
        # Create deployment report
        await self._create_deployment_report(target_dir, deployment_results)
        
        return deployment_results
    
    # Private helper methods
    
    async def _apply_profile_policies(self, target_dir: Path, results: Dict[str, Any]):
        """Apply business profile-specific policies."""
        governance_dir = target_dir / "governance" / "policies"
        
        profile_policies = {
            BusinessProfile.STARTUP_BASIC: [
                ('growth-ready-standards.md', self._create_startup_growth_policy),
                ('investor-ready-documentation.md', self._create_investor_documentation_policy)
            ],
            BusinessProfile.CHARITY_NONPROFIT: [
                ('transparency-policy.md', self._create_transparency_policy),
                ('donor-privacy-protection.md', self._create_donor_privacy_policy)
            ],
            BusinessProfile.SMB_STANDARD: [
                ('business-continuity.md', self._create_business_continuity_policy),
                ('professional-standards.md', self._create_professional_standards_policy)
            ],
            BusinessProfile.CONSULTING_FIRM: [
                ('client-data-policy.md', self._create_client_data_policy),
                ('partner-approval-process.md', self._create_partner_approval_policy)
            ]
        }
        
        if self.config.business_profile in profile_policies:
            for policy_file, policy_generator in profile_policies[self.config.business_profile]:
                policy_content = policy_generator()
                policy_path = governance_dir / policy_file
                
                if not self.dry_run:
                    with open(policy_path, 'w') as f:
                        f.write(policy_content)
                    self.logger.info(f"✅ Created policy: {policy_file}")
                else:
                    self.logger.info(f"🔍 DRY RUN: Would create policy: {policy_file}")
                
                results['policies_applied'].append(policy_file)
    
    async def _setup_codeowners(self, target_dir: Path, org_name: str, results: Dict[str, Any]):
        """Set up CODEOWNERS file based on business profile."""
        github_dir = target_dir / ".github"
        github_dir.mkdir(exist_ok=True)
        
        codeowners_content = self._generate_codeowners(org_name)
        codeowners_file = github_dir / "CODEOWNERS"
        
        if not self.dry_run:
            with open(codeowners_file, 'w') as f:
                f.write(codeowners_content)
            self.logger.info(f"✅ Created CODEOWNERS file")
        else:
            self.logger.info(f"🔍 DRY RUN: Would create CODEOWNERS file")
        
        results['governance_files'].append('CODEOWNERS')
    
    async def _create_compliance_policies(self, target_dir: Path, results: Dict[str, Any]):
        """Create business profile-specific compliance policies."""
        compliance_dir = target_dir / "compliance"
        compliance_dir.mkdir(exist_ok=True)
        
        # Create compliance framework document
        framework_content = self._generate_compliance_framework()
        framework_file = compliance_dir / "compliance-framework.md"
        
        if not self.dry_run:
            with open(framework_file, 'w') as f:
                f.write(framework_content)
            self.logger.info(f"✅ Created compliance framework")
        else:
            self.logger.info(f"🔍 DRY RUN: Would create compliance framework")
        
        results['policies_created'].append('compliance-framework.md')
    
    async def _setup_dashboard_config(self, target_dir: Path, results: Dict[str, Any]):
        """Set up dashboard configuration for business metrics."""
        reports_dir = target_dir / "reports"
        
        dashboard_config = {
            'business_profile': self.config.business_profile.value,
            'dashboards': {
                'compliance': {
                    'enabled': True,
                    'update_frequency': 'weekly',
                    'metrics': ['policy_compliance', 'security_status', 'documentation_completeness']
                },
                'business_metrics': {
                    'enabled': True,
                    'update_frequency': 'daily',
                    'metrics': ['repository_health', 'team_activity', 'automation_effectiveness']
                }
            }
        }
        
        # Add profile-specific dashboard configs
        if self.config.business_profile == BusinessProfile.CHARITY_NONPROFIT:
            dashboard_config['dashboards']['transparency'] = {
                'enabled': True,
                'update_frequency': 'monthly',
                'metrics': ['donor_privacy_compliance', 'impact_reporting', 'transparency_score']
            }
        
        dashboard_file = reports_dir / "dashboard-config.yml"
        
        if not self.dry_run:
            with open(dashboard_file, 'w') as f:
                yaml.dump(dashboard_config, f, default_flow_style=False)
            self.logger.info(f"✅ Created dashboard configuration")
        else:
            self.logger.info(f"🔍 DRY RUN: Would create dashboard configuration")
        
        results['reports_configured'].append('dashboard-config.yml')
    
    async def _create_remediation_config(self, target_dir: Path, results: Dict[str, Any]):
        """Create auto-remediation configuration."""
        governance_dir = target_dir / "governance"
        
        remediation_config = {
            'auto_remediation': {
                'enabled': self.config.self_healing_enabled,
                'level': self.config.automation_level.value,
                'business_profile': self.config.business_profile.value,
                'rules': self._get_remediation_rules()
            }
        }
        
        config_file = governance_dir / "auto-remediation-config.yml"
        
        if not self.dry_run:
            with open(config_file, 'w') as f:
                yaml.dump(remediation_config, f, default_flow_style=False)
            self.logger.info(f"✅ Created auto-remediation configuration")
        else:
            self.logger.info(f"🔍 DRY RUN: Would create auto-remediation configuration")
        
        results['remediation_rules'] = list(remediation_config['auto_remediation']['rules'].keys())
    
    def _get_remediation_rules(self) -> Dict[str, Any]:
        """Get auto-remediation rules based on business profile and automation level."""
        base_rules = {
            'fix_branch_protection': {
                'enabled': True,
                'conditions': ['missing_protection_rules', 'drift_from_profile']
            },
            'update_dependencies': {
                'enabled': self.config.automation_level != AutomationLevel.CONSERVATIVE,
                'conditions': ['security_vulnerabilities', 'outdated_packages']
            },
            'restore_workflows': {
                'enabled': True,
                'conditions': ['missing_ci_workflow', 'missing_compliance_check']
            }
        }
        
        # Add profile-specific rules
        if self.config.business_profile == BusinessProfile.CHARITY_NONPROFIT:
            base_rules['transparency_compliance'] = {
                'enabled': True,
                'conditions': ['missing_transparency_policy', 'donor_privacy_issues']
            }
        elif self.config.business_profile == BusinessProfile.CONSULTING_FIRM:
            base_rules['client_confidentiality'] = {
                'enabled': True,
                'conditions': ['missing_client_policy', 'confidentiality_breach_risk']
            }
        
        return base_rules
    
    def _generate_codeowners(self, org_name: str) -> str:
        """Generate CODEOWNERS file content based on business profile."""
        base_content = f"""# CODEOWNERS for {org_name}
# Auto-generated by Business Operations Automation
# Business Profile: {self.config.business_profile.value}

# Global code owners
* @{org_name}/core-team

# Governance and compliance
/governance/ @{org_name}/governance-team
/compliance/ @{org_name}/compliance-team

# Documentation
/docs/ @{org_name}/documentation-team

# Infrastructure and automation
/.github/ @{org_name}/infrastructure-team
/infrastructure/ @{org_name}/infrastructure-team
"""
        
        # Add profile-specific CODEOWNERS rules
        if self.config.business_profile == BusinessProfile.CHARITY_NONPROFIT:
            base_content += f"""
# Transparency and donor-related files
/governance/policies/transparency-policy.md @{org_name}/board-members
/reports/transparency/ @{org_name}/board-members
"""
        elif self.config.business_profile == BusinessProfile.CONSULTING_FIRM:
            base_content += f"""
# Client-related files (partner approval required)
/governance/policies/client-data-policy.md @{org_name}/partners
/client-work/ @{org_name}/partners
"""
        
        return base_content
    
    def _generate_branch_protection_config(self) -> Dict[str, Any]:
        """Generate branch protection configuration based on business profile."""
        base_config = {
            'main': {
                'required_status_checks': {
                    'strict': True,
                    'contexts': ['ci', 'compliance-check']
                },
                'enforce_admins': False,
                'required_pull_request_reviews': {
                    'required_approving_review_count': 1,
                    'dismiss_stale_reviews': True,
                    'require_code_owner_reviews': True
                }
            }
        }
        
        # Customize based on business profile
        if self.config.business_profile == BusinessProfile.CHARITY_NONPROFIT:
            base_config['main']['required_pull_request_reviews']['required_approving_review_count'] = 2
            base_config['main']['required_status_checks']['contexts'].append('transparency-audit')
            
        elif self.config.business_profile == BusinessProfile.CONSULTING_FIRM:
            base_config['main']['enforce_admins'] = True
            base_config['main']['required_status_checks']['contexts'].append('client-data-protection')
            base_config['main']['restrictions'] = {
                'users': [],
                'teams': ['partners', 'senior-consultants']
            }
        
        return base_config
    
    def _generate_reporting_workflow(self, org_name: str) -> str:
        """Generate business reporting workflow content."""
        return f"""name: Business Operations Reporting
# Auto-generated business reporting workflow
# Business Profile: {self.config.business_profile.value}

on:
  schedule:
    - cron: '0 9 * * 1'  # Weekly Monday 9 AM
  workflow_dispatch:

jobs:
  generate-business-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate business metrics report
        run: |
          echo "📊 Generating business operations report"
          mkdir -p reports/business-metrics
          
          report_file="reports/business-metrics/weekly-$(date +%Y-%m-%d).md"
          
          cat > "$report_file" << EOF
          # Weekly Business Operations Report - $(date +%Y-%m-%d)
          
          **Organization:** {org_name}
          **Business Profile:** {self.config.business_profile.value}
          **Automation Level:** {self.config.automation_level.value}
          
          ## Repository Health
          - Self-Healing Status: {'✅ Active' if self.config.self_healing_enabled else '⏸️ Disabled'}
          - Compliance Enforcement: {'✅ Active' if self.config.compliance_enforcement else '⏸️ Disabled'}
          - Automated Reporting: {'✅ Active' if self.config.automated_reporting else '⏸️ Disabled'}
          
          ## Automation Effectiveness
          - Workflows Running: [Auto-calculated]
          - Issues Auto-Resolved: [Auto-calculated]
          - Compliance Score: [Auto-calculated]
          
          ## Business Profile Compliance
          - Profile Requirements Met: [Auto-validated]
          - Governance Policies Current: [Auto-checked]
          - Security Standards Maintained: [Auto-verified]
          
          EOF
          
      - name: Commit report
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "Business Operations Bot"
          git add reports/business-metrics/
          git commit -m "📊 Weekly business operations report [automated]" || exit 0
          git push
"""
    
    def _generate_compliance_framework(self) -> str:
        """Generate compliance framework document."""
        return f"""# Compliance Framework

**Business Profile:** {self.config.business_profile.value}
**Automation Level:** {self.config.automation_level.value}
**Last Updated:** Auto-generated by Business Operations Automation

## Overview

This repository follows automated compliance enforcement based on the **{self.config.business_profile.value}** business profile.

## Compliance Components

### 1. Automated Policy Enforcement
- Governance policies automatically applied
- Code quality standards enforced via CI/CD
- Security scanning on all changes
- Documentation standards validated

### 2. Self-Governing Operations
- Branch protection rules automatically maintained
- Workflow integrity monitored and restored
- Configuration drift detection and remediation
- Dependency security updates automated

### 3. Business Profile Compliance
{self._get_profile_specific_compliance_text()}

### 4. Reporting and Auditing
- Weekly compliance reports generated automatically
- Audit trails maintained for all automated actions
- Dashboard metrics updated continuously
- Stakeholder notifications for critical issues

## Escalation Procedures

1. **Automated Resolution:** Most issues resolved without human intervention
2. **Issue Creation:** Unresolved problems automatically create GitHub issues
3. **Team Notification:** Critical issues notify appropriate team members
4. **Manual Override:** Human oversight available for complex decisions

---
*This framework is automatically maintained by Business Operations Automation*
"""
    
    def _get_profile_specific_compliance_text(self) -> str:
        """Get business profile-specific compliance text."""
        profile_text = {
            BusinessProfile.STARTUP_BASIC: """
- Growth-ready infrastructure standards maintained
- Investor-ready documentation automatically updated
- Professional presentation standards enforced
- Scaling patterns and best practices applied
""",
            BusinessProfile.CHARITY_NONPROFIT: """
- Transparency policy compliance automatically monitored
- Donor privacy protection measures enforced
- Impact reporting frameworks maintained
- Board oversight requirements implemented
""",
            BusinessProfile.SMB_STANDARD: """
- Business continuity procedures maintained
- Professional service standards enforced
- Employee access controls managed automatically
- Operational efficiency metrics tracked
""",
            BusinessProfile.CONSULTING_FIRM: """
- Client confidentiality policies strictly enforced
- Partner approval workflows automated
- Professional service delivery standards maintained
- Client data protection measures implemented
"""
        }
        
        return profile_text.get(self.config.business_profile, "Standard compliance measures applied.")
    
    # Policy generator methods
    
    def _create_startup_growth_policy(self) -> str:
        return """# Growth-Ready Standards Policy

## Purpose
Ensure repository maintains standards suitable for rapid startup growth and scaling.

## Standards
1. Code quality thresholds maintained for new team members
2. Documentation updated automatically for investor presentations  
3. Architecture patterns support horizontal scaling
4. Professional presentation maintained at all times

## Automation
- Automated code quality enforcement
- Documentation generation and updates
- Professional branding consistency
- Growth metrics tracking
"""
    
    def _create_transparency_policy(self) -> str:
        return """# Transparency Policy

## Commitment to Transparency
This organization commits to maintaining transparency in all operations.

## Automated Transparency Measures
1. Regular public reporting of activities and impacts
2. Open documentation of processes and decisions
3. Accessible communication channels for stakeholders
4. Automated compliance monitoring and reporting

## Donor Privacy Protection
- Personal information strictly protected
- Automated privacy compliance checks
- Regular audit of data handling practices
- Transparent privacy policies maintained
"""
    
    def _create_client_data_policy(self) -> str:
        return """# Client Data Protection Policy

## Client Confidentiality
All client data and work products are strictly confidential.

## Automated Protection Measures
1. Access controls automatically enforced by team role
2. Partner approval required for sensitive changes
3. Client data segregation maintained automatically
4. Confidentiality breach monitoring active

## Professional Standards
- All client work requires partner review
- Automated compliance with professional service standards
- Client approval workflows enforced
- Intellectual property protection automated
"""
    
    def _create_investor_documentation_policy(self) -> str:
        return """# Investor-Ready Documentation Policy

## Professional Presentation
All documentation maintained at investor presentation quality.

## Automated Standards
1. Professional formatting enforced automatically
2. Business metrics updated continuously
3. Technical documentation kept current
4. Professional branding applied consistently

## Content Requirements
- Business model clearly documented
- Technical architecture professionally presented
- Growth metrics automatically tracked
- Investment-relevant information highlighted
"""
    
    def _create_donor_privacy_policy(self) -> str:
        return """# Donor Privacy Protection Policy

## Privacy Commitment
Donor personal information receives the highest level of protection.

## Automated Privacy Measures
1. Personal data automatically identified and protected
2. Access controls enforce need-to-know principles
3. Data retention policies automatically enforced
4. Privacy breach monitoring and alerting active

## Transparency Balance
- Public reporting protects individual privacy
- Aggregate data used for impact measurement
- Automated anonymization of sensitive information
- Regular privacy compliance audits
"""
    
    def _create_business_continuity_policy(self) -> str:
        return """# Business Continuity Policy

## Continuity Planning
Automated measures ensure business operations continue during disruptions.

## Automated Continuity Measures
1. Critical systems monitored continuously
2. Backup and recovery procedures automated
3. Team access and permissions managed automatically
4. Business process documentation kept current

## Risk Mitigation
- Single points of failure identified and mitigated
- Automated testing of continuity procedures
- Emergency contact information maintained
- Business impact assessments updated automatically
"""
    
    def _create_professional_standards_policy(self) -> str:
        return """# Professional Standards Policy

## Professional Excellence
All work maintains professional service delivery standards.

## Automated Quality Assurance
1. Professional presentation standards enforced
2. Quality metrics monitored continuously
3. Professional communication templates applied
4. Service delivery standards validated automatically

## Client Service
- Professional response times maintained
- Quality standards exceed client expectations
- Automated service level monitoring
- Continuous improvement processes active
"""
    
    def _create_partner_approval_policy(self) -> str:
        return """# Partner Approval Process Policy

## Partner Oversight
Critical decisions require partner-level approval.

## Automated Approval Workflows
1. Partner approval required for sensitive changes
2. Automated escalation for partner review
3. Approval tracking and audit trails maintained
4. Partner notification automation active

## Decision Authority
- Technical decisions: Senior consultant approval
- Business decisions: Partner approval required
- Client-facing work: Partner review mandatory
- Financial decisions: Partner approval required
"""
    
    def _generate_deployment_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment summary from component results."""
        summary = {
            'total_components': len(results['components_deployed']),
            'successful_components': 0,
            'failed_components': 0,
            'workflows_created': 0,
            'policies_applied': 0,
            'governance_files': 0
        }
        
        for component_name, component_result in results['components_deployed'].items():
            if component_result.get('success', False):
                summary['successful_components'] += 1
                
                # Count specific items
                summary['workflows_created'] += len(component_result.get('workflows_created', []))
                summary['policies_applied'] += len(component_result.get('policies_applied', []))
                summary['governance_files'] += len(component_result.get('governance_files', []))
                
            else:
                summary['failed_components'] += 1
        
        summary['success_rate'] = (summary['successful_components'] / summary['total_components'] * 100) if summary['total_components'] > 0 else 0
        
        return summary
    
    async def _create_deployment_report(self, target_dir: Path, results: Dict[str, Any]):
        """Create deployment report file."""
        reports_dir = target_dir / "reports" / "business-operations"
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        report_content = f"""# Business Operations Deployment Report

**Date:** {Path().cwd()}  # Timestamp placeholder
**Business Profile:** {results['business_profile']}
**Automation Level:** {results['automation_level']}

## Deployment Summary

- **Overall Success:** {'✅ Success' if results['overall_success'] else '❌ Failed'}
- **Components Deployed:** {results['deployment_summary']['successful_components']}/{results['deployment_summary']['total_components']}
- **Success Rate:** {results['deployment_summary']['success_rate']:.1f}%

## Component Details

"""
        
        for component_name, component_result in results['components_deployed'].items():
            status = '✅' if component_result.get('success', False) else '❌'
            report_content += f"### {component_name.replace('_', ' ').title()} {status}\n\n"
            
            if 'workflows_created' in component_result:
                report_content += f"- Workflows: {', '.join(component_result['workflows_created'])}\n"
            if 'policies_applied' in component_result:
                report_content += f"- Policies: {', '.join(component_result['policies_applied'])}\n"
            if 'governance_files' in component_result:
                report_content += f"- Governance: {', '.join(component_result['governance_files'])}\n"
            
            if not component_result.get('success', False) and 'errors' in component_result:
                report_content += f"- Errors: {', '.join(component_result['errors'])}\n"
            
            report_content += "\n"
        
        report_content += f"""## Next Steps

1. Review any failed components and resolve issues
2. Test the automated workflows by creating a pull request
3. Verify governance policies are properly applied
4. Monitor the business operations dashboard
5. Schedule regular compliance reviews

---
*Report generated by Business Operations Automation System*
"""
        
        report_file = reports_dir / "deployment-report.md"
        
        if not self.dry_run:
            with open(report_file, 'w') as f:
                f.write(report_content)
            self.logger.info(f"✅ Created deployment report: {report_file}")
        else:
            self.logger.info(f"🔍 DRY RUN: Would create deployment report")


# Convenience function for integration with existing CLI
async def deploy_business_operations_automation(
    target_dir: Path,
    org_name: str,
    repo_name: str,
    business_profile: str = "startup-basic",
    automation_level: str = "standard",
    dry_run: bool = False
) -> Dict[str, Any]:
    """
    Deploy complete business operations automation to a repository.
    
    Args:
        target_dir: Target repository directory
        org_name: GitHub organization name  
        repo_name: Repository name
        business_profile: Business profile (startup-basic, charity-nonprofit, etc.)
        automation_level: Automation level (conservative, standard, aggressive)
        dry_run: If True, simulate deployment without making changes
        
    Returns:
        Dictionary with deployment results
    """
    # Create configuration
    config = BusinessOperationsConfig(
        business_profile=BusinessProfile(business_profile),
        automation_level=AutomationLevel(automation_level),
        self_healing_enabled=True,
        compliance_enforcement=True,
        automated_reporting=True
    )
    
    # Create manager and deploy
    manager = BusinessOperationsManager(config, dry_run=dry_run)
    return await manager.deploy_complete_automation(target_dir, org_name, repo_name)


if __name__ == "__main__":
    # Test the business operations automation
    import tempfile
    
    async def test_deployment():
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        
        with tempfile.TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir) / "test-repo"
            test_dir.mkdir()
            
            print("=== Testing Business Operations Automation ===")
            
            results = await deploy_business_operations_automation(
                target_dir=test_dir,
                org_name="test-org",
                repo_name="test-repo",
                business_profile="startup-basic",
                automation_level="standard", 
                dry_run=True
            )
            
            print(f"\n✅ Deployment Success: {results['overall_success']}")
            print(f"📊 Success Rate: {results['deployment_summary']['success_rate']:.1f}%")
            print(f"⚙️ Workflows: {results['deployment_summary']['workflows_created']}")
            print(f"📋 Policies: {results['deployment_summary']['policies_applied']}")
            
            if not results['overall_success']:
                print("\n❌ Errors:")
                for error in results['errors']:
                    print(f"  - {error}")
    
    asyncio.run(test_deployment())
