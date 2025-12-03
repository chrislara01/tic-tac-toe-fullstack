from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.errors import ErrorResponse
from app.schemas.game import (
    CreateGameRequest,
    CreateGameResponse,
    MoveRequest,
    MoveResponse,
)
from app.services.game_service import GameService
from app.repositories.memory import InMemoryGameRepository
from app.core.settings import Settings
from app.domain.exceptions import GameOverError, InvalidMoveError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/games", tags=["games"])

_settings = Settings.from_env()
_memory_repo = InMemoryGameRepository()
_memory_service = GameService(
    _memory_repo,
    gemini_api_key=_settings.gemini_api_key,
    gemini_model=_settings.gemini_model,
)
_use_db = bool(_settings.database_url)

def maybe_session():
    if not _use_db:
        # DB disabled; no session
        yield None
        return
    # Import only when DB is enabled to avoid hard dependency when not used
    from app.db.session import get_session
    # Delegate lifecycle to get_session generator
    yield from get_session()


def get_service(db: Any = Depends(maybe_session)) -> GameService:
    if _use_db and db is not None:
        # Dynamic import to avoid top-level dependency
        from app.repositories.sqlalchemy import SQLAlchemyGameRepository

        repo = SQLAlchemyGameRepository(db)
        return GameService(
            repo,
            gemini_api_key=_settings.gemini_api_key,
            gemini_model=_settings.gemini_model,
        )
    return _memory_service


@router.post("", response_model=CreateGameResponse, responses={400: {"model": ErrorResponse}})
async def create_game(payload: CreateGameRequest, svc: GameService = Depends(get_service)) -> CreateGameResponse:
    try:
        first_is_human = payload.first_player == "human"
        game = svc.create_game(
            difficulty=payload.difficulty,
            first_player_is_human=first_is_human,
            human_symbol=payload.human_symbol,
        )
        logger.info(
            "create_game_ok",
            extra={
                "game_id": game.id,
                "difficulty": game.difficulty.value,
                "first_player": payload.first_player,
                "human_symbol": payload.human_symbol.value,
            },
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
    logger.debug("get_game_ok", extra={"game_id": game_id, "status": game.status.value})
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
        logger.info(
            "human_move_ok",
            extra={"game_id": game_id, "human_pos": payload.position, "ai_pos": ai_move},
        )
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
