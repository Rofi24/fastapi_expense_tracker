import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# --- AMBIL URL LANGSUNG DARI ENV ---
DB_URL = os.getenv("DATABASE_URL", "")

# --- LOGIC FIX URL POSTGRES (Supaya Asyncpg mau baca) ---
if DB_URL:
    DB_URL = DB_URL.strip("'").strip('"')
    
    # Ubah postgres:// jadi postgresql+asyncpg://
    if "postgresql+asyncpg://" not in DB_URL:
        if DB_URL.startswith("postgres://"):
            DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
        elif DB_URL.startswith("postgresql://"):
            DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

if not DB_URL:
    print("⚠️ WARNING: DATABASE_URL is missing! Server might crash.")

# --- BIKIN ENGINE ---
engine = create_async_engine(DB_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session