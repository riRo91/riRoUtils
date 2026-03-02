# AGENT.md — riRoUtils

Instructions for AI agents (Claude Code, Cursor, or any LLM-based tool) working on this repository.

## Project Purpose

This is a **utility repository** — a collection of reusable, generic skills, rules, scripts, and documentation templates for AI-assisted software engineering workflows. It does not contain application code.

## Repository Layout

```
riRoUtils/
├── AGENT.md                  # You are here — read this first
├── README.md                 # Human-facing project overview
├── .claude/skills/           # Claude Code skills (.md format)
├── .cursor/rules/            # Cursor rules (.mdc format) — mirrors of Claude skills
├── docs/                     # Detailed documentation for each skill
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

### Naming Conventions
- Skill/rule files: `kebab-case.md` / `kebab-case.mdc`
- Documentation files: `kebab-case.md` in `docs/`
- Scripts: `kebab-case.sh` in `scripts/`

### Content Principles
- **No project-specific identifiers** — all content must be generic and reusable
- **Self-contained** — each skill should work without external dependencies
- **Actionable** — skills are procedures, not essays; use imperative instructions
- **Context-efficient** — minimize token usage while maximizing clarity

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

### GitHub Isolation
This repo uses project-scoped SSH keys and gh CLI config. See `README.md > GitHub Isolation` for details. Never modify global git or GitHub configuration.
