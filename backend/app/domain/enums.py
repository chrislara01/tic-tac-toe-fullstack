from __future__ import annotations

from enum import Enum


class Player(str, Enum):
    X = "x"
    O = "o"

    @property
    def other(self) -> "Player":
        return Player.O if self is Player.X else Player.X


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    X_WON = "x_won"
    O_WON = "o_won"
    DRAW = "draw"
