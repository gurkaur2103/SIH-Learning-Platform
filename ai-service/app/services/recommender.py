import json
from pathlib import Path
from app.models.schemas import RecommendationRequest
from app.utils.embeddings import cosine, embed
from app.utils.scoring import recommendation_score

COURSES = Path(__file__).parents[1]/"data"/"courses.json"

def recommend_courses(request: RecommendationRequest) -> list[dict]:
    courses = json.loads(COURSES.read_text())
    targets = " ".join(g.name for g in request.gaps if g.required_level>g.demonstrated_level)
    target_vector = embed(targets)
    output = []
    for course in courses:
        match = max(0, cosine(target_vector,embed(" ".join(course["competencies"]))))
        language = 1 if request.language in course["languages"] else .3
        time = min(1, request.available_minutes/course["duration_minutes"])
        score = recommendation_score(match,1,time,1,language)
        output.append({**course,"score":score,
          "reason":f"Matches {', '.join(course['competencies'])}; available in {', '.join(course['languages'])}."})
    return sorted(output,key=lambda x:x["score"],reverse=True)
