from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.errors import ErrorResponse
from ..schemas.game import (
    CreateGameRequest,
    CreateGameResponse,
    MoveRequest,
    MoveResponse,
)
from ..services.game_service import GameService
from ..repositories.memory import InMemoryGameRepository
from ..domain.enums import Difficulty, Player
from ..domain.exceptions import GameOverError, InvalidMoveError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])

# Simple dependency: use in-memory repo for now. Replace with DB-backed repo later.
_repo = InMemoryGameRepository()
_service = GameService(_repo)

def get_service() -> GameService:
    return _service


@router.post("", response_model=CreateGameResponse, responses={400: {"model": ErrorResponse}})
async def create_game(payload: CreateGameRequest, svc: GameService = Depends(get_service)) -> CreateGameResponse:
    try:
        first_is_human = payload.first_player == "human"
        game = svc.create_game(
            difficulty=payload.difficulty,
            first_player_is_human=first_is_human,
            human_symbol=payload.human_symbol,
        )
        return CreateGameResponse(
            id=game.id,
            board=game.board.to_string(),
            next_player=game.next_player,
            difficulty=game.difficulty,
            status=game.status,
            human_symbol=game.human_symbol,
            computer_symbol=game.computer_symbol,
            moves=game.moves,
            created_at=game.created_at,
            updated_at=game.updated_at,
        )
    except Exception as e:
        logger.exception("create_game_failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{game_id}", response_model=CreateGameResponse, responses={404: {"model": ErrorResponse}})
async def get_game(game_id: str, svc: GameService = Depends(get_service)) -> CreateGameResponse:
    game = svc.get_game(game_id)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="game_not_found")
    return CreateGameResponse(
        id=game.id,
        board=game.board.to_string(),
        next_player=game.next_player,
        difficulty=game.difficulty,
        status=game.status,
        human_symbol=game.human_symbol,
        computer_symbol=game.computer_symbol,
        moves=game.moves,
        created_at=game.created_at,
        updated_at=game.updated_at,
    )


@router.post("/{game_id}/moves", response_model=MoveResponse, responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 409: {"model": ErrorResponse}})
async def post_move(game_id: str, payload: MoveRequest, svc: GameService = Depends(get_service)) -> MoveResponse:
    try:
        game, ai_move = svc.play_human_move(game_id, payload.position)
        return MoveResponse(
            id=game.id,
            board=game.board.to_string(),
            next_player=game.next_player,
            difficulty=game.difficulty,
            status=game.status,
            human_symbol=game.human_symbol,
            computer_symbol=game.computer_symbol,
            moves=game.moves,
            created_at=game.created_at,
            updated_at=game.updated_at,
            ai_move=ai_move,
        )
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="game_not_found")
    except GameOverError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidMoveError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.exception("post_move_failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
