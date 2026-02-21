from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import create_tables

# Создаём приложение FastAPI
app = FastAPI(
    title="Educational Platform API",
    description="API для управления учебными материалами и заданиями",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
    openapi_url="/openapi.json"
)

# CORS настройки (разрешаем все источники для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаём таблицы при запуске
create_tables()

# Подключаем роуты
app.include_router(router)

# Главная страница
@app.get("/")
async def root():
    return {
        "message": "Добро пожаловать в Educational Platform API!",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }
