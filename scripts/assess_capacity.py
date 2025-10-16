#!/usr/bin/env python3
"""
Daily Capacity Assessment Tool

This tool helps assess daily capacity and recommends work items to pull
from the Kanban board based on available time and current priorities.
"""

import sys
from datetime import datetime
from pathlib import Path


def assess_capacity():
    """Assess daily capacity and recommend work items."""
    print("🎯 Daily Capacity Assessment")
    print("=" * 50)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()

    # Capacity levels
    capacity_levels = {
        "high": {
            "time": "2+ hours",
            "description": "Full development session",
            "recommendations": [
                "Customer onboarding workflow (2 hours)",
                "Security testing setup (1 hour)",
                "Process monitoring dashboard (1.5 hours)",
            ],
        },
        "medium": {
            "time": "1-2 hours",
            "description": "Partial development session",
            "recommendations": [
                "Add API endpoint tests (45 min)",
                "Fix OrganizationSeeder error (30 min)",
                "Documentation automation (1 hour)",
            ],
        },
        "low": {
            "time": "30-60 minutes",
            "description": "Quick tasks and maintenance",
            "recommendations": [
                "Update README (15 min)",
                "Fix minor linting issues (30 min)",
                "Review technical debt items (45 min)",
            ],
        },
        "minimal": {
            "time": "< 30 minutes",
            "description": "Review and planning only",
            "recommendations": [
                "Review Kanban board (10 min)",
                "Plan tomorrow's work (15 min)",
                "Update documentation (20 min)",
            ],
        },
    }

    print("📊 Capacity Levels:")
    for level, info in capacity_levels.items():
        print(f"  {level.upper()}: {info['time']} - {info['description']}")

    print()
    print("🎯 Quick Pull Recommendations:")
    print()

    # High priority items (always show)
    print("🔴 HIGH PRIORITY (Priority Score: 8+)")
    print("  • Fix OrganizationSeeder NoneType error (30 min) - Score: 9")
    print("  • Add API endpoint tests (45 min) - Score: 8")
    print()

    print("🟡 MEDIUM PRIORITY (Priority Score: 5-7)")
    print("  • Customer onboarding workflow (2 hours) - Score: 7")
    print("  • Security testing setup (1 hour) - Score: 6")
    print("  • Process monitoring dashboard (1.5 hours) - Score: 5")
    print()

    print("⚠️  TECHNICAL DEBT (Priority Score: 4-6)")
    print("  • Re-enable and fix flake8 linting (2-3 hours) - Score: 6")
    print("    - Fix 200+ linting issues across codebase")
    print("    - Re-enable flake8 in pre-commit hooks")
    print()

    # Capacity-based recommendations
    print("📋 CAPACITY-BASED RECOMMENDATIONS:")
    print()

    for level, info in capacity_levels.items():
        print(f"🟡 {level.upper()} CAPACITY:")
        for rec in info["recommendations"]:
            print(f"  • {rec}")
        print()

    print("💡 TIPS:")
    print("  • Pull items that match your available time")
    print("  • Prioritize high-impact, low-effort items")
    print("  • Maintain WIP limit of 2 items maximum")
    print("  • Update Kanban board after completing items")
    print()

    print("📋 NEXT STEPS:")
    print("  1. Assess your actual capacity")
    print("  2. Pull appropriate items from backlog")
    print("  3. Update Kanban board status")
    print("  4. Focus on completing pulled items")
    print()

    print("🔗 RESOURCES:")
    print("  • Unified Kanban Board: UNIFIED_KANBAN_BOARD.md")
    print("  • ODR Framework: docs/operations/odr/001-unified-kanban-workflow.md")
    print("  • Work Item Template: docs/operations/work-item-template.md")
    print("  • TDD Guide: docs/development/tdd-workflow.md")
    print("  • Git Standards: docs/development/git-workflow.md")


def show_kanban_status():
    """Show current Kanban board status."""
    print("📋 Current Kanban Status")
    print("=" * 30)
    print()

    print("🟡 IN PROGRESS (WIP: 1/2)")
    print("  • Process hardening implementation")
    print()

    print("✅ RECENTLY COMPLETED")
    print("  • Comprehensive test suite (21 tests)")
    print("  • Documentation structure update")
    print("  • Process improvement recommendations")
    print()

    print("🔴 READY TO PULL")
    print("  • Install pre-commit hooks (15 min)")
    print("  • Fix OrganizationSeeder error (30 min)")
    print("  • Add API endpoint tests (45 min)")
    print()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_kanban_status()
    else:
        assess_capacity()
