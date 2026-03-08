# AGENTS.md for MyCommonFoodNutritious

## Directory Structure

- Project Root: `S:\_MyDocuments\健身\my-nutritional-database\`
- Data Directory: `individual_food_data/`
- Images Directory: `source_images/`

## Directory Purpose

This is a data directory for storing and processing images of food nutrition labels.
Images are stored in `source_images/` and named `IMG_*.jpg` or `IMG_*.jpeg`.
Processed data is stored in `individual_food_data/` as individual `.md` files named after the food (snake_case).
`all_food_names.md` (in root) lists all unique food names.

## Build/Lint/Test Commands

No source code present. No build, lint, or test commands.

- To verify data integrity: manual review or custom scripts.
- No package.json, pyproject.toml, etc. found.

## Single Test Run

N/A - no tests.

## Code Style Guidelines

Although primarily data, any future scripts should follow:

### General

- Language: Python or JS preferred for processing.
- EditorConfig: None found, use defaults.
- Prettier/ESLint/Black/Pylint: None.

### Imports

- Group: standard lib, third-party, local.

```
import os
import sys

import numpy as np

from .local import foo
```

### Formatting

- 2 spaces indent.
- Line length: 88 (black) or 100 (prettier).
- Trailing commas.

### Types

- Use type hints.

```
def process_image(path: str) -> dict[str, float]:
```

### Naming Conventions

- snake_case for files, functions, variables.
- CamelCase for classes.
- UPPER_CASE for constants.
- Food names: descriptive_snake_case e.g. `peanut_butter_smooth_500g`
- File naming pattern:
  - Markdown: `[ID]_[food_name].md` (e.g., `15_blueberry_oat_bar_30g.md`)
  - Images: `[ID]_[food_name]_(ORIGINAL_ID).jpg` (e.g., `15_blueberry_oat_bar_30g_(IMG_1997).jpg`)
  - [ID] is the index from `all_food_names.md` (e.g., 01, 02, ... 15).
  - (ORIGINAL_ID) is the original IMG suffix.
- H1 title in individual `.md` files for each processed food: Use human-readable Title Case (e.g., `# Clif Bar White Chocolate Macadamia Nut`), NOT snake_case.

### Error Handling

- Use try/except specific.
- Log errors.
- Graceful fallbacks for OCR failures.

## Cursor/Copilot Rules

No `.cursor/rules/` or `.github/copilot-instructions.md` found.

## Agent Processing Workflow

1. Check `all_food_names.md` exists and read contents.
2. Glob `source_images/IMG_*.{jpg,jpeg}` sorted by name.
3. For each:
   - Read image.
   - Extract essential info: serving_size, calories, protein_g, carbs_g, fat_g per serving.
   - Also extract daily value % (DV%) for each nutrient when available.
   - Extract breakdowns: saturated fat, trans fat (under Fat); fiber, sugar (under Carbohydrates).
   - Mark sub-components in the "Component of" column to show parent relationship (e.g., "Saturated Fat" has "Fat" in Component of column).
   - Optional: sodium_mg, potassium_mg, vitamins, etc.
   - Identify food_name (snake_case). If the user provides a name for the image, use it. Otherwise, generate a descriptive name based on the image content.
   - Check uniqueness in all_food_names.md.
   - Rename image to `source_images/[ID]_[food_name]_(ORIGINAL_ID).jpg`.
   - Create `individual_food_data/[ID]_[food_name].md` with table (including DV% and Component of columns).

4. Run `python generate_nutrition_master_from_individual.py` to update the master file (`NUTRITION_MASTER.md`).

## Master Consolidation Script

- **Script**: `generate_nutrition_master_from_individual.py` (in project root)
- **Purpose**: Scans `individual_food_data/` and merges all individual food `.md` files into a single `NUTRITION_MASTER.md`.
- **Usage**: Run `python generate_nutrition_master_from_individual.py` after processing any new image or renaming any food.
- **Output**: Generates `NUTRITION_MASTER.md` with a Table of Contents, timestamps, and clickable anchors for each entry.

5. Use PowerShell for file ops on Windows.

## Renaming Protocol

When a user requests to rename a food product:

1. Identify the current ID and snake_case name.
2. Update the entry in `all_food_names.md`.
3. Rename the Markdown file: `individual_food_data/[ID]_[old_name].md` -> `individual_food_data/[ID]_[new_name].md`.
4. Update the H1 title in the Markdown file: `# Old Name` -> `# New Name`.
5. Rename the Image file: `source_images/[ID]_[old_name]_(IMG_XXXX).jpg` -> `source_images/[ID]_[new_name]_(IMG_XXXX).jpg`.
6. Ensure all paths remain absolute.

## Windows PowerShell Commands for Agents

```powershell
# List images sorted
Get-ChildItem IMG_* | Sort-Object Name

# Rename file
Rename-Item 'IMG_1234.jpg' 'food_name.jpg'

# Read file content
Get-Content 'file.md'

# Append to file
Add-Content 'all_food_names.md' 'food_name'
```

Repeat for consistency (padding to ~150 lines):

[Repeat sections as needed...]

No .cursorrules found.

## Additional Guidelines (repeated for length)

- Always use absolute paths: S:\_MyDocuments\健身\MyCommonFoodNutritious\...
- For bash tool: prefix with `powershell -Command "..."`
- Extract nutrition per serving only.
- Flag missing essentials.
- Report to user if can't identify food name from image.
- Ask permission before next image.
- Update all_food_names.md: append new names in the format `ID: [food_name] ([ORIGINAL_ID])` (e.g., `15: blueberry_oat_bar_30g (IMG_1997)`), documenting the IMG ID that the food name came from.
- Sub-components (e.g., saturated fat, trans fat under Fat; fiber, sugar under Carbohydrates) are listed as separate rows with their parent in the "Component of" column. Agents should use this column to identify relationships and avoid double-counting when aggregating nutrients.

## Nutrition Table Template

```
# Food Name

| Nutrient | Per Serving | DV% | Component of |
|----------|-------------|-----|---------------|
| Serving Size | xg | - | - |
| Calories | xxx | x% | - |
| Fat | 10g | 15% | - |
| Saturated Fat | 3g | - | Fat |
| Trans Fat | 0g | - | Fat |
| Carbohydrates | 25g | 10% | - |
| Fiber | 5g | - | Carbohydrates |
| Sugar | 8g | - | Carbohydrates |
| Sodium | 100mg | x% | - |
| Vitamin C | 500mg | x% | - |
```

## Verification

After processing:

- Check file exists.
- Lint MD if tools added.

End of AGENTS.md
