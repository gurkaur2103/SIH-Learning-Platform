from fastapi import APIRouter
from app.models.schemas import RecommendationRequest
from app.services.recommender import recommend_courses

router=APIRouter(prefix="/recommendations",tags=["Recommendations"])
@router.post("")
async def recommendations(body:RecommendationRequest):
    return {"source":"local_iGOT_ready_catalogue","courses":recommend_courses(body)}
