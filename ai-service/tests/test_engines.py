from app.models.schemas import CompetencyInput, MasteryRequest, RoadmapRequest
from app.services.gap_engine import calculate_gaps
from app.services.mastery_engine import calculate_mastery
from app.services.roadmap_engine import generate_roadmap

def test_gap_ranking():
    rows=[CompetencyInput(name="A",domain="x",required_level=4,demonstrated_level=3,role_weight=.5),
          CompetencyInput(name="B",domain="x",required_level=4,demonstrated_level=1)]
    assert calculate_gaps(rows)[0]["name"]=="B"

def test_roadmap_length():
    gap=CompetencyInput(name="Sampling",domain="Statistical",required_level=4,demonstrated_level=2)
    assert len(generate_roadmap(RoadmapRequest(gaps=[gap],weeks=8))["weeks"])==8

def test_mastery_action():
    result=calculate_mastery(MasteryRequest(accuracy=90,difficulty=80,retention=80,consistency=90,practical=85))
    assert result["action"]=="advance"
