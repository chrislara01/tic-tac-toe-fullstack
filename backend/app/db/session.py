from __future__ import annotations

from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import Settings
import logging

settings = Settings.from_env()
logger = logging.getLogger(__name__)

def _normalize_url(url: str) -> str:
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+psycopg2://", 1)
    return url

_engine = create_engine(_normalize_url(settings.database_url)) if settings.database_url else None
_SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False) if _engine else None


def get_engine():
    if _engine is None:
        raise RuntimeError("DATABASE_URL not configured; engine is unavailable")
    return _engine


def get_session() -> Generator[Session, None, None]:
    if _SessionLocal is None:
        raise RuntimeError("DATABASE_URL not configured; cannot create DB session")
    db: Session = _SessionLocal()
    try:
        logger.debug("db_session_opened")
        yield db
        db.commit()
        logger.debug("db_session_committed")
    except Exception:
        logger.exception("db_session_error")
        db.rollback()
        logger.debug("db_session_rolled_back")
        raise
    finally:
        db.close()
        logger.debug("db_session_closed")
