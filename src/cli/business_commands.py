"""
Business-in-a-Box CLI Commands

Provides business-focused CLI commands for organizational deployment:
- deploy-business: Complete organizational infrastructure deployment
- launch-product: 10-minute product deployment with CI/CD
- start-onboarding: Begin post-deployment business setup
- validate-deployment: Verify organizational deployment success
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
import logging

# Add the root directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from seeding import RepoSeeder, setup_logging


class BusinessDeploymentProfiles:
    """Business deployment profile definitions."""
    
    PROFILES = {
        'startup-basic': {
            'name': 'Startup Basic',
            'description': 'Growth-ready infrastructure with professional standards',
            'target_market': 'Early-stage startups and solo founders',
            'features': [
                'Multi-tier portfolio architecture',
                'Professional governance frameworks',
                'Automated CI/CD pipelines',
                'Growth-ready scaling patterns',
                'Investor-ready documentation'
            ],
            'providers': {
                'vcs': 'github',
                'cicd': 'github-actions',
                'paas': 'vercel',
                'secrets': 'github-secrets'
            }
        },
        
        'charity-nonprofit': {
            'name': 'Charity & Non-Profit',
            'description': 'Cost-optimized with compliance and donation frameworks',
            'target_market': 'Charities, non-profits, and social impact organizations',
            'features': [
                'Cost-optimized infrastructure',
                'Donation and volunteer management',
                'Impact reporting frameworks',
                'Compliance and transparency tools',
                'Grant application templates'
            ],
            'providers': {
                'vcs': 'github',
                'cicd': 'github-actions',
                'paas': 'netlify',  # Often has non-profit benefits
                'secrets': 'github-secrets'
            }
        },
        
        'smb-standard': {
            'name': 'Small-Medium Business',
            'description': 'Professional operations with operational simplicity',
            'target_market': 'Small to medium businesses and professional services',
            'features': [
                'Professional business operations',
                'Client management systems',
                'Operational simplicity focus',
                'Business compliance frameworks',
                'Professional service templates'
            ],
            'providers': {
                'vcs': 'github',
                'cicd': 'github-actions',
                'paas': 'cloudflare',
                'secrets': 'github-secrets'
            }
        },
        
        'consulting-firm': {
            'name': 'Consulting Firm',
            'description': 'Client project management and professional service delivery',
            'target_market': 'Consulting firms and professional service providers',
            'features': [
                'Client project management',
                'Professional deliverable tracking',
                'Stakeholder communication templates',
                'Multi-client portfolio management',
                'Professional branding systems'
            ],
            'providers': {
                'vcs': 'github',
                'cicd': 'github-actions',
                'paas': 'vercel',
                'secrets': 'github-secrets'
            }
        }
    }
    
    @classmethod
    def get_profile(cls, profile_name: str) -> Optional[Dict]:
        """Get business deployment profile by name."""
        return cls.PROFILES.get(profile_name)
    
    @classmethod
    def list_profiles(cls) -> List[str]:
        """List available business deployment profiles."""
        return list(cls.PROFILES.keys())
    
    @classmethod
    def get_profile_description(cls, profile_name: str) -> str:
        """Get human-readable profile description."""
        profile = cls.get_profile(profile_name)
        if profile:
            return f"{profile['name']}: {profile['description']}"
        return f"Unknown profile: {profile_name}"


class ProductStackTemplates:
    """Product stack template definitions for 10-minute launches."""
    
    STACKS = {
        'nextjs': {
            'name': 'Next.js Application',
            'description': 'Full-stack React application with SSR/SSG',
            'technologies': ['React', 'Next.js', 'TypeScript', 'Tailwind CSS'],
            'deployment_target': 'vercel',
            'features': ['SSR/SSG', 'API routes', 'Authentication ready', 'Database integration']
        },
        
        'python-api': {
            'name': 'Python API',
            'description': 'FastAPI-based REST API with async support',
            'technologies': ['Python', 'FastAPI', 'PostgreSQL', 'Docker'],
            'deployment_target': 'fly.io',
            'features': ['REST API', 'OpenAPI docs', 'Database models', 'Authentication']
        },
        
        'node-api': {
            'name': 'Node.js API',
            'description': 'Express.js REST API with TypeScript',
            'technologies': ['Node.js', 'Express', 'TypeScript', 'PostgreSQL'],
            'deployment_target': 'fly.io',
            'features': ['REST API', 'Middleware', 'Database ORM', 'API documentation']
        },
        
        'static-site': {
            'name': 'Static Website',
            'description': 'Static site with modern build tools',
            'technologies': ['HTML', 'CSS', 'JavaScript', 'Vite'],
            'deployment_target': 'cloudflare-pages',
            'features': ['Fast builds', 'Modern tooling', 'CDN deployment', 'Forms integration']
        },
        
        'react-spa': {
            'name': 'React SPA',
            'description': 'Single-page React application',
            'technologies': ['React', 'TypeScript', 'Vite', 'React Router'],
            'deployment_target': 'netlify',
            'features': ['SPA routing', 'State management', 'Component library', 'Testing setup']
        }
    }
    
    @classmethod
    def get_stack(cls, stack_name: str) -> Optional[Dict]:
        """Get product stack template by name."""
        return cls.STACKS.get(stack_name)
    
    @classmethod
    def list_stacks(cls) -> List[str]:
        """List available product stack templates."""
        return list(cls.STACKS.keys())


def deploy_business_command(args) -> int:
    """
    Deploy complete business infrastructure.
    
    This command creates a complete organizational deployment with:
    - Multi-tier portfolio architecture
    - Professional governance systems  
    - Automated CI/CD pipelines
    - Enterprise documentation standards
    """
    logger = setup_logging(args.verbose)
    
    # Validate business profile
    if args.profile not in BusinessDeploymentProfiles.list_profiles():
        logger.error(f"Unknown business profile: {args.profile}")
        logger.info("Available profiles:")
        for profile_name in BusinessDeploymentProfiles.list_profiles():
            logger.info(f"  {profile_name}: {BusinessDeploymentProfiles.get_profile_description(profile_name)}")
        return 1
    
    profile = BusinessDeploymentProfiles.get_profile(args.profile)
    logger.info(f"Deploying business infrastructure: {profile['name']}")
    logger.info(f"Target market: {profile['target_market']}")
    
    if args.dry_run:
        logger.info("DRY RUN - Would deploy:")
        logger.info("  ✓ Organization blueprint with multi-tier architecture")
        logger.info("  ✓ Professional governance frameworks")
        logger.info("  ✓ Automated CI/CD pipeline templates")
        logger.info("  ✓ Enterprise documentation standards")
        logger.info("  ✓ Team structure and permissions")
        logger.info(f"  ✓ Provider integrations: {', '.join(profile['providers'].values())}")
        return 0
    
    # TODO: Implement actual business deployment
    logger.info("🚀 Business deployment starting...")
    logger.info("This feature is under development - Phase 0 Sprint 2")
    return 0


def launch_product_command(args) -> int:
    """
    Launch new product with 10-minute deployment.
    
    Creates a new product with:
    - Pre-configured stack template
    - Full CI/CD pipeline 
    - Automated deployment to PaaS
    - Secrets management setup
    """
    logger = setup_logging(args.verbose)
    
    # Validate product stack
    if args.stack not in ProductStackTemplates.list_stacks():
        logger.error(f"Unknown product stack: {args.stack}")
        logger.info("Available stacks:")
        for stack_name in ProductStackTemplates.list_stacks():
            stack = ProductStackTemplates.get_stack(stack_name)
            logger.info(f"  {stack_name}: {stack['description']}")
        return 1
    
    stack = ProductStackTemplates.get_stack(args.stack)
    logger.info(f"Launching product: {args.name}")
    logger.info(f"Stack: {stack['name']} ({stack['description']})")
    logger.info(f"Technologies: {', '.join(stack['technologies'])}")
    logger.info(f"Deployment target: {stack['deployment_target']}")
    
    if args.dry_run:
        logger.info("DRY RUN - Would launch:")
        logger.info(f"  ✓ Repository: {args.name}")
        logger.info(f"  ✓ Stack template: {stack['name']}")
        logger.info(f"  ✓ CI/CD pipeline with testing and deployment")
        logger.info(f"  ✓ PaaS deployment to {stack['deployment_target']}")
        logger.info(f"  ✓ Secrets management setup")
        logger.info(f"  ✓ Features: {', '.join(stack['features'])}")
        return 0
    
    # TODO: Implement actual product launch
    logger.info("🚀 Product launch starting...")
    logger.info("This feature is under development - Phase 0 Sprint 3")
    return 0


def start_onboarding_command(args) -> int:
    """
    Start post-deployment business onboarding workflow.
    
    Begins guided setup process for:
    - Company information and branding
    - Domain and DNS configuration
    - Team member invitation
    - Security and compliance setup
    """
    logger = setup_logging(args.verbose)
    
    logger.info("Starting business onboarding workflow...")
    
    if args.dry_run:
        logger.info("DRY RUN - Would start onboarding:")
        logger.info("  ✓ Company information setup")
        logger.info("  ✓ Domain and DNS configuration")
        logger.info("  ✓ Team member invitation workflow")
        logger.info("  ✓ Security and compliance checklist")
        logger.info("  ✓ Integration with GitHub Issues/Projects")
        return 0
    
    # TODO: Implement onboarding workflow
    logger.info("🚀 Onboarding workflow starting...")
    logger.info("This feature is under development - Phase 1 Sprint 1")
    return 0


def validate_deployment_command(args) -> int:
    """
    Validate business deployment success.
    
    Checks organizational deployment for:
    - Infrastructure completeness
    - Governance compliance
    - Security configuration
    - Professional presentation
    """
    logger = setup_logging(args.verbose)
    
    logger.info("Validating business deployment...")
    
    if args.dry_run:
        logger.info("DRY RUN - Would validate:")
        logger.info("  ✓ Organizational infrastructure completeness")
        logger.info("  ✓ Governance framework compliance")
        logger.info("  ✓ Security configuration verification")
        logger.info("  ✓ Professional presentation standards")
        logger.info("  ✓ Team permissions and access control")
        return 0
    
    # TODO: Implement deployment validation
    logger.info("🚀 Deployment validation starting...")
    logger.info("This feature is under development - Phase 1 Sprint 2")
    return 0


def create_business_cli_parser() -> argparse.ArgumentParser:
    """Create the main CLI parser with business-focused commands."""
    
    parser = argparse.ArgumentParser(
        prog='meta-repo-seed',
        description='Business-in-a-Box: Deploy complete organizational infrastructures in under 10 minutes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Business Deployment Examples:
  meta-repo-seed deploy-business --profile=startup-basic      # Complete startup infrastructure
  meta-repo-seed deploy-business --profile=charity-nonprofit  # Non-profit organization setup
  meta-repo-seed launch-product --stack=nextjs --name=webapp  # 10-minute product launch
  meta-repo-seed start-onboarding                            # Begin post-deployment setup
  meta-repo-seed validate-deployment --business               # Verify deployment success

Business Profiles:
  startup-basic      Growth-ready infrastructure for early-stage startups
  charity-nonprofit  Cost-optimized systems for charities and non-profits  
  smb-standard      Professional operations for small-medium businesses
  consulting-firm   Client management for professional service providers

Product Stacks:
  nextjs           Full-stack React application with SSR/SSG
  python-api       FastAPI-based REST API with async support
  node-api         Express.js REST API with TypeScript
  react-spa        Single-page React application
  static-site      Static website with modern build tools

Target Market: Startups, charities, non-profits, and SMBs needing professional 
infrastructure to focus on their core business instead of technology setup.
        """
    )
    
    # Add subcommands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Business deployment commands',
        metavar='COMMAND'
    )
    
    # deploy-business command
    deploy_parser = subparsers.add_parser(
        'deploy-business',
        help='Deploy complete business infrastructure',
        description='Deploy complete organizational infrastructure with professional governance and automation'
    )
    deploy_parser.add_argument(
        '--profile',
        choices=BusinessDeploymentProfiles.list_profiles(),
        default='startup-basic',
        help='Business deployment profile (default: startup-basic)'
    )
    deploy_parser.add_argument('--dry-run', action='store_true', help='Preview deployment without making changes')
    deploy_parser.add_argument('--verbose', '-v', action='store_true', help='Enable detailed logging')
    deploy_parser.set_defaults(func=deploy_business_command)
    
    # launch-product command  
    launch_parser = subparsers.add_parser(
        'launch-product',
        help='Launch new product with 10-minute deployment',
        description='Create and deploy new product with full CI/CD pipeline in under 10 minutes'
    )
    launch_parser.add_argument('--stack', choices=ProductStackTemplates.list_stacks(), required=True,
                              help='Product stack template')
    launch_parser.add_argument('--name', required=True, help='Product name')
    launch_parser.add_argument('--dry-run', action='store_true', help='Preview launch without making changes')
    launch_parser.add_argument('--verbose', '-v', action='store_true', help='Enable detailed logging')
    launch_parser.set_defaults(func=launch_product_command)
    
    # start-onboarding command
    onboard_parser = subparsers.add_parser(
        'start-onboarding',
        help='Start post-deployment business onboarding',
        description='Begin guided setup workflow for business configuration and team onboarding'
    )
    onboard_parser.add_argument('--dry-run', action='store_true', help='Preview onboarding without making changes')
    onboard_parser.add_argument('--verbose', '-v', action='store_true', help='Enable detailed logging')
    onboard_parser.set_defaults(func=start_onboarding_command)
    
    # validate-deployment command
    validate_parser = subparsers.add_parser(
        'validate-deployment',
        help='Validate business deployment success',
        description='Verify organizational deployment completeness and professional standards'
    )
    validate_parser.add_argument('--business', action='store_true', 
                                help='Perform business-focused validation (organizational, governance, compliance)')
    validate_parser.add_argument('--dry-run', action='store_true', help='Preview validation without making changes')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Enable detailed logging')
    validate_parser.set_defaults(func=validate_deployment_command)
    
    # If no command provided, show help
    parser.set_defaults(func=lambda args: parser.print_help())
    
    return parser


def main_business_cli():
    """Main entry point for business CLI commands."""
    parser = create_business_cli_parser()
    args = parser.parse_args()
    
    # Execute the command
    if hasattr(args, 'func'):
        return args.func(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main_business_cli())
