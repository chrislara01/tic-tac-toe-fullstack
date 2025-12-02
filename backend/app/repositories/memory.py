from __future__ import annotations

from threading import RLock
from typing import Dict, Optional

from ..domain.game import Game
from .base import GameRepository


class InMemoryGameRepository(GameRepository):
    def __init__(self) -> None:
        self._store: Dict[str, Game] = {}
        self._lock = RLock()

    def get(self, game_id: str) -> Optional[Game]:
        with self._lock:
            return self._store.get(game_id)

    def save(self, game: Game) -> Game:
        with self._lock:
            self._store[game.id] = game
        return game
