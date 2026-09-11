from app.utils.validators import validate_question

def audit_question(question: dict, source: str) -> dict:
    errors = validate_question(question)
    quote = question.get("supporting_quote","")
    if quote and quote.casefold() not in source.casefold():
        errors.append("Supporting quote is not verbatim in the source")
    score = max(0,100-20*len(errors))
    return {"valid":not errors,"score":score,"errors":errors,
            "suggestions":[] if not errors else ["Regenerate using a narrower source passage"]}

def audit_quiz(questions: list[dict], source: str) -> dict:
    reports = [audit_question(q,source) for q in questions]
    return {"score":round(sum(r["score"] for r in reports)/max(len(reports),1),2),
            "valid":all(r["valid"] for r in reports),"questions":reports}
