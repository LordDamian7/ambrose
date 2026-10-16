#!/usr/bin/env python3
"""Git pre-commit guard: refuse commits that would publish the Principal's private files.

Install once per clone:
    python butler/hooks/precommit_privacy_check.py --install
Exit code 1 = commit blocked.
"""
import os
import re
import subprocess
import sys

PRIVATE = re.compile(
    r"^(butler/user-model/(?!\.gitkeep$)|butler/cabinet/HYPOTHESES\.md$|butler/cabinet/briefs/(?!\.gitkeep$)"
    r"|butler/journal/(?!\.gitkeep$)|butler/inbox/(?!\.gitkeep$)|\.claude/agent-memory)"
)
SECRET = re.compile(
    r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[A-Za-z0-9-]{10,}"
    r"|-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)


def install() -> None:
    root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
    hook = os.path.join(root, ".git", "hooks", "pre-commit")
    with open(hook, "w", newline="\n") as fh:
        fh.write('#!/bin/sh\nexec python "$(git rev-parse --show-toplevel)/butler/hooks/precommit_privacy_check.py"\n')
    os.chmod(hook, 0o755)
    print(f"Installed {hook}")


def main() -> int:
    staged = subprocess.check_output(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"], text=True
    ).splitlines()
    problems = [f"private file: {p}" for p in staged if PRIVATE.search(p)]
    for p in staged:
        try:
            blob = subprocess.check_output(["git", "show", f":{p}"], stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            continue
        if SECRET.search(blob.decode("utf-8", "ignore")):
            problems.append(f"possible secret in: {p}")
    if problems:
        print("Commit blocked by the household privacy check:", *problems, sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if "--install" in sys.argv:
        install()
        sys.exit(0)
    sys.exit(main())
