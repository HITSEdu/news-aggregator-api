from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres:5432/appdb"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логирование SQL запросов (можно отключить в production)
    future=True,
    poolclass=NullPool,  # Или используйте AsyncAdaptedQueuePool для пула соединений
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    future=True,
)

Base = declarative_base()


async def get_db(): 
    """
    Генератор сессий для зависимостей FastAPI
    """
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)