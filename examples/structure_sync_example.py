#!/usr/bin/env python3
"""
Example usage of Structure Synchronization Scripts

This script demonstrates how to use the structure synchronization functionality
to create and manage project templates.
"""

import os
import shutil
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
sys.path.insert(0, src_path)

from meta_repo_seed.structure_sync import StructureSynchronizer


def create_example_project():
    """Create an example project structure."""
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    project_dir = os.path.join(temp_dir, 'example_project')
    
    # Create directory structure
    os.makedirs(os.path.join(project_dir, 'src', 'example_project'))
    os.makedirs(os.path.join(project_dir, 'tests'))
    os.makedirs(os.path.join(project_dir, 'docs'))
    
    # Create files
    files = {
        'README.md': '''# Example Project

This is an example project for demonstrating structure synchronization.

## Installation

```bash
pip install -e .
```

## Usage

```python
import example_project
print("Hello World!")
```
''',
        'setup.py': '''from setuptools import setup, find_packages

setup(
    name="example_project",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
''',
        'src/example_project/__init__.py': '''"""Example project package."""

__version__ = "1.0.0"

def hello():
    """Say hello."""
    return "Hello from example_project!"
''',
        'tests/test_example.py': '''import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import example_project

class TestExample(unittest.TestCase):
    def test_hello(self):
        result = example_project.hello()
        self.assertEqual(result, "Hello from example_project!")

if __name__ == '__main__':
    unittest.main()
''',
        'docs/api.md': '''# API Documentation

## example_project.hello()

Returns a greeting message.

**Returns:** str - A greeting message
''',
        '.gitignore': '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
'''
    }
    
    for file_path, content in files.items():
        full_path = os.path.join(project_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
    
    return project_dir, temp_dir


def demonstrate_structure_sync():
    """Demonstrate structure synchronization functionality."""
    print("=== Structure Synchronization Demonstration ===\n")
    
    # Create example project
    print("1. Creating example project structure...")
    example_dir, temp_dir = create_example_project()
    print(f"   Created example project at: {example_dir}")
    
    try:
        # Initialize synchronizer
        config_path = os.path.join(os.path.dirname(__file__), 'sync_config.yaml')
        sync = StructureSynchronizer(config_path)
        print("   Initialized StructureSynchronizer")
        
        # Scan the example project
        print("\n2. Scanning project structure...")
        structure = sync.scan_structure(example_dir)
        print(f"   Scanned structure: {structure.name}")
        print(f"   Files found: {len(structure.files)}")
        print(f"   Subdirectories: {len(structure.subdirs)}")
        
        # Save as template
        print("\n3. Saving as template...")
        template_name = 'demo_template'
        sync.save_structure(structure, template_name)
        print(f"   Template '{template_name}' saved")
        
        # List available templates
        print("\n4. Listing available templates...")
        templates = sync.list_structures()
        print("   Available templates:")
        for template in templates:
            print(f"     - {template}")
        
        # Create new project from template
        print("\n5. Creating new project from template...")
        new_project_dir = os.path.join(temp_dir, 'new_project')
        template_vars = {
            'project_name': 'new_project',
            'author_name': 'Demo User',
            'author_email': 'demo@example.com',
            'description': 'A project created from template'
        }
        
        loaded_template = sync.load_structure(template_name)
        sync.sync_structure(loaded_template, new_project_dir, template_vars)
        print(f"   New project created at: {new_project_dir}")
        
        # Verify the new project
        print("\n6. Verifying new project structure...")
        new_structure = sync.scan_structure(new_project_dir)
        print(f"   New project files: {len(new_structure.files)}")
        print(f"   New project subdirs: {len(new_structure.subdirs)}")
        
        # Compare structures
        print("\n7. Comparing original and new structures...")
        differences = sync.compare_structures(structure, new_structure)
        
        total_changes = (len(differences['files_added']) + 
                        len(differences['files_removed']) +
                        len(differences['files_modified']) +
                        len(differences['dirs_added']) +
                        len(differences['dirs_removed']))
        
        if total_changes == 0:
            print("   ✓ Structures are identical!")
        else:
            print(f"   Found {total_changes} differences:")
            for change_type, changes in differences.items():
                if changes:
                    print(f"     {change_type}: {changes}")
        
        # Show directory contents
        print(f"\n8. New project directory contents:")
        for root, dirs, files in os.walk(new_project_dir):
            level = root.replace(new_project_dir, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
        
        print("\n=== Demonstration completed successfully! ===")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\nCleaning up temporary files...")
        shutil.rmtree(temp_dir)
        print("Cleanup completed.")


def demonstrate_cli_usage():
    """Demonstrate CLI usage examples."""
    print("\n=== CLI Usage Examples ===\n")
    
    examples = [
        ("Scan a directory to create a template:",
         "python sync_structures.py scan --source ./my_project --structure my_template"),
        
        ("Sync a template to create a new project:",
         "python sync_structures.py sync --structure my_template --target ./new_project"),
        
        ("Sync with template variables:",
         '''python sync_structures.py sync --structure my_template --target ./new_project --vars '{"project_name": "MyApp", "author_name": "John Doe"}' '''),
        
        ("List available templates:",
         "python sync_structures.py list"),
        
        ("Compare two templates:",
         "python sync_structures.py compare --structure1 old_template --structure2 new_template"),
        
        ("Compare template with directory:",
         "python sync_structures.py compare --structure1 my_template --source ./existing_project"),
        
        ("Interactive sync (prompts for variables):",
         "python sync_structures.py sync --structure my_template --target ./new_project --interactive"),
    ]
    
    for description, command in examples:
        print(f"{description}")
        print(f"  {command}")
        print()


def main():
    """Main function."""
    print("Structure Synchronization Example")
    print("=" * 40)
    
    # Check if we should run the full demonstration
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        demonstrate_structure_sync()
    else:
        print("This script demonstrates the Structure Synchronization functionality.")
        print("Add --demo flag to run the full demonstration:")
        print(f"  python {sys.argv[0]} --demo")
        
        demonstrate_cli_usage()


if __name__ == '__main__':
    main()