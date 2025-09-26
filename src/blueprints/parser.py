"""
Organization Blueprint Parser

Parses and validates organization blueprint YAML files for Business-in-a-Box deployment.
Provides structured data models for multi-tier organizational architecture.
"""

import json
import logging
# Add the root directory to path for imports
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import jsonschema
import yaml
from jsonschema import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


@dataclass
class RepositoryConfig:
    """Repository configuration within a blueprint."""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    template: Optional[str] = None
    visibility: str = "private"
    features: List[str] = field(default_factory=list)
    protection: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RepositoryConfig':
        """Create RepositoryConfig from dictionary."""
        return cls(
            name=data['name'],
            display_name=data.get('displayName'),
            description=data.get('description'),
            template=data.get('template'),
            visibility=data.get('visibility', 'private'),
            features=data.get('features', []),
            protection=data.get('protection', {})
        )


@dataclass
class EnvironmentConfig:
    """Environment configuration for deployments."""
    name: str
    type: str
    deployment_target: Dict[str, Any] = field(default_factory=dict)
    secrets: List[Dict[str, Any]] = field(default_factory=list)
    protection: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EnvironmentConfig':
        """Create EnvironmentConfig from dictionary."""
        return cls(
            name=data['name'],
            type=data['type'],
            deployment_target=data.get('deploymentTarget', {}),
            secrets=data.get('secrets', []),
            protection=data.get('protection', {})
        )


@dataclass
class PortfolioConfig:
    """Portfolio configuration within an organization."""
    name: str
    type: str
    description: Optional[str] = None
    repositories: List[RepositoryConfig] = field(default_factory=list)
    environments: List[EnvironmentConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PortfolioConfig':
        """Create PortfolioConfig from dictionary."""
        repositories = [
            RepositoryConfig.from_dict(repo) 
            for repo in data.get('repositories', [])
        ]
        environments = [
            EnvironmentConfig.from_dict(env) 
            for env in data.get('environments', [])
        ]
        
        return cls(
            name=data['name'],
            type=data['type'],
            description=data.get('description'),
            repositories=repositories,
            environments=environments
        )


@dataclass
class TeamConfig:
    """Team configuration and permissions."""
    name: str
    role: str
    members: List[str] = field(default_factory=list)
    repositories: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TeamConfig':
        """Create TeamConfig from dictionary."""
        return cls(
            name=data['name'],
            role=data['role'],
            members=data.get('members', []),
            repositories=data.get('repositories', [])
        )


@dataclass
class GovernanceConfig:
    """Governance and compliance configuration."""
    policies: List[Dict[str, Any]] = field(default_factory=list)
    compliance: Dict[str, Any] = field(default_factory=dict)
    templates: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GovernanceConfig':
        """Create GovernanceConfig from dictionary."""
        return cls(
            policies=data.get('policies', []),
            compliance=data.get('compliance', {}),
            templates=data.get('templates', {})
        )


@dataclass
class ProvidersConfig:
    """External service provider configurations."""
    vcs: Dict[str, Any] = field(default_factory=dict)
    cicd: Dict[str, Any] = field(default_factory=dict)
    paas: Dict[str, Any] = field(default_factory=dict)
    secrets: Dict[str, Any] = field(default_factory=dict)
    observability: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProvidersConfig':
        """Create ProvidersConfig from dictionary."""
        return cls(
            vcs=data.get('vcs', {}),
            cicd=data.get('cicd', {}),
            paas=data.get('paas', {}),
            secrets=data.get('secrets', {}),
            observability=data.get('observability', {})
        )


@dataclass
class OrganizationStructure:
    """Core organization structure definition."""
    meta_repo: Optional[RepositoryConfig] = None
    platform_services: Optional[RepositoryConfig] = None
    cloud_storage: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrganizationStructure':
        """Create OrganizationStructure from dictionary."""
        meta_repo = None
        if 'metaRepo' in data:
            meta_repo = RepositoryConfig.from_dict(data['metaRepo'])
            
        platform_services = None
        if 'platformServices' in data:
            platform_services = RepositoryConfig.from_dict(data['platformServices'])
        
        return cls(
            meta_repo=meta_repo,
            platform_services=platform_services,
            cloud_storage=data.get('cloudStorage', {})
        )


@dataclass
class OrganizationSpec:
    """Complete organization specification."""
    structure: OrganizationStructure
    teams: List[TeamConfig] = field(default_factory=list)
    settings: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrganizationSpec':
        """Create OrganizationSpec from dictionary."""
        structure = OrganizationStructure.from_dict(data.get('structure', {}))
        teams = [TeamConfig.from_dict(team) for team in data.get('teams', [])]
        
        return cls(
            structure=structure,
            teams=teams,
            settings=data.get('settings', {})
        )


@dataclass
class BlueprintMetadata:
    """Blueprint metadata and business profile information."""
    name: str
    display_name: Optional[str] = None
    description: Optional[str] = None
    business_profile: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BlueprintMetadata':
        """Create BlueprintMetadata from dictionary."""
        return cls(
            name=data['name'],
            display_name=data.get('displayName'),
            description=data.get('description'),
            business_profile=data.get('businessProfile'),
            tags=data.get('tags', [])
        )


@dataclass
class OrganizationBlueprint:
    """Complete organization blueprint definition."""
    api_version: str
    kind: str
    metadata: BlueprintMetadata
    organization: OrganizationSpec
    portfolios: List[PortfolioConfig] = field(default_factory=list)
    governance: Optional[GovernanceConfig] = None
    providers: Optional[ProvidersConfig] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrganizationBlueprint':
        """Create OrganizationBlueprint from dictionary."""
        spec = data['spec']
        
        metadata = BlueprintMetadata.from_dict(data['metadata'])
        organization = OrganizationSpec.from_dict(spec['organization'])
        portfolios = [
            PortfolioConfig.from_dict(portfolio) 
            for portfolio in spec.get('portfolios', [])
        ]
        
        governance = None
        if 'governance' in spec:
            governance = GovernanceConfig.from_dict(spec['governance'])
        
        providers = None
        if 'providers' in spec:
            providers = ProvidersConfig.from_dict(spec['providers'])
        
        return cls(
            api_version=data['apiVersion'],
            kind=data['kind'],
            metadata=metadata,
            organization=organization,
            portfolios=portfolios,
            governance=governance,
            providers=providers
        )

    def get_all_repositories(self) -> List[RepositoryConfig]:
        """Get all repositories across organization and portfolios."""
        repositories = []
        
        # Add organization-level repositories
        if self.organization.structure.meta_repo:
            repositories.append(self.organization.structure.meta_repo)
        
        if self.organization.structure.platform_services:
            repositories.append(self.organization.structure.platform_services)
        
        # Add portfolio repositories
        for portfolio in self.portfolios:
            repositories.extend(portfolio.repositories)
        
        return repositories

    def get_all_environments(self) -> List[EnvironmentConfig]:
        """Get all environments across all portfolios."""
        environments = []
        for portfolio in self.portfolios:
            environments.extend(portfolio.environments)
        return environments

    def get_repositories_by_portfolio(self, portfolio_name: str) -> List[RepositoryConfig]:
        """Get repositories for a specific portfolio."""
        for portfolio in self.portfolios:
            if portfolio.name == portfolio_name:
                return portfolio.repositories
        return []


class BlueprintParser:
    """Parser for organization blueprint YAML files."""

    def __init__(self, schema_path: Optional[Path] = None):
        """
        Initialize blueprint parser.
        
        Args:
            schema_path: Path to the JSON schema file for validation
        """
        self.logger = logging.getLogger(__name__)
        
        # Load schema for validation
        if schema_path is None:
            schema_path = Path(__file__).parent.parent.parent / "schemas" / "organization-blueprint-v1.json"
        
        self.schema = None
        if schema_path.exists():
            try:
                with open(schema_path, 'r') as f:
                    self.schema = json.load(f)
                self.logger.debug(f"Loaded blueprint schema from {schema_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load schema from {schema_path}: {e}")
        else:
            self.logger.warning(f"Schema file not found: {schema_path}")

    def parse_file(self, blueprint_path: Union[str, Path]) -> OrganizationBlueprint:
        """
        Parse organization blueprint from YAML file.
        
        Args:
            blueprint_path: Path to the blueprint YAML file
            
        Returns:
            Parsed OrganizationBlueprint object
            
        Raises:
            FileNotFoundError: If blueprint file doesn't exist
            yaml.YAMLError: If YAML parsing fails
            ValidationError: If blueprint doesn't match schema
            ValueError: If blueprint structure is invalid
        """
        blueprint_path = Path(blueprint_path)
        
        if not blueprint_path.exists():
            raise FileNotFoundError(f"Blueprint file not found: {blueprint_path}")
        
        self.logger.info(f"Parsing organization blueprint: {blueprint_path}")
        
        # Load and parse YAML
        try:
            with open(blueprint_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML from {blueprint_path}: {e}")
        
        if not data:
            raise ValueError(f"Empty or invalid YAML file: {blueprint_path}")
        
        # Validate against schema if available
        if self.schema:
            try:
                jsonschema.validate(data, self.schema)
                self.logger.debug("Blueprint passed schema validation")
            except ValidationError as e:
                raise ValidationError(f"Blueprint validation failed: {e.message}")
        
        # Parse into structured data
        try:
            blueprint = OrganizationBlueprint.from_dict(data)
            self.logger.info(f"Successfully parsed blueprint: {blueprint.metadata.name}")
            return blueprint
        except KeyError as e:
            raise ValueError(f"Missing required field in blueprint: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse blueprint structure: {e}")

    def parse_yaml(self, yaml_content: str) -> OrganizationBlueprint:
        """
        Parse organization blueprint from YAML string.
        
        Args:
            yaml_content: YAML content as string
            
        Returns:
            Parsed OrganizationBlueprint object
        """
        try:
            data = yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Failed to parse YAML content: {e}")
        
        if self.schema:
            try:
                jsonschema.validate(data, self.schema)
            except ValidationError as e:
                raise ValidationError(f"Blueprint validation failed: {e.message}")
        
        return OrganizationBlueprint.from_dict(data)

    def validate_blueprint(self, blueprint: OrganizationBlueprint) -> List[str]:
        """
        Validate blueprint for business deployment readiness.
        
        Args:
            blueprint: Parsed blueprint to validate
            
        Returns:
            List of validation warnings/issues
        """
        warnings = []
        
        # Check for required business profile
        if not blueprint.metadata.business_profile:
            warnings.append("No business profile specified - consider adding businessProfile")
        
        # Validate repository names for DNS safety
        for repo in blueprint.get_all_repositories():
            if not repo.name.replace('-', '').replace('_', '').isalnum():
                warnings.append(f"Repository name may not be DNS-safe: {repo.name}")
        
        # Check for production environment protection
        prod_envs = [env for env in blueprint.get_all_environments() if env.type == 'production']
        for env in prod_envs:
            if not env.protection.get('requiredReviewers'):
                warnings.append(f"Production environment '{env.name}' has no required reviewers")
        
        # Validate team permissions
        if not blueprint.organization.teams:
            warnings.append("No teams defined - consider adding team structure")
        
        # Check provider configuration
        if blueprint.providers:
            if not blueprint.providers.vcs.get('organization'):
                warnings.append("No GitHub organization specified in VCS provider")
        
        return warnings

    def get_deployment_order(self, blueprint: OrganizationBlueprint) -> List[str]:
        """
        Determine the correct deployment order for repositories.
        
        Args:
            blueprint: Parsed blueprint
            
        Returns:
            List of repository names in deployment order
        """
        deployment_order = []
        
        # 1. Meta repo first (governance and automation)
        if blueprint.organization.structure.meta_repo:
            deployment_order.append(blueprint.organization.structure.meta_repo.name)
        
        # 2. Platform services (shared infrastructure)
        if blueprint.organization.structure.platform_services:
            deployment_order.append(blueprint.organization.structure.platform_services.name)
        
        # 3. Portfolio repositories (products and services)
        for portfolio in blueprint.portfolios:
            for repo in portfolio.repositories:
                deployment_order.append(repo.name)
        
        return deployment_order


def load_example_blueprints() -> Dict[str, OrganizationBlueprint]:
    """Load all example blueprints for testing and demonstration."""
    examples_dir = Path(__file__).parent.parent.parent / "examples" / "blueprints"
    parser = BlueprintParser()
    blueprints = {}
    
    if examples_dir.exists():
        for blueprint_file in examples_dir.glob("*.yaml"):
            try:
                blueprint = parser.parse_file(blueprint_file)
                blueprints[blueprint_file.stem] = blueprint
            except Exception as e:
                logging.warning(f"Failed to load example blueprint {blueprint_file}: {e}")
    
    return blueprints


if __name__ == '__main__':
    # Test the parser with example blueprint
    logging.basicConfig(level=logging.INFO)
    
    examples_dir = Path(__file__).parent.parent.parent / "examples" / "blueprints"
    startup_blueprint = examples_dir / "startup-basic.yaml"
    
    if startup_blueprint.exists():
        parser = BlueprintParser()
        try:
            blueprint = parser.parse_file(startup_blueprint)
            print(f"SUCCESS: Successfully parsed blueprint: {blueprint.metadata.name}")
            print(f"   Business Profile: {blueprint.metadata.business_profile}")
            print(f"   Repositories: {len(blueprint.get_all_repositories())}")
            print(f"   Portfolios: {len(blueprint.portfolios)}")
            print(f"   Teams: {len(blueprint.organization.teams)}")
            
            warnings = parser.validate_blueprint(blueprint)
            if warnings:
                print(f"WARNING: Validation warnings:")
                for warning in warnings:
                    print(f"   - {warning}")
            else:
                print("SUCCESS: No validation warnings")
                
            deployment_order = parser.get_deployment_order(blueprint)
            print(f"DEPLOYMENT ORDER: {' -> '.join(deployment_order)}")
            
        except Exception as e:
            print(f"ERROR: Failed to parse blueprint: {e}")
    else:
        print(f"ERROR: Example blueprint not found: {startup_blueprint}")
