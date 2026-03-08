# MyNutritionalDatabase 🥗

A structured, AI-agent-powered repository for converting food nutrition labels into high-quality Markdown data.

## 🚀 The Core Concept
Unlike traditional databases, this project is designed to be managed by **LLM-based Agents** (like GitHub Copilot, Cursor, or OpenCode). The heart of the project is `AGENTS.md`, which contains the "System Instructions" for an AI to act as a data entry clerk, OCR processor, and file manager.

## 📂 Project Structure
- `[ID]_[food_name].md`: Processed data files containing structured tables.
- `all_food_names.md`: A master index of all processed items.
- `AGENTS.md`: The "Source of Truth" for how an AI agent should process new data.
- **Note on Images:** Raw nutrition label images (`IMG_*.jpg`, etc.) are processed by the agent but are **gitignored** to protect privacy and keep the repository size small. Only the structured Markdown data is tracked in version control.

## 🤖 Workflow: How to Process New Images
This repository is optimized for use with a coding agent. To add new data:

1. **Add a Photo:** Drop a new `IMG_XXXX.jpg` into the root directory.
2. **Invoke the Agent:** Ask your AI agent (e.g., "process the new image").
3. **The Agent's Task:**
   - The agent reads `AGENTS.md` to understand the naming convention and table format.
   - It performs OCR on the image to extract calories, macros (fat, carbs, protein), and DV%.
   - It identifies sub-components (like Saturated Fat or Fiber) and tags them correctly in the "Component of" column.
   - It renames the image (locally) and creates a matching `.md` file automatically.
   - It updates `all_food_names.md` with the new entry.

## ⚖️ License
This project is licensed under the **MIT License**. This covers both the structured nutritional data and the unique agent-based processing workflow defined in `AGENTS.md`.
