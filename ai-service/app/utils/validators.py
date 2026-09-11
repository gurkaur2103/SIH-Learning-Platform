import re

def clean_text(text: str) -> str:
    text = re.sub(r"\x00", "", text)
    return re.sub(r"[ \t]+", " ", text).strip()

def validate_question(question: dict) -> list[str]:
    errors = []
    required = {"question", "options", "correct_index", "explanation",
                "supporting_quote", "source_marker"}
    missing = required - set(question)
    if missing: errors.append(f"Missing fields: {sorted(missing)}")
    options = question.get("options", [])
    if len(options) != 4: errors.append("Exactly four options are required")
    if len(set(map(str.casefold, options))) != len(options):
        errors.append("Duplicate options detected")
    index = question.get("correct_index")
    if not isinstance(index, int) or not 0 <= index < len(options):
        errors.append("Invalid correct_index")
    if not question.get("supporting_quote", "").strip():
        errors.append("Question has no source evidence")
    return errors
