#!/usr/bin/env python3
"""
Repository Initializer

This module provides automated repository initialization based on structure.json files.
Uses the Structure Parser Module to read and validate repository structures.
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set

# Import our Structure Parser Module
try:
    from structure_parser import StructureParser, StructureParserError
except ImportError:
    print("ERROR: Structure Parser Module not found. Ensure it's installed.")
    sys.exit(1)


class RepositoryInitializer:
    """Automated repository structure initialization."""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """Initialize the repository initializer.
        
        Args:
            dry_run: If True, show what would be created without making changes
            verbose: Enable detailed logging
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.logger = self._setup_logging()
        self.parser = StructureParser()
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger('repository_initializer')
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
    def initialize_repository(self, structure_file: Path, target_directory: Path = None) -> bool:
        """Initialize repository structure based on structure.json file.
        
        Args:
            structure_file: Path to structure.json file
            target_directory: Target directory for initialization (default: current dir)
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        try:
            if target_directory is None:
                target_directory = Path.cwd()
                
            self.logger.info(f"🚀 Initializing repository from {structure_file}")
            self.logger.info(f"📁 Target directory: {target_directory}")
            
            if self.dry_run:
                self.logger.info("🔍 DRY RUN MODE - No actual changes will be made")
                
            # Parse the structure file
            self.logger.info("📖 Parsing structure file...")
            structure_data = self.parser.parse_file(structure_file)
            
            # Validate the structure
            self.logger.info("✅ Validating structure...")
            validation_result = self.parser.validate(structure_data.__dict__)
            
            if not validation_result.is_valid:
                self.logger.error("❌ Structure validation failed:")
                self.logger.error(validation_result.get_detailed_report())
                return False
                
            self.logger.info(f"✅ Structure validation passed for project: {structure_data.project_name}")
            
            # Create directory structure
            directories_created = self._create_directory_structure(structure_data, target_directory)
            
            # Create placeholder files
            files_created = self._create_placeholder_files(structure_data, target_directory)
            
            # Create README files
            readmes_created = self._create_readme_files(structure_data, target_directory)
            
            # Summary
            self.logger.info("🎉 Repository initialization completed!")
            self.logger.info(f"📁 Directories created: {directories_created}")
            self.logger.info(f"📄 Files created: {files_created}")
            self.logger.info(f"📚 README files created: {readmes_created}")
            
            if self.dry_run:
                self.logger.info("ℹ️  This was a dry run - no actual changes were made")
                
            return True
            
        except StructureParserError as e:
            self.logger.error(f"❌ Structure parser error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected error during initialization: {e}")
            return False
            
    def _create_directory_structure(self, structure_data, target_directory: Path) -> int:
        """Create the directory structure from parsed data."""
        self.logger.info("📁 Creating directory structure...")
        
        directories = self.parser.get_directory_structure(structure_data)
        created_count = 0
        
        for directory_path in directories:
            full_path = target_directory / directory_path
            
            if self.dry_run:
                self.logger.debug(f"[DRY RUN] Would create directory: {full_path}")
            else:
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    self.logger.debug(f"Created directory: {full_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to create directory {full_path}: {e}")
                    continue
                    
            created_count += 1
            
        return created_count
        
    def _create_placeholder_files(self, structure_data, target_directory: Path) -> int:
        """Create placeholder files from the structure data."""
        self.logger.info("📄 Creating placeholder files...")
        
        created_count = 0
        
        # Get all files from structure
        all_directories = structure_data.get_all_directories()
        
        for directory in all_directories:
            files = structure_data.get_directory_files(directory)
            
            for file_name in files:
                file_path = target_directory / directory / file_name
                
                if self.dry_run:
                    self.logger.debug(f"[DRY RUN] Would create file: {file_path}")
                else:
                    if not file_path.exists():
                        try:
                            file_path.parent.mkdir(parents=True, exist_ok=True)
                            file_path.touch()
                            self.logger.debug(f"Created placeholder file: {file_path}")
                        except Exception as e:
                            self.logger.warning(f"Failed to create file {file_path}: {e}")
                            continue
                    else:
                        self.logger.debug(f"File already exists: {file_path}")
                        
                created_count += 1
                
        return created_count
        
    def _create_readme_files(self, structure_data, target_directory: Path) -> int:
        """Create README.md files for major directories."""
        self.logger.info("📚 Creating README files...")
        
        created_count = 0
        
        # Create README for main directories
        main_directories = structure_data.get_top_level_directories()
        
        for directory in main_directories:
            readme_path = target_directory / directory / "README.md"
            
            if self.dry_run:
                self.logger.debug(f"[DRY RUN] Would create README: {readme_path}")
            else:
                if not readme_path.exists():
                    try:
                        readme_content = self._generate_readme_content(directory, structure_data)
                        readme_path.parent.mkdir(parents=True, exist_ok=True)
                        readme_path.write_text(readme_content, encoding='utf-8')
                        self.logger.debug(f"Created README: {readme_path}")
                    except Exception as e:
                        self.logger.warning(f"Failed to create README {readme_path}: {e}")
                        continue
                else:
                    self.logger.debug(f"README already exists: {readme_path}")
                    
            created_count += 1
            
        return created_count
        
    def _generate_readme_content(self, directory: str, structure_data) -> str:
        """Generate README content for a directory."""
        content = f"""# {directory.replace('-', ' ').title()}

This directory is part of the **{structure_data.project_name}** repository structure.

## Structure

"""
        
        # List subdirectories and files
        if structure_data.has_directory(directory):
            files = structure_data.get_directory_files(directory)
            if files:
                content += "### Files:\n"
                for file_name in sorted(files):
                    content += f"- `{file_name}`\n"
                content += "\n"
                
        content += f"""## Purpose

This directory serves as part of the automated repository structure for {structure_data.project_name}.

---

*This README was automatically generated by the Repository Initializer.*
*Last updated: {structure_data.created_date}*
"""
        
        return content


def main():
    """Main entry point for the repository initializer."""
    parser = argparse.ArgumentParser(
        description="Initialize repository structure from structure.json",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python repository_initializer.py                           # Use structure.json in current dir
  python repository_initializer.py --structure custom.json   # Use custom structure file
  python repository_initializer.py --dry-run                 # Preview changes only
  python repository_initializer.py --target /path/to/repo    # Initialize in specific directory
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
    
    # Validate structure file exists
    if not args.structure.exists():
        print(f"❌ Error: Structure file not found: {args.structure}")
        print("💡 Make sure you're running from a repository with a governance/structure/structure.json file")
        return 1
        
    # Initialize the repository
    initializer = RepositoryInitializer(dry_run=args.dry_run, verbose=args.verbose)
    
    success = initializer.initialize_repository(args.structure, args.target)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())