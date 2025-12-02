from __future__ import annotations

import random

from ..board import Board
from ..enums import Player
from .base import Strategy


class RandomStrategy(Strategy):
    def select_move(self, board: Board, me: Player) -> int:
        choices = board.available_positions()
        if not choices:
            raise RuntimeError("No available moves")
        return random.choice(choices)
