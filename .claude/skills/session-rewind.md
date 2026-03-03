# Session Rewind

Rewind a compressed Claude Code session to a point before context compression occurred. Inspect available rewind points, then create a truncated copy that lets you resume from any earlier message.

## Trigger

- The user asks to "rewind a session", "go back to before compression", "restore earlier context", or similar
- The user wants to inspect what was lost during context compaction
- The user provides a session ID and wants to see its message history

## Background

When Claude Code conversations hit the context limit, they get "compacted" — a `compact_boundary` system message is inserted, and resuming the session starts from the compressed summary instead of the original messages. However, **all pre-compression messages are preserved** in the JSONL file. This skill creates a truncated copy that lets you resume from any earlier point.

## Procedure

### Step 1 — Resolve Session Path

Session JSONL files are stored under `~/.claude/projects/`. The directory name is derived from the project's absolute path with slashes replaced by dashes.

If the user provides a UUID session ID, resolve it:

```bash
# Auto-detect project directory from cwd
PROJECT_DIR=$(python3 -c "import os; print('-' + os.getcwd().replace('/', '-'))")
SESSION_PATH="$HOME/.claude/projects/${PROJECT_DIR}/${SESSION_ID}.jsonl"
```

If the user provides a full path to a `.jsonl` file, use it directly.

### Step 2 — Inspect or Rewind

**Inspect mode** (no line number specified) — show available rewind points:

```bash
python3 scripts/session-rewind.py inspect "<session-path>"
```

This lists all user/assistant messages with line numbers, marks compression boundaries, and shows which messages are post-compression. Present the output and ask which line the user wants to rewind to.

**Rewind mode** (line number specified) — create a truncated copy:

```bash
python3 scripts/session-rewind.py rewind "<session-path>" <line-number>
```

This creates a new JSONL file with a fresh UUID, containing only messages up to the specified line.

### Step 3 — Report

Show the user:

1. The new session ID
2. The exact `claude --resume <new-session-id>` command
3. A summary of what the session will contain at that rewind point (last few user/assistant messages)

## Setup

### As a slash command

To make this available as `/session-rewind` in a project, copy the files:

```bash
# Copy to your project
mkdir -p .claude/commands .claude/scripts
cp riRoUtils/.claude/skills/session-rewind.md your-project/.claude/commands/session-rewind.md
cp riRoUtils/scripts/session-rewind.py your-project/.claude/scripts/session-rewind.py
```

Then add this frontmatter to the command copy:

```yaml
---
description: Rewind a compressed Claude Code session to a specific point
argument-hint: <session-id-or-path> [line-number]
allowed-tools: [Bash, Read]
---
```

### As a standalone script

```bash
python3 scripts/session-rewind.py inspect <session-file.jsonl>
python3 scripts/session-rewind.py rewind <session-file.jsonl> <line-number>
```

## How It Works

1. The JSONL file contains every message from the conversation, including those before compression
2. A `compact_boundary` system message marks where compression happened
3. When you `claude --resume`, it starts from the compact_boundary forward (summary only)
4. This tool creates a truncated copy with a new UUID, keeping only messages up to your chosen line
5. Resuming the truncated copy restores the full pre-compression context at that point

## Important Notes

- The original session file is **never modified** — only copies are created
- The new session gets a fresh UUID so it doesn't conflict with the original
- All `sessionId` fields inside messages are rewritten to match the new UUID
- Works with any Claude Code project — auto-detects session directory from the current working directory

## Output

```
Rewound Session
  Session ID: {new-uuid}
  Truncated to line {N} — {brief description of where in the conversation}
  claude --resume {new-uuid}
```
