from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class GameModel(Base):
    __tablename__ = "games"

    # Use string UUIDs for portability
    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # Board stored as 9-character string with 'x', 'o', ' '
    board: Mapped[str] = mapped_column(String(9), nullable=False)

    next_player: Mapped[str] = mapped_column(String(1), nullable=False)  # 'x' | 'o'
    difficulty: Mapped[str] = mapped_column(String(16), nullable=False)  # easy|medium|hard
    status: Mapped[str] = mapped_column(String(32), nullable=False)  # in_progress|x_won|o_won|draw

    human_symbol: Mapped[str] = mapped_column(String(1), nullable=False)
    computer_symbol: Mapped[str] = mapped_column(String(1), nullable=False)

    # Moves in numpad positions (1..9)
    moves: Mapped[Optional[List[int]]] = mapped_column(ARRAY(Integer), nullable=True, default=list)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
