#!/usr/bin/env python3
"""
Demo script for the Structure Parser Module.

This script demonstrates the basic functionality of the StructureParser
module for parsing and validating structure.json files.
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from structure_parser import StructureParser, StructureParserError


def demo_parser():
    """Demonstrate parser functionality."""
    print("🔧 Structure Parser Module Demo")
    print("=" * 50)
    
    # Initialize parser
    print("1. Initializing parser...")
    parser = StructureParser()
    schema_info = parser.get_schema_info()
    print(f"   Schema validation: {'✅ Enabled' if schema_info['has_validation'] else '❌ Disabled (fallback mode)'}")
    print(f"   Schema version: {schema_info['schema_version']}")
    print()
    
    # Test with fixtures
    fixtures_dir = Path("tests/test_structure_parser/fixtures")
    
    if fixtures_dir.exists():
        # Test valid structure
        valid_file = fixtures_dir / "valid_structure.json"
        if valid_file.exists():
            print("2. Parsing valid structure file...")
            try:
                result = parser.parse_file(valid_file)
                print(f"   ✅ Successfully parsed: {result.project_name}")
                print(f"   Project: {result.project_name}")
                print(f"   User: {result.github_username}")
                print(f"   Version: {result.version}")
                print(f"   Top-level directories: {', '.join(result.get_top_level_directories())}")
                
                # Demonstrate directory checking
                print("\n   Directory structure analysis:")
                print(f"   - Has 'meta-repo': {result.has_directory('meta-repo')}")
                print(f"   - Has 'meta-repo/governance': {result.has_directory('meta-repo/governance')}")
                print(f"   - Has 'nonexistent': {result.has_directory('nonexistent')}")
                
                # Show files in governance
                governance_files = result.get_directory_files('meta-repo/governance')
                if governance_files:
                    print(f"   - Files in meta-repo/governance: {', '.join(governance_files[:3])}...")
                
            except StructureParserError as e:
                print(f"   ❌ Error: {e}")
        else:
            print("2. ❌ Valid fixture file not found")
        
        print()
        
        # Test invalid structure
        invalid_file = fixtures_dir / "invalid_structure.json"
        if invalid_file.exists():
            print("3. Testing invalid structure file...")
            try:
                result = parser.parse_file(invalid_file)
                print("   ❌ Expected validation to fail!")
            except StructureParserError as e:
                print(f"   ✅ Correctly caught validation error: {type(e).__name__}")
                print(f"   Error details: {str(e)[:100]}...")
        else:
            print("3. ❌ Invalid fixture file not found")
    else:
        print("2-3. ❌ Fixtures directory not found, skipping file tests")
    
    print()
    
    # Test string parsing
    print("4. Testing string parsing...")
    test_structure = {
        "project_name": "demo-project",
        "github_username": "demouser",
        "version": "2.0",
        "created_date": "2025-09-24",
        "structure": {
            "meta-repo": {
                "governance": {
                    "structure": ["structure.json"],
                    "policies": ["contributing.md"]
                }
            }
        }
    }
    
    try:
        result = parser.parse_string(json.dumps(test_structure))
        print(f"   ✅ Successfully parsed demo structure")
        print(f"   Directories found: {len(result.get_all_directories())}")
        
        # Test validation
        validation_result = parser.validate(test_structure)
        print(f"   Validation: {'✅ Passed' if validation_result.is_valid else '❌ Failed'}")
        if validation_result.error_count > 0:
            print(f"   Errors: {validation_result.error_count}")
        if validation_result.warning_count > 0:
            print(f"   Warnings: {validation_result.warning_count}")
        
    except StructureParserError as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # Test directory structure extraction
    print("5. Testing directory structure extraction...")
    if 'result' in locals():
        directories = parser.get_directory_structure(result)
        print(f"   ✅ Extracted {len(directories)} directory paths")
        for i, directory in enumerate(directories[:5]):
            print(f"   - {directory}")
        if len(directories) > 5:
            print(f"   ... and {len(directories) - 5} more")
    
    print()
    print("🎯 Demo completed!")
    print("\nNext steps:")
    print("- Install jsonschema for full validation: pip install jsonschema")
    print("- Run tests: python -m pytest tests/test_structure_parser/")
    print("- Check out docs/architecture/structure-parser-interface.md for details")


if __name__ == "__main__":
    demo_parser()