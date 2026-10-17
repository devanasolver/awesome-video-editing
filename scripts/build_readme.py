#!/usr/bin/env python3
"""Build README.md from data/entries.json, data/resources.json and data/meta.json.
Run: python scripts/build_readme.py"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
meta = json.loads((root / "data/meta.json").read_text(encoding="utf-8"))
repos = json.loads((root / "data/entries.json").read_text(encoding="utf-8"))
assets = json.loads((root / "data/resources.json").read_text(encoding="utf-8"))
cats = meta["categories"]
out = [meta["header"].rstrip(), "", "## Contents\n"]
for part, label in (("software", "Part 1: Software and skills"), ("assets", "Part 2: Assets")):
    out.append(f"**{label}**\n")
    for c in cats:
        if c["part"] == part:
            out.append(f"- [{c['title']}](#{c['anchor']})")
    out.append("")
out += ["- [Using assets safely](#using-assets-safely)", "- [How to choose software](#how-to-choose-software)", "- [Contributing](#contributing)", ""]
for part, label in (("software", "Part 1: Software and skills"), ("assets", "Part 2: Assets")):
    out.append(f"# {label}\n")
    for c in cats:
        if c["part"] != part:
            continue
        out.append(f"## {c['title']}\n")
        out.append(c["blurb"] + "\n")
        if part == "software":
            for e in sorted([e for e in repos if e["category"] == c["id"]], key=lambda e: e["repo"].lower()):
                lic = e["license"] if e["license"] not in ("NOASSERTION", "none") else "check repo"
                out.append(f"- [{e['repo']}](https://github.com/{e['repo']}) "
                           f"![stars](https://img.shields.io/github/stars/{e['repo']}?style=flat&label=%E2%98%85) "
                           f"- {e['description']} _({lic})_")
        else:
            for e in sorted([e for e in assets if e["category"] == c["id"]], key=lambda e: e["name"].lower()):
                out.append(f"- [{e['name']}]({e['url']}) - {e['description']} _License: {e['license']}. [Terms]({e['license_url']})_")
        out.append("")
out.append(meta["footer"].rstrip())
(root / "README.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("built", len(repos), "repos and", len(assets), "asset sources")
