"""
Repository Automation Module

This module provides automation tools for repository initialization, 
structure enforcement, and maintenance tasks.
"""

__version__ = "1.0.0"
__author__ = "Meta-Repo Seed Team"

# Import main automation classes for easy access
try:
    from .repository_initializer import RepositoryInitializer
    __all__ = ['RepositoryInitializer']
except ImportError:
    # Handle case where modules aren't available yet
    __all__ = []