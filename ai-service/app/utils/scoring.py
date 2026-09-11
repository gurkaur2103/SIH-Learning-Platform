DIFFICULTY_WEIGHTS = {"easy": 1.0, "medium": 1.5, "hard": 2.0}

def diagnostic_score(answers: list[dict]) -> float:
    denominator = sum(DIFFICULTY_WEIGHTS[a["difficulty"]] for a in answers) or 1
    numerator = sum(DIFFICULTY_WEIGHTS[a["difficulty"]] for a in answers if a["correct"])
    return round(numerator / denominator * 100, 2)

def mastery_score(accuracy: float, difficulty: float, retention: float,
                  consistency: float, practical: float) -> float:
    return round(.35*accuracy + .20*difficulty + .15*retention +
                 .15*consistency + .15*practical, 2)

def recommendation_score(match: float, level: float, time: float,
                         prerequisites: float, language: float) -> float:
    return round(.40*match + .20*level + .15*time +
                 .15*prerequisites + .10*language, 4)
