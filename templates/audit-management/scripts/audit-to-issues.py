#!/usr/bin/env python3
"""
Audit to GitHub Issues converter for {{PROJECT_NAME}}
"""

def main():
    """Convert audit findings to GitHub issues."""
    print("gh issue create --title 'audit-finding'")
    print("--label audit-finding")

if __name__ == "__main__":
    main()
