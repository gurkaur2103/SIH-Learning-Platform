import json, os
from pathlib import Path
from google import genai

PROMPT = Path(__file__).parents[1]/"prompts"/"profile_extraction.txt"

def extract_profile(text: str) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"mode":"demo","designation":None,"years_experience":None,
                "skills":[],"education":[],"completed_training":[],
                "message":"Set GEMINI_API_KEY for AI extraction."}
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),
        contents=f"{PROMPT.read_text()}\n\nPROFILE:\n{text[:50000]}",
        config={"response_mime_type":"application/json"})
    return json.loads(response.text)
