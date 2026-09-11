from uuid import uuid4
from app.utils.embeddings import cosine, embed

class InMemoryRAG:
    def __init__(self):
        self.documents: dict[str, dict] = {}

    def ingest(self, parsed: dict) -> str:
        document_id = str(uuid4())
        chunks = []
        for chunk in parsed["chunks"]:
            chunks.append({**chunk, "embedding":embed(chunk["text"])})
        self.documents[document_id] = {**parsed, "chunks":chunks}
        return document_id

    def retrieve(self, document_id: str, query: str, limit: int = 5) -> list[dict]:
        document = self.documents.get(document_id)
        if not document: raise KeyError("Document not found")
        query_vector = embed(query)
        ranked = sorted(document["chunks"],
                        key=lambda c:cosine(query_vector,c["embedding"]), reverse=True)
        return [{k:v for k,v in c.items() if k!="embedding"} for c in ranked[:limit]]

    def get(self, document_id: str) -> dict:
        if document_id not in self.documents: raise KeyError("Document not found")
        return self.documents[document_id]

rag = InMemoryRAG()
