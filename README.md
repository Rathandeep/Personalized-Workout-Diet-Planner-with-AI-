# Personalized Fitness Agent

This is an original, lightweight *Personalized Workout & Diet Planner* designed for students.
It uses rule-based heuristics to generate:
- A 4-week progressive workout plan.
- A 7-day culturally-aware meal plan that respects cuisine preference and budget.

## Features
- Personalized based on age, gender, height, weight, activity level, goal, cuisine, and budget.
- Runs locally in VS Code with no external API or paid keys required.
- Simple Flask web UI.

## How to run (VS Code)
1. Make sure you have Python 3.10+ installed.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:
   - Windows:
     ```
     python -m venv venv
     venv\Scripts\activate
     ```
   - macOS / Linux:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the app:
   ```
   python app.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

## Notes
- This project is original and intended for learning and demonstration purposes.
- If you want to extend it with a real AI backend (e.g., an LLM), do so with ethical use and proper API keys.
