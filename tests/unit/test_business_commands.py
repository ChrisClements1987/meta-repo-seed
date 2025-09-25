"""
Unit tests for Business-in-a-Box CLI commands.

Tests the business deployment commands, profiles, and stack templates.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "cli"))
from business_commands import (BusinessDeploymentProfiles,
                               ProductStackTemplates,
                               create_business_cli_parser)


class TestBusinessDeploymentProfiles(unittest.TestCase):
    """Test cases for business deployment profiles."""
    
    def test_get_profile_valid(self):
        """Test getting valid business profile."""
        profile = BusinessDeploymentProfiles.get_profile('startup-basic')
        self.assertIsNotNone(profile)
        self.assertEqual(profile['name'], 'Startup Basic')
        self.assertIn('Early-stage startups', profile['target_market'])
    
    def test_get_profile_invalid(self):
        """Test getting invalid business profile."""
        profile = BusinessDeploymentProfiles.get_profile('invalid-profile')
        self.assertIsNone(profile)
    
    def test_list_profiles(self):
        """Test listing all available profiles."""
        profiles = BusinessDeploymentProfiles.list_profiles()
        self.assertIsInstance(profiles, list)
        self.assertIn('startup-basic', profiles)
        self.assertIn('charity-nonprofit', profiles)
        self.assertIn('smb-standard', profiles)
        self.assertIn('consulting-firm', profiles)
    
    def test_get_profile_description(self):
        """Test getting profile description."""
        desc = BusinessDeploymentProfiles.get_profile_description('startup-basic')
        self.assertIn('Startup Basic', desc)
        self.assertIn('Growth-ready infrastructure', desc)
        
        unknown_desc = BusinessDeploymentProfiles.get_profile_description('unknown')
        self.assertIn('Unknown profile', unknown_desc)


class TestProductStackTemplates(unittest.TestCase):
    """Test cases for product stack templates."""
    
    def test_get_stack_valid(self):
        """Test getting valid product stack."""
        stack = ProductStackTemplates.get_stack('nextjs')
        self.assertIsNotNone(stack)
        self.assertEqual(stack['name'], 'Next.js Application')
        self.assertIn('React', stack['technologies'])
    
    def test_get_stack_invalid(self):
        """Test getting invalid product stack."""
        stack = ProductStackTemplates.get_stack('invalid-stack')
        self.assertIsNone(stack)
    
    def test_list_stacks(self):
        """Test listing all available stacks."""
        stacks = ProductStackTemplates.list_stacks()
        self.assertIsInstance(stacks, list)
        self.assertIn('nextjs', stacks)
        self.assertIn('python-api', stacks)
        self.assertIn('node-api', stacks)
        self.assertIn('react-spa', stacks)
        self.assertIn('static-site', stacks)
    
    def test_stack_has_required_fields(self):
        """Test that stacks have required configuration fields."""
        for stack_name in ProductStackTemplates.list_stacks():
            stack = ProductStackTemplates.get_stack(stack_name)
            self.assertIn('name', stack)
            self.assertIn('description', stack)
            self.assertIn('technologies', stack)
            self.assertIn('deployment_target', stack)
            self.assertIn('features', stack)


class TestBusinessCLIParser(unittest.TestCase):
    """Test cases for business CLI parser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = create_business_cli_parser()
    
    def test_deploy_business_command_parsing(self):
        """Test parsing deploy-business command."""
        args = self.parser.parse_args(['deploy-business', '--profile=startup-basic', '--dry-run'])
        self.assertEqual(args.command, 'deploy-business')
        self.assertEqual(args.profile, 'startup-basic')
        self.assertTrue(args.dry_run)
    
    def test_launch_product_command_parsing(self):
        """Test parsing launch-product command."""
        args = self.parser.parse_args(['launch-product', '--stack=nextjs', '--name=my-app'])
        self.assertEqual(args.command, 'launch-product')
        self.assertEqual(args.stack, 'nextjs')
        self.assertEqual(args.name, 'my-app')
    
    def test_start_onboarding_command_parsing(self):
        """Test parsing start-onboarding command."""
        args = self.parser.parse_args(['start-onboarding', '--verbose'])
        self.assertEqual(args.command, 'start-onboarding')
        self.assertTrue(args.verbose)
    
    def test_validate_deployment_command_parsing(self):
        """Test parsing validate-deployment command."""
        args = self.parser.parse_args(['validate-deployment', '--business'])
        self.assertEqual(args.command, 'validate-deployment')
        self.assertTrue(args.business)
    
    def test_invalid_profile_validation(self):
        """Test that invalid profiles are caught by argparse."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['deploy-business', '--profile=invalid'])
    
    def test_invalid_stack_validation(self):
        """Test that invalid stacks are caught by argparse."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['launch-product', '--stack=invalid', '--name=test'])
    
    def test_missing_required_arguments(self):
        """Test that missing required arguments are caught."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(['launch-product', '--stack=nextjs'])  # Missing --name


if __name__ == '__main__':
    unittest.main()
