"""
user_profile.py — Thin wrapper around db.py for user profile logic.
Keeps app.py clean.
"""

from db import save_profile, load_profile
from calorie_calc import full_calculation


def create_or_update_profile(
    name: str,
    age: int,
    weight_kg: float,
    height_cm: float,
    gender: str,
    activity: str,
    goal: str,
) -> dict:
    """
    Calculate calories and persist the profile to SQLite.
    Returns the complete profile dict including calorie_goal and macros.
    """
    calc = full_calculation(weight_kg, height_cm, age, gender, activity, goal)
    save_profile(
        name, age, weight_kg, height_cm, gender, activity, goal, calc["goal_cal"]
    )
    return {
        "name":       name,
        "age":        age,
        "weight_kg":  weight_kg,
        "height_cm":  height_cm,
        "gender":     gender,
        "activity":   activity,
        "goal":       goal,
        "calorie_goal": calc["goal_cal"],
        **calc,
    }


def get_profile() -> dict | None:
    """Load the saved profile, or None if not set up yet."""
    return load_profile()


def profile_summary(profile: dict) -> str:
    """Return a one-line human-readable summary of the profile."""
    return (
        f"👤 {profile['name']} · "
        f"{profile['age']} yrs · "
        f"{profile['weight_kg']} kg · "
        f"{profile['height_cm']} cm · "
        f"{profile['gender']} · "
        f"Goal: {profile['goal']} · "
        f"🎯 {profile['calorie_goal']:.0f} kcal/day"
    )