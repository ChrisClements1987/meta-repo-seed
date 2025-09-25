# Structure Synchronization Scripts

## Overview

The Structure Synchronization Scripts provide a powerful way to maintain consistency across multiple repositories by defining, managing, and applying directory structures and file templates. This system addresses Issue #33 by implementing automated structure synchronization functionality.

## Features

- **Structure Scanning**: Analyze existing directories to create reusable structure templates
- **Template Management**: Save, load, and manage structure definitions
- **Synchronization**: Apply structure templates to new or existing directories
- **Template Variables**: Support for parameterized templates with variable substitution
- **Comparison**: Compare structures to identify differences
- **Configuration**: Flexible configuration system with YAML support
- **Backup**: Automatic backup creation before synchronization
- **CLI Interface**: Command-line tool for easy usage

## Installation

The structure synchronization functionality is part of the meta-repo-seed package:

```bash
pip install -e .
```

## Quick Start

### 1. Scan an existing directory to create a template

```bash
python sync_structures.py scan --source ./my_project --structure python_template
```

### 2. Apply a template to create a new project

```bash
python sync_structures.py sync --structure python_template --target ./new_project --vars '{"project_name": "MyApp", "author_name": "John Doe"}'
```

### 3. List available templates

```bash
python sync_structures.py list
```

## Configuration

The system uses a YAML configuration file (`sync_config.yaml`) to control behavior:

```yaml
templates_dir: templates
output_dir: output
sync_rules:
  preserve_existing: true
  backup_before_sync: true
  exclude_patterns:
    - .git
    - __pycache__
    - "*.pyc"

template_variables:
  common:
    project_name: "{project_name}"
    author_name: "{author_name}"
    author_email: "{author_email}"
    description: "{description}"
    version: "1.0.0"
```

## Command-Line Interface

### Scan Command

Create a structure template from an existing directory:

```bash
python sync_structures.py scan --source <directory> [--structure <name>] [--config <config_file>]
```

**Options:**
- `--source`: Directory to scan (required)
- `--structure`: Name for the template (default: directory name)
- `--config`: Configuration file path

**Example:**
```bash
python sync_structures.py scan --source ./my_python_project --structure python_base
```

### Sync Command

Apply a structure template to a target directory:

```bash
python sync_structures.py sync --structure <template> --target <directory> [--vars <json>] [--interactive]
```

**Options:**
- `--structure`: Template name (required)
- `--target`: Target directory (required)
- `--vars`: Template variables in JSON format
- `--interactive`: Interactively collect template variables
- `--config`: Configuration file path

**Examples:**
```bash
# Basic sync
python sync_structures.py sync --structure python_base --target ./new_project

# With template variables
python sync_structures.py sync --structure python_base --target ./new_project --vars '{"project_name": "MyApp", "author_name": "John Doe"}'

# Interactive mode
python sync_structures.py sync --structure python_base --target ./new_project --interactive
```

### List Command

List available structure templates:

```bash
python sync_structures.py list [--config <config_file>]
```

**Example:**
```bash
python sync_structures.py list
# Output:
# Available structure templates:
#   • python_project
#     Files: 8, Subdirs: 3
#     Created: 2025-09-25T10:30:00
```

### Compare Command

Compare two structure templates or a template with a directory:

```bash
python sync_structures.py compare --structure1 <template1> [--structure2 <template2>] [--source <directory>]
```

**Options:**
- `--structure1`: First template (required)
- `--structure2`: Second template
- `--source`: Directory to compare with (alternative to --structure2)

**Examples:**
```bash
# Compare two templates
python sync_structures.py compare --structure1 old_template --structure2 new_template

# Compare template with directory
python sync_structures.py compare --structure1 python_base --source ./existing_project
```

## Python API

### Basic Usage

```python
from meta_repo_seed.structure_sync import StructureSynchronizer

# Initialize synchronizer
sync = StructureSynchronizer('sync_config.yaml')

# Scan a directory
structure = sync.scan_structure('./my_project')

# Save the structure as a template
sync.save_structure(structure, 'my_template')

# Load a template
template = sync.load_structure('my_template')

# Sync to a new directory
sync.sync_structure(template, './new_project', {
    'project_name': 'MyNewProject',
    'author_name': 'John Doe',
    'author_email': 'john@example.com'
})
```

### Advanced Usage

```python
# Compare structures
differences = sync.compare_structures(template1, template2)
print(f"Files added: {differences['files_added']}")
print(f"Files removed: {differences['files_removed']}")

# List available templates
templates = sync.list_structures()
for template_name in templates:
    print(f"Template: {template_name}")
```

## Structure Templates

Structure templates are JSON files that define:

- **Directory hierarchy**: Nested folder structure
- **File templates**: File content with template variables
- **Metadata**: Information about the template
- **Template variables**: Parameterized values

### Template Format

```json
{
  "name": "python_project",
  "path": "python_project",
  "subdirs": [
    {
      "name": "src",
      "path": "src",
      "subdirs": [...],
      "files": [...],
      "metadata": {}
    }
  ],
  "files": [
    {
      "path": "README.md",
      "content": "# {project_name}\n\n{description}\n",
      "template_vars": {
        "project_name": "",
        "description": ""
      },
      "checksum": "abc123",
      "last_updated": "2025-09-25T10:30:00"
    }
  ],
  "metadata": {
    "template_version": "1.0.0",
    "description": "Standard Python project structure"
  }
}
```

## Template Variables

Templates support variable substitution using `{variable_name}` syntax:

### Common Variables

- `{project_name}`: Name of the project
- `{author_name}`: Author's name
- `{author_email}`: Author's email
- `{description}`: Project description
- `{version}`: Version number

### Using Variables

When syncing, provide variables in JSON format:

```bash
python sync_structures.py sync --structure python_base --target ./new_project --vars '{
  "project_name": "MyAwesomeProject",
  "author_name": "Jane Developer",
  "author_email": "jane@dev.com",
  "description": "An awesome Python project",
  "version": "1.0.0"
}'
```

## Synchronization Rules

The system supports various synchronization rules:

### Preserve Existing Files

When `preserve_existing` is true, existing files won't be overwritten:

```yaml
sync_rules:
  preserve_existing: true
```

### Backup Before Sync

Create backups before synchronization:

```yaml
sync_rules:
  backup_before_sync: true
```

### Exclusion Patterns

Exclude files and directories from scanning/syncing:

```yaml
sync_rules:
  exclude_patterns:
    - .git
    - __pycache__
    - "*.pyc"
    - node_modules
    - .env
```

## Built-in Templates

The system comes with several built-in templates:

### Python Project Template

A complete Python project structure with:
- Source package layout (`src/` directory)
- Test directory with basic test files
- Documentation structure
- Setup files (`setup.py`, `pyproject.toml`)
- Development configuration files
- Git ignore file

**Usage:**
```bash
python sync_structures.py sync --structure python_project --target ./my_new_project --vars '{
  "project_name": "my_package",
  "author_name": "Your Name",
  "author_email": "your@email.com",
  "description": "A new Python package"
}'
```

## Error Handling

The system provides comprehensive error handling:

- **File not found**: Clear messages when templates or directories don't exist
- **Permission errors**: Handled gracefully with informative messages
- **JSON parsing**: Validation of template files and variable inputs
- **Encoding issues**: Proper handling of different file encodings

## Logging

Logging is configured to provide useful information:

```python
import logging
logging.basicConfig(level=logging.INFO)

# Logs will show:
# INFO - Scanning structure: /path/to/source
# INFO - Structure saved to: templates/my_template.json
# INFO - Syncing structure to: /path/to/target
```

## Best Practices

1. **Use descriptive template names**: Choose clear, meaningful names for your templates
2. **Keep templates focused**: Create specific templates for different project types
3. **Version your templates**: Include version information in template metadata
4. **Test templates**: Always test new templates before using in production
5. **Backup important data**: Enable backup_before_sync for important projects
6. **Use exclusion patterns**: Exclude unnecessary files from templates
7. **Document variables**: Clearly document what template variables do

## Examples

### Creating a Web Project Template

```bash
# Scan an existing web project
python sync_structures.py scan --source ./my_web_app --structure web_project

# Use the template
python sync_structures.py sync --structure web_project --target ./new_web_app --vars '{
  "project_name": "MyWebApp",
  "author_name": "Web Developer"
}'
```

### Updating Project Structures

```bash
# Compare current project with template
python sync_structures.py compare --structure1 python_project --source ./existing_project

# Apply updates (with backup)
python sync_structures.py sync --structure python_project --target ./existing_project
```

### Batch Operations

```python
from meta_repo_seed.structure_sync import StructureSynchronizer

sync = StructureSynchronizer()
template = sync.load_structure('python_project')

# Create multiple projects
projects = [
    {'name': 'project1', 'author': 'Alice'},
    {'name': 'project2', 'author': 'Bob'},
    {'name': 'project3', 'author': 'Carol'}
]

for project in projects:
    sync.sync_structure(
        template,
        f"./{project['name']}",
        {
            'project_name': project['name'],
            'author_name': project['author'],
            'author_email': f"{project['author'].lower()}@company.com"
        }
    )
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure the package is installed with `pip install -e .`
2. **Template not found**: Check that templates are in the correct directory
3. **Permission denied**: Ensure write permissions for target directories
4. **Encoding issues**: Use UTF-8 encoding for template files

### Debug Mode

Enable debug logging for detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

To contribute to the structure synchronization system:

1. Add new template types in the `templates/` directory
2. Extend the CLI with new commands
3. Add tests for new functionality
4. Update documentation

## License

This functionality is part of the meta-repo-seed project and follows the same license terms.