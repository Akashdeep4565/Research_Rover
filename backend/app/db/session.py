"""
Database engine and async session management for Research Rover
"""
import os
from typing import AsyncGenerator, Optional, Any
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from app.core.config import get_settings
from app.db.models import Base


# Configure SQLite connection pragmas (foreign keys, busy timeout, synchronous)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Ensure SQLite enforces foreign keys and handles concurrent access reliably"""
    try:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.execute("PRAGMA busy_timeout=30000;")
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()
    except Exception:
        # Ignore for non-SQLite connections or mock engines
        pass


_engine: Optional[AsyncEngine] = None


def get_engine(db_url_override: Optional[str] = None) -> AsyncEngine:
    """Get or create singleton async database engine"""
    global _engine
    if db_url_override:
        return create_async_engine(db_url_override, echo=False)
    
    if _engine is None:
        settings = get_settings()
        os.makedirs(settings.DATA_FOLDER, exist_ok=True)
        _engine = create_async_engine(settings.DATABASE_URL, echo=False)
    return _engine


def get_session_factory(engine_instance: Optional[AsyncEngine] = None, settings_instance: Optional[Any] = None):
    """Get async sessionmaker bound to engine"""
    if engine_instance:
        eng = engine_instance
    elif settings_instance and getattr(settings_instance, "DATABASE_URL", None):
        eng = get_engine(settings_instance.DATABASE_URL)
    else:
        eng = get_engine()
    return async_sessionmaker(
        bind=eng,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False
    )


async_session_factory = get_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for obtaining an async database session"""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db(engine_override: Optional[AsyncEngine] = None) -> None:
    """Initialize database tables idempotently and set WAL journal mode once"""
    eng = engine_override or get_engine()
    async with eng.begin() as conn:
        try:
            await conn.execute(text("PRAGMA journal_mode=WAL;"))
        except Exception:
            pass
        await conn.run_sync(Base.metadata.create_all)
