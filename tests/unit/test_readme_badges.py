"""
Test for README badge functionality demonstration.
This test demonstrates the TDD approach required by our PR templates.
"""

import pytest
from pathlib import Path


def test_readme_contains_build_status_badge():
    """
    Test that README.md contains a build status badge for CI/CD visibility.
    
    This follows TDD - test written FIRST before implementation.
    Expected to fail initially (RED phase of TDD).
    """
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    assert readme_path.exists(), "README.md should exist"
    
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Check for CI/CD status badge
    assert "![CI Status]" in readme_content, "README should contain CI status badge"
    assert "github.com" in readme_content, "Badge should link to GitHub Actions"


def test_readme_contains_test_coverage_badge():
    """
    Test that README.md contains a test coverage badge for quality visibility.
    
    This follows TDD - test written FIRST before implementation.
    Expected to fail initially (RED phase of TDD).
    """
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Check for test coverage badge
    assert "![Coverage]" in readme_content, "README should contain coverage badge"
    assert "codecov" in readme_content or "coveralls" in readme_content, "Badge should link to coverage service"


def test_readme_has_proper_status_section():
    """
    Test that README.md has a proper project status section.
    
    This follows TDD - test written FIRST before implementation.
    Expected to fail initially (RED phase of TDD).
    """
    readme_path = Path(__file__).parent.parent.parent / "README.md"
    readme_content = readme_path.read_text(encoding='utf-8')
    
    # Check for status section with badges
    assert "## 🚀 Status" in readme_content or "## Status" in readme_content, "README should have status section"