import streamlit as st
import pandas as pd
from datetime import date, datetime
from random import choice
from typing import Tuple, Dict

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(
    page_title="Hinge Labs Concept: Dating Check-In & Follow-Through Coach",
    page_icon="💘",
    layout="wide",
)

# --- Color & visual system (colorful, but product-y) ---
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

    .block-container {{
        padding-top: 1.5rem;
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
    """
    Seed a small synthetic dataset so the researcher-facing views
    are populated when first opened.
    """
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
            # step back in weeks for a mini time series
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
    """
    Simple derived persona label to help reason about
    segments and patterns. Not meant as a production taxonomy.
    """
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
    """
    Extremely lightweight auto-tagging to show how
    qualitative notes could be structured for analysis.
    """
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
    return choice(["A", "B", "C"])


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
# Sidebar navigation & header
# ---------------------------------------------------
with st.sidebar:
    st.image(
        "https://logowik.com/content/uploads/images/hinge-app1178.jpg",
        width=120,
    )

    st.markdown("### Hinge Labs Concept")

    user_id = st.text_input(
        "Simulated participant ID",
        placeholder="e.g., P01, AB, etc.",
    )

    page = st.radio(
        "Views",
        [
            "Participant Profile (simulated)",
            "Check-In Flow (participant view)",
            "Participant Insights (participant view)",
            "Research Dashboard (Hinge Labs view)",
            "Study Design Notes",
            "About This Prototype",
        ],
        index=1,
    )

    st.markdown("---")
    st.caption(
        "Independent concept prototype inspired by Hinge Labs’ research themes.\n"
        "Not an official Hinge product."
    )

if not user_id:
    st.warning("Enter a simulated participant ID to walk through the flows.")
    st.stop()

init_data()
seed_sample_data()

# Wrap all main pages in a "card" container for a focused layout
st.markdown('<div class="page-card">', unsafe_allow_html=True)


# ---------------------------------------------------
# Page: Participant Profile (simulated)
# ---------------------------------------------------
if page == "Participant Profile (simulated)":
    st.header("👤 Participant Profile (Simulated Research Fields)")

    st.markdown(
        "These fields represent the type of **explicit segmentation metadata** "
        "that could be collected (with consent) and attached to check-ins for analysis."
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
                "Neurotype (self-identified, optional)",
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
            "Optional context the participant might share with researchers",
            value=existing_profile.get("additional_notes", ""),
            placeholder="E.g., work schedule, mental health context, cultural background, etc.",
        )

        submitted_profile = st.form_submit_button("Save simulated profile")

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

        st.success("Profile stored. New check-ins will reference these fields.")

    st.markdown("### Notes for Hinge Labs")
    st.markdown(
        """
- Intention is to show **explicit, consentful segmentation**, not inference.  
- Fields are deliberately lightweight and editable to support iterative research.  
- In a production context these would sit behind consent flows and privacy controls.
"""
    )


# ---------------------------------------------------
# Page: Check-In Flow (participant view)
# ---------------------------------------------------
elif page == "Check-In Flow (participant view)":
    st.header("🧭 Weekly Check-In (Participant Flow)")

    st.markdown(
        "This screen models a **lightweight diary-style interaction** a Hinge user could complete "
        "on a weekly basis, either in-app or via a companion surface."
    )

    with st.form("checkin_form"):
        st.subheader("1. Current dating climate")

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
                help="1 = extremely burnt out, 7 = very energized/optimistic",
            )

        with col2:
            goal = st.selectbox(
                "Short-term focus for the next few weeks",
                [
                    "Go on at least one date",
                    "Be more intentional about who I match with",
                    "Be more honest about what I want",
                    "Take a gentler, slower approach to dating",
                    "I’m not sure yet",
                ],
            )

            friction = st.selectbox(
                "Which feels most like your current friction?",
                [
                    "I match but rarely move to dates",
                    "I overthink sending messages",
                    "I say yes to dates I’m not excited about",
                    "I struggle with consistent communication",
                    "Something else / it changes a lot",
                ],
            )

        st.markdown("---")
        st.subheader("2. This week’s activity snapshot")

        c1, c2, c3 = st.columns(3)
        with c1:
            matches = st.number_input(
                "Matches this week",
                min_value=0,
                step=1,
                value=0,
            )
        with c2:
            conversations = st.number_input(
                "New conversations started",
                min_value=0,
                step=1,
                value=0,
            )
        with c3:
            dates_count = st.number_input(
                "Dates this week",
                min_value=0,
                step=1,
                value=0,
            )

        burnout_note = st.text_area(
            "Anything that felt especially energising or draining?",
            placeholder="Short, natural-language reflection. This is used qualitatively, not for UX copy.",
        )

        st.markdown("---")
        st.subheader("3. Follow-through after dates")

        went_on_date = st.radio(
            "Did you go on at least one date this week?",
            ["No", "Yes"],
            horizontal=True,
        )

        want_see_again = "N/A"
        standout_moment = ""

        if went_on_date == "Yes":
            want_see_again = st.radio(
                "For your most recent date, do you think you’d like to see them again?",
                ["Yes", "Not sure", "No"],
                horizontal=True,
            )

            standout_moment = st.text_area(
                "One moment or topic that stood out (for you)",
                placeholder="E.g., ‘We laughed about our favorite bad movies’",
            )

        st.markdown("---")
        st.subheader("4. Nudge assignment (experiment control)")

        col_exp1, col_exp2 = st.columns(2)

        with col_exp1:
            experiment_mode = st.radio(
                "Nudge assignment mode (for research)",
                [
                    "Random arm (A/B/C)",
                    "Force Scripted (Arm A)",
                    "Force Reflective (Arm B)",
                    "Force Planning (Arm C)",
                ],
            )

        with col_exp2:
            st.caption(
                """
- Arm **A** → Scripted message suggestions  
- Arm **B** → Reflective prompts  
- Arm **C** → Planning / time-boxing nudges  
"""
            )

        submitted = st.form_submit_button("Save check-in & generate nudge")

    if submitted:
        # Pull profile values if stored
        profile_store = st.session_state.get(PROFILE_KEY, {})
        profile_for_user = profile_store.get(user_id, {})

        age_bracket = profile_for_user.get("age_bracket", "Prefer not to say")
        location_region = profile_for_user.get("location_region", "")
        gender = profile_for_user.get("gender", "Prefer not to say")
        orientation = profile_for_user.get("orientation", "Prefer not to say")
        neurotype = profile_for_user.get("neurotype", "Prefer not to say")
        dating_intention = profile_for_user.get(
            "dating_intention", "Exploring / not sure"
        )

        # Determine experiment arm
        if experiment_mode == "Random arm (A/B/C)":
            experiment_arm = assign_experiment_arm()
        elif experiment_mode == "Force Scripted (Arm A)":
            experiment_arm = "A"
        elif experiment_mode == "Force Reflective (Arm B)":
            experiment_arm = "B"
        else:
            experiment_arm = "C"

        # Derived metrics
        burnout_index = 8 - dating_feel  # simple inverse of mood
        conversation_rate = (
            (conversations / matches) if matches > 0 else 0.0
        )
        date_rate = (dates_count / conversations) if conversations > 0 else 0.0

        persona_label = generate_persona_label(
            dating_feel=dating_feel,
            goal=goal,
            friction=friction,
            neurotype=neurotype,
        )

        research_tags = tag_burnout_note(burnout_note)

        # Generate nudge
        if went_on_date == "Yes":
            nudge_type, nudge_text = generate_nudge(
                friction=friction,
                want_see_again=want_see_again,
                standout_moment=standout_moment,
                experiment_arm=experiment_arm,
            )
        else:
            nudge_type = "None (no date this week)"
            nudge_text = (
                "No date this week — that’s totally fine. "
                "A very small commitment, like sending one message you feel good about next week, can still count as progress."
            )

        row = {
            # Identity / segmentation
            "user_id": user_id,
            "age_bracket": age_bracket,
            "location_region": location_region,
            "gender": gender,
            "orientation": orientation,
            "neurotype": neurotype,
            "dating_intention": dating_intention,
            # Check-in meta
            "checkin_date": checkin_date.isoformat(),
            "dating_feel": dating_feel,
            "burnout_index": burnout_index,
            "goal": goal,
            "friction": friction,
            # Behaviour
            "matches": int(matches),
            "conversations": int(conversations),
            "dates": int(dates_count),
            "conversation_rate": conversation_rate,
            "date_rate": date_rate,
            # Follow-through
            "went_on_date": went_on_date,
            "want_see_again": want_see_again,
            "standout_moment": standout_moment,
            "nudge_arm": experiment_arm,
            "nudge_type": nudge_type,
            "nudge_text": nudge_text,
            # Qualitative
            "burnout_note": burnout_note,
            "research_tags": research_tags,
            # Derived
            "persona_label": persona_label,
            "created_at": datetime.utcnow().isoformat(),
        }

        save_checkin(row)

        st.success("Check-in captured. Below is the assigned nudge for this participant state.")

        st.markdown("### Generated nudge (example of experiment arm logic)")
        st.markdown(f"**Experiment arm:** {experiment_arm}")
        st.markdown(f"**Derived persona (for analysis, not UX copy):** `{persona_label}`")
        st.markdown(f"**Nudge style:** {nudge_type}")
        st.info(nudge_text)

        if research_tags:
            st.caption(f"Auto-tagged qualitative themes (toy demo): {research_tags}")

        st.markdown("---")
        st.caption("You can now switch to **Participant Insights** or **Research Dashboard** to see how this surfaces for researchers.")


# ---------------------------------------------------
# Page: Participant Insights (participant view)
# ---------------------------------------------------
elif page == "Participant Insights (participant view)":
    st.header("🔍 Participant Insights (Simulated)")

    df = get_data()
    if df.empty or user_id not in df["user_id"].unique():
        st.info("This simulated participant has no check-ins yet. Add at least one via the Check-In Flow.")
    else:
        user_df = df[df["user_id"] == user_id].copy()
        user_df["checkin_date_dt"] = pd.to_datetime(user_df["checkin_date"])

        st.markdown(
            "This view illustrates what a **lightweight reflective surface** for the participant could look like, "
            "on top of the underlying data used for research."
        )

        # Overall vs global summary
        st.subheader("High-level snapshot")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Avg. dating feel (this participant)",
                f"{user_df['dating_feel'].mean():.1f} / 7",
            )
        with col2:
            global_df = df.copy()
            st.metric(
                "Avg. dating feel (all simulated participants)",
                f"{global_df['dating_feel'].mean():.1f} / 7",
            )
        with col3:
            st.metric(
                "Total check-ins",
                f"{len(user_df)}",
            )

        st.markdown("---")
        st.subheader("Mood & behavior over time")

        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Dating feel by check-in date**")
            mood_series = (
                user_df.sort_values("checkin_date_dt")[["checkin_date_dt", "dating_feel"]]
                .set_index("checkin_date_dt")
            )
            st.line_chart(mood_series)

        with col5:
            st.markdown("**Burnout index vs. number of dates**")
            small = user_df.sort_values("checkin_date_dt")[
                ["checkin_date_dt", "burnout_index", "dates"]
            ].set_index("checkin_date_dt")
            st.line_chart(small)

        st.markdown("---")
        st.subheader("Personas & recurring frictions")

        persona_counts = (
            user_df["persona_label"]
            .value_counts()
            .rename_axis("persona")
            .reset_index(name="count")
        )

        col6, col7 = st.columns(2)
        with col6:
            st.markdown("**Derived persona labels (frequency)**")
            st.dataframe(persona_counts, use_container_width=True)

        with col7:
            st.markdown("**Top friction statements**")
            st.dataframe(
                user_df["friction"].value_counts().rename("count").to_frame(),
                use_container_width=True,
            )

        st.markdown("---")
        st.subheader("Heuristic insight cards (illustrative)")

        insight_cards = []

        if user_df["burnout_index"].mean() >= 4:
            insight_cards.append(
                "Average burnout index is relatively high. Weeks with more conversations may be depleting; "
                "narrowing focus or introducing guardrails could be helpful."
            )

        if (
            user_df["conversation_rate"].mean() < 0.5
            and user_df["matches"].mean() > 0
        ):
            insight_cards.append(
                "This participant starts conversations with fewer than half of their matches. "
                "Scripted initiator nudges might meaningfully change behavior here."
            )

        if user_df["date_rate"].mean() < 0.4 and user_df["conversations"].mean() > 0:
            insight_cards.append(
                "A small portion of conversations convert into dates. "
                "Nudges that support decision-making around who to progress with could be impactful."
            )

        if (
            "ADHD / attention challenges"
            in user_df["neurotype"].unique()
        ):
            insight_cards.append(
                "Participant self-identifies with attention challenges. Time-bound, concrete nudges are likely "
                "a better fit than generic encouragement or open-ended advice."
            )

        if not insight_cards:
            insight_cards.append(
                "With the current number of check-ins, patterns are still emerging. "
                "More longitudinal data would make these insights more robust."
            )

        for idx, text in enumerate(insight_cards, start=1):
            st.markdown(f"**Insight {idx} (example)**")
            st.info(text)

        st.markdown("---")
        st.subheader("Mood distribution (for this participant)")

        mood_hist = (
            user_df["dating_feel"]
            .value_counts()
            .sort_index()
            .rename_axis("dating_feel")
            .reset_index(name="count")
        )
        if not mood_hist.empty:
            st.bar_chart(mood_hist.set_index("dating_feel"))

        st.markdown("---")
        st.subheader("Underlying check-in data for this participant")

        st.dataframe(
            user_df[
                [
                    "checkin_date",
                    "dating_feel",
                    "goal",
                    "friction",
                    "matches",
                    "conversations",
                    "dates",
                    "went_on_date",
                    "want_see_again",
                    "nudge_type",
                    "persona_label",
                    "research_tags",
                ]
            ],
            use_container_width=True,
        )


# ---------------------------------------------------
# Page: Research Dashboard (Hinge Labs view)
# ---------------------------------------------------
elif page == "Research Dashboard (Hinge Labs view)":
    st.header("📊 Research Dashboard (Concept View for Hinge Labs)")

    df = get_data()

    if df.empty:
        st.info("No check-ins recorded in this session. The seeding function can be extended for richer demo data.")
    else:
        st.markdown(
            "This view is meant to illustrate how **aggregated patterns** might look for a Hinge Labs-style study "
            "using this flow."
        )

        # Filters
        st.subheader("Filters (by simulated segmentation)")

        colf1, colf2, colf3 = st.columns(3)
        with colf1:
            users = sorted(df["user_id"].unique())
            filter_user = st.selectbox(
                "Participant filter",
                options=["All participants"] + users,
            )
        with colf2:
            neuro_filter = st.selectbox(
                "Neurotype filter",
                options=["All neurotypes"] + sorted(df["neurotype"].unique()),
            )
        with colf3:
            intention_filter = st.selectbox(
                "Dating intention filter",
                options=["All intentions"] + sorted(df["dating_intention"].unique()),
            )

        filtered = df.copy()
        if filter_user != "All participants":
            filtered = filtered[filtered["user_id"] == filter_user]
        if neuro_filter != "All neurotypes":
            filtered = filtered[filtered["neurotype"] == neuro_filter]
        if intention_filter != "All intentions":
            filtered = filtered[filtered["dating_intention"] == intention_filter]

        if filtered.empty:
            st.warning("No data matches the current filter selection.")
        else:
            filtered["checkin_date_dt"] = pd.to_datetime(filtered["checkin_date"])

            st.markdown("---")
            st.subheader("Study-level metrics (for current filters)")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(
                    "Unique participants",
                    f"{filtered['user_id'].nunique()}",
                )
            with c2:
                st.metric(
                    "Total check-ins",
                    f"{len(filtered)}",
                )
            with c3:
                st.metric(
                    "Avg. dating feel",
                    f"{filtered['dating_feel'].mean():.1f} / 7",
                )
            with c4:
                st.metric(
                    "Avg. burnout index",
                    f"{filtered['burnout_index'].mean():.1f}",
                )

            st.markdown("---")
            colg1, colg2 = st.columns(2)

            with colg1:
                st.markdown("**Dating feel over time (filtered)**")
                mood_series = (
                    filtered.sort_values("checkin_date_dt")[
                        ["checkin_date_dt", "dating_feel"]
                    ]
                    .set_index("checkin_date_dt")
                )
                st.line_chart(mood_series)

            with colg2:
                st.markdown("**Nudge styles delivered (for this slice)**")
                nudge_counts = (
                    filtered["nudge_type"]
                    .value_counts()
                    .rename_axis("nudge_type")
                    .reset_index(name="count")
                )
                if not nudge_counts.empty:
                    st.bar_chart(
                        nudge_counts.set_index("nudge_type")
                    )
                else:
                    st.caption("No nudges recorded yet for the current filters.")

            st.markdown("---")
            st.subheader("Behavior vs. burnout (toy scatter)")

            if not filtered.empty:
                scatter_df = filtered[["conversations", "burnout_index"]]
                st.scatter_chart(scatter_df)

            st.markdown("---")
            st.subheader("Goals, frictions & derived personas")

            colg3, colg4, colg5 = st.columns(3)
            with colg3:
                st.markdown("**Top goals**")
                st.dataframe(
                    filtered["goal"].value_counts().rename("count").to_frame(),
                    use_container_width=True,
                )
            with colg4:
                st.markdown("**Top friction statements**")
                st.dataframe(
                    filtered["friction"].value_counts().rename("count").to_frame(),
                    use_container_width=True,
                )
            with colg5:
                st.markdown("**Top derived persona labels**")
                st.dataframe(
                    filtered["persona_label"]
                    .value_counts()
                    .rename("count")
                    .to_frame(),
                    use_container_width=True,
                )

            st.markdown("---")
            st.subheader("Qualitative themes (auto-tagged, illustrative only)")

            tag_counts = (
                filtered["research_tags"]
                .dropna()
                .astype(str)
                .str.split(",")
                .explode()
            )
            tag_counts = tag_counts.str.strip()
            tag_counts = tag_counts[tag_counts != ""]
            if not tag_counts.empty:
                tag_counts = tag_counts.value_counts().rename("count").to_frame()
                st.dataframe(tag_counts, use_container_width=True)
            else:
                st.caption("No auto-tagged qualitative themes in this slice yet.")

            st.markdown("---")
            st.subheader("Underlying check-in rows (exportable)")

            st.dataframe(
                filtered[
                    [
                        "user_id",
                        "checkin_date",
                        "dating_feel",
                        "burnout_index",
                        "goal",
                        "friction",
                        "matches",
                        "conversations",
                        "dates",
                        "conversation_rate",
                        "date_rate",
                        "went_on_date",
                        "want_see_again",
                        "nudge_arm",
                        "nudge_type",
                        "persona_label",
                        "research_tags",
                    ]
                ],
                use_container_width=True,
            )

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download current slice as CSV (concept)",
                data=csv,
                file_name="hinge_labs_concept_checkins.csv",
                mime="text/csv",
            )


# ---------------------------------------------------
# Page: Study Design Notes
# ---------------------------------------------------
elif page == "Study Design Notes":
    st.header("🧪 Study Design Notes (for Hinge Labs)")

    st.markdown(
        """
This page is meant purely as **scaffolding for a research conversation** – it’s not user-facing.
"""
    )

    st.markdown("### Framing")

    st.markdown(
        """
**Concept:** A lightweight “Dating Check-In & Follow-Through Coach” that:

- Captures **weekly state + behavior** (burnout, mindset, matches / convos / dates)  
- Randomizes participants into different **follow-through nudge styles** after dates  
- Surfaces data back to both **participants** (reflection) and **researchers** (experiments)  
"""
    )

    st.markdown("### Example research questions")

    st.markdown(
        """
1. How do weekly reflections and check-ins relate to dating burnout over time?  
2. Which nudge style (scripted, reflective, planning) best supports follow-through after dates?  
3. How do responses vary across segments (e.g., ADHD vs. non-ADHD, different intentions, regions)?  
"""
    )

    st.markdown("### Illustrative hypotheses")

    st.markdown(
        """
- **H1**: Participants completing weekly check-ins show a **decrease in burnout index** over 3–4 weeks.  
- **H2**: **Scripted nudges (Arm A)** increase the self-reported rate of follow-up outreach after a date.  
- **H3**: **Planning nudges (Arm C)** increase the likelihood of a second date being scheduled.  
- **H4**: For participants with **attention challenges**, time-bound scripted nudges feel more usable than generic advice.  
"""
    )

    st.markdown("### MVP study design (diary + in-product instrumentation)")

    st.markdown(
        """
- **Method:** Mixed-methods diary-style study  
    - Participants complete weekly check-ins for ~4 weeks  
    - Nudge arm assignment is either fixed or rotated when they have a date  
- **Quantitative signals:**  
    - `dating_feel` (1–7) → `burnout_index`  
    - `matches`, `conversations`, `dates` and conversion rates  
    - Nudge arm (`nudge_arm`) and style (`nudge_type`)  
- **Qualitative signals:**  
    - Weekly reflections (`burnout_note`)  
    - Standout date moments (`standout_moment`)  
    - Light auto-tagging demo (`research_tags`) – would be replaced with proper coding work in practice  
"""
    )

    st.markdown("### How this could map into production")

    st.markdown(
        """
In a live Hinge context, this concept could:

- Sit adjacent to, or be integrated with, the existing **Hinge Labs** content and experiments  
- Replace the self-reported behavioral metrics with **instrumented events** (e.g., message send, date confirmation surfaces)  
- Use existing experimentation frameworks for **A/B/C testing** nudge content, timing, and audience segmentation  
- Provide a structured path for **longitudinal, wellbeing-oriented research** around burnout and follow-through  
"""
    )

    st.markdown(
        """
A natural next step would be to discuss:

> “If this were running inside Hinge for 6–8 weeks, what would you want to observe or test that isn’t currently covered here?”
"""
    )


# ---------------------------------------------------
# Page: About This Prototype
# ---------------------------------------------------
elif page == "About This Prototype":
    st.header("ℹ️ About This Prototype")

    st.markdown(
        """
This is an **independent concept prototype** created specifically for a conversation with the
**Hinge Research / Hinge Labs** team.

It aims to demonstrate:

- The ability to translate **Hinge Labs-style themes** (burnout, mindset, follow-through, neurodivergence) into product flows  
- Designing surfaces that are **experiment-ready** (arms, segmentation, metrics) from day one  
- Combining **participant-facing reflection** with **researcher-facing dashboards** in a single, coherent artifact  

Implementation details:

- Built in Streamlit for speed of iteration and ease of sharing  
- All data in this demo is **ephemeral in-memory** and/or **synthetic**, purely for illustration  
- Nothing here is connected to real Hinge data or real users  
"""
    )

# Close the page card wrapper
st.markdown('</div>', unsafe_allow_html=True)
