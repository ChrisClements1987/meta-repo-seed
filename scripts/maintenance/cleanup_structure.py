#!/usr/bin/env python3
"""
Project Structure Cleanup Tool

This script helps identify and optionally fix project structure violations
according to our Business-in-a-Box project organization standards.
"""

import os
import shutil
from pathlib import Path
from typing import List, Tuple, Dict


def get_allowed_root_files() -> List[str]:
    """Return list of files allowed in the root directory."""
    return [
        "README.md",
        "LICENSE",
        "LICENSE.txt", 
        "LICENSE.md",
        ".gitignore",
        ".gitattributes",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "requirements-test.txt",
        "setup.py",
        "setup.cfg",
        "pytest.ini",
        "tox.ini",
        ".pre-commit-config.yaml",
        ".pre-commit-config.yml", 
        "seeding.py",  # Legacy main script
        "PROJECT_NORTH_STAR.md",  # Strategic document
        "AGENTS.md",  # AI context
    ]


def suggest_proper_location(filename: str) -> str:
    """Suggest proper location for a misplaced file."""
    if filename.endswith('.md'):
        if any(word in filename.upper() for word in ['SUMMARY', 'WORKFLOW', 'PROCESS']):
            return "docs/development/"
        elif filename.startswith('ISSUE_') or 'IMPLEMENTATION' in filename.upper():
            return "docs/development/implementation-notes/"
        elif any(word in filename.upper() for word in ['ANALYSIS', 'RESEARCH']):
            return "docs/research/"
        else:
            return "docs/"
    
    elif filename.endswith('.py'):
        if filename.startswith('demo_') or filename.startswith('test_'):
            return "scripts/demo/"
        elif filename.startswith('sync_') or filename.endswith('_manager.py'):
            return "scripts/maintenance/"
        elif filename.startswith('_') or 'temp' in filename.lower():
            return "scripts/temp/ (or consider removing)"
        else:
            return "scripts/"
    
    elif filename.endswith(('.yaml', '.yml')):
        return "configs/ or .github/"
    
    elif filename.endswith(('.json', '.toml', '.cfg', '.ini')):
        if 'config' in filename.lower() or 'sync' in filename.lower():
            return "configs/"
        else:
            return "configs/ or root (if build configuration)"
    
    else:
        return "appropriate subdirectory"


def find_root_violations() -> List[Tuple[str, str]]:
    """Find files in root that violate project structure."""
    root_path = Path(".")
    allowed_files = set(get_allowed_root_files())
    violations = []
    
    for item in root_path.iterdir():
        # Skip directories and hidden files
        if item.is_dir() or item.name.startswith('.'):
            continue
            
        if item.name not in allowed_files:
            suggested_location = suggest_proper_location(item.name)
            violations.append((item.name, suggested_location))
    
    return violations


def create_directory_if_needed(path: str) -> None:
    """Create directory structure if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def move_file_safely(source: str, destination: str, dry_run: bool = True) -> bool:
    """Move file safely with proper handling."""
    source_path = Path(source)
    dest_path = Path(destination)
    
    if not source_path.exists():
        print(f"❌ Source file not found: {source}")
        return False
    
    # Create destination directory
    if not dry_run:
        create_directory_if_needed(str(dest_path.parent))
    
    # Check if destination exists
    if dest_path.exists():
        print(f"⚠️  Destination already exists: {destination}")
        if not dry_run:
            # Create backup
            backup_path = dest_path.with_suffix(dest_path.suffix + '.backup')
            print(f"   Creating backup: {backup_path}")
            shutil.copy2(dest_path, backup_path)
    
    if dry_run:
        print(f"   WOULD MOVE: {source} → {destination}")
    else:
        try:
            shutil.move(str(source_path), str(dest_path))
            print(f"✅ MOVED: {source} → {destination}")
        except Exception as e:
            print(f"❌ ERROR moving {source}: {e}")
            return False
    
    return True


def update_references(old_path: str, new_path: str, dry_run: bool = True) -> None:
    """Update references to moved files in documentation."""
    # Find markdown files that might reference the moved file
    md_files = list(Path(".").rglob("*.md"))
    
    for md_file in md_files:
        try:
            content = md_file.read_text(encoding='utf-8')
            old_ref = f"({old_path})"
            new_ref = f"({new_path})"
            
            if old_ref in content:
                if dry_run:
                    print(f"   WOULD UPDATE: {md_file} - reference to {old_path}")
                else:
                    updated_content = content.replace(old_ref, new_ref)
                    md_file.write_text(updated_content, encoding='utf-8')
                    print(f"✅ UPDATED: {md_file} - reference to {old_path}")
        except Exception as e:
            print(f"⚠️  Could not process {md_file}: {e}")


def main():
    """Main cleanup function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up project structure violations")
    parser.add_argument('--fix', action='store_true', help='Actually perform the moves (default is dry-run)')
    parser.add_argument('--auto-yes', action='store_true', help='Automatically confirm all moves')
    args = parser.parse_args()
    
    print("🔍 Project Structure Cleanup Tool")
    print("=" * 40)
    
    violations = find_root_violations()
    
    if not violations:
        print("✅ No root directory violations found!")
        print("   Project structure is compliant.")
        return
    
    print(f"❌ Found {len(violations)} root directory violations:")
    print()
    
    for filename, suggested_location in violations:
        print(f"📄 {filename}")
        print(f"   → Suggested location: {suggested_location}")
        
        if suggested_location.endswith("(or consider removing)"):
            print(f"   ⚠️  This file might be temporary and could be deleted")
        
        print()
    
    if not args.fix:
        print("💡 This was a dry run. Use --fix to actually move files.")
        print("💡 Use --auto-yes with --fix to skip confirmations.")
        return
    
    print("🔧 Starting cleanup process...")
    print()
    
    for filename, suggested_location in violations:
        if suggested_location.endswith("(or consider removing)"):
            if not args.auto_yes:
                response = input(f"Delete temporary file {filename}? [y/N]: ")
                if response.lower() != 'y':
                    continue
            
            try:
                Path(filename).unlink()
                print(f"🗑️  DELETED: {filename}")
            except Exception as e:
                print(f"❌ ERROR deleting {filename}: {e}")
            continue
        
        # Determine final destination path
        if suggested_location.endswith('/'):
            dest_path = suggested_location + filename
        else:
            dest_path = suggested_location
        
        if not args.auto_yes:
            response = input(f"Move {filename} to {dest_path}? [y/N]: ")
            if response.lower() != 'y':
                continue
        
        # Move the file
        if move_file_safely(filename, dest_path, dry_run=False):
            # Update references
            update_references(filename, dest_path, dry_run=False)
    
    print()
    print("🎯 Cleanup complete!")
    print("   Remember to:")
    print("   - Update any broken imports in Python files")
    print("   - Test that all functionality still works")
    print("   - Update documentation links manually if needed")
    print("   - Commit these changes with proper PR documentation")


if __name__ == "__main__":
    main()