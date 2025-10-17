#!/bin/bash
# Workspace Setup Script - Ensures consistent environment across all workspaces

set -e

echo "Setting up workspace..."

# 1. Validate Python version
if [ -f .python-version ]; then
    REQUIRED_VERSION=$(cat .python-version)
    CURRENT_VERSION=$(python --version | cut -d' ' -f2)
    
    if [ "$CURRENT_VERSION" != "$REQUIRED_VERSION" ]; then
        echo "[WARN] Python version mismatch: $CURRENT_VERSION != $REQUIRED_VERSION"
        echo "Consider using pyenv or update .python-version"
    fi
fi

# 2. Install dependencies
echo "Installing dependencies..."
pip install -r requirements-test.txt

# 3. Validate environment
echo "Validating environment..."
python scripts/validate-environment.py

# 4. Install pre-commit hooks
if [ ! -f .git/hooks/pre-commit ]; then
    echo "Installing pre-commit hooks..."
    if [ -f .git/hooks/pre-commit.sample ]; then
        cp .git/hooks/pre-commit .git/hooks/pre-commit 2>/dev/null || true
    fi
    chmod +x .git/hooks/pre-commit 2>/dev/null || true
fi

# 5. Verify Git config
if [ -z "$(git config user.name)" ]; then
    echo "[WARN] Git user.name not set. Run: git config user.name 'Your Name'"
fi

if [ -z "$(git config user.email)" ]; then
    echo "[WARN] Git user.email not set. Run: git config user.email 'your@email.com'"
fi

echo ""
echo "[SUCCESS] Workspace setup complete!"
echo "Run 'python scripts/validate-environment.py' anytime to verify environment"
