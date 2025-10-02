"""
Unit tests for Legacy Bridge CLI.

Tests backward compatibility layer between legacy seeding.py and new business CLI.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add src modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from src.cli.legacy_bridge import (create_unified_cli_parser, detect_command_mode,
                                    main_unified_cli)


class TestDetectCommandMode(unittest.TestCase):
    """Test cases for command mode detection."""
    
    def test_detect_business_command_deploy(self):
        """Test detection of deploy-business command."""
        mode = detect_command_mode(['deploy-business', '--profile=startup'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_command_launch(self):
        """Test detection of launch-product command."""
        mode = detect_command_mode(['launch-product', '--stack=nextjs'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_command_onboarding(self):
        """Test detection of start-onboarding command."""
        mode = detect_command_mode(['start-onboarding'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_command_validate(self):
        """Test detection of validate-deployment command."""
        mode = detect_command_mode(['validate-deployment'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_flag_profile(self):
        """Test detection via --profile flag."""
        mode = detect_command_mode(['--profile', 'startup-basic'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_flag_stack(self):
        """Test detection via --stack flag."""
        mode = detect_command_mode(['--stack', 'nextjs'])
        self.assertEqual(mode, 'business')
    
    def test_detect_business_flag_business(self):
        """Test detection via --business flag."""
        mode = detect_command_mode(['--business'])
        self.assertEqual(mode, 'business')
    
    def test_detect_legacy_mode_project(self):
        """Test legacy mode detection for --project."""
        mode = detect_command_mode(['--project', 'myproject'])
        self.assertEqual(mode, 'legacy')
    
    def test_detect_legacy_mode_username(self):
        """Test legacy mode detection for --username."""
        mode = detect_command_mode(['--username', 'johndoe'])
        self.assertEqual(mode, 'legacy')
    
    def test_detect_legacy_mode_dry_run(self):
        """Test legacy mode detection for --dry-run."""
        mode = detect_command_mode(['--dry-run'])
        self.assertEqual(mode, 'legacy')
    
    def test_detect_legacy_mode_config(self):
        """Test legacy mode detection for --config."""
        mode = detect_command_mode(['--config', 'project.yaml'])
        self.assertEqual(mode, 'legacy')
    
    def test_detect_legacy_mode_empty_args(self):
        """Test legacy mode as default for empty args."""
        mode = detect_command_mode([])
        self.assertEqual(mode, 'legacy')
    
    def test_detect_mode_with_none_args(self):
        """Test detection when args is None (uses sys.argv)."""
        with patch('sys.argv', ['script', '--dry-run']):
            mode = detect_command_mode(None)
            self.assertEqual(mode, 'legacy')


class TestCreateUnifiedCliParser(unittest.TestCase):
    """Test cases for unified CLI parser creation."""
    
    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = create_unified_cli_parser()
        self.assertIsNotNone(parser)
        self.assertEqual(parser.prog, 'meta-repo-seed')
    
    def test_parser_has_business_subcommand(self):
        """Test that parser includes business subcommand."""
        parser = create_unified_cli_parser()
        # Parse a business command to verify it's recognized
        # Note: business subcommand requires additional args, so just verify help doesn't fail
        help_text = parser.format_help()
        self.assertIn('business', help_text)
    
    def test_parser_has_legacy_subcommand(self):
        """Test that parser includes legacy subcommand."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--project', 'test'])
        self.assertEqual(args.command, 'legacy')
        self.assertEqual(args.project, 'test')
    
    def test_parser_legacy_dry_run_flag(self):
        """Test legacy --dry-run flag."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--dry-run'])
        self.assertTrue(args.dry_run)
    
    def test_parser_legacy_verbose_flag(self):
        """Test legacy --verbose flag."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--verbose'])
        self.assertTrue(args.verbose)
    
    def test_parser_legacy_config_option(self):
        """Test legacy --config option."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--config', 'project.yaml'])
        self.assertEqual(args.config, Path('project.yaml'))
    
    def test_parser_legacy_save_config_option(self):
        """Test legacy --save-config option."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--save-config', 'output.yaml'])
        self.assertEqual(args.save_config, Path('output.yaml'))
    
    def test_parser_legacy_list_configs_flag(self):
        """Test legacy --list-configs flag."""
        parser = create_unified_cli_parser()
        args = parser.parse_args(['legacy', '--list-configs'])
        self.assertTrue(args.list_configs)
    
    def test_parser_help_message_contains_business_commands(self):
        """Test that help message documents business commands."""
        parser = create_unified_cli_parser()
        help_text = parser.format_help()
        self.assertIn('deploy-business', help_text)
        self.assertIn('launch-product', help_text)
        self.assertIn('start-onboarding', help_text)
        self.assertIn('validate-deployment', help_text)
    
    def test_parser_help_message_contains_legacy_commands(self):
        """Test that help message documents legacy commands."""
        parser = create_unified_cli_parser()
        help_text = parser.format_help()
        self.assertIn('--project', help_text)
        self.assertIn('--username', help_text)
        self.assertIn('LEGACY', help_text)


class TestMainUnifiedCli(unittest.TestCase):
    """Test cases for main unified CLI entry point."""
    
    @patch('src.cli.legacy_bridge.main_business_cli')
    @patch('src.cli.legacy_bridge.detect_command_mode')
    def test_routes_to_business_cli(self, mock_detect, mock_business_main):
        """Test routing to business CLI when business mode detected."""
        mock_detect.return_value = 'business'
        mock_business_main.return_value = 0
        
        result = main_unified_cli()
        
        mock_detect.assert_called_once()
        mock_business_main.assert_called_once()
        self.assertEqual(result, 0)
    
    @patch('src.cli.legacy_bridge.legacy_main')
    @patch('src.cli.legacy_bridge.detect_command_mode')
    def test_routes_to_legacy_cli(self, mock_detect, mock_legacy_main):
        """Test routing to legacy CLI when legacy mode detected."""
        mock_detect.return_value = 'legacy'
        mock_legacy_main.return_value = 0
        
        result = main_unified_cli()
        
        mock_detect.assert_called_once()
        mock_legacy_main.assert_called_once()
        self.assertEqual(result, 0)
    
    @patch('src.cli.legacy_bridge.legacy_main')
    @patch('src.cli.legacy_bridge.detect_command_mode')
    def test_returns_business_cli_exit_code(self, mock_detect, mock_legacy_main):
        """Test that business CLI exit code is returned."""
        mock_detect.return_value = 'legacy'
        mock_legacy_main.return_value = 1
        
        result = main_unified_cli()
        
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
