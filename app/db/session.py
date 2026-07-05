from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import get_database_config

_engine: Engine | None = None
_session_local: sessionmaker[Session] | None = None


def create_database_engine() -> Engine:
    database_config = get_database_config()

    return create_engine(
        database_config.connection_string,
        pool_pre_ping=True,
    )


def get_engine() -> Engine:
    global _engine

    if _engine is None:
        _engine = create_database_engine()

    return _engine


def get_session_local() -> sessionmaker[Session]:
    global _session_local

    if _session_local is None:
        _session_local = sessionmaker(
            bind=get_engine(),
            autoflush=False,
            autocommit=False,
        )

    return _session_local


def get_session() -> Generator[Session, None, None]:
    session_local = get_session_local()

    with session_local() as session:
        yield session
