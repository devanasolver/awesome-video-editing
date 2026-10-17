# Contributing

Thanks for helping. This list stays useful only if every entry is real, current and honestly described.

## What gets in

**Software (GitHub repos)**

1. It is **public** and **not archived**.
2. It has **a license**, or says clearly how it can be used.
3. It has had **a commit in the last 12 months**.
4. It fits this list: video editing, tools for making or processing video, or agent skills for video.
5. It does something you can show in the README. No empty shells, no "coming soon".
6. It is **not a copy** of another repo on the list.

**Assets (websites)**

1. The source states how its content may be used, on a page you can link.
2. The content is free to download.
3. If the license limits use (credit needed, non-commercial only, per-file rules), the description says so.
4. No sources that scrape or re-host other people's work without permission.

Owners may add their own project. It is judged by the same rules. Mark it with "(by the author)" in the description.

## How to add a repo

1. Fork this repo.
2. Add **one** object to `data/entries.json`:
   ```json
   {
     "repo": "owner/name",
     "category": "edit",
     "description": "One plain sentence. What it does. Say if it needs paid keys.",
     "license": "MIT",
     "verified": "YYYY-MM-DD",
     "last_commit": "YYYY-MM-DD"
   }
   ```
   Categories: `edit`, `code`, `skills`, `speech`, `audio`, `enhance`, `tools`, `screen`, `vfx`, `anim`, `gen`, `lists`.
3. Run `python scripts/build_readme.py`. Do not edit `README.md` by hand.
4. Open a pull request using the template. One entry per PR.

## How to add an asset source

Add one object to `data/resources.json`:
```json
{
  "name": "Site name",
  "url": "https://example.com/",
  "category": "footage",
  "description": "One plain sentence. Say about any limits.",
  "license": "Short license summary",
  "license_url": "https://example.com/license",
  "verified": "YYYY-MM-DD"
}
```
Categories: `footage`, `music`, `sfx`, `fonts`, `graphics`, `textures`, `templates`. Then run the build script.

## Writing the description

- Plain words. Short. One sentence, two at most.
- Say what it does, not how great it is. No "best", "powerful", "revolutionary".
- If it needs paid keys or a paid plan, say so.
- If the claims are unproven, do not repeat them as facts.
- No affiliate or tracking links.

## Removing or fixing entries

A weekly check (GitHub Action) opens an issue when a listed repo is archived, renamed, missing or has no commits for a year, or when an asset link stops answering. Maintainers remove or fix those. You can also open a PR to remove a dead entry.

## Changelog

Add a line to `CHANGELOG.md` under "Unreleased" for each change.
