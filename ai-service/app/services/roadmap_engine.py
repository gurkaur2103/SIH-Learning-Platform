from app.models.schemas import RoadmapRequest
from app.services.gap_engine import calculate_gaps

def generate_roadmap(request: RoadmapRequest) -> dict:
    gaps = [g for g in calculate_gaps(request.gaps) if g["gap"]>0]
    weekly_minutes = request.minutes_per_day*request.days_per_week
    weeks = []
    for index in range(request.weeks):
        gap = gaps[index%len(gaps)] if gaps else None
        weeks.append({"week":index+1,
          "competency":gap["name"] if gap else "Retention and consolidation",
          "minutes":weekly_minutes,
          "activities":["Learn","Guided practice","Assessment"],
          "reason":gap["explanation"] if gap else "No active gap."})
    return {"weekly_capacity_minutes":weekly_minutes,"weeks":weeks}
