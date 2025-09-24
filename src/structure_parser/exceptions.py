"""
Custom exceptions for the structure parser module.
"""


class StructureParserError(Exception):
    """Base exception for all structure parser errors."""
    pass


class ValidationError(StructureParserError):
    """Raised when structure validation fails."""
    
    def __init__(self, message: str, errors: list = None, line_number: int = None):
        super().__init__(message)
        self.errors = errors or []
        self.line_number = line_number
        
    def __str__(self):
        base_message = super().__str__()
        if self.line_number:
            base_message = f"Line {self.line_number}: {base_message}"
        if self.errors:
            error_details = "\n".join(f"  - {error}" for error in self.errors)
            base_message = f"{base_message}\nValidation errors:\n{error_details}"
        return base_message


class SchemaError(StructureParserError):
    """Raised when schema loading or validation fails."""
    pass


class FileNotFoundError(StructureParserError):
    """Raised when structure.json file is not found."""
    pass


class ParseError(StructureParserError):
    """Raised when JSON parsing fails."""
    
    def __init__(self, message: str, line_number: int = None, column: int = None):
        super().__init__(message)
        self.line_number = line_number
        self.column = column
        
    def __str__(self):
        base_message = super().__str__()
        if self.line_number and self.column:
            return f"Line {self.line_number}, Column {self.column}: {base_message}"
        elif self.line_number:
            return f"Line {self.line_number}: {base_message}"
        return base_message


class MigrationError(StructureParserError):
    """Raised when schema migration fails."""
    pass