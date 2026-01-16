from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import check_db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Цей код виконується при старті сервера
    await check_db_connection()
    yield
    # Цей код виконується при вимкненні (закриваємо пули)
    from src.database import engine
    await engine.dispose()

app = FastAPI(title="Treehouse API", lifespan=lifespan)

# Налаштування CORS (щоб фронтенд міг стукатись)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Поки дозволяємо всім (для розробки)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Treehouse API", "status": "operational"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}