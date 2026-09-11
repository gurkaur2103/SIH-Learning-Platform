from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analytics, competency, profile, quiz, recommendation, roadmap, tutor

app=FastAPI(title="KarmSankhya AI Service",version="1.0.0",
            description="Competency intelligence, adaptive learning and grounded assessment APIs.")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3000"],
                   allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
for router in [profile.router,competency.router,recommendation.router,
               roadmap.router,quiz.router,tutor.router,analytics.router]:
    app.include_router(router,prefix="/api/v1")

@app.get("/health")
async def health():
    import os
    return {"status":"ok","gemini_configured":bool(os.getenv("GEMINI_API_KEY"))}
