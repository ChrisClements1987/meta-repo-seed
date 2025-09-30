"""
Seed Script for Our Company Repo Structure  

This script sets up the initial structure for a new meta-repo and
placeholders for our cloud-storage and portfolio project repos.

The script is idempotent and can be safely run multiple times.
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
import logging
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import tempfile
from datetime import datetime


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def sanitize_project_name(name: str) -> str:
    """
    Sanitize and validate project name to prevent path traversal attacks.
    
    Args:
        name: The project name to sanitize
        
    Returns:
        Sanitized project name
        
    Raises:
        ValueError: If the project name is invalid or potentially dangerous
    """
    import re
    
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty")
    
    name = name.strip()
    
    # Check for reserved names
    if name in ("", ".", ".."):
        raise ValueError("Invalid project name: cannot be '.', '..', or empty")
    
    # Check for absolute paths
    if Path(name).is_absolute():
        raise ValueError("Project name must not be an absolute path")
    
    # Check for path separators
    seps = {os.sep}
    if os.altsep:  # Windows also has forward slash
        seps.add(os.altsep)
    if any(sep in name for sep in seps):
        raise ValueError("Project name must not contain path separators")
    
    # Check for parent directory traversal
    if ".." in name:
        raise ValueError("Project name must not contain '..' sequences")
    
    # Validate against safe character set (allow Unicode letters/numbers plus common safe chars)
    if not re.match(r"^[\w\-_\.]+$", name, re.UNICODE):
        raise ValueError("Project name may only contain letters, numbers, hyphens, underscores, and periods")
    
    # Additional length check for sanity
    if len(name) > 255:
        raise ValueError("Project name too long (maximum 255 characters)")
    
    return name


def get_project_name() -> str:
    """Get the project name from the current directory name."""
    current_dir = Path.cwd()
    # If we're in meta-repo-seed, go up one level
    if current_dir.name == 'meta-repo-seed':
        project_name = current_dir.parent.name
    else:
        project_name = current_dir.name
    
    logger.info(f"Detected project name: {project_name}")
    
    # Sanitize the detected project name
    try:
        return sanitize_project_name(project_name)
    except ValueError as e:
        logger.error(f"Detected project name is invalid: {e}")
        raise ValueError(f"Invalid project name '{project_name}': {e}")


def get_github_username() -> str:
    """
    Get GitHub username from multiple sources in priority order.
    
    Priority order:
    1. GITHUB_USERNAME environment variable
    2. git config github.user (GitHub-specific)  
    3. git config user.name (fallback)
    4. Interactive prompt (only if TTY is available)
    
    Returns:
        GitHub username string
        
    Raises:
        ValueError: If no username found and not running in interactive environment
    """
    # 1. Check environment variable first (best for CI/CD)
    env_username = os.environ.get("GITHUB_USERNAME")
    if env_username and env_username.strip():
        logger.info(f"Using GitHub username from environment: {env_username.strip()}")
        return env_username.strip()
    
    # 2. Try GitHub-specific git config first
    try:
        result = subprocess.run(
            ['git', 'config', '--global', 'github.user'],
            capture_output=True,
            text=True,
            check=True
        )
        username = result.stdout.strip()
        if username:
            logger.info(f"Detected GitHub username from git config (github.user): {username}")
            return username
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.debug("GitHub username not found in git config github.user")
    
    # 3. Fallback to general git user.name
    try:
        result = subprocess.run(
            ['git', 'config', '--global', 'user.name'],
            capture_output=True,
            text=True,
            check=True
        )
        username = result.stdout.strip()
        if username:
            logger.info(f"Using git user.name as GitHub username: {username}")
            return username
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.debug("Could not detect username from git config user.name")
    
    # 4. Interactive prompt only if TTY is available
    if sys.stdin.isatty():
        try:
            username = input("Please enter your GitHub username: ").strip()
            if username:
                logger.info(f"GitHub username provided interactively: {username}")
                return username
        except (EOFError, KeyboardInterrupt):
            logger.info("Interactive input cancelled by user")
    
    # If we reach here, no username was found and we're in non-interactive environment
    raise ValueError(
        "GitHub username not provided and no non-interactive source available. "
        "Use --username argument or set GITHUB_USERNAME environment variable for CI/CD environments."
    )


def ensure_directory_exists(path: Path, description: str = "") -> bool:
    """
    Ensure a directory exists, creating it if necessary.
    Returns True if directory was created, False if it already existed.
    """
    if path.exists():
        if path.is_dir():
            logger.debug(f"Directory already exists: {path}")
            return False
        else:
            raise FileExistsError(f"Path exists but is not a directory: {path}")
    
    try:
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path} {description}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        raise


def safe_open_for_write(path: Path, encoding: str = 'utf-8'):
    """
    Safely open a file for writing, refusing to follow symlinks.
    
    Args:
        path: Path to the file to open
        encoding: File encoding (default: utf-8)
        
    Returns:
        File object opened for writing
        
    Raises:
        RuntimeError: If the path is a symlink
        OSError: If file operations fail
    """
    # Check if the path is a symlink before attempting to write
    if path.is_symlink():
        raise RuntimeError(f"Refusing to write to symlink: {path}")
    
    # Use O_NOFOLLOW on systems that support it for additional protection
    if hasattr(os, 'O_NOFOLLOW') and os.name != 'nt':  # Not available on Windows
        try:
            # Open with O_NOFOLLOW to prevent following symlinks at the OS level
            fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW)
            return os.fdopen(fd, 'w', encoding=encoding)
        except OSError as e:
            # If O_NOFOLLOW fails due to symlink, provide clear error
            import errno
            if e.errno == errno.ELOOP:  # Too many symbolic links encountered
                raise RuntimeError(f"Symlink detected and blocked: {path}")
            raise
    
    # Fallback for Windows or systems without O_NOFOLLOW
    # The path.is_symlink() check above provides protection
    return open(path, 'w', encoding=encoding)


def safe_copy_file(source: Path, destination: Path) -> None:
    """
    Safely copy a file, refusing to follow symlinks in the destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Raises:
        RuntimeError: If destination is a symlink
        OSError: If file operations fail
    """
    # Check if destination is a symlink
    if destination.is_symlink():
        raise RuntimeError(f"Refusing to overwrite symlink: {destination}")
    
    # Open destination safely for binary writing
    if hasattr(os, 'O_NOFOLLOW') and os.name != 'nt':
        # Use O_NOFOLLOW on Unix systems
        fd = os.open(str(destination), os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_NOFOLLOW)
        with open(source, 'rb') as src, os.fdopen(fd, 'wb') as dst:
            shutil.copyfileobj(src, dst)
    else:
        # Fallback for Windows (we already checked for symlinks above)
        with open(source, 'rb') as src, open(destination, 'wb') as dst:
            shutil.copyfileobj(src, dst)
    
    # Copy metadata (permissions, timestamps) safely
    # Note: shutil.copystat follows symlinks, so we avoid it
    try:
        stat = source.stat()
        os.utime(destination, (stat.st_atime, stat.st_mtime))
        if os.name != 'nt':  # Unix-like systems
            os.chmod(destination, stat.st_mode)
    except (OSError, AttributeError):
        # If metadata copying fails, file copy still succeeded
        logger.debug(f"Could not copy metadata for {destination}")


def copy_template_file(source: Path, destination: Path, description: str = "") -> bool:
    """
    Copy a template file to destination if it doesn't exist.
    Returns True if file was copied, False if it already existed.
    """
    if destination.exists():
        logger.debug(f"File already exists: {destination}")
        return False
    
    try:
        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Use safe file copying to prevent symlink attacks
        safe_copy_file(source, destination)
        
        logger.info(f"Copied template file: {destination} {description}")
        return True
    except RuntimeError as e:
        # Handle symlink protection errors specifically
        logger.error(f"Security violation: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to copy {source} to {destination}: {e}")
        raise


def process_template_content(content: str, replacements: Dict[str, str]) -> str:
    """
    Process template content by replacing placeholder variables.
    
    Args:
        content: Template content with {{VARIABLE}} placeholders
        replacements: Dictionary mapping variable names to replacement values
    
    Returns:
        Processed content with variables replaced
    """
    if not content or not replacements:
        return content
    
    # Replace each placeholder with its corresponding value
    for placeholder, value in replacements.items():
        content = content.replace(f"{{{{{placeholder}}}}}", str(value))
    
    return content


def create_file_from_template(template_path: Path, destination: Path, replacements: Dict[str, str], description: str = "") -> bool:
    """
    Create a file from a template with placeholder replacements.
    Returns True if file was created, False if it already existed.
    """
    if destination.exists():
        logger.debug(f"File already exists: {destination}")
        return False
    
    if not template_path.exists():
        logger.warning(f"Template file not found: {template_path}")
        return False
    
    try:
        # Read template content with encoding error handling
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Handle binary files gracefully by copying as-is
            logger.warning(f"Template file contains binary content, copying as-is: {template_path}")
            safe_copy_file(template_path, destination)
            logger.info(f"Copied binary template file: {destination} {description}")
            return True
        except PermissionError as e:
            # Handle permission errors when reading template
            logger.error(f"Permission denied reading template {template_path}: {e}")
            return False
        
        # Process template content with variable replacements
        content = process_template_content(content, replacements)
        
        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Write processed content to destination safely
        with safe_open_for_write(destination, encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created file from template: {destination} {description}")
        return True
    except RuntimeError as e:
        # Handle symlink protection errors specifically  
        logger.error(f"Security violation: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create {destination} from template {template_path}: {e}")
        raise


class Configuration:
    """
    Handle configuration file operations for seeding parameters.
    
    Supports both data container interface (for tests) and configuration manager interface (for main script).
    """
    
    def __init__(
        self, 
        project_name: Optional[str] = None,
        github_username: Optional[str] = None,
        dry_run: bool = False,
        templates_dir: Optional[Union[str, Path]] = None,
        base_path: Optional[Union[str, Path]] = None
    ):
        """Initialize configuration with optional parameters."""
        self.project_name = project_name
        self.github_username = github_username
        self.dry_run = dry_run
        self.templates_dir = Path(templates_dir) if templates_dir else None
        self.base_path = Path(base_path) if base_path else None
        
        # Legacy interface support
        self.config_data = {}
        self.supported_formats = ['.yaml', '.yml', '.json']
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Configuration':
        """Create Configuration instance from dictionary."""
        return cls(
            project_name=data.get('project_name'),
            github_username=data.get('github_username'),
            dry_run=data.get('dry_run', False),
            templates_dir=data.get('templates_dir'),
            base_path=data.get('base_path')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Configuration to dictionary."""
        return {
            'project_name': self.project_name,
            'github_username': self.github_username,
            'dry_run': self.dry_run,
            'templates_dir': str(self.templates_dir) if self.templates_dir else None,
            'base_path': str(self.base_path) if self.base_path else None
        }
    
    @classmethod
    def load(cls, config_file: Path) -> Optional['Configuration']:
        """
        Load configuration from file.
        
        Args:
            config_file: Path to configuration file
            
        Returns:
            Configuration instance or None if failed
        """
        if not config_file.exists():
            return None
            
        try:
            suffix = config_file.suffix.lower()
            
            if suffix == '.yaml' or suffix == '.yml':
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            elif suffix == '.json':
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                module_logger = logger if logger else logging.getLogger(__name__)
                module_logger.warning(f"Unsupported config format: {suffix}")
                return None
            
            if data is None:
                return None
                
            return cls.from_dict(data)
            
        except Exception as e:
            module_logger = logger if logger else logging.getLogger(__name__)
            module_logger.error(f"Failed to load configuration from {config_file}: {e}")
            return None
    
    def save(self, config_file: Path) -> bool:
        """
        Save configuration to file.
        
        Args:
            config_file: Path to save configuration file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure parent directory exists
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Determine format from file extension
            suffix = config_file.suffix.lower()
            
            data = self.to_dict()
            
            if suffix == '.yaml' or suffix == '.yml':
                with open(config_file, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(data, f, default_flow_style=False, indent=2)
            elif suffix == '.json':
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
            else:
                raise ValueError(f"Unsupported config format: {suffix}")
            
            # Use module logger or create one if needed
            module_logger = logger if logger else logging.getLogger(__name__)
            module_logger.info(f"Saved configuration to: {config_file}")
            return True
            
        except Exception as e:
            # Use module logger or create one if needed
            module_logger = logger if logger else logging.getLogger(__name__)
            module_logger.error(f"Failed to save configuration to {config_file}: {e}")
            # Re-raise ValueError for unsupported formats
            if isinstance(e, ValueError) and "Unsupported config format" in str(e):
                raise
            return False
    
    def save_config(self, config_path: Path, project_name: str, github_username: str, 
                   template_path: Optional[str] = None, **kwargs) -> None:
        """Save current configuration to a file."""
        config_data = {
            'project_name': project_name,
            'github_username': github_username,
            'created_at': datetime.now().isoformat(),
            'version': '1.1.0',
            'template_path': template_path,
            'replacements': {
                'PROJECT_NAME': project_name,
                'GITHUB_USERNAME': github_username,
                'CURRENT_DATE': datetime.now().strftime('%Y-%m-%d'),
                'DECISION_NUMBER': kwargs.get('decision_number', '001'),
                'DECISION_TITLE': kwargs.get('decision_title', 'Sample Decision'),
                'STATUS': kwargs.get('status', 'Proposed'),
                'ALTERNATIVE_NAME': kwargs.get('alternative_name', 'Alternative Option')
            }
        }
        
        # Add any additional configuration options
        for key, value in kwargs.items():
            if key not in config_data and key not in config_data['replacements']:
                config_data[key] = value
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config_path.suffix.lower() in ['.yaml', '.yml']:
            try:
                with open(config_path, 'w', encoding='utf-8') as f:
                    yaml.safe_dump(config_data, f, default_flow_style=False, sort_keys=False)
                logger.info(f"✓ Configuration saved to {config_path}")
            except ImportError:
                logger.warning("PyYAML not available, falling back to JSON format")
                json_path = config_path.with_suffix('.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(config_data, f, indent=2)
                logger.info(f"✓ Configuration saved to {json_path}")
        else:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"✓ Configuration saved to {config_path}")
    
    def load_config(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from a file."""
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        if config_path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported config format. Supported: {', '.join(self.supported_formats)}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    try:
                        self.config_data = yaml.safe_load(f) or {}
                    except ImportError:
                        raise ImportError("PyYAML is required for YAML config files. Install with: pip install pyyaml")
                else:
                    self.config_data = json.load(f)
            
            logger.info(f"✓ Configuration loaded from {config_path}")
            return self.config_data
            
        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ValueError(f"Invalid configuration file format: {e}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {e}")
    
    def get_project_name(self) -> Optional[str]:
        """Get project name from loaded configuration."""
        return self.config_data.get('project_name')
    
    def get_github_username(self) -> Optional[str]:
        """Get GitHub username from loaded configuration."""
        return self.config_data.get('github_username')
    
    def get_template_path(self) -> Optional[str]:
        """Get template path from loaded configuration."""
        return self.config_data.get('template_path')
    
    def get_replacements(self) -> Dict[str, str]:
        """Get template replacements from loaded configuration."""
        return self.config_data.get('replacements', {})
    
    def list_available_configs(self, directory: Path = None) -> List[Path]:
        """List available configuration files in a directory."""
        search_dir = directory or Path.cwd()
        config_files = []
        
        for ext in self.supported_formats:
            config_files.extend(search_dir.glob(f"*{ext}"))
        
        return sorted(config_files)


class RepoSeeder:
    """Main class for seeding repository structure."""
    
    def __init__(self, project_name: str, github_username: str, dry_run: bool = False, 
                 config_data: Optional[Dict[str, Any]] = None):
        self.project_name = project_name
        self.github_username = github_username
        self.dry_run = dry_run
        self.config_data = config_data or {}
        self.base_path = Path.cwd().parent if Path.cwd().name == 'meta-repo-seed' else Path.cwd()
        self.project_root = self.base_path / project_name
        self.meta_repo_path = self.project_root / 'meta-repo'
        self.cloud_storage_path = self.project_root / 'cloud-storage'
        self.template_path = Path.cwd()  # Current directory contains templates
        self.templates_dir = self.template_path / 'templates'
        
        # Template replacements dictionary - use config data if available
        if self.config_data and 'replacements' in self.config_data:
            self.replacements = self.config_data['replacements'].copy()
            # Update with current values to ensure they're fresh
            self.replacements['PROJECT_NAME'] = project_name
            self.replacements['GITHUB_USERNAME'] = github_username
            self.replacements['CURRENT_DATE'] = datetime.now().strftime('%Y-%m-%d')
        else:
            self.replacements = {
                'PROJECT_NAME': project_name,
                'GITHUB_USERNAME': github_username,
                'CURRENT_DATE': datetime.now().strftime('%Y-%m-%d'),
                'DECISION_NUMBER': '001',
                'DECISION_TITLE': 'Sample Decision',
                'STATUS': 'Proposed',
                'ALTERNATIVE_NAME': 'Alternative Option'
            }
        
        logger.info(f"Initializing RepoSeeder for project: {project_name}")
        logger.info(f"GitHub username: {github_username}")
        logger.info(f"Project root: {self.project_root}")
        logger.info(f"Templates directory: {self.templates_dir}")
        logger.info(f"Dry run mode: {dry_run}")
        if config_data:
            logger.info(f"Using configuration data with {len(config_data)} settings")
    
    def run(self):
        """Main execution method."""
        if self.dry_run:
            logger.info("DRY RUN MODE - No actual changes will be made")
        
        logger.info("Starting repository seeding process...")
        
        # Core structure setup
        self.create_base_structure()
        self.setup_meta_repo()
        self.setup_cloud_storage()
        self.create_governance_structure()
        self.create_automation_scripts()
        self.setup_documentation()
        self.create_template_content()
        self.create_infrastructure_templates()
        self.setup_code_formatting()
        self.create_github_repository_settings()
        
        logger.info("Repository seeding completed successfully!")
    
    def create_base_structure(self):
        """Create the base project structure."""
        logger.info("Creating base project structure...")
        
        if not self.dry_run:
            ensure_directory_exists(self.project_root, f"(project root)")
            ensure_directory_exists(self.meta_repo_path, "(meta-repo)")
            ensure_directory_exists(self.cloud_storage_path, "(cloud-storage)")
            
            # Create placeholder directories for future repos
            ensure_directory_exists(self.project_root / 'core-services', "(core-services)")
            ensure_directory_exists(self.project_root / 'saas-products', "(saas-products)")
            ensure_directory_exists(self.project_root / 'partner-products', "(partner-products)")
            ensure_directory_exists(self.project_root / 'charity-products', "(charity-products)")

    def setup_meta_repo(self):
        """Set up the meta-repo with Git initialization and GitHub workflows."""
        logger.info("Setting up meta-repo...")
        
        if not self.dry_run:
            # Initialize Git repository
            self.init_git_repo(self.meta_repo_path)
            
            # Create .gitignore
            self.create_gitignore()
            
            # Create GitHub workflows
            workflows_path = self.meta_repo_path / '.github' / 'workflows'
            ensure_directory_exists(workflows_path, "(GitHub workflows)")
            
            # Copy workflow templates
            ci_template = self.templates_dir / 'github' / 'workflows' / 'ci.yml.template'
            ci_dest = workflows_path / 'ci.yml'
            copy_template_file(ci_template, ci_dest, "(CI workflow)")
            
            readme_template = self.templates_dir / 'github' / 'workflows' / 'readme-docs.yml.template'
            readme_dest = workflows_path / 'readme-docs.yml'
            copy_template_file(readme_template, readme_dest, "(README docs workflow)")
    
    def init_git_repo(self, repo_path: Path):
        """Initialize a Git repository if it doesn't exist."""
        git_path = repo_path / '.git'
        if git_path.exists():
            logger.debug(f"Git repository already exists at: {repo_path}")
            return
        
        try:
            # Use cwd parameter instead of changing process directory
            subprocess.run(['git', 'init'], check=True, capture_output=True, text=True, cwd=str(repo_path))
            logger.info(f"Initialized Git repository: {repo_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to initialize Git repository: {e}")
            raise
    
    def create_gitignore(self):
        """Create a comprehensive .gitignore file from template."""
        gitignore_path = self.meta_repo_path / '.gitignore'
        if gitignore_path.exists():
            logger.debug(".gitignore already exists")
            return
        
        template_path = self.templates_dir / 'gitignore.template'
        copy_template_file(template_path, gitignore_path, "(.gitignore)")
    
    def setup_cloud_storage(self):
        """Set up the cloud storage directory structure."""
        logger.info("Setting up cloud storage structure...")
        
        if not self.dry_run:
            # Strategy directories
            strategy_path = self.cloud_storage_path / 'strategy'
            ensure_directory_exists(strategy_path, "(strategy)")
            
            # Architecture directories
            arch_path = self.cloud_storage_path / 'architecture'
            ensure_directory_exists(arch_path, "(architecture)")
            ensure_directory_exists(arch_path / 'principles', "(architecture principles)")
            ensure_directory_exists(arch_path / 'adr', "(architecture decision records)")
            ensure_directory_exists(arch_path / 'patterns', "(architecture patterns)")
            ensure_directory_exists(arch_path / 'portfolio', "(architecture portfolio)")
            
            # Workspace directories
            workspace_path = self.cloud_storage_path / 'workspace'
            ensure_directory_exists(workspace_path, "(workspace)")
            ensure_directory_exists(workspace_path / 'initiatives', "(initiatives)")
            ensure_directory_exists(workspace_path / 'meeting-minutes', "(meeting minutes)")
            ensure_directory_exists(workspace_path / 'projects', "(projects)")
            ensure_directory_exists(workspace_path / 'ad-hoc', "(ad-hoc)")
            ensure_directory_exists(workspace_path / 'notes', "(notes)")
            ensure_directory_exists(workspace_path / 'personal', "(personal)")
            ensure_directory_exists(workspace_path / 'family', "(family)")
            
            # Documentation directories
            docs_path = self.cloud_storage_path / 'documentation'
            ensure_directory_exists(docs_path, "(cloud documentation)")
            ensure_directory_exists(docs_path / 'meta-repo', "(meta-repo docs)")
            ensure_directory_exists(docs_path / 'core-services', "(core-services docs)")
            ensure_directory_exists(docs_path / 'saas-products', "(saas-products docs)")
            ensure_directory_exists(docs_path / 'partner-products', "(partner-products docs)")
            ensure_directory_exists(docs_path / 'charity-products', "(charity-products docs)")
    
    def create_governance_structure(self):
        """Create the governance structure in meta-repo."""
        logger.info("Creating governance structure...")
        
        if not self.dry_run:
            governance_path = self.meta_repo_path / 'governance'
            
            # Structure directory (for JSON schemas)
            structure_path = governance_path / 'structure'
            ensure_directory_exists(structure_path, "(structure)")
            
            # Create structure.json and schema files
            self.create_structure_json(structure_path)
            self.create_meta_repo_schema(structure_path)
            
            # Policies directory
            policies_path = governance_path / 'policies'
            ensure_directory_exists(policies_path, "(policies)")
            
            # Processes directory
            processes_path = governance_path / 'processes'
            ensure_directory_exists(processes_path, "(processes)")
            
            # Shared resources directory
            resources_path = governance_path / 'shared-resources'
            ensure_directory_exists(resources_path, "(shared resources)")
            ensure_directory_exists(resources_path / 'templates', "(templates)")
            
            # Standards directory
            standards_path = governance_path / 'standards'
            ensure_directory_exists(standards_path, "(standards)")
    
    def create_structure_json(self, structure_path: Path):
        """Create the structure.json file that defines the repository structure."""
        structure_file = structure_path / 'structure.json'
        if structure_file.exists():
            logger.debug("structure.json already exists")
            return
        
        structure_data = {
            "project_name": self.project_name,
            "github_username": self.github_username,
            "created_date": datetime.now().date().isoformat(),
            "version": "2.1.0",
            "structure": {
                "cloud-storage": {
                    "strategy": ["vision.md", "mission.md", "strategic-roadmap.md"],
                    "architecture": {
                        "principles": ["principles.md"],
                        "adr": [],
                        "patterns": [],
                        "portfolio": []
                    },
                    "workspace": {
                        "initiatives": [],
                        "meeting-minutes": [],
                        "projects": [],
                        "ad-hoc": [],
                        "notes": [],
                        "personal": [],
                        "family": []
                    },
                    "documentation": {
                        "meta-repo": [],
                        "core-services": [],
                        "saas-products": [],
                        "partner-products": [],
                        "charity-products": []
                    }
                },
                "meta-repo": {
                    "governance": {
                        "structure": ["structure.json", "meta-repo-schema.json"],
                        "policies": [
                            "contributing.md",
                            "code-of-conduct.md", 
                            "privacy-policy.md",
                            "security-policy.md",
                            "license.md",
                            "terms-of-service.md"
                        ],
                        "processes": [
                            "onboarding.md",
                            "offboarding.md",
                            "code-review.md",
                            "issue-management.md",
                            "release-management.md",
                            "security-management.md"
                        ],
                        "shared-resources": {
                            "templates": [
                                "pull-request-template.md",
                                "issue-template.md",
                                "architecture-decision-record-template.md"
                            ]
                        },
                        "standards": [
                            "coding-standards.md",
                            "documentation-standards.md",
                            "testing-standards.md",
                            "security-standards.md",
                            "access-control-standards.md"
                        ]
                    },
                    "automation": {
                        "scripts": [
                            "initialise_repo.py",
                            "enforce_structure.py", 
                            "generate_readmes.py"
                        ]
                    },
                    "documentation": {
                        "guides": ["getting-started.md"],
                        "shared-resources": [
                            "templates.md",
                            "glossary.md", 
                            "faq.md"
                        ]
                    }
                },
                "core-services": {
                    "contented-cms": [],
                    "lightbulb-innovation-hub": [],
                    "product-backlog-management": [],
                    "tasks": []
                },
                "saas-products": {
                    "sports-league": [],
                    "saas-product-2": []
                },
                "partner-products": {},
                "charity-products": {}
            }
        }
        
        try:
            with open(structure_file, 'w', encoding='utf-8') as f:
                json.dump(structure_data, f, indent=2)
            logger.info(f"Created structure.json: {structure_file}")
        except Exception as e:
            logger.error(f"Failed to create structure.json: {e}")
            raise
    
    def create_meta_repo_schema(self, structure_path: Path):
        """Create the meta-repo-schema.json file."""
        schema_file = structure_path / 'meta-repo-schema.json'
        if schema_file.exists():
            logger.debug("meta-repo-schema.json already exists")
            return
        
        schema_data = {
            "$schema": "https://json-schema.org/draft-07/schema#",
            "title": "Meta Repository Structure Schema",
            "description": "Schema for validating meta-repository structure",
            "type": "object",
            "properties": {
                "project_name": {"type": "string"},
                "github_username": {"type": "string"},
                "created_date": {"type": "string", "format": "date"},
                "version": {"type": "string"},
                "structure": {
                    "type": "object",
                    "properties": {
                        "cloud-storage": {"type": "object"},
                        "meta-repo": {"type": "object"},
                        "core-services": {"type": "object"},
                        "saas-products": {"type": "object"},
                        "partner-products": {"type": "object"},
                        "charity-products": {"type": "object"}
                    },
                    "required": ["cloud-storage", "meta-repo"]
                }
            },
            "required": ["project_name", "github_username", "version", "structure"]
        }
        
        try:
            with open(schema_file, 'w', encoding='utf-8') as f:
                json.dump(schema_data, f, indent=2)
            logger.info(f"Created meta-repo-schema.json: {schema_file}")
        except Exception as e:
            logger.error(f"Failed to create meta-repo-schema.json: {e}")
            raise
    
    def create_automation_scripts(self):
        """Create the automation scripts directory and placeholder scripts."""
        logger.info("Creating automation scripts...")
        
        if not self.dry_run:
            scripts_path = self.meta_repo_path / 'automation' / 'scripts'
            ensure_directory_exists(scripts_path, "(automation scripts)")
            
            # Create placeholder script files
            self.create_script_file(scripts_path / 'initialise_repo.py', 'initialise_repo')
            self.create_script_file(scripts_path / 'enforce_structure.py', 'enforce_structure')
            self.create_script_file(scripts_path / 'generate_readmes.py', 'generate_readmes')
    
    def create_script_file(self, script_path: Path, script_type: str):
        """Create a placeholder script file."""
        if script_path.exists():
            logger.debug(f"Script already exists: {script_path}")
            return
        
        script_templates = {
            'initialise_repo': '''#!/usr/bin/env python3
"""
Repository Initialization Script

This script initializes repository structure based on governance/structure/structure.json.
Uses the Repository Automation Module (Issue #32 implementation).

Usage:
    python initialise_repo.py [--dry-run] [--verbose] [--structure PATH] [--target PATH]

Note: This script requires the Structure Parser Module and Repository Automation Module.
      Run from the repository root directory.
"""

import sys
import argparse
from pathlib import Path

# Add the src directory to Python path for imports
src_path = Path(__file__).parent.parent.parent / 'src'
if src_path.exists():
    sys.path.insert(0, str(src_path))

try:
    from automation.repository_initializer import RepositoryInitializer
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the repository root with the src/ directory available")
    print("💡 This script requires the Repository Automation Module (Issue #32)")
    sys.exit(1)


def main():
    """Initialize repository structure based on structure.json."""
    parser = argparse.ArgumentParser(
        description="Initialize repository structure from structure.json"
    )
    
    parser.add_argument('--structure', type=Path, 
                       default=Path('governance/structure/structure.json'),
                       help='Path to structure.json file')
    parser.add_argument('--target', type=Path,
                       help='Target directory for initialization')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without making them')
    parser.add_argument('--verbose', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    print("🚀 Repository Structure Initializer")
    print("=" * 40)
    
    if not args.structure.exists():
        print(f"❌ Structure file not found: {args.structure}")
        return 1
    
    try:
        initializer = RepositoryInitializer(dry_run=args.dry_run, verbose=args.verbose)
        success = initializer.initialize_repository(args.structure, args.target)
        
        if success:
            print("✅ Repository initialization completed!")
            return 0
        else:
            print("❌ Repository initialization failed.")
            return 1
            
    except KeyboardInterrupt:
        print("\\n⏹️  Initialization cancelled")
        return 1


if __name__ == "__main__":
    sys.exit(main())
''',
            'enforce_structure': '''#!/usr/bin/env python3
"""
Script to enforce the structure of the repo based on 
governance/structure/structure.json
"""

import json
import logging
from pathlib import Path


def main():
    """Enforce repository structure compliance."""
    print(f"Enforcing repository structure...")
    # TODO: Implementation needed
    

if __name__ == "__main__":
    main()
''',
            'generate_readmes': '''#!/usr/bin/env python3
"""
Script to generate README files for each service based on 
governance/structure/structure.json
"""

import json
import logging
from pathlib import Path


def main():
    """Generate README files based on structure."""
    print(f"Generating README files...")
    # TODO: Implementation needed
    

if __name__ == "__main__":
    main()
'''
        }
        
        try:
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_templates.get(script_type, '# TODO: Implement script\n'))
            script_path.chmod(0o755)  # Make executable
            logger.info(f"Created script: {script_path}")
        except Exception as e:
            logger.error(f"Failed to create script {script_path}: {e}")
            raise
    
    def setup_documentation(self):
        """Set up the documentation structure."""
        logger.info("Setting up documentation structure...")
        
        if not self.dry_run:
            docs_path = self.meta_repo_path / 'documentation'
            ensure_directory_exists(docs_path, "(meta-repo documentation)")
            
            # Create documentation subdirectories
            ensure_directory_exists(docs_path / 'guides', "(guides)")
            ensure_directory_exists(docs_path / 'shared-resources', "(shared resources)")
            
            # Create placeholder documentation files
            self.create_placeholder_docs()
    
    def create_placeholder_docs(self):
        """Create placeholder documentation files from templates."""
        docs_path = self.meta_repo_path / 'documentation'
        
        # Getting started guide from template
        getting_started_path = docs_path / 'guides' / 'getting-started.md'
        template_path = self.templates_dir / 'documentation' / 'guides' / 'getting-started.md.template'
        
        if not self.dry_run:
            create_file_from_template(
                template_path, 
                getting_started_path, 
                self.replacements, 
                "(getting started guide)"
            )
    
    def create_template_content(self):
        """Create content files from templates."""
        logger.info("Creating content from templates...")
        
        if not self.dry_run:
            # Create governance policy files
            self.create_governance_policies()
            # Create cloud storage strategy files  
            self.create_strategy_files()
            # Create shared resource templates
            self.create_shared_resource_templates()
    
    def create_governance_policies(self):
        """Create governance policy files from templates."""
        policies_path = self.meta_repo_path / 'governance' / 'policies'
        
        policy_templates = [
            'contributing.md.template',
            'code-of-conduct.md.template'
        ]
        
        for template_name in policy_templates:
            template_path = self.templates_dir / 'governance' / 'policies' / template_name
            dest_path = policies_path / template_name.replace('.template', '')
            create_file_from_template(template_path, dest_path, self.replacements, f"(policy: {template_name})")
    
    def create_strategy_files(self):
        """Create strategy files from templates."""
        strategy_path = self.cloud_storage_path / 'strategy'
        
        strategy_templates = [
            'vision.md.template',
            'mission.md.template'
        ]
        
        for template_name in strategy_templates:
            template_path = self.templates_dir / 'cloud-storage' / 'strategy' / template_name
            dest_path = strategy_path / template_name.replace('.template', '')
            create_file_from_template(template_path, dest_path, self.replacements, f"(strategy: {template_name})")
    
    def create_shared_resource_templates(self):
        """Create shared resource template files."""
        templates_path = self.meta_repo_path / 'governance' / 'shared-resources' / 'templates'
        
        resource_templates = [
            'pull-request-template.md.template',
            'issue-template.md.template',
            'architecture-decision-record-template.md.template'
        ]
        
        for template_name in resource_templates:
            template_path = self.templates_dir / 'governance' / 'shared-resources' / 'templates' / template_name
            dest_path = templates_path / template_name.replace('.template', '')
            create_file_from_template(template_path, dest_path, self.replacements, f"(template: {template_name})")

    def create_infrastructure_templates(self):
        """Create Infrastructure as Code templates for 10-minute deployment.
        
        Creates comprehensive infrastructure templates including:
        - Terraform configurations for multiple cloud providers
        - Kubernetes manifests for container orchestration
        - Docker configurations for containerization
        - Environment-specific configurations (dev/staging/production)
        """
        if not self.dry_run:
            logger.info("📦 Creating Infrastructure as Code templates...")
        
        infrastructure_path = self.meta_repo_path / 'infrastructure'
        if not self.dry_run:
            ensure_directory_exists(infrastructure_path, "Infrastructure as Code root directory")
        
        # Create main directory structure
        terraform_path = infrastructure_path / 'terraform'
        kubernetes_path = infrastructure_path / 'kubernetes'
        docker_path = infrastructure_path / 'docker'
        environments_path = infrastructure_path / 'environments'
        
        if not self.dry_run:
            ensure_directory_exists(terraform_path, "Terraform configuration directory")
            ensure_directory_exists(kubernetes_path, "Kubernetes manifests directory")
            ensure_directory_exists(docker_path, "Docker configuration directory")
            ensure_directory_exists(environments_path, "Environment configurations directory")
        
        # Create provider-specific directories
        aws_terraform_path = terraform_path / 'aws'
        azure_terraform_path = terraform_path / 'azure'
        gcp_terraform_path = terraform_path / 'gcp'
        
        if not self.dry_run:
            ensure_directory_exists(aws_terraform_path, "AWS Terraform modules")
            ensure_directory_exists(azure_terraform_path, "Azure Terraform modules")
            ensure_directory_exists(gcp_terraform_path, "GCP Terraform modules")
        
        # Create environment directories
        if not self.dry_run:
            for env in ['dev', 'staging', 'production']:
                env_path = environments_path / env
                ensure_directory_exists(env_path, f"{env.capitalize()} environment configuration")
        
        # Create main Terraform configuration files
        terraform_templates = [
            'main.tf',
            'variables.tf',
            'outputs.tf',
            'providers.tf'
        ]
        
        for template_name in terraform_templates:
            template_path = self.templates_dir / 'infrastructure' / 'terraform' / template_name
            dest_path = terraform_path / template_name
            create_file_from_template(template_path, dest_path, self.replacements, f"(terraform: {template_name})")
        
        # Create provider-specific Terraform modules
        provider_configs = [
            ('aws', aws_terraform_path),
            ('azure', azure_terraform_path),
            ('gcp', gcp_terraform_path)
        ]
        
        for provider, dest_path in provider_configs:
            provider_template_path = self.templates_dir / 'infrastructure' / 'terraform' / provider / 'main.tf'
            provider_dest_path = dest_path / 'main.tf'
            create_file_from_template(provider_template_path, provider_dest_path, self.replacements, f"(terraform: {provider.upper()} infrastructure)")
        
        # Create Kubernetes manifests
        kubernetes_templates = [
            'namespace.yaml',
            'deployment.yaml',
            'service.yaml',
            'ingress.yaml',
            'configmap.yaml',
            'secret.yaml'
        ]
        
        for template_name in kubernetes_templates:
            template_path = self.templates_dir / 'infrastructure' / 'kubernetes' / template_name
            dest_path = kubernetes_path / template_name
            create_file_from_template(template_path, dest_path, self.replacements, f"(kubernetes: {template_name})")
        
        # Create Docker configuration files
        docker_templates = [
            'Dockerfile.template',
            'docker-compose.yml',
            'docker-compose.prod.yml',
            '.dockerignore'
        ]
        
        for template_name in docker_templates:
            template_path = self.templates_dir / 'infrastructure' / 'docker' / template_name
            dest_path = docker_path / template_name
            create_file_from_template(template_path, dest_path, self.replacements, f"(docker: {template_name})")
        
        # Create environment-specific configuration files
        for env in ['dev', 'staging', 'production']:
            # Terraform variables for each environment
            tfvars_template_path = self.templates_dir / 'infrastructure' / 'environments' / env / 'terraform.tfvars'
            tfvars_dest_path = environments_path / env / 'terraform.tfvars'
            create_file_from_template(tfvars_template_path, tfvars_dest_path, self.replacements, f"(terraform vars: {env})")
            
            # Kubernetes configuration for each environment
            k8s_template_path = self.templates_dir / 'infrastructure' / 'environments' / env / 'kubernetes.yaml'
            k8s_dest_path = environments_path / env / 'kubernetes.yaml'
            create_file_from_template(k8s_template_path, k8s_dest_path, self.replacements, f"(kubernetes config: {env})")
        
        if not self.dry_run:
            logger.info("✅ Infrastructure as Code templates created successfully!")
            logger.info(f"    📂 Terraform configurations: {terraform_path}")
            logger.info(f"    📂 Kubernetes manifests: {kubernetes_path}")
            logger.info(f"    📂 Docker configurations: {docker_path}")
            logger.info(f"    📂 Environment configs: {environments_path}")

    def setup_code_formatting(self):
        """Set up code formatting and pre-commit hooks for development workflow.
        
        Creates comprehensive code formatting configuration including:
        - Pre-commit hooks for automated formatting and quality checks
        - Black, isort, flake8 configurations for consistent code style
        - pyproject.toml with tool configurations and project metadata
        - Setup script for easy developer environment configuration
        - Requirements file for formatting dependencies
        """
        if not self.dry_run:
            logger.info("🎨 Setting up code formatting and pre-commit hooks...")
        
        # Create scripts directory if it doesn't exist
        scripts_path = self.meta_repo_path / 'scripts'
        if not self.dry_run:
            ensure_directory_exists(scripts_path, "Scripts directory")
        
        # Create pre-commit configuration
        precommit_template_path = self.templates_dir / 'code-formatting' / '.pre-commit-config.yaml'
        precommit_dest_path = self.meta_repo_path / '.pre-commit-config.yaml'
        if not self.dry_run:
            create_file_from_template(precommit_template_path, precommit_dest_path, self.replacements, "(pre-commit config)")
        
        # Create pyproject.toml configuration
        pyproject_template_path = self.templates_dir / 'code-formatting' / 'pyproject.toml'
        pyproject_dest_path = self.meta_repo_path / 'pyproject.toml'
        if not self.dry_run:
            create_file_from_template(pyproject_template_path, pyproject_dest_path, self.replacements, "(pyproject.toml config)")
        
        # Create formatting requirements file
        requirements_template_path = self.templates_dir / 'code-formatting' / 'requirements-formatting.txt'
        requirements_dest_path = self.meta_repo_path / 'requirements-formatting.txt'
        if not self.dry_run:
            create_file_from_template(requirements_template_path, requirements_dest_path, self.replacements, "(formatting requirements)")
        
        # Create setup script
        setup_script_template_path = self.templates_dir / 'code-formatting' / 'setup-formatting.py'
        setup_script_dest_path = scripts_path / 'setup-formatting.py'
        if not self.dry_run:
            create_file_from_template(setup_script_template_path, setup_script_dest_path, self.replacements, "(formatting setup script)")
        
        if not self.dry_run:
            logger.info("✅ Code formatting setup completed successfully!")
            logger.info(f"    📋 Pre-commit config: {precommit_dest_path}")
            logger.info(f"    ⚙️  Project config: {pyproject_dest_path}")
            logger.info(f"    📦 Requirements: {requirements_dest_path}")
            logger.info(f"    🔧 Setup script: {setup_script_dest_path}")
            logger.info("    💡 Run 'python scripts/setup-formatting.py' to configure your environment")

    def create_github_repository_settings(self):
        """Create GitHub Repository Settings as Code for automated governance.
        
        Creates comprehensive GitHub repository automation including:
        - Repository settings configuration for governance and security
        - Branch protection rules for code quality enforcement
        - Standardized labels for issue and PR management
        - Automation scripts for applying settings via GitHub CLI/API
        - GitHub Actions workflow for automated settings application
        """
        if not self.dry_run:
            logger.info("⚙️ Creating GitHub Repository Settings as Code...")
        
        # Ensure .github directory exists
        github_path = self.meta_repo_path / '.github'
        scripts_path = self.meta_repo_path / 'scripts'
        workflows_path = github_path / 'workflows'
        
        if not self.dry_run:
            ensure_directory_exists(github_path, "GitHub configuration directory")
            ensure_directory_exists(scripts_path, "Scripts directory")
            ensure_directory_exists(workflows_path, "GitHub workflows directory")
        
        # Create repository settings configuration
        settings_template_path = self.templates_dir / 'github-settings' / 'repository-settings.yml'
        settings_dest_path = github_path / 'repository-settings.yml'
        if not self.dry_run:
            create_file_from_template(settings_template_path, settings_dest_path, self.replacements, "(repository settings)")
        
        # Create labels configuration
        labels_template_path = self.templates_dir / 'github-settings' / 'labels.yml'
        labels_dest_path = github_path / 'labels.yml'
        if not self.dry_run:
            create_file_from_template(labels_template_path, labels_dest_path, self.replacements, "(repository labels)")
        
        # Create automation script
        script_template_path = self.templates_dir / 'github-settings' / 'apply-github-settings.py'
        script_dest_path = scripts_path / 'apply-github-settings.py'
        if not self.dry_run:
            create_file_from_template(script_template_path, script_dest_path, self.replacements, "(GitHub settings automation)")
        
        # Create GitHub Actions workflow
        workflow_template_path = self.templates_dir / 'github-settings' / 'repository-settings-workflow.yml'
        workflow_dest_path = workflows_path / 'repository-settings.yml'
        if not self.dry_run:
            create_file_from_template(workflow_template_path, workflow_dest_path, self.replacements, "(repository settings workflow)")
        
        if not self.dry_run:
            logger.info("✅ GitHub Repository Settings as Code created successfully!")
            logger.info(f"    ⚙️  Repository settings: {settings_dest_path}")
            logger.info(f"    🏷️  Labels configuration: {labels_dest_path}")
            logger.info(f"    🔧 Automation script: {script_dest_path}")
            logger.info(f"    🤖 GitHub workflow: {workflow_dest_path}")
            logger.info("    💡 Run 'python scripts/apply-github-settings.py' to configure your repository")


# Global logger will be initialized in main()
logger = None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Idempotent repository seeding script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python seeding.py                              # Run with auto-detection
  python seeding.py --dry-run                   # Preview changes without making them  
  python seeding.py --verbose                   # Enable detailed logging
  python seeding.py --project myproj --username johndoe
  
Configuration file examples:
  python seeding.py --save-config myproject.yaml    # Save current settings to config
  python seeding.py --config myproject.yaml         # Load settings from config
  python seeding.py --list-configs                  # List available config files
        """
    )
    
    # Basic options
    parser.add_argument(
        '--project',
        type=str,
        help='Project name (default: auto-detect from directory)'
    )
    
    parser.add_argument(
        '--username', 
        type=str,
        help='GitHub username (default: auto-detect from git config)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without making them'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true', 
        help='Enable verbose logging'
    )
    
    # Configuration file options
    parser.add_argument(
        '--config',
        type=Path,
        help='Load configuration from YAML or JSON file'
    )
    
    parser.add_argument(
        '--save-config',
        type=Path,
        help='Save current configuration to file (supports .yaml, .yml, .json)'
    )
    
    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List available configuration files in current directory'
    )
    
    # Advanced template options
    parser.add_argument(
        '--template-path',
        type=Path,
        help='Custom path to templates directory'
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    global logger
    
    args = parse_arguments()
    logger = setup_logging(args.verbose)
    
    try:
        config = Configuration()
        config_data = None
        
        # Handle list-configs option
        if args.list_configs:
            config_files = config.list_available_configs()
            if config_files:
                logger.info("📋 Available configuration files:")
                for config_file in config_files:
                    try:
                        # Try to load and show basic info
                        temp_config = config.load_config(config_file)
                        project_name = temp_config.get('project_name', 'Unknown')
                        created_at = temp_config.get('created_at', 'Unknown')
                        logger.info(f"  {config_file} - Project: {project_name}, Created: {created_at}")
                    except Exception as e:
                        logger.info(f"  {config_file} - Error reading: {e}")
            else:
                logger.info("No configuration files found in current directory")
            return
        
        # Load configuration if specified
        if args.config:
            if not args.config.exists():
                logger.error(f"Configuration file not found: {args.config}")
                sys.exit(1)
            
            logger.info(f"Loading configuration from {args.config}")
            config_data = config.load_config(args.config)
        
        # Get project configuration (CLI args override config file)
        raw_project_name = args.project or (config.get_project_name() if config_data else None) or get_project_name()
        
        # Sanitize project name for security
        try:
            project_name = sanitize_project_name(raw_project_name)
        except ValueError as e:
            logger.error(f"Invalid project name: {e}")
            sys.exit(1)
        github_username = args.username or (config.get_github_username() if config_data else None) or get_github_username()
        
        # Handle save-config option (save and exit)
        if args.save_config:
            logger.info(f"Saving configuration to {args.save_config}")
            config.save_config(
                args.save_config, 
                project_name, 
                github_username,
                template_path=str(args.template_path) if args.template_path else None
            )
            logger.info("✓ Configuration saved successfully!")
            return
        
        # Initialize and run seeder
        seeder = RepoSeeder(project_name, github_username, args.dry_run, config_data)
        
        # Override template path if specified
        if args.template_path:
            if args.template_path.exists():
                seeder.templates_dir = args.template_path
                logger.info(f"Using custom template path: {args.template_path}")
            else:
                logger.warning(f"Template path does not exist, using default: {seeder.templates_dir}")
        
        seeder.run()
        
        logger.info("✓ Repository seeding completed successfully!")
        if args.dry_run:
            logger.info("This was a dry run - no actual changes were made.")
            logger.info("Run without --dry-run to apply changes.")
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except ImportError as e:
        if "yaml" in str(e).lower():
            logger.error("PyYAML is required for YAML configuration files.")
            logger.error("Install with: pip install pyyaml")
            logger.error("Alternatively, use JSON format for configuration files.")
        else:
            logger.error(f"Import error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



