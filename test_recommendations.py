from recommendations import generate_recommendations


result = generate_recommendations(
    theme_name="Payment & Checkout",
    keywords="payment, checkout, failed, transaction",
    insight=(
        "This theme appears in 6 customer reviews, "
        "with 83.3% showing negative sentiment. "
        "It is currently classified as a high priority issue."
    ),
    evidence=[
        "Payment failed three times when I tried to checkout.",
        "The payment page keeps crashing.",
        "Checkout is broken and payment does not work."
    ]
)

print(result)