# MyNutritionalDatabase 🥗

A structured, AI-agent-powered food nutrition database. Designed to be managed by **LLM-based Agents** via the Hermes skill system.

## Project Structure

```
my-nutritional-database/
├── nutrition-database-management/    # Agent skill modules
│   ├── SKILL.md                      # Skill router (for Hermes)
│   └── modules/
│       ├── food-image-processor.md  # Add food from image
│       ├── food-deleter.md          # Remove food entry
│       ├── food-renamer.md          # Rename food entry
│       └── menu-manager.md          # Manage meal templates
├── individual_food_data/             # Processed food data (Markdown tables)
├── source_images/                   # Raw nutrition label photos
├── NUTRITION_MASTER.md              # Auto-generated consolidated view
├── all_food_names.md                # Master index of all foods
└── generate_nutrition_master_from_individual.py  # Rebuild NUTRITION_MASTER.md
```

## How It Works

This project is managed by the **Training Coach** agent system. When you ask the agent to help with food database tasks, it loads the `nutrition-database-management` skill and routes your request to the appropriate module.

### Available Operations

| You say | Agent does |
|---------|-----------|
| "Add this food" (with image) | Extracts nutrition data, saves to database, commits |
| "Delete [food name]" | Confirms, removes files, updates index, commits |
| "Rename [food]" | Confirms old/new names, renames files, commits |
| "Update my menu" | Validates ingredients, updates MENU.md, commits |
| "List all foods" | Shows all entries (read-only, no changes) |

## Naming Convention

Every food entry uses a **timestamp prefix**:

```
individual_food_data/20260407_090339_laozhengzhou_huimian_beef_flavor_115g.md
source_images/20260407_090339_laozhengzhou_huimian_beef_flavor_115g.jpg
all_food_names.md entry: 20260407_090339: laozhengzhou_huimian_beef_flavor_115g
```

Food names are in `snake_case`, with weight/size included when relevant.

## Data Format

Each food entry in `individual_food_data/` is a Markdown table:

```markdown
# Food Name (Title Case)

| Nutrient      | Per Serving | DV% | Component of  |
| ------------- | ----------- | --- | ------------- |
| Serving Size  | 115g        | -   | -             |
| Calories      | 450         | 23% | -             |
| Fat           | 18g         | 28% | -             |
| Saturated Fat | 3g          | -   | Fat           |
| Carbohydrates | 58g         | 21% | -             |
| Fiber         | 2g          | -   | Carbohydrates |
| Protein       | 15g         | 30% | -             |
| Sodium        | 800mg       | 35% | -             |
```

Sub-components (Saturated Fat, Fiber, etc.) are tagged with their parent nutrient to avoid double-counting.

## Workflow: Adding a New Food

1. **Send an image** of the nutrition label to the agent
2. Agent uses vision to extract text and nutrition data
3. Agent asks you to confirm the food name (follows snake_case convention)
4. Agent checks for duplicates in the database
5. Agent creates the `.md` file and renames the image with timestamp prefix
6. Agent updates `all_food_names.md` and runs consolidation
7. Agent commits the changes (reports commit hash — you push when ready)

## MENU.md (Meal Templates)

Managed separately by the `menu-manager` module. Not part of the food database — stores your personal meal templates with ingredients and gram amounts.

## License

MIT
