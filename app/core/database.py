import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings 

# 1. Ambil URL Database
DB_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# 2. Fix Bug URL Render
if DB_URL and DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# 3. Bikin Engine
engine = create_async_engine(DB_URL, echo=True)

# 4. Bikin Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# 5. Base Model
Base = declarative_base()

# 6. Dependency Injection
async def get_db():
    async with SessionLocal() as session:
        yield session