"""
food_database.py — Comprehensive local food database (calories per 100 g or per unit).
Structure:  { "food_name": {"cal_per_100g": X, "typical_unit": "...", "unit_grams": Y} }
"""

FOOD_DB = {
    # ── Fruits ────────────────────────────────────────────────────────────────
    "banana":           {"cal_per_100g": 89,  "typical_unit": "medium banana",  "unit_grams": 118},
    "apple":            {"cal_per_100g": 52,  "typical_unit": "medium apple",   "unit_grams": 182},
    "mango":            {"cal_per_100g": 60,  "typical_unit": "medium mango",   "unit_grams": 200},
    "orange":           {"cal_per_100g": 47,  "typical_unit": "medium orange",  "unit_grams": 131},
    "grapes":           {"cal_per_100g": 69,  "typical_unit": "cup of grapes",  "unit_grams": 92},
    "watermelon":       {"cal_per_100g": 30,  "typical_unit": "slice",          "unit_grams": 280},
    "papaya":           {"cal_per_100g": 43,  "typical_unit": "cup cubed",      "unit_grams": 140},
    "pineapple":        {"cal_per_100g": 50,  "typical_unit": "cup chunks",     "unit_grams": 165},
    "strawberry":       {"cal_per_100g": 32,  "typical_unit": "cup",            "unit_grams": 152},
    "blueberry":        {"cal_per_100g": 57,  "typical_unit": "cup",            "unit_grams": 148},
    "guava":            {"cal_per_100g": 68,  "typical_unit": "medium guava",   "unit_grams": 90},
    "pomegranate":      {"cal_per_100g": 83,  "typical_unit": "medium fruit",   "unit_grams": 282},
    "kiwi":             {"cal_per_100g": 61,  "typical_unit": "medium kiwi",    "unit_grams": 76},
    "lychee":           {"cal_per_100g": 66,  "typical_unit": "piece",          "unit_grams": 10},
    "avocado":          {"cal_per_100g": 160, "typical_unit": "half avocado",   "unit_grams": 100},

    # ── Vegetables ────────────────────────────────────────────────────────────
    "tomato":           {"cal_per_100g": 18,  "typical_unit": "medium tomato",  "unit_grams": 123},
    "onion":            {"cal_per_100g": 40,  "typical_unit": "medium onion",   "unit_grams": 110},
    "potato":           {"cal_per_100g": 77,  "typical_unit": "medium potato",  "unit_grams": 150},
    "sweet potato":     {"cal_per_100g": 86,  "typical_unit": "medium",         "unit_grams": 130},
    "carrot":           {"cal_per_100g": 41,  "typical_unit": "medium carrot",  "unit_grams": 61},
    "spinach":          {"cal_per_100g": 23,  "typical_unit": "cup",            "unit_grams": 30},
    "broccoli":         {"cal_per_100g": 34,  "typical_unit": "cup florets",    "unit_grams": 91},
    "cabbage":          {"cal_per_100g": 25,  "typical_unit": "cup shredded",   "unit_grams": 89},
    "cauliflower":      {"cal_per_100g": 25,  "typical_unit": "cup",            "unit_grams": 100},
    "peas":             {"cal_per_100g": 81,  "typical_unit": "cup",            "unit_grams": 145},
    "corn":             {"cal_per_100g": 86,  "typical_unit": "ear of corn",    "unit_grams": 77},
    "cucumber":         {"cal_per_100g": 16,  "typical_unit": "medium",         "unit_grams": 301},
    "bell pepper":      {"cal_per_100g": 31,  "typical_unit": "medium",         "unit_grams": 119},
    "eggplant":         {"cal_per_100g": 25,  "typical_unit": "cup cubed",      "unit_grams": 82},
    "mushroom":         {"cal_per_100g": 22,  "typical_unit": "cup sliced",     "unit_grams": 70},
    "garlic":           {"cal_per_100g": 149, "typical_unit": "clove",          "unit_grams": 3},
    "ginger":           {"cal_per_100g": 80,  "typical_unit": "teaspoon grated","unit_grams": 2},
    "drumstick":        {"cal_per_100g": 37,  "typical_unit": "pod",            "unit_grams": 20},
    "bitter gourd":     {"cal_per_100g": 17,  "typical_unit": "medium",         "unit_grams": 90},
    "bottle gourd":     {"cal_per_100g": 14,  "typical_unit": "cup cubed",      "unit_grams": 130},

    # ── Indian Staples & Street Food ─────────────────────────────────────────
    "dosa":             {"cal_per_100g": 168, "typical_unit": "plain dosa",     "unit_grams": 80},
    "masala dosa":      {"cal_per_100g": 190, "typical_unit": "masala dosa",    "unit_grams": 150},
    "idli":             {"cal_per_100g": 58,  "typical_unit": "idli piece",     "unit_grams": 60},
    "sambar":           {"cal_per_100g": 50,  "typical_unit": "cup",            "unit_grams": 240},
    "chapati":          {"cal_per_100g": 297, "typical_unit": "chapati",        "unit_grams": 45},
    "roti":             {"cal_per_100g": 297, "typical_unit": "roti",           "unit_grams": 45},
    "paratha":          {"cal_per_100g": 260, "typical_unit": "paratha",        "unit_grams": 80},
    "aloo paratha":     {"cal_per_100g": 280, "typical_unit": "aloo paratha",   "unit_grams": 110},
    "naan":             {"cal_per_100g": 310, "typical_unit": "naan bread",     "unit_grams": 90},
    "puri":             {"cal_per_100g": 340, "typical_unit": "puri",           "unit_grams": 35},
    "rice":             {"cal_per_100g": 130, "typical_unit": "cup cooked",     "unit_grams": 185},
    "brown rice":       {"cal_per_100g": 122, "typical_unit": "cup cooked",     "unit_grams": 195},
    "biryani":          {"cal_per_100g": 160, "typical_unit": "plate",          "unit_grams": 350},
    "dal":              {"cal_per_100g": 116, "typical_unit": "cup",            "unit_grams": 240},
    "dal tadka":        {"cal_per_100g": 120, "typical_unit": "cup",            "unit_grams": 240},
    "dal makhani":      {"cal_per_100g": 145, "typical_unit": "cup",            "unit_grams": 240},
    "rajma":            {"cal_per_100g": 127, "typical_unit": "cup",            "unit_grams": 240},
    "chole":            {"cal_per_100g": 140, "typical_unit": "cup",            "unit_grams": 240},
    "paneer":           {"cal_per_100g": 265, "typical_unit": "100g piece",     "unit_grams": 100},
    "paneer butter masala": {"cal_per_100g": 180, "typical_unit": "cup",       "unit_grams": 240},
    "palak paneer":     {"cal_per_100g": 150, "typical_unit": "cup",            "unit_grams": 240},
    "butter chicken":   {"cal_per_100g": 165, "typical_unit": "cup",            "unit_grams": 240},
    "chicken tikka masala": {"cal_per_100g": 155, "typical_unit": "cup",       "unit_grams": 240},
    "fish curry":       {"cal_per_100g": 130, "typical_unit": "cup",            "unit_grams": 240},
    "egg curry":        {"cal_per_100g": 150, "typical_unit": "cup with 2 eggs","unit_grams": 250},
    "upma":             {"cal_per_100g": 120, "typical_unit": "cup",            "unit_grams": 200},
    "poha":             {"cal_per_100g": 180, "typical_unit": "cup",            "unit_grams": 200},
    "pongal":           {"cal_per_100g": 150, "typical_unit": "cup",            "unit_grams": 220},
    "khichdi":          {"cal_per_100g": 120, "typical_unit": "cup",            "unit_grams": 240},
    "curd rice":        {"cal_per_100g": 130, "typical_unit": "cup",            "unit_grams": 240},
    "lemon rice":       {"cal_per_100g": 150, "typical_unit": "cup",            "unit_grams": 200},
    "tamarind rice":    {"cal_per_100g": 165, "typical_unit": "cup",            "unit_grams": 200},
    "samosa":           {"cal_per_100g": 262, "typical_unit": "samosa",         "unit_grams": 65},
    "vada":             {"cal_per_100g": 285, "typical_unit": "medu vada",      "unit_grams": 55},
    "pakora":           {"cal_per_100g": 290, "typical_unit": "piece",          "unit_grams": 25},
    "bhel puri":        {"cal_per_100g": 160, "typical_unit": "plate",          "unit_grams": 150},
    "pani puri":        {"cal_per_100g": 80,  "typical_unit": "piece",          "unit_grams": 20},
    "dahi puri":        {"cal_per_100g": 110, "typical_unit": "piece",          "unit_grams": 30},
    "pav bhaji":        {"cal_per_100g": 180, "typical_unit": "plate (bhaji+2 pav)", "unit_grams": 350},
    "vada pav":         {"cal_per_100g": 290, "typical_unit": "vada pav",       "unit_grams": 140},
    "misal pav":        {"cal_per_100g": 200, "typical_unit": "plate",          "unit_grams": 300},
    "thali":            {"cal_per_100g": 140, "typical_unit": "full thali",     "unit_grams": 600},
    "chole bhature":    {"cal_per_100g": 250, "typical_unit": "plate",          "unit_grams": 400},

    # ── Dairy & Eggs ──────────────────────────────────────────────────────────
    "milk":             {"cal_per_100g": 61,  "typical_unit": "glass (200ml)",  "unit_grams": 200},
    "whole milk":       {"cal_per_100g": 61,  "typical_unit": "glass (200ml)",  "unit_grams": 200},
    "skim milk":        {"cal_per_100g": 34,  "typical_unit": "glass (200ml)",  "unit_grams": 200},
    "curd":             {"cal_per_100g": 98,  "typical_unit": "cup",            "unit_grams": 245},
    "yogurt":           {"cal_per_100g": 98,  "typical_unit": "cup",            "unit_grams": 245},
    "greek yogurt":     {"cal_per_100g": 59,  "typical_unit": "cup",            "unit_grams": 245},
    "butter":           {"cal_per_100g": 717, "typical_unit": "tablespoon",     "unit_grams": 14},
    "ghee":             {"cal_per_100g": 900, "typical_unit": "tablespoon",     "unit_grams": 13},
    "cheese":           {"cal_per_100g": 402, "typical_unit": "slice",          "unit_grams": 28},
    "egg":              {"cal_per_100g": 155, "typical_unit": "large egg",      "unit_grams": 50},
    "boiled egg":       {"cal_per_100g": 155, "typical_unit": "large egg",      "unit_grams": 50},
    "fried egg":        {"cal_per_100g": 196, "typical_unit": "egg",            "unit_grams": 46},
    "omelette":         {"cal_per_100g": 154, "typical_unit": "2-egg omelette", "unit_grams": 120},
    "scrambled eggs":   {"cal_per_100g": 149, "typical_unit": "2-egg serving",  "unit_grams": 110},
    "lassi":            {"cal_per_100g": 70,  "typical_unit": "glass",          "unit_grams": 250},
    "buttermilk":       {"cal_per_100g": 40,  "typical_unit": "glass",          "unit_grams": 250},
    "kheer":            {"cal_per_100g": 120, "typical_unit": "cup",            "unit_grams": 220},
    "rabri":            {"cal_per_100g": 180, "typical_unit": "cup",            "unit_grams": 200},
    "paneer tikka":     {"cal_per_100g": 220, "typical_unit": "skewer (3 pcs)", "unit_grams": 150},

    # ── Grains & Legumes ──────────────────────────────────────────────────────
    "oats":             {"cal_per_100g": 389, "typical_unit": "cup dry",        "unit_grams": 80},
    "oatmeal":          {"cal_per_100g": 71,  "typical_unit": "cup cooked",     "unit_grams": 240},
    "wheat":            {"cal_per_100g": 340, "typical_unit": "cup flour",      "unit_grams": 120},
    "quinoa":           {"cal_per_100g": 120, "typical_unit": "cup cooked",     "unit_grams": 185},
    "lentils":          {"cal_per_100g": 116, "typical_unit": "cup cooked",     "unit_grams": 198},
    "chickpeas":        {"cal_per_100g": 164, "typical_unit": "cup cooked",     "unit_grams": 164},
    "black beans":      {"cal_per_100g": 132, "typical_unit": "cup cooked",     "unit_grams": 172},
    "kidney beans":     {"cal_per_100g": 127, "typical_unit": "cup cooked",     "unit_grams": 177},
    "moong dal":        {"cal_per_100g": 105, "typical_unit": "cup cooked",     "unit_grams": 200},
    "masoor dal":       {"cal_per_100g": 116, "typical_unit": "cup cooked",     "unit_grams": 200},
    "toor dal":         {"cal_per_100g": 118, "typical_unit": "cup cooked",     "unit_grams": 200},
    "urad dal":         {"cal_per_100g": 341, "typical_unit": "cup dry",        "unit_grams": 80},
    "soybeans":         {"cal_per_100g": 147, "typical_unit": "cup cooked",     "unit_grams": 172},
    "bread":            {"cal_per_100g": 265, "typical_unit": "slice",          "unit_grams": 30},
    "white bread":      {"cal_per_100g": 265, "typical_unit": "slice",          "unit_grams": 30},
    "whole wheat bread":{"cal_per_100g": 247, "typical_unit": "slice",          "unit_grams": 35},
    "pasta":            {"cal_per_100g": 131, "typical_unit": "cup cooked",     "unit_grams": 140},

    # ── Meat & Seafood ────────────────────────────────────────────────────────
    "chicken breast":   {"cal_per_100g": 165, "typical_unit": "medium breast",  "unit_grams": 174},
    "chicken thigh":    {"cal_per_100g": 209, "typical_unit": "thigh",          "unit_grams": 120},
    "chicken leg":      {"cal_per_100g": 191, "typical_unit": "drumstick",      "unit_grams": 95},
    "mutton":           {"cal_per_100g": 258, "typical_unit": "cup cooked",     "unit_grams": 150},
    "lamb":             {"cal_per_100g": 258, "typical_unit": "100g serving",   "unit_grams": 100},
    "beef":             {"cal_per_100g": 250, "typical_unit": "100g serving",   "unit_grams": 100},
    "pork":             {"cal_per_100g": 242, "typical_unit": "100g serving",   "unit_grams": 100},
    "salmon":           {"cal_per_100g": 208, "typical_unit": "fillet",         "unit_grams": 154},
    "tuna":             {"cal_per_100g": 132, "typical_unit": "can (drained)",  "unit_grams": 142},
    "rohu fish":        {"cal_per_100g": 97,  "typical_unit": "medium piece",   "unit_grams": 120},
    "prawn":            {"cal_per_100g": 99,  "typical_unit": "cup",            "unit_grams": 145},
    "crab":             {"cal_per_100g": 87,  "typical_unit": "cup meat",       "unit_grams": 118},

    # ── Nuts, Seeds & Oils ────────────────────────────────────────────────────
    "almonds":          {"cal_per_100g": 579, "typical_unit": "handful (23)",   "unit_grams": 28},
    "cashews":          {"cal_per_100g": 553, "typical_unit": "handful",        "unit_grams": 28},
    "walnuts":          {"cal_per_100g": 654, "typical_unit": "handful",        "unit_grams": 28},
    "peanuts":          {"cal_per_100g": 567, "typical_unit": "handful",        "unit_grams": 28},
    "peanut butter":    {"cal_per_100g": 588, "typical_unit": "tablespoon",     "unit_grams": 16},
    "sunflower seeds":  {"cal_per_100g": 584, "typical_unit": "tablespoon",     "unit_grams": 9},
    "chia seeds":       {"cal_per_100g": 486, "typical_unit": "tablespoon",     "unit_grams": 12},
    "flaxseeds":        {"cal_per_100g": 534, "typical_unit": "tablespoon",     "unit_grams": 10},
    "coconut":          {"cal_per_100g": 354, "typical_unit": "cup shredded",   "unit_grams": 80},
    "coconut oil":      {"cal_per_100g": 862, "typical_unit": "tablespoon",     "unit_grams": 14},
    "olive oil":        {"cal_per_100g": 884, "typical_unit": "tablespoon",     "unit_grams": 14},
    "sunflower oil":    {"cal_per_100g": 884, "typical_unit": "tablespoon",     "unit_grams": 14},
    "mustard oil":      {"cal_per_100g": 884, "typical_unit": "tablespoon",     "unit_grams": 14},

    # ── Snacks & Packaged ─────────────────────────────────────────────────────
    "biscuit":          {"cal_per_100g": 450, "typical_unit": "biscuit",        "unit_grams": 12},
    "marie biscuit":    {"cal_per_100g": 423, "typical_unit": "biscuit",        "unit_grams": 7},
    "chips":            {"cal_per_100g": 536, "typical_unit": "small bag",      "unit_grams": 28},
    "popcorn":          {"cal_per_100g": 375, "typical_unit": "cup popped",     "unit_grams": 8},
    "namkeen":          {"cal_per_100g": 450, "typical_unit": "cup",            "unit_grams": 50},
    "chakli":           {"cal_per_100g": 480, "typical_unit": "piece",          "unit_grams": 20},
    "murukku":          {"cal_per_100g": 500, "typical_unit": "piece",          "unit_grams": 25},
    "granola bar":      {"cal_per_100g": 471, "typical_unit": "bar",            "unit_grams": 47},
    "protein bar":      {"cal_per_100g": 380, "typical_unit": "bar",            "unit_grams": 60},

    # ── Sweets & Desserts ─────────────────────────────────────────────────────
    "gulab jamun":      {"cal_per_100g": 390, "typical_unit": "piece",          "unit_grams": 50},
    "jalebi":           {"cal_per_100g": 380, "typical_unit": "piece",          "unit_grams": 60},
    "halwa":            {"cal_per_100g": 310, "typical_unit": "cup",            "unit_grams": 150},
    "laddu":            {"cal_per_100g": 400, "typical_unit": "piece",          "unit_grams": 50},
    "barfi":            {"cal_per_100g": 370, "typical_unit": "piece",          "unit_grams": 40},
    "rasgulla":         {"cal_per_100g": 186, "typical_unit": "piece",          "unit_grams": 60},
    "ice cream":        {"cal_per_100g": 207, "typical_unit": "scoop",          "unit_grams": 66},
    "chocolate":        {"cal_per_100g": 546, "typical_unit": "small bar",      "unit_grams": 40},
    "dark chocolate":   {"cal_per_100g": 598, "typical_unit": "small bar",      "unit_grams": 40},
    "cake":             {"cal_per_100g": 347, "typical_unit": "slice",          "unit_grams": 90},
    "cookie":           {"cal_per_100g": 480, "typical_unit": "cookie",         "unit_grams": 30},
    "donut":            {"cal_per_100g": 452, "typical_unit": "donut",          "unit_grams": 60},

    # ── Beverages ─────────────────────────────────────────────────────────────
    "tea":              {"cal_per_100g": 2,   "typical_unit": "cup (plain)",    "unit_grams": 240},
    "masala chai":      {"cal_per_100g": 37,  "typical_unit": "cup with milk+sugar", "unit_grams": 240},
    "coffee":           {"cal_per_100g": 2,   "typical_unit": "cup (black)",    "unit_grams": 240},
    "cappuccino":       {"cal_per_100g": 40,  "typical_unit": "cup",            "unit_grams": 240},
    "latte":            {"cal_per_100g": 55,  "typical_unit": "cup",            "unit_grams": 240},
    "orange juice":     {"cal_per_100g": 45,  "typical_unit": "glass",          "unit_grams": 248},
    "mango juice":      {"cal_per_100g": 60,  "typical_unit": "glass",          "unit_grams": 248},
    "coconut water":    {"cal_per_100g": 19,  "typical_unit": "cup",            "unit_grams": 240},
    "sugarcane juice":  {"cal_per_100g": 54,  "typical_unit": "glass",          "unit_grams": 240},
    "cola":             {"cal_per_100g": 41,  "typical_unit": "can (330ml)",    "unit_grams": 330},
    "soda":             {"cal_per_100g": 0,   "typical_unit": "can",            "unit_grams": 330},
    "beer":             {"cal_per_100g": 43,  "typical_unit": "can (330ml)",    "unit_grams": 330},
    "wine":             {"cal_per_100g": 83,  "typical_unit": "glass (150ml)",  "unit_grams": 150},
    "protein shake":    {"cal_per_100g": 80,  "typical_unit": "scoop in water", "unit_grams": 350},

    # ── Fast Food ─────────────────────────────────────────────────────────────
    "pizza":            {"cal_per_100g": 266, "typical_unit": "slice",          "unit_grams": 107},
    "burger":           {"cal_per_100g": 295, "typical_unit": "burger",         "unit_grams": 226},
    "french fries":     {"cal_per_100g": 312, "typical_unit": "medium serving", "unit_grams": 117},
    "hot dog":          {"cal_per_100g": 290, "typical_unit": "hot dog",        "unit_grams": 98},
    "sandwich":         {"cal_per_100g": 218, "typical_unit": "sandwich",       "unit_grams": 200},
    "wrap":             {"cal_per_100g": 230, "typical_unit": "wrap",           "unit_grams": 200},
    "noodles":          {"cal_per_100g": 138, "typical_unit": "cup cooked",     "unit_grams": 220},
    "fried rice":       {"cal_per_100g": 185, "typical_unit": "cup",            "unit_grams": 200},
    "spring roll":      {"cal_per_100g": 125, "typical_unit": "piece",          "unit_grams": 60},
    "momos":            {"cal_per_100g": 175, "typical_unit": "plate (8 pcs)",  "unit_grams": 200},
    "maggi":            {"cal_per_100g": 350, "typical_unit": "packet cooked",  "unit_grams": 85},
    "instant noodles":  {"cal_per_100g": 350, "typical_unit": "packet",         "unit_grams": 85},
    "shawarma":         {"cal_per_100g": 220, "typical_unit": "wrap",           "unit_grams": 270},

    # ── Sauces & Condiments ───────────────────────────────────────────────────
    "ketchup":          {"cal_per_100g": 112, "typical_unit": "tablespoon",     "unit_grams": 17},
    "mayonnaise":       {"cal_per_100g": 680, "typical_unit": "tablespoon",     "unit_grams": 15},
    "chutney":          {"cal_per_100g": 90,  "typical_unit": "tablespoon",     "unit_grams": 20},
    "pickle":           {"cal_per_100g": 40,  "typical_unit": "tablespoon",     "unit_grams": 15},
    "sugar":            {"cal_per_100g": 387, "typical_unit": "teaspoon",       "unit_grams": 4},
    "honey":            {"cal_per_100g": 304, "typical_unit": "tablespoon",     "unit_grams": 21},
    "salt":             {"cal_per_100g": 0,   "typical_unit": "pinch",          "unit_grams": 1},
}


def search_food(query: str) -> dict | None:
    """
    Search the database for a food item.
    Returns the entry dict with the matched key, or None.
    """
    q = query.lower().strip()
    # Exact match first
    if q in FOOD_DB:
        return {"name": q, **FOOD_DB[q]}
    # Partial match
    for key, val in FOOD_DB.items():
        if q in key or key in q:
            return {"name": key, **val}
    return None


def get_calories_for_unit(food_name: str, quantity: float = 1.0) -> float:
    """
    Return estimated calories for `quantity` typical units of a food item.
    e.g., get_calories_for_unit("banana", 2)  →  calories for 2 bananas
    """
    entry = search_food(food_name)
    if not entry:
        return 0.0
    cal_per_unit = (entry["cal_per_100g"] * entry["unit_grams"]) / 100
    return round(cal_per_unit * quantity, 1)


def get_all_food_names() -> list:
    return sorted(FOOD_DB.keys())