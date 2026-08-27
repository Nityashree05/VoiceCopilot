from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_representative_reviews(
    reviews,
    max_reviews=3
):
    """
    Select the most representative reviews
    from a group of reviews.
    """

    # If there are no reviews
    if not reviews:
        return []

    # If there are very few reviews,
    # simply return them
    if len(reviews) <= max_reviews:
        return reviews

    # Convert reviews into TF-IDF vectors
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(
        reviews
    )

    # Calculate how similar every review is
    # to every other review
    similarity_matrix = cosine_similarity(
        tfidf_matrix
    )

    # Calculate average similarity of each review
    # to all other reviews
    average_similarity = (
        similarity_matrix.sum(axis=1)
        - 1
    ) / (len(reviews) - 1)

    # Select reviews with highest average similarity
    representative_indices = (
        average_similarity
        .argsort()[::-1][:max_reviews]
    )

    return [
        reviews[index]
        for index in representative_indices
    ]