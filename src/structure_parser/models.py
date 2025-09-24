"""
Data models for the structure parser.

These models represent the parsed structure data and validation results.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime


@dataclass
class StructureData:
    """Represents parsed structure.json data with typed access."""
    
    # Metadata fields (extracted from metadata object)
    project_name: str
    github_username: str
    created_date: str
    version: str
    schema_version: str
    structure: Dict[str, Any]
    
    # Optional metadata
    description: Optional[str] = None
    updated_date: Optional[str] = None
    template_path: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StructureData":
        """Create StructureData from parsed JSON data."""
        if "metadata" in data:
            # V2 format with nested metadata
            metadata = data["metadata"]
            return cls(
                project_name=metadata.get("project_name", ""),
                github_username=metadata.get("github_username", ""),
                created_date=metadata.get("created_date", ""),
                version=metadata.get("version", ""),
                schema_version=metadata.get("schema_version", "2.0.0"),
                structure=data.get("structure", {}),
                description=metadata.get("description"),
                updated_date=metadata.get("updated_date"),
                template_path=metadata.get("template_path"),
                tags=metadata.get("tags", [])
            )
        else:
            # V1 format with fields at root level
            return cls(
                project_name=data.get("project_name", ""),
                github_username=data.get("github_username", ""),
                created_date=data.get("created_date", ""),
                version=data.get("version", ""),
                schema_version="1.0",  # V1 format
                structure=data.get("structure", {}),
                description=data.get("description"),
                updated_date=data.get("updated_date"),
                template_path=data.get("template_path"),
                tags=data.get("tags", [])
            )
    
    def get_top_level_directories(self) -> List[str]:
        """Get list of top-level directory names."""
        return list(self.structure.keys())
    
    def get_directory_files(self, directory_path: str) -> List[str]:
        """Get list of files for a specific directory path."""
        parts = directory_path.split('/')
        current = self.structure
        
        for part in parts:
            if part in current:
                current = current[part]
            else:
                return []
        
        # If we find a list, return it; otherwise return empty list
        if isinstance(current, list):
            return current
        elif isinstance(current, dict):
            # Return all keys that map to lists (files)
            files = []
            for key, value in current.items():
                if isinstance(value, list):
                    files.extend(value)
            return files
        
        return []
    
    def has_directory(self, directory_path: str) -> bool:
        """Check if a directory path exists in the structure."""
        parts = directory_path.split('/')
        current = self.structure
        
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return False
        
        return True
    
    def get_all_directories(self) -> List[str]:
        """Get all directory paths in the structure."""
        directories = []
        
        def collect_directories(obj: Dict[str, Any], path: str = ""):
            for key, value in obj.items():
                current_path = f"{path}/{key}" if path else key
                directories.append(current_path)
                
                if isinstance(value, dict):
                    collect_directories(value, current_path)
        
        collect_directories(self.structure)
        return directories
    
    def get_all_files(self) -> Dict[str, List[str]]:
        """Get all files organized by directory path."""
        files_by_dir = {}
        
        def collect_files(obj: Dict[str, Any], path: str = ""):
            for key, value in obj.items():
                current_path = f"{path}/{key}" if path else key
                
                if isinstance(value, list):
                    files_by_dir[current_path] = value
                elif isinstance(value, dict):
                    collect_files(value, current_path)
        
        collect_files(self.structure)
        return files_by_dir


@dataclass
class ValidationError:
    """Represents a single validation error."""
    
    message: str
    path: str
    error_code: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    
    def __str__(self):
        location = f" at {self.path}" if self.path else ""
        line_info = f" (line {self.line_number})" if self.line_number else ""
        return f"{self.error_code}: {self.message}{location}{line_info}"


@dataclass
class ValidationResult:
    """Result of structure validation."""
    
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    schema_version: Optional[str] = None
    
    @property
    def error_count(self) -> int:
        """Number of validation errors."""
        return len(self.errors)
    
    @property
    def warning_count(self) -> int:
        """Number of validation warnings."""
        return len(self.warnings)
    
    @property
    def has_errors(self) -> bool:
        """True if there are validation errors."""
        return len(self.errors) > 0
    
    @property
    def has_warnings(self) -> bool:
        """True if there are validation warnings."""
        return len(self.warnings) > 0
    
    def add_error(self, message: str, path: str = "", error_code: str = "VALIDATION_ERROR", 
                  line_number: int = None):
        """Add a validation error."""
        error = ValidationError(
            message=message,
            path=path,
            error_code=error_code,
            line_number=line_number
        )
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, message: str, path: str = "", error_code: str = "VALIDATION_WARNING",
                    line_number: int = None):
        """Add a validation warning."""
        warning = ValidationError(
            message=message,
            path=path,
            error_code=error_code,
            line_number=line_number
        )
        self.warnings.append(warning)
    
    def get_summary(self) -> str:
        """Get a summary of validation results."""
        if self.is_valid:
            if self.warning_count > 0:
                return f"Valid with {self.warning_count} warning(s)"
            return "Valid"
        else:
            return f"Invalid: {self.error_count} error(s), {self.warning_count} warning(s)"
    
    def get_detailed_report(self) -> str:
        """Get a detailed validation report."""
        lines = [f"Validation Result: {self.get_summary()}"]
        
        if self.schema_version:
            lines.append(f"Schema Version: {self.schema_version}")
        
        if self.errors:
            lines.append("\nErrors:")
            for error in self.errors:
                lines.append(f"  {error}")
        
        if self.warnings:
            lines.append("\nWarnings:")
            for warning in self.warnings:
                lines.append(f"  {warning}")
        
        return "\n".join(lines)