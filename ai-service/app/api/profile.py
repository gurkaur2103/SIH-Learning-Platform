from fastapi import APIRouter, File, HTTPException, UploadFile
from app.services.document_parser import parse_document
from app.services.profile_extractor import extract_profile

router=APIRouter(prefix="/profile",tags=["Profile"])
@router.post("/extract")
async def profile(file:UploadFile=File(...)):
    try: parsed=parse_document(await file.read(),file.filename or "profile.pdf")
    except ValueError as exc: raise HTTPException(400,str(exc))
    return {"document":{k:v for k,v in parsed.items() if k!="text" and k!="chunks"},
            "profile":extract_profile(parsed["text"])}
