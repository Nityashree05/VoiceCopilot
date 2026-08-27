from debate import debate_solutions


solutions = [

    {
        "title": "Automatic Payment Retry",
        "description": (
            "Automatically retry failed payments "
            "before asking the customer to try again."
        ),
        "pros": [
            "Can recover failed transactions",
            "Relatively small implementation"
        ],
        "cons": [
            "Does not solve all checkout problems",
            "Repeated retries may frustrate users"
        ]
    },

    {
        "title": "Checkout Redesign",
        "description": (
            "Redesign the checkout experience to "
            "reduce payment and usability problems."
        ),
        "pros": [
            "Addresses multiple checkout issues",
            "Potentially improves overall conversion"
        ],
        "cons": [
            "Higher development effort",
            "Longer implementation time"
        ]
    },

    {
        "title": "Alternative Payment Methods",
        "description": (
            "Add additional payment providers so "
            "customers have fallback options."
        ),
        "pros": [
            "Provides payment alternatives",
            "Reduces dependence on one provider"
        ],
        "cons": [
            "Requires additional integrations",
            "More systems to maintain"
        ]
    }
]


result = debate_solutions(

    theme_name="Payment & Checkout",

    insight=(
        "Payment and checkout problems appear in "
        "6 customer reviews with 83.3% negative sentiment."
    ),

    evidence=[
        "Payment failed three times when I tried to checkout.",
        "The payment page keeps crashing.",
        "Checkout is broken and payment does not work."
    ],

    solutions=solutions
)


print(result)