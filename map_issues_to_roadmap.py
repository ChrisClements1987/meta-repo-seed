#!/usr/bin/env python3
"""
Roadmap Issue Mapper

This script maps GitHub issues to roadmap items by matching titles
and updates the ROADMAP.md file with issue references.

Usage:
    python map_issues_to_roadmap.py [--dry-run]
"""

import argparse
import re
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional

def get_github_issues() -> List[Dict]:
    """Get all GitHub issues using gh CLI"""
    try:
        result = subprocess.run(['gh', 'issue', 'list', '--state', 'open', '--json', 'number,title,labels'], 
                              capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to get GitHub issues: {e.stderr}")
        return []

def extract_feature_name_from_issue_title(title: str) -> str:
    """Extract the feature name from GitHub issue title"""
    # Remove [FEATURE] prefix and clean up
    if title.startswith('[FEATURE] '):
        return title[10:].strip()
    return title.strip()

def find_matching_issue(feature_name: str, issues: List[Dict]) -> Optional[Dict]:
    """Find GitHub issue that matches the roadmap feature name"""
    for issue in issues:
        issue_feature_name = extract_feature_name_from_issue_title(issue['title'])
        if issue_feature_name.lower() == feature_name.lower():
            return issue
    return None

def update_roadmap_with_issues(dry_run: bool = False) -> bool:
    """Update ROADMAP.md with GitHub issue references"""
    roadmap_path = Path("ROADMAP.md")
    if not roadmap_path.exists():
        print("❌ ROADMAP.md not found")
        return False
    
    # Get GitHub issues
    issues = get_github_issues()
    if not issues:
        print("❌ No GitHub issues found")
        return False
    
    print(f"📋 Found {len(issues)} GitHub issues")
    
    # Read roadmap content
    content = roadmap_path.read_text(encoding='utf-8')
    updated_content = content
    matches_found = 0
    
    # Find all feature items in the roadmap
    pattern = r'- \[ \] \*\*(.*?)\*\* - (.*?)(?=\n|$)'
    
    def replace_feature(match):
        nonlocal matches_found
        feature_name = match.group(1)
        description = match.group(2)
        
        # Find matching GitHub issue
        matching_issue = find_matching_issue(feature_name, issues)
        if matching_issue:
            issue_number = matching_issue['number']
            matches_found += 1
            # Replace with issue reference
            return f"- [ ] **{feature_name}** ([#{issue_number}](https://github.com/ChrisClements1987/meta-repo-seed/issues/{issue_number})) - {description}"
        else:
            # Keep original if no match found
            return match.group(0)
    
    # Apply replacements
    updated_content = re.sub(pattern, replace_feature, updated_content)
    
    if dry_run:
        print(f"\n🔍 DRY RUN - Would update {matches_found} roadmap items with issue references")
        print("Preview of changes:")
        print("-" * 50)
        
        # Show a few examples
        preview_pattern = r'- \[ \] \*\*(.*?)\*\* \(\[#(\d+)\].*?\) - (.*?)(?=\n|$)'
        preview_matches = re.findall(preview_pattern, updated_content)
        for i, (name, issue_num, desc) in enumerate(preview_matches[:3]):
            print(f"  {name} → Issue #{issue_num}")
        if len(preview_matches) > 3:
            print(f"  ... and {len(preview_matches) - 3} more")
        
        return True
    
    # Write updated content
    roadmap_path.write_text(updated_content, encoding='utf-8')
    print(f"✅ Updated {matches_found} roadmap items with GitHub issue references")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Map GitHub issues to roadmap items')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be updated without making changes')
    
    args = parser.parse_args()
    
    print("🗺️  Roadmap Issue Mapper")
    print("=" * 30)
    
    success = update_roadmap_with_issues(args.dry_run)
    
    if success and not args.dry_run:
        print("\n🎉 Roadmap successfully updated!")
        print("You can now:")
        print("  - Use issue numbers in branch names: git checkout -b feature/issue-5-config-support")
        print("  - Reference issues in commits: 'Fix #5: Add YAML configuration loading'")
        print("  - Track progress through GitHub issues")
    
    return 0 if success else 1

if __name__ == '__main__':
    exit(main())