#!/usr/bin/env python3
"""
Repository Initialization Script

This script initializes repository structure based on governance/structure/structure.json.
It's an automation script that leverages the Structure Parser Module and Repository Initializer.

Usage:
    python initialise_repo.py [--dry-run] [--verbose] [--structure PATH] [--target PATH]

This script is typically placed in meta-repo/automation/scripts/ and run from the repository root.
"""

import argparse
import sys
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent.parent / 'src'
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from automation.repository_initializer import RepositoryInitializer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the repository root with the src/ directory available")
    sys.exit(1)


def main():
    """Initialize repository structure based on structure.json."""
    parser = argparse.ArgumentParser(
        description="Initialize repository structure from structure.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script is part of the repository automation suite. It reads the structure
definition from governance/structure/structure.json and creates the complete
directory structure with placeholder files and README documentation.

Examples:
  python initialise_repo.py                    # Initialize using default structure.json
  python initialise_repo.py --dry-run         # Preview what would be created
  python initialise_repo.py --verbose         # Show detailed progress
        """
    )
    
    parser.add_argument(
        '--structure',
        type=Path,
        default=Path('governance/structure/structure.json'),
        help='Path to structure.json file (default: governance/structure/structure.json)'
    )
    
    parser.add_argument(
        '--target',
        type=Path,
        help='Target directory for initialization (default: current directory)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without making them'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true', 
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    print("🚀 Repository Structure Initializer")
    print("=" * 40)
    
    # Check if structure file exists
    if not args.structure.exists():
        print(f"❌ Structure file not found: {args.structure}")
        print()
        print("💡 This script expects a structure.json file that defines your repository layout.")
        print("   Common locations:")
        print("   - governance/structure/structure.json")
        print("   - structure.json")
        print() 
        print("   You can specify a custom path with --structure /path/to/structure.json")
        return 1
    
    # Initialize repository
    try:
        initializer = RepositoryInitializer(dry_run=args.dry_run, verbose=args.verbose)
        success = initializer.initialize_repository(args.structure, args.target)
        
        if success:
            print()
            print("✅ Repository initialization completed successfully!")
            if args.dry_run:
                print("🔍 This was a preview - run without --dry-run to apply changes")
            else:
                print("🎉 Your repository structure is now ready!")
            return 0
        else:
            print()
            print("❌ Repository initialization failed. Check the log messages above.")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Initialization cancelled by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())