# MyNutritionalDatabase 🥗

A structured, AI-agent-powered repository for converting food nutrition labels into high-quality Markdown data.

## 🚀 The Core Concept
Unlike traditional databases, this project is designed to be managed by **LLM-based Agents** (like GitHub Copilot, Cursor, or OpenCode). The heart of the project is `AGENTS.md`, which contains the "System Instructions" for an AI to act as a data entry clerk, OCR processor, and file manager.

## 📂 Project Structure
- `individual_food_data/`: Processed data files containing structured tables (tracked by Git).
- `source_images/`: Folder for raw photos (gitignored, contains `.gitkeep` to maintain folder structure).
- `generate_nutrition_master_from_individual.py`: Python script to merge all individual food data into a single master file.
- `NUTRITION_MASTER.md`: Auto-generated consolidated file containing all foods (for AI consumption).
- `all_food_names.md`: A master index of all processed items.
- `AGENTS.md`: The "Source of Truth" for agent instructions.
- **Note on Images:** Raw nutrition label images (`IMG_*.jpg`, etc.) are processed by the agent but are **gitignored** in the `source_images/` directory to protect privacy and keep the repository size small.

## 🤖 Workflow: How to Process New Images
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
