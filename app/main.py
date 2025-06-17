from fastapi import FastAPI, APIRouter
from app.routes.auth import router as auth_router
from contextlib import asynccontextmanager
from app.models.database import engine, create_tables
from app.models.ticker import create_initial_tickers, get_tickers
from app.models.price import load_prices_for_ticker
from app.models.news import load_initial_news_by_ticker
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables...")
    await create_tables()
    await create_initial_tickers()
    tickers = await get_tickers()
    for ticker in tickers:
        await load_prices_for_ticker(ticker=ticker.name, ticker_id=ticker.id)
        await load_initial_news_by_ticker(ticker_name=ticker.name)
    await load_prices_for_ticker("GAZP", 2)
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
