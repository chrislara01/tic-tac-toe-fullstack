from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from ..domain.board import Board
from ..domain.enums import Difficulty, GameStatus, Player
from ..domain.game import Game
from ..db.models import GameModel
from .base import GameRepository


class SQLAlchemyGameRepository(GameRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, game_id: str) -> Optional[Game]:
        model = self.session.get(GameModel, game_id)
        if not model:
            return None
        return self._to_domain(model)

    def save(self, game: Game) -> Game:
        model = self.session.get(GameModel, game.id)
        if model is None:
            model = GameModel(
                id=game.id,
                board=game.board.to_string(),
                next_player=game.next_player.value,
                difficulty=game.difficulty.value,
                status=game.status.value,
                human_symbol=game.human_symbol.value,
                computer_symbol=game.computer_symbol.value,
                moves=list(game.moves) if game.moves else [],
                created_at=game.created_at,
                updated_at=game.updated_at,
            )
            self.session.add(model)
        else:
            model.board = game.board.to_string()
            model.next_player = game.next_player.value
            model.difficulty = game.difficulty.value
            model.status = game.status.value
            model.human_symbol = game.human_symbol.value
            model.computer_symbol = game.computer_symbol.value
            model.moves = list(game.moves) if game.moves else []
            model.updated_at = game.updated_at
        # Commit is managed by dependency in get_session
        return game

    @staticmethod
    def _to_domain(model: GameModel) -> Game:
        return Game(
            id=model.id,
            board=Board.from_string(model.board),
            next_player=Player(model.next_player),
            difficulty=Difficulty(model.difficulty),
            status=GameStatus(model.status),
            human_symbol=Player(model.human_symbol),
            computer_symbol=Player(model.computer_symbol),
            moves=list(model.moves or []),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
