import os
import json
import time

from google import genai


def debate_solutions(
    theme_name,
    insight,
    evidence,
    solutions
):
    """
    Compare multiple AI-generated product solutions.

    The AI evaluates trade-offs but does NOT make
    the final product decision.
    """

    # --------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        return {
            "debate": [],
            "error": "GEMINI_API_KEY is not configured."
        }


    # --------------------------------------------------
    # CHECK SOLUTIONS
    # --------------------------------------------------

    if not solutions:

        return {
            "debate": [],
            "error": "No solutions available for debate."
        }


    # --------------------------------------------------
    # CREATE GEMINI CLIENT
    # --------------------------------------------------

    client = genai.Client(
        api_key=api_key
    )


    # --------------------------------------------------
    # PREPARE SOLUTIONS
    # --------------------------------------------------

    solutions_text = ""

    for i, solution in enumerate(
        solutions,
        start=1
    ):

        solutions_text += f"""
OPTION {i}
Title:
{solution.get("title", "")}

Description:
{solution.get("description", "")}

Advantages:
{solution.get("pros", [])}

Disadvantages:
{solution.get("cons", [])}

"""


    # --------------------------------------------------
    # PREPARE EVIDENCE
    # --------------------------------------------------

    evidence_text = "\n".join(
        f"- {review}"
        for review in evidence
    )


    # --------------------------------------------------
    # CREATE DEBATE PROMPT
    # --------------------------------------------------

    prompt = f"""
You are the decision-support component of
VoiceCopilot.

A product team has identified a customer problem
and generated multiple possible solutions.

Your job is NOT to make the final decision.

Instead, critically compare the alternatives and
explain the trade-offs so that a human product
manager can make the final decision.

CUSTOMER THEME:
{theme_name}

CUSTOMER INSIGHT:
{insight}

CUSTOMER EVIDENCE:
{evidence_text}

POSSIBLE SOLUTIONS:
{solutions_text}

Evaluate each option using:

1. Customer Impact
2. Feasibility
3. Implementation Complexity
4. Expected Benefit
5. Risk

For each option provide:

- strengths
- weaknesses
- tradeoffs
- scores from 1 to 10 for each criterion

Then provide a short comparison explaining
when each option would be preferable.

IMPORTANT:

Do NOT say that one option is definitely the
correct decision.

Do NOT make the final product decision.

The final decision must remain with the human
product manager.

Return ONLY valid JSON.

Use this structure:

{{
    "options": [
        {{
            "title": "...",
            "strengths": [
                "...",
                "..."
            ],
            "weaknesses": [
                "...",
                "..."
            ],
            "tradeoffs": "...",
            "scores": {{
                "customer_impact": 1,
                "feasibility": 1,
                "implementation_complexity": 1,
                "expected_benefit": 1,
                "risk": 1
            }}
        }}
    ],

    "comparison": "..."
}}
"""


    # --------------------------------------------------
    # MODELS
    # --------------------------------------------------

    models_to_try = [
        "gemini-3.1-flash-lite-preview",
        "gemini-3.1-flash-preview"
    ]


    # --------------------------------------------------
    # CALL GEMINI
    # --------------------------------------------------

    response = None

    for model_name in models_to_try:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                break

            except Exception:

                if attempt == 0:

                    time.sleep(3)

                else:

                    response = None
                    break


        if response is not None:
            break


    # --------------------------------------------------
    # HANDLE FAILURE
    # --------------------------------------------------

    if response is None:

        return {
            "debate": [],
            "error": (
                "Gemini is temporarily unavailable. "
                "Please try again later."
            )
        }


    # --------------------------------------------------
    # GET RESPONSE
    # --------------------------------------------------

    response_text = response.text.strip()


    # --------------------------------------------------
    # REMOVE MARKDOWN
    # --------------------------------------------------

    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    # --------------------------------------------------
    # PARSE JSON
    # --------------------------------------------------

    try:

        result = json.loads(
            response_text
        )

        return result

    except json.JSONDecodeError:

        return {
            "debate": [],
            "error": (
                "Gemini returned invalid JSON."
            ),
            "raw_response": response_text
        }