# riRoUtils

Reusable AI-agent skills, scripts, and utilities for project bootstrapping, documentation, debugging, and workflow automation.

## What This Is

A curated collection of generic, project-agnostic skills, agents, and rules designed for use with AI coding agents (Claude Code and Cursor). Each skill is a battle-tested procedure distilled from real engineering sessions, scrubbed of project-specific details, and packaged for immediate reuse. Agents compose skills into specialized roles that can be dispatched as a dev support team.

## Repository Structure

```
riRoUtils/
├── AGENT.md                  # Instructions for AI agents working on this repo
├── README.md                 # This file
├── .claude/
│   ├── skills/               # Claude Code skills (.md)
│   ├── agents/               # Agent definitions (.md with YAML frontmatter)
│   └── team.md               # Team coordination manifest
├── .cursor/
│   └── rules/                # Cursor rules (.mdc) — mirrors of Claude skills
├── docs/                     # Detailed documentation
│   ├── team-workflows.md     # Multi-agent workflow guide
│   └── session-rewind.md     # Session rewind usage guide
├── scripts/                  # Executable utility scripts
│   ├── setup-github.sh       # Project-scoped GitHub CLI setup
│   └── session-rewind.py     # Session rewind script
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
| 7 | **Visualize Architecture** | Scan a codebase and produce mermaid diagrams of its architecture, component relationships, data flow, directory structure, and pipeline DAGs |
| 8 | **Scaffold Microservice** | Generate a full microservice project with standardized lifecycle (batch job, long-running service, or CLI tool), config validation, Dockerfile, and tests |
| 9 | **Message Queue Patterns** | Design message queue topologies, exchange/queue layouts, dead-letter handling, message envelope schemas, RPC request-reply, and retry policies |
| 10 | **Database Metadata Patterns** | Implement database metadata storage with connection pooling, scoped CRUD, batch operations, flexible schemas, index strategies, and init scripts |
| 11 | **Pipeline DAG Definition** | Design and validate pipeline definitions as DAGs with step dependencies, conditions, resource specs, timeouts, retries, and interactive design workflow |
| 12 | **Review Code Compliance** | Review code against project conventions using a configurable PASS/FAIL checklist covering lifecycle, messaging, storage, security, and containerization |
| 13 | **Session Rewind** | Recover pre-compression context from Claude Code sessions — inspect rewind points and create truncated copies to resume from any earlier message |

## Agents

Specialized agents that compose skills into focused roles. Each agent is defined in `.claude/agents/` with YAML frontmatter specifying its role, tools, and skills.

| Agent | Role | Model | Skills Used |
|-------|------|-------|-------------|
| **project-architect** | Bootstrap projects, design structure, set up isolation | opus | scaffold-project-structure, github-isolation-setup, scaffold-microservice |
| **documentarian** | Extract docs, generate diagrams, persist knowledge | opus | post-implementation-docs, visualize-architecture, conversation-to-memory |
| **debugger** | Systematic debugging, RCA, fix proposals | opus | debugging-rca-report |
| **infra-engineer** | K8s, MQ, databases, pipeline DAGs | opus | message-queue-patterns, database-metadata-patterns, pipeline-dag-definition |
| **code-reviewer** | Review conventions, sync rules | sonnet | review-code-compliance, mirror-agent-rules |

See `.claude/team.md` for dispatch rules and `docs/team-workflows.md` for composition chains.

## Team Workflows

Agents can be composed into multi-step workflows:

- **Build & Document** — project-architect → *(implement)* → documentarian
- **Debug & Fix** — debugger → *(fix)* → code-reviewer → documentarian
- **Infrastructure Setup** — infra-engineer → project-architect → code-reviewer
- **Full Project Bootstrap** — project-architect → infra-engineer → project-architect → documentarian
- **Code Quality Pass** — code-reviewer → *(fix)* → code-reviewer → documentarian

See `docs/team-workflows.md` for detailed step-by-step guides with examples.

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

### Copy an agent into your project

```bash
cp riRoUtils/.claude/agents/<agent-name>.md /path/to/your/project/.claude/agents/
```

### Copy the team manifest

```bash
cp riRoUtils/.claude/team.md /path/to/your/project/.claude/team.md
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
- **Composable** — Skills are building blocks; agents compose them into specialized roles

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
