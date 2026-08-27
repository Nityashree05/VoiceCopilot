import os
import json
import time

from google import genai


def generate_recommendations(
    theme_name,
    keywords,
    insight,
    evidence
):
    """
    Generate multiple product solutions using Gemini.

    The model receives analyzed customer evidence
    instead of the entire raw dataset.
    """

    # --------------------------------------------------
    # CHECK API KEY
    # --------------------------------------------------

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        return {
            "solutions": [],
            "error": "GEMINI_API_KEY is not configured."
        }


    # --------------------------------------------------
    # CREATE GEMINI CLIENT
    # --------------------------------------------------

    client = genai.Client(
        api_key=api_key
    )


    # --------------------------------------------------
    # PREPARE CUSTOMER EVIDENCE
    # --------------------------------------------------

    evidence_text = "\n".join(
        f"- {review}"
        for review in evidence
    )


    # --------------------------------------------------
    # CREATE PROMPT
    # --------------------------------------------------

    prompt = f"""
You are VoiceCopilot, an AI product management assistant.

Your job is to help a product manager understand
customer problems and propose possible solutions.

IMPORTANT:
- Use only the evidence provided.
- Do not invent customer complaints.
- Do not claim that a solution is definitely correct.
- Generate different alternatives with different trade-offs.
- The final product decision will be made by a human.

CUSTOMER THEME:
{theme_name}

KEYWORDS:
{keywords}

ANALYZED INSIGHT:
{insight}

CUSTOMER EVIDENCE:
{evidence_text}

Generate exactly 3 different possible product solutions.

For each solution provide:

1. title
2. description
3. exactly 2 advantages
4. exactly 2 disadvantages

The three solutions should be meaningfully different.

Return ONLY valid JSON in this format:

{{
    "solutions": [
        {{
            "title": "Solution title",
            "description": "Clear explanation",
            "pros": [
                "Advantage 1",
                "Advantage 2"
            ],
            "cons": [
                "Disadvantage 1",
                "Disadvantage 2"
            ]
        }}
    ]
}}
"""


    # --------------------------------------------------
    # AVAILABLE MODELS
    # --------------------------------------------------

    models_to_try = [
        "gemini-3.1-flash-lite-preview",
        "gemini-3.1-flash-preview"
    ]


    # --------------------------------------------------
    # TRY AVAILABLE GEMINI MODELS
    # --------------------------------------------------

    response = None

    for model_name in models_to_try:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )

                # Successful response
                break

            except Exception as e:

                # Try again after a short delay
                if attempt == 0:

                    time.sleep(3)

                else:

                    # Move to the next model
                    response = None

                    break


        # If a model worked, stop trying
        if response is not None:
            break


    # --------------------------------------------------
    # IF ALL MODELS FAILED
    # --------------------------------------------------

    if response is None:

        return {
            "solutions": [],
            "error": (
                "Gemini is temporarily unavailable. "
                "Please try again later."
            )
        }


    # --------------------------------------------------
    # GET MODEL RESPONSE
    # --------------------------------------------------

    response_text = response.text.strip()


    # --------------------------------------------------
    # REMOVE MARKDOWN CODE BLOCK
    # --------------------------------------------------

    if response_text.startswith("```"):

        response_text = (
            response_text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )


    # --------------------------------------------------
    # CONVERT JSON TO PYTHON OBJECT
    # --------------------------------------------------

    try:

        result = json.loads(
            response_text
        )

        return result

    except json.JSONDecodeError:

        return {
            "solutions": [],
            "error": (
                "Gemini returned an invalid JSON response."
            ),
            "raw_response": response_text
        }