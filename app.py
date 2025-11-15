import streamlit as st
import pandas as pd
from datetime import date, datetime
from random import choice
from typing import Tuple, Dict

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(
    page_title="Dating Check-In & Follow-Through Coach",
    page_icon="💘",
    layout="wide",
)

# --- Color & visual system ---
# More colorful, still soft and product-y
ACCENT = "#FF5A7A"        # rosy accent
ACCENT_DARK = "#D74463"
BG_GRADIENT_TOP = "#FDF2FF"
BG_GRADIENT_BOTTOM = "#E3F5FF"
TEXT_MAIN = "#13141F"
CARD_BG = "#FFFFFF"
CARD_BORDER = "#E2E6F0"

st.markdown(
    f"""
    <style>
    /* Global background as gradient */
    .stApp {{
        background: linear-gradient(160deg, {BG_GRADIENT_TOP} 0%, {BG_GRADIENT_BOTTOM} 60%);
        color: {TEXT_MAIN};
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
    }}

    /* Center content a bit and give it a card feel */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}

    /* Main "card" look for each page content area */
    .page-card {{
        background-color: {CARD_BG};
        border-radius: 18px;
        padding: 1.75rem 1.75rem 2rem 1.75rem;
        border: 1px solid {CARD_BORDER};
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
    }}

    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: rgba(255, 255, 255, 0.96);
        border-right: 1px solid #E0E3EC;
    }}

    /* Headings */
    h1, h2, h3, h4, h5, h6 {{
        color: {TEXT_MAIN} !important;
        font-weight: 650;
    }}

    /* Buttons */
    div.stButton > button, div.stDownloadButton > button {{
        background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_DARK} 100%) !important;
        color: #FFFFFF !important;
        border-radius: 999px !important;
        border: none;
        padding: 0.5rem 1.3rem;
        font-weight: 600;
    }}
    div.stButton > button:hover, div.stDownloadButton > button:hover {{
        filter: brightness(1.05);
        box-shadow: 0 8px 20px rgba(255, 90, 122, 0.35);
    }}

    /* Inputs & selects */
    .stTextInput > div > div > input,
    .stNumberInput input,
    .stSelectbox > div > div > select,
    .stTextArea textarea {{
        border-radius: 999px !important;
        border: 1px solid #D0D6EA !important;
    }}

    .stTextArea textarea {{
        border-radius: 14px !important;
    }}

    /* Sliders */
    .stSlider > div > div > div {{
        color: {ACCENT};
    }}

    /* Radio / checkbox labels */
    .stRadio > label, .stSelectbox > label, .stTextInput > label, .stNumberInput > label {{
        font-weight: 500;
    }}

    /* Alerts (info/success) */
    .stAlert > div {{
        border-radius: 16px;
        border: none;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_KEY = "checkin_data"
PROFILE_KEY = "profile_data"
SEED_KEY = "seeded_sample_data"


# ---------------------------------------------------
# Data / session helpers
# ---------------------------------------------------
def init_data():
    if DATA_KEY not in st.session_state:
        st.session_state[DATA_KEY] = pd.DataFrame(
            columns=[
                # Identity / segmentation
                "user_id",
                "age_bracket",
                "location_region",
                "gender",
                "orientation",
                "neurotype",
                "dating_intention",
                # Check-in meta
                "checkin_date",
                "dating_feel",
                "burnout_index",
                "goal",
                "friction",
                # Behavioral data
                "matches",
                "conversations",
                "dates",
                "conversation_rate",
                "date_rate",
                # Date & follow-through
                "went_on_date",
                "want_see_again",
                "standout_moment",
                "nudge_arm",
                "nudge_type",
                "nudge_text",
                # Qualitative
                "burnout_note",
                "research_tags",
                # Derived
                "persona_label",
                "created_at",
            ]
        )


def get_data() -> pd.DataFrame:
    init_data()
    return st.session_state[DATA_KEY]


def save_checkin(row: Dict):
    df = get_data()
    st.session_state[DATA_KEY] = pd.concat(
        [df, pd.DataFrame([row])], ignore_index=True
    )


def seed_sample_data():
    """Populate with a few synthetic participants so visuals look alive."""
    init_data()
    if st.session_state.get(SEED_KEY, False):
        return

    df = st.session_state[DATA_KEY]
    if not df.empty:
        st.session_state[SEED_KEY] = True
        return

    sample_rows = []
    sample_users = [
        {
            "user_id": "MG",
            "age_bracket": "25–29",
            "location_region": "NYC",
            "gender": "Woman",
            "orientation": "Straight",
            "neurotype": "ADHD / attention challenges",
            "dating_intention": "Primarily looking for a long-term relationship",
        },
        {
            "user_id": "RS",
            "age_bracket": "30–34",
            "location_region": "London",
            "gender": "Man",
            "orientation": "Bi / pan",
            "neurotype": "Neurotypical (self-described)",
            "dating_intention": "Exploring / not sure",
        },
        {
            "user_id": "AJ",
            "age_bracket": "18–24",
            "location_region": "SF Bay Area",
            "gender": "Non-binary",
            "orientation": "Queer",
            "neurotype": "Other neurodivergence",
            "dating_intention": "Friendship / low pressure",
        },
    ]

    goals = [
        "Go on at least one date",
        "Be more intentional about who I match with",
        "Be more honest about what I want",
        "Take a gentler, slower approach to dating",
    ]
    frictions = [
        "I match but rarely move to dates",
        "I overthink sending messages",
        "I say yes to dates I’m not excited about",
        "I struggle with consistent communication",
    ]
    standout_examples = [
        "we laughed about our worst first dates",
        "we talked about our favorite bad movies",
        "we shared stories about our families",
    ]

    base_date = date.today()

    for u in sample_users:
        for offset in range(3):
            # Just a simple step back in weeks
            d = base_date.replace(day=max(1, base_date.day - (7 * offset)))
            dating_feel = choice([3, 4, 5, 6])
            burnout_index = 8 - dating_feel
            goal = choice(goals)
            friction = choice(frictions)
            matches = choice([2, 3, 5, 7])
            conversations = choice([1, 2, 3, 4])
            dates_count = choice([0, 1, 1, 2])
            conversation_rate = conversations / matches if matches > 0 else 0
            date_rate = dates_count / conversations if conversations > 0 else 0
            went_on_date = "Yes" if dates_count > 0 else "No"
            want_see_again = choice(["Yes", "Not sure", "No"]) if went_on_date == "Yes" else "N/A"
            standout_moment = choice(standout_examples) if went_on_date == "Yes" else ""
            nudge_arm = choice(["A", "B", "C"])
            nudge_type = choice(["Scripted", "Reflective", "Planning"])
            nudge_text = "Sample nudge text for demo purposes."
            burnout_note = choice(
                [
                    "Felt a bit drained after so many small talks.",
                    "Actually felt hopeful this week.",
                    "Messaging back and forth is tiring but dates were good.",
                ]
            )
            research_tags = "burnout, anxiety" if burnout_index >= 4 else "positive"

            persona_label = generate_persona_label(
                dating_feel=dating_feel,
                goal=goal,
                friction=friction,
                neurotype=u["neurotype"],
            )

            sample_rows.append(
                {
                    **u,
                    "checkin_date": d.isoformat(),
                    "dating_feel": dating_feel,
                    "burnout_index": burnout_index,
                    "goal": goal,
                    "friction": friction,
                    "matches": matches,
                    "conversations": conversations,
                    "dates": dates_count,
                    "conversation_rate": conversation_rate,
                    "date_rate": date_rate,
                    "went_on_date": went_on_date,
                    "want_see_again": want_see_again,
                    "standout_moment": standout_moment,
                    "nudge_arm": nudge_arm,
                    "nudge_type": nudge_type,
                    "nudge_text": nudge_text,
                    "burnout_note": burnout_note,
                    "research_tags": research_tags,
                    "persona_label": persona_label,
                    "created_at": datetime.utcnow().isoformat(),
                }
            )

    if sample_rows:
        st.session_state[DATA_KEY] = pd.concat(
            [df, pd.DataFrame(sample_rows)], ignore_index=True
        )

    st.session_state[SEED_KEY] = True


# ---------------------------------------------------
# Persona logic
# ---------------------------------------------------
def generate_persona_label(
    dating_feel: int, goal: str, friction: str, neurotype: str
) -> str:
    """Return a short persona-ish label."""
    neuro_tag = ""
    if neurotype in ["ADHD / attention challenges", "Autistic / on the spectrum"]:
        neuro_tag = "Neurodivergent "

    if dating_feel <= 3:
        mood_tag = "Burnt-Out "
    elif dating_feel >= 6:
        mood_tag = "Optimistic "
    else:
        mood_tag = "Thoughtful "

    if "overthink" in friction.lower():
        friction_tag = "Overthinking Initiator"
    elif "rarely move to dates" in friction.lower():
        friction_tag = "Hesitant Planner"
    elif "consistent communication" in friction.lower():
        friction_tag = "Inconsistent Communicator"
    elif "not excited" in friction.lower():
        friction_tag = "People-Pleaser Dater"
    else:
        friction_tag = "Exploring Dater"

    if "gentler, slower" in goal.lower():
        goal_tag = "Gentle "
    elif "intentional" in goal.lower():
        goal_tag = "Intentional "
    else:
        goal_tag = ""

    return f"{neuro_tag}{mood_tag}{goal_tag}{friction_tag}".strip()


# ---------------------------------------------------
# Tagging qualitative notes
# ---------------------------------------------------
def tag_burnout_note(note: str) -> str:
    note_lower = note.lower()

    tags = []
    if any(w in note_lower for w in ["tired", "exhausted", "burnt", "burned"]):
        tags.append("burnout")
    if any(w in note_lower for w in ["anxious", "nervous", "overwhelmed"]):
        tags.append("anxiety")
    if any(w in note_lower for w in ["excited", "hopeful", "optimistic"]):
        tags.append("positive")
    if any(w in note_lower for w in ["ghost", "ghosted"]):
        tags.append("ghosting")
    if any(w in note_lower for w in ["adhd", "focus", "distracted"]):
        tags.append("attention")

    return ", ".join(sorted(set(tags))) if tags else ""


# ---------------------------------------------------
# Nudge experiment logic
# ---------------------------------------------------
SCRIPTED_TEMPLATES = [
    "Hey, I had a really good time talking about **{moment}**. "
    "Would you be up for **{suggestion}** sometime next week?",
    "I’ve been thinking about our convo about **{moment}** — it was really fun. "
    "Want to check out **{suggestion}** soon?",
]

REFLECTIVE_TEMPLATES = [
    "Take 30 seconds to write down how you felt during the date, "
    "especially around **{moment}**. That reflection can make your next step feel easier.",
    "Before you decide what to do next, write one sentence: "
    "“When we talked about **{moment}**, I felt…” Use that to choose your next step.",
]

PLANNING_TEMPLATES = [
    "Pick a specific day and time you’d want to see them again, then send a message: "
    "“Free **{suggestion}** for a round two?”",
    "Open your calendar and block a tentative slot for a second date. "
    "Then send a simple message suggesting that time.",
]


def assign_experiment_arm() -> str:
    """Randomly assign an experiment arm (A/B/C) for nudges."""
    arm = choice(["A", "B", "C"])
    return arm


def generate_nudge(
    friction: str, want_see_again: str, standout_moment: str, experiment_arm: str
) -> Tuple[str, str]:
    """
    Returns (nudge_type, nudge_text)
    experiment_arm:
        A -> scripted focus
        B -> reflective focus
        C -> planning focus
    """
    if not standout_moment:
        standout_moment = "our conversation"
    default_suggestion = "later this week"

    if want_see_again.lower() == "no":
        nudge_type = "Reflective (closure)"
        text = (
            "It’s okay not to want a second date. Take a moment to note one thing you appreciated "
            "about the experience and one thing you’d like to look for differently next time."
        )
        return nudge_type, text

    # Map experiment arm to primary style
    if experiment_arm == "A":
        primary_pool = SCRIPTED_TEMPLATES
        primary_type = "Scripted"
    elif experiment_arm == "B":
        primary_pool = REFLECTIVE_TEMPLATES
        primary_type = "Reflective"
    else:
        primary_pool = PLANNING_TEMPLATES
        primary_type = "Planning"

    # Adjust slightly based on declared friction
    friction_lower = friction.lower()
    if "overthink" in friction_lower and experiment_arm != "B":
        primary_pool = SCRIPTED_TEMPLATES
        primary_type = "Scripted"
    elif "rarely move to dates" in friction_lower and experiment_arm != "C":
        primary_pool = PLANNING_TEMPLATES
        primary_type = "Planning"

    template = choice(primary_pool)
    text = template.format(moment=standout_moment, suggestion=default_suggestion)
    return primary_type, text


# ---------------------------------------------------
# Sidebar navigation & profile
# ---------------------------------------------------
with st.sidebar:
    # Logo
    st.image(
        "https://logowik.com/content/uploads/images/hinge-app1178.jpg",
        width=120,
    )

    st.markdown("### Check-In Coach")

    user_id = st.text_input(
        "Your initials or nickname",
        placeholder="e.g., AB, J.S., etc.",
    )

    page = st.radio(
        "Navigation",
        [
            "Participant Profile",
            "New Check-In",
            "Insights (Your Patterns)",
            "Research Dashboard",
            "Research Design",
            "About",
        ],
        index=1,
    )

    st.markdown("---")
    st.caption(
        "Prototype for exploring dating burnout, habits, and follow-through.\n"
        "Designed as a UX research + product exploration."
    )

if not user_id:
    st.warning("Please enter your initials or nickname in the sidebar to continue.")
    st.stop()

init_data()
seed_sample_data()

# Wrap all main pages in a "card" container for nicer layout
st.markdown('<div class="page-card">', unsafe_allow_html=True)


# ---------------------------------------------------
# Page: Participant Profile
# ---------------------------------------------------
if page == "Participant Profile":
    st.header("👤 Participant Profile (Research View)")

    st.markdown(
        "Lightweight participant profile used for segmentation. "
        "These fields attach to each of your check-ins."
    )

    # Load existing profile if present
    existing_profile = st.session_state.get(PROFILE_KEY, {}).get(user_id, {})

    with st.form("profile_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            age_bracket = st.selectbox(
                "Age range",
                [
                    "Prefer not to say",
                    "18–24",
                    "25–29",
                    "30–34",
                    "35–39",
                    "40+",
                ],
                index=(
                    ["Prefer not to say", "18–24", "25–29", "30–34", "35–39", "40+"].index(
                        existing_profile.get("age_bracket", "Prefer not to say")
                    )
                    if existing_profile
                    else 0
                ),
            )
            gender = st.selectbox(
                "Gender identity (self-described)",
                [
                    "Prefer not to say",
                    "Woman",
                    "Man",
                    "Non-binary",
                    "Multiple / fluid",
                    "Self-describe in notes",
                ],
                index=(
                    [
                        "Prefer not to say",
                        "Woman",
                        "Man",
                        "Non-binary",
                        "Multiple / fluid",
                        "Self-describe in notes",
                    ].index(existing_profile.get("gender", "Prefer not to say"))
                    if existing_profile
                    else 0
                ),
            )

        with col2:
            orientation = st.selectbox(
                "Sexual orientation",
                [
                    "Prefer not to say",
                    "Straight",
                    "Gay",
                    "Lesbian",
                    "Bi / pan",
                    "Queer",
                    "Other / self-describe",
                ],
                index=(
                    [
                        "Prefer not to say",
                        "Straight",
                        "Gay",
                        "Lesbian",
                        "Bi / pan",
                        "Queer",
                        "Other / self-describe",
                    ].index(existing_profile.get("orientation", "Prefer not to say"))
                    if existing_profile
                    else 0
                ),
            )
            neurotype = st.selectbox(
                "Neurotype (self-identified)",
                [
                    "Prefer not to say",
                    "ADHD / attention challenges",
                    "Autistic / on the spectrum",
                    "Other neurodivergence",
                    "Neurotypical (self-described)",
                ],
                index=(
                    [
                        "Prefer not to say",
                        "ADHD / attention challenges",
                        "Autistic / on the spectrum",
                        "Other neurodivergence",
                        "Neurotypical (self-described)",
                    ].index(existing_profile.get("neurotype", "Prefer not to say"))
                    if existing_profile
                    else 0
                ),
            )

        with col3:
            dating_intention = st.selectbox(
                "Current dating intention",
                [
                    "Exploring / not sure",
                    "Primarily looking for a long-term relationship",
                    "Short-term / casual first",
                    "Friendship / low pressure",
                    "Taking a break but still curious",
                ],
                index=(
                    [
                        "Exploring / not sure",
                        "Primarily looking for a long-term relationship",
                        "Short-term / casual first",
                        "Friendship / low pressure",
                        "Taking a break but still curious",
                    ].index(
                        existing_profile.get(
                            "dating_intention", "Exploring / not sure"
                        )
                    )
                    if existing_profile
                    else 0
                ),
            )
            location_region = st.text_input(
                "Location (city or region)",
                value=existing_profile.get("location_region", ""),
                placeholder="e.g., NYC, London, Bay Area",
            )

        additional_notes = st.text_area(
            "Anything else you'd want a researcher to know about how you date?",
            value=existing_profile.get("additional_notes", ""),
            placeholder="Optional context (e.g., work schedule, mental health, family, culture...).",
        )

        submitted_profile = st.form_submit_button("Save profile notes")

    if submitted_profile:
        profile_store = st.session_state.get(PROFILE_KEY, {})
        profile_store[user_id] = {
            "age_bracket": age_bracket,
            "gender": gender,
            "orientation": orientation,
            "neurotype": neurotype,
            "dating_intention": dating_intention,
            "location_region": location_region,
            "additional_notes": additional_notes,
        }
        st.session_state[PROFILE_KEY] = profile_store

        st.success("Profile preferences saved. These values will be attached to your future check-ins.")

    st.markdown("### How these fields are used (for the Director)")
    st.markdown(
        """
- **Segmentation**: Compare patterns across groups (e.g., ADHD vs. non-ADHD, different intentions).  
- **Context**: Add qualitative nuance to what you see on the dashboard.  
- **Filterability**: In a real implementation, charts can be filtered by these fields.
"""
    )


# ---------------------------------------------------
# Page: New Check-In
# ---------------------------------------------------
elif page == "New Check-In":
    st.header("🧭 Weekly Dating Check-In")

    st.markdown(
        "Capture how dating feels, your behaviors this week, and get a tailored follow-through nudge."
    )

    with st.form("checkin_form"):
        st.subheader("1. How is dating feeling right now?")

        col1, col2 = st.columns(2)

        with col1:
            checkin_date = st.date_input(
                "Check-in date",
                value=date.today(),
            )

            dating_feel = st.slider(
                "Overall, how does dating feel right now?",
                min_value=1,
                max_value=7,
                value=4,
                help="1 = extremely burnt out, 7
