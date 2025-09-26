"""
Structure Parser Module

This module provides parsing and validation capabilities for structure.json files
used in the meta-repo seeding system.

Based on the architecture analysis in docs/architecture/structure-parser-interface.md
"""

from .exceptions import FileNotFoundError as StructureFileNotFoundError
from .exceptions import (MigrationError, ParseError, SchemaError,
                         StructureParserError, ValidationError)
from .models import StructureData, ValidationResult
from .parser import StructureParser

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