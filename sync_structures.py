#!/usr/bin/env python3
"""
Structure Synchronization CLI Script

Command-line interface for the Structure Synchronization functionality.
This script provides easy access to scan, sync, and manage repository structures.

Usage:
    python sync_structures.py scan --source /path/to/source --structure my_template
    python sync_structures.py sync --structure my_template --target /path/to/target
    python sync_structures.py list
"""

import sys
import os
import argparse
import json
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from meta_repo_seed.structure_sync import StructureSynchronizer, DirectoryStructure
except ImportError:
    print("Error: Unable to import StructureSynchronizer. Make sure the module is installed.")
    sys.exit(1)


def scan_command(args):
    """Handle the scan command."""
    if not args.source:
        print("Error: --source is required for scan command")
        return 1
    
    if not os.path.exists(args.source):
        print(f"Error: Source directory does not exist: {args.source}")
        return 1
    
    try:
        sync = StructureSynchronizer(args.config)
        structure = sync.scan_structure(args.source)
        
        structure_name = args.structure or Path(args.source).name
        sync.save_structure(structure, structure_name)
        
        print(f"✓ Structure '{structure_name}' scanned and saved successfully")
        print(f"  - Files: {len(structure.files)}")
        print(f"  - Subdirectories: {len(structure.subdirs)}")
        print(f"  - Template saved to: templates/{structure_name}.json")
        
        return 0
    except Exception as e:
        print(f"Error scanning structure: {e}")
        return 1


def sync_command(args):
    """Handle the sync command."""
    if not args.structure:
        print("Error: --structure is required for sync command")
        return 1
    
    if not args.target:
        print("Error: --target is required for sync command")
        return 1
    
    try:
        sync = StructureSynchronizer(args.config)
        structure = sync.load_structure(args.structure)
        
        # Parse template variables
        template_vars = {}
        if args.vars:
            try:
                template_vars = json.loads(args.vars)
            except json.JSONDecodeError as e:
                print(f"Error parsing template variables: {e}")
                return 1
        
        # Interactive variable collection if not provided
        if not template_vars and args.interactive:
            template_vars = collect_template_vars()
        
        sync.sync_structure(structure, args.target, template_vars)
        
        print(f"✓ Structure '{args.structure}' synced to '{args.target}' successfully")
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: Structure template not found: {e}")
        return 1
    except Exception as e:
        print(f"Error syncing structure: {e}")
        return 1


def list_command(args):
    """Handle the list command."""
    try:
        sync = StructureSynchronizer(args.config)
        structures = sync.list_structures()
        
        if not structures:
            print("No structure templates found.")
            print("Use 'scan' command to create templates from existing directories.")
            return 0
        
        print("Available structure templates:")
        for structure_name in structures:
            try:
                structure = sync.load_structure(structure_name)
                print(f"  • {structure_name}")
                print(f"    Files: {len(structure.files)}, Subdirs: {len(structure.subdirs)}")
                if 'scanned_at' in structure.metadata:
                    print(f"    Created: {structure.metadata['scanned_at']}")
            except Exception as e:
                print(f"  • {structure_name} (error loading: {e})")
        
        return 0
    except Exception as e:
        print(f"Error listing structures: {e}")
        return 1


def compare_command(args):
    """Handle the compare command."""
    if not args.structure1 or not args.structure2:
        print("Error: Both --structure1 and --structure2 are required for compare command")
        return 1
    
    try:
        sync = StructureSynchronizer(args.config)
        
        if args.source:
            # Compare with a directory
            structure1 = sync.load_structure(args.structure1)
            structure2 = sync.scan_structure(args.source)
        else:
            # Compare two templates
            structure1 = sync.load_structure(args.structure1)
            structure2 = sync.load_structure(args.structure2)
        
        differences = sync.compare_structures(structure1, structure2)
        
        print(f"Comparison between '{args.structure1}' and '{args.structure2 or args.source}':")
        
        if differences['files_added']:
            print(f"  Files added ({len(differences['files_added'])}):")
            for f in differences['files_added']:
                print(f"    + {f}")
        
        if differences['files_removed']:
            print(f"  Files removed ({len(differences['files_removed'])}):")
            for f in differences['files_removed']:
                print(f"    - {f}")
        
        if differences['files_modified']:
            print(f"  Files modified ({len(differences['files_modified'])}):")
            for f in differences['files_modified']:
                print(f"    ~ {f}")
        
        if differences['dirs_added']:
            print(f"  Directories added ({len(differences['dirs_added'])}):")
            for d in differences['dirs_added']:
                print(f"    + {d}/")
        
        if differences['dirs_removed']:
            print(f"  Directories removed ({len(differences['dirs_removed'])}):")
            for d in differences['dirs_removed']:
                print(f"    - {d}/")
        
        if not any(differences.values()):
            print("  No differences found!")
        
        return 0
    except Exception as e:
        print(f"Error comparing structures: {e}")
        return 1


def collect_template_vars():
    """Interactively collect template variables."""
    print("Enter template variables (press Enter to skip):")
    vars_dict = {}
    
    common_vars = [
        ('project_name', 'Project name'),
        ('author_name', 'Author name'),
        ('author_email', 'Author email'),
        ('description', 'Project description'),
    ]
    
    for var, prompt in common_vars:
        value = input(f"{prompt}: ").strip()
        if value:
            vars_dict[var] = value
    
    return vars_dict


def create_parser():
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        description='Structure Synchronization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan a directory to create a template
  python sync_structures.py scan --source ./my_project --structure python_template
  
  # Sync a template to a new directory
  python sync_structures.py sync --structure python_template --target ./new_project
  
  # Sync with template variables
  python sync_structures.py sync --structure python_template --target ./new_project --vars '{"project_name": "MyApp", "author_name": "John Doe"}'
  
  # List available templates
  python sync_structures.py list
  
  # Compare structures
  python sync_structures.py compare --structure1 template1 --structure2 template2
        """)
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan a directory to create a structure template')
    scan_parser.add_argument('--source', required=True, help='Source directory to scan')
    scan_parser.add_argument('--structure', help='Name for the structure template (default: directory name)')
    scan_parser.add_argument('--config', help='Configuration file path')
    
    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Synchronize a structure template to a target directory')
    sync_parser.add_argument('--structure', required=True, help='Structure template name')
    sync_parser.add_argument('--target', required=True, help='Target directory for sync')
    sync_parser.add_argument('--vars', help='Template variables in JSON format')
    sync_parser.add_argument('--config', help='Configuration file path')
    sync_parser.add_argument('--interactive', action='store_true', help='Interactively collect template variables')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available structure templates')
    list_parser.add_argument('--config', help='Configuration file path')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two structure templates or template with directory')
    compare_parser.add_argument('--structure1', required=True, help='First structure template')
    compare_parser.add_argument('--structure2', help='Second structure template')
    compare_parser.add_argument('--source', help='Directory to compare with (alternative to --structure2)')
    compare_parser.add_argument('--config', help='Configuration file path')
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Command dispatch
    commands = {
        'scan': scan_command,
        'sync': sync_command,
        'list': list_command,
        'compare': compare_command
    }
    
    return commands[args.command](args)


if __name__ == '__main__':
    sys.exit(main())