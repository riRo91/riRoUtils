# Mirror Agent Rules

Synchronize skills and rules between Claude Code (`.claude/skills/`) and Cursor (`.cursor/rules/`) so both agents always operate from identical instructions.

## Trigger

- A skill file is created or modified in `.claude/skills/*.md`
- A rule file is created or modified in `.cursor/rules/*.mdc`
- The user asks to "sync rules", "mirror skills", or "update agent rules"

## Procedure

### 1. Inventory Both Directories

Scan `.claude/skills/` for `*.md` files and `.cursor/rules/` for `*.mdc` files. Build a unified list of skill names by stripping extensions. Classify each entry as:

- **Matched** — exists in both directories
- **Claude-only** — exists in `.claude/skills/` but not `.cursor/rules/`
- **Cursor-only** — exists in `.cursor/rules/` but not `.claude/skills/`

For matched pairs, compare the body content (the portion below any frontmatter in `.mdc` files) to detect content drift. Flag any pair whose bodies differ.

### 2. Determine Sync Direction

- If the user triggered the skill by editing a specific file, treat that file as the **source of truth** and sync toward the other format.
- If running a full sync (no single file specified), use modification timestamps to decide which side is newer for each mismatched pair. Ask the user to confirm when timestamps are ambiguous or identical.
- For files that exist on only one side, generate the missing mirror.

### 3. Convert Claude .md to Cursor .mdc

Given a Claude skill file at `.claude/skills/{name}.md`:

1. Read the full file content.
2. Extract a one-line description:
   - Prefer the first sentence of the section immediately after the title heading.
   - If the file begins with a YAML-like metadata block, use the `description` field if present.
   - Fall back to the first non-empty, non-heading line.
3. Build the `.mdc` file with this structure:

```
---
description: {extracted-description}
globs:
alwaysApply: false
---

{original-body-content}
```

4. Write the result to `.cursor/rules/{name}.mdc`.

Notes:
- The `globs` field is left empty by default. If the skill content references specific file patterns (e.g., `*.py`, `docker-compose*.yml`), populate `globs` with those patterns.
- Do not alter the body content. Keep headings, formatting, and code blocks identical.

### 4. Convert Cursor .mdc to Claude .md

Given a Cursor rule file at `.cursor/rules/{name}.mdc`:

1. Read the full file content.
2. Strip the YAML frontmatter block (everything between the opening `---` and closing `---`, inclusive).
3. Trim any leading blank lines left after stripping.
4. Write the remaining body content to `.claude/skills/{name}.md`.

Notes:
- Do not inject any new metadata or frontmatter into the `.md` file.
- Preserve all original formatting, headings, and code blocks.

### 5. Handle Edge Cases

- **Filename normalization**: Both sides should use the same kebab-case base name (e.g., `scaffold-microservice`). If a file on one side uses underscores or camelCase, rename the mirror to match the source's convention.
- **Deletion**: If a file was intentionally deleted from one side, ask the user whether to delete the mirror or restore the missing file.
- **Binary or non-text files**: Skip any non-text files found in these directories and warn the user.
- **Nested directories**: Only process files at the top level of each directory. Warn about any subdirectories found.

### 6. Validate

After syncing, re-scan both directories and confirm:
- Every `.md` in `.claude/skills/` has a corresponding `.mdc` in `.cursor/rules/`
- Every `.mdc` in `.cursor/rules/` has a corresponding `.md` in `.claude/skills/`
- Body content matches for all pairs

## Output

Report a summary table:

| Skill Name | Action | Direction |
|---|---|---|
| `{name}` | Created / Updated / Unchanged | Claude -> Cursor / Cursor -> Claude / N/A |

If all files are already in sync, report: "All skills and rules are in sync. No changes needed."

If any files were created or updated, list each file path and the action taken.
