import streamlit as st
import pandas as pd

from data_processor import process_uploaded_file
from sentiment import analyze_reviews
from themes import discover_themes
from evidence import extract_representative_reviews
from insights import calculate_theme_insight
from recommendations import generate_recommendations
from debate import debate_solutions


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="VoiceCopilot",
    page_icon="🎙️",
    layout="wide"
)


# ==================================================
# SESSION STATE
# ==================================================

if "solutions" not in st.session_state:
    st.session_state.solutions = {}

if "debates" not in st.session_state:
    st.session_state.debates = {}

if "decisions" not in st.session_state:
    st.session_state.decisions = {}


# ==================================================
# CUSTOM LIGHT UI
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        color: #111827 !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #1E293B !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #334155 !important;
        font-weight: 700 !important;
    }

    p {
        color: #475569;
    }

    .stCaption {
        color: #64748B !important;
    }

    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.25rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }

    [data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800 !important;
    }

    [data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stExpander"] summary {
        color: #1E293B !important;
        font-weight: 700 !important;
    }

    .stButton > button {
        background-color: #7C3AED;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 1.2rem;
        font-weight: 700;
    }

    .stButton > button:hover {
        background-color: #6D28D9;
        color: #FFFFFF;
    }

    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #E2E8F0;
    }

    hr {
        border-color: #E2E8F0;
    }

    .solution-card {
        background-color: #FFFFFF;
        border: 1px solid #DDD6FE;
        border-radius: 14px;
        padding: 1.2rem;
        min-height: 280px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
    }

    .debate-card {
        background-color: #F5F3FF;
        border: 1px solid #DDD6FE;
        border-radius: 16px;
        padding: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# HEADER
# ==================================================

st.title("🎙️ VoiceCopilot")

st.caption(
    "Turn customer feedback into evidence-backed product decisions."
)


# ==================================================
# FILE UPLOAD
# ==================================================

uploaded_file = st.file_uploader(
    "Upload customer feedback",
    type=["csv", "xlsx", "txt"]
)


# ==================================================
# ANALYSIS
# ==================================================

if uploaded_file is not None:

    try:

        # ==================================================
        # READ FILE
        # ==================================================

        df = process_uploaded_file(uploaded_file)

        st.success(
            f"Successfully loaded {len(df)} customer reviews."
        )


        # ==================================================
        # SENTIMENT
        # ==================================================

        sentiment_results = analyze_reviews(
            df["review"].tolist()
        )

        sentiment_df = pd.DataFrame(
            sentiment_results
        )


        # ==================================================
        # COUNTS
        # ==================================================

        total_reviews = len(sentiment_df)

        positive_count = (
            sentiment_df["sentiment"] == "Positive"
        ).sum()

        neutral_count = (
            sentiment_df["sentiment"] == "Neutral"
        ).sum()

        negative_count = (
            sentiment_df["sentiment"] == "Negative"
        ).sum()


        # ==================================================
        # PERCENTAGES
        # ==================================================

        if total_reviews > 0:

            positive_pct = (
                positive_count / total_reviews * 100
            )

            neutral_pct = (
                neutral_count / total_reviews * 100
            )

            negative_pct = (
                negative_count / total_reviews * 100
            )

        else:

            positive_pct = 0
            neutral_pct = 0
            negative_pct = 0


        # ==================================================
        # DASHBOARD
        # ==================================================

        st.divider()

        st.header(
            "Customer Insights Dashboard"
        )

        st.caption(
            f"Analysis of {total_reviews} customer reviews"
        )


        # ==================================================
        # SENTIMENT CARDS
        # ==================================================

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "😊 Positive",
            f"{positive_pct:.1f}%"
        )

        col2.metric(
            "😐 Neutral",
            f"{neutral_pct:.1f}%"
        )

        col3.metric(
            "😡 Negative",
            f"{negative_pct:.1f}%"
        )


        # ==================================================
        # THEME DISCOVERY
        # ==================================================

        st.subheader(
            "Top Customer Themes"
        )

        theme_df = discover_themes(
            df["review"].tolist(),
            number_of_themes=5
        )


        if not theme_df.empty:

            for theme_index, theme in theme_df.iterrows():

                # ==================================================
                # THEME INSIGHT
                # ==================================================

                insight = calculate_theme_insight(
                    theme["reviews"],
                    sentiment_df
                )


                # ==================================================
                # THEME EXPANDER
                # ==================================================

                with st.expander(
                    f"🔹 {theme['theme']}  •  "
                    f"{theme['percentage']}% of reviews"
                ):

                    st.write(
                        f"**Keywords:** "
                        f"{theme['keywords']}"
                    )

                    st.write(
                        f"**Reviews:** "
                        f"{insight['review_count']}"
                    )

                    st.write(
                        f"**Negative sentiment:** "
                        f"{insight['negative_rate']}%"
                    )


                    # ==================================================
                    # PRIORITY
                    # ==================================================

                    if insight["priority"] == "High":

                        st.error(
                            "🔥 HIGH PRIORITY"
                        )

                    elif insight["priority"] == "Medium":

                        st.warning(
                            "⚠️ MEDIUM PRIORITY"
                        )

                    else:

                        st.success(
                            "🟢 LOW PRIORITY"
                        )


                    # ==================================================
                    # KEY INSIGHT
                    # ==================================================

                    st.markdown(
                        "### 💡 Key Insight"
                    )

                    st.write(
                        insight["insight"]
                    )


                    # ==================================================
                    # CUSTOMER EVIDENCE
                    # ==================================================

                    st.markdown(
                        "### 🗣️ Customer Evidence"
                    )

                    theme_reviews = theme["reviews"]

                    representative_reviews = (
                        extract_representative_reviews(
                            theme_reviews,
                            max_reviews=3
                        )
                    )


                    for review in representative_reviews:

                        st.info(
                            f'"{review}"'
                        )


                    # ==================================================
                    # AI SOLUTIONS
                    # ==================================================

                    st.markdown("---")

                    st.markdown(
                        "### 🤖 AI-Generated Solutions"
                    )

                    st.caption(
                        "AI proposes alternatives based on "
                        "customer evidence. The final decision "
                        "remains with the product team."
                    )


                    # ==================================================
                    # GENERATE SOLUTIONS
                    # ==================================================

                    if st.button(
                        "✨ Generate Solutions",
                        key=f"generate_{theme_index}"
                    ):

                        with st.spinner(
                            "Gemini is analyzing "
                            "the customer evidence..."
                        ):

                            recommendation_result = (
                                generate_recommendations(
                                    theme_name=theme["theme"],
                                    keywords=theme["keywords"],
                                    insight=insight["insight"],
                                    evidence=representative_reviews
                                )
                            )


                        if recommendation_result.get("error"):

                            st.warning(
                                recommendation_result["error"]
                            )

                        else:

                            st.session_state.solutions[
                                theme_index
                            ] = recommendation_result.get(
                                "solutions",
                                []
                            )

                            # Clear old debate when generating
                            # completely new solutions.

                            st.session_state.debates.pop(
                                theme_index,
                                None
                            )


                    # ==================================================
                    # RETRIEVE SAVED SOLUTIONS
                    # ==================================================

                    solutions = (
                        st.session_state.solutions.get(
                            theme_index,
                            []
                        )
                    )


                    # ==================================================
                    # DISPLAY SOLUTIONS
                    # ==================================================

                    if solutions:

                        solution_columns = st.columns(
                            len(solutions)
                        )


                        for i, solution in enumerate(
                            solutions
                        ):

                            with solution_columns[i]:

                                st.markdown(
                                    f"""
                                    <div class="solution-card">

                                    <h4>
                                    Option {i + 1}
                                    </h4>

                                    <strong>
                                    {solution['title']}
                                    </strong>

                                    <p>
                                    {solution['description']}
                                    </p>

                                    <strong>
                                    ✅ Advantages
                                    </strong>

                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )


                                for pro in solution["pros"]:

                                    st.write(
                                        f"• {pro}"
                                    )


                                st.markdown(
                                    "**❌ Disadvantages**"
                                )


                                for con in solution["cons"]:

                                    st.write(
                                        f"• {con}"
                                    )


                        # ==================================================
                        # AI DEBATE
                        # ==================================================

                        st.markdown("---")

                        st.markdown(
                            "### ⚔️ AI Debate"
                        )

                        st.caption(
                            "The AI compares the alternatives "
                            "and highlights their trade-offs. "
                            "It does not make the final decision."
                        )


                        # ==================================================
                        # COMPARE SOLUTIONS
                        # ==================================================

                        if st.button(
                            "⚔️ Compare Solutions",
                            key=f"debate_{theme_index}"
                        ):

                            with st.spinner(
                                "Gemini is comparing "
                                "the solutions..."
                            ):

                                debate_result = (
                                    debate_solutions(
                                        theme_name=theme["theme"],
                                        insight=insight["insight"],
                                        evidence=representative_reviews,
                                        solutions=solutions
                                    )
                                )


                            if debate_result.get("error"):

                                st.warning(
                                    debate_result["error"]
                                )

                            else:

                                st.session_state.debates[
                                    theme_index
                                ] = debate_result


                        # ==================================================
                        # RETRIEVE SAVED DEBATE
                        # ==================================================

                        debate_result = (
                            st.session_state.debates.get(
                                theme_index
                            )
                        )


                        # ==================================================
                        # DISPLAY DEBATE
                        # ==================================================

                        if debate_result:

                            debate_options = (
                                debate_result.get(
                                    "options",
                                    []
                                )
                            )


                            for option in debate_options:

                                st.markdown(
                                    f"#### 🧠 {option['title']}"
                                )


                                # --------------------------------------------------
                                # STRENGTHS
                                # --------------------------------------------------

                                st.markdown(
                                    "**💪 Strengths**"
                                )

                                for strength in option[
                                    "strengths"
                                ]:

                                    st.write(
                                        f"• {strength}"
                                    )


                                # --------------------------------------------------
                                # WEAKNESSES
                                # --------------------------------------------------

                                st.markdown(
                                    "**⚠️ Weaknesses**"
                                )

                                for weakness in option[
                                    "weaknesses"
                                ]:

                                    st.write(
                                        f"• {weakness}"
                                    )


                                # --------------------------------------------------
                                # TRADE-OFF
                                # --------------------------------------------------

                                st.markdown(
                                    "**⚖️ Trade-off**"
                                )

                                st.write(
                                    option["tradeoffs"]
                                )


                                # --------------------------------------------------
                                # SCORES
                                # --------------------------------------------------

                                scores = option["scores"]


                                st.markdown(
                                    "**📊 Evaluation**"
                                )


                                score_col1, score_col2 = (
                                    st.columns(2)
                                )


                                with score_col1:

                                    st.write(
                                        "Customer Impact"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                scores[
                                                    "customer_impact"
                                                ] / 10,
                                                0
                                            ),
                                            1
                                        )
                                    )


                                    st.write(
                                        "Feasibility"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                scores[
                                                    "feasibility"
                                                ] / 10,
                                                0
                                            ),
                                            1
                                        )
                                    )


                                    st.write(
                                        "Expected Benefit"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                scores[
                                                    "expected_benefit"
                                                ] / 10,
                                                0
                                            ),
                                            1
                                        )
                                    )


                                with score_col2:

                                    st.write(
                                        "Implementation Complexity"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                scores[
                                                    "implementation_complexity"
                                                ] / 10,
                                                0
                                            ),
                                            1
                                        )
                                    )


                                    st.write(
                                        "Risk"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                scores[
                                                    "risk"
                                                ] / 10,
                                                0
                                            ),
                                            1
                                        )
                                    )


                                st.divider()


                            # ==================================================
                            # OVERALL COMPARISON
                            # ==================================================

                            comparison = (
                                debate_result.get(
                                    "comparison"
                                )
                            )


                            if comparison:

                                st.markdown(
                                    "### ⚖️ Overall Comparison"
                                )

                                st.info(
                                    comparison
                                )


                            # ==================================================
                            # HUMAN DECISION
                            # ==================================================

                            st.markdown("---")

                            st.markdown(
                                "### 👤 Your Decision"
                            )

                            st.caption(
                                "AI has provided the analysis. "
                                "You make the final product decision."
                            )


                            option_titles = [
                                solution["title"]
                                for solution in solutions
                            ]


                            selected_option = st.radio(
                                "Which solution would you choose?",
                                option_titles,
                                key=f"decision_{theme_index}"
                            )


                            # ==================================================
                            # CONFIRM DECISION
                            # ==================================================

                            if st.button(
                                "✅ Confirm Decision",
                                key=f"confirm_{theme_index}"
                            ):

                                st.session_state.decisions[
                                    theme_index
                                ] = selected_option

                                st.success(
                                    f"Decision recorded: "
                                    f"{selected_option}"
                                )

                                st.info(
                                    "The AI provided recommendations "
                                    "and trade-off analysis, but the "
                                    "final decision was made by the "
                                    "human product manager."
                                )


                            # ==================================================
                            # SHOW SAVED DECISION
                            # ==================================================

                            saved_decision = (
                                st.session_state.decisions.get(
                                    theme_index
                                )
                            )


                            if saved_decision:

                                st.success(
                                    f"👤 Human decision: "
                                    f"{saved_decision}"
                                )


                    else:

                        st.info(
                            "Click **Generate Solutions** "
                            "to see AI-generated alternatives."
                        )


        else:

            st.info(
                "Not enough reviews to discover themes."
            )


        # ==================================================
        # SENTIMENT CHART
        # ==================================================

        st.subheader(
            "Sentiment Distribution"
        )

        chart_data = pd.DataFrame({

            "Sentiment": [
                "Positive",
                "Neutral",
                "Negative"
            ],

            "Reviews": [
                positive_count,
                neutral_count,
                negative_count
            ]

        })


        st.bar_chart(
            chart_data.set_index("Sentiment")
        )


        # ==================================================
        # DETAILED RESULTS
        # ==================================================

        st.subheader(
            "Analyzed Feedback"
        )

        st.dataframe(
            sentiment_df,
            use_container_width=True
        )


    # ==================================================
    # ERROR HANDLING
    # ==================================================

    except Exception as e:

        st.error(
            f"Could not analyze the uploaded file: {e}"
        )