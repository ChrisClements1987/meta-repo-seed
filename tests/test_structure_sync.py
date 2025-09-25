"""
Tests for Structure Synchronization functionality.

This module contains unit tests for the structure synchronization system
implemented for Issue #33.
"""

import unittest
import tempfile
import shutil
import json
import os
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from meta_repo_seed.structure_sync import (
    StructureSynchronizer,
    DirectoryStructure,
    FileTemplate
)


class TestStructureSynchronizer(unittest.TestCase):
    """Test cases for StructureSynchronizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.templates_dir = os.path.join(self.test_dir, 'templates')
        self.output_dir = os.path.join(self.test_dir, 'output')
        self.config_path = os.path.join(self.test_dir, 'test_config.yaml')
        
        # Create test config with isolated templates directory
        test_config = {
            'templates_dir': os.path.join(self.test_dir, 'templates'),
            'output_dir': os.path.join(self.test_dir, 'output'),
            'sync_rules': {
                'preserve_existing': True,
                'backup_before_sync': False,
                'exclude_patterns': ['.git', '__pycache__']
            }
        }
        
        with open(self.config_path, 'w') as f:
            import yaml
            yaml.safe_dump(test_config, f)
        
        # Initialize synchronizer
        self.sync = StructureSynchronizer(self.config_path)
        
        # Create test directory structure
        self.test_source = os.path.join(self.test_dir, 'test_source')
        os.makedirs(self.test_source)
        os.makedirs(os.path.join(self.test_source, 'subdir'))
        
        # Create test files
        with open(os.path.join(self.test_source, 'file1.txt'), 'w') as f:
            f.write('Test content 1')
        
        with open(os.path.join(self.test_source, 'subdir', 'file2.txt'), 'w') as f:
            f.write('Test content 2')
    
    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)
    
    def test_scan_structure(self):
        """Test scanning a directory structure."""
        structure = self.sync.scan_structure(self.test_source)
        
        self.assertIsInstance(structure, DirectoryStructure)
        self.assertEqual(structure.name, 'test_source')
        self.assertEqual(len(structure.files), 1)  # file1.txt
        self.assertEqual(len(structure.subdirs), 1)  # subdir
        
        # Check subdir
        subdir = structure.subdirs[0]
        self.assertEqual(subdir.name, 'subdir')
        self.assertEqual(len(subdir.files), 1)  # file2.txt
    
    def test_save_and_load_structure(self):
        """Test saving and loading structure definitions."""
        structure = self.sync.scan_structure(self.test_source)
        
        # Save structure
        self.sync.save_structure(structure, 'test_template')
        
        # Load structure
        loaded_structure = self.sync.load_structure('test_template')
        
        self.assertEqual(structure.name, loaded_structure.name)
        self.assertEqual(len(structure.files), len(loaded_structure.files))
        self.assertEqual(len(structure.subdirs), len(loaded_structure.subdirs))
    
    def test_sync_structure(self):
        """Test synchronizing a structure to a target directory."""
        # Create and save a structure
        structure = self.sync.scan_structure(self.test_source)
        self.sync.save_structure(structure, 'test_template')
        
        # Sync to target
        target_dir = os.path.join(self.test_dir, 'sync_target')
        template_vars = {'test_var': 'test_value'}
        
        self.sync.sync_structure(structure, target_dir, template_vars)
        
        # Verify sync
        self.assertTrue(os.path.exists(target_dir))
        self.assertTrue(os.path.exists(os.path.join(target_dir, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(target_dir, 'subdir')))
        self.assertTrue(os.path.exists(os.path.join(target_dir, 'subdir', 'file2.txt')))
    
    def test_list_structures(self):
        """Test listing available structure templates."""
        # Should initially be empty in isolated test directory
        structures = self.sync.list_structures()
        self.assertEqual(len(structures), 0)
        
        # Add a structure
        structure = self.sync.scan_structure(self.test_source)
        self.sync.save_structure(structure, 'test_template')
        
        # Should now have one structure
        structures = self.sync.list_structures()
        self.assertEqual(len(structures), 1)
        self.assertIn('test_template', structures)
    
    def test_compare_structures(self):
        """Test comparing two structures."""
        # Create two similar structures
        structure1 = self.sync.scan_structure(self.test_source)
        
        # Create a modified copy
        test_source2 = os.path.join(self.test_dir, 'test_source2')
        shutil.copytree(self.test_source, test_source2)
        
        # Add a file to the second structure
        with open(os.path.join(test_source2, 'new_file.txt'), 'w') as f:
            f.write('New content')
        
        structure2 = self.sync.scan_structure(test_source2)
        
        # Compare structures
        differences = self.sync.compare_structures(structure1, structure2)
        
        # Should have at least 1 file added (new_file.txt)
        self.assertGreaterEqual(len(differences['files_added']), 1)
        # Check that new_file.txt is in the added files
        added_files_str = str(differences['files_added'])
        self.assertTrue('new_file.txt' in added_files_str)


class TestFileTemplate(unittest.TestCase):
    """Test cases for FileTemplate."""
    
    def test_file_template_creation(self):
        """Test creating a FileTemplate."""
        template = FileTemplate(
            path='test.txt',
            content='Test content',
            template_vars={'var': 'value'}
        )
        
        self.assertEqual(template.path, 'test.txt')
        self.assertEqual(template.content, 'Test content')
        self.assertEqual(template.template_vars, {'var': 'value'})
        self.assertIsNotNone(template.checksum)
        self.assertIsNotNone(template.last_updated)
    
    def test_checksum_calculation(self):
        """Test checksum calculation."""
        template1 = FileTemplate(
            path='test.txt',
            content='Test content',
            template_vars={}
        )
        
        template2 = FileTemplate(
            path='test.txt',
            content='Test content',
            template_vars={}
        )
        
        template3 = FileTemplate(
            path='test.txt',
            content='Different content',
            template_vars={}
        )
        
        # Same content should have same checksum
        self.assertEqual(template1.checksum, template2.checksum)
        
        # Different content should have different checksum
        self.assertNotEqual(template1.checksum, template3.checksum)


class TestDirectoryStructure(unittest.TestCase):
    """Test cases for DirectoryStructure."""
    
    def test_directory_structure_creation(self):
        """Test creating a DirectoryStructure."""
        files = [
            FileTemplate('file1.txt', 'content1', {}),
            FileTemplate('file2.txt', 'content2', {})
        ]
        
        subdirs = [
            DirectoryStructure('subdir1', 'path/subdir1', [], [], {})
        ]
        
        structure = DirectoryStructure(
            name='test_dir',
            path='path/test_dir',
            subdirs=subdirs,
            files=files,
            metadata={'key': 'value'}
        )
        
        self.assertEqual(structure.name, 'test_dir')
        self.assertEqual(len(structure.files), 2)
        self.assertEqual(len(structure.subdirs), 1)
        self.assertEqual(structure.metadata['key'], 'value')
    
    def test_to_dict_and_from_dict(self):
        """Test serialization and deserialization."""
        files = [
            FileTemplate('file1.txt', 'content1', {})
        ]
        
        structure = DirectoryStructure(
            name='test_dir',
            path='path/test_dir',
            subdirs=[],
            files=files,
            metadata={'key': 'value'}
        )
        
        # Convert to dict
        data = structure.to_dict()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], 'test_dir')
        
        # Convert back from dict
        restored = DirectoryStructure.from_dict(data)
        self.assertEqual(restored.name, structure.name)
        self.assertEqual(restored.path, structure.path)
        self.assertEqual(len(restored.files), len(structure.files))


if __name__ == '__main__':
    unittest.main()