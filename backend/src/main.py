import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

# 1. ДОДАНО: Імпорт Base для доступу до метаданих
from src.database import Base, check_db_connection, engine, get_db

# 2. ДОДАНО: Імпорт моделі, щоб вона зареєструвалася в Base.metadata
# Без цього create_all створить порожню базу
from src.models.infrastructure import InfrastructureItem  #noqa
from src.routers import infrastructure

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("backend.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This code runs on startup
    logger.info("Starting Treehouse API...")

    # 3. ДОДАНО: Примусове створення таблиць при старті
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables verified/created.")

    if not await check_db_connection():
        logger.error("Failed to connect to database on startup!")
    
    yield
    
    # This code runs on shutdown
    logger.info("Shutting down...")
    await engine.dispose()

app = FastAPI(title="Treehouse API", lifespan=lifespan)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(infrastructure.router)

@app.get("/")
async def root():
    """Root endpoint to verify service is up."""
    return {"message": "Welcome to the Treehouse API", "status": "operational"}

@app.get("/health")
async def health_check(response: Response, db: AsyncSession = Depends(get_db)):
    """
    Production health check.
    Returns 200 if DB is connected, 503 if not.
    """
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "error", "database": "disconnected", "detail": str(e)}