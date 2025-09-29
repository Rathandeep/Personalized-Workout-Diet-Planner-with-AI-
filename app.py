from flask import Flask, render_template, request, jsonify
from planner import generate_workout, generate_meal_plan, explain_plan

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    # basic validation
    required = ['name','age','gender','height_cm','weight_kg','goal','activity_level','cuisine','budget_per_day']
    for r in required:
        if r not in data:
            return jsonify({"error": f"missing field {r}"}), 400

    workout = generate_workout(data)
    meal_plan = generate_meal_plan(data)
    explanation = explain_plan(data, workout, meal_plan)
    return jsonify({
        "workout": workout,
        "meal_plan": meal_plan,
        "explanation": explanation
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
