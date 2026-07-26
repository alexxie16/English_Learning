#!/usr/bin/env python3
import sys
import re
import os


def make_anchor(text):
    a = text.lower()
    a = re.sub(r'[^a-z0-9 _-]', '', a)
    a = a.replace(' ', '-')
    a = re.sub(r'-{2,}', '-', a)
    return a.strip('-')


def extract_week_links(body):
    return re.findall(r'\[Week[^\]]*\]\([^)]+\)', body)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print("Error: file not found")
        sys.exit(1)

    excluded = {
        'words-with-questions', 'words-explain', 'special-words',
        'verb-words', 'words-gallery', 'conversation',
        'interesting', 'economist-newsletter',
    }

    with open(filepath) as f:
        lines = f.readlines()

    has_regular = any(l.startswith('## Regular') for l in lines)

    if has_regular:
        print("""## Regular

📘 **Study**
- ✍️ [Word Review](../../words-review.md)
- ❓ [Words with Questions](#words-with-questions)
- 💡 [New Words to Explain](#words-explain)

📚 **Vocabulary**
- 🧩 [Special Words](#special-words)
- 🔧 [Verb Words](#verb-words)
- 🖼️ [Words Gallery](#words-gallery)

📰 **Reading & Usage**
- 💬 [Conversation](#conversation)
- ✨ [Interesting](#interesting)
- 🏛️ [Economist Newsletter](#economist-newsletter)
""")

    section_idx = 0
    in_body = False
    body = ""
    visible_section = False
    seen_sections = set()
    out = []

    for line in lines:
        raw = line.rstrip('\n')

        if raw.startswith('## '):
            section_idx += 1

            if has_regular and section_idx == 1:
                in_body = False
                body = ""
                visible_section = False
                continue

            if in_body and body:
                for link in extract_week_links(body):
                    out.append(f"- {link}")

            header = raw[3:].strip()
            anchor = make_anchor(header)
            visible = anchor not in excluded

            if visible:
                if anchor in seen_sections:
                    visible = False
                else:
                    seen_sections.add(anchor)
                    out.append(f"\n## {header}")

            in_body = section_idx == 1 or (has_regular and section_idx == 2)
            body = ""
            visible_section = visible
            continue

        if not visible_section:
            continue

        if raw.startswith('### '):
            if in_body and body:
                for link in extract_week_links(body):
                    out.append(f"- {link}")

            in_body = False
            header = raw[4:].strip()
            anchor = make_anchor(header)
            if anchor in excluded:
                continue
            out.append(f"- [{header}](#{anchor})")
            continue

        bullet = re.match(r'- \[(.+?)\]\(#(.+?)\)', raw)
        if bullet:
            in_body = False
            anchor = bullet.group(2)
            if anchor in excluded:
                continue
            out.append(raw)
            continue

        if in_body:
            body += line

    if in_body and body:
        for link in extract_week_links(body):
            out.append(f"- {link}")

    for l in out:
        print(l)


if __name__ == '__main__':
    main()