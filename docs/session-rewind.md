# Session Rewind

Recover pre-compression context from Claude Code sessions by creating truncated copies you can resume from any earlier point.

## Problem

When Claude Code conversations hit the context window limit, the session gets "compacted" — a `compact_boundary` marker is inserted and all prior messages are replaced with a compressed summary. Resuming with `claude --resume` starts from the summary, losing the full original context.

However, the original messages are **still preserved** in the JSONL file on disk. This tool lets you inspect those messages and create a truncated copy that restores the full context at any point before compression.

## How It Works

```
Original session (1200 lines):
  L0-620:   Full messages (pre-compression) ← still in the file, but skipped on resume
  L621:     compact_boundary marker
  L622-1200: Post-compression messages (summary + new messages) ← what --resume uses

After rewind to line 621:
  New session (621 lines):
  L0-620:   Full messages (pre-compression) ← now this IS the session

  Resume this → Claude sees the full original context up to that point
```

## Usage

### Inspect a session

See all messages with line numbers and compression boundaries:

```bash
python3 scripts/session-rewind.py inspect ~/.claude/projects/-Users-me-myproject/SESSION_ID.jsonl
```

Output:

```
COMPRESSION BOUNDARIES at line(s): 621
Messages after these lines are post-compression (summary only).

LINE   TYPE       UUID           CONTENT
----------------------------------------------------------------------------------------------------
0      user       a1b2c3d4e5f6   Set up the database connection pool...
15     assistant  f6e5d4c3b2a1   I'll create the connection factory with pooling...
42     user       a1b2c3d4e5f6   Now add retry logic...
...
621    system                    [COMPACT BOUNDARY] <-- COMPRESSION
622    assistant  x9y8z7w6v5u4   Based on our conversation... (post-compression)
...

Total lines: 1200
Pre-compression messages: lines 0-620

To rewind: scripts/session-rewind.py rewind '...' <LINE_NUMBER>
```

### Rewind to a specific line

```bash
python3 scripts/session-rewind.py rewind ~/.claude/projects/-Users-me-myproject/SESSION_ID.jsonl 621
```

Output:

```
Created: /Users/me/.claude/projects/-Users-me-myproject/NEW_UUID.jsonl
Session ID: NEW_UUID
Lines: 621 (original had 1200)

Session ends with:
  L618 [assistant]: The connection pool is configured with max 10 connections...
  L615 [user]: Can you add health check on startup?
  L610 [assistant]: Here's the retry logic with exponential backoff...

Resume with:
  claude --resume NEW_UUID
```

### Finding session files

Session JSONL files live in `~/.claude/projects/`. The directory name is derived from your project's absolute path:

```bash
# Project at /Users/me/my-project → directory name:
ls ~/.claude/projects/-Users-me-my-project/

# List all sessions for a project
ls ~/.claude/projects/-Users-me-my-project/*.jsonl
```

## Setup in a Project

### As a slash command (`/session-rewind`)

```bash
mkdir -p .claude/commands .claude/scripts
cp riRoUtils/scripts/session-rewind.py .claude/scripts/session-rewind.py
```

Create `.claude/commands/session-rewind.md`:

```markdown
---
description: Rewind a compressed Claude Code session to a specific point
argument-hint: <session-id-or-path> [line-number]
allowed-tools: [Bash, Read]
---

# Session Rewind

(Copy content from riRoUtils/.claude/skills/session-rewind.md)
```

Then use it:

```
/session-rewind abc12345-6789-...
/session-rewind abc12345-6789-... 621
```

### As a standalone script

```bash
# Copy to your project or run from riRoUtils
python3 riRoUtils/scripts/session-rewind.py inspect <file>
python3 riRoUtils/scripts/session-rewind.py rewind <file> <line>
```

## Important Notes

- The original session file is **never modified** — only copies are created
- The new session gets a fresh UUID so it doesn't conflict
- All `sessionId` fields inside messages are rewritten to match the new UUID
- Works with any Claude Code project
- No dependencies beyond Python 3 standard library
