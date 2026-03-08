# MyNutritionalDatabase 🥗

A structured, AI-agent-powered repository for converting food nutrition labels into high-quality Markdown data.

## 🚀 The Core Concept

Unlike traditional databases, this project is designed to be managed by **LLM-based Agents** (like GitHub Copilot, Cursor, or OpenCode). The heart of the project is `AGENTS.md`, which contains the "System Instructions" for an AI to act as a data entry clerk, OCR processor, and file manager.

## 📂 Project Structure

- `individual_food_data/`: Processed data files containing structured tables (tracked by Git).
- `source_images/`: Folder for raw photos (gitignored, contains `.gitkeep` to maintain folder structure).
- `generate_nutrition_master_from_individual.py`: Python script to merge all individual food data into a single master file.
- `NUTRITION_MASTER.md`: Auto-generated consolidated file containing all foods (for AI consumption).
- `MENU.md`: User-defined meal templates combining multiple ingredients.
- `COACH_INSTRUCTIONS.md`: System prompt for an external "Coach AI" to track intake.
- `all_food_names.md`: A master index of all processed items.
- `AGENTS.md`: The "Source of Truth" for agent instructions.
- **Note on Images:** Raw nutrition label images (`IMG_*.jpg`, etc.) are processed by the agent but are **gitignored** in the `source_images/` directory to protect privacy and keep the repository size small.

## 🥗 How to Use the Coach System

This repository is designed to work with a "Coach AI" (like ChatGPT, Claude, or a local LLM).

### 1. Set Up Your Menu (`MENU.md`)

Human users should define their recurring meals in `MENU.md`.

- **Format**: Use a `## Meal Name` heading followed by a list of `- Ingredient Name: Xg`.
- **Tip**: Use **ingredient** names that match or closely resemble the ones in `all_food_names.md` for better accuracy.

### 2. Activate the Coach (`COACH_INSTRUCTIONS.md`)

To start tracking your nutrition:

1. Open a new chat with your preferred AI.
2. **Upload/Paste** the contents of `COACH_INSTRUCTIONS.md`, `MENU.md`, and `NUTRITION_MASTER.md`.
3. Tell the AI: _"You are my Nutritional Coach. I'll report what I eat, and you'll track it using these files."_

### 3. Report Your Intake

Simply tell the Coach what you ate (e.g., _"I had a Greek Yogurt Bowl for breakfast, but with 200g of yogurt instead of 180g"_). The Coach will:

- Look up the meal in your **Menu**.
- Calculate macros/micros using your **Master Database**.
- Scale the portions automatically.
- Provide a summary of your daily goals and warnings (like high sodium).

## 🤖 Workflow: How to Process New Nutrition Table Images (adding new nutrition data)

This repository is optimized for use with a coding agent. To add new data:

1. **Add a Photo:** Drop a new `IMG_XXXX.jpg` into the `source_images/` folder.
2. **Invoke the Agent:** Ask your AI agent (e.g., "process the new image").
3. **The Agent's Task:**
   - The agent reads `AGENTS.md` to understand the naming convention and table format.
   - It performs OCR on the image to extract calories, macros (fat, carbs, protein), and DV%.
   - It identifies sub-components (like Saturated Fat or Fiber) and tags them correctly in the "Component of" column.
   - It renames the image (locally) and creates a matching `.md` file in `individual_food_data/`.
   - It updates `all_food_names.md` with the new entry.
4. **Auto-Consolidation:** The agent runs `python generate_nutrition_master_from_individual.py` to update `NUTRITION_MASTER.md` with the latest data.

## ⚖️ License

This project is licensed under the **MIT License**. This covers both the structured nutritional data and the unique agent-based processing workflow defined in `AGENTS.md`.
