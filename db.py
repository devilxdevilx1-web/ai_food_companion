"""
db.py — Database layer for AI Food Companion
Handles all SQLite operations: user profiles, food logs, chat history.
"""

import sqlite3
import json
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "food_companion.db"


def get_connection():
    """Return a connection to the SQLite database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    return conn


def init_db():
    """Create all tables if they don't already exist."""
    conn = get_connection()
    c = conn.cursor()

    # ── User profile ─────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            age         INTEGER NOT NULL,
            weight_kg   REAL    NOT NULL,
            height_cm   REAL    NOT NULL,
            gender      TEXT    NOT NULL,
            activity    TEXT    NOT NULL,
            goal        TEXT    NOT NULL,
            calorie_goal REAL   NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Daily food log ────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS food_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            log_date    TEXT    NOT NULL,
            meal_type   TEXT    DEFAULT 'General',
            raw_input   TEXT    NOT NULL,
            foods_json  TEXT    NOT NULL,   -- JSON list of {name, calories, quantity}
            total_cal   REAL    NOT NULL,
            logged_at   TEXT    DEFAULT (datetime('now'))
        )
    """)

    # ── Chat history ──────────────────────────────────────────────────────────
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_date   TEXT    NOT NULL,
            role        TEXT    NOT NULL,   -- 'user' or 'assistant'
            content     TEXT    NOT NULL,
            logged_at   TEXT    DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


# ── Profile helpers ───────────────────────────────────────────────────────────

def save_profile(name, age, weight_kg, height_cm, gender, activity, goal, calorie_goal):
    conn = get_connection()
    conn.execute("DELETE FROM user_profile")          # only one profile at a time
    conn.execute("""
        INSERT INTO user_profile
            (name, age, weight_kg, height_cm, gender, activity, goal, calorie_goal)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, age, weight_kg, height_cm, gender, activity, goal, calorie_goal))
    conn.commit()
    conn.close()


def load_profile():
    conn = get_connection()
    row = conn.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return dict(row) if row else None


# ── Food log helpers ──────────────────────────────────────────────────────────

def log_food(raw_input, foods: list, total_cal: float, meal_type="General", log_date=None):
    if log_date is None:
        log_date = str(date.today())
    conn = get_connection()
    conn.execute("""
        INSERT INTO food_log (log_date, meal_type, raw_input, foods_json, total_cal)
        VALUES (?, ?, ?, ?, ?)
    """, (log_date, meal_type, raw_input, json.dumps(foods), total_cal))
    conn.commit()
    conn.close()


def get_daily_logs(log_date=None):
    if log_date is None:
        log_date = str(date.today())
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM food_log WHERE log_date = ? ORDER BY logged_at",
        (log_date,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["foods"] = json.loads(d["foods_json"])
        result.append(d)
    return result


def get_total_calories_today(log_date=None):
    if log_date is None:
        log_date = str(date.today())
    conn = get_connection()
    row = conn.execute(
        "SELECT COALESCE(SUM(total_cal), 0) AS total FROM food_log WHERE log_date = ?",
        (log_date,)
    ).fetchone()
    conn.close()
    return float(row["total"])


def get_weekly_data():
    """Return last 7 days of calorie totals for charting."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT log_date, SUM(total_cal) AS total
        FROM   food_log
        GROUP  BY log_date
        ORDER  BY log_date DESC
        LIMIT  7
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_history(days=30):
    """Return log_date + total calories for the last N days."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT log_date, SUM(total_cal) AS total, COUNT(*) AS entries
        FROM   food_log
        GROUP  BY log_date
        ORDER  BY log_date DESC
        LIMIT  ?
    """, (days,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_log_entry(entry_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM food_log WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


# ── Chat history helpers ──────────────────────────────────────────────────────

def save_chat_message(role: str, content: str, chat_date=None):
    if chat_date is None:
        chat_date = str(date.today())
    conn = get_connection()
    conn.execute(
        "INSERT INTO chat_history (chat_date, role, content) VALUES (?, ?, ?)",
        (chat_date, role, content)
    )
    conn.commit()
    conn.close()


def get_chat_history(chat_date=None, limit=50):
    if chat_date is None:
        chat_date = str(date.today())
    conn = get_connection()
    rows = conn.execute("""
        SELECT role, content FROM chat_history
        WHERE  chat_date = ?
        ORDER  BY logged_at DESC
        LIMIT  ?
    """, (chat_date, limit)).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]


# initialise on import
init_db()