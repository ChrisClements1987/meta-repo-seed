"""
Unit tests for template processing functionality.

Tests template file processing, variable replacement, and file creation.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile
import os

# Import the module we're testing
import sys
sys.path.append(str(Path(__file__).parent.parent))
from seeding import create_file_from_template, process_template_content


class TestTemplateContentProcessing:
    """Test cases for template content processing."""
    
    def test_simple_variable_replacement(self, sample_replacements):
        """Test basic template variable replacement."""
        template_content = "Project: {{PROJECT_NAME}}, User: {{GITHUB_USERNAME}}"
        
        result = process_template_content(template_content, sample_replacements)
        
        assert result == "Project: test-project, User: test-user"
    
    def test_multiple_same_variable_replacement(self, sample_replacements):
        """Test replacement of the same variable multiple times."""
        template_content = "{{PROJECT_NAME}} is a great project. {{PROJECT_NAME}} rules!"
        
        result = process_template_content(template_content, sample_replacements)
        
        assert result == "test-project is a great project. test-project rules!"
    
    def test_all_standard_variables_replacement(self, sample_replacements):
        """Test replacement of all standard template variables."""
        template_content = """
Project: {{PROJECT_NAME}}
User: {{GITHUB_USERNAME}}
Date: {{CURRENT_DATE}}
Decision: {{DECISION_NUMBER}} - {{DECISION_TITLE}}
Status: {{STATUS}}
Alternative: {{ALTERNATIVE_NAME}}
"""
        
        result = process_template_content(template_content, sample_replacements)
        
        assert "Project: test-project" in result
        assert "User: test-user" in result
        assert "Date: 2025-09-24" in result
        assert "Decision: 001 - Test Decision" in result
        assert "Status: Accepted" in result
        assert "Alternative: Test Alternative" in result
    
    def test_missing_variable_unchanged(self, sample_replacements):
        """Test that missing variables are left unchanged."""
        template_content = "{{PROJECT_NAME}} has {{MISSING_VARIABLE}}"
        
        result = process_template_content(template_content, sample_replacements)
        
        assert result == "test-project has {{MISSING_VARIABLE}}"
    
    def test_empty_template_content(self, sample_replacements):
        """Test processing empty template content."""
        result = process_template_content("", sample_replacements)
        
        assert result == ""
    
    def test_no_variables_in_template(self, sample_replacements):
        """Test processing template with no variables."""
        template_content = "This is just plain text without any variables."
        
        result = process_template_content(template_content, sample_replacements)
        
        assert result == template_content
    
    def test_malformed_variable_syntax(self, sample_replacements):
        """Test handling of malformed variable syntax."""
        template_content = "{{PROJECT_NAME}} and {MISSING_BRACE and {{INCOMPLETE"
        
        result = process_template_content(template_content, sample_replacements)
        
        # Should replace valid variables and leave malformed ones unchanged
        assert "test-project" in result
        assert "{MISSING_BRACE" in result
        assert "{{INCOMPLETE" in result
    
    def test_nested_braces(self, sample_replacements):
        """Test handling of nested or adjacent braces."""
        template_content = "{{{PROJECT_NAME}}} and {{{{PROJECT_NAME}}}}"
        
        result = process_template_content(template_content, sample_replacements)
        
        # Should handle nested braces appropriately
        assert "test-project" in result
    
    def test_case_sensitive_variables(self, sample_replacements):
        """Test that variable names are case-sensitive."""
        template_content = "{{project_name}} vs {{PROJECT_NAME}}"
        
        result = process_template_content(template_content, sample_replacements)
        
        # Only PROJECT_NAME should be replaced
        assert result == "{{project_name}} vs test-project"
    
    def test_special_characters_in_replacement_values(self):
        """Test replacement values containing special characters."""
        replacements = {
            'PROJECT_NAME': 'test-project!@#$%^&*()',
            'GITHUB_USERNAME': 'user_with-special.chars',
            'DESCRIPTION': 'Contains "quotes" and \'apostrophes\' and \n newlines'
        }
        
        template_content = """
Name: {{PROJECT_NAME}}
User: {{GITHUB_USERNAME}}
Desc: {{DESCRIPTION}}
"""
        
        result = process_template_content(template_content, replacements)
        
        assert 'test-project!@#$%^&*()' in result
        assert 'user_with-special.chars' in result
        assert 'Contains "quotes"' in result
    
    def test_unicode_characters_in_template(self, sample_replacements):
        """Test processing template with Unicode characters."""
        template_content = "Проект: {{PROJECT_NAME}} 🚀 用户: {{GITHUB_USERNAME}} ñoño"
        
        result = process_template_content(template_content, sample_replacements)
        
        assert "Проект: test-project" in result
        assert "用户: test-user" in result
        assert "🚀" in result
        assert "ñoño" in result


class TestFileTemplateCreation:
    """Test cases for creating files from templates."""
    
    def test_create_file_from_template_success(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test successful file creation from template."""
        # Create a test template
        template_file = mock_templates_dir / "test.template"
        template_content = "Project: {{PROJECT_NAME}}\nUser: {{GITHUB_USERNAME}}"
        template_file.write_text(template_content)
        
        # Create output file
        output_file = temp_dir / "output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "Project: test-project" in content
        assert "User: test-user" in content
    
    def test_create_file_creates_parent_directories(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test that create_file_from_template creates parent directories."""
        # Create template
        template_file = mock_templates_dir / "nested.template"
        template_file.write_text("Content: {{PROJECT_NAME}}")
        
        # Output file in nested directory
        output_file = temp_dir / "level1" / "level2" / "output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        assert output_file.parent.exists()
        
        content = output_file.read_text()
        assert "Content: test-project" in content
    
    def test_create_file_nonexistent_template(self, temp_dir, sample_replacements):
        """Test handling of non-existent template file."""
        template_file = temp_dir / "nonexistent.template"
        output_file = temp_dir / "output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is False
        assert not output_file.exists()
    
    def test_create_file_empty_template(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test creating file from empty template."""
        template_file = mock_templates_dir / "empty.template"
        template_file.write_text("")
        
        output_file = temp_dir / "empty_output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        assert output_file.read_text() == ""
    
    def test_create_file_with_binary_content(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test handling of template files with binary content."""
        template_file = mock_templates_dir / "binary.template"
        # Write binary content that might cause encoding issues
        template_file.write_bytes(b'\x00\x01\x02{{PROJECT_NAME}}\xff\xfe')
        
        output_file = temp_dir / "binary_output.txt"
        
        # This should handle encoding errors gracefully
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        # Behavior depends on implementation - might succeed with error handling
        # or fail gracefully
        assert isinstance(result, bool)
    
    def test_create_file_permission_error(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test handling of permission errors during file creation."""
        template_file = mock_templates_dir / "permission.template"
        template_file.write_text("Content: {{PROJECT_NAME}}")
        
        output_file = temp_dir / "readonly_output.txt"
        
        with patch('builtins.open', side_effect=PermissionError("Access denied")):
            result = create_file_from_template(template_file, output_file, sample_replacements)
            
            assert result is False
    
    def test_create_file_overwrite_existing(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test behavior with existing file (should not overwrite)."""
        # Create template
        template_file = mock_templates_dir / "overwrite.template"
        template_file.write_text("New content: {{PROJECT_NAME}}")
        
        # Create existing output file
        output_file = temp_dir / "existing.txt"
        output_file.write_text("Old content")
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        # Should return False because file already exists
        assert result is False
        assert output_file.exists()
        
        # Content should remain unchanged
        content = output_file.read_text()
        assert "Old content" in content
        assert "New content: test-project" not in content
    
    def test_create_file_large_template(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test processing large template file."""
        # Create large template content
        template_content = "\n".join([
            f"Line {i}: {{{{PROJECT_NAME}}}} - {{{{GITHUB_USERNAME}}}}"
            for i in range(1000)
        ])
        
        template_file = mock_templates_dir / "large.template"
        template_file.write_text(template_content)
        
        output_file = temp_dir / "large_output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "Line 0: test-project - test-user" in content
        assert "Line 999: test-project - test-user" in content
        
        # Verify all lines were processed
        lines = content.split('\n')
        assert len(lines) == 1000


class TestTemplateFileHandling:
    """Test cases for template file system operations."""
    
    def test_template_file_encoding_handling(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test handling of different file encodings."""
        # Test UTF-8 encoding
        template_file = mock_templates_dir / "utf8.template"
        utf8_content = "Проект: {{PROJECT_NAME}} 🚀 用户: {{GITHUB_USERNAME}}"
        template_file.write_text(utf8_content, encoding='utf-8')
        
        output_file = temp_dir / "utf8_output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        
        content = output_file.read_text(encoding='utf-8')
        assert "Проект: test-project" in content
        assert "🚀" in content
    
    def test_template_file_with_different_line_endings(self, temp_dir, mock_templates_dir, sample_replacements):
        """Test handling of different line ending styles."""
        # Create template with mixed line endings
        template_content = "Line 1: {{PROJECT_NAME}}\r\nLine 2: {{GITHUB_USERNAME}}\nLine 3: End"
        
        template_file = mock_templates_dir / "line_endings.template"
        template_file.write_text(template_content)
        
        output_file = temp_dir / "line_endings_output.txt"
        
        result = create_file_from_template(template_file, output_file, sample_replacements)
        
        assert result is True
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "Line 1: test-project" in content
        assert "Line 2: test-user" in content
        assert "Line 3: End" in content


class TestTemplateErrorHandling:
    """Test cases for error handling in template processing."""
    
    def test_invalid_replacement_dict(self):
        """Test handling of invalid replacement dictionary."""
        template_content = "{{PROJECT_NAME}}"
        
        # Test with None
        result1 = process_template_content(template_content, None)
        # Should handle gracefully or raise appropriate error
        assert isinstance(result1, str)
        
        # Test with invalid types
        with pytest.raises((TypeError, AttributeError)):
            process_template_content(template_content, "not a dict")
    
    def test_template_with_recursive_replacements(self):
        """Test handling of potentially recursive replacements."""
        replacements = {
            'PROJECT_NAME': '{{GITHUB_USERNAME}}',
            'GITHUB_USERNAME': '{{PROJECT_NAME}}'
        }
        
        template_content = "{{PROJECT_NAME}}"
        
        result = process_template_content(template_content, replacements)
        
        # Should not cause infinite recursion
        # Result depends on implementation - might be partial replacement
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_template_with_extremely_long_variable_names(self, sample_replacements):
        """Test handling of very long variable names."""
        long_var_name = "VERY_" * 100 + "LONG_VARIABLE_NAME"
        template_content = f"{{{{{long_var_name}}}}}"
        
        result = process_template_content(template_content, sample_replacements)
        
        # Should handle long variable names without issues
        assert result == template_content  # Should remain unchanged
    
    def test_template_with_many_variables(self):
        """Test processing template with many different variables."""
        # Create many replacement variables
        replacements = {f'VAR_{i}': f'value_{i}' for i in range(100)}
        
        # Create template using all variables
        template_content = " ".join([f"{{{{VAR_{i}}}}}" for i in range(100)])
        
        result = process_template_content(template_content, replacements)
        
        # Should replace all variables correctly
        for i in range(100):
            assert f'value_{i}' in result
    
    def test_memory_efficiency_large_replacements(self):
        """Test memory efficiency with large replacement dictionaries."""
        # Create large replacement dictionary
        replacements = {f'VAR_{i}': f'value_{i}' * 100 for i in range(1000)}
        
        template_content = "{{VAR_0}} {{VAR_500}} {{VAR_999}}"
        
        result = process_template_content(template_content, replacements)
        
        # Should handle large dictionaries without memory issues
        assert 'value_0' * 100 in result
        assert 'value_500' * 100 in result
        assert 'value_999' * 100 in result


class TestTemplateIntegrationWithRepoSeeder:
    """Test cases for template integration with RepoSeeder functionality."""
    
    def test_template_directory_discovery(self, temp_dir):
        """Test template directory discovery and usage."""
        from seeding import RepoSeeder
        
        # Create templates directory structure
        templates_dir = temp_dir / "templates"
        templates_dir.mkdir()
        
        (templates_dir / "gitignore.template").write_text("# {{PROJECT_NAME}}\n*.log")
        (templates_dir / "readme.template").write_text("# {{PROJECT_NAME}}\n\nBy {{GITHUB_USERNAME}}")
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("template-project", "template-user", dry_run=True)
            seeder.templates_dir = templates_dir
            
            # Test that seeder can find and process templates
            assert seeder.templates_dir.exists()
            assert (seeder.templates_dir / "gitignore.template").exists()
            assert (seeder.templates_dir / "readme.template").exists()
    
    def test_template_processing_with_seeder_replacements(self, temp_dir, mock_templates_dir):
        """Test template processing using RepoSeeder's replacement dictionary."""
        from seeding import RepoSeeder
        
        # Create template
        template_file = mock_templates_dir / "integration.template"
        template_content = """
Project: {{PROJECT_NAME}}
User: {{GITHUB_USERNAME}}
Date: {{CURRENT_DATE}}
"""
        template_file.write_text(template_content)
        
        # Create seeder and get its replacements
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("integration-project", "integration-user", dry_run=True)
            
            output_file = temp_dir / "integration_output.txt"
            result = create_file_from_template(template_file, output_file, seeder.replacements)
            
            assert result is True
            assert output_file.exists()
            
            content = output_file.read_text()
            assert "Project: integration-project" in content
            assert "User: integration-user" in content
            # Should have current date from seeder's replacements
            assert "Date:" in content