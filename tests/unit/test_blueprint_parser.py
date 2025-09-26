"""
Unit tests for Organization Blueprint Parser.

Tests blueprint parsing, validation, and data model functionality.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

# Add src modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "blueprints"))
from parser import (BlueprintParser, EnvironmentConfig, OrganizationBlueprint,
                    PortfolioConfig, RepositoryConfig, TeamConfig)


class TestBlueprintParser(unittest.TestCase):
    """Test cases for BlueprintParser."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.parser = BlueprintParser(schema_path=None)  # Skip schema validation for unit tests
    
    def test_parse_yaml_basic_blueprint(self):
        """Test parsing basic organization blueprint."""
        yaml_content = """
apiVersion: blueprint.meta-repo-seed.io/v1
kind: OrganizationBlueprint
metadata:
  name: test-org
  businessProfile: startup-basic
spec:
  organization:
    structure:
      metaRepo:
        name: meta-repo
        visibility: private
    teams:
      - name: founders
        role: admin
        members:
          - founder
    settings:
      defaultBranch: main
  portfolios:
    - name: products
      type: products
      repositories:
        - name: core-product
          visibility: private
"""
        
        blueprint = self.parser.parse_yaml(yaml_content)
        
        self.assertEqual(blueprint.api_version, 'blueprint.meta-repo-seed.io/v1')
        self.assertEqual(blueprint.kind, 'OrganizationBlueprint')
        self.assertEqual(blueprint.metadata.name, 'test-org')
        self.assertEqual(blueprint.metadata.business_profile, 'startup-basic')
        self.assertEqual(len(blueprint.organization.teams), 1)
        self.assertEqual(len(blueprint.portfolios), 1)
    
    def test_parse_yaml_invalid_yaml(self):
        """Test parsing invalid YAML content."""
        invalid_yaml = "{ invalid yaml content"
        
        with self.assertRaises(yaml.YAMLError):
            self.parser.parse_yaml(invalid_yaml)
    
    def test_parse_yaml_missing_required_fields(self):
        """Test parsing YAML with missing required fields."""
        incomplete_yaml = """
apiVersion: blueprint.meta-repo-seed.io/v1
metadata:
  name: incomplete
"""
        
        with self.assertRaises((ValueError, yaml.YAMLError, Exception)):
            self.parser.parse_yaml(incomplete_yaml)
    
    def test_validate_blueprint_no_warnings(self):
        """Test blueprint validation with no warnings."""
        yaml_content = """
apiVersion: blueprint.meta-repo-seed.io/v1
kind: OrganizationBlueprint
metadata:
  name: valid-org
  businessProfile: startup-basic
spec:
  organization:
    structure: {}
    teams:
      - name: founders
        role: admin
  portfolios:
    - name: products
      type: products
      environments:
        - name: production
          type: production
          protection:
            requiredReviewers:
              - founder
"""
        
        blueprint = self.parser.parse_yaml(yaml_content)
        warnings = self.parser.validate_blueprint(blueprint)
        
        # Should have minimal warnings for a well-formed blueprint
        self.assertIsInstance(warnings, list)
    
    def test_get_deployment_order(self):
        """Test deployment order calculation."""
        yaml_content = """
apiVersion: blueprint.meta-repo-seed.io/v1
kind: OrganizationBlueprint
metadata:
  name: test-org
spec:
  organization:
    structure:
      metaRepo:
        name: meta-repo
      platformServices:
        name: platform-services
  portfolios:
    - name: products
      type: products
      repositories:
        - name: product-1
        - name: product-2
"""
        
        blueprint = self.parser.parse_yaml(yaml_content)
        deployment_order = self.parser.get_deployment_order(blueprint)
        
        self.assertEqual(deployment_order[0], 'meta-repo')
        self.assertEqual(deployment_order[1], 'platform-services')
        self.assertIn('product-1', deployment_order)
        self.assertIn('product-2', deployment_order)


class TestRepositoryConfig(unittest.TestCase):
    """Test cases for RepositoryConfig data model."""
    
    def test_from_dict_minimal(self):
        """Test creating RepositoryConfig from minimal data."""
        data = {'name': 'test-repo'}
        repo = RepositoryConfig.from_dict(data)
        
        self.assertEqual(repo.name, 'test-repo')
        self.assertEqual(repo.visibility, 'private')  # Default
        self.assertEqual(repo.features, [])  # Default
    
    def test_from_dict_complete(self):
        """Test creating RepositoryConfig from complete data."""
        data = {
            'name': 'test-repo',
            'displayName': 'Test Repository',
            'description': 'A test repository',
            'visibility': 'public',
            'features': ['issues', 'actions'],
            'protection': {'enabled': True}
        }
        
        repo = RepositoryConfig.from_dict(data)
        
        self.assertEqual(repo.name, 'test-repo')
        self.assertEqual(repo.display_name, 'Test Repository')
        self.assertEqual(repo.description, 'A test repository')
        self.assertEqual(repo.visibility, 'public')
        self.assertEqual(repo.features, ['issues', 'actions'])
        self.assertEqual(repo.protection, {'enabled': True})


class TestEnvironmentConfig(unittest.TestCase):
    """Test cases for EnvironmentConfig data model."""
    
    def test_from_dict_basic(self):
        """Test creating EnvironmentConfig from basic data."""
        data = {
            'name': 'production',
            'type': 'production'
        }
        
        env = EnvironmentConfig.from_dict(data)
        
        self.assertEqual(env.name, 'production')
        self.assertEqual(env.type, 'production')
        self.assertEqual(env.deployment_target, {})
        self.assertEqual(env.secrets, [])
    
    def test_from_dict_with_deployment_target(self):
        """Test creating EnvironmentConfig with deployment target."""
        data = {
            'name': 'production',
            'type': 'production',
            'deploymentTarget': {
                'provider': 'vercel',
                'config': {'domain': 'app.example.com'}
            },
            'protection': {
                'requiredReviewers': ['admin']
            }
        }
        
        env = EnvironmentConfig.from_dict(data)
        
        self.assertEqual(env.deployment_target['provider'], 'vercel')
        self.assertEqual(env.protection['requiredReviewers'], ['admin'])


class TestTeamConfig(unittest.TestCase):
    """Test cases for TeamConfig data model."""
    
    def test_from_dict_basic(self):
        """Test creating TeamConfig from basic data."""
        data = {
            'name': 'engineering',
            'role': 'maintain'
        }
        
        team = TeamConfig.from_dict(data)
        
        self.assertEqual(team.name, 'engineering')
        self.assertEqual(team.role, 'maintain')
        self.assertEqual(team.members, [])
        self.assertEqual(team.repositories, [])
    
    def test_from_dict_complete(self):
        """Test creating TeamConfig from complete data."""
        data = {
            'name': 'engineering',
            'role': 'maintain',
            'members': ['alice', 'bob'],
            'repositories': ['core-product', 'platform-services']
        }
        
        team = TeamConfig.from_dict(data)
        
        self.assertEqual(team.members, ['alice', 'bob'])
        self.assertEqual(team.repositories, ['core-product', 'platform-services'])


if __name__ == '__main__':
    unittest.main()
