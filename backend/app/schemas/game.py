from __future__ import annotations

from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator

from ..domain.enums import Difficulty, GameStatus, Player


class CreateGameRequest(BaseModel):
    difficulty: Difficulty = Field(default=Difficulty.EASY)
    first_player: Literal["human", "computer"] = Field(default="human")
    human_symbol: Player = Field(default=Player.X)


class GameRead(BaseModel):
    id: str
    board: str
    next_player: Player
    difficulty: Difficulty
    status: GameStatus
    human_symbol: Player
    computer_symbol: Player
    moves: List[int]
    created_at: datetime
    updated_at: datetime


class CreateGameResponse(GameRead):
    pass


class MoveRequest(BaseModel):
    position: int = Field(ge=1, le=9, description="Position in numpad layout 1..9")


class MoveResponse(GameRead):
    ai_move: Optional[int] = None
