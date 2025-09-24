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
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import tempfile


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def get_project_name() -> str:
    """Get the project name from the current directory name."""
    current_dir = Path.cwd()
    # If we're in meta-repo-seed, go up one level
    if current_dir.name == 'meta-repo-seed':
        project_name = current_dir.parent.name
    else:
        project_name = current_dir.name
    
    logger.info(f"Detected project name: {project_name}")
    return project_name


def get_github_username() -> str:
    """Get GitHub username from git config or prompt user."""
    try:
        # Try to get from git config
        result = subprocess.run(
            ['git', 'config', '--global', 'user.name'],
            capture_output=True,
            text=True,
            check=True
        )
        username = result.stdout.strip()
        if username:
            logger.info(f"Detected GitHub username from git config: {username}")
            return username
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("Could not detect GitHub username from git config")
    
    # Fallback to user input
    username = input("Please enter your GitHub username: ").strip()
    if not username:
        raise ValueError("GitHub username is required")
    
    return username


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
        shutil.copy2(source, destination)
        logger.info(f"Copied template file: {destination} {description}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy {source} to {destination}: {e}")
        raise


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
        # Read template content
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace placeholders
        for placeholder, value in replacements.items():
            content = content.replace(f"{{{{{placeholder}}}}}", value)
        
        # Ensure destination directory exists
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Write processed content to destination
        with open(destination, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created file from template: {destination} {description}")
        return True
    except Exception as e:
        logger.error(f"Failed to create {destination} from template {template_path}: {e}")
        raise


class RepoSeeder:
    """Main class for seeding repository structure."""
    
    def __init__(self, project_name: str, github_username: str, dry_run: bool = False):
        self.project_name = project_name
        self.github_username = github_username
        self.dry_run = dry_run
        self.base_path = Path.cwd().parent if Path.cwd().name == 'meta-repo-seed' else Path.cwd()
        self.project_root = self.base_path / project_name
        self.meta_repo_path = self.project_root / 'meta-repo'
        self.cloud_storage_path = self.project_root / 'cloud-storage'
        self.template_path = Path.cwd()  # Current directory contains templates
        self.templates_dir = self.template_path / 'templates'
        
        # Template replacements dictionary
        self.replacements = {
            'PROJECT_NAME': project_name,
            'GITHUB_USERNAME': github_username,
            'CURRENT_DATE': '2025-09-24',
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
            os.chdir(repo_path)
            subprocess.run(['git', 'init'], check=True, capture_output=True)
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
            "created_date": "2025-09-24",
            "version": "1.0.0",
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
            "$schema": "http://json-schema.org/draft-07/schema#",
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
Initial commit script to create the initial structure of the repo 
based on governance/structure/structure.json
"""

import json
import logging
from pathlib import Path


def main():
    """Initialize repository structure based on structure.json."""
    print(f"Initializing repository structure...")
    # TODO: Implementation needed
    

if __name__ == "__main__":
    main()
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


# Global logger will be initialized in main()
logger = None


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Idempotent repository seeding script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python seeding.py                    # Run with auto-detection
  python seeding.py --dry-run         # Preview changes without making them  
  python seeding.py --verbose         # Enable detailed logging
  python seeding.py --project myproj --username johndoe
        """
    )
    
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
    
    return parser.parse_args()


def main():
    """Main entry point."""
    global logger
    
    args = parse_arguments()
    logger = setup_logging(args.verbose)
    
    try:
        # Get project configuration
        project_name = args.project or get_project_name()
        github_username = args.username or get_github_username()
        
        # Initialize and run seeder
        seeder = RepoSeeder(project_name, github_username, args.dry_run)
        seeder.run()
        
        logger.info("✓ Repository seeding completed successfully!")
        if args.dry_run:
            logger.info("This was a dry run - no actual changes were made.")
            logger.info("Run without --dry-run to apply changes.")
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



