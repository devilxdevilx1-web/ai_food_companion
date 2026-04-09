from datetime import date, timedelta
import re

# ─────────────────────────────────────────
# DATE HELPERS
# ─────────────────────────────────────────
def today_str() -> str:
    return str(date.today())

def date_range(days: int) -> list:
    today = date.today()
    return [str(today - timedelta(days=i)) for i in range(days)]


# ─────────────────────────────────────────
# CALORIE COLOR LOGIC
# ─────────────────────────────────────────
def calorie_progress_color(consumed: float, goal: float):
    if goal <= 0:
        return "#4ade80"

    pct = consumed / goal

    if pct < 0.5:
        return "#4ade80"  # green
    elif pct < 0.85:
        return "#facc15"  # yellow
    elif pct <= 1.0:
        return "#fb923c"  # orange
    else:
        return "#f87171"  # red


# ─────────────────────────────────────────
# FORMAT CALORIES
# ─────────────────────────────────────────
def format_calories(cal: float) -> str:
    return f"{cal:.0f} kcal"


# ─────────────────────────────────────────
# BMI CALCULATION
# ─────────────────────────────────────────
def bmi_category(weight_kg: float, height_cm: float):
    h_m = height_cm / 100
    bmi = weight_kg / (h_m ** 2)

    if bmi < 18.5:
        cat = "Underweight"
    elif bmi < 25:
        cat = "Normal weight"
    elif bmi < 30:
        cat = "Overweight"
    else:
        cat = "Obese"

    return round(bmi, 1), cat


# ─────────────────────────────────────────
# FOOD MESSAGE DETECTOR (VERY IMPORTANT)
# ─────────────────────────────────────────
def is_food_log_message(text: str) -> bool:
    text = text.lower()

    keywords = [
        "ate", "had", "eat", "drank", "drink",
        "breakfast", "lunch", "dinner",
        "meal", "food", "snack"
    ]

    # detect numbers (like "2 rotis")
    has_number = bool(re.search(r"\d+", text))

    return any(k in text for k in keywords) or has_number