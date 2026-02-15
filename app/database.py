import pathlib

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import get_database_uri, SQLITE_FALLBACK_URI


class Base(DeclarativeBase):
    pass


engine = None
async_session_factory = None


async def _create_engine_and_tables(uri: str):
    if "sqlite" in uri:
        pathlib.Path("instance").mkdir(exist_ok=True)
    eng = create_async_engine(uri, echo=False)
    from app import models  # noqa: F401
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return eng


async def init_db():
    global engine, async_session_factory
    uri = get_database_uri()
    try:
        engine = await _create_engine_and_tables(uri)
    except (OperationalError, OSError):
        if "sqlite" in uri:
            raise
        print(
            "PostgreSQL недоступен, используется SQLite:",
            SQLITE_FALLBACK_URI,
        )
        engine = await _create_engine_and_tables(SQLITE_FALLBACK_URI)
    async_session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )


def get_session_factory():
    return async_session_factory
