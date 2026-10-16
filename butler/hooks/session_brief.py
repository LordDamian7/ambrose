#!/usr/bin/env python3
"""SessionStart hook: prints a short household status for Ambrose.

Whatever this prints is added to the session's context, so Ambrose starts
every session already knowing the latest Cabinet decisions and open loops.
Never fails the session: any error just prints a one-line note.
"""
import datetime as dt
import glob
import os
import re

root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
B = os.path.join(root, "butler")


def newest(pattern: str):
    files = [f for f in glob.glob(os.path.join(B, pattern)) if not f.endswith(".gitkeep")]
    return max(files, key=os.path.getmtime) if files else None


def read(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return ""


def section(text: str, heading: str) -> str:
    m = re.search(rf"^## {re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def main() -> None:
    out = ["[Household status for Ambrose — read, don't recite]"]

    profile = read(os.path.join(B, "user-model", "PROFILE.md"))
    if "STATUS: UNINITIALISED" in profile:
        out.append("- Profile: UNINITIALISED → run the intake-interview skill (after any urgent task).")
    consent = read(os.path.join(B, "user-model", "CONSENT.md"))
    if "Proactive contact: PAUSED" in consent:
        out.append("- Proactive contact is PAUSED (Principal said 'stand down'). Raise nothing unprompted.")

    brief = newest("cabinet/briefs/*.md")
    if brief:
        text = read(brief)
        head = re.search(r"\*\*Headline:\*\*\s*(.+)", text)
        out.append(f"- Latest Cabinet brief: {os.path.relpath(brief, root)}")
        if head:
            out.append(f"  Headline: {head.group(1).strip()}")
        raises = [ln for ln in section(text, "Ambrose's decisions").splitlines() if "| Raise" in ln]
        for ln in raises[:2]:
            out.append(f"  To raise: {ln.strip()}")
    else:
        out.append("- No Cabinet brief yet.")

    journal = newest("journal/*.md")
    if journal:
        loops = [ln.strip() for ln in read(journal).splitlines() if ln.strip().startswith("- Open loops:")]
        loops = [ln for ln in loops if ln.rstrip(":") != "- Open loops"]
        if loops:
            out.append(f"- Open loops from {os.path.basename(journal)}: {loops[-1][len('- Open loops:'):].strip()}")

    log = read(os.path.join(B, "evolution", "CHANGELOG.md"))
    dates = re.findall(r"^\| (\d{4}-\d{2}-\d{2}) \|", log, re.M)
    if dates:
        days = (dt.date.today() - dt.date.fromisoformat(max(dates))).days
        if days >= 7:
            out.append(f"- Last household review was {days} days ago → offer 'review the household'.")
    else:
        out.append("- No household review logged yet.")

    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block a session start
        print(f"[Household status unavailable: {exc}]")
