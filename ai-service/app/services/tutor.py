import json, os
from pathlib import Path
from google import genai
from app.services.rag_service import rag

PROMPT = Path(__file__).parents[1]/"prompts"/"tutor.txt"

def answer(document_id: str, question: str, language: str) -> dict:
    chunks = rag.retrieve(document_id,question)
    source = "\n\n".join(f"[{c['id']}] {c['text']}" for c in chunks)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return {"answer":"Gemini is not configured. The most relevant source passage is shown below.",
                "citations":chunks[:1],"grounded":False}
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
      model=os.getenv("GEMINI_MODEL","gemini-2.5-flash"),
      contents=f"{PROMPT.read_text()}\nLanguage:{language}\nQUESTION:{question}\nSOURCE:{source}",
      config={"response_mime_type":"application/json"})
    return {**json.loads(response.text),"grounded":True}
