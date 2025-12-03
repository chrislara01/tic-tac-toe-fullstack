from __future__ import annotations

from typing import Iterable, List

from app.domain.board import Board
from app.domain.enums import Player
from app.domain.ai.base import Strategy


PRIORITY_CORNERS = [7, 9, 1, 3]
PRIORITY_SIDES = [8, 4, 6, 2]
CENTER = 5


class HeuristicStrategy(Strategy):
    def select_move(self, board: Board, me: Player) -> int:
        # 1) Win if possible
        for pos in board.available_positions():
            if board.with_move(pos, me).winner() == me:
                return pos
        # 2) Block opponent win
        opp = me.other
        for pos in board.available_positions():
            if board.with_move(pos, opp).winner() == opp:
                return pos
        # 3) Take center
        if CENTER in board.available_positions():
            return CENTER
        # 4) Take a corner
        for pos in PRIORITY_CORNERS:
            if pos in board.available_positions():
                return pos
        # 5) Take a side
        for pos in PRIORITY_SIDES:
            if pos in board.available_positions():
                return pos
        # fallback (shouldn't happen)
        avail = board.available_positions()
        if not avail:
            raise RuntimeError("No available moves")
        return avail[0]
