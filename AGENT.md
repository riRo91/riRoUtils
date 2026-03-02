# AGENT.md — riRoUtils

Instructions for AI agents (Claude Code, Cursor, or any LLM-based tool) working on this repository.

## Project Purpose

This is a **utility repository** — a collection of reusable, generic skills, agents, rules, scripts, and documentation templates for AI-assisted software engineering workflows. It does not contain application code.

## Repository Layout

```
riRoUtils/
├── AGENT.md                  # You are here — read this first
├── README.md                 # Human-facing project overview
├── .claude/
│   ├── skills/               # Claude Code skills (.md format)
│   ├── agents/               # Agent definitions (.md with YAML frontmatter)
│   └── team.md               # Team coordination manifest
├── .cursor/rules/            # Cursor rules (.mdc format) — mirrors of Claude skills
├── docs/                     # Detailed documentation
│   └── team-workflows.md     # Multi-agent workflow guide
├── scripts/                  # Executable utility scripts
├── .envrc                    # GitHub isolation (GH_CONFIG_DIR)
└── .gitignore
```

## Key Conventions

### Dual-Format Skills
Every skill exists in two identical-content formats:
- `.claude/skills/<name>.md` — Claude Code format
- `.cursor/rules/<name>.mdc` — Cursor format (with YAML frontmatter)

When creating or modifying a skill, **always update both files**. Use the `mirror-agent-rules` skill to automate this.

### Skill File Structure (Claude .md)
```markdown
# Skill Name

## Trigger
When to activate this skill (natural language conditions).

## Procedure
Step-by-step instructions the agent should follow.

## Output
What the skill produces (files, reports, diagrams, etc.).
```

### Rule File Structure (Cursor .mdc)
```markdown
---
description: One-line description for Cursor's rule matching
globs:
alwaysApply: false
---

# Rule Name

(Same content as the Claude skill)
```

### Agent File Structure (`.claude/agents/<name>.md`)

Agent definitions use YAML frontmatter to declare metadata, followed by a markdown system prompt:

```markdown
---
name: agent-name
role: Brief description of the agent's role
model: opus | sonnet | haiku (optional, defaults to opus)
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
skills:
  - skill-name-1
  - skill-name-2
---

# Agent Display Name

System prompt describing the agent's behavior, when to use it,
how it works, and its boundaries.
```

**Frontmatter fields:**
- `name` (required): kebab-case identifier, matches the filename
- `role` (required): one-line description of what this agent does
- `model` (optional): which model to use (defaults to opus)
- `tools` (required): list of tools the agent is allowed to use
- `skills` (required): list of skills the agent references

### Team Manifest (`.claude/team.md`)

The team manifest is a coordination document that describes:
- **Team Roster** — table of all agents with roles, tools, model, and when to use
- **Dispatch Rules** — signal → agent mapping for routing requests
- **Composition Chains** — multi-agent workflows for common scenarios
- **Escalation** — what to do when a subagent gets stuck

### Naming Conventions
- Skill/rule files: `kebab-case.md` / `kebab-case.mdc`
- Agent files: `kebab-case.md` in `.claude/agents/`
- Documentation files: `kebab-case.md` in `docs/`
- Scripts: `kebab-case.sh` in `scripts/`

### Content Principles
- **No project-specific identifiers** — all content must be generic and reusable
- **Self-contained** — each skill should work without external dependencies
- **Actionable** — skills are procedures, not essays; use imperative instructions
- **Context-efficient** — minimize token usage while maximizing clarity
- **Composable** — skills are building blocks; agents compose them into roles

## Working on This Repo

### Adding a new skill
1. Write the skill in `.claude/skills/<name>.md`
2. Create the mirror in `.cursor/rules/<name>.mdc` (add YAML frontmatter)
3. Add documentation in `docs/<name>.md` if the skill is complex
4. Update the skills catalog table in `README.md`
5. If the skill needs a script, add it to `scripts/`

### Modifying an existing skill
1. Edit the source in `.claude/skills/<name>.md`
2. Apply the same change to `.cursor/rules/<name>.mdc`
3. Update `docs/<name>.md` if applicable

### Adding a new agent
1. Create `.claude/agents/<name>.md` with YAML frontmatter (name, role, tools, skills)
2. Add the agent to the Team Roster in `.claude/team.md`
3. Add dispatch rules in `.claude/team.md`
4. Update composition chains if the agent participates in workflows
5. Update the Agents table in `README.md`

### Modifying an existing agent
1. Edit `.claude/agents/<name>.md`
2. Update `.claude/team.md` if the role, tools, or skills changed
3. Update `README.md` agent table if externally visible fields changed

### GitHub Isolation
This repo uses project-scoped SSH keys and gh CLI config. See `README.md > GitHub Isolation` for details. Never modify global git or GitHub configuration.
