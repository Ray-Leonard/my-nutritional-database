#!/usr/bin/env python3
"""
Migration Script: Sequential ID → Timestamp Prefixes

Migrates:
1. individual_food_data/*.md files: [ID]_ → [YYYYMMDD_HHMMSS]_
2. source_images/* files: same rename (skip if empty)
3. all_food_names.md: rewrite entries from "ID: food_name (IMG_XXXX)" → "YYYYMMDD_HHMMSS: food_name"
4. generate_nutrition_master_from_individual.py: update ID extraction regex
"""

import re
import os
import shutil
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "individual_food_data"
IMAGES_DIR = BASE_DIR / "source_images"
ALL_FOOD_NAMES = BASE_DIR / "all_food_names.md"
SCRIPT = BASE_DIR / "generate_nutrition_master_from_individual.py"

# ─── Step 1: Rename individual_food_data files ─────────────────────────────────

print("=== Step 1: Rename individual_food_data files ===")

# Map old ID → new timestamp (from mtime)
id_to_ts = {}
renamed = []

for filepath in sorted(DATA_DIR.glob("*.md")):
    old_name = filepath.name
    m = re.match(r"^(\d+)_(.+)\.md$", old_name)
    if not m:
        print(f"  SKIP (no ID match): {old_name}")
        continue

    old_id = int(m.group(1))
    food_name = m.group(2)

    # Generate timestamp from mtime
    mtime = filepath.stat().st_mtime
    ts = datetime.fromtimestamp(mtime).strftime("%Y%m%d_%H%M%S")
    new_name = f"{ts}_{food_name}.md"
    new_path = filepath.parent / new_name

    filepath.rename(new_path)
    id_to_ts[old_id] = ts
    renamed.append((old_id, old_name, ts, new_name))
    print(f"  {old_name} → {new_name}")

print(f"  Renamed {len(renamed)} files, mapped {len(id_to_ts)} IDs")

# ─── Step 2: Rename source_images (skip if empty) ─────────────────────────────

print("\n=== Step 2: Rename source_images ===")

image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
image_files = [f for f in IMAGES_DIR.iterdir() if f.suffix.lower() in image_extensions and f.name != ".gitkeep"]

if not image_files:
    print("  SKIP: source_images is empty")
else:
    for filepath in sorted(image_files):
        old_name = filepath.name
        # Old pattern: [ID]_[food_name]_(IMG_XXXX).ext
        m = re.match(r"^(\d+)_(.+?)_(IMG_\d+)\.(\w+)$", old_name, re.IGNORECASE)
        if not m:
            print(f"  SKIP (no match): {old_name}")
            continue

        old_id = int(m.group(1))
        food_name = m.group(2)
        img_ext = m.group(4).lower()

        mtime = filepath.stat().st_mtime
        ts = datetime.fromtimestamp(mtime).strftime("%Y%m%d_%H%M%S")
        new_name = f"{ts}_{food_name}.{img_ext}"
        new_path = filepath.parent / new_name

        filepath.rename(new_path)
        print(f"  {old_name} → {new_name}")

    print(f"  Renamed {len(image_files)} image files")

# ─── Step 3: Rewrite all_food_names.md ────────────────────────────────────────

print("\n=== Step 3: Rewrite all_food_names.md ===")

lines = ALL_FOOD_NAMES.read_text(encoding="utf-8").splitlines()
new_lines = []

# Parse patterns:
#   Normal:  "44: peanut_butter (IMG_2361)"
#   Bugged:  "48: 48: great_value_diced_tomatoes (IMG_2381)"
#   No IMG:  "32: clover_leaf_chili_can_tuna_small (2296)"
#
# Strategy: take FIRST number as ID, take LAST ":"-separated field as food_name
#   Normal:  "44: peanut_butter (IMG_2361)"  → ID=44, name="peanut_butter (IMG_2361)"
#   Bugged:  "48: 48: great_value_diced_tomomas (IMG_2381)" → ID=48, name="great_value_diced_tomatoes (IMG_2381)"
#   No IMG:  "32: clover_leaf_chili_can_tuna_small (2296)"  → ID=32, name="clover_leaf_chili_can_tuna_small (2296)"
#
# Then strip trailing "(IMG_XXXX)" or "(XXXX)" from name

parsed_count = 0
skipped = []

for line in lines:
    original = line.strip()
    if not original:
        continue

    # Extract the first integer ID
    id_m = re.match(r"^(\d+):", original)
    if not id_m:
        print(f"  SKIP (no ID): {original}")
        skipped.append(original)
        new_lines.append(original)
        continue

    old_id = int(id_m.group(1))

    # Extract food name: everything after the first ": "
    rest = original[id_m.end():].strip()  # "peanut_butter (IMG_2361)" or "48: great_value_diced_tomatoes (IMG_2381)"

    # If rest starts with another "ID:", skip that prefix
    if re.match(r"^\d+:", rest):
        rest = re.sub(r"^\d+:\s*", "", rest)

    # Strip trailing "(IMG_XXXX)" or "(XXXX)" from name
    food_name = re.sub(r"\s+\(IMG_\d+\)$", "", rest, flags=re.IGNORECASE)
    food_name = re.sub(r"\s+\(\d+\)$", "", food_name)
    food_name = food_name.strip()

    if old_id in id_to_ts:
        ts = id_to_ts[old_id]
        new_line = f"{ts}: {food_name}"
        new_lines.append(new_line)
        print(f"  {original} → {new_line}")
        parsed_count += 1
    else:
        print(f"  WARN: ID {old_id} not in rename map, keeping: {original}")
        skipped.append(original)
        new_lines.append(original)

ALL_FOOD_NAMES.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
print(f"  Wrote {len(new_lines)} entries ({parsed_count} migrated, {len(skipped)} kept as-is)")

# ─── Step 4: Rewrite generate_nutrition_master_from_individual.py ───────────────

print("\n=== Step 4: Rewrite generate_nutrition_master_from_individual.py ===")

old_script = SCRIPT.read_text(encoding="utf-8")

# Build new script
new_script_lines = []

for line in old_script.splitlines(keepends=True):
    # Replace extract_id → extract_timestamp
    if "def extract_id(filename: str) -> int:" in line:
        new_script_lines.append("def extract_timestamp(filename: str) -> str:\n")
        continue
    # Replace the return statement inside extract_id
    if '    match = re.match(r"(\\d+)_", filename)' in line:
        new_script_lines.append('    match = re.match(r"(\\d{8}_\\d{6})_(.+)\\.md$", filename)\n')
        new_script_lines.append('    return match.group(1) if match else ""\n')
        continue
    if "    return int(match.group(1)) if match else -1" in line:
        # Skip this line (it's the old return)
        continue

    # Replace sort key
    if "key=lambda f: extract_id(f.name)" in line:
        new_script_lines.append(line.replace("extract_id", "extract_timestamp"))
        continue

    # Replace type annotations and comments referencing id_num
    if "id_num: int" in line:
        new_script_lines.append(line.replace("id_num: int", "timestamp: str"))
        continue
    if "id_num:02d" in line:
        new_script_lines.append(line.replace("id_num:02d", "timestamp"))
        continue
    if "id_num" in line and ("entries" in line or "anchor" in line):
        new_script_lines.append(line.replace("id_num", "timestamp"))
        continue

    new_script_lines.append(line)

new_script = "".join(new_script_lines)

# Verify key changes were made
checks = [
    ("extract_timestamp" in new_script, "extract_timestamp function present"),
    ('r"(\\d{8}_\\d{6})_(.+)\\.md$"' in new_script, "timestamp regex present"),
    ("extract_timestamp(f.name)" in new_script, "sort uses extract_timestamp"),
    ("timestamp: str" in new_script, "type annotation updated"),
]

all_ok = True
for condition, desc in checks:
    status = "✅" if condition else "❌"
    print(f"  {status} {desc}")
    if not condition:
        all_ok = True  # Don't fail, just report

SCRIPT.write_text(new_script, encoding="utf-8")
print("  Script updated")

# ─── Summary ──────────────────────────────────────────────────────────────────

print("\n=== Migration Summary ===")
print(f"  Files renamed: {len(renamed)}")
print(f"  ID→Timestamp mappings created: {len(id_to_ts)}")
print(f"  all_food_names entries migrated: {parsed_count}")
print(f"  entries skipped/kept: {len(skipped)}")
print("\nSample mappings:")
for old_id, old_name, ts, new_name in renamed[:5]:
    print(f"    ID {old_id:>3} ({old_name}) → {ts} ({new_name})")
if len(renamed) > 5:
    print(f"    ... and {len(renamed) - 5} more")
if skipped:
    print(f"\nSkipped entries (review manually):")
    for s in skipped:
        print(f"    {s}")
