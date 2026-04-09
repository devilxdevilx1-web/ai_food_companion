"""
calorie_calc.py — BMR / TDEE / Goal calorie calculations
Uses the Mifflin-St Jeor equation (most accurate for general population).
"""

# ── Activity multipliers ──────────────────────────────────────────────────────
ACTIVITY_MULTIPLIERS = {
    "Sedentary (little or no exercise)":         1.2,
    "Lightly active (1-3 days/week)":            1.375,
    "Moderately active (3-5 days/week)":         1.55,
    "Very active (6-7 days/week)":               1.725,
    "Extra active (physical job or 2x training)": 1.9,
}

# ── Goal adjustments (kcal/day) ───────────────────────────────────────────────
GOAL_ADJUSTMENTS = {
    "Lose weight":      -500,
    "Maintain weight":     0,
    "Gain muscle/weight": +300,
}


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Mifflin-St Jeor BMR formula.
    Male:   10*weight + 6.25*height - 5*age + 5
    Female: 10*weight + 6.25*height - 5*age - 161
    """
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if gender.lower() == "male" else base - 161


def calculate_tdee(bmr: float, activity: str) -> float:
    """Total Daily Energy Expenditure = BMR × activity multiplier."""
    multiplier = ACTIVITY_MULTIPLIERS.get(activity, 1.2)
    return bmr * multiplier


def calculate_goal_calories(tdee: float, goal: str) -> float:
    """Adjust TDEE based on the user's goal."""
    adjustment = GOAL_ADJUSTMENTS.get(goal, 0)
    return max(1200, tdee + adjustment)  # never below 1 200 kcal for safety


def full_calculation(weight_kg: float, height_cm: float, age: int,
                     gender: str, activity: str, goal: str) -> dict:
    """Run the full pipeline and return a dict with all values."""
    bmr  = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity)
    goal_cal = calculate_goal_calories(tdee, goal)
    return {
        "bmr":        round(bmr, 1),
        "tdee":       round(tdee, 1),
        "goal_cal":   round(goal_cal, 1),
        "macro_carbs": round(goal_cal * 0.50 / 4, 1),   # 50 % carbs  → grams
        "macro_fat":   round(goal_cal * 0.25 / 9, 1),   # 25 % fat    → grams
        "macro_prot":  round(goal_cal * 0.25 / 4, 1),   # 25 % protein→ grams
    }


def get_activity_options() -> list:
    return list(ACTIVITY_MULTIPLIERS.keys())


def get_goal_options() -> list:
    return list(GOAL_ADJUSTMENTS.keys())