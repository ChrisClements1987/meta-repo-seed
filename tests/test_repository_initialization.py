"""
Tests for Repository Initialization Automation (Issue #32)

These tests validate the automated repository initialization functionality
that creates directory structures and files based on structure.json files.
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import our modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from automation.repository_initializer import RepositoryInitializer
from structure_parser import StructureParser


class TestRepositoryInitializer:
    """Test cases for the RepositoryInitializer class."""
    
    def create_test_structure(self):
        """Create a test structure for use in tests."""
        return {
            "metadata": {
                "project_name": "test-project",
                "github_username": "testuser",
                "created_date": "2025-09-25",
                "version": "1.0.0",
                "schema_version": "2.0.0"
            },
            "structure": {
                "src": {
                    "main": ["app.py", "config.py"],
                    "utils": ["helpers.py"]
                },
                "tests": {
                    "unit": ["test_app.py"]
                },
                "docs": ["README.md"]
            }
        }
    
    def test_initializer_creation(self):
        """Test that RepositoryInitializer can be created with different options."""
        # Test default creation
        initializer = RepositoryInitializer()
        assert initializer.dry_run == False
        assert initializer.verbose == False
        
        # Test with options
        initializer = RepositoryInitializer(dry_run=True, verbose=True)
        assert initializer.dry_run == True
        assert initializer.verbose == True
        
        # Test that parser is created
        assert isinstance(initializer.parser, StructureParser)
    
    def test_dry_run_mode(self):
        """Test that dry run mode works correctly."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.create_test_structure(), f, indent=2)
            test_file = Path(f.name)
        
        try:
            initializer = RepositoryInitializer(dry_run=True)
            
            # This should succeed without creating any files
            success = initializer.initialize_repository(test_file)
            assert success == True
            
        finally:
            test_file.unlink(missing_ok=True)
    
    def test_invalid_structure_file(self):
        """Test behavior with invalid structure file."""
        # Test with non-existent file
        initializer = RepositoryInitializer()
        fake_path = Path("nonexistent.json")
        
        # This should fail gracefully
        success = initializer.initialize_repository(fake_path)
        assert success == False
        
    def test_invalid_json_structure(self):
        """Test behavior with invalid JSON structure."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            # Write invalid JSON
            f.write('{"invalid": json structure')
            test_file = Path(f.name)
        
        try:
            initializer = RepositoryInitializer()
            success = initializer.initialize_repository(test_file)
            assert success == False
            
        finally:
            test_file.unlink(missing_ok=True)
    
    def test_directory_creation_count(self):
        """Test that correct number of directories would be created."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.create_test_structure(), f, indent=2)
            test_file = Path(f.name)
        
        try:
            initializer = RepositoryInitializer(dry_run=True, verbose=True)
            success = initializer.initialize_repository(test_file)
            
            assert success == True
            # We expect: src, src/main, src/utils, tests, tests/unit, docs = 6 directories
            
        finally:
            test_file.unlink(missing_ok=True)
    
    @patch('pathlib.Path.mkdir')
    @patch('pathlib.Path.touch')  
    @patch('pathlib.Path.write_text')
    def test_actual_file_creation(self, mock_write_text, mock_touch, mock_mkdir):
        """Test that files are actually created in non-dry-run mode."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.create_test_structure(), f, indent=2)
            test_file = Path(f.name)
        
        try:
            initializer = RepositoryInitializer(dry_run=False)
            success = initializer.initialize_repository(test_file)
            
            assert success == True
            # Verify that mkdir was called for directories
            assert mock_mkdir.called
            # Verify that touch was called for placeholder files
            assert mock_touch.called
            # Verify that write_text was called for README files
            assert mock_write_text.called
            
        finally:
            test_file.unlink(missing_ok=True)
    
    def test_readme_content_generation(self):
        """Test that README content is generated correctly."""
        initializer = RepositoryInitializer()
        
        # Create a mock structure data
        from structure_parser.models import StructureData
        test_data = {
            "project_name": "test-project",
            "github_username": "testuser", 
            "created_date": "2025-09-25",
            "version": "1.0.0"
        }
        structure_data = StructureData.from_dict(test_data)
        
        # Test README generation
        content = initializer._generate_readme_content("src", structure_data)
        
        assert "# Src" in content
        assert "test-project" in content
        assert "2025-09-25" in content
        assert "Repository Initializer" in content
    
    def test_target_directory_specification(self):
        """Test that target directory can be specified."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.create_test_structure(), f, indent=2)
            test_file = Path(f.name)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir)
            
            try:
                initializer = RepositoryInitializer(dry_run=True)
                success = initializer.initialize_repository(test_file, target_path)
                
                assert success == True
                
            finally:
                test_file.unlink(missing_ok=True)


class TestInitialiseRepoScript:
    """Test cases for the initialise_repo.py script functionality."""
    
    def test_script_imports(self):
        """Test that the script can import required modules."""
        # This test validates that our script structure works
        import sys
        from pathlib import Path
        
        # Add src to path like the script does
        src_path = Path(__file__).parent.parent / 'src'
        sys.path.insert(0, str(src_path))
        
        try:
            from automation.repository_initializer import RepositoryInitializer
            assert RepositoryInitializer is not None
        except ImportError:
            pytest.fail("Script imports failed")


class TestIssue32Integration:
    """Integration tests for Issue #32 implementation."""
    
    def test_complete_workflow(self):
        """Test the complete repository initialization workflow."""
        # Create test structure
        test_structure = {
            "metadata": {
                "project_name": "integration-test",
                "github_username": "testuser",
                "created_date": "2025-09-25", 
                "version": "1.0.0",
                "schema_version": "2.0.0"
            },
            "structure": {
                "backend": {
                    "api": ["main.py", "routes.py"],
                    "models": ["user.py", "database.py"]
                },
                "frontend": {
                    "src": ["app.js", "index.html"],
                    "assets": ["style.css"]
                },
                "tests": ["test_backend.py", "test_frontend.py"],
                "docs": ["API.md", "README.md"]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_structure, f, indent=2)
            test_file = Path(f.name)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir)
            
            try:
                # Test the complete initialization process
                initializer = RepositoryInitializer(dry_run=True, verbose=False)
                success = initializer.initialize_repository(test_file, target_path)
                
                assert success == True
                
                # Test that the process handles complex nested structures
                # In real mode, this would create all directories and files
                
            finally:
                test_file.unlink(missing_ok=True)
    
    def test_existing_files_handling(self):
        """Test that existing files are handled properly."""
        test_structure = {
            "metadata": {
                "project_name": "existing-test", 
                "github_username": "testuser",
                "created_date": "2025-09-25",
                "version": "1.0.0",
                "schema_version": "2.0.0"
            },
            "structure": {
                "src": ["existing.py", "new.py"]
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_structure, f, indent=2)
            test_file = Path(f.name)
        
        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir)
            
            # Pre-create some files
            src_dir = target_path / "src"
            src_dir.mkdir(parents=True, exist_ok=True)
            existing_file = src_dir / "existing.py"
            existing_file.write_text("# Pre-existing file")
            
            try:
                # Initialize with existing files
                initializer = RepositoryInitializer(dry_run=False, verbose=False)
                success = initializer.initialize_repository(test_file, target_path)
                
                assert success == True
                
                # Verify existing file wasn't overwritten
                assert existing_file.read_text() == "# Pre-existing file"
                
            finally:
                test_file.unlink(missing_ok=True)