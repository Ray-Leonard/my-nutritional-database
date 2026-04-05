# MyNutritionalDatabase 🥗

A structured, AI-agent-powered repository for converting food nutrition labels into high-quality Markdown data.

## 🚀 The Core Concept

Unlike traditional databases, this project is designed to be managed by **LLM-based Agents**. The heart of the project is `AGENTS.md`, which contains the "System Instructions" for an AI to act as a data entry clerk, OCR processor, and file manager.

This database is **pure food data only** — it stores and processes nutrition label images. Calculation, meal tracking, and coaching are handled by a separate system.

## 📂 Project Structure

| Path | Purpose |
|------|---------|
| `AGENTS.md` | Source of Truth — agent instructions for processing images |
| `individual_food_data/` | Processed data files as structured Markdown tables |
| `source_images/` | Raw nutrition label photos (gitignored) |
| `NUTRITION_MASTER.md` | Auto-generated consolidated file with all foods |
| `all_food_names.md` | Master index of all processed items |
| `generate_nutrition_master_from_individual.py` | Script to rebuild NUTRITION_MASTER.md |

## 🤖 Workflow: How to Process New Nutrition Table Images

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

MIT License.
