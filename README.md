# Ambrose · a butler-orchestrator household

Ambrose is a head-of-household AI. He works with you directly, commissions named **Aides** for specialist jobs, and chairs a **Cabinet** of four Ministers who study how you work, research what would help you grow, scan the world for opportunities, and audit each other every 8 hours. He learns you over time, but only from what you allow, and improves himself only with your approval.

```
                         You (the Principal)
                                 │
                          ┌──────┴──────┐
                          │   AMBROSE   │  orchestrator · only one who talks to you
                          └──┬───────┬──┘  and touches your accounts
              delegates      │       │      chairs, every 8 h
        ┌────────────────────┘       └────────────────────┐
   AIDES (named, created on demand)              THE CABINET (advise Ambrose)
   · Pemberton, Scribe   (journal)               · Sir Cedric Vale     Insight
   · Finch, Courier      (channel drafts)        · Dame Ottoline Hart  Growth
   · <new aides Ambrose commissions>             · Lord Bastian Reeve  Intelligence
                                                 · Mistress Agatha Thorne  Audit (checks the rest)
                         └──────────── butler/  (memory, briefs, hypotheses, changelog) ───────────┘
```

## What's in the box
| Path | What it is |
|---|---|
| `CLAUDE.md` | The master prompt: Part 1 House Rules (every agent), Part 2 Ambrose |
| `.claude/agents/` | 4 Ministers + 2 starter Aides (subagent files) |
| `.claude/skills/` | `convene-cabinet`, `intake-interview`, `evolve-household` |
| `.claude/settings.json` | Session-start briefing hook; denies `rm -rf` and `sudo` |
| `butler/` | The household's memory: user model, consent, briefs, hypotheses, journal, staff registry, changelog |
| `butler/hooks/` | `guard_writes.py` (subagents can only write in `butler/`), `session_brief.py` (Ambrose starts every session briefed) |
| `grok/AMBROSE-FOR-GROK-APP.md` | Single paste-in version for grok.com / the X app |
| `SCHEDULING.md` | How to run the Cabinet every 8 hours, and Telegram setup |
| `tests/` | `run_checks.py` (automated) and `ACCEPTANCE.md` (16 live behaviour tests) |

## Install
**Claude Code (recommended: full household)**
1. Unzip anywhere, e.g. `~/ambrose`. Python 3 must be on your PATH (the hooks use it).
2. `cd ~/ambrose && claude`, and accept the folder-trust prompt (hooks only run in trusted folders).
3. Copy the blank personal files into place (they are never committed; see `.gitignore`): follow `butler/templates/fresh-install/README.md`.
4. Say "Hello". Ambrose runs a 10-minute intake interview and writes your profile, goals and consent rules.
5. Optional: `python3 tests/run_checks.py` should report all checks passing.
6. Follow `SCHEDULING.md` for the 8-hour Cabinet and Telegram.

**If Ambrose doesn't seem to know who he is:** the session was probably opened in the wrong folder. Claude Code loads `CLAUDE.md`, the hooks and the skills from the folder you start in. Open the folder that contains `CLAUDE.md` and `butler/`. If unzipping created a nested folder (e.g. `ambrose/ambrose/`), either open the inner one, or put a one-line `CLAUDE.md` in the outer one that says: *"The household lives in `<inner-folder>/`. Reopen the session there before doing anything."*

**Grok Build (xAI's CLI)**: xAI's documentation says Grok Build reads Claude Code's `CLAUDE.md`, agents, skills, hooks and MCP servers with no extra configuration. `cd ~/ambrose && grok`, then run `/hooks-trust` so the write guard is active. I could not run Grok Build here, so treat it as untested and run `tests/ACCEPTANCE.md` first.

**Grok app**: use `grok/AMBROSE-FOR-GROK-APP.md`. One model plays all roles; state lives in a pasted Ledger.

## Capability check (what actually works, as of 8 Oct 2026)
| Capability you asked for | Claude Code | Grok Build | Grok app |
|---|---|---|---|
| Named subagents (Ministers, Aides) | ✅ `.claude/agents/`; up to 20 at once by default | ✅ per xAI docs (untested here) | ⚠️ simulated roles |
| Ambrose creates new subagents himself | ✅ writes an agent file; picked up within seconds, no restart | ⚠️ likely, untested | ⚠️ Ledger entry only |
| Ministers advise every 8 hours | ✅ cloud routine (min. interval 1 h) or local Desktop task | ❌ no scheduler found; use a Claude routine | ✅ Tasks / Automations |
| Remembers you across sessions | ✅ `butler/` files + each Minister's own memory folder | ✅ `butler/` files | ⚠️ pasted Ledger (+ Grok memory) |
| Studies your patterns | ✅ from journal + allowed accounts, as hypotheses | ✅ same | ⚠️ within the conversation |
| Reaches you on other channels | ✅ Telegram/Discord/iMessage via channels (research preview; session must be running), Notion page, email draft | ⚠️ via MCP | ✅ app notifications |
| Computer use | ✅ CLI: macOS, Pro/Max, interactive sessions only. Desktop app: macOS and Windows | ❓ not confirmed | ❓ "Grok Computer" in limited beta |
| Uses tools to test hypotheses | ✅ Ministers have web + file tools only; write guard enforced by hook | ⚠️ if hooks trusted | ⚠️ prompt rule only |
| Self-evolving | ✅ weekly proposals → Audit → your approval → changelog | ✅ same files | ⚠️ Ledger changelog |

## Recommended tools
Ambrose works best with a few connectors. Connect only what you need, and grant access in `CONSENT.md` before Ambrose studies anything.

| Connector | Role in the household |
|---|---|
| Google Calendar | Read your load for the Cabinet; place habit and focus blocks (with your yes) |
| Gmail | Drafts only by default; study subjects and senders only if `CONSENT.md` allows it |
| Notion | Weekly digest page for unattended Cabinet sittings; long-form notes |
| Todoist | One next small step a day, so it buzzes your phone |
| GitHub | Publish iterations; required for the always-on cloud Cabinet |
| Zapier | Bridge to apps with no connector |
| A database (e.g. Supabase) | Upgrade path: move `butler/user-model` into a database shared across agents |

**Channels:** a Telegram channel plugin gives a two-way "reach me anywhere" route (steps in `SCHEDULING.md`). Keep finance and trading connectors **off** for the Cabinet unless a stated goal needs them.

## Honest limits
- **Not unlimited.** Ambrose can only act through the tools, connectors and permissions you give him, and every Minister run uses your plan's usage. Three Cabinet sittings a day is about 15 subagent runs; drop to twice daily if usage bites.
- **He will always stop before** sending, paying, signing, deleting or changing settings. That is a feature.
- Channels and routines are research previews; their behaviour may change.
- The Cabinet only knows what's in `butler/` and what you've allowed it to read. A thin journal means thin insight for the first week or two.

## Commands
`convene the Cabinet` · `show me what you know` · `forget …` · `stand down` / `resume` · `who's on staff` · `review the household` · `be blunt`
