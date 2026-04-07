---
name: nutrition-database-management
description: "Central hub for nutrition database operations. Routes to sub-modules: food-image-processor, food-deleter, food-renamer, menu-manager."
version: 1.0.0
author: Cagoo 加拿大鹅 (Hermes Agent)
license: MIT
metadata:
  hermes:
    tags: [nutrition, database, food, menu, health]
    category: health
---


# Nutrition Database Management

## When to Use

This skill should be automatically loaded when the **Training Coach meta-agent** skill is invoked and the user requests any nutrition database operation, including:

- Adding a new food item (from an image or manual entry)
- Removing an existing food item from the database
- Viewing the current food database
- Managing or updating the user's meal menu (`MENU.md`)

This skill is a sub-skill of the Training Coach system. It is not triggered directly by the user — it is dispatched by the Training Coach meta-agent when database operations are needed.

> **Note**:
> - The Training Coach meta-agent skill is planned for future phases. Until then, this skill can be triggered directly when the user asks for any database operation listed in the Trigger Routing table below. But if you are the Training Coach meta-agent, you are loaded and please ignore this note and proceed with your work.

## Architecture

**Location** (absolute path): `~/workspace/training-coach/my-nutritional-database/nutrition-database-management/`

**Purpose**: Central routing hub for all nutrition database operations. Routes user requests to the appropriate sub-module.

```
nutrition-database-management/
├── SKILL.md                          ← This file (router)
├── modules/
│   ├── food-image-processor.md       ← Add new food from image
│   ├── food-deleter.md               ← Remove existing food
│   ├── food-renamer.md               ← Rename existing food entry
│   └── menu-manager.md               ← Manage MENU.md
└── references/                        # Static references
```

## Routing Rules

Read the user's request and route to the appropriate sub-module:

| User says | Sub-module |
|-----------|-----------|
| "process this image", "add food", "new food", "save this to database" | `modules/food-image-processor.md` |
| "delete food", "remove from database", "delete this entry" | `modules/food-deleter.md` |
| "list foods", "what's in the database", "show all foods" | `modules/food-deleter.md` (read-only mode) |
| "rename food", "rename this entry", "change the name of this food", "update food name" | `modules/food-renamer.md` |
| "update menu", "add to menu", "change my meals", "manage menu", "add a new meal" | `modules/menu-manager.md` |

## Shared Conventions

All sub-modules share these:

- **Database root**: `~/workspace/training-coach/my-nutritional-database/`
- **NUTRITION_MASTER.md**: single source of truth for individual item nutritions plus a easy-to-navigate TOC.
- **all_food_names.md**: Single source of truth for food name → file mapping

> ⚠️ **Path Resolution**: Sub-modules use relative paths (`./my-nutritional-database/`) relative to the skill location (`~/workspace/training-coach/my-nutritional-database/`). If this absolute path does not exist on the system, **do not guess** — ask the user to confirm or provide the correct path, and update this skill's documentation accordingly.

## Error Handling (shared)

| Error | Action |
|-------|--------|
| Food not found in database | Report alternatives, ask for clarification |
| File operation fails | Report error, suggest manual intervention |
| Ingredient missing from database (while using menu-manager) | Ask user whether Add it first before proceeding |
