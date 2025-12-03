from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from app.domain.board import Board
from app.domain.enums import Difficulty, GameStatus, Player


@dataclass
class Game:
    id: str
    board: Board
    next_player: Player
    difficulty: Difficulty
    status: GameStatus
    human_symbol: Player
    computer_symbol: Player
    moves: List[int] = field(default_factory=list)  # positions in numpad layout 1..9
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def with_board(self, board: Board) -> "Game":
        self.board = board
        self.updated_at = datetime.now(timezone.utc)
        # update status
        w = board.winner()
        if w == Player.X:
            self.status = GameStatus.X_WON
        elif w == Player.O:
            self.status = GameStatus.O_WON
        elif board.is_draw():
            self.status = GameStatus.DRAW
        else:
            self.status = GameStatus.IN_PROGRESS
        return self

    def apply_move(self, position: int, player: Player) -> "Game":
        # mutate in-place for simplicity; repository will persist
        self.board = self.board.with_move(position, player)
        self.moves.append(position)
        self.updated_at = datetime.now(timezone.utc)
        # update status
        w = self.board.winner()
        if w == Player.X:
            self.status = GameStatus.X_WON
        elif w == Player.O:
            self.status = GameStatus.O_WON
        elif self.board.is_draw():
            self.status = GameStatus.DRAW
        else:
            self.status = GameStatus.IN_PROGRESS
        # flip next player if still playing
        if self.status == GameStatus.IN_PROGRESS:
            self.next_player = self.next_player.other
        return self

    @staticmethod
    def new(
        game_id: str,
        difficulty: Difficulty,
        first_player_is_human: bool,
        human_symbol: Player = Player.X,
    ) -> "Game":
        human_symbol = Player(human_symbol)
        computer_symbol = human_symbol.other
        next_player = human_symbol if first_player_is_human else computer_symbol
        return Game(
            id=game_id,
            board=Board.empty(),
            next_player=next_player,
            difficulty=difficulty,
            status=GameStatus.IN_PROGRESS,
            human_symbol=human_symbol,
            computer_symbol=computer_symbol,
            moves=[],
        )
