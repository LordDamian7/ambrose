# Scheduling the Cabinet (every 8 hours) and the weekly review

Pick **one** home for the Cabinet. All three run the same `convene-cabinet` skill.

| Option | Runs where | Needs | Best when |
|---|---|---|---|
| A. Claude Code **routine** | Anthropic cloud, laptop can be off | Pro/Max/Team/Enterprise plan, this folder in a **private GitHub repo** | You want it truly always-on |
| B. Claude Desktop **scheduled task** (Local) | Your computer | Claude Desktop app, computer awake | You don't want the folder on GitHub |
| C. Grok **Task / Automation** | Grok app | SuperGrok or X Premium as required | You use the Grok-app version (`grok/AMBROSE-FOR-GROK-APP.md`) |

Avoid starting exactly on the hour; a few minutes past (e.g. 06:07) runs closer to time.

---

## Option A · Claude Code routine (cloud)
1. Put this folder in a **private** GitHub repo and connect GitHub to Claude Code (`/web-setup` or claude.ai/code).
2. In Claude Code run `/schedule`, or open claude.ai/code/routines → **New routine**.
3. Repository: this repo. Environment: Default. Model: your choice.
4. **Connectors:** remove everything the Cabinet doesn't need. Keep only what `CONSENT.md` allows it to read (e.g. Google Calendar, Notion). Routines can use every tool of an included connector **without asking**, so leave Gmail out unless you've allowed email study.
5. Trigger: schedule. Ask: "every 8 hours starting 06:07 Africa/Lagos time".
6. Paste this prompt:

```
You are Ambrose (see CLAUDE.md). This is an UNATTENDED scheduled Cabinet sitting:
nobody is present to answer questions.

1. Run the convene-cabinet skill in unattended mode.
2. House Rules apply in full. You may write only inside butler/ and create drafts.
   Do not send, post, buy, sign, delete or change settings. Anything that needs
   the Principal's yes becomes a "Raise" item in the brief.
3. Read connected accounts only as butler/user-model/CONSENT.md allows, and record
   summaries only, never message bodies.
4. If CONSENT.md names a cabinet digest channel, post at most 5 lines there.
5. Commit butler/ to the default branch with the message
   "cabinet: <date time> sitting" and push.
6. Finish with one line: the brief path and its headline.
```

7. Weekly review (optional second routine, e.g. Sundays 18:07): prompt
   `You are Ambrose. Run the evolve-household skill steps 1–3 only (gather, draft, audit). Do not apply anything. Leave the audited proposals in butler/evolution/PROPOSALS.md for the Principal, commit and push.`
   Ambrose will show them to you at your next session.

**Branch note:** routines push to `claude/`-prefixed branches unless told otherwise; the prompt above tells it to push to the default branch. If your default branch is protected, merge the `claude/` branch or relax protection for this private repo.

## Option B · Claude Desktop scheduled task (local)
1. Open this folder in the Claude Desktop app's **Code** tab.
2. **Routines → New routine → Local**. Use the same prompt as Option A but drop step 5 (no git needed), and add: "If it is between 22:00 and 07:00 Lagos time, write the brief but post no digest."
3. The picker offers Hourly/Daily/Weekly; for 8 hours, ask in any Desktop session: "change my cabinet task to run every 8 hours".
4. Click **Run now** once, watch for permission prompts, and choose "always allow" for the file edits it needs, so later runs don't stall.
5. It runs only while the app is open and the computer is awake. After sleep, Desktop does one catch-up run for the latest missed time.

## Option C · Grok
See the Task prompt at the bottom of `grok/AMBROSE-FOR-GROK-APP.md`.

## Hearing from Ambrose between sessions
- **Telegram (two-way, Claude Code):** `/plugin install telegram@claude-plugins-official`, `/telegram:configure <bot token from @BotFather>`, restart with `claude --channels plugin:telegram@claude-plugins-official`, pair with `/telegram:access pair <code>`, then `/telegram:access policy allowlist`. Requires Bun. Messages flow only while that session is running. Then set Telegram to YES in `CONSENT.md`.
- **Notion digest page:** create a page "Cabinet Digest", allow it in `CONSENT.md`, and keep the Notion connector on the routine.
- **Email draft to self:** allow it in `CONSENT.md`; Ambrose creates a draft, never sends.
