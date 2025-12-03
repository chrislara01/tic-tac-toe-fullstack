from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.game import Game


class GameRepository(ABC):
    @abstractmethod
    def get(self, game_id: str) -> Optional[Game]:
        raise NotImplementedError

    @abstractmethod
    def save(self, game: Game) -> Game:
        raise NotImplementedError
