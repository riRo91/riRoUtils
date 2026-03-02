# Set Up an Isolated GitHub Environment for a Project

## Description

Creates a fully isolated GitHub environment for any project, ensuring that SSH keys, `gh` CLI credentials, and git identity are scoped exclusively to the project directory. This prevents credential leakage to other projects, agents, or global configurations on the same machine.

## Trigger

Use this skill when the user:
- Asks to set up GitHub for a new or existing project with environment isolation
- Wants project-local SSH keys, git identity, or `gh` CLI configuration
- Says "isolate GitHub", "set up GitHub for this project", "project-scoped git", or similar
- Needs to clone a private repo with a dedicated SSH key
- Wants to prevent one project's credentials from affecting another

## Procedure

### Step 0 — Gather Information

Ask the user for the following:
- **Flow type**: "clone existing repo" or "init new repo"
- **Repository URL or name** (e.g., `git@github.com:org/repo.git` or `org/repo`)
- **Project directory path** (where the project lives or should be created)
- **Git user name** (for commits)
- **Git email** (for commits)
- **SSH key**: generate a new one, or path to an existing key to copy
- **GitHub account** (if the machine has multiple `gh` accounts, clarify which one)
- **Repo visibility** (if creating new: `private` or `public`)

### Step 1 — Initialize the Repository

**Flow A — Clone existing repo:**
```bash
git clone <REPO_URL> <PROJECT_DIR>
cd <PROJECT_DIR>
```

**Flow B — Init new repo:**
```bash
mkdir -p <PROJECT_DIR>
cd <PROJECT_DIR>
git init
```

### Step 2 — Set Up Project-Local SSH Key

Create the `.ssh/` directory inside the project:
```bash
mkdir -p <PROJECT_DIR>/.ssh
chmod 700 <PROJECT_DIR>/.ssh
```

**If generating a new key:**
```bash
ssh-keygen -t ed25519 -C "<GIT_EMAIL>" -f <PROJECT_DIR>/.ssh/id_ed25519 -N ""
chmod 600 <PROJECT_DIR>/.ssh/id_ed25519
chmod 644 <PROJECT_DIR>/.ssh/id_ed25519.pub
```

**If copying an existing key:**
```bash
cp <SOURCE_KEY_PATH> <PROJECT_DIR>/.ssh/id_ed25519
cp <SOURCE_KEY_PATH>.pub <PROJECT_DIR>/.ssh/id_ed25519.pub
chmod 600 <PROJECT_DIR>/.ssh/id_ed25519
chmod 644 <PROJECT_DIR>/.ssh/id_ed25519.pub
```

Display the public key and instruct the user to add it as a deploy key or SSH key on GitHub:
```bash
cat <PROJECT_DIR>/.ssh/id_ed25519.pub
```

### Step 3 — Configure Git to Use Only the Project-Local Key

```bash
cd <PROJECT_DIR>
git config core.sshCommand "ssh -i <PROJECT_DIR>/.ssh/id_ed25519 -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new"
```

This ensures that git operations in this repo never use `~/.ssh/` keys or the SSH agent. The `IdentitiesOnly=yes` flag is critical: without it, the SSH client may try keys from the agent first, potentially authenticating as the wrong account.

### Step 4 — Configure Local Git Identity

```bash
cd <PROJECT_DIR>
git config user.name "<GIT_USER_NAME>"
git config user.email "<GIT_EMAIL>"
```

Verify that these are set locally (not globally) by checking:
```bash
git config --local --list | grep user
```

### Step 5 — Set Up Project-Scoped `gh` CLI Configuration

Create a project-local `gh` config directory:
```bash
mkdir -p <PROJECT_DIR>/.gh
```

Create the `.envrc` file for automatic environment activation:
```bash
cat > <PROJECT_DIR>/.envrc << 'ENVRC'
# Project-scoped gh CLI configuration
# Ensures `gh` commands in this directory use the project's own GitHub credentials
export GH_CONFIG_DIR="${PWD}/.gh"
ENVRC
```

If the user has `direnv` installed, allow the `.envrc`:
```bash
direnv allow <PROJECT_DIR>
```

If `direnv` is not installed, inform the user they must manually source the file:
```bash
source <PROJECT_DIR>/.envrc
```

Mention that `direnv` is recommended for automatic activation (`brew install direnv` on macOS, with the appropriate shell hook).

### Step 6 — Create the GitHub Auth Setup Script

```bash
mkdir -p <PROJECT_DIR>/scripts
cat > <PROJECT_DIR>/scripts/setup-github.sh << 'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

export GH_CONFIG_DIR="${PROJECT_DIR}/.gh"

echo "=== GitHub Authentication Setup ==="
echo "Config directory: ${GH_CONFIG_DIR}"
echo ""
echo "This will authenticate the gh CLI for this project only."
echo "Other projects and global gh config will not be affected."
echo ""

gh auth login --git-protocol ssh

echo ""
echo "Authentication complete. Config stored in: ${GH_CONFIG_DIR}"
echo "Verify with: gh auth status"
SCRIPT
chmod +x <PROJECT_DIR>/scripts/setup-github.sh
```

### Step 7 — Update `.gitignore`

Append the isolation directories to `.gitignore` (create the file if it does not exist). Only add entries that are not already present:

```
# Project-local secrets (GitHub isolation)
.ssh/
.gh/
.envrc
```

Note: `.envrc` is included in `.gitignore` because it is a local environment file. If the team wants to share it, remove it from `.gitignore` and commit it (it contains no secrets, only a path reference).

### Step 8 — Set the Remote (if applicable)

**Flow A — Clone:** The remote is already configured. Update it if needed to use SSH:
```bash
git remote set-url origin git@github.com:<ORG>/<REPO>.git
```

**Flow B — Init new repo + create remote:**

Ensure the `.envrc` is sourced so `gh` uses the project-scoped config:
```bash
source <PROJECT_DIR>/.envrc
```

Then create the remote:
```bash
gh repo create <ORG>/<REPO> --<VISIBILITY> --source=<PROJECT_DIR> --remote=origin
```

If the repo already exists on GitHub but no remote is set:
```bash
git remote add origin git@github.com:<ORG>/<REPO>.git
```

### Step 9 — Verify the Setup

Run these verification checks:

```bash
cd <PROJECT_DIR>

# 1. Verify SSH key is project-local
git config core.sshCommand
# Should show the path to .ssh/id_ed25519 inside the project

# 2. Verify git identity is local
git config user.email
git config user.name

# 3. Verify gh config is scoped
echo $GH_CONFIG_DIR
# Should point to <PROJECT_DIR>/.gh

# 4. Test SSH connectivity (after adding the key to GitHub)
ssh -i .ssh/id_ed25519 -o IdentitiesOnly=yes -T git@github.com 2>&1 || true
# Should greet the correct GitHub user

# 5. Test gh auth (after running setup-github.sh)
gh auth status
```

### Step 10 — Inform the User About Remaining Manual Steps

Tell the user what they still need to do:
1. **Add the SSH public key to GitHub** — as a deploy key (repo-level) or SSH key (account-level)
2. **Run `scripts/setup-github.sh`** — to authenticate the `gh` CLI under the scoped config
3. **Install `direnv`** (if not already installed) — for automatic `.envrc` activation
4. **First push** — `git push -u origin main` (or the appropriate branch)

## Output

After completing the procedure, provide a summary including:
- Full path to the project directory
- SSH key location and fingerprint
- Git identity configured (name and email)
- Remote URL
- List of files created or modified (`.ssh/`, `.gh/`, `.envrc`, `scripts/setup-github.sh`, `.gitignore`)
- Any remaining manual steps the user must complete
- A reminder that `.ssh/` and `.gh/` must never be committed (they are in `.gitignore`)
