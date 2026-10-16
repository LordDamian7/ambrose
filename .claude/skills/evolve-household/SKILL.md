---
name: evolve-household
description: Weekly self-improvement review - Ambrose gathers what worked and what the Principal corrected, drafts specific edits to the agent files, has the Minister of Audit check them, and applies only what the Principal approves. Use weekly or when the Principal says "review the household".
---

# Evolve the household

The household improves deliberately, with the Principal's approval, never by silent drift.

## 1. Gather evidence (last 7 days, or since the last review)
- Every `Corrections:` and `Stated preferences:` line in `butler/journal/`.
- Raise items from Cabinet briefs, and whether the Principal took them up, ignored them, or pushed back.
- Audit failures and what they had in common.
- Aides commissioned, used, or idle for 30+ days.
- Anything the Principal said about the household itself ("too chatty", "stop suggesting X", "more of Y").

## 2. Draft proposals
Write up to **5** proposals in `butler/evolution/PROPOSALS.md`, each as:

```
### P-<number> · <title>
- Evidence: <dated references>
- File: <path>
- Change: <exact old text → exact new text, or the new file in full>
- Expected effect: <what will be better, and how we'll know>
- Risk: <what could go worse>
```

Good proposals are specific: a changed default, a new rule drawn from a repeated correction, a narrower tool list, a new standing Aide, a retired Aide, a better question to ask. Vague proposals ("be more helpful") are not allowed.

## 3. Audit
Spawn `minister-audit` with the proposals file. She marks each Pass, Pass with amendment, or Fail. Anything that weakens House Rules, expands permissions or tools, or drifts from the Principal's stated wishes fails by default.

## 4. Ask the Principal
Show the surviving proposals in a compact list: title, one-line effect, one-line risk. Ask which to apply. Changes to Part 1 of `CLAUDE.md`, `.claude/settings.json`, or any hook need the Principal to approve the exact wording.

## 5. Apply and log
- Apply only approved proposals, exactly as approved.
- Append to `butler/evolution/CHANGELOG.md`: date, proposal ID, file, one-line summary, "approved by Principal".
- Move rejected proposals to the changelog as "declined" with the Principal's reason, so they are not re-proposed for 30 days.
- If this folder is a git repository, commit with `household: weekly review YYYY-MM-DD`.
