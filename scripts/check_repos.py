#!/usr/bin/env python3
"""Check every repo in data/entries.json: exists, public, not archived, recent commit.
Prints a Markdown report. Exit code 0 always; the workflow opens an issue if the report has problems."""
import json, os, pathlib, sys, urllib.request, urllib.error, datetime
root = pathlib.Path(__file__).resolve().parent.parent
entries = json.loads((root / "data/entries.json").read_text(encoding="utf-8"))
tok = os.environ.get("GITHUB_TOKEN", "")
STALE_DAYS = 365
problems = []
today = datetime.date.today()
for e in entries:
    req = urllib.request.Request(f"https://api.github.com/repos/{e['repo']}",
                                 headers={"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {tok}"} if tok else {})})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=30))
    except urllib.error.HTTPError as ex:
        problems.append(f"- `{e['repo']}`: HTTP {ex.code} (moved, renamed, deleted or made private?)")
        continue
    if d.get("archived"):
        problems.append(f"- `{e['repo']}`: archived")
    pushed = datetime.date.fromisoformat(d["pushed_at"][:10])
    if (today - pushed).days > STALE_DAYS:
        problems.append(f"- `{e['repo']}`: no commits since {pushed}")
    if d["full_name"].lower() != e["repo"].lower():
        problems.append(f"- `{e['repo']}`: renamed to `{d['full_name']}`")
if problems:
    print("Repos that need a look:\n\n" + "\n".join(problems))
else:
    print("All repos OK.")
