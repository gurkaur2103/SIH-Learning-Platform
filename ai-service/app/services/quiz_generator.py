import json
import os
from pathlib import Path

from google import genai
from google.genai.errors import ServerError

from app.services.question_validator import audit_quiz

PROMPT = Path(__file__).parents[1] / "prompts" / "quiz_generation.txt"


def create_fallback_quiz(source: str) -> list[dict]:
    quote = source[:180].strip()

    return [
        {
            "question": (
                "Which statement is directly supported "
                "by the uploaded material?"
            ),
            "options": [
                "The statement shown in the source passage",
                "An unrelated claim",
                "An unsupported exception",
                "None of the material",
            ],
            "correct_index": 0,
            "explanation": (
                "The first option is supported by the retrieved source."
            ),
            "competency": "Document comprehension",
            "bloom_level": "understand",
            "difficulty": "medium",
            "supporting_quote": quote,
            "source_marker": "document",
            "confidence": 0.65,
        }
    ]


def generate_quiz(
    source: str,
    count: int,
    difficulty: str,
    language: str,
    bloom_levels: list[str],
) -> dict:

    api_key = os.getenv("GEMINI_API_KEY")
    fallback_used = False
    fallback_reason = None

    if api_key:
        try:
            client = genai.Client(api_key=api_key)

            response = client.models.generate_content(
                model=os.getenv(
                    "GEMINI_MODEL",
                    "gemini-3.6-flash",
                ),
                contents=(
                    f"{PROMPT.read_text()}\n"
                    f"Count: {count}\n"
                    f"Difficulty: {difficulty}\n"
                    f"Language: {language}\n"
                    f"Bloom: {bloom_levels}\n"
                    f"SOURCE:\n{source[:70000]}"
                ),
                config={
                    "response_mime_type": "application/json"
                },
            )

            questions = json.loads(response.text)

        except ServerError as error:
            # Gemini may temporarily return 503 during high demand.
            questions = create_fallback_quiz(source)
            fallback_used = True
            fallback_reason = (
                "Gemini is temporarily unavailable because of high demand."
            )

        except (json.JSONDecodeError, TypeError, ValueError) as error:
            questions = create_fallback_quiz(source)
            fallback_used = True
            fallback_reason = (
                "Gemini returned an invalid quiz response."
            )

    else:
        questions = create_fallback_quiz(source)
        fallback_used = True
        fallback_reason = "GEMINI_API_KEY is not configured."

    return {
        "questions": questions,
        "validation": audit_quiz(questions, source),
        "fallback_used": fallback_used,
        "fallback_reason": fallback_reason,
    }