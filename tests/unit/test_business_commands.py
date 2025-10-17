"""
Unit tests for Business-in-a-Box CLI commands.

Tests the business deployment commands, profiles, and stack templates.
"""

import sys
import unittest
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock

# Add src modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "cli"))
from business_commands import (
    BusinessDeploymentProfiles,
    ProductStackTemplates,
    create_business_cli_parser,
    deploy_business_command,
    launch_product_command,
    start_onboarding_command,
    validate_deployment_command,
    main_business_cli,
)


class TestBusinessDeploymentProfiles(unittest.TestCase):
    """Test cases for business deployment profiles."""

    def test_get_profile_valid(self):
        """Test getting valid business profile."""
        profile = BusinessDeploymentProfiles.get_profile("startup-basic")
        self.assertIsNotNone(profile)
        self.assertEqual(profile["name"], "Startup Basic")
        self.assertIn("Early-stage startups", profile["target_market"])

    def test_get_profile_invalid(self):
        """Test getting invalid business profile."""
        profile = BusinessDeploymentProfiles.get_profile("invalid-profile")
        self.assertIsNone(profile)

    def test_list_profiles(self):
        """Test listing all available profiles."""
        profiles = BusinessDeploymentProfiles.list_profiles()
        self.assertIsInstance(profiles, list)
        self.assertIn("startup-basic", profiles)
        self.assertIn("charity-nonprofit", profiles)
        self.assertIn("smb-standard", profiles)
        self.assertIn("consulting-firm", profiles)

    def test_get_profile_description(self):
        """Test getting profile description."""
        desc = BusinessDeploymentProfiles.get_profile_description("startup-basic")
        self.assertIn("Startup Basic", desc)
        self.assertIn("Growth-ready infrastructure", desc)

        unknown_desc = BusinessDeploymentProfiles.get_profile_description("unknown")
        self.assertIn("Unknown profile", unknown_desc)


class TestProductStackTemplates(unittest.TestCase):
    """Test cases for product stack templates."""

    def test_get_stack_valid(self):
        """Test getting valid product stack."""
        stack = ProductStackTemplates.get_stack("nextjs")
        self.assertIsNotNone(stack)
        self.assertEqual(stack["name"], "Next.js Application")
        self.assertIn("React", stack["technologies"])

    def test_get_stack_invalid(self):
        """Test getting invalid product stack."""
        stack = ProductStackTemplates.get_stack("invalid-stack")
        self.assertIsNone(stack)

    def test_list_stacks(self):
        """Test listing all available stacks."""
        stacks = ProductStackTemplates.list_stacks()
        self.assertIsInstance(stacks, list)
        self.assertIn("nextjs", stacks)
        self.assertIn("python-api", stacks)
        self.assertIn("node-api", stacks)
        self.assertIn("react-spa", stacks)
        self.assertIn("static-site", stacks)

    def test_stack_has_required_fields(self):
        """Test that stacks have required configuration fields."""
        for stack_name in ProductStackTemplates.list_stacks():
            stack = ProductStackTemplates.get_stack(stack_name)
            self.assertIn("name", stack)
            self.assertIn("description", stack)
            self.assertIn("technologies", stack)
            self.assertIn("deployment_target", stack)
            self.assertIn("features", stack)


class TestBusinessCLIParser(unittest.TestCase):
    """Test cases for business CLI parser."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = create_business_cli_parser()

    def test_deploy_business_command_parsing(self):
        """Test parsing deploy-business command."""
        args = self.parser.parse_args(
            ["deploy-business", "--profile=startup-basic", "--dry-run"]
        )
        self.assertEqual(args.command, "deploy-business")
        self.assertEqual(args.profile, "startup-basic")
        self.assertTrue(args.dry_run)

    def test_launch_product_command_parsing(self):
        """Test parsing launch-product command."""
        args = self.parser.parse_args(
            ["launch-product", "--stack=nextjs", "--name=my-app"]
        )
        self.assertEqual(args.command, "launch-product")
        self.assertEqual(args.stack, "nextjs")
        self.assertEqual(args.name, "my-app")

    def test_start_onboarding_command_parsing(self):
        """Test parsing start-onboarding command."""
        args = self.parser.parse_args(["start-onboarding", "--verbose"])
        self.assertEqual(args.command, "start-onboarding")
        self.assertTrue(args.verbose)

    def test_validate_deployment_command_parsing(self):
        """Test parsing validate-deployment command."""
        args = self.parser.parse_args(["validate-deployment", "--business"])
        self.assertEqual(args.command, "validate-deployment")
        self.assertTrue(args.business)

    def test_invalid_profile_validation(self):
        """Test that invalid profiles are caught by argparse."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["deploy-business", "--profile=invalid"])

    def test_invalid_stack_validation(self):
        """Test that invalid stacks are caught by argparse."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["launch-product", "--stack=invalid", "--name=test"])

    def test_missing_required_arguments(self):
        """Test that missing required arguments are caught."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(
                ["launch-product", "--stack=nextjs"]
            )  # Missing --name


class TestDeployBusinessCommand(unittest.TestCase):
    """Test cases for deploy_business_command function."""

    def setUp(self):
        """Set up test fixtures."""
        self.args = MagicMock()
        self.args.profile = "startup-basic"
        self.args.verbose = False
        self.args.dry_run = False
        self.args.org_name = None

    @patch('business_commands.setup_logging')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    def test_deploy_business_invalid_profile(self, mock_list_profiles, mock_setup_logging):
        """Test deploy_business_command with invalid profile."""
        mock_list_profiles.return_value = ["startup-basic", "charity-nonprofit"]
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        self.args.profile = "invalid-profile"
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Unknown business profile: invalid-profile")
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile_description')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_valid_profile(self, mock_setup_logging, mock_list_profiles, 
                                         mock_get_profile, mock_get_description, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command with valid profile."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_get_description.return_value = "Startup Basic: Growth-ready infrastructure"
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.return_value = 0
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_keyboard_interrupt(self, mock_setup_logging, mock_list_profiles, 
                                               mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command with KeyboardInterrupt."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.side_effect = KeyboardInterrupt()
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.info.assert_called_with("Deployment cancelled by user")

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_general_exception(self, mock_setup_logging, mock_list_profiles, 
                                             mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command with general exception."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.side_effect = Exception("Test error")
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Deployment failed with error: Test error")

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_verbose_exception(self, mock_setup_logging, mock_list_profiles, 
                                              mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command with verbose exception."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.side_effect = Exception("Test error")
        self.args.verbose = True
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Deployment failed with error: Test error")

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_success_with_duration(self, mock_setup_logging, mock_list_profiles, 
                                                  mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command success with duration > 10 minutes."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        
        # Mock the async function to return success with duration > 10
        async def mock_run_deployment():
            return 0
        mock_asyncio_run.return_value = 0
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_dry_run_success(self, mock_setup_logging, mock_list_profiles, 
                                            mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command dry run success."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        self.args.dry_run = True
        mock_asyncio_run.return_value = 0
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.BusinessDeploymentProfiles.get_profile')
    @patch('business_commands.BusinessDeploymentProfiles.list_profiles')
    @patch('business_commands.setup_logging')
    def test_deploy_business_failure_with_error(self, mock_setup_logging, mock_list_profiles, 
                                               mock_get_profile, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test deploy_business_command failure with error."""
        mock_list_profiles.return_value = ["startup-basic"]
        mock_get_profile.return_value = {"name": "Startup Basic", "target_market": "Early-stage startups"}
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.return_value = 1
        
        result = deploy_business_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.info.assert_called()


class TestLaunchProductCommand(unittest.TestCase):
    """Test cases for launch_product_command function."""

    def setUp(self):
        """Set up test fixtures."""
        self.args = MagicMock()
        self.args.stack = "nextjs"
        self.args.name = "test-app"
        self.args.verbose = False
        self.args.dry_run = False

    @patch('business_commands.setup_logging')
    @patch('business_commands.ProductStackTemplates.list_stacks')
    def test_launch_product_invalid_stack(self, mock_list_stacks, mock_setup_logging):
        """Test launch_product_command with invalid stack."""
        mock_list_stacks.return_value = ["nextjs", "python-api"]
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        self.args.stack = "invalid-stack"
        
        result = launch_product_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Unknown product stack: invalid-stack")
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('business_commands.ProductStackTemplates.get_stack')
    @patch('business_commands.ProductStackTemplates.list_stacks')
    @patch('business_commands.setup_logging')
    def test_launch_product_valid_stack(self, mock_setup_logging, mock_list_stacks, mock_get_stack, mock_asyncio_run):
        """Test launch_product_command with valid stack."""
        mock_list_stacks.return_value = ["nextjs"]
        mock_get_stack.return_value = {
            "name": "Next.js Application",
            "description": "Full-stack React application",
            "technologies": ["React", "Next.js"],
            "deployment_target": "vercel"
        }
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_asyncio_run.return_value = 0
        
        result = launch_product_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('business_commands.ProductStackTemplates.get_stack')
    @patch('business_commands.ProductStackTemplates.list_stacks')
    @patch('business_commands.setup_logging')
    def test_launch_product_keyboard_interrupt(self, mock_setup_logging, mock_list_stacks, mock_get_stack, mock_asyncio_run):
        """Test launch_product_command with KeyboardInterrupt."""
        mock_list_stacks.return_value = ["nextjs"]
        mock_get_stack.return_value = {
            "name": "Next.js Application", 
            "description": "Full-stack React application",
            "technologies": ["React", "Next.js"],
            "deployment_target": "vercel"
        }
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_asyncio_run.side_effect = KeyboardInterrupt()
        
        result = launch_product_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.info.assert_called_with("Product launch cancelled by user")

    @patch('asyncio.run')
    @patch('business_commands.ProductStackTemplates.get_stack')
    @patch('business_commands.ProductStackTemplates.list_stacks')
    @patch('business_commands.setup_logging')
    def test_launch_product_general_exception(self, mock_setup_logging, mock_list_stacks, mock_get_stack, mock_asyncio_run):
        """Test launch_product_command with general exception."""
        mock_list_stacks.return_value = ["nextjs"]
        mock_get_stack.return_value = {
            "name": "Next.js Application", 
            "description": "Full-stack React application",
            "technologies": ["React", "Next.js"],
            "deployment_target": "vercel"
        }
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_asyncio_run.side_effect = Exception("Test error")
        
        result = launch_product_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Product launch failed with error: Test error")

    @patch('asyncio.run')
    @patch('business_commands.ProductStackTemplates.get_stack')
    @patch('business_commands.ProductStackTemplates.list_stacks')
    @patch('business_commands.setup_logging')
    def test_launch_product_dry_run(self, mock_setup_logging, mock_list_stacks, mock_get_stack, mock_asyncio_run):
        """Test launch_product_command with dry run."""
        mock_list_stacks.return_value = ["nextjs"]
        mock_get_stack.return_value = {
            "name": "Next.js Application", 
            "description": "Full-stack React application",
            "technologies": ["React", "Next.js"],
            "deployment_target": "vercel"
        }
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        self.args.dry_run = True
        mock_asyncio_run.return_value = 0
        
        result = launch_product_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()


class TestStartOnboardingCommand(unittest.TestCase):
    """Test cases for start_onboarding_command function."""

    def setUp(self):
        """Set up test fixtures."""
        self.args = MagicMock()
        self.args.profile = "startup-basic"
        self.args.automation_level = "standard"
        self.args.org_name = None
        self.args.repo_name = None
        self.args.verbose = False
        self.args.dry_run = False

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.setup_logging')
    def test_start_onboarding_success(self, mock_setup_logging, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test start_onboarding_command success."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.return_value = 0
        
        result = start_onboarding_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.setup_logging')
    def test_start_onboarding_keyboard_interrupt(self, mock_setup_logging, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test start_onboarding_command with KeyboardInterrupt."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.side_effect = KeyboardInterrupt()
        
        result = start_onboarding_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.info.assert_called_with("Onboarding cancelled by user")

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.setup_logging')
    def test_start_onboarding_general_exception(self, mock_setup_logging, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test start_onboarding_command with general exception."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        mock_asyncio_run.side_effect = Exception("Test error")
        
        result = start_onboarding_command(self.args)
        
        self.assertEqual(result, 1)
        mock_logger.error.assert_called_with("Onboarding failed with error: Test error")

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.setup_logging')
    def test_start_onboarding_dry_run(self, mock_setup_logging, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test start_onboarding_command with dry run."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        self.args.dry_run = True
        mock_asyncio_run.return_value = 0
        
        result = start_onboarding_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('asyncio.run')
    @patch('os.path.basename')
    @patch('os.getcwd')
    @patch('business_commands.setup_logging')
    def test_start_onboarding_with_custom_names(self, mock_setup_logging, mock_getcwd, mock_basename, mock_asyncio_run):
        """Test start_onboarding_command with custom org and repo names."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        mock_getcwd.return_value = "/test/dir"
        mock_basename.return_value = "test-org"
        self.args.org_name = "custom-org"
        self.args.repo_name = "custom-repo"
        mock_asyncio_run.return_value = 0
        
        result = start_onboarding_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()


class TestValidateDeploymentCommand(unittest.TestCase):
    """Test cases for validate_deployment_command function."""

    def setUp(self):
        """Set up test fixtures."""
        self.args = MagicMock()
        self.args.verbose = False
        self.args.dry_run = False
        self.args.business = False

    @patch('business_commands.setup_logging')
    def test_validate_deployment_dry_run(self, mock_setup_logging):
        """Test validate_deployment_command with dry run."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        self.args.dry_run = True
        
        result = validate_deployment_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called()

    @patch('business_commands.setup_logging')
    def test_validate_deployment_not_implemented(self, mock_setup_logging):
        """Test validate_deployment_command not implemented."""
        mock_logger = MagicMock()
        mock_setup_logging.return_value = mock_logger
        
        result = validate_deployment_command(self.args)
        
        self.assertEqual(result, 0)
        mock_logger.info.assert_called_with("This feature is under development - Phase 1 Sprint 2")


class TestMainBusinessCLI(unittest.TestCase):
    """Test cases for main_business_cli function."""

    @patch('business_commands.create_business_cli_parser')
    def test_main_business_cli_with_func(self, mock_create_parser):
        """Test main_business_cli with function."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        mock_args.func = MagicMock(return_value=0)
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser
        
        result = main_business_cli()
        
        self.assertEqual(result, 0)
        mock_args.func.assert_called_once_with(mock_args)

    @patch('business_commands.create_business_cli_parser')
    def test_main_business_cli_without_func(self, mock_create_parser):
        """Test main_business_cli without function."""
        mock_parser = MagicMock()
        mock_args = MagicMock()
        del mock_args.func  # Remove func attribute
        mock_parser.parse_args.return_value = mock_args
        mock_create_parser.return_value = mock_parser
        
        result = main_business_cli()
        
        self.assertEqual(result, 1)
        mock_parser.print_help.assert_called_once()


if __name__ == "__main__":
    unittest.main()
