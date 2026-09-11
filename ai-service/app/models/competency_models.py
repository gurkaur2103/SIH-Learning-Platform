from dataclasses import dataclass, field

@dataclass
class CompetencyNode:
    name: str
    domain: str
    prerequisites: list[str] = field(default_factory=list)
    required_level: float = 1

@dataclass
class Course:
    id: str
    title: str
    competencies: list[str]
    level: str
    duration_minutes: int
    languages: list[str]

@dataclass
class SourceChunk:
    id: str
    document_id: str
    text: str
    page: int | None = None
    slide: int | None = None
