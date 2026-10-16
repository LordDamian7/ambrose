# Household changelog

| Date | ID | File | Change | Status |
|---|---|---|---|---|
| (install) | v1.0 | all | Household founded | installed |
| 2026-10-16 | v1.1 | `.gitignore`, `butler/templates/fresh-install/` | Public/private split: the household's system can be published while the Principal's profile, goals, consent, hypotheses, briefs, journal, ideas and Minister memories stay local. Blank templates added for fresh installs. Test: dry-run `git add` on a copy staged 36 files, 0 private, 0 personal names. | applied (Principal approved 2026-10-15) |
| 2026-10-16 | v1.1.1 | `.claude/rules/github.md`, `CLAUDE.md` (Part 2, Tools) | GitHub rules added from GitHub's rulesets documentation: every repo, push, merge, tag and ruleset change needs the Principal's yes; three privacy layers (gitignore, pre-publish check, push ruleset where available); default `protect-main` and `protect-releases` rulesets; no bypass for agents. Part 1 unchanged. | applied (Principal requested 2026-10-16) |
| 2026-10-16 | v1.2 | `README.md`, `.claude/agents/minister-intelligence.md`, `SECURITY.md`, `butler/hooks/precommit_privacy_check.py` | Pre-publication hardening: removed account-specific details from the README tools section and a location/profession example from Intelligence's brief; added SECURITY.md (threat model, fork/PR rules, private reporting); added a git pre-commit privacy and secret check. | applied (Principal requested 2026-10-16) |
