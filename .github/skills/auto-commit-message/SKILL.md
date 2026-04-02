---
name: auto-commit-message
description: "Generate a commit message from the current workspace git diff. Use for summarizing uncommitted changes, writing commit messages before committing, or producing Conventional Commit style messages from staged or unstaged edits. English only. Never push automatically."
argument-hint: "Describe whether to inspect staged, unstaged, or all changes before generating the commit message"
---

# Auto Commit Message Skill

Use this skill when commit-ready code changes exist in the current workspace and you need a concise, standards-compliant commit message without writing it manually.

## When to Use

- Generate a commit message from the current git diff.
- Summarize recent staged or unstaged changes before committing.
- Produce a Conventional Commits style message in English.
- Prepare a commit body when the change spans multiple files or behaviors.

## Core Workflow

1. Get the current changes with `get_changed_files` or inspect the diff directly with `run_in_terminal`.
2. Determine whether the message should describe staged changes, unstaged changes, or all pending modifications.
3. Analyze the affected files, changed functions, and behavioral impact.
4. Classify the change using the best matching type, such as `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `build`, or `chore`.
5. Generate an English commit message in the format `<type>(<scope>): <subject>`.
6. Add a body only when it materially improves clarity.
7. If the user asks to commit, perform only the commit action and never push.

## Commit Rules

- English only.
- Keep every line at 100 characters or fewer.
- Use a short, specific subject.
- Prefer a meaningful scope when it is obvious from the diff.
- Include a body only for important secondary details.
- Perform commit operations only after the message is ready.
- Never run `git push` automatically.

## Recommended Tools

- `get_changed_files`: inspect staged and unstaged file changes quickly.
- `run_in_terminal`: run `git diff`, `git diff --cached`, or targeted git status commands when needed.
- `mcp_gitkraken_git_add_or_commit`: create the commit after the message is finalized.

## Example Requests

- Help me generate a commit message for the current changes.
- Summarize what I changed and turn it into a commit message.
- Write a Conventional Commit message based on the current diff.