#!/usr/bin/env python3
"""Structural and hook tests for the Ambrose household.

Run from the folder root:  python3 tests/run_checks.py
Exit code 0 = all checks passed.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))


def frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    try:
        import yaml  # type: ignore
        return yaml.safe_load(raw), text
    except ImportError:  # minimal fallback: top-level key: value pairs
        data = {}
        for line in raw.splitlines():
            m = re.match(r"^([A-Za-z]+):\s*(.*)$", line)
            if m:
                data[m.group(1)] = m.group(2) or True
        return data, text


# ---------- 1. Agent files ----------
KNOWN_TOOLS = {"Read", "Grep", "Glob", "Write", "Edit", "WebSearch", "WebFetch", "Bash", "Agent", "Skill", "NotebookEdit", "TodoWrite"}
KNOWN_MODELS = {"sonnet", "opus", "haiku", "fable", "inherit"}
agents_dir = os.path.join(ROOT, ".claude", "agents")
names, desc_chars = [], 0
for fn in sorted(os.listdir(agents_dir)):
    p = os.path.join(agents_dir, fn)
    fm, body = frontmatter(p)
    check(f"agent {fn}: frontmatter parses", fm is not None)
    if not fm:
        continue
    name, desc = fm.get("name"), fm.get("description")
    check(f"agent {fn}: has name and description", bool(name) and bool(desc))
    check(f"agent {fn}: legal name", isinstance(name, str) and ":" not in name and not name.startswith("-") and len(name) <= 256)
    names.append(name)
    desc_chars += len(str(desc))
    tools = fm.get("tools", "")
    tool_list = [t.strip() for t in (tools if isinstance(tools, list) else str(tools).split(",")) if t.strip()]
    unknown = [t for t in tool_list if t not in KNOWN_TOOLS]
    check(f"agent {fn}: tools recognised", not unknown, ",".join(unknown))
    check(f"agent {fn}: no Agent tool (cannot spawn staff)", "Agent" not in tool_list)
    check(f"agent {fn}: model valid", fm.get("model", "inherit") in KNOWN_MODELS)
    check(f"agent {fn}: write-guard hook attached", "guard_writes.py" in body)
check("agent names unique", len(names) == len(set(names)))
check("agent descriptions well under 15k-token budget", desc_chars / 4 < 15000, f"~{desc_chars // 4} tokens")

# ---------- 2. Skills ----------
skills_dir = os.path.join(ROOT, ".claude", "skills")
skill_names = []
for d in sorted(os.listdir(skills_dir)):
    p = os.path.join(skills_dir, d, "SKILL.md")
    fm, _ = frontmatter(p) if os.path.exists(p) else (None, "")
    check(f"skill {d}: SKILL.md with name+description", bool(fm and fm.get("name") and fm.get("description")))
    check(f"skill {d}: name matches folder", bool(fm) and fm.get("name") == d)
    skill_names.append(d)

# ---------- 3. Cross-references ----------
all_text = ""
for dp, _, fns in os.walk(ROOT):
    if "/tests" in dp:
        continue
    for fn in fns:
        if fn.endswith(".md"):
            all_text += open(os.path.join(dp, fn), encoding="utf-8").read()
for ref in set(re.findall(r"`(minister-[a-z]+|aide-[a-z]+)`", all_text)):
    check(f"referenced agent exists: {ref}", ref in names)
for ref in ["convene-cabinet", "intake-interview", "evolve-household"]:
    check(f"referenced skill exists: {ref}", ref in skill_names)
claude_md = open(os.path.join(ROOT, "CLAUDE.md"), encoding="utf-8").read()
for path in re.findall(r"`(butler/[^`*<]+?)`", claude_md):
    path = path.rstrip("/")
    check(f"CLAUDE.md path exists: {path}", os.path.exists(os.path.join(ROOT, path)))
check("CLAUDE.md under 300 lines", claude_md.count("\n") < 300, f"{claude_md.count(chr(10))} lines")
for must in ["PART 1", "PART 2", "Action gates", "Consent and privacy", "Wellbeing and safety", "If you were started as a subagent"]:
    check(f"CLAUDE.md contains '{must}'", must in claude_md)

# ---------- 4. settings.json ----------
try:
    settings = json.load(open(os.path.join(ROOT, ".claude", "settings.json")))
    check("settings.json valid JSON", True)
    cmd = settings["hooks"]["SessionStart"][0]["hooks"][0]["command"]
    check("SessionStart hook script exists", os.path.exists(os.path.join(ROOT, "butler/hooks/session_brief.py")) and "session_brief.py" in cmd)
except Exception as exc:
    check("settings.json valid JSON", False, str(exc))

# ---------- 5. guard_writes.py behaviour ----------
guard = os.path.join(ROOT, "butler", "hooks", "guard_writes.py")


def run_guard(file_path, project, raw=None):
    payload = raw if raw is not None else json.dumps({"tool_name": "Write", "tool_input": {"file_path": file_path}, "cwd": project})
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project)
    r = subprocess.run([sys.executable, "-I", guard], input=payload, capture_output=True, text=True, env=env)
    return r.returncode, r.stderr.strip()


with tempfile.TemporaryDirectory() as proj:
    proj = os.path.realpath(proj)
    for sub in ["butler/journal", "butler/user-model", "butler/hooks", ".claude/agent-memory/minister-insight"]:
        os.makedirs(os.path.join(proj, sub))
    os.symlink("/etc", os.path.join(proj, "butler", "escape"))
    cases = [
        ("journal write allowed", f"{proj}/butler/journal/2026-10-08.md", 0),
        ("relative path inside butler allowed", "butler/cabinet/briefs/x.md", 0),
        ("agent memory allowed", f"{proj}/.claude/agent-memory/minister-insight/MEMORY.md", 0),
        ("CLAUDE.md blocked", f"{proj}/CLAUDE.md", 2),
        ("settings.json blocked", f"{proj}/.claude/settings.json", 2),
        ("../ traversal blocked", f"{proj}/butler/../CLAUDE.md", 2),
        ("symlink escape blocked", f"{proj}/butler/escape/passwd", 2),
        ("user-model blocked for subagents", f"{proj}/butler/user-model/CONSENT.md", 2),
        ("hooks blocked (no self-unlocking)", f"{proj}/butler/hooks/guard_writes.py", 2),
        ("home directory blocked", os.path.expanduser("~/.bashrc"), 2),
    ]
    for label, path, want in cases:
        code, err = run_guard(path, proj)
        check(f"guard: {label}", code == want, f"exit {code} {err}")
    code, _ = run_guard(None, proj, raw="not json")
    check("guard: malformed input fails closed", code == 2)
    code, _ = run_guard(None, proj, raw=json.dumps({"tool_input": {}}))
    check("guard: missing path fails closed", code == 2)

# ---------- 6. session_brief.py behaviour ----------
brief_script = os.path.join(ROOT, "butler", "hooks", "session_brief.py")


def run_brief(project):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project)
    return subprocess.run([sys.executable, "-I", brief_script], capture_output=True, text=True, env=env).stdout


with tempfile.TemporaryDirectory() as tmp:
    proj = os.path.join(tmp, "house")
    shutil.copytree(ROOT, proj, ignore=shutil.ignore_patterns("tests", ".git"))
    out = run_brief(proj)
    check("brief: fresh install asks for intake", "UNINITIALISED" in out, out)
    check("brief: fresh install notes no Cabinet yet", "No Cabinet brief yet" in out)

    prof = os.path.join(proj, "butler/user-model/PROFILE.md")
    text = open(prof).read()
    check("fixture: profile placeholder present", "STATUS: UNINITIALISED" in text)
    open(prof, "w").write(text.replace("STATUS: UNINITIALISED", "STATUS: ACTIVE since 2026-10-08"))
    cons = os.path.join(proj, "butler/user-model/CONSENT.md")
    text = open(cons).read()
    check("fixture: consent ACTIVE line present", "Proactive contact: ACTIVE" in text)
    open(cons, "w").write(text.replace("Proactive contact: ACTIVE", "Proactive contact: PAUSED"))
    tpl = open(os.path.join(proj, "butler/templates/brief-template.md")).read()
    tpl = tpl.replace("<one line, written last by Ambrose>", "Two strong role leads; writing slot idea")
    tpl = tpl.replace("|---|---|---|---|---|---|", "|---|---|---|---|---|---|\n| 1 | Intelligence | Apply to role X by Fri | Pass | Raise | Deadline Friday |\n| 2 | Growth | 45-min writing block | Pass | Hold | Needs consent |")
    open(os.path.join(proj, "butler/cabinet/briefs/2026-10-08-1407.md"), "w").write(tpl)
    open(os.path.join(proj, "butler/journal/2026-10-08.md"), "w").write("## 09:00 · CV\n- Open loops: send draft to supervisor by Thursday\n")
    out = run_brief(proj)
    check("brief: active profile no longer asks for intake", "UNINITIALISED" not in out and "Latest Cabinet brief" in out, out)
    check("brief: honours stand-down", "PAUSED" in out)
    check("brief: shows headline", "Two strong role leads" in out)
    check("brief: surfaces Raise item only", "Apply to role X" in out and "45-min writing block" not in out)
    check("brief: surfaces open loops", "send draft to supervisor" in out)
    check("brief: output stays short", out.count("\n") <= 12, f"{out.count(chr(10))} lines")

# ---------- report ----------
failed = [r for r in results if not r[1]]
for name, ok, detail in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
sys.exit(1 if failed else 0)
