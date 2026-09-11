from fastapi import APIRouter
from app.models.schemas import CompetencyInput
from app.services.gap_engine import calculate_gaps

router=APIRouter(prefix="/competencies",tags=["Competencies"])
@router.post("/gaps")
async def gaps(items:list[CompetencyInput]): return calculate_gaps(items)
