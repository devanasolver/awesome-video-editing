#!/usr/bin/env python3
"""Check that every asset URL and license URL in data/resources.json still answers.
Some sites block scripts (403/429); those are reported as 'unverified', not broken."""
import json, pathlib, urllib.request, urllib.error
root = pathlib.Path(__file__).resolve().parent.parent
items = json.loads((root / "data/resources.json").read_text(encoding="utf-8"))
bad, unverified = [], []
for e in items:
    for key in ("url", "license_url"):
        req = urllib.request.Request(e[key], headers={"User-Agent": "Mozilla/5.0 (link check)"})
        try:
            urllib.request.urlopen(req, timeout=30)
        except urllib.error.HTTPError as ex:
            (unverified if ex.code in (401, 403, 429) else bad).append(f"- {e['name']} {key}: HTTP {ex.code}")
        except Exception as ex:
            bad.append(f"- {e['name']} {key}: {type(ex).__name__}")
if bad:
    print("Asset links that need a look:\n\n" + "\n".join(bad))
else:
    print("All asset links OK.")
if unverified:
    print("\nBlocked from scripts (check by hand):\n" + "\n".join(unverified))
