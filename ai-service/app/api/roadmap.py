from fastapi import APIRouter
from app.models.schemas import RoadmapRequest
from app.services.roadmap_engine import generate_roadmap

router=APIRouter(prefix="/roadmaps",tags=["Roadmaps"])
@router.post("")
async def roadmap(body:RoadmapRequest): return generate_roadmap(body)
