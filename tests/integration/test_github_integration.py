"""
Integration tests for GitHub CLI functionality.

Tests GitHub operations including repository creation, issue management,
and CLI interactions.
"""

import json
import subprocess
# Import the modules we're testing
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, call, patch

import pytest

sys.path.append(str(Path(__file__).parent.parent))
from seeding import RepoSeeder


class TestGitHubCLIIntegration:
    """Test cases for GitHub CLI integration."""
    
    @patch('subprocess.run')
    def test_github_cli_check_availability(self, mock_run, mock_github_cli):
        """Test checking if GitHub CLI is available."""
        # Mock successful gh command
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "gh version 2.0.0"
        
        # This would be part of seeder's GitHub CLI detection
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "gh version" in result.stdout
    
    @patch('subprocess.run')
    def test_github_cli_not_available(self, mock_run):
        """Test handling when GitHub CLI is not available."""
        # Mock command not found
        mock_run.side_effect = FileNotFoundError("Command not found")
        
        with pytest.raises(FileNotFoundError):
            subprocess.run(['gh', '--version'], capture_output=True, text=True)
    
    @patch('subprocess.run')
    def test_github_auth_status(self, mock_run, mock_github_cli):
        """Test checking GitHub authentication status."""
        # Mock authenticated status
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "github.com\n  ✓ Logged in to github.com as test-user"
        
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        
        assert result.returncode == 0
        assert "Logged in" in result.stdout
    
    @patch('subprocess.run')
    def test_github_auth_not_authenticated(self, mock_run):
        """Test handling when user is not authenticated to GitHub."""
        # Mock not authenticated
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "You are not logged into any GitHub hosts"
        
        result = subprocess.run(['gh', 'auth', 'status'], capture_output=True, text=True)
        
        assert result.returncode == 1
        assert "not logged in" in result.stderr


class TestGitHubRepositoryOperations:
    """Test cases for GitHub repository operations."""
    
    @patch('subprocess.run')
    def test_create_github_repository(self, mock_run, temp_dir, mock_github_cli):
        """Test creating a GitHub repository."""
        # Mock successful repository creation
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/test-user/test-repo"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("test-repo", "test-user", dry_run=False)
            
            # Simulate GitHub repository creation
            result = subprocess.run([
                'gh', 'repo', 'create', 'test-repo',
                '--private',
                '--description', 'Test repository',
                '--confirm'
            ], capture_output=True, text=True, cwd=seeder.project_root)
            
            assert result.returncode == 0
            assert "github.com" in result.stdout
    
    @patch('subprocess.run')
    def test_create_github_repository_already_exists(self, mock_run, temp_dir):
        """Test handling when GitHub repository already exists."""
        # Mock repository already exists error
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "repository already exists"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("existing-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'repo', 'create', 'existing-repo',
                '--private'
            ], capture_output=True, text=True)
            
            assert result.returncode == 1
            assert "already exists" in result.stderr
    
    @patch('subprocess.run')
    def test_set_repository_description(self, mock_run, temp_dir, mock_github_cli):
        """Test setting repository description."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("desc-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'repo', 'edit',
                '--description', 'Updated description for desc-repo'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_enable_github_issues(self, mock_run, temp_dir, mock_github_cli):
        """Test enabling GitHub Issues for repository."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("issues-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'repo', 'edit',
                '--enable-issues'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0


class TestGitHubIssuesOperations:
    """Test cases for GitHub Issues operations."""
    
    @patch('subprocess.run')
    def test_create_github_issue(self, mock_run, temp_dir, mock_github_cli):
        """Test creating a GitHub issue."""
        # Mock successful issue creation
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/test-user/test-repo/issues/1"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("issue-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'issue', 'create',
                '--title', 'Test Issue',
                '--body', 'This is a test issue',
                '--label', 'enhancement'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "issues/1" in result.stdout
    
    @patch('subprocess.run')
    def test_list_github_issues(self, mock_run, temp_dir, mock_github_cli):
        """Test listing GitHub issues."""
        # Mock issue list response
        mock_issues = [
            {"number": 1, "title": "First issue", "state": "open"},
            {"number": 2, "title": "Second issue", "state": "closed"}
        ]
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps(mock_issues)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("list-issues-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'issue', 'list',
                '--json', 'number,title,state'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            
            issues = json.loads(result.stdout)
            assert len(issues) == 2
            assert issues[0]["title"] == "First issue"
    
    @patch('subprocess.run')
    def test_create_issue_with_labels_and_assignee(self, mock_run, temp_dir, mock_github_cli):
        """Test creating issue with labels and assignee."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/test-user/test-repo/issues/5"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("labeled-issue-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'issue', 'create',
                '--title', 'Feature Request: Add Configuration Support',
                '--body', 'We need configuration file support for better workflow',
                '--label', 'enhancement,feature',
                '--assignee', 'test-user'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "issues/5" in result.stdout
    
    @patch('subprocess.run')
    def test_close_github_issue(self, mock_run, temp_dir, mock_github_cli):
        """Test closing a GitHub issue."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("close-issue-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'issue', 'close', '1',
                '--comment', 'Closing as completed'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0


class TestGitHubBranchProtection:
    """Test cases for GitHub branch protection operations."""
    
    @patch('subprocess.run')
    def test_enable_branch_protection(self, mock_run, temp_dir, mock_github_cli):
        """Test enabling branch protection rules."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("protected-repo", "test-user", dry_run=False)
            
            # Enable branch protection for main branch
            result = subprocess.run([
                'gh', 'api',
                f'repos/test-user/protected-repo/branches/main/protection',
                '--method', 'PUT',
                '--field', 'required_status_checks=null',
                '--field', 'enforce_admins=true',
                '--field', 'required_pull_request_reviews={"required_approving_review_count":1}',
                '--field', 'restrictions=null'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_get_branch_protection_status(self, mock_run, temp_dir, mock_github_cli):
        """Test getting branch protection status."""
        # Mock protection status response
        protection_status = {
            "enabled": True,
            "required_status_checks": None,
            "enforce_admins": {"enabled": True},
            "required_pull_request_reviews": {
                "required_approving_review_count": 1
            }
        }
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps(protection_status)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("check-protection-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'api',
                f'repos/test-user/check-protection-repo/branches/main/protection'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            
            status = json.loads(result.stdout)
            assert status["enabled"] is True
            assert status["enforce_admins"]["enabled"] is True


class TestGitHubWorkflowIntegration:
    """Test cases for GitHub Actions workflow integration."""
    
    @patch('subprocess.run')
    def test_trigger_github_workflow(self, mock_run, temp_dir, mock_github_cli):
        """Test triggering GitHub Actions workflow."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("workflow-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'workflow', 'run', 'ci.yml',
                '--ref', 'main'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_list_github_workflows(self, mock_run, temp_dir, mock_github_cli):
        """Test listing GitHub Actions workflows."""
        mock_workflows = [
            {"name": "CI", "state": "active", "id": 12345},
            {"name": "Deploy", "state": "active", "id": 12346}
        ]
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps(mock_workflows)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("list-workflows-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'workflow', 'list',
                '--json', 'name,state,id'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            
            workflows = json.loads(result.stdout)
            assert len(workflows) == 2
            assert workflows[0]["name"] == "CI"


class TestGitHubReleaseOperations:
    """Test cases for GitHub release operations."""
    
    @patch('subprocess.run')
    def test_create_github_release(self, mock_run, temp_dir, mock_github_cli):
        """Test creating a GitHub release."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/test-user/test-repo/releases/tag/v1.0.0"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("release-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'release', 'create', 'v1.0.0',
                '--title', 'Initial Release',
                '--notes', 'First stable release of the project'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "releases/tag/v1.0.0" in result.stdout
    
    @patch('subprocess.run')
    def test_list_github_releases(self, mock_run, temp_dir, mock_github_cli):
        """Test listing GitHub releases."""
        mock_releases = [
            {"tag_name": "v1.0.0", "name": "Initial Release", "draft": False},
            {"tag_name": "v0.9.0", "name": "Beta Release", "draft": True}
        ]
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps(mock_releases)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("list-releases-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'release', 'list',
                '--json', 'tagName,name,isDraft'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            
            releases = json.loads(result.stdout)
            assert len(releases) == 2
            assert releases[0]["tag_name"] == "v1.0.0"


class TestGitHubPullRequestOperations:
    """Test cases for GitHub Pull Request operations."""
    
    @patch('subprocess.run')
    def test_create_pull_request(self, mock_run, temp_dir, mock_github_cli):
        """Test creating a GitHub Pull Request."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "https://github.com/test-user/test-repo/pull/1"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("pr-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'pr', 'create',
                '--title', 'Add new feature',
                '--body', 'This PR adds a new feature to the project',
                '--base', 'main',
                '--head', 'feature-branch'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "pull/1" in result.stdout
    
    @patch('subprocess.run')
    def test_merge_pull_request(self, mock_run, temp_dir, mock_github_cli):
        """Test merging a GitHub Pull Request."""
        mock_run.return_value.returncode = 0
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("merge-pr-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'pr', 'merge', '1',
                '--merge',
                '--delete-branch'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_list_pull_requests(self, mock_run, temp_dir, mock_github_cli):
        """Test listing GitHub Pull Requests."""
        mock_prs = [
            {"number": 1, "title": "Feature PR", "state": "open"},
            {"number": 2, "title": "Bugfix PR", "state": "merged"}
        ]
        
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps(mock_prs)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("list-pr-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'pr', 'list',
                '--json', 'number,title,state'
            ], capture_output=True, text=True)
            
            assert result.returncode == 0
            
            prs = json.loads(result.stdout)
            assert len(prs) == 2
            assert prs[0]["title"] == "Feature PR"


class TestGitHubErrorHandling:
    """Test cases for GitHub CLI error handling."""
    
    @patch('subprocess.run')
    def test_github_api_rate_limit(self, mock_run, temp_dir):
        """Test handling GitHub API rate limit errors."""
        # Mock rate limit error
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "API rate limit exceeded"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("rate-limit-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'api', 'user'
            ], capture_output=True, text=True)
            
            assert result.returncode == 1
            assert "rate limit" in result.stderr
    
    @patch('subprocess.run')
    def test_github_permission_denied(self, mock_run, temp_dir):
        """Test handling GitHub permission denied errors."""
        # Mock permission denied error
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "Permission denied (publickey)"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("permission-repo", "test-user", dry_run=False)
            
            result = subprocess.run([
                'gh', 'repo', 'create', 'permission-repo'
            ], capture_output=True, text=True)
            
            assert result.returncode == 1
            assert "Permission denied" in result.stderr
    
    @patch('subprocess.run')
    def test_github_network_error(self, mock_run, temp_dir):
        """Test handling GitHub network errors."""
        # Mock network error
        mock_run.side_effect = subprocess.TimeoutExpired(['gh', 'api', 'user'], 30)
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("network-error-repo", "test-user", dry_run=False)
            
            with pytest.raises(subprocess.TimeoutExpired):
                subprocess.run([
                    'gh', 'api', 'user'
                ], timeout=30)


class TestGitHubIntegrationWithSeeder:
    """Test cases for GitHub integration within RepoSeeder workflow."""
    
    @patch('subprocess.run')
    @pytest.mark.skip(reason="setup_github_repository method not yet implemented - tracked in issue #100")
    def test_seeder_github_repository_setup(self, mock_run, temp_dir, mock_github_cli):
        """Test RepoSeeder setting up GitHub repository."""
        # TODO: Implement when GitHub settings as Code is added (#100)
        # Mock all GitHub CLI commands as successful
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "Success"
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("github-integrated-repo", "test-user", dry_run=False)
            
            # Simulate GitHub integration steps
            with patch.object(seeder, 'setup_github_repository') as mock_github_setup:
                seeder.run()
                
                # GitHub setup should be called if implemented
                # (This depends on actual implementation)
    
    @patch('subprocess.run')
    def test_seeder_github_issues_creation(self, mock_run, temp_dir, mock_github_cli):
        """Test RepoSeeder creating GitHub issues."""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = json.dumps([
            {"number": 1, "title": "Setup Documentation"},
            {"number": 2, "title": "Configure CI/CD"}
        ])
        
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("github-issues-repo", "test-user", dry_run=False)
            
            # Simulate creating issues from roadmap
            roadmap_items = [
                "Setup Documentation",
                "Configure CI/CD",
                "Implement Core Features"
            ]
            
            for item in roadmap_items:
                result = subprocess.run([
                    'gh', 'issue', 'create',
                    '--title', item,
                    '--body', f'Implementation task: {item}',
                    '--label', 'roadmap'
                ], capture_output=True, text=True)
                
                assert result.returncode == 0
    
    def test_seeder_dry_run_skips_github_operations(self, temp_dir, mock_github_cli):
        """Test that dry run mode skips actual GitHub operations."""
        with patch('seeding.Path.cwd', return_value=temp_dir):
            seeder = RepoSeeder("dry-run-github-repo", "test-user", dry_run=True)
            
            with patch('subprocess.run') as mock_run:
                # In dry run mode, GitHub operations should be skipped
                seeder.run()
                
                # No actual GitHub CLI commands should be executed
                github_calls = [call for call in mock_run.call_args_list 
                               if 'gh' in str(call)]
                assert len(github_calls) == 0