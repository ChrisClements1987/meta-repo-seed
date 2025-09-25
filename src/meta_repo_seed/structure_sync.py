"""
Structure Synchronization Module for Meta-Repo-Seed

This module provides functionality to synchronize directory structures and files
across repositories, ensuring consistency and automated maintenance of project layouts.

Issue #33: Structure Synchronization Scripts
"""

import hashlib
import json
import logging
import os
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class FileTemplate:
    """Represents a file template for synchronization."""
    path: str
    content: str
    template_vars: Dict[str, Any]
    checksum: Optional[str] = None
    last_updated: Optional[str] = None

    def __post_init__(self):
        if self.checksum is None:
            self.checksum = self._calculate_checksum()
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()

    def _calculate_checksum(self) -> str:
        """Calculate MD5 checksum of the content."""
        return hashlib.md5(self.content.encode()).hexdigest()


@dataclass
class DirectoryStructure:
    """Represents a directory structure for synchronization."""
    name: str
    path: str
    subdirs: List['DirectoryStructure']
    files: List[FileTemplate]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'name': self.name,
            'path': self.path,
            'subdirs': [subdir.to_dict() for subdir in self.subdirs],
            'files': [asdict(file) for file in self.files],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DirectoryStructure':
        """Create from dictionary."""
        subdirs = [cls.from_dict(subdir) for subdir in data.get('subdirs', [])]
        files = [FileTemplate(**file_data) for file_data in data.get('files', [])]
        
        return cls(
            name=data['name'],
            path=data['path'],
            subdirs=subdirs,
            files=files,
            metadata=data.get('metadata', {})
        )


class StructureSynchronizer:
    """Main class for synchronizing repository structures."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "sync_config.yaml"
        self.config = self._load_config()
        self.templates_dir = Path(self.config.get('templates_dir', 'templates'))
        self.output_dir = Path(self.config.get('output_dir', 'output'))
        
    def _load_config(self) -> Dict[str, Any]:
        """Load synchronization configuration."""
        if not os.path.exists(self.config_path):
            # Create default config
            default_config = {
                'templates_dir': 'templates',
                'output_dir': 'output',
                'sync_rules': {
                    'preserve_existing': True,
                    'backup_before_sync': True,
                    'exclude_patterns': ['.git', '__pycache__', '*.pyc']
                },
                'structure_definitions': {}
            }
            self._save_config(default_config)
            return default_config
            
        with open(self.config_path, 'r') as f:
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                return yaml.safe_load(f)
            else:
                return json.load(f)
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            if self.config_path.endswith('.yaml') or self.config_path.endswith('.yml'):
                yaml.safe_dump(config, f, default_flow_style=False)
            else:
                json.dump(config, f, indent=2)

    def scan_structure(self, source_path: str) -> DirectoryStructure:
        """Scan a directory and create a structure definition."""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source path does not exist: {source_path}")
        
        logger.info(f"Scanning structure: {source_path}")
        
        return self._scan_directory(source, source.name)
    
    def _scan_directory(self, path: Path, name: str) -> DirectoryStructure:
        """Recursively scan a directory structure."""
        subdirs = []
        files = []
        
        exclude_patterns = self.config.get('sync_rules', {}).get('exclude_patterns', [])
        
        for item in path.iterdir():
            # Check exclusion patterns
            if any(pattern in item.name for pattern in exclude_patterns):
                continue
                
            if item.is_dir():
                subdirs.append(self._scan_directory(item, item.name))
            elif item.is_file():
                try:
                    with open(item, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    files.append(FileTemplate(
                        path=str(item.relative_to(path.parent)),
                        content=content,
                        template_vars={}
                    ))
                except (UnicodeDecodeError, PermissionError) as e:
                    logger.warning(f"Skipping file {item}: {e}")
        
        return DirectoryStructure(
            name=name,
            path=str(path),
            subdirs=subdirs,
            files=files,
            metadata={
                'scanned_at': datetime.now().isoformat(),
                'total_files': len(files),
                'total_subdirs': len(subdirs)
            }
        )
    
    def save_structure(self, structure: DirectoryStructure, filename: str):
        """Save a structure definition to a file."""
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = self.templates_dir / f"{filename}.json"
        
        with open(output_path, 'w') as f:
            json.dump(structure.to_dict(), f, indent=2)
        
        logger.info(f"Structure saved to: {output_path}")
    
    def load_structure(self, filename: str) -> DirectoryStructure:
        """Load a structure definition from a file."""
        file_path = self.templates_dir / f"{filename}.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Structure file not found: {file_path}")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return DirectoryStructure.from_dict(data)
    
    def sync_structure(self, structure: DirectoryStructure, target_path: str, 
                      template_vars: Optional[Dict[str, str]] = None):
        """Synchronize a structure to a target directory."""
        target = Path(target_path)
        template_vars = template_vars or {}
        
        logger.info(f"Syncing structure to: {target_path}")
        
        # Create backup if configured
        if self.config.get('sync_rules', {}).get('backup_before_sync', False):
            self._create_backup(target)
        
        # Create target directory
        target.mkdir(parents=True, exist_ok=True)
        
        # Sync files
        for file_template in structure.files:
            self._sync_file(file_template, target, template_vars)
        
        # Sync subdirectories
        for subdir in structure.subdirs:
            subdir_path = target / subdir.name
            self.sync_structure(subdir, str(subdir_path), template_vars)
        
        logger.info(f"Structure synchronization completed: {target_path}")
    
    def _sync_file(self, file_template: FileTemplate, target_dir: Path, 
                   template_vars: Dict[str, str]):
        """Sync a single file."""
        target_file = target_dir / Path(file_template.path).name
        
        # Check if file exists and preserve_existing is True
        if (target_file.exists() and 
            self.config.get('sync_rules', {}).get('preserve_existing', True)):
            logger.info(f"Preserving existing file: {target_file}")
            return
        
        # Process template variables
        content = file_template.content
        for var, value in template_vars.items():
            content = content.replace(f"{{{var}}}", value)
        
        # Write file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.debug(f"Synced file: {target_file}")
    
    def _create_backup(self, target: Path):
        """Create a backup of the target directory."""
        if not target.exists():
            return
        
        backup_name = f"{target.name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_path = target.parent / backup_name
        
        shutil.copytree(target, backup_path)
        logger.info(f"Backup created: {backup_path}")
    
    def compare_structures(self, structure1: DirectoryStructure, 
                          structure2: DirectoryStructure) -> Dict[str, Any]:
        """Compare two directory structures."""
        differences = {
            'files_added': [],
            'files_removed': [],
            'files_modified': [],
            'dirs_added': [],
            'dirs_removed': []
        }
        
        # Compare files
        files1 = {f.path: f for f in structure1.files}
        files2 = {f.path: f for f in structure2.files}
        
        for path in files1.keys() - files2.keys():
            differences['files_removed'].append(path)
        
        for path in files2.keys() - files1.keys():
            differences['files_added'].append(path)
        
        for path in files1.keys() & files2.keys():
            if files1[path].checksum != files2[path].checksum:
                differences['files_modified'].append(path)
        
        # Compare directories
        dirs1 = {d.name for d in structure1.subdirs}
        dirs2 = {d.name for d in structure2.subdirs}
        
        differences['dirs_removed'].extend(dirs1 - dirs2)
        differences['dirs_added'].extend(dirs2 - dirs1)
        
        return differences
    
    def list_structures(self) -> List[str]:
        """List available structure templates."""
        if not self.templates_dir.exists():
            return []
        
        return [f.stem for f in self.templates_dir.glob('*.json')]


def main():
    """Main entry point for the structure synchronizer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Structure Synchronization Tool')
    parser.add_argument('command', choices=['scan', 'sync', 'list', 'compare'],
                       help='Command to execute')
    parser.add_argument('--source', help='Source directory to scan')
    parser.add_argument('--target', help='Target directory for sync')
    parser.add_argument('--structure', help='Structure template name')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--vars', help='Template variables (JSON format)')
    
    args = parser.parse_args()
    
    # Initialize synchronizer
    sync = StructureSynchronizer(args.config)
    
    try:
        if args.command == 'scan':
            if not args.source:
                print("Error: --source is required for scan command")
                return 1
            
            structure = sync.scan_structure(args.source)
            structure_name = args.structure or Path(args.source).name
            sync.save_structure(structure, structure_name)
            print(f"Structure '{structure_name}' scanned and saved")
        
        elif args.command == 'sync':
            if not args.structure or not args.target:
                print("Error: --structure and --target are required for sync command")
                return 1
            
            structure = sync.load_structure(args.structure)
            template_vars = json.loads(args.vars) if args.vars else {}
            sync.sync_structure(structure, args.target, template_vars)
            print(f"Structure '{args.structure}' synced to '{args.target}'")
        
        elif args.command == 'list':
            structures = sync.list_structures()
            print("Available structure templates:")
            for s in structures:
                print(f"  - {s}")
        
        elif args.command == 'compare':
            # Implementation for compare command would go here
            print("Compare command not yet implemented")
        
        return 0
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == '__main__':
    exit(main())