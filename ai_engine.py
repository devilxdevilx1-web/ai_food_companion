"""
ai_engine.py — AI engine that talks to Ollama (local LLM).

Flow:
  1. Build a rich system prompt with user context + food database knowledge.
  2. Send user message to Ollama /api/chat endpoint.
  3. Parse structured response (food list + calories).
  4. Fall back to the local food database when AI is unavailable.
"""

import json
import re
import requests
from food_database import search_food, get_calories_for_unit, FOOD_DB

OLLAMA_BASE   = "http://localhost:11434"
OLLAMA_MODEL  = "llama3.2"          # change to any model you have pulled
TIMEOUT       = 60                  # seconds to wait for Ollama response


# ── System prompt ─────────────────────────────────────────────────────────────

def build_system_prompt(user_profile: dict) -> str:
    name  = user_profile.get("name", "User")
    goal  = user_profile.get("goal", "maintain weight")
    cals  = user_profile.get("calorie_goal", 2000)
    # Give AI a small slice of the food DB so it can reason accurately
    sample_foods = "\n".join(
        f"  - {k}: ~{int(v['cal_per_100g'] * v['unit_grams'] / 100)} kcal per {v['typical_unit']}"
        for k, v in list(FOOD_DB.items())[:60]
    )

    return f"""You are NutriAI, a friendly and knowledgeable AI nutrition assistant.

USER PROFILE:
- Name: {name}
- Daily calorie goal: {cals} kcal
- Goal: {goal}

YOUR JOB:
When the user tells you what they ate, you must respond with ONLY a raw JSON object — no markdown, no backticks, no explanation text before or after. Just the JSON.

The JSON must have exactly this structure:
{{
  "foods": [
    {{"name": "food item", "quantity": "description", "calories": 123}},
    {{"name": "food item 2", "quantity": "description", "calories": 200}}
  ],
  "total_calories": 323,
  "message": "Friendly, motivating 1-2 sentence response mentioning remaining calories.",
  "meal_suggestions": ["suggestion 1", "suggestion 2", "suggestion 3"]
}}

DO NOT wrap in ```json``` or any code block. Output ONLY the raw JSON object, nothing else.

IMPORTANT RULES:
- Always use realistic Indian / international calorie values.
- If you don't know a food, make a reasonable estimate.
- Keep quantities in plain English (e.g., "2 pieces", "1 cup").
- The "message" should be warm, personal (use name {name}), mention remaining calories, and give one tip.
- meal_suggestions should be 2-3 appropriate next meals given their goal ({goal}).

REFERENCE CALORIE VALUES (per typical serving):
{sample_foods}
"""


# ── Ollama API call ───────────────────────────────────────────────────────────

def is_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def get_available_models() -> list:
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        pass
    return []


def chat_with_ollama(messages: list, system_prompt: str) -> str:
    """
    Send a conversation to Ollama and return the assistant's raw text reply.
    `messages` is a list of {"role": "user"/"assistant", "content": "..."}.
    """
    payload = {
        "model":    OLLAMA_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
        "stream":   False,
    }
    try:
        r = requests.post(
            f"{OLLAMA_BASE}/api/chat",
            json=payload,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return r.json()["message"]["content"]
    except requests.exceptions.ConnectionError:
        return None   # Ollama not running
    except Exception as e:
        return f"__ERROR__: {e}"


# ── JSON parser ───────────────────────────────────────────────────────────────

def extract_json_from_response(text: str) -> dict | None:
    """Pull the JSON block out of the AI's markdown-formatted reply."""
    # Try ```json ... ``` (standard)
    m = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Try ``` ... ``` (no language tag)
    m = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Try ``json ... `` (double backtick — some models do this)
    m = re.search(r"``json\s*(.*?)\s*``", text, re.DOTALL | re.IGNORECASE)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Try bare JSON object anywhere in the text
    m = re.search(r"\{[^{}]*\"foods\"[^{}]*\[.*?\].*?\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass

    # Last resort: find outermost { ... }
    start = text.find("{")
    end   = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass

    return None


# ── Fallback: pure local parsing ──────────────────────────────────────────────

_NUMBER_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3,
    "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
    "nine": 9, "ten": 10, "half": 0.5,
}


def _parse_quantity(token: str) -> float:
    token = token.strip().lower()
    if token in _NUMBER_WORDS:
        return _NUMBER_WORDS[token]
    try:
        return float(token)
    except ValueError:
        return 1.0


def local_food_parse(text: str, calorie_goal: float, consumed_so_far: float) -> dict:
    """
    Pure-Python fallback: parse food items from free text using the local DB.
    Returns the same structure as the AI JSON block.
    """
    text_lower = text.lower()
    found_foods = []

    # Sort DB keys by length descending so "aloo paratha" matches before "paratha"
    for food_key in sorted(FOOD_DB.keys(), key=len, reverse=True):
        if food_key in text_lower:
            # Try to find a number before this food name
            pattern = rf"(\d+\.?\d*|\b(?:{'|'.join(_NUMBER_WORDS.keys())})\b)?\s*{re.escape(food_key)}"
            m = re.search(pattern, text_lower)
            qty = 1.0
            if m and m.group(1):
                qty = _parse_quantity(m.group(1))
            calories = get_calories_for_unit(food_key, qty)
            found_foods.append({
                "name":     food_key.title(),
                "quantity": f"{qty:.0f}" if qty == int(qty) else f"{qty}",
                "calories": calories,
            })
            # Remove matched text to avoid double-counting
            text_lower = text_lower.replace(food_key, "___")

    if not found_foods:
        return {
            "foods": [],
            "total_calories": 0,
            "message": (
                "I couldn't identify any food items in your message. "
                "Try being more specific, e.g., '2 bananas and 1 dosa'."
            ),
            "meal_suggestions": [],
        }

    total = round(sum(f["calories"] for f in found_foods), 1)
    remaining = round(calorie_goal - consumed_so_far - total, 1)
    sign = "+" if remaining >= 0 else ""
    message = (
        f"Logged {total:.0f} kcal from {len(found_foods)} item(s). "
        f"You have {remaining:.0f} kcal remaining today "
        f"({'on track 🎯' if remaining >= 0 else 'over budget ⚠️'})."
    )
    return {
        "foods": found_foods,
        "total_calories": total,
        "message": message,
        "meal_suggestions": _default_suggestions(remaining),
    }


def _default_suggestions(remaining: float) -> list:
    if remaining > 600:
        return [
            "A balanced meal with rice, dal, and sabzi (~400 kcal)",
            "Grilled chicken breast with vegetables (~350 kcal)",
            "Roti with paneer curry (~450 kcal)",
        ]
    elif remaining > 300:
        return [
            "A light dal and sabzi with 1 roti (~300 kcal)",
            "Oats with fruits (~280 kcal)",
            "Vegetable soup with bread (~250 kcal)",
        ]
    else:
        return [
            "A small fruit salad (~100 kcal)",
            "1 glass of buttermilk (~60 kcal)",
            "A handful of almonds (~165 kcal)",
        ]


# ── Main entry point ──────────────────────────────────────────────────────────

def process_food_input(
    user_message: str,
    conversation_history: list,
    user_profile: dict,
    calories_consumed_today: float,
) -> dict:
    """
    Process a food log message.  Returns a structured dict:
    {
        "foods": [...],
        "total_calories": float,
        "message": str,
        "meal_suggestions": [...],
        "source": "ai" | "local",
    }
    """
    calorie_goal = float(user_profile.get("calorie_goal", 2000))
    remaining    = calorie_goal - calories_consumed_today

    # Build conversation for Ollama (add remaining calories to context)
    context_msg = (
        f"[Context: User has consumed {calories_consumed_today:.0f} kcal today, "
        f"{remaining:.0f} kcal remaining from their {calorie_goal:.0f} kcal goal]\n\n"
        f"{user_message}"
    )
    messages = conversation_history + [{"role": "user", "content": context_msg}]
    system   = build_system_prompt(user_profile)

    # Try Ollama first
    if is_ollama_running():
        raw = chat_with_ollama(messages, system)
        if raw and not raw.startswith("__ERROR__"):
            parsed = extract_json_from_response(raw)
            if parsed and "foods" in parsed and len(parsed["foods"]) > 0:
                parsed["source"] = "ai"
                # Ensure total_calories is a number
                if "total_calories" not in parsed or not parsed["total_calories"]:
                    parsed["total_calories"] = round(sum(
                        float(f.get("calories", 0)) for f in parsed["foods"]
                    ), 1)
                # Clean message — if it contains JSON, replace it
                msg = parsed.get("message", "")
                if not msg or "{" in msg or '"foods"' in msg or "```" in msg:
                    remaining_now = calorie_goal - calories_consumed_today - parsed["total_calories"]
                    parsed["message"] = (
                        f"Got it! Logged {parsed['total_calories']:.0f} kcal. "
                        f"You have {max(remaining_now, 0):.0f} kcal remaining today "
                        f"({'on track 🎯' if remaining_now >= 0 else 'over budget ⚠️'})."
                    )
                return parsed

    # Fallback to local database (also used when Ollama JSON parse fails)
    result = local_food_parse(user_message, calorie_goal, calories_consumed_today)
    result["source"] = "local"
    return result


def get_general_response(
    user_message: str,
    conversation_history: list,
    user_profile: dict,
) -> str:
    """
    For non-food questions (e.g. 'what should I eat?'), just pass through to Ollama.
    Returns plain text.
    """
    system   = build_system_prompt(user_profile)
    messages = conversation_history + [{"role": "user", "content": user_message}]
    if is_ollama_running():
        raw = chat_with_ollama(messages, system)
        if raw and not raw.startswith("__ERROR__"):
            return raw
    return (
        "Ollama is not running. Please start it with `ollama serve` in a terminal. "
        "I can still log your food using the local database."
    )