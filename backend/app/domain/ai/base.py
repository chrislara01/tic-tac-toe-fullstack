from __future__ import annotations

from abc import ABC, abstractmethod

from ..board import Board
from ..enums import Player


class Strategy(ABC):
    """Strategy interface for AI players.

    select_move returns the external position (1..9, numpad layout)
    where the AI intends to play.
    """

    @abstractmethod
    def select_move(self, board: Board, me: Player) -> int:
        raise NotImplementedError
