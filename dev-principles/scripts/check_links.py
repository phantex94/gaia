#!/usr/bin/env python3
"""Check local Markdown navigation and reference reachability."""
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def links(text):
    text = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)
    return re.findall(r"\[[^\]]*\]\(([^)]+)\)", text)


def check(root):
    root = root.resolve()
    files = set(root.rglob("*.md"))
    graph = {p: set() for p in files}
    errors = []
    for source in sorted(files):
        text = source.read_text()
        if not text.endswith("\n") or any(line.rstrip() != line for line in text.splitlines()):
            errors.append(f"{source.relative_to(root)}: invalid whitespace")
        if text.count("```") % 2:
            errors.append(f"{source.relative_to(root)}: unclosed code fence")
        for link in links(text):
            parsed = urlsplit(link.strip("<>"))
            if parsed.scheme or parsed.netloc:
                continue
            target = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            if not target.exists():
                errors.append(f"{source.relative_to(root)}: missing target {link}")
            elif target in files:
                graph[source].add(target)
    entry = root / "SKILL.md"
    pending = [entry]
    visited = set()
    while pending:
        source = pending.pop()
        if source not in visited:
            visited.add(source)
            pending.extend(graph.get(source, set()) - visited)
    for reference in sorted((root / "references").glob("*.md")):
        if reference not in visited:
            errors.append(f"{reference.relative_to(root)}: unreachable from SKILL.md")
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print(f"Checked {len(files)} Markdown files; all local links resolve and references are reachable.")
    return 0


if __name__ == "__main__":
    sys.exit(check(Path(__file__).resolve().parents[1]))
