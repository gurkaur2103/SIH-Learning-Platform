from fastapi import APIRouter
from app.models.schemas import AttemptInput, MasteryRequest
from app.services.mastery_engine import analyze_attempts, calculate_mastery

router=APIRouter(prefix="/analytics",tags=["Analytics"])
@router.post("/mastery")
async def mastery(body:MasteryRequest): return calculate_mastery(body)
@router.post("/attempts")
async def attempts(body:list[AttemptInput]): return analyze_attempts(body)
