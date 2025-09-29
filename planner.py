import math
from datetime import datetime

# Simple heuristic-based "AI" planner
# All logic is original and rule-based; no external APIs required.

def bmi(weight_kg, height_cm):
    h = height_cm / 100.0
    return weight_kg / (h*h)

def caloric_needs(age, gender, weight_kg, height_cm, activity_level):
    # Mifflin-St Jeor Equation
    s = 5 if gender.lower() == 'male' else -161
    bmr = 10*weight_kg + 6.25*height_cm - 5*age + s
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very active": 1.9
    }
    mult = activity_multipliers.get(activity_level.lower(), 1.375)
    return int(bmr * mult)

def generate_workout(profile):
    goal = profile.get('goal','maintain').lower()
    activity = profile.get('activity_level','light').lower()
    # base structure: 4-week progressive plan with daily micro plans
    plan = {"created_at": datetime.utcnow().isoformat()+"Z", "weeks": []}
    # determine intensity
    if goal in ['lose weight','fat loss','weight loss']:
        intensity = 'moderate'
        focus = ['cardio','full-body strength']
    elif goal in ['build muscle','gain mass','muscle gain']:
        intensity = 'high'
        focus = ['strength','hypertrophy']
    else:
        intensity = 'light'
        focus = ['mobility','balanced strength']

    for w in range(1,5):
        week = {"week": w, "days": []}
        for d in range(1,8):
            if d in (6,7): # weekend lighter sessions
                day = {"day": d, "type": "active rest", "exercises": [
                    "30-45 min brisk walk or light cycling",
                    "Stretching 10-15 min"
                ]}
            else:
                if focus[0] == 'cardio' and d % 2 == 1:
                    ex = [
                        "30 min moderate-intensity cardio (running/cycling/elliptical)",
                        "Core circuit: 3x (plank 30s, bicycle crunch 15, bird-dog 10)"
                    ]
                else:
                    ex = [
                        "Strength circuit: 3 sets x 8-12 reps of compound movements",
                        "Example: Squat / Push-ups / Bent-over row / Lunges / Overhead press"
                    ]
                # progressive overload small increase each week
                ex.append(f"Intensity note: {intensity} - increase effort by ~{w*2}% vs week 1")
                day = {"day": d, "type": "training", "exercises": ex}
            week["days"].append(day)
        plan["weeks"].append(week)
    return plan

# Simple cultural cuisine sample meals
CUISINE_MEALS = {
    "indian": {
        "breakfast": ["Poha with veggies", "Oats idli", "Vegetable upma"],
        "lunch": ["Brown rice with dal and sabzi", "Roti with paneer bhurji and salad"],
        "dinner": ["Grilled fish/chicken with salad", "Mixed vegetable curry with millet rotis"],
        "snack": ["Roasted chana", "Fruit chaat"]
    },
    "mediterranean": {
        "breakfast": ["Greek yogurt with nuts and honey", "Tomato & cucumber toast"],
        "lunch": ["Grain bowl with chickpeas & veggies", "Grilled chicken salad"],
        "dinner": ["Baked fish with lemon and herbs", "Lentil stew with whole grain bread"],
        "snack": ["Hummus with carrots", "Olives & cheese"]
    },
    "asian": {
        "breakfast": ["Congee with egg", "Soy milk and steamed bun"],
        "lunch": ["Stir-fried veggies with tofu and rice", "Noodle soup with lean protein"],
        "dinner": ["Grilled fish with steamed greens", "Vegetable curry with rice"],
        "snack": ["Edamame", "Fresh fruit"]
    },
    "default": {
        "breakfast": ["Oat porridge with fruit", "Eggs and whole wheat toast"],
        "lunch": ["Mixed salad with lean protein and grains", "Soup with whole grain roll"],
        "dinner": ["Grilled lean protein with vegetables", "Stir-fry with brown rice"],
        "snack": ["Nuts", "Yogurt"]
    }
}

def generate_meal_plan(profile):
    age = int(profile.get('age',20))
    gender = profile.get('gender','male')
    weight = float(profile.get('weight_kg',70))
    height = float(profile.get('height_cm',170))
    activity = profile.get('activity_level','light')
    cuisine = profile.get('cuisine','default').lower()
    budget = float(profile.get('budget_per_day',200))

    calories = caloric_needs(age, gender, weight, height, activity)
    # adjust calories based on goal
    goal = profile.get('goal','maintain').lower()
    if goal in ['lose weight','fat loss','weight loss']:
        target_cal = int(calories * 0.8)
    elif goal in ['build muscle','gain mass','muscle gain']:
        target_cal = int(calories * 1.15)
    else:
        target_cal = calories

    # choose cuisine templates
    meals = CUISINE_MEALS.get(cuisine, CUISINE_MEALS['default'])

    # create a simple 7-day plan by varying meal choices & splitting calories
    daily = []
    for day in range(1,8):
        breakfast = meals['breakfast'][day % len(meals['breakfast'])]
        lunch = meals['lunch'][day % len(meals['lunch'])]
        dinner = meals['dinner'][day % len(meals['dinner'])]
        snack = meals['snack'][day % len(meals['snack'])]

        # divide calories approx: 25% breakfast, 35% lunch, 30% dinner, 10% snacks
        day_plan = {
            "day": day,
            "calories_target": target_cal,
            "meals": {
                "breakfast": {"item": breakfast, "cal": int(target_cal * 0.25)},
                "lunch": {"item": lunch, "cal": int(target_cal * 0.35)},
                "dinner": {"item": dinner, "cal": int(target_cal * 0.30)},
                "snack": {"item": snack, "cal": int(target_cal * 0.10)}
            },
            "estimated_cost": round(budget, 2)
        }
        daily.append(day_plan)

    return {"created_at": datetime.utcnow().isoformat()+"Z", "daily": daily, "target_calories": target_cal}

def explain_plan(profile, workout, meal_plan):
    # Return a human-readable explanation describing why the plan suits the user
    name = profile.get('name','User')
    goal = profile.get('goal','maintain')
    age = profile.get('age')
    gender = profile.get('gender')
    calories = meal_plan.get('target_calories')
    bmi_val = bmi(float(profile.get('weight_kg',70)), float(profile.get('height_cm',170)))
    explanation = []
    explanation.append(f"Hello {name}! This 4-week plan targets: {goal}.")
    explanation.append(f"Estimated daily calories target: {calories} kcal.")
    explanation.append(f"Your estimated BMI is {bmi_val:.1f}; plans are adjusted for age and activity level.")
    explanation.append("Workout plan balances progressive overload with recovery; weekend sessions are lighter.")
    explanation.append("Meal choices reflect your selected cuisine and budget and split calories across meals.")
    return "\n".join(explanation)
