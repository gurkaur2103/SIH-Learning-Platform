from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.schemas import QuizRequest
from app.services.document_parser import parse_document
from app.services.quiz_generator import generate_quiz
from app.services.rag_service import rag

router=APIRouter(prefix="/quizzes",tags=["Quizzes"])
@router.post("/documents")
async def ingest(file:UploadFile=File(...)):
    data=await file.read()
    if len(data)>25*1024*1024: raise HTTPException(413,"File exceeds 25 MB")
    try: parsed=parse_document(data,file.filename or "upload")
    except ValueError as exc: raise HTTPException(400,str(exc))
    document_id=rag.ingest(parsed)
    return {"document_id":document_id,"filename":parsed["filename"],
            "chunks":len(parsed["chunks"]),"characters":parsed["characters"]}

@router.post("/generate")
async def quiz(body:QuizRequest):
    try: source=rag.get(body.document_id)["text"]
    except KeyError: raise HTTPException(404,"Document not found")
    return generate_quiz(source,body.count,body.difficulty,body.language,body.bloom_levels)
