from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from src.config import settings

# Створюємо асинхронний двигун
engine = create_async_engine(settings.DATABASE_URL, echo=True)

async def check_db_connection():
    """Перевірка з'єднання (просто робить SELECT 1)"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print(f"✅ Database connected! Result: {result.scalar()}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False