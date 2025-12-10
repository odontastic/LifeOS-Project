#!/usr/bin/env python3
import pathlib
import sys

repo_root = pathlib.Path(__file__).parent
bad_files = []

for md_file in repo_root.rglob("*.md"):
    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"⚠️  Could not read {md_file}: {e}", file=sys.stderr)
        continue

    # Strip BOM if present
    if text.startswith("\ufeff"):
        text = text[1:]

    lines = [l for l in text.splitlines() if l.strip() != ""]
    if not lines or lines[0].strip() != "---":
        bad_files.append(md_file)
        continue

    # Find the closing front‑matter marker
    try:
        closing_index = lines[1:].index("---") + 1
    except ValueError:
        bad_files.append(md_file)
        continue

    # Anything before the first non‑empty line after the closing marker is content
    content_start = closing_index + 1
    if content_start >= len(lines):
        bad_files.append(md_file)

if bad_files:
    print("\n⚠️  The following markdown files are missing or malformed front‑matter:")
    for f in bad_files:
        print(f"  - {f.relative_to(repo_root)}")
else:
    print("✅ All markdown files have proper YAML front‑matter.")
