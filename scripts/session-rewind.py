#!/usr/bin/env python3
"""
Session Rewind — Inspect and truncate Claude Code session JSONL files.

Modes:
  inspect <session-file>                 List all user/assistant messages as rewind points
  rewind  <session-file> <line-number>   Create a truncated copy at the given line

The truncated copy gets a new UUID and is written to the same directory.
The original file is never modified.

Usage:
  python3 session-rewind.py inspect /path/to/session.jsonl
  python3 session-rewind.py rewind  /path/to/session.jsonl 621
"""

import json
import sys
import uuid
from pathlib import Path


def extract_text(msg):
    """Extract displayable text from a message dict."""
    if not isinstance(msg, dict):
        return str(msg)[:200]
    content = msg.get("content", "")
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if "text" in block:
                    parts.append(block["text"][:200])
                elif block.get("type") == "tool_use":
                    parts.append("[tool: %s]" % block.get("name", "?"))
        return " | ".join(parts)
    return str(content)[:200]


def inspect_session(path):
    """Print user/assistant messages with line numbers for rewind selection."""
    with open(path) as f:
        lines = f.readlines()

    # Find compression boundaries
    compact_lines = []
    for i, line in enumerate(lines):
        d = json.loads(line)
        if d.get("type") == "system" and d.get("subtype") == "compact_boundary":
            compact_lines.append(i)

    if compact_lines:
        print("COMPRESSION BOUNDARIES at line(s): %s" % ", ".join(str(l) for l in compact_lines))
        print("Messages after these lines are post-compression (summary only).")
        print()

    print("%-6s %-10s %-14s %s" % ("LINE", "TYPE", "UUID", "CONTENT"))
    print("-" * 100)

    for i, line in enumerate(lines):
        d = json.loads(line)
        t = d.get("type", "")
        if t not in ("user", "assistant", "system"):
            continue
        if t == "system" and d.get("subtype") not in ("compact_boundary",):
            continue

        uid = (d.get("uuid") or "")[:12]
        msg = d.get("message", {})
        text = extract_text(msg) if t == "user" else ""

        if t == "system":
            text = "[COMPACT BOUNDARY]"
        elif t == "assistant":
            msg = d.get("message", {})
            text = extract_text(msg)
            # Only show assistant messages with meaningful text (skip pure tool calls)
            if text.startswith("[tool:") or not text.strip():
                continue

        marker = ""
        if compact_lines and i == compact_lines[0]:
            marker = " <-- COMPRESSION"
        elif compact_lines and i > compact_lines[0]:
            marker = " (post-compression)"

        print("%-6d %-10s %-14s %s%s" % (i, t, uid, text[:120], marker))

    print()
    print("Total lines: %d" % len(lines))
    if compact_lines:
        print("Pre-compression messages: lines 0-%d" % (compact_lines[0] - 1))
        print()
        print("To rewind: %s rewind '%s' <LINE_NUMBER>" % (sys.argv[0], path))


def rewind_session(path, cutoff_line):
    """Create a truncated copy of the session at the given line number."""
    path = Path(path)

    with open(path) as f:
        lines = f.readlines()

    if cutoff_line > len(lines):
        print("ERROR: Session only has %d lines, cannot truncate at %d" % (len(lines), cutoff_line))
        sys.exit(1)

    truncated = lines[:cutoff_line]
    new_id = str(uuid.uuid4())
    dst = path.parent / ("%s.jsonl" % new_id)

    with open(dst, "w") as f:
        for line in truncated:
            d = json.loads(line)
            if "sessionId" in d:
                d["sessionId"] = new_id
            f.write(json.dumps(d) + "\n")

    # Show what the session ends with
    print("Created: %s" % dst)
    print("Session ID: %s" % new_id)
    print("Lines: %d (original had %d)" % (len(truncated), len(lines)))
    print()

    # Show last few meaningful messages
    print("Session ends with:")
    shown = 0
    for i in range(len(truncated) - 1, -1, -1):
        d = json.loads(truncated[i])
        t = d.get("type", "")
        if t not in ("user", "assistant"):
            continue
        msg = d.get("message", {})
        text = extract_text(msg)
        if text.strip() and not text.startswith("[tool"):
            print("  L%d [%s]: %s" % (i, t, text[:150]))
            shown += 1
            if shown >= 3:
                break

    print()
    print("Resume with:")
    print("  claude --resume %s" % new_id)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  %s inspect <session-file.jsonl>" % sys.argv[0])
        print("  %s rewind  <session-file.jsonl> <line-number>" % sys.argv[0])
        sys.exit(1)

    mode = sys.argv[1]
    path = sys.argv[2]

    if mode == "inspect":
        inspect_session(path)
    elif mode == "rewind":
        if len(sys.argv) < 4:
            print("ERROR: rewind requires a line number")
            sys.exit(1)
        rewind_session(path, int(sys.argv[3]))
    else:
        print("Unknown mode: %s (use 'inspect' or 'rewind')" % mode)
        sys.exit(1)


if __name__ == "__main__":
    main()
