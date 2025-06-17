from fastapi import FastAPI, APIRouter
from app.routes.auth import router as auth_router
from contextlib import asynccontextmanager
from app.models.database import engine, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    await create_tables()
    yield
    print("Disposing engine...")
    await engine.dispose()


app = FastAPI(
    title="My API",
    description="API Documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

router = APIRouter()

router.include_router(auth_router)


@router.get("/")
async def get_root():
    return {"message": "hello world"}

app.include_router(router)
