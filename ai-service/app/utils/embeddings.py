import hashlib
import math
import re
from collections import Counter

def embed(text: str, dimensions: int = 384) -> list[float]:
    """Dependency-free hashing embedding for local semantic retrieval."""
    vector = [0.0] * dimensions
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        index = int(hashlib.sha256(token.encode()).hexdigest(), 16) % dimensions
        vector[index] += 1
    norm = math.sqrt(sum(v*v for v in vector)) or 1
    return [v/norm for v in vector]

def cosine(a: list[float], b: list[float]) -> float:
    return sum(x*y for x, y in zip(a, b))
