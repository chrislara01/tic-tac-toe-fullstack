from __future__ import annotations

import logging
import uuid
from typing import Optional, Tuple

from ..domain.ai.factory import strategy_for
from ..domain.board import Board
from ..domain.enums import Difficulty, GameStatus, Player
from ..domain.exceptions import GameOverError, InvalidMoveError
from ..domain.game import Game
from ..repositories.base import GameRepository

logger = logging.getLogger(__name__)


class GameService:
    def __init__(self, repo: GameRepository) -> None:
        self.repo = repo

    def create_game(
        self,
        difficulty: Difficulty,
        first_player_is_human: bool,
        human_symbol: Player,
    ) -> Game:
        gid = str(uuid.uuid4())
        game = Game.new(gid, difficulty=difficulty, first_player_is_human=first_player_is_human, human_symbol=human_symbol)
        # If computer starts, make its opening move
        if not first_player_is_human and game.status == GameStatus.IN_PROGRESS:
            ai = strategy_for(difficulty)
            pos = ai.select_move(game.board, game.computer_symbol)
            game.apply_move(pos, game.computer_symbol)
            logger.info("ai_opening_move", extra={"game_id": game.id, "pos": pos, "difficulty": difficulty.value})
        self.repo.save(game)
        return game

    def get_game(self, game_id: str) -> Optional[Game]:
        return self.repo.get(game_id)

    def play_human_move(self, game_id: str, position: int) -> Tuple[Game, Optional[int]]:
        game = self.repo.get(game_id)
        if not game:
            raise KeyError("game_not_found")
        if game.status != GameStatus.IN_PROGRESS:
            raise GameOverError("game_is_over")
        if game.next_player != game.human_symbol:
            # Only allow human move when it's their turn
            raise InvalidMoveError("not_human_turn")

        game.apply_move(position, game.human_symbol)
        human_move = position

        ai_move: Optional[int] = None
        # If game still in progress, AI responds
        if game.status == GameStatus.IN_PROGRESS:
            ai = strategy_for(game.difficulty)
            ai_move = ai.select_move(game.board, game.computer_symbol)
            game.apply_move(ai_move, game.computer_symbol)
            logger.info("ai_move", extra={"game_id": game.id, "pos": ai_move, "difficulty": game.difficulty.value})

        self.repo.save(game)
        return game, ai_move
