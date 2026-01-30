#!/usr/bin/env bash
# Setup git hooks for svg-matrix Python wrapper
#
# Usage: ./scripts/setup-hooks.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
HOOKS_DIR="$PROJECT_DIR/.git/hooks"

echo "Setting up git hooks for svg-matrix Python wrapper..."

# Handle submodule case where .git is a file pointing to the actual git dir
if [ -f "$PROJECT_DIR/.git" ]; then
    # This is a submodule
    GIT_DIR=$(cat "$PROJECT_DIR/.git" | sed 's/gitdir: //')
    if [[ "$GIT_DIR" != /* ]]; then
        # Relative path
        GIT_DIR="$PROJECT_DIR/$GIT_DIR"
    fi
    HOOKS_DIR="$GIT_DIR/hooks"
fi

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Copy pre-push hook
cp "$SCRIPT_DIR/pre-push" "$HOOKS_DIR/pre-push"
chmod +x "$HOOKS_DIR/pre-push"

echo "✓ Installed pre-push hook to $HOOKS_DIR/pre-push"
echo ""
echo "The hook will run automatically before each 'git push' and check:"
echo "  - Code formatting (ruff format)"
echo "  - Linting (ruff check)"
echo "  - Type checking (mypy)"
echo "  - Security (bandit)"
echo "  - Tests (pytest)"
echo "  - Build (uv build)"
echo ""
echo "To bypass the hook in emergencies: git push --no-verify"
