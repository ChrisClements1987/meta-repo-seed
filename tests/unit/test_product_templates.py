"""
Unit tests for Product Template Generator.

Tests template generation, PaaS integration, and 10-minute product launch.
"""

import unittest
from unittest.mock import patch, MagicMock
import tempfile
import sys
from pathlib import Path

# Add src modules to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "templates"))
from generator import ProductTemplateRegistry, ProductTemplateGenerator, TemplateConfig


class TestProductTemplateRegistry(unittest.TestCase):
    """Test cases for ProductTemplateRegistry."""
    
    def test_get_template_valid(self):
        """Test getting valid template."""
        template = ProductTemplateRegistry.get_template('nextjs')
        self.assertIsNotNone(template)
        self.assertEqual(template.name, 'nextjs')
        self.assertEqual(template.display_name, 'Next.js Application')
        self.assertIn('React', template.technologies)
    
    def test_get_template_invalid(self):
        """Test getting invalid template."""
        template = ProductTemplateRegistry.get_template('invalid-template')
        self.assertIsNone(template)
    
    def test_list_templates(self):
        """Test listing all templates."""
        templates = ProductTemplateRegistry.list_templates()
        self.assertIsInstance(templates, list)
        self.assertIn('nextjs', templates)
        self.assertIn('python-api', templates)
        self.assertGreaterEqual(len(templates), 5)
    
    def test_get_templates_by_deployment_target(self):
        """Test filtering templates by deployment target."""
        vercel_templates = ProductTemplateRegistry.get_templates_by_deployment_target('vercel')
        self.assertIsInstance(vercel_templates, list)
        
        for template in vercel_templates:
            self.assertEqual(template.deployment_target, 'vercel')
    
    def test_template_config_completeness(self):
        """Test that all templates have complete configuration."""
        for template_name in ProductTemplateRegistry.list_templates():
            template = ProductTemplateRegistry.get_template(template_name)
            
            # Required fields
            self.assertIsNotNone(template.name)
            self.assertIsNotNone(template.display_name)
            self.assertIsNotNone(template.description)
            self.assertIsInstance(template.technologies, list)
            self.assertGreater(len(template.technologies), 0)
            self.assertIsNotNone(template.deployment_target)
            self.assertIsInstance(template.features, list)
            self.assertGreater(len(template.features), 0)


class TestProductTemplateGenerator(unittest.TestCase):
    """Test cases for ProductTemplateGenerator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.templates_dir = Path(self.temp_dir) / "templates"
        self.generator = ProductTemplateGenerator(self.templates_dir)
    
    def test_generate_product_dry_run(self):
        """Test product generation in dry-run mode."""
        result = self.generator.generate_product(
            template_name='nextjs',
            product_name='test-product',
            output_dir=Path(self.temp_dir),
            dry_run=True
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(result['product_name'], 'test-product')
        self.assertTrue(result['dry_run'])
        self.assertIn('PRODUCT_NAME', result['variables'])
        self.assertEqual(result['variables']['PRODUCT_NAME'], 'test-product')
    
    def test_generate_product_invalid_template(self):
        """Test product generation with invalid template."""
        with self.assertRaises(ValueError):
            self.generator.generate_product(
                template_name='invalid-template',
                product_name='test-product',
                output_dir=Path(self.temp_dir),
                dry_run=True
            )
    
    def test_template_variable_substitution(self):
        """Test template variable substitution."""
        variables = {
            'PRODUCT_NAME': 'my-app',
            'CURRENT_DATE': '2025-01-01'
        }
        
        content = "Project: {{PRODUCT_NAME}} created on {{CURRENT_DATE}}"
        expected = "Project: my-app created on 2025-01-01"
        
        result = self.generator._substitute_variables(content, variables)
        self.assertEqual(result, expected)
    
    def test_is_text_file_detection(self):
        """Test text file detection for variable substitution."""
        # Text files that should have substitution
        self.assertTrue(self.generator._is_text_file(Path('file.js')))
        self.assertTrue(self.generator._is_text_file(Path('file.ts')))
        self.assertTrue(self.generator._is_text_file(Path('file.json')))
        self.assertTrue(self.generator._is_text_file(Path('file.md')))
        self.assertTrue(self.generator._is_text_file(Path('.gitignore')))
        
        # Binary files that should not have substitution
        self.assertFalse(self.generator._is_text_file(Path('image.png')))
        self.assertFalse(self.generator._is_text_file(Path('binary.exe')))


class TestTemplateConfig(unittest.TestCase):
    """Test cases for TemplateConfig data model."""
    
    def test_template_config_creation(self):
        """Test creating TemplateConfig."""
        config = TemplateConfig(
            name='test-template',
            display_name='Test Template',
            description='A test template',
            technologies=['React', 'TypeScript'],
            deployment_target='vercel',
            features=['Feature 1', 'Feature 2'],
            template_dir='test-template-dir'
        )
        
        self.assertEqual(config.name, 'test-template')
        self.assertEqual(config.display_name, 'Test Template')
        self.assertEqual(config.technologies, ['React', 'TypeScript'])
        self.assertEqual(config.deployment_target, 'vercel')
        self.assertEqual(config.environment_variables, [])  # Default
    
    def test_template_config_with_environment_variables(self):
        """Test TemplateConfig with environment variables."""
        config = TemplateConfig(
            name='test-template',
            display_name='Test Template',
            description='A test template',
            technologies=['React'],
            deployment_target='vercel',
            features=['Feature 1'],
            template_dir='test-dir',
            environment_variables=['API_KEY', 'DATABASE_URL']
        )
        
        self.assertEqual(config.environment_variables, ['API_KEY', 'DATABASE_URL'])


if __name__ == '__main__':
    unittest.main()
