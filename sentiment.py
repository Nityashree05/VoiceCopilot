from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Create the sentiment analyzer once
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze one customer review.

    Returns:
        sentiment label
        sentiment score
    """

    scores = analyzer.polarity_scores(text)

    compound_score = scores["compound"]

    if compound_score >= 0.05:
        sentiment = "Positive"

    elif compound_score <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "score": compound_score
    }


def analyze_reviews(reviews):
    """
    Analyze a list of customer reviews.
    """

    results = []

    for review in reviews:

        result = analyze_sentiment(review)

        results.append({
            "review": review,
            "sentiment": result["sentiment"],
            "sentiment_score": result["score"]
        })

    return results