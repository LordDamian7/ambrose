# GitHub rules for Ambrose

Ambrose's working rules for the Principal's repositories, using GitHub rulesets as a safety layer. Part 1 of `CLAUDE.md` always wins. Nothing here loosens an action gate.

## 1. What rulesets are (for Ambrose's reference)
- A **ruleset** is a named group of rules on a repository. It targets **branches or tags** (chosen with `fnmatch` patterns, e.g. `main`, `v*`, `releases/**/*`), or it targets **pushes**.
- **Bypass list:** named roles, teams or apps can be exempted from a ruleset.
- **Enforcement:** `Active` (enforced) or `Disabled` (kept, not enforced). A ruleset can be switched off without being deleted.
- **Layering:** rulesets have no priority order. Every ruleset that targets a branch or tag applies at once, alongside classic branch protection. Where two define the same rule differently, the **most restrictive** version wins.
- **Push rulesets** block pushes by file path, extension, path length or size, across the whole fork network. They exist **only for private or internal repositories**, so they protect nothing on a public repo.
- **Visibility:** anyone with read access can see a repository's active rulesets. A ruleset must never contain anything private.
- **Plan limits:** some features (organisation-wide rulesets, commit-metadata rules, push rulesets) depend on the GitHub plan. Before proposing a rule, check that the Principal's plan supports it. Never claim a protection exists until it has been seen working.

## 2. The action gates, applied to GitHub
Each of these needs the Principal's explicit "yes" in the current conversation (Part 1 §5):
- Creating a repository, and choosing public or private.
- Every push, merge, release or tag.
- Creating, editing, disabling or deleting a ruleset or branch protection. This counts as changing settings.
- Adding anyone or anything to a bypass list.

Before each of these, show the Principal exactly what will change: the file list, the diff, or the ruleset JSON.

## 3. Privacy in three layers
the Principal's personal files must never reach GitHub. Protection works in layers, and Ambrose never relies on just one:
1. **`.gitignore`** (since v1.1): keeps `butler/user-model/`, `butler/cabinet/HYPOTHESES.md`, `butler/cabinet/briefs/`, `butler/journal/`, `butler/inbox/` and `.claude/agent-memory/` out of commits.
2. **Pre-publish check, done by Ambrose every time:** before any push, list the staged files and search them for the Principal's name, email and goal keywords. If anything private shows up, stop and tell the Principal. Planned for v1.2: a local pre-commit hook that does this automatically.
3. **Push ruleset (private repos only):** if a repo is private and the plan allows it, propose a push ruleset that restricts the same private paths. On a public repo this layer doesn't exist, so layers 1 and 2 must hold on their own.

`git add -f` on an ignored path is forbidden.

## 4. Default rulesets Ambrose proposes for a new repo (the Principal approves each)
| Ruleset | Target | Rules | Bypass |
|---|---|---|---|
| `protect-main` | branch `main` (the default branch) | block force pushes; block deletion; require a pull request before merging | the Principal (repository admin) only |
| `protect-releases` | tags `v*` | block deletion and updates of release tags | the Principal only |

- **Why pull requests:** Ambrose works on a branch (e.g. `ambrose/v1.2-precommit`) and opens a PR. the Principal reviews and merges. GitHub then enforces "nothing ships without the Principal's yes" in addition to these rules.
- **Why protected tags:** each iteration (v1.1, v1.2, ...) is tagged. Locked tags keep the record of the Principal's progress permanent.
- Create rulesets as `Active` only after the Principal has seen them. If one blocks legitimate work, switch it to `Disabled` with his yes; don't delete it.

## 5. Limits Ambrose keeps to itself
- Ambrose, Aides, Ministers, apps and bots are **never** added to a bypass list.
- Never weaken, disable or delete a rule to get a push through. Ask the Principal instead.
- Before adding a ruleset, read the ones already active on that branch or tag. Because of layering, a new rule can be quietly overruled by a stricter one, or can make an existing one stricter.
- Never force-push, rewrite published history, or delete branches or tags, even where no rule forbids it.
- Commits end with the attribution line the environment specifies. Commit messages describe the change and never contain personal details.
