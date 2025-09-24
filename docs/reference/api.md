# API Reference

Complete Python API reference for the Meta-Repo Seed system. This documentation covers all classes, methods, and functions available for programmatic use.

## 🏗️ Core Classes

### RepoSeeder

Main class for repository seeding operations.

```python
from seeding import RepoSeeder

class RepoSeeder:
    def __init__(self, 
                 target_dir: str = ".", 
                 project_name: str = None,
                 github_username: str = None,
                 config: Configuration = None,
                 verbose: bool = False,
                 dry_run: bool = False)
```

#### Parameters

**target_dir** (`str`, optional)
- Target directory for project creation
- Default: `"."`

**project_name** (`str`, optional)
- Project name for templates and repository
- Default: Auto-detected from directory name

**github_username** (`str`, optional)
- GitHub username for templates
- Default: Auto-detected from git config

**config** (`Configuration`, optional)
- Configuration object with project settings
- Default: `None` (uses defaults)

**verbose** (`bool`, optional)
- Enable verbose logging output
- Default: `False`

**dry_run** (`bool`, optional)
- Preview mode without making changes
- Default: `False`

#### Methods

##### `seed_repository() -> bool`

Main method to execute repository seeding.

```python
seeder = RepoSeeder(target_dir="./my-project", verbose=True)
success = seeder.seed_repository()
```

**Returns**: `bool` - `True` if seeding successful, `False` otherwise

**Raises**:
- `FileNotFoundError`: Target directory doesn't exist
- `PermissionError`: Insufficient permissions
- `TemplateError`: Template processing error

##### `create_directory_structure() -> None`

Creates the basic directory structure for the project.

```python
seeder.create_directory_structure()
```

##### `process_templates(template_names: List[str] = None) -> None`

Process specified templates or all available templates.

```python
# Process all templates
seeder.process_templates()

# Process specific templates
seeder.process_templates(["gitignore", "github_workflows"])
```

**Parameters**:
- `template_names` (`List[str]`, optional): List of template names to process

##### `setup_github_integration() -> bool`

Configure GitHub integration features.

```python
success = seeder.setup_github_integration()
```

**Returns**: `bool` - `True` if GitHub setup successful

##### `get_template_variables() -> Dict[str, str]`

Get all available template variables and their current values.

```python
variables = seeder.get_template_variables()
print(variables["PROJECT_NAME"])
```

**Returns**: `Dict[str, str]` - Dictionary of variable names and values

### Configuration

Configuration management class for handling project settings.

```python
from seeding import Configuration

class Configuration:
    def __init__(self, config_file: str = None)
```

#### Parameters

**config_file** (`str`, optional)
- Path to configuration file (YAML or JSON)
- Default: `None`

#### Methods

##### `load_config(config_file: str) -> None`

Load configuration from file.

```python
config = Configuration()
config.load_config("./configs/web-app.yml")
```

**Parameters**:
- `config_file` (`str`): Path to configuration file

**Raises**:
- `FileNotFoundError`: Configuration file not found
- `yaml.YAMLError`: Invalid YAML syntax
- `json.JSONDecodeError`: Invalid JSON syntax

##### `save_config(config_file: str, format: str = "yaml") -> None`

Save current configuration to file.

```python
config.save_config("./output/my-config.yml", format="yaml")
config.save_config("./output/my-config.json", format="json")
```

**Parameters**:
- `config_file` (`str`): Output file path
- `format` (`str`, optional): Output format ("yaml" or "json"), default "yaml"

##### `get(key: str, default: Any = None) -> Any`

Get configuration value by key.

```python
project_name = config.get("project.name", "default-project")
github_enabled = config.get("github.enabled", False)
```

**Parameters**:
- `key` (`str`): Configuration key (supports dot notation)
- `default` (`Any`, optional): Default value if key not found

**Returns**: `Any` - Configuration value or default

##### `set(key: str, value: Any) -> None`

Set configuration value.

```python
config.set("project.name", "my-awesome-project")
config.set("github.enabled", True)
```

**Parameters**:
- `key` (`str`): Configuration key (supports dot notation)
- `value` (`Any`): Value to set

##### `merge(other_config: Union[dict, 'Configuration']) -> None`

Merge another configuration into this one.

```python
base_config = Configuration("./configs/base.yml")
override_config = Configuration("./configs/overrides.yml")
base_config.merge(override_config)
```

**Parameters**:
- `other_config` (`Union[dict, Configuration]`): Configuration to merge

## 🔧 Utility Functions

### Template Processing

##### `process_template_file(template_path: str, output_path: str, variables: Dict[str, str]) -> None`

Process a single template file with variable replacement.

```python
from seeding import process_template_file

variables = {
    "PROJECT_NAME": "My Project",
    "GITHUB_USERNAME": "john-doe",
    "CURRENT_DATE": "2025-01-14"
}

process_template_file(
    template_path="./templates/readme.md.template",
    output_path="./README.md", 
    variables=variables
)
```

**Parameters**:
- `template_path` (`str`): Path to template file
- `output_path` (`str`): Path for output file
- `variables` (`Dict[str, str]`): Variables for template replacement

##### `get_available_templates() -> List[str]`

Get list of all available template names.

```python
from seeding import get_available_templates

templates = get_available_templates()
print(templates)  # ['gitignore', 'github_workflows', 'governance', ...]
```

**Returns**: `List[str]` - List of template names

##### `validate_template(template_path: str) -> Tuple[bool, List[str]]`

Validate template file for syntax errors.

```python
from seeding import validate_template

is_valid, errors = validate_template("./templates/my-template.md.template")
if not is_valid:
    for error in errors:
        print(f"Template error: {error}")
```

**Parameters**:
- `template_path` (`str`): Path to template file

**Returns**: `Tuple[bool, List[str]]` - (is_valid, list_of_errors)

### GitHub Integration

##### `create_github_repository(repo_name: str, private: bool = False, organization: str = None) -> bool`

Create GitHub repository using GitHub CLI.

```python
from seeding import create_github_repository

success = create_github_repository(
    repo_name="my-new-project",
    private=True,
    organization="my-org"
)
```

**Parameters**:
- `repo_name` (`str`): Repository name
- `private` (`bool`, optional): Create private repository, default `False`
- `organization` (`str`, optional): Organization name

**Returns**: `bool` - `True` if repository created successfully

##### `setup_branch_protection(repo_name: str, branch: str = "main") -> bool`

Set up branch protection rules.

```python
from seeding import setup_branch_protection

success = setup_branch_protection("my-repo", "main")
```

**Parameters**:
- `repo_name` (`str`): Repository name
- `branch` (`str`, optional): Branch name, default "main"

**Returns**: `bool` - `True` if branch protection set up successfully

### File System Utilities

##### `create_directory_if_not_exists(directory: str) -> None`

Create directory if it doesn't exist (similar to `mkdir -p`).

```python
from seeding import create_directory_if_not_exists

create_directory_if_not_exists("./my-project/src/components")
```

**Parameters**:
- `directory` (`str`): Directory path to create

##### `backup_file(file_path: str, backup_dir: str = None) -> str`

Create backup of existing file.

```python
from seeding import backup_file

backup_path = backup_file("./README.md", "./backups")
print(f"Backup created at: {backup_path}")
```

**Parameters**:
- `file_path` (`str`): Path to file to backup
- `backup_dir` (`str`, optional): Backup directory, default same directory

**Returns**: `str` - Path to backup file

## 🎯 Usage Examples

### Basic Repository Seeding

```python
from seeding import RepoSeeder, Configuration

# Simple seeding
seeder = RepoSeeder(
    target_dir="./my-project",
    project_name="My Awesome Project",
    github_username="john-doe",
    verbose=True
)

success = seeder.seed_repository()
if success:
    print("Repository seeded successfully!")
```

### Configuration-Based Seeding

```python
from seeding import RepoSeeder, Configuration

# Load configuration
config = Configuration()
config.load_config("./configs/web-app.yml")

# Override specific settings
config.set("project.name", "Custom Project Name")
config.set("github.private", True)

# Create seeder with configuration
seeder = RepoSeeder(
    target_dir="./custom-project",
    config=config,
    verbose=True
)

success = seeder.seed_repository()
```

### Custom Template Processing

```python
from seeding import RepoSeeder, process_template_file

# Custom variables
custom_vars = {
    "PROJECT_NAME": "Data Analysis Tool",
    "TECH_STACK": "Python, Pandas, Jupyter",
    "DATA_SOURCE": "CSV Files",
    "CURRENT_DATE": "2025-01-14"
}

# Process custom template
process_template_file(
    template_path="./custom-templates/data-science.md.template",
    output_path="./PROJECT_OVERVIEW.md",
    variables=custom_vars
)

# Use with seeder
seeder = RepoSeeder(target_dir="./data-project")
seeder.process_templates(["gitignore", "documentation"])
```

### Advanced GitHub Integration

```python
from seeding import RepoSeeder, Configuration, create_github_repository, setup_branch_protection

# Create configuration
config = Configuration()
config.set("project.name", "Enterprise App")
config.set("github.enabled", True)
config.set("github.private", True)
config.set("github.organization", "my-company")

# Seed repository
seeder = RepoSeeder(config=config, verbose=True)
seeder.seed_repository()

# Custom GitHub setup
repo_name = config.get("project.name").lower().replace(" ", "-")
create_github_repository(
    repo_name=repo_name,
    private=True,
    organization="my-company"
)

setup_branch_protection(repo_name)
```

### Batch Processing

```python
from seeding import RepoSeeder, Configuration
import os

# Configuration templates
configs = [
    {"name": "web-app", "config": "./configs/web-app.yml"},
    {"name": "api-service", "config": "./configs/api.yml"},
    {"name": "data-pipeline", "config": "./configs/data.yml"}
]

# Create multiple projects
for project in configs:
    config = Configuration()
    config.load_config(project["config"])
    
    target_dir = f"./projects/{project['name']}"
    os.makedirs(target_dir, exist_ok=True)
    
    seeder = RepoSeeder(
        target_dir=target_dir,
        config=config,
        verbose=True
    )
    
    success = seeder.seed_repository()
    print(f"Project {project['name']}: {'✓' if success else '✗'}")
```

## 🔍 Error Handling

### Exception Classes

**`TemplateError`**
- Raised when template processing fails
- Common causes: Invalid template syntax, missing variables

**`ConfigurationError`**
- Raised when configuration is invalid
- Common causes: Invalid YAML/JSON, missing required fields

**`GitHubIntegrationError`**  
- Raised when GitHub operations fail
- Common causes: Authentication issues, API errors

### Error Handling Examples

```python
from seeding import RepoSeeder, TemplateError, ConfigurationError

try:
    seeder = RepoSeeder(target_dir="./my-project", verbose=True)
    success = seeder.seed_repository()
    
except TemplateError as e:
    print(f"Template processing failed: {e}")
    
except ConfigurationError as e:
    print(f"Configuration error: {e}")
    
except FileNotFoundError as e:
    print(f"File not found: {e}")
    
except PermissionError as e:
    print(f"Permission denied: {e}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 📊 Type Hints

The API uses Python type hints for better IDE support and documentation:

```python
from typing import Dict, List, Optional, Union, Tuple, Any
from pathlib import Path

def process_template_file(
    template_path: Union[str, Path],
    output_path: Union[str, Path], 
    variables: Dict[str, str]
) -> None: ...

def get_available_templates() -> List[str]: ...

def validate_template(template_path: str) -> Tuple[bool, List[str]]: ...
```

## 🧪 Testing Utilities

### Mock Objects for Testing

```python
from seeding.testing import MockConfiguration, MockRepoSeeder

# Create mock configuration for testing
mock_config = MockConfiguration({
    "project.name": "test-project",
    "github.enabled": False
})

# Create mock seeder for testing
mock_seeder = MockRepoSeeder(config=mock_config, dry_run=True)
```

### Test Helpers

```python
from seeding.testing import create_temp_project, cleanup_temp_project

# Create temporary project for testing
temp_dir = create_temp_project("test-project")

try:
    # Run your tests
    seeder = RepoSeeder(target_dir=temp_dir)
    seeder.seed_repository()
    
finally:
    # Clean up
    cleanup_temp_project(temp_dir)
```

---

*For more examples and usage patterns, see the [Configuration Guide](../guides/configuration.md) and [Template System Guide](../guides/templates.md).*