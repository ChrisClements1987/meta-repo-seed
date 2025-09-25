"""
Organization Blueprint Orchestrator

Orchestrates the deployment of complete organizational infrastructures based on 
organization blueprints. Handles multi-repository creation, team setup, environment
configuration, and governance policy deployment.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import time

# Add the root directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import blueprint parser from the same package
sys.path.insert(0, str(Path(__file__).parent))
from parser import OrganizationBlueprint, RepositoryConfig, EnvironmentConfig
from seeding import setup_logging


class DeploymentStatus(Enum):
    """Deployment status for tracking progress."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DeploymentTask:
    """Individual deployment task."""
    name: str
    type: str  # repository, team, environment, policy, etc.
    dependencies: List[str]
    config: Dict[str, Any]
    status: DeploymentStatus = DeploymentStatus.PENDING
    error_message: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None

    @property
    def duration(self) -> Optional[float]:
        """Get task duration in seconds."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class DeploymentPlan:
    """Complete deployment plan with ordered tasks."""
    blueprint: OrganizationBlueprint
    tasks: List[DeploymentTask]
    estimated_duration_minutes: int

    def get_tasks_by_status(self, status: DeploymentStatus) -> List[DeploymentTask]:
        """Get tasks filtered by status."""
        return [task for task in self.tasks if task.status == status]

    def get_ready_tasks(self) -> List[DeploymentTask]:
        """Get tasks that are ready to execute (dependencies completed)."""
        ready_tasks = []
        completed_task_names = {task.name for task in self.get_tasks_by_status(DeploymentStatus.COMPLETED)}
        
        for task in self.get_tasks_by_status(DeploymentStatus.PENDING):
            if all(dep in completed_task_names for dep in task.dependencies):
                ready_tasks.append(task)
        
        return ready_tasks


class GitHubProvider:
    """GitHub API provider for repository and organization management."""
    
    def __init__(self, token: Optional[str] = None, dry_run: bool = False):
        """
        Initialize GitHub provider.
        
        Args:
            token: GitHub personal access token or None for dry-run
            dry_run: If True, simulate operations without making actual API calls
        """
        self.token = token
        self.dry_run = dry_run
        self.logger = logging.getLogger(f"{__name__}.GitHubProvider")
        
        if not dry_run and not token:
            self.logger.warning("No GitHub token provided - operations will be simulated")
            self.dry_run = True

    async def create_repository(self, org: str, repo_config: RepositoryConfig) -> bool:
        """
        Create a GitHub repository.
        
        Args:
            org: GitHub organization name
            repo_config: Repository configuration
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would create repository {org}/{repo_config.name}")
            self.logger.info(f"  Visibility: {repo_config.visibility}")
            self.logger.info(f"  Features: {', '.join(repo_config.features)}")
            if repo_config.protection.get('enabled'):
                self.logger.info(f"  Branch protection: {repo_config.protection}")
            await asyncio.sleep(0.5)  # Simulate API delay
            return True
        
        # TODO: Implement actual GitHub API calls
        self.logger.info(f"Creating repository {org}/{repo_config.name}")
        return True

    async def create_team(self, org: str, team_name: str, role: str, members: List[str]) -> bool:
        """
        Create a GitHub team.
        
        Args:
            org: GitHub organization name
            team_name: Team name
            role: Team role/permission level
            members: List of member usernames
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would create team {org}/{team_name}")
            self.logger.info(f"  Role: {role}")
            self.logger.info(f"  Members: {', '.join(members)}")
            await asyncio.sleep(0.3)
            return True
        
        # TODO: Implement actual GitHub API calls
        self.logger.info(f"Creating team {org}/{team_name}")
        return True

    async def setup_environment(self, org: str, repo: str, env_config: EnvironmentConfig) -> bool:
        """
        Setup GitHub environment with protection rules.
        
        Args:
            org: GitHub organization name
            repo: Repository name
            env_config: Environment configuration
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would setup environment {env_config.name} for {org}/{repo}")
            self.logger.info(f"  Type: {env_config.type}")
            if env_config.deployment_target:
                self.logger.info(f"  Deployment: {env_config.deployment_target}")
            if env_config.protection:
                self.logger.info(f"  Protection: {env_config.protection}")
            await asyncio.sleep(0.2)
            return True
        
        # TODO: Implement actual GitHub API calls
        self.logger.info(f"Setting up environment {env_config.name} for {org}/{repo}")
        return True

    async def apply_branch_protection(self, org: str, repo: str, protection_config: Dict[str, Any]) -> bool:
        """
        Apply branch protection rules.
        
        Args:
            org: GitHub organization name
            repo: Repository name
            protection_config: Branch protection configuration
            
        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            self.logger.info(f"DRY RUN: Would apply branch protection to {org}/{repo}")
            self.logger.info(f"  Config: {protection_config}")
            await asyncio.sleep(0.2)
            return True
        
        # TODO: Implement actual GitHub API calls
        self.logger.info(f"Applying branch protection to {org}/{repo}")
        return True


class OrganizationOrchestrator:
    """Orchestrates complete organizational infrastructure deployment."""
    
    def __init__(self, github_provider: GitHubProvider, dry_run: bool = False):
        """
        Initialize orchestrator.
        
        Args:
            github_provider: GitHub API provider
            dry_run: If True, simulate deployment without making changes
        """
        self.github = github_provider
        self.dry_run = dry_run
        self.logger = logging.getLogger(f"{__name__}.OrganizationOrchestrator")

    def create_deployment_plan(self, blueprint: OrganizationBlueprint) -> DeploymentPlan:
        """
        Create deployment plan from organization blueprint.
        
        Args:
            blueprint: Organization blueprint to deploy
            
        Returns:
            Complete deployment plan with ordered tasks
        """
        self.logger.info(f"Creating deployment plan for: {blueprint.metadata.name}")
        
        tasks = []
        
        # 1. Organization setup tasks
        org_name = blueprint.providers.vcs.get('organization') if blueprint.providers else blueprint.metadata.name
        
        # 2. Team creation tasks (no dependencies)
        for team in blueprint.organization.teams:
            tasks.append(DeploymentTask(
                name=f"team-{team.name}",
                type="team",
                dependencies=[],
                config={
                    'org': org_name,
                    'team_name': team.name,
                    'role': team.role,
                    'members': team.members
                }
            ))
        
        # 3. Repository creation tasks (depend on teams)
        team_dependencies = [f"team-{team.name}" for team in blueprint.organization.teams]
        
        # Get deployment order
        from parser import BlueprintParser
        parser = BlueprintParser()
        deployment_order = parser.get_deployment_order(blueprint)
        
        for repo_name in deployment_order:
            # Find the repository config
            repo_config = None
            for repo in blueprint.get_all_repositories():
                if repo.name == repo_name:
                    repo_config = repo
                    break
            
            if repo_config:
                tasks.append(DeploymentTask(
                    name=f"repo-{repo_name}",
                    type="repository",
                    dependencies=team_dependencies,
                    config={
                        'org': org_name,
                        'repo_config': repo_config
                    }
                ))
        
        # 4. Environment setup tasks (depend on repositories)
        for portfolio in blueprint.portfolios:
            for env in portfolio.environments:
                # Find which repositories this environment applies to
                for repo in portfolio.repositories:
                    tasks.append(DeploymentTask(
                        name=f"env-{repo.name}-{env.name}",
                        type="environment",
                        dependencies=[f"repo-{repo.name}"],
                        config={
                            'org': org_name,
                            'repo': repo.name,
                            'env_config': env
                        }
                    ))
        
        # 5. Branch protection tasks (depend on repositories)
        for repo in blueprint.get_all_repositories():
            if repo.protection.get('enabled', True):
                tasks.append(DeploymentTask(
                    name=f"protection-{repo.name}",
                    type="branch_protection",
                    dependencies=[f"repo-{repo.name}"],
                    config={
                        'org': org_name,
                        'repo': repo.name,
                        'protection_config': repo.protection
                    }
                ))
        
        # 6. Governance policy tasks (depend on all repositories)
        if blueprint.governance and blueprint.governance.policies:
            repo_dependencies = [f"repo-{repo.name}" for repo in blueprint.get_all_repositories()]
            tasks.append(DeploymentTask(
                name="governance-policies",
                type="governance",
                dependencies=repo_dependencies,
                config={
                    'org': org_name,
                    'policies': blueprint.governance.policies
                }
            ))
        
        # Estimate deployment duration (rough estimate)
        estimated_minutes = max(10, len(tasks) * 2)  # At least 10 minutes, 2 minutes per task
        
        self.logger.info(f"Deployment plan created: {len(tasks)} tasks, ~{estimated_minutes} minutes")
        
        return DeploymentPlan(
            blueprint=blueprint,
            tasks=tasks,
            estimated_duration_minutes=estimated_minutes
        )

    async def execute_task(self, task: DeploymentTask) -> bool:
        """
        Execute individual deployment task.
        
        Args:
            task: Task to execute
            
        Returns:
            True if successful, False otherwise
        """
        self.logger.info(f"Executing task: {task.name} ({task.type})")
        
        task.status = DeploymentStatus.IN_PROGRESS
        task.start_time = time.time()
        
        try:
            success = False
            
            if task.type == "team":
                success = await self.github.create_team(
                    task.config['org'],
                    task.config['team_name'],
                    task.config['role'],
                    task.config['members']
                )
            
            elif task.type == "repository":
                success = await self.github.create_repository(
                    task.config['org'],
                    task.config['repo_config']
                )
            
            elif task.type == "environment":
                success = await self.github.setup_environment(
                    task.config['org'],
                    task.config['repo'],
                    task.config['env_config']
                )
            
            elif task.type == "branch_protection":
                success = await self.github.apply_branch_protection(
                    task.config['org'],
                    task.config['repo'],
                    task.config['protection_config']
                )
            
            elif task.type == "governance":
                # TODO: Implement governance policy deployment
                if self.dry_run:
                    self.logger.info(f"DRY RUN: Would deploy governance policies")
                    success = True
                else:
                    self.logger.info("Deploying governance policies")
                    success = True
            
            else:
                self.logger.error(f"Unknown task type: {task.type}")
                success = False
            
            task.status = DeploymentStatus.COMPLETED if success else DeploymentStatus.FAILED
            if not success:
                task.error_message = f"Task execution failed for type: {task.type}"
            
        except Exception as e:
            self.logger.error(f"Task {task.name} failed: {e}")
            task.status = DeploymentStatus.FAILED
            task.error_message = str(e)
            success = False
        
        finally:
            task.end_time = time.time()
        
        duration = task.duration
        status_symbol = "✓" if success else "✗"
        self.logger.info(f"{status_symbol} Task {task.name} {task.status.value} ({duration:.1f}s)")
        
        return success

    async def deploy_organization(self, blueprint: OrganizationBlueprint) -> Tuple[bool, Dict[str, Any]]:
        """
        Deploy complete organizational infrastructure.
        
        Args:
            blueprint: Organization blueprint to deploy
            
        Returns:
            Tuple of (success, deployment_report)
        """
        start_time = time.time()
        self.logger.info(f"Starting organizational deployment: {blueprint.metadata.name}")
        self.logger.info(f"Business Profile: {blueprint.metadata.business_profile}")
        
        # Create deployment plan
        plan = self.create_deployment_plan(blueprint)
        
        self.logger.info(f"Executing deployment plan: {len(plan.tasks)} tasks")
        self.logger.info(f"Estimated duration: {plan.estimated_duration_minutes} minutes")
        
        # Execute tasks in dependency order
        while plan.get_tasks_by_status(DeploymentStatus.PENDING):
            ready_tasks = plan.get_ready_tasks()
            
            if not ready_tasks:
                # Check if we're stuck due to failed dependencies
                failed_tasks = plan.get_tasks_by_status(DeploymentStatus.FAILED)
                if failed_tasks:
                    self.logger.error("Deployment blocked by failed tasks:")
                    for task in failed_tasks:
                        self.logger.error(f"  - {task.name}: {task.error_message}")
                    break
                else:
                    # No ready tasks but no failures - shouldn't happen
                    self.logger.error("No ready tasks found but no failures - dependency issue?")
                    break
            
            # Execute ready tasks (could be parallelized in the future)
            for task in ready_tasks:
                await self.execute_task(task)
        
        # Generate deployment report
        end_time = time.time()
        duration_minutes = (end_time - start_time) / 60
        
        completed_tasks = plan.get_tasks_by_status(DeploymentStatus.COMPLETED)
        failed_tasks = plan.get_tasks_by_status(DeploymentStatus.FAILED)
        
        success = len(failed_tasks) == 0
        
        report = {
            'organization': blueprint.metadata.name,
            'business_profile': blueprint.metadata.business_profile,
            'success': success,
            'duration_minutes': duration_minutes,
            'tasks_total': len(plan.tasks),
            'tasks_completed': len(completed_tasks),
            'tasks_failed': len(failed_tasks),
            'repositories_created': len([t for t in completed_tasks if t.type == 'repository']),
            'teams_created': len([t for t in completed_tasks if t.type == 'team']),
            'environments_configured': len([t for t in completed_tasks if t.type == 'environment']),
            'failed_tasks': [{'name': t.name, 'error': t.error_message} for t in failed_tasks],
            'deployment_order': [t.name for t in completed_tasks if t.type == 'repository']
        }
        
        if success:
            self.logger.info(f"✓ Organization deployment completed successfully in {duration_minutes:.1f} minutes")
            self.logger.info(f"  - {report['repositories_created']} repositories created")
            self.logger.info(f"  - {report['teams_created']} teams created")
            self.logger.info(f"  - {report['environments_configured']} environments configured")
        else:
            self.logger.error(f"✗ Organization deployment failed after {duration_minutes:.1f} minutes")
            self.logger.error(f"  - {len(failed_tasks)} tasks failed")
        
        return success, report


# Integration with CLI commands
async def deploy_business_from_profile(profile_name: str, org_name: str, dry_run: bool = True) -> Tuple[bool, Dict[str, Any]]:
    """
    Deploy business infrastructure from profile name.
    
    Args:
        profile_name: Business profile (startup-basic, charity-nonprofit, etc.)
        org_name: Organization name for deployment
        dry_run: If True, simulate deployment
        
    Returns:
        Tuple of (success, deployment_report)
    """
    logger = logging.getLogger(f"{__name__}.deploy_business_from_profile")
    
    # Load blueprint template for profile
    examples_dir = Path(__file__).parent.parent.parent / "examples" / "blueprints"
    blueprint_file = examples_dir / f"{profile_name}.yaml"
    
    if not blueprint_file.exists():
        logger.error(f"Blueprint template not found for profile: {profile_name}")
        return False, {'error': f'Blueprint template not found: {profile_name}'}
    
    # Parse blueprint
    from parser import BlueprintParser
    parser = BlueprintParser()
    
    try:
        blueprint = parser.parse_file(blueprint_file)
        logger.info(f"Loaded blueprint template: {blueprint.metadata.name}")
        
        # Customize blueprint for organization
        blueprint.metadata.name = org_name
        if blueprint.providers and blueprint.providers.vcs:
            blueprint.providers.vcs['organization'] = org_name
        
    except Exception as e:
        logger.error(f"Failed to parse blueprint: {e}")
        return False, {'error': f'Blueprint parsing failed: {e}'}
    
    # Create orchestrator
    github_provider = GitHubProvider(dry_run=dry_run)
    orchestrator = OrganizationOrchestrator(github_provider, dry_run=dry_run)
    
    # Deploy organization
    return await orchestrator.deploy_organization(blueprint)


if __name__ == '__main__':
    # Test the orchestrator
    import asyncio
    
    async def test_deployment():
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        
        print("=== Testing Organization Deployment ===")
        success, report = await deploy_business_from_profile(
            profile_name='startup-basic',
            org_name='test-startup',
            dry_run=True
        )
        
        print(f"\nDeployment Success: {success}")
        print(f"Duration: {report.get('duration_minutes', 0):.1f} minutes")
        print(f"Repositories: {report.get('repositories_created', 0)}")
        print(f"Teams: {report.get('teams_created', 0)}")
        print(f"Environments: {report.get('environments_configured', 0)}")
        
        if not success:
            print("Failed tasks:")
            for task in report.get('failed_tasks', []):
                print(f"  - {task['name']}: {task['error']}")
    
    asyncio.run(test_deployment())
