#!/usr/bin/env python3

import re
import sys
from pathlib import Path


def slugify(title):
    # Markdown/GitHub-style-ish anchor:
    # lowercase, spaces -> -, remove punctuation
    title = title.lower().strip()
    title = re.sub(r"\s+", "-", title)
    title = re.sub(r"[^\w\-]", "", title, flags=re.UNICODE)
    return title


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} FILE.md", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")

    headings = []

    for line in text.splitlines():
        match = re.match(r"^(#+)\s+(.+?)\s*$", line)
        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2)
        anchor = slugify(title)

        headings.append(
            f'{"  " * (level - 1)}- [{title}](#{anchor})'
        )

    print("\n".join(headings))


if __name__ == "__main__":
    main()
