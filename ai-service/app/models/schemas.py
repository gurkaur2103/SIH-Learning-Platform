from typing import Literal
from pydantic import BaseModel, Field

class CompetencyInput(BaseModel):
    name: str
    domain: str
    required_level: float = Field(ge=0, le=5)
    demonstrated_level: float = Field(ge=0, le=5)
    role_weight: float = Field(default=1, ge=0, le=1)
    urgency: float = Field(default=1, ge=0, le=1)

class RecommendationRequest(BaseModel):
    gaps: list[CompetencyInput]
    language: str = "English"
    available_minutes: int = Field(default=225, ge=30)

class RoadmapRequest(BaseModel):
    gaps: list[CompetencyInput]
    minutes_per_day: int = Field(default=45, ge=10, le=480)
    days_per_week: int = Field(default=5, ge=1, le=7)
    weeks: int = Field(default=8, ge=1, le=52)

class QuizRequest(BaseModel):
    document_id: str
    count: int = Field(default=5, ge=1, le=30)
    difficulty: Literal["easy", "medium", "hard", "mixed"] = "mixed"
    language: str = "English"
    bloom_levels: list[str] = ["understand", "apply"]

class TutorRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=2, max_length=3000)
    language: str = "English"

class MasteryRequest(BaseModel):
    accuracy: float = Field(ge=0, le=100)
    difficulty: float = Field(ge=0, le=100)
    retention: float = Field(ge=0, le=100)
    consistency: float = Field(ge=0, le=100)
    practical: float = Field(ge=0, le=100)

class AttemptInput(BaseModel):
    competency: str
    correct: bool
    difficulty: Literal["easy", "medium", "hard"]
    response_seconds: int = 0
    hints_used: int = 0
