import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Create Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Session Factory
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

class Base(AsyncAttrs, DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

async def get_db():
    """Dependency for dependency injection in routes."""
    async with SessionLocal() as session:
        yield session

async def check_db_connection():
    """
    Checks the database connection by executing a simple SELECT 1 query.
    Returns True if successful, False otherwise.
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info(f"Database connected! Result: {result.scalar()}")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
