#!/usr/bin/env bash
#
# One-time GitHub CLI setup for this project.
# Authenticates gh under a project-local config so it never
# touches the machine-wide gh credentials.
#
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export GH_CONFIG_DIR="${PROJECT_DIR}/.gh"

mkdir -p "$GH_CONFIG_DIR"

echo "==> Project-scoped GitHub CLI setup"
echo "    GH_CONFIG_DIR=${GH_CONFIG_DIR}"
echo ""

if gh auth status &>/dev/null; then
    echo "Already authenticated:"
    gh auth status
else
    echo "Log in with your GitHub account."
    echo ""
    echo "If browser auth fails, select 'Paste an authentication token' and"
    echo "create one at: https://github.com/settings/tokens"
    echo "(scopes needed: repo, read:org)"
    echo ""
    gh auth login -h github.com -p https
fi

echo ""
echo "==> Done. To activate this environment in any shell, run:"
echo "    source ${PROJECT_DIR}/.envrc"
