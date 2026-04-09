"""
app.py — AI Food Companion  |  Main Streamlit application
Run with:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import date, timedelta

import db
import ai_engine
import user_profile as up
import calorie_calc as cc
from utils.helpers import (
    calorie_progress_color,
    format_calories,
    bmi_category,
    is_food_log_message,
    today_str,
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Food Companion",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ─────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Root colours ────────────────────────────────────────────── */
:root {
    --bg:        #0f1117;
    --surface:   #1a1d27;
    --surface2:  #22263a;
    --accent:    #6ee7b7;
    --accent2:   #818cf8;
    --warn:      #fbbf24;
    --danger:    #f87171;
    --text:      #e2e8f0;
    --muted:     #94a3b8;
    --radius:    14px;
}

/* ── App background ──────────────────────────────────────────── */
.stApp { background: var(--bg); color: var(--text); }
section[data-testid="stSidebar"] { background: var(--surface); }

/* ── Headings ────────────────────────────────────────────────── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; color: var(--accent) !important; }

/* ── Cards ───────────────────────────────────────────────────── */
.card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(110,231,183,0.12);
}
.card-accent { border-left: 4px solid var(--accent); }
.card-warn   { border-left: 4px solid var(--warn);   }
.card-danger { border-left: 4px solid var(--danger);  }

/* ── Metric boxes ────────────────────────────────────────────── */
.metric-box {
    background: var(--surface2);
    border-radius: var(--radius);
    padding: 1rem;
    text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 700; color: var(--accent); }
.metric-label { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Chat bubbles ────────────────────────────────────────────── */
.bubble-user {
    background: var(--accent2);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0 0.4rem 20%;
    max-width: 80%;
}
.bubble-ai {
    background: var(--surface2);
    color: var(--text);
    border-radius: 18px 18px 18px 4px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 20% 0.4rem 0;
    max-width: 80%;
    border: 1px solid rgba(110,231,183,0.15);
}

/* ── Food item row ───────────────────────────────────────────── */
.food-row {
    display: flex;
    justify-content: space-between;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(148,163,184,0.1);
    font-size: 0.95rem;
}
.food-cal { color: var(--accent); font-weight: 600; }

/* ── Progress bar ────────────────────────────────────────────── */
.prog-wrap { background: var(--surface2); border-radius: 99px; height: 18px; overflow: hidden; }
.prog-fill  { height: 100%; border-radius: 99px; transition: width 0.5s ease; }

/* ── Suggestion pill ─────────────────────────────────────────── */
.pill {
    display: inline-block;
    background: rgba(110,231,183,0.12);
    color: var(--accent);
    border: 1px solid rgba(110,231,183,0.3);
    border-radius: 99px;
    padding: 0.25rem 0.85rem;
    font-size: 0.85rem;
    margin: 0.2rem;
}

/* ── Status badge ────────────────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 99px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-green  { background: rgba(74,222,128,0.2);  color: #4ade80; }
.badge-yellow { background: rgba(250,204,21,0.2);  color: #facc15; }
.badge-red    { background: rgba(248,113,113,0.2); color: #f87171; }

/* ── Streamlit widget overrides ──────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid rgba(110,231,183,0.25) !important;
    border-radius: 10px !important;
}
.stSelectbox > div > div {
    background: var(--surface2) !important;
    color: var(--text) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6ee7b7, #818cf8) !important;
    color: #0f1117 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: var(--surface); border-radius: var(--radius); padding: 4px; }
.stTabs [data-baseweb="tab"]      { color: var(--muted) !important; }
.stTabs [aria-selected="true"]    { background: var(--surface2) !important; color: var(--accent) !important; border-radius: 8px; }

/* Divider */
hr { border-color: rgba(148,163,184,0.1) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--surface); }
::-webkit-scrollbar-thumb { background: rgba(110,231,183,0.3); border-radius: 99px; }

/* Alert */
.stAlert { border-radius: var(--radius) !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALISATION
# ════════════════════════════════════════════════════════════════════════════

if "chat_messages"   not in st.session_state: st.session_state.chat_messages   = []
if "profile_saved"   not in st.session_state: st.session_state.profile_saved   = False
if "active_tab"      not in st.session_state: st.session_state.active_tab      = "chat"


# ════════════════════════════════════════════════════════════════════════════
# HELPER RENDER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def render_calorie_gauge(consumed: float, goal: float):
    pct   = min(consumed / goal, 1.0) if goal > 0 else 0
    color = calorie_progress_color(consumed, goal)
    remaining = max(goal - consumed, 0)
    over      = max(consumed - goal, 0)

    fig = go.Figure(go.Indicator(
        mode  = "gauge+number+delta",
        value = consumed,
        delta = {"reference": goal, "valueformat": ".0f",
                 "increasing": {"color": "#f87171"},
                 "decreasing": {"color": "#4ade80"}},
        title = {"text": "Calories Today", "font": {"color": "#94a3b8", "size": 14}},
        number= {"suffix": " kcal", "font": {"color": color, "size": 28}},
        gauge = {
            "axis":      {"range": [0, max(goal * 1.2, consumed * 1.1)],
                          "tickcolor": "#475569"},
            "bar":       {"color": color},
            "bgcolor":   "#22263a",
            "bordercolor": "#1a1d27",
            "steps": [
                {"range": [0, goal * 0.5],  "color": "rgba(74,222,128,0.08)"},
                {"range": [goal * 0.5, goal],"color": "rgba(250,204,21,0.08)"},
            ],
            "threshold": {
                "line": {"color": "#f87171", "width": 3},
                "thickness": 0.75,
                "value": goal,
            },
        },
    ))
    fig.update_layout(
        height=240, margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)", font_color="#e2e8f0",
    )
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class='metric-box'>
          <div class='metric-value' style='color:#6ee7b7'>{consumed:.0f}</div>
          <div class='metric-label'>Consumed</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='metric-box'>
          <div class='metric-value' style='color:#818cf8'>{goal:.0f}</div>
          <div class='metric-label'>Goal</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        if over > 0:
            st.markdown(f"""
            <div class='metric-box'>
              <div class='metric-value' style='color:#f87171'>+{over:.0f}</div>
              <div class='metric-label'>Over Budget</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='metric-box'>
              <div class='metric-value' style='color:#fbbf24'>{remaining:.0f}</div>
              <div class='metric-label'>Remaining</div>
            </div>""", unsafe_allow_html=True)


def render_food_breakdown(foods: list, total: float):
    st.markdown("<div class='card card-accent'>", unsafe_allow_html=True)
    st.markdown("**🍽️ Food Breakdown**")
    for f in foods:
        st.markdown(
            f"<div class='food-row'>"
            f"<span>🔸 {f.get('name','?')} "
            f"<span style='color:#94a3b8;font-size:0.8em'>({f.get('quantity','1 serving')})</span></span>"
            f"<span class='food-cal'>{f.get('calories',0):.0f} kcal</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
    st.markdown(
        f"<div class='food-row' style='font-weight:700;margin-top:0.5rem'>"
        f"<span>Total</span><span class='food-cal'>{total:.0f} kcal</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_suggestions(suggestions: list):
    if suggestions:
        pills = " ".join(f"<span class='pill'>💡 {s}</span>" for s in suggestions)
        st.markdown(
            f"<div class='card' style='margin-top:0.5rem'>"
            f"<div style='font-size:0.8rem;color:#94a3b8;margin-bottom:0.5rem'>MEAL SUGGESTIONS</div>"
            f"{pills}</div>",
            unsafe_allow_html=True,
        )


def render_ollama_status():
    running = ai_engine.is_ollama_running()
    if running:
        models  = ai_engine.get_available_models()
        st.sidebar.success(f"🟢 Ollama running  |  {len(models)} model(s)")
    else:
        st.sidebar.warning("🔴 Ollama offline — using local DB")
        st.sidebar.code("ollama serve", language="bash")


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("<h2 style='margin-top:0'>🥗 AI Food Companion</h2>", unsafe_allow_html=True)
    render_ollama_status()
    st.divider()

    profile = up.get_profile()
    if profile:
        st.markdown(f"**👤 {profile['name']}**")
        st.caption(
            f"{profile['age']} yrs · {profile['weight_kg']} kg · {profile['height_cm']} cm"
        )
        bmi_val, bmi_cat = bmi_category(profile["weight_kg"], profile["height_cm"])
        badge_class = "badge-green" if bmi_cat == "Normal weight" else "badge-yellow"
        st.markdown(
            f"BMI: {bmi_val} &nbsp;<span class='{badge_class} badge'>{bmi_cat}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"🎯 **{profile['calorie_goal']:.0f} kcal / day**")
        st.markdown(f"*{profile['goal']}*")
        st.divider()

        consumed_today = db.get_total_calories_today()
        remaining      = max(profile["calorie_goal"] - consumed_today, 0)
        pct            = min(int(consumed_today / profile["calorie_goal"] * 100), 100)
        color          = calorie_progress_color(consumed_today, profile["calorie_goal"])
        st.markdown("**Today's Progress**")
        st.markdown(
            f"<div class='prog-wrap'>"
            f"<div class='prog-fill' style='width:{pct}%;background:{color}'></div>"
            f"</div>"
            f"<div style='font-size:0.8rem;color:#94a3b8;margin-top:4px'>"
            f"{consumed_today:.0f} / {profile['calorie_goal']:.0f} kcal</div>",
            unsafe_allow_html=True,
        )
        if consumed_today > profile["calorie_goal"]:
            st.markdown("<span class='badge badge-red'>⚠️ Over daily goal</span>", unsafe_allow_html=True)
        st.divider()

    nav = st.radio(
        "Navigate",
        ["💬 Chat & Log", "📊 Dashboard", "📅 History", "👤 Profile"],
        label_visibility="collapsed",
    )

    if profile:
        with st.expander("⚙️ Macros"):
            calc = cc.full_calculation(
                profile["weight_kg"], profile["height_cm"],
                profile["age"], profile["gender"],
                profile["activity"], profile["goal"],
            )
            st.metric("Carbs",    f"{calc['macro_carbs']:.0f}g")
            st.metric("Fat",      f"{calc['macro_fat']:.0f}g")
            st.metric("Protein",  f"{calc['macro_prot']:.0f}g")


# ════════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ════════════════════════════════════════════════════════════════════════════

# ── Profile setup (shown when no profile exists) ──────────────────────────

if nav == "👤 Profile" or not up.get_profile():
    if not up.get_profile():
        st.markdown("## 👋 Welcome! Let's set up your profile first.")
    else:
        st.markdown("## 👤 Update Profile")

    profile = up.get_profile() or {}

    with st.form("profile_form"):
        c1, c2 = st.columns(2)
        name       = c1.text_input("Your Name",         value=profile.get("name", ""))
        age        = c2.number_input("Age (years)",      value=int(profile.get("age", 25)),        min_value=10, max_value=100)
        weight_kg  = c1.number_input("Weight (kg)",      value=float(profile.get("weight_kg", 70)),min_value=30.0, max_value=300.0, step=0.5)
        height_cm  = c2.number_input("Height (cm)",      value=float(profile.get("height_cm", 170)),min_value=100.0, max_value=250.0, step=0.5)
        gender     = c1.selectbox("Gender",              ["Male", "Female"],
                                   index=0 if profile.get("gender","Male")=="Male" else 1)
        activity   = st.selectbox("Activity Level",      cc.get_activity_options(),
                                   index=cc.get_activity_options().index(profile["activity"])
                                         if "activity" in profile else 1)
        goal       = st.selectbox("Your Goal",           cc.get_goal_options(),
                                   index=cc.get_goal_options().index(profile["goal"])
                                         if "goal" in profile else 0)

        submitted = st.form_submit_button("💾 Save Profile & Calculate Calories")
        if submitted:
            if not name.strip():
                st.error("Please enter your name.")
            else:
                saved = up.create_or_update_profile(
                    name.strip(), age, weight_kg, height_cm, gender, activity, goal
                )
                st.session_state.profile_saved = True
                st.success(
                    f"✅ Profile saved!  "
                    f"BMR: **{saved['bmr']:.0f}** kcal  |  "
                    f"TDEE: **{saved['tdee']:.0f}** kcal  |  "
                    f"Daily Goal: **{saved['goal_cal']:.0f}** kcal"
                )
                st.rerun()

    if up.get_profile():
        bmi_val, bmi_cat = bmi_category(
            up.get_profile()["weight_kg"], up.get_profile()["height_cm"]
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMR",        f"{up.get_profile().get('bmr',0):.0f} kcal")
        c2.metric("TDEE",       f"{up.get_profile().get('tdee',0):.0f} kcal")
        c3.metric("Daily Goal", f"{up.get_profile()['calorie_goal']:.0f} kcal")
        c4.metric("BMI",        f"{bmi_val} ({bmi_cat})")

    if not up.get_profile():
        st.stop()  # Don't show other sections until profile is set


# ── Guard: redirect to profile if missing ────────────────────────────────
profile = up.get_profile()
if not profile:
    st.warning("Please set up your profile first.")
    st.stop()


# ════════════════════════════════════════════════════════════════════════════
# CHAT & LOG
# ════════════════════════════════════════════════════════════════════════════

if nav == "💬 Chat & Log":
    st.markdown("## 💬 Chat with NutriAI")

    consumed_today = db.get_total_calories_today()
    remaining      = max(profile["calorie_goal"] - consumed_today, 0)

    col_chat, col_dash = st.columns([3, 2], gap="large")

    with col_chat:
        # ── Display conversation ──────────────────────────────────────────
        chat_container = st.container()
        with chat_container:
            if not st.session_state.chat_messages:
                st.markdown(
                    f"<div class='bubble-ai'>"
                    f"👋 Hi <b>{profile['name']}</b>! I'm NutriAI, your personal food companion.<br><br>"
                    f"Your daily goal is <b>{profile['calorie_goal']:.0f} kcal</b> to help you <i>{profile['goal'].lower()}</i>.<br><br>"
                    f"Just tell me what you've eaten — e.g.:<br>"
                    f"<i>\"I ate 2 idlis with sambar and a banana\"</i><br><br>"
                    f"I'll track the calories for you! 🥗"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(
                        f"<div class='bubble-user'>{msg['content']}</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"<div class='bubble-ai'>{msg['content']}</div>",
                        unsafe_allow_html=True,
                    )
                    if "foods" in msg and msg["foods"]:
                        render_food_breakdown(msg["foods"], msg.get("total_cal", 0))
                    if "suggestions" in msg and msg["suggestions"]:
                        render_suggestions(msg["suggestions"])

        # ── Input ─────────────────────────────────────────────────────────
        st.markdown("---")
        meal_type = st.selectbox(
            "Meal type",
            ["Breakfast 🍳", "Lunch 🍛", "Dinner 🌙", "Snack 🍎", "Drink 🥤"],
            label_visibility="collapsed",
        )
        user_input = st.chat_input("Tell me what you ate…  e.g. 'I had 2 rotis with dal and salad'")

        if user_input:
            # Add user bubble
            st.session_state.chat_messages.append(
                {"role": "user", "content": user_input}
            )
            db.save_chat_message("user", user_input)

            # Decide: food log or general chat?
            history_for_ai = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.chat_messages[:-1]
            ]

            if is_food_log_message(user_input) or any(
                kw in user_input.lower() for kw in [
                    "ate","had","eat","drank","drunk","consumed","snack",
                    "breakfast","lunch","dinner","meal","food","calories"
                ]
            ):
                with st.spinner("Analysing your meal…"):
                    result = ai_engine.process_food_input(
                        user_input,
                        history_for_ai,
                        profile,
                        db.get_total_calories_today(),
                    )

                total_cal  = result.get("total_calories", 0)
                foods      = result.get("foods", [])
                message    = result.get("message", "")
                suggestions= result.get("meal_suggestions", [])
                source     = result.get("source", "local")

                # Ensure calories are numbers not strings
                try:
                    total_cal = float(total_cal)
                except (TypeError, ValueError):
                    total_cal = 0.0
                for f in foods:
                    try:
                        f["calories"] = float(f.get("calories", 0))
                    except (TypeError, ValueError):
                        f["calories"] = 0.0

                # Safety: if message contains raw JSON, replace with clean fallback
                if not message or "{" in message or '"foods"' in message or "```" in message:
                    message = (
                        f"Got it! Logged {total_cal:.0f} kcal from {len(foods)} item(s)."
                    )

                # ── Log to DB FIRST, then read updated total ──────────────────
                if total_cal > 0 or foods:
                    db.log_food(
                        raw_input=user_input,
                        foods=foods,
                        total_cal=total_cal,
                        meal_type=meal_type.split()[0],
                    )

                # Read fresh totals AFTER logging
                consumed_now  = db.get_total_calories_today()
                remaining_now = max(profile["calorie_goal"] - consumed_now, 0)
                src_badge     = "🤖 AI" if source == "ai" else "📚 Local DB"

                alert = ""
                if consumed_now > profile["calorie_goal"]:
                    over = consumed_now - profile["calorie_goal"]
                    alert = f"<br><br>⚠️ <b>You're {over:.0f} kcal over your daily goal.</b> Consider lighter options for the rest of the day."
                elif remaining_now < 200:
                    alert = f"<br><br>🟡 <b>Only {remaining_now:.0f} kcal left</b> for today — choose wisely!"

                reply_html = (
                    f"<span style='font-size:0.7rem;color:#94a3b8'>{src_badge}</span><br>"
                    f"{message}{alert}"
                )

                st.session_state.chat_messages.append({
                    "role":       "assistant",
                    "content":    reply_html,
                    "foods":      foods,
                    "total_cal":  total_cal,
                    "suggestions":suggestions,
                })
                db.save_chat_message("assistant", message)

            else:
                # General nutrition Q&A
                with st.spinner("Thinking…"):
                    reply = ai_engine.get_general_response(
                        user_input, history_for_ai, profile
                    )
                st.session_state.chat_messages.append(
                    {"role": "assistant", "content": reply}
                )
                db.save_chat_message("assistant", reply)

            st.rerun()

        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = []
            st.rerun()

    # ── Right panel: today's summary ─────────────────────────────────────
    with col_dash:
        consumed_today = db.get_total_calories_today()
        render_calorie_gauge(consumed_today, profile["calorie_goal"])
        st.markdown("---")

        today_logs = db.get_daily_logs()
        if today_logs:
            st.markdown("**📋 Today's Log**")
            for log in today_logs:
                with st.expander(
                    f"{log['meal_type']} — {log['total_cal']:.0f} kcal  ·  {log['logged_at'][11:16]}"
                ):
                    for food in log["foods"]:
                        st.markdown(
                            f"• **{food['name']}** ({food['quantity']}) — {food['calories']:.0f} kcal"
                        )
                    if st.button("🗑️ Delete", key=f"del_{log['id']}"):
                        db.delete_log_entry(log["id"])
                        st.rerun()
        else:
            st.info("No food logged yet today. Start chatting! 👆")


# ════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════════════════════

elif nav == "📊 Dashboard":
    st.markdown("## 📊 Your Nutrition Dashboard")

    consumed_today = db.get_total_calories_today()
    render_calorie_gauge(consumed_today, profile["calorie_goal"])
    st.markdown("---")

    # ── Weekly bar chart ──────────────────────────────────────────────────
    weekly = db.get_weekly_data()
    if weekly:
        df_week = pd.DataFrame(weekly)
        df_week = df_week.sort_values("log_date")
        df_week["day"] = pd.to_datetime(df_week["log_date"]).dt.strftime("%a %b %d")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df_week["day"], y=df_week["total"],
            marker_color=[
                "#6ee7b7" if v <= profile["calorie_goal"] else "#f87171"
                for v in df_week["total"]
            ],
            name="Calories",
        ))
        fig.add_hline(
            y=profile["calorie_goal"],
            line_dash="dot", line_color="#818cf8",
            annotation_text=f"Goal: {profile['calorie_goal']:.0f} kcal",
            annotation_font_color="#818cf8",
        )
        fig.update_layout(
            title="📅 Weekly Calorie Intake",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            xaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
            yaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
            height=320,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data yet. Start logging your meals to see charts here!")

    # ── Today's meals breakdown ───────────────────────────────────────────
    today_logs = db.get_daily_logs()
    if today_logs:
        st.markdown("### Today's Meals Breakdown")
        meal_totals: dict = {}
        all_foods: list   = []
        for log in today_logs:
            mt = log["meal_type"]
            meal_totals[mt] = meal_totals.get(mt, 0) + log["total_cal"]
            all_foods.extend(log["foods"])

        c1, c2 = st.columns(2)
        with c1:
            fig_pie = go.Figure(go.Pie(
                labels=list(meal_totals.keys()),
                values=list(meal_totals.values()),
                hole=0.5,
                marker_colors=["#6ee7b7","#818cf8","#fbbf24","#f87171","#38bdf8"],
            ))
            fig_pie.update_layout(
                title="Calories by Meal",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#e2e8f0",
                height=300,
                legend=dict(font=dict(color="#e2e8f0")),
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            # Top foods by calories
            food_cals: dict = {}
            for f in all_foods:
                food_cals[f["name"]] = food_cals.get(f["name"], 0) + f["calories"]
            if food_cals:
                top = sorted(food_cals.items(), key=lambda x: x[1], reverse=True)[:8]
                fig_bar = go.Figure(go.Bar(
                    x=[t[1] for t in top],
                    y=[t[0] for t in top],
                    orientation="h",
                    marker_color="#818cf8",
                ))
                fig_bar.update_layout(
                    title="Top Foods Today",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e2e8f0",
                    height=300,
                    xaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
                    yaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
                )
                st.plotly_chart(fig_bar, use_container_width=True)

    # ── Macro progress ────────────────────────────────────────────────────
    st.markdown("### 🥩 Macro Targets")
    calc = cc.full_calculation(
        profile["weight_kg"], profile["height_cm"],
        profile["age"], profile["gender"],
        profile["activity"], profile["goal"],
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("🌾 Carbs",   f"{calc['macro_carbs']:.0f}g / day", help="50% of goal calories")
    c2.metric("🥑 Fat",     f"{calc['macro_fat']:.0f}g / day",   help="25% of goal calories")
    c3.metric("🥩 Protein", f"{calc['macro_prot']:.0f}g / day",  help="25% of goal calories")


# ════════════════════════════════════════════════════════════════════════════
# HISTORY
# ════════════════════════════════════════════════════════════════════════════

elif nav == "📅 History":
    st.markdown("## 📅 Food History")

    days_back = st.slider("Show last N days", 7, 90, 30)
    history   = db.get_history(days_back)

    if not history:
        st.info("No history yet. Start logging meals in the Chat tab!")
    else:
        df_hist = pd.DataFrame(history)
        df_hist["log_date"] = pd.to_datetime(df_hist["log_date"])
        df_hist = df_hist.sort_values("log_date")

        # ── Trend line ────────────────────────────────────────────────────
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_hist["log_date"], y=df_hist["total"],
            mode="lines+markers",
            line=dict(color="#6ee7b7", width=2),
            marker=dict(color="#6ee7b7", size=7),
            fill="tozeroy",
            fillcolor="rgba(110,231,183,0.08)",
            name="Calories",
        ))
        fig_trend.add_hline(
            y=profile["calorie_goal"],
            line_dash="dot", line_color="#818cf8",
            annotation_text="Daily Goal",
            annotation_font_color="#818cf8",
        )
        fig_trend.update_layout(
            title="📈 Calorie Trend",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e2e8f0",
            height=320,
            xaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
            yaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # ── Stats ─────────────────────────────────────────────────────────
        avg_cal   = df_hist["total"].mean()
        goal_days = int((df_hist["total"] <= profile["calorie_goal"]).sum())
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Days tracked",  len(df_hist))
        c2.metric("Avg calories",  f"{avg_cal:.0f} kcal")
        c3.metric("Goal met days", f"{goal_days} / {len(df_hist)}")
        c4.metric("Best day",      f"{df_hist['total'].min():.0f} kcal")

        # ── Table ─────────────────────────────────────────────────────────
        st.markdown("### 📋 Day-by-Day Log")
        df_show = df_hist[["log_date","total","entries"]].copy()
        df_show["log_date"] = df_show["log_date"].dt.strftime("%Y-%m-%d")
        df_show["vs goal"]  = df_show["total"].apply(
            lambda x: f"+{x-profile['calorie_goal']:.0f}"
            if x > profile["calorie_goal"]
            else f"{x-profile['calorie_goal']:.0f}"
        )
        df_show.columns = ["Date","Calories","Log Entries","vs Goal"]
        st.dataframe(df_show, use_container_width=True, hide_index=True)

        # ── Drill into a day ──────────────────────────────────────────────
        st.markdown("### 🔍 Drill into a Day")
        selected_date = st.date_input("Pick a date", value=date.today())
        day_logs      = db.get_daily_logs(str(selected_date))
        if day_logs:
            for log in day_logs:
                with st.expander(
                    f"{log['meal_type']} · {log['total_cal']:.0f} kcal — {log['raw_input'][:50]}"
                ):
                    for food in log["foods"]:
                        st.write(f"• **{food['name']}** ({food['quantity']}) — {food['calories']:.0f} kcal")
        else:
            st.info(f"No logs for {selected_date}.")