import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def discover_themes(reviews, number_of_themes=5):
    """
    Discover recurring themes in customer feedback
    using TF-IDF and K-Means clustering.

    Also keeps track of which reviews belong
    to each theme.
    """

    # We need at least 2 reviews
    if len(reviews) < 2:
        return pd.DataFrame()

    # We cannot create more clusters than reviews
    number_of_themes = min(
        number_of_themes,
        len(reviews)
    )

    # --------------------------------------------------
    # STEP 1: Convert reviews into TF-IDF vectors
    # --------------------------------------------------

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=1000,
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        reviews
    )

    # --------------------------------------------------
    # STEP 2: Group similar reviews
    # --------------------------------------------------

    model = KMeans(
        n_clusters=number_of_themes,
        random_state=42,
        n_init=10
    )

    clusters = model.fit_predict(
        tfidf_matrix
    )

    # --------------------------------------------------
    # STEP 3: Get important words for each theme
    # --------------------------------------------------

    feature_names = (
        vectorizer.get_feature_names_out()
    )

    theme_rows = []

    for cluster_number in range(
        number_of_themes
    ):

        # Find the reviews belonging to
        # this particular cluster
        cluster_indices = [
            i
            for i, cluster in enumerate(clusters)
            if cluster == cluster_number
        ]

        # Get the TF-IDF vectors
        # belonging to this cluster
        cluster_vectors = tfidf_matrix[
            cluster_indices
        ]

        # Calculate average TF-IDF score
        # for every word in this cluster
        average_scores = cluster_vectors.mean(
            axis=0
        )

        average_scores = average_scores.A1

        # Get the most important words
        top_indices = (
            average_scores
            .argsort()[-5:][::-1]
        )

        keywords = [
            feature_names[i]
            for i in top_indices
        ]

        # --------------------------------------------------
        # NEW: Store the actual reviews
        # belonging to this theme
        # --------------------------------------------------

        cluster_reviews = [
            reviews[i]
            for i in cluster_indices
        ]

        theme_rows.append({
            "theme": f"Theme {cluster_number + 1}",

            "keywords": ", ".join(
                keywords
            ),

            "review_count": len(
                cluster_reviews
            ),

            "percentage": round(
                len(cluster_reviews)
                / len(reviews)
                * 100,
                1
            ),

            "reviews": cluster_reviews
        })

    return pd.DataFrame(
        theme_rows
    )