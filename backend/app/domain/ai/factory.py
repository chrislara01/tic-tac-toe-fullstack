from __future__ import annotations

from app.domain.enums import Difficulty
from app.domain.ai.base import Strategy
from app.domain.ai.easy import RandomStrategy
from app.domain.ai.medium import HeuristicStrategy

def strategy_for(
    difficulty: Difficulty,
    gemini_api_key: str | None = None,
    gemini_model: str = "gemini-2.0-flash",
) -> Strategy:
    if difficulty == Difficulty.EASY:
        return RandomStrategy()
    if difficulty == Difficulty.MEDIUM:
        return HeuristicStrategy()
    # HARD: prefer Gemini if API key is provided; otherwise fallback to heuristic
    if gemini_api_key:
        from .gemini import GeminiStrategy

        return GeminiStrategy(api_key=gemini_api_key, model=gemini_model)
    return HeuristicStrategy()
