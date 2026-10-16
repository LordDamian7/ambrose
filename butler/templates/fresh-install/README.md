# Fresh-install templates

The Principal's personal files are never committed (see `.gitignore`). On a new install, copy these into place once:

| Template | Copy to |
|---|---|
| PROFILE.md, GOALS.md, PATTERNS.md, CONSENT.md | `butler/user-model/` |
| HYPOTHESES.md | `butler/cabinet/` |
| IDEAS.md | `butler/inbox/` |

    cp butler/templates/fresh-install/{PROFILE,GOALS,PATTERNS,CONSENT}.md butler/user-model/
    cp butler/templates/fresh-install/HYPOTHESES.md butler/cabinet/
    cp butler/templates/fresh-install/IDEAS.md butler/inbox/
