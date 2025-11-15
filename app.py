import streamlit as st
import pandas as pd
from datetime import date, datetime
from random import choice, randint
from typing import Tuple, Dict

# ---------------------------------------------------
# Page config
# ---------------------------------------------------
st.set_page_config(
    page_title="Dating Check-In & Follow-Through Coach",
    page_icon="💘",
    layout="wide",
)

DATA_KEY = "checkin_data"
PROFILE_KEY = "profile_data"


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
    st.title("💘 Check-In Coach")

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


# ---------------------------------------------------
# Page: Participant Profile
# ---------------------------------------------------
if page == "Participant Profile":
    st.header("👤 Participant Profile (Research View)")

    st.markdown(
        "This section is a lightweight participant profile used for segmentation. "
        "It’s stored with each of your check-ins so that researchers can examine patterns "
        "across different groups."
    )

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
            )
            location_region = st.text_input(
                "Location (city or region)",
                placeholder="e.g., NYC, London, Bay Area",
            )

        additional_notes = st.text_area(
            "Anything else you'd want a researcher to know about how you date?",
            placeholder="Optional context (e.g., work schedule, mental health, family, culture...).",
        )

        submitted_profile = st.form_submit_button("Save profile notes")

    if submitted_profile:
        st.success(
            "Profile preferences saved. These values will be attached to your future check-ins."
        )

    st.markdown("### How these fields are used (for the Director)")

    st.markdown(
        """
- **Segmentation**: Enables comparison across segments (e.g., ADHD vs. non-ADHD, different intentions).
- **Context**: Gives qualitative nuance to patterns seen in the dashboard.
- **Filterability**: In a fuller implementation, researchers could filter charts by these fields.

This page shows you’re thinking about **responsible, explicit segmentation** rather than
just inferring everything from behavior.
"""
    )

# ---------------------------------------------------
# Page: New Check-In
# ---------------------------------------------------
elif page == "New Check-In":
    st.header("🧭 Weekly Dating Check-In")

    st.markdown(
        "This flow captures a quick snapshot of how dating feels for you, "
        "your habits this week, and support for following through after dates."
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
                help="1 = extremely burnt out, 7 = very energized/optimistic",
            )

        with col2:
            goal = st.selectbox(
                "What’s your main focus this month?",
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
        st.subheader("2. This week in your dating life")

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
                "Conversations started",
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
            "Anything that felt especially good or draining this week?",
            placeholder="Optional, but helpful to capture patterns over time.",
        )

        st.markdown("---")
        st.subheader("3. Follow-through after a date")

        went_on_date = st.radio(
            "Did you go on a date this week?",
            ["No", "Yes"],
            horizontal=True,
        )

        want_see_again = "N/A"
        standout_moment = ""

        if went_on_date == "Yes":
            want_see_again = st.radio(
                "Do you think you’d like to see them again?",
                ["Yes", "Not sure", "No"],
                horizontal=True,
            )

            standout_moment = st.text_area(
                "What’s one moment or topic that stood out from the date?",
                placeholder="E.g., ‘We laughed about our favorite bad movies’",
            )

        st.markdown("---")
        st.subheader("4. Experiment setup (for research)")

        col_exp1, col_exp2 = st.columns(2)

        with col_exp1:
            experiment_mode = st.radio(
                "Nudge assignment mode",
                [
                    "Random arm (A/B/C)",
                    "Force Scripted",
                    "Force Reflective",
                    "Force Planning",
                ],
            )

        with col_exp2:
            st.caption(
                """
- Arm A → Scripted nudges  
- Arm B → Reflective nudges  
- Arm C → Planning nudges  
"""
            )

        submitted = st.form_submit_button("Generate support nudge & save check-in")

    if submitted:
        # Simulate profile values from sidebar form (if set), else fall back
        # In a fuller app you might persist these separately.
        age_bracket = st.session_state.get("age_bracket", "Prefer not to say")
        location_region = st.session_state.get("location_region", "")
        gender = st.session_state.get("gender", "Prefer not to say")
        orientation = st.session_state.get("orientation", "Prefer not to say")
        neurotype = st.session_state.get("neurotype", "Prefer not to say")
        dating_intention = st.session_state.get(
            "dating_intention", "Exploring / not sure"
        )

        # Determine experiment arm
        if experiment_mode == "Random arm (A/B/C)":
            experiment_arm = assign_experiment_arm()
        elif experiment_mode == "Force Scripted":
            experiment_arm = "A"
        elif experiment_mode == "Force Reflective":
            experiment_arm = "B"
        else:
            experiment_arm = "C"

        # Compute derived metrics
        burnout_index = 8 - dating_feel  # inverse of mood
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
                "No date this week — that’s totally okay. "
                "You might set a tiny goal for next week, like sending one message you feel good about."
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

        st.success("Your check-in has been saved.")

        st.markdown("### Your support nudge for this week")
        st.markdown(f"**Experiment arm:** {experiment_arm}")
        st.markdown(f"**Persona:** `{persona_label}`")
        st.markdown(f"**Nudge type:** {nudge_type}")
        st.info(nudge_text)

        if research_tags:
            st.caption(f"Auto-tagged research themes: {research_tags}")

        st.markdown("---")
        st.caption("You can review patterns and data on the *Insights* and *Research Dashboard* tabs.")


# ---------------------------------------------------
# Page: Insights (Your Patterns)
# ---------------------------------------------------
elif page == "Insights (Your Patterns)":
    st.header("🔍 Your Patterns Over Time")

    df = get_data()
    if df.empty or user_id not in df["user_id"].unique():
        st.info("You don’t have any saved check-ins yet. Submit at least one to see insights.")
    else:
        user_df = df[df["user_id"] == user_id].copy()
        user_df["checkin_date_dt"] = pd.to_datetime(user_df["checkin_date"])

        # Overall vs global summary
        st.subheader("At a glance")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Average dating feel (you)",
                f"{user_df['dating_feel'].mean():.1f} / 7",
            )
        with col2:
            global_df = df.copy()
            st.metric(
                "Average dating feel (all participants)",
                f"{global_df['dating_feel'].mean():.1f} / 7",
            )
        with col3:
            st.metric(
                "Total check-ins recorded (you)",
                f"{len(user_df)}",
            )

        st.markdown("---")
        st.subheader("Mood & behavior over time")

        col4, col5 = st.columns(2)
        with col4:
            st.markdown("**Dating feel (1–7) over time**")
            mood_series = (
                user_df.sort_values("checkin_date_dt")[["checkin_date_dt", "dating_feel"]]
                .set_index("checkin_date_dt")
            )
            st.line_chart(mood_series)

        with col5:
            st.markdown("**Burnout index vs. dates**")
            small = user_df.sort_values("checkin_date_dt")[
                ["checkin_date_dt", "burnout_index", "dates"]
            ].set_index("checkin_date_dt")
            st.line_chart(small)

        st.markdown("---")
        st.subheader("Your personas & frictions")

        persona_counts = (
            user_df["persona_label"]
            .value_counts()
            .rename_axis("persona")
            .reset_index(name="count")
        )

        col6, col7 = st.columns(2)
        with col6:
            st.markdown("**Persona labels (how often they show up)**")
            st.dataframe(persona_counts)

        with col7:
            st.markdown("**Top friction statements for you**")
            st.dataframe(
                user_df["friction"].value_counts().rename("count").to_frame()
            )

        st.markdown("---")
        st.subheader("Auto-generated insight cards")

        # Heuristic “insights”
        insight_cards = []

        if user_df["burnout_index"].mean() >= 4:
            insight_cards.append(
                "Your average burnout index is on the higher side. "
                "Weeks with more conversations might be draining you—consider narrowing your focus."
            )

        if (
            user_df["conversation_rate"].mean() < 0.5
            and user_df["matches"].mean() > 0
        ):
            insight_cards.append(
                "You tend to start conversations with less than half of your matches. "
                "One micro-goal could be starting just one extra conversation per week."
            )

        if user_df["date_rate"].mean() < 0.4 and user_df["conversations"].mean() > 0:
            insight_cards.append(
                "A relatively small share of your conversations turn into dates. "
                "Experimenting with more direct, scripted messages might help reduce decision fatigue."
            )

        if (
            "ADHD / attention challenges"
            in user_df["neurotype"].unique()
        ):
            insight_cards.append(
                "You’ve identified attention challenges. Structuring your nudges to be time-bound "
                "(e.g., ‘tonight’ or ‘this weekend’) may support follow-through."
            )

        if not insight_cards:
            insight_cards.append(
                "So far, your data doesn’t show a clear pattern yet — more check-ins will help this view become more meaningful."
            )

        for idx, text in enumerate(insight_cards, start=1):
            st.markdown(f"**Insight {idx}**")
            st.info(text)

        st.markdown("---")
        st.subheader("Your raw check-in entries")

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
            ]
        )


# ---------------------------------------------------
# Page: Research Dashboard (aggregate view)
# ---------------------------------------------------
elif page == "Research Dashboard":
    st.header("📊 Research Dashboard (All Participants)")

    df = get_data()

    if df.empty:
        st.info("No check-ins recorded yet. Submit a check-in to see data here.")
    else:
        # Filters
        st.subheader("Filters")

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

        # If empty after filters
        if filtered.empty:
            st.warning("No data matches the current filter selection.")
        else:
            filtered["checkin_date_dt"] = pd.to_datetime(filtered["checkin_date"])

            st.markdown("---")
            st.subheader("Study-level metrics")

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(
                    "Participants",
                    f"{filtered['user_id'].nunique()}",
                )
            with c2:
                st.metric(
                    "Total check-ins",
                    f"{len(filtered)}",
                )
            with c3:
                st.metric(
                    "Avg dating feel",
                    f"{filtered['dating_feel'].mean():.1f} / 7",
                )
            with c4:
                st.metric(
                    "Avg burnout index",
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
                st.markdown("**Nudge arms & types**")
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
            st.subheader("Goals, frictions & personas")

            colg3, colg4, colg5 = st.columns(3)
            with colg3:
                st.markdown("**Top goals**")
                st.dataframe(
                    filtered["goal"].value_counts().rename("count").to_frame()
                )
            with colg4:
                st.markdown("**Top friction statements**")
                st.dataframe(
                    filtered["friction"].value_counts().rename("count").to_frame()
                )
            with colg5:
                st.markdown("**Top personas**")
                st.dataframe(
                    filtered["persona_label"]
                    .value_counts()
                    .rename("count")
                    .to_frame()
                )

            st.markdown("---")
            st.subheader("Qualitative themes (auto-tagged)")

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
                st.dataframe(tag_counts)
            else:
                st.caption("No auto-tagged qualitative themes yet.")

            st.markdown("---")
            st.subheader("Raw check-in data (filtered)")

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
                ]
            )

            csv = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download filtered data as CSV",
                data=csv,
                file_name="dating_checkin_data.csv",
                mime="text/csv",
            )


# ---------------------------------------------------
# Page: Research Design
# ---------------------------------------------------
elif page == "Research Design":
    st.header("🧪 Embedded Research Design")

    st.markdown(
        """
This page is here so you can **talk like a researcher** in your call.

Use it to walk through:

- Research questions  
- Hypotheses  
- Study design  
- Metrics and possible next steps  
"""
    )

    st.markdown("### 1. Research questions")

    st.markdown(
        """
1. How do weekly reflections and check-ins relate to dating burnout over time?  
2. Which nudge style (scripted, reflective, planning) best supports follow-through after dates?  
3. Do different segments (e.g., ADHD vs. non-ADHD, different dating intentions) respond differently to these nudges?  
"""
    )

    st.markdown("### 2. Hypotheses")

    st.markdown(
        """
- **H1**: Participants who complete weekly check-ins will show a **decrease in burnout index** over 3–4 weeks.  
- **H2**: **Scripted nudges (Arm A)** will increase the self-reported rate of follow-up messages after a date.  
- **H3**: **Planning nudges (Arm C)** will increase the likelihood of a second date being scheduled.  
- **H4**: For participants with **ADHD / attention challenges**, time-bound scripted nudges will feel more helpful than generic advice.  
"""
    )

    st.markdown("### 3. Study design (MVP version)")

    st.markdown(
        """
- **Method**: Mixed-methods diary study  
    - Participants complete weekly check-ins for 3–4 weeks  
    - The app randomizes them into nudge arms (A/B/C) when they go on a date  
- **Quantitative data** (captured in this prototype):  
    - `dating_feel` (1–7) and derived `burnout_index`  
    - `matches`, `conversations`, `dates`, conversion rates  
    - Experiment arm (`nudge_arm`) and nudge type (`nudge_type`)  
- **Qualitative data**:  
    - Weekly burnout notes (`burnout_note`)  
    - Auto-tagged themes (`research_tags`)  
    - Standout moments from dates  
"""
    )

    st.markdown("### 4. Metrics & analyses")

    st.markdown(
        """
- Change in average **burnout index** over time per participant and segment  
- **Conversion metrics**:  
    - conversations / matches (interest engagement)  
    - dates / conversations (follow-through to IRL)  
- Nudge effectiveness:  
    - Self-reported follow-up behavior (future enhancement)  
    - Rate of “want to see again = Yes” that lead to a planned second date  
"""
    )

    st.markdown("### 5. How this could scale inside Hinge")

    st.markdown(
        """
If this were integrated into a production environment, it could:

- Use **real behavioral signals** instead of self-report (e.g., messaging events, date confirmations).  
- Run as a **within-app experiment** where Hinge Labs tweaks nudge content & timing.  
- Support **segment-level analysis** for Gen Z, LGBTQ+ users, neurodivergent users, etc., with proper consent & privacy.  

You can end by asking: *“If you were to run this inside Hinge Labs, what would you want to add, remove, or change?”*  
That invites them to imagine you collaborating with them.
"""
    )


# ---------------------------------------------------
# Page: About
# ---------------------------------------------------
elif page == "About":
    st.header("ℹ️ About this prototype")

    st.markdown(
        """
This prototype is a **Dating Check-In & Follow-Through Coach** designed specifically
as a **UX research + product exploration**.

It showcases that you can:

- Translate **research themes** (burnout, dating mindset, follow-through) into product flows  
- Design with **experimentability** in mind (nudge arms, metrics, segmentation)  
- Create both **participant-facing** and **researcher-facing** views  

The data is stored in memory (session-level) and meant purely for demonstration.
In a real setting, this could connect to:

- A secure backend with participant consent & privacy controls  
- Hinge's existing experimentation framework  
- A richer qualitative analysis workflow (e.g., tagging, clustering, export to research tools)  
"""
    )
