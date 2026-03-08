import re
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path.cwd()
DATA_DIR = PROJECT_ROOT / "individual_food_data"
MASTER_FILE = PROJECT_ROOT / "NUTRITION_MASTER.md"


def extract_id(filename: str) -> int:
    match = re.match(r"(\d+)_", filename)
    return int(match.group(1)) if match else -1


def extract_title(content: str) -> str:
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    return match.group(1).strip() if match else "Unknown Title"


def strip_h1(content: str) -> str:
    # Remove the first H1 heading line to avoid duplicate titles in the master file
    return re.sub(r"^#\s+.+\n?", "", content, count=1, flags=re.MULTILINE).strip()


def make_anchor(id_num: int, title: str) -> str:
    # Build a clean, unique anchor from ID + title
    raw = f"{id_num:02d}-{title.lower()}"
    raw = raw.replace(" ", "-")
    # Keep only alphanumeric, hyphens, and underscores
    raw = re.sub(r"[^a-z0-9\-_]", "", raw)
    return raw


def consolidate_nutrition() -> None:
    if not DATA_DIR.exists():
        print(f"Error: Data directory {DATA_DIR} does not exist.")
        return

    md_files = sorted(DATA_DIR.glob("*.md"), key=lambda f: extract_id(f.name))

    if not md_files:
        print("No markdown files found.")
        return

    # ---- Pass 1: collect titles and pre-compute anchors ----
    entries: list[tuple[int, str, str]] = []  # (id_num, title, anchor)
    for md_file in md_files:
        content = md_file.read_text(encoding="utf-8")
        title = extract_title(content)
        id_num = extract_id(md_file.name)
        anchor = make_anchor(id_num, title)
        entries.append((id_num, title, anchor))

    # ---- Build Table of Contents ----
    toc_lines = ["## 📋 Table of Contents", ""]
    for id_num, title, anchor in entries:
        toc_lines.append(f"- [{id_num:02d} {title}](#{anchor})")
    toc = "\n".join(toc_lines)

    # ---- Build body sections ----
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    body_parts = [
        "# 🥗 Master Nutritional Database",
        f"> **Last Updated:** {timestamp}",
        "> This file is auto-generated from `individual_food_data/`. Do not edit manually.",
        "",
    ]

    for (id_num, title, anchor), md_file in zip(entries, md_files):
        content = md_file.read_text(encoding="utf-8")
        # Use an explicit HTML anchor tag so TOC links are guaranteed to work
        body_parts.append(f'<a name="{anchor}"></a>')
        body_parts.append(f"## {id_num:02d} {title}")
        body_parts.append(strip_h1(content))
        body_parts.append("---")

    final_content = toc + "\n\n---\n\n" + "\n\n".join(body_parts)

    MASTER_FILE.write_text(final_content, encoding="utf-8")
    print(f"Successfully consolidated {len(md_files)} files into {MASTER_FILE}")


if __name__ == "__main__":
    consolidate_nutrition()
