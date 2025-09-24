#!/usr/bin/env python3
"""
Roadmap Management Helper

This script helps manage the roadmap by providing utilities to:
- Move features between roadmap sections
- Update feature status
- Generate roadmap reports
- Sync with GitHub issues

Usage:
    python roadmap_manager.py --help
"""

import argparse
import re
from datetime import datetime
from pathlib import Path

def read_roadmap():
    """Read the current ROADMAP.md file"""
    roadmap_path = Path("ROADMAP.md")
    if roadmap_path.exists():
        return roadmap_path.read_text(encoding='utf-8')
    return ""

def read_changelog():
    """Read the current CHANGELOG.md file"""
    changelog_path = Path("CHANGELOG.md")
    if changelog_path.exists():
        return changelog_path.read_text(encoding='utf-8')
    return ""

def move_to_changelog(feature_name, version, feature_description):
    """Move a completed feature from roadmap to changelog"""
    print(f"Moving '{feature_name}' to CHANGELOG.md under version {version}")
    
    # Read current changelog
    changelog_content = read_changelog()
    
    # Find the unreleased section
    unreleased_pattern = r'## \[Unreleased\]\s*\n\s*\n### Added\s*\n'
    new_entry = f"- **{feature_name}** - {feature_description}\n"
    
    # Add the feature to the unreleased section
    if '## [Unreleased]' in changelog_content:
        # Insert after "### Added"
        updated_content = re.sub(
            r'(### Added\s*\n)',
            f'\\1{new_entry}',
            changelog_content
        )
    else:
        # Create unreleased section if it doesn't exist
        unreleased_section = f"""## [Unreleased]

### Added
{new_entry}
"""
        # Insert after the main header
        updated_content = re.sub(
            r'(# Changelog.*?\n\n)',
            f'\\1{unreleased_section}\n',
            changelog_content,
            flags=re.DOTALL
        )
    
    # Write back to file
    Path("CHANGELOG.md").write_text(updated_content, encoding='utf-8')
    print("✅ Feature added to CHANGELOG.md")

def remove_from_roadmap(feature_name):
    """Remove a completed feature from the roadmap"""
    print(f"Removing '{feature_name}' from ROADMAP.md")
    
    roadmap_content = read_roadmap()
    
    # Pattern to match feature items (lines starting with - [ ])
    pattern = rf'- \[ \] \*\*{re.escape(feature_name)}\*\*.*?\n(?:  .*?\n)*'
    updated_content = re.sub(pattern, '', roadmap_content, flags=re.MULTILINE)
    
    Path("ROADMAP.md").write_text(updated_content, encoding='utf-8')
    print("✅ Feature removed from ROADMAP.md")

def add_to_roadmap(feature_name, feature_description, section="Next Release"):
    """Add a new feature to the roadmap"""
    print(f"Adding '{feature_name}' to ROADMAP.md in {section} section")
    
    roadmap_content = read_roadmap()
    
    # Create the feature entry
    feature_entry = f"- [ ] **{feature_name}** - {feature_description}\n"
    
    # Find the appropriate section and add the feature
    if section == "Next Release":
        section_pattern = r'(### High Priority\s*\n)'
    elif section == "Future Releases":
        section_pattern = r'(### Advanced Features\s*\n)'
    else:
        section_pattern = rf'(### {section}\s*\n)'
    
    updated_content = re.sub(
        section_pattern,
        f'\\1{feature_entry}',
        roadmap_content
    )
    
    Path("ROADMAP.md").write_text(updated_content, encoding='utf-8')
    print("✅ Feature added to ROADMAP.md")

def list_roadmap_features():
    """List all features currently in the roadmap"""
    roadmap_content = read_roadmap()
    
    # Extract all feature items
    pattern = r'- \[ \] \*\*(.*?)\*\* - (.*?)(?:\n|$)'
    features = re.findall(pattern, roadmap_content)
    
    if features:
        print("\n📋 Current Roadmap Features:")
        print("-" * 50)
        for i, (name, description) in enumerate(features, 1):
            print(f"{i:2d}. {name}")
            print(f"    {description}")
            print()
    else:
        print("No features found in roadmap")

def generate_roadmap_report():
    """Generate a summary report of the roadmap"""
    roadmap_content = read_roadmap()
    
    # Count features in each section
    sections = {
        "High Priority": 0,
        "Medium Priority": 0,
        "Advanced Features": 0,
        "Developer Experience": 0,
        "Integration & Automation": 0
    }
    
    for section in sections.keys():
        pattern = rf'### {section}.*?(?=###|\Z)'
        section_content = re.search(pattern, roadmap_content, re.DOTALL)
        if section_content:
            feature_count = len(re.findall(r'- \[ \]', section_content.group()))
            sections[section] = feature_count
    
    print("\n📊 Roadmap Summary Report")
    print("=" * 30)
    total_features = sum(sections.values())
    print(f"Total Features: {total_features}")
    print("-" * 30)
    
    for section, count in sections.items():
        if count > 0:
            print(f"{section:<25} {count:3d} features")
    
    print(f"\nReport generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    parser = argparse.ArgumentParser(description='Roadmap Management Helper')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add feature to roadmap
    add_parser = subparsers.add_parser('add', help='Add feature to roadmap')
    add_parser.add_argument('name', help='Feature name')
    add_parser.add_argument('description', help='Feature description')
    add_parser.add_argument('--section', default='Next Release', 
                          help='Roadmap section (default: Next Release)')
    
    # Move feature to changelog
    move_parser = subparsers.add_parser('complete', help='Move feature to changelog')
    move_parser.add_argument('name', help='Feature name')
    move_parser.add_argument('version', help='Version number (e.g., 1.1.0)')
    move_parser.add_argument('description', help='Feature description for changelog')
    
    # List features
    subparsers.add_parser('list', help='List all roadmap features')
    
    # Generate report
    subparsers.add_parser('report', help='Generate roadmap summary report')
    
    args = parser.parse_args()
    
    if args.command == 'add':
        add_to_roadmap(args.name, args.description, args.section)
    elif args.command == 'complete':
        move_to_changelog(args.name, args.version, args.description)
        remove_from_roadmap(args.name)
    elif args.command == 'list':
        list_roadmap_features()
    elif args.command == 'report':
        generate_roadmap_report()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()