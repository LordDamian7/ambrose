#!/usr/bin/env python3
"""PreToolUse guard for Ministers and Aides.

Blocks any Write/Edit outside the household's working areas, and blocks
subagents from editing the Principal's user-model files or the hooks themselves.
Exit code 2 = block the tool call (Claude Code feeds stderr back to the agent).
Fails closed: if the input can't be understood, the write is blocked.
"""
import json
import os
import sys

ALLOWED = ["butler", ".claude/agent-memory", ".claude/agent-memory-local"]
PROTECTED = ["butler/user-model", "butler/hooks"]


def block(msg: str) -> None:
    print(f"Blocked by house rules: {msg}", file=sys.stderr)
    sys.exit(2)


def inside(path: str, root: str) -> bool:
    return path == root or path.startswith(root + os.sep)


def main() -> None:
    try:
        data = json.load(sys.stdin)
    except Exception:
        block("could not read the tool request.")
        return

    tool_input = data.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not target:
        block("no file path in the request.")

    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    project = os.path.realpath(project)
    if not os.path.isabs(target):
        target = os.path.join(project, target)
    target = os.path.realpath(target)  # defeats ../ tricks and symlinks

    for rel in PROTECTED:
        if inside(target, os.path.join(project, rel)):
            block(f"subagents may not edit {rel}/. Ask Ambrose to make this change.")

    for rel in ALLOWED:
        if inside(target, os.path.join(project, rel)):
            sys.exit(0)

    block("subagents may only write inside butler/ (or their own agent memory).")


if __name__ == "__main__":
    main()
