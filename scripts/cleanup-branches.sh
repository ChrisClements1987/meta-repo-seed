#!/bin/bash
#
# Branch Cleanup Script for Meta-Repo-Seed
# 
# This script helps clean up merged branches both locally and remotely.
# 
# Usage:
#   ./scripts/cleanup-branches.sh [options]
#
# Options:
#   --dry-run    Show what would be deleted without actually deleting
#   --local      Clean up local branches only
#   --remote     Clean up remote branches only
#   --help       Show this help message
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default options
DRY_RUN=false
LOCAL_ONLY=false
REMOTE_ONLY=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --local)
            LOCAL_ONLY=true
            shift
            ;;
        --remote)
            REMOTE_ONLY=true
            shift
            ;;
        --help)
            echo "Branch Cleanup Script for Meta-Repo-Seed"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --dry-run    Show what would be deleted without actually deleting"
            echo "  --local      Clean up local branches only"
            echo "  --remote     Clean up remote branches only"
            echo "  --help       Show this help message"
            echo ""
            echo "This script will:"
            echo "1. Remove local branches that have been merged into develop"
            echo "2. Remove remote feature branches that have been merged"
            echo "3. Prune remote-tracking branches"
            echo ""
            echo "Protected branches: main, develop, HEAD"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${GREEN}🧹 Meta-Repo-Seed Branch Cleanup${NC}"
echo "================================================"

# Function to log actions
log_action() {
    if [ "$DRY_RUN" = true ]; then
        echo -e "${YELLOW}[DRY-RUN]${NC} $1"
    else
        echo -e "${GREEN}[ACTION]${NC} $1"
    fi
}

# Function to clean up local merged branches
cleanup_local_branches() {
    echo ""
    echo -e "${GREEN}📍 Cleaning up local merged branches${NC}"
    echo "------------------------------------------------"
    
    # Get list of local branches merged into develop (excluding main, develop, and current branch)
    merged_branches=$(git branch --merged develop | grep -v -E "(main|develop|\*)" | sed 's/^[ \t]*//' || true)
    
    if [ -z "$merged_branches" ]; then
        echo "No local merged branches to clean up."
        return
    fi
    
    echo "Found merged local branches:"
    echo "$merged_branches"
    echo ""
    
    # Delete each merged branch
    for branch in $merged_branches; do
        if [ "$DRY_RUN" = true ]; then
            log_action "Would delete local branch: $branch"
        else
            log_action "Deleting local branch: $branch"
            git branch -d "$branch" || git branch -D "$branch"
        fi
    done
}

# Function to clean up remote merged branches
cleanup_remote_branches() {
    echo ""
    echo -e "${GREEN}🌐 Cleaning up remote merged branches${NC}"
    echo "------------------------------------------------"
    
    # Check if gh CLI is available
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}GitHub CLI (gh) not found. Skipping remote branch cleanup.${NC}"
        return
    fi
    
    # Get list of merged PRs and their branch names
    merged_prs=$(gh pr list --state merged --json headRefName --jq '.[].headRefName' | grep -E "^(feature/|fix/|feat/|hotfix/)" || true)
    
    if [ -z "$merged_prs" ]; then
        echo "No remote merged feature branches to clean up."
        return
    fi
    
    echo "Found merged remote branches:"
    echo "$merged_prs"
    echo ""
    
    # Delete each merged remote branch (only if auto-delete didn't work)
    for branch in $merged_prs; do
        # Check if branch still exists remotely
        if git ls-remote --heads origin "$branch" | grep -q "$branch"; then
            if [ "$DRY_RUN" = true ]; then
                log_action "Would delete remote branch: $branch"
            else
                log_action "Deleting remote branch: $branch"
                gh api -X DELETE "repos/$(gh repo view --json nameWithOwner --jq '.nameWithOwner')/git/refs/heads/$branch" || echo "Failed to delete $branch (may not exist)"
            fi
        else
            echo "Remote branch $branch already deleted (auto-cleanup worked)"
        fi
    done
}

# Function to prune remote-tracking branches
prune_remote_branches() {
    echo ""
    echo -e "${GREEN}🔄 Pruning remote-tracking branches${NC}"
    echo "------------------------------------------------"
    
    if [ "$DRY_RUN" = true ]; then
        log_action "Would prune remote-tracking branches"
        git remote prune origin --dry-run
    else
        log_action "Pruning remote-tracking branches"
        git remote prune origin
    fi
}

# Main execution
echo "Current branch: $(git branch --show-current)"
echo "Repository: $(git remote get-url origin)"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}🚨 DRY RUN MODE - No changes will be made${NC}"
fi

# Execute cleanup based on options
if [ "$REMOTE_ONLY" = true ]; then
    cleanup_remote_branches
    prune_remote_branches
elif [ "$LOCAL_ONLY" = true ]; then
    cleanup_local_branches
else
    # Clean up both local and remote
    cleanup_local_branches
    cleanup_remote_branches
    prune_remote_branches
fi

echo ""
echo -e "${GREEN}✅ Branch cleanup complete!${NC}"
echo ""
echo "Current branches:"
git branch -a
