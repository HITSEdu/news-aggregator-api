from fastapi import FastAPI, APIRouter
from app.routes.auth import router as auth_router
from contextlib import asynccontextmanager
from app.models.database import engine, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске приложения
    print("Creating tables...")
    await create_tables()
    yield
    # При остановке приложения
    print("Disposing engine...")
    await engine.dispose()


# Создаем приложение с включенной документацией
app = FastAPI(
    title="My API",
    description="API Documentation",
    version="1.0.0",
    docs_url="/docs",  # Включить Swagger по /docs (это значение по умолчанию)
    redoc_url="/redoc",  # Включить ReDoc по /redoc (опционально)
    lifespan=lifespan,
)

router = APIRouter()

# Подключаем роутеры
router.include_router(auth_router)


# Корневой эндпоинт
@router.get("/")
async def get_root():
    return {"message": "hello world"}


# Подключаем основной роутер к приложению
app.include_router(router)
