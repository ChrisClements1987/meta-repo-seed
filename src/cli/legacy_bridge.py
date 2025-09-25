"""
Legacy Bridge for Business-in-a-Box CLI

This module provides backward compatibility with the existing seeding.py interface
while introducing new business-focused commands.

During Phase 0, both interfaces will be available:
- Legacy: python seeding.py (repository scaffolding)
- Business: python -m src.cli.business_commands (business deployment)

In Phase 1, the legacy interface will be deprecated in favor of the business CLI.
"""

import sys
from pathlib import Path
import argparse
from typing import Optional

# Import existing seeding functionality
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from seeding import parse_arguments as legacy_parse_arguments, main as legacy_main

from .business_commands import create_business_cli_parser, main_business_cli


def detect_command_mode(args: Optional[list] = None) -> str:
    """
    Detect whether user intends business commands or legacy repository scaffolding.
    
    Business commands:
    - deploy-business, launch-product, start-onboarding, validate-deployment
    
    Legacy commands:
    - All existing seeding.py arguments (--project, --username, --dry-run, etc.)
    """
    if args is None:
        args = sys.argv[1:]
    
    # Check for business commands
    business_commands = {'deploy-business', 'launch-product', 'start-onboarding', 'validate-deployment'}
    
    if args and args[0] in business_commands:
        return 'business'
    
    # Check for business-specific flags that indicate business mode intention
    business_flags = {'--profile', '--stack', '--business'}
    if any(flag in args for flag in business_flags):
        return 'business'
    
    # Default to legacy for backward compatibility
    return 'legacy'


def create_unified_cli_parser() -> argparse.ArgumentParser:
    """
    Create unified CLI parser that supports both business and legacy commands.
    
    This provides a smooth transition during Phase 0 where both interfaces coexist.
    """
    parser = argparse.ArgumentParser(
        prog='meta-repo-seed',
        description='Meta-Repo Seed: Business-in-a-Box Organizational Deployment Platform',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🚀 BUSINESS-IN-A-BOX COMMANDS (NEW - Phase 0):
  deploy-business     Deploy complete business infrastructure in <10 minutes
  launch-product      Launch new product with full CI/CD in <10 minutes  
  start-onboarding    Begin post-deployment business setup workflow
  validate-deployment Verify organizational deployment success

📦 LEGACY REPOSITORY COMMANDS (Backward Compatibility):
  --project PROJECT   Create single repository (legacy mode)
  --username USERNAME GitHub username for repository creation
  --config FILE       Load repository configuration from file

BUSINESS DEPLOYMENT EXAMPLES:
  meta-repo-seed deploy-business --profile=startup-basic
  meta-repo-seed launch-product --stack=nextjs --name=my-app
  meta-repo-seed start-onboarding

LEGACY REPOSITORY EXAMPLES:
  meta-repo-seed --project=my-repo --username=johndoe
  meta-repo-seed --config=project.yaml --dry-run

TARGET MARKET: Startups, charities, non-profits, and SMBs needing professional
infrastructure to focus on their core business instead of technology setup.

For more information: https://github.com/ChrisClements1987/meta-repo-seed
        """
    )
    
    # Add subcommands for business operations
    subparsers = parser.add_subparsers(
        dest='command',
        help='Choose deployment mode: business infrastructure or legacy repository',
        metavar='MODE'
    )
    
    # Business commands (new Phase 0 interface)
    business_parser = subparsers.add_parser(
        'business',
        help='Business-in-a-Box deployment commands',
        parents=[create_business_cli_parser()],
        add_help=False
    )
    
    # Legacy repository commands (backward compatibility)
    legacy_parser = subparsers.add_parser(
        'legacy',
        help='Legacy repository scaffolding (backward compatibility)',
        description='Legacy repository scaffolding interface for backward compatibility'
    )
    
    # Add legacy arguments to legacy parser
    legacy_parser.add_argument('--project', type=str, help='Project name (default: auto-detect)')
    legacy_parser.add_argument('--username', type=str, help='GitHub username (default: auto-detect)')
    legacy_parser.add_argument('--dry-run', action='store_true', help='Preview changes without making them')
    legacy_parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    legacy_parser.add_argument('--config', type=Path, help='Load configuration from file')
    legacy_parser.add_argument('--save-config', type=Path, help='Save configuration to file')
    legacy_parser.add_argument('--list-configs', action='store_true', help='List available configurations')
    legacy_parser.add_argument('--template-path', type=Path, help='Custom template directory path')
    
    return parser


def main_unified_cli():
    """
    Main entry point for unified CLI that supports both business and legacy modes.
    
    Automatically detects command mode and routes to appropriate handler.
    """
    mode = detect_command_mode()
    
    if mode == 'business':
        # Route to business CLI
        return main_business_cli()
    else:
        # Route to legacy CLI for backward compatibility
        return legacy_main()


if __name__ == '__main__':
    sys.exit(main_unified_cli())
