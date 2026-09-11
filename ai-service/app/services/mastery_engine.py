from app.models.schemas import AttemptInput, MasteryRequest
from app.utils.scoring import diagnostic_score, mastery_score

def calculate_mastery(request: MasteryRequest) -> dict:
    score = mastery_score(**request.model_dump())
    return {"mastery_score":score,
      "level":5 if score>=90 else 4 if score>=75 else 3 if score>=60 else 2 if score>=40 else 1,
      "action":"advance" if score>=80 else "revise" if score>=60 else "remediate"}

def analyze_attempts(attempts: list[AttemptInput]) -> dict:
    rows=[a.model_dump() for a in attempts]
    score=diagnostic_score(rows)
    return {"diagnostic_score":score,
      "next_difficulty":"hard" if score>=80 else "medium" if score>=55 else "easy",
      "needs_prerequisite_check":score<55}
