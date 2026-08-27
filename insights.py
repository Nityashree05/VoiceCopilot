# --------------------------------------------------
# THEME INSIGHT CALCULATION
# --------------------------------------------------


def calculate_theme_insight(
    theme_reviews,
    sentiment_df
):
    """
    Calculate useful product insight for a theme.

    Returns:
    - review count
    - negative count
    - negative percentage
    - priority
    - human-readable insight
    """

    # --------------------------------------------------
    # TOTAL REVIEWS IN THEME
    # --------------------------------------------------

    total_theme_reviews = len(theme_reviews)


    # --------------------------------------------------
    # HANDLE EMPTY THEME
    # --------------------------------------------------

    if total_theme_reviews == 0:

        return {
            "review_count": 0,
            "negative_count": 0,
            "negative_rate": 0.0,
            "priority": "Low",
            "insight": (
                "There is not enough customer feedback "
                "to identify a meaningful issue."
            )
        }


    # --------------------------------------------------
    # FIND SENTIMENT FOR THEME REVIEWS
    # --------------------------------------------------

    theme_sentiments = sentiment_df[
        sentiment_df["review"].isin(theme_reviews)
    ]


    # --------------------------------------------------
    # COUNT NEGATIVE REVIEWS
    # --------------------------------------------------

    negative_count = (
        theme_sentiments["sentiment"] == "Negative"
    ).sum()


    # --------------------------------------------------
    # CALCULATE NEGATIVE RATE
    # --------------------------------------------------

    negative_rate = (
        negative_count
        / total_theme_reviews
        * 100
    )


    # --------------------------------------------------
    # DETERMINE PRIORITY
    # --------------------------------------------------

    if (
        total_theme_reviews >= 5
        and negative_rate >= 60
    ):

        priority = "High"


    elif (
        total_theme_reviews >= 3
        and negative_rate >= 40
    ):

        priority = "Medium"


    else:

        priority = "Low"


    # --------------------------------------------------
    # CREATE HUMAN-READABLE INSIGHT
    # --------------------------------------------------

    insight = (
        f"This theme appears in "
        f"{total_theme_reviews} customer reviews, "
        f"with {negative_rate:.1f}% showing negative "
        f"sentiment. It is currently classified as a "
        f"{priority.lower()} priority issue."
    )


    # --------------------------------------------------
    # RETURN RESULT
    # --------------------------------------------------

    return {
        "review_count": total_theme_reviews,

        "negative_count": int(
            negative_count
        ),

        "negative_rate": round(
            negative_rate,
            1
        ),

        "priority": priority,

        "insight": insight
    }