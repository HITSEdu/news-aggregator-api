from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.models.database import engine, create_tables
from app.models.news import load_initial_news_by_ticker
from app.models.price import load_prices_for_ticker
from app.models.ticker import create_initial_tickers, get_tickers
from app.routes.auth import router as auth_router
from app.routes.news import news_router
from app.routes.price import router as price_router
from app.routes.tickets import router as ticket_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    await create_initial_tickers()
    tickers = await get_tickers()
    for ticker in tickers:
        await load_prices_for_ticker(ticker=ticker.name, ticker_id=ticker.id)
        await load_initial_news_by_ticker(ticker_name=ticker.name)
    yield
    await engine.dispose()


app = FastAPI(
    title="Trading API",
    description="API Documentation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

router.include_router(auth_router)
router.include_router(price_router)
router.include_router(ticket_router)
router.include_router(news_router)

app.include_router(router)

# uvicorn app.main:app --host 0.0.0.0 --port 8000
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
