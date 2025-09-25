"""
Meta-Repo-Seed Package

A comprehensive toolkit for managing and synchronizing repository structures,
templates, and configurations across multiple projects.

This package provides:
- Structure synchronization scripts (Issue #33)
- Template management and variable substitution
- Configuration file parsing and validation
- Command-line tools for repository management

Author: ChrisClements1987
"""

__version__ = "1.0.0"
__author__ = "ChrisClements1987"

# Import main components for easy access
try:
    from .structure_sync import (
        StructureSynchronizer,
        DirectoryStructure, 
        FileTemplate
    )
    __all__ = [
        'StructureSynchronizer',
        'DirectoryStructure',
        'FileTemplate'
    ]
except ImportError:
    # Allow package to be imported even if dependencies aren't installed
    __all__ = []