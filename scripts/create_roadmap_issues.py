#!/usr/bin/env python3
"""
GitHub Issue Creator from Roadmap

This script automatically creates GitHub issues for roadmap items using the GitHub CLI.
It parses the ROADMAP.md file and creates properly formatted issues with labels and templates.

Requirements:
- GitHub CLI (gh) installed and authenticated
- Repository must be a GitHub repository

Usage:
    python create_roadmap_issues.py [--dry-run] [--section "High Priority"]
"""

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


def check_gh_cli():
    """Check if GitHub CLI is installed and authenticated"""
    try:
        result = subprocess.run(['gh', 'auth', 'status'], 
                              capture_output=True, text=True, check=True)
        print("✅ GitHub CLI is authenticated")
        return True
    except subprocess.CalledProcessError:
        print("❌ GitHub CLI is not authenticated. Run 'gh auth login' first.")
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI is not installed. Install it from https://cli.github.com/")
        return False

def parse_roadmap() -> List[Dict[str, str]]:
    """Parse ROADMAP.md and extract features with their sections"""
    roadmap_path = Path("ROADMAP.md")
    if not roadmap_path.exists():
        print("❌ ROADMAP.md not found")
        return []
    
    content = roadmap_path.read_text(encoding='utf-8')
    features = []
    current_section = None
    current_priority = None
    
    # Split content into lines
    lines = content.split('\n')
    
    for line in lines:
        # Detect main sections
        if line.startswith('## 🎯 Next Release'):
            current_section = "Next Release (v1.1.0)"
            current_priority = "high"
        elif line.startswith('## 🚀 Future Releases'):
            current_section = "Future Releases (v1.2.0+)"
            current_priority = "medium"
        elif line.startswith('### '):
            # Subsection within a release
            subsection = line.replace('### ', '').strip()
            if current_section:
                current_section = f"{current_section} - {subsection}"
        
        # Detect feature items
        if line.strip().startswith('- [ ] **') and current_section:
            # Extract feature name and description
            match = re.match(r'- \[ \] \*\*(.*?)\*\* - (.*)', line.strip())
            if match:
                name = match.group(1)
                description = match.group(2)
                
                features.append({
                    'name': name,
                    'description': description,
                    'section': current_section,
                    'priority': current_priority or 'medium'
                })
    
    return features

def create_issue_body(feature: Dict[str, str]) -> str:
    """Create a GitHub issue body from a feature"""
    body = f"""## 🎯 Feature Description
{feature['description']}

## 💡 Problem/Use Case
This feature has been identified as important for improving the Meta-Repo Seeding System's functionality and user experience.

## 🏗️ Proposed Solution
_To be defined during implementation planning._

## 📋 Acceptance Criteria
- [ ] Feature is implemented according to the description
- [ ] Tests are written for the new functionality
- [ ] Documentation is updated
- [ ] Feature works cross-platform (Windows, macOS, Linux)

## 🔧 Implementation Considerations
- Should maintain backward compatibility
- Follow existing code patterns and architecture
- Consider performance implications

## 📚 Related Items
- Roadmap Section: {feature['section']}
- Priority Level: {feature['priority']}

---
*This issue was automatically created from the roadmap using create_roadmap_issues.py*"""
    
    return body

def get_priority_label(priority: str) -> str:
    """Map priority to GitHub label"""
    priority_map = {
        'high': 'priority: high',
        'medium': 'priority: medium', 
        'low': 'priority: low'
    }
    return priority_map.get(priority, 'priority: medium')

def create_github_issue(feature: Dict[str, str], dry_run: bool = False) -> bool:
    """Create a GitHub issue using gh CLI"""
    title = f"[FEATURE] {feature['name']}"
    body = create_issue_body(feature)
    
    # Determine labels
    labels = [
        'enhancement',
        'roadmap',
        get_priority_label(feature['priority'])
    ]
    
    if dry_run:
        print(f"\n🔍 DRY RUN - Would create issue:")
        print(f"Title: {title}")
        print(f"Labels: {', '.join(labels)}")
        print(f"Body preview: {body[:200]}...")
        print("-" * 50)
        return True
    
    try:
        # Create the issue using gh CLI
        cmd = [
            'gh', 'issue', 'create',
            '--title', title,
            '--body', body,
            '--label', ','.join(labels)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issue_url = result.stdout.strip()
        print(f"✅ Created issue: {feature['name']}")
        print(f"   URL: {issue_url}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create issue for {feature['name']}")
        print(f"   Error: {e.stderr}")
        return False

def filter_features_by_section(features: List[Dict[str, str]], section_filter: str = None) -> List[Dict[str, str]]:
    """Filter features by section if specified"""
    if not section_filter:
        return features
    
    filtered = [f for f in features if section_filter.lower() in f['section'].lower()]
    return filtered

def main():
    parser = argparse.ArgumentParser(description='Create GitHub issues from roadmap items')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Show what would be created without actually creating issues')
    parser.add_argument('--section', type=str,
                       help='Only create issues for features in this section (partial match)')
    parser.add_argument('--priority', choices=['high', 'medium', 'low'],
                       help='Only create issues with this priority level')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of issues to create (useful for testing)')
    
    args = parser.parse_args()
    
    print("🚀 GitHub Issue Creator from Roadmap")
    print("=" * 40)
    
    # Check prerequisites
    if not args.dry_run and not check_gh_cli():
        return 1
    
    # Parse roadmap
    features = parse_roadmap()
    if not features:
        print("❌ No features found in ROADMAP.md")
        return 1
    
    print(f"📋 Found {len(features)} features in roadmap")
    
    # Apply filters
    if args.section:
        features = filter_features_by_section(features, args.section)
        print(f"🔍 Filtered to {len(features)} features matching section '{args.section}'")
    
    if args.priority:
        features = [f for f in features if f['priority'] == args.priority]
        print(f"🎯 Filtered to {len(features)} features with priority '{args.priority}'")
    
    if args.limit:
        features = features[:args.limit]
        print(f"⚡ Limited to first {len(features)} features")
    
    if not features:
        print("❌ No features match the specified filters")
        return 1
    
    # Show what will be processed
    print(f"\n📝 Will process {len(features)} features:")
    for i, feature in enumerate(features, 1):
        print(f"  {i:2d}. {feature['name']} [{feature['priority']}]")
    
    if not args.dry_run:
        confirm = input(f"\n❓ Create {len(features)} GitHub issues? (y/N): ")
        if confirm.lower() != 'y':
            print("⏹️  Operation cancelled")
            return 0
    
    # Create issues
    print(f"\n🏗️  {'[DRY RUN] ' if args.dry_run else ''}Creating issues...")
    print("-" * 50)
    
    success_count = 0
    for feature in features:
        if create_github_issue(feature, args.dry_run):
            success_count += 1
    
    print("-" * 50)
    print(f"✅ Successfully {'would create' if args.dry_run else 'created'} {success_count}/{len(features)} issues")
    
    if not args.dry_run and success_count > 0:
        print(f"\n🎉 All issues created! You can now create feature branches using:")
        print(f"   git checkout -b feature/issue-<number>-<feature-name>")
    
    return 0

if __name__ == '__main__':
    exit(main())