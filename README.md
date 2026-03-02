# riRoUtils

Reusable AI-agent skills, scripts, and utilities for project bootstrapping, documentation, debugging, and workflow automation.

## What This Is

A curated collection of generic, project-agnostic skills and rules designed for use with AI coding agents (Claude Code and Cursor). Each skill is a battle-tested procedure distilled from real engineering sessions, scrubbed of project-specific details, and packaged for immediate reuse.

## Repository Structure

```
riRoUtils/
├── AGENT.md                  # Instructions for AI agents working on this repo
├── README.md                 # This file
├── .claude/
│   └── skills/               # Claude Code skills (.md)
├── .cursor/
│   └── rules/                # Cursor rules (.mdc) — mirrors of Claude skills
├── docs/                     # Detailed documentation for each skill
├── scripts/                  # Executable utility scripts
│   └── setup-github.sh       # Project-scoped GitHub CLI setup
├── .envrc                    # direnv config for GitHub isolation
└── .gitignore
```

## Skills Catalog

| # | Skill | Description |
|---|-------|-------------|
| 1 | **GitHub Isolation Setup** | Create a fully isolated GitHub environment for any project — project-local SSH keys, scoped `gh` CLI, no credential leakage |
| 2 | **Post-Implementation Documentation** | Scan a full conversation session and extract comprehensive documentation: component inventory, relationships, mermaid diagrams, project structure |
| 3 | **Debugging RCA Report** | After a debugging session, systematically explore the system, identify root cause, suggest fixes, implement the chosen solution, and produce a detailed report |
| 4 | **Mirror Agent Rules** | Sync skills/rules between `.claude/skills/` (.md) and `.cursor/rules/` (.mdc) to keep both agent environments consistent |
| 5 | **Scaffold Project Structure** | Bootstrap a new project with a standardized layout: AGENT.md, README, .claude/, .cursor/, docs/, scripts/, and all config files |
| 6 | **Conversation-to-Memory** | Extract key learnings, patterns, and decisions from a session and persist them to structured memory files for future context |
| 7 | **Visualize Architecture** | Scan a codebase and produce mermaid diagrams of its architecture, component relationships, data flow, and directory structure |

## How to Use

### Copy a skill into your project

Claude Code:
```bash
cp riRoUtils/.claude/skills/<skill-name>.md /path/to/your/project/.claude/skills/
```

Cursor:
```bash
cp riRoUtils/.cursor/rules/<skill-name>.mdc /path/to/your/project/.cursor/rules/
```

### Use the GitHub isolation script directly

```bash
# Clone or create a new repo with full isolation
# See docs/github-isolation-setup.md for details
bash riRoUtils/scripts/setup-github.sh
```

## Design Principles

- **Generic** — No project-specific identifiers; every skill works with any codebase
- **Dual-format** — Each skill exists as both a Claude skill (.md) and a Cursor rule (.mdc)
- **Self-documenting** — Skills include trigger conditions, step-by-step procedures, and expected outputs
- **Context-efficient** — Designed to give AI agents maximum understanding with minimum token usage
- **Battle-tested** — Each skill originates from a real engineering workflow that proved effective

## GitHub Isolation

This project uses scoped credentials that never touch your global git/GitHub config:

- **SSH**: Project-local key in `.ssh/` with `core.sshCommand` in `.git/config`
- **gh CLI**: Project-local config via `GH_CONFIG_DIR` in `.envrc`
- **Secrets**: `.ssh/` and `.gh/` are gitignored

To set up gh auth for this project:
```bash
bash scripts/setup-github.sh
```

## License

MIT
