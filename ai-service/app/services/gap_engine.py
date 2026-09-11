from app.models.schemas import CompetencyInput

def calculate_gaps(items: list[CompetencyInput]) -> list[dict]:
    result = []
    for item in items:
        gap = max(0, item.required_level-item.demonstrated_level)
        score = gap*item.role_weight*item.urgency
        result.append({**item.model_dump(),"gap":gap,
          "priority_score":round(score,3),
          "priority":"high" if score>=1.6 else "medium" if score>=.75 else "low",
          "explanation":f"{item.name} requires Level {item.required_level:g}, while demonstrated evidence indicates Level {item.demonstrated_level:g}."})
    return sorted(result,key=lambda x:x["priority_score"],reverse=True)
