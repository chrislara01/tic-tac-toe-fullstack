from __future__ import annotations

from ..enums import Difficulty
from .base import Strategy
from .easy import RandomStrategy
from .medium import HeuristicStrategy


def strategy_for(difficulty: Difficulty) -> Strategy:
    if difficulty == Difficulty.EASY:
        return RandomStrategy()
    if difficulty == Difficulty.MEDIUM:
        return HeuristicStrategy()
    # HARD will be wired to Gemini later; for now fallback to heuristic
    return HeuristicStrategy()
