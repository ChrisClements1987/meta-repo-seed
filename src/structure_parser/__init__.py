"""
Structure Parser Module

This module provides parsing and validation capabilities for structure.json files
used in the meta-repo seeding system.

Based on the architecture analysis in docs/architecture/structure-parser-interface.md
"""

from .parser import StructureParser
from .models import StructureData, ValidationResult
from .exceptions import (
    StructureParserError,
    ValidationError,
    SchemaError,
    FileNotFoundError as StructureFileNotFoundError,
    ParseError,
    MigrationError
)

__version__ = "1.0.0"
__all__ = [
    "StructureParser",
    "StructureData", 
    "ValidationResult",
    "StructureParserError",
    "ValidationError",
    "SchemaError",
    "StructureFileNotFoundError",
    "ParseError",
    "MigrationError"
]