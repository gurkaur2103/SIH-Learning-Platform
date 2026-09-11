from fastapi import APIRouter, HTTPException
from app.models.schemas import TutorRequest
from app.services.tutor import answer

router=APIRouter(prefix="/tutor",tags=["Tutor"])
@router.post("/chat")
async def chat(body:TutorRequest):
    try: return answer(body.document_id,body.question,body.language)
    except KeyError: raise HTTPException(404,"Document not found")
