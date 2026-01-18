import asyncio

from sqlalchemy import text
from src.database import engine


async def add_dns_column():
    async with engine.begin() as conn:
        try:
            print("Attempting to add dns_name column...")
            await conn.execute(text("ALTER TABLE infrastructure_items ADD COLUMN IF NOT EXISTS dns_name VARCHAR;"))
            print("Column 'dns_name' added successfully (if it didn't exist).")
        except Exception as e:
            print(f"Error adding column: {e}")

if __name__ == "__main__":
    asyncio.run(add_dns_column())
