import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. AMBIL URL DARI ENV
DB_URL = os.getenv("DATABASE_URL")

# 2. CEK APAKAH URL ADA?
if not DB_URL:
    raise ValueError("FATAL ERROR: DATABASE_URL tidak ditemukan! Cek Environment Variables di Vercel.")

# 3. BERSIHKAN URL (Hapus spasi/kutip yang nyangkut)
DB_URL = DB_URL.strip().strip("'").strip('"')

# 4. LOGIC GANTI PROTOCOL (Biar Asyncpg mau jalan)
if "postgresql+asyncpg://" not in DB_URL:
    if DB_URL.startswith("postgres://"):
        DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DB_URL.startswith("postgresql://"):
        DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

print(f"CONNECTING TO DATABASE: {DB_URL.split('@')[1] if '@' in DB_URL else 'UNKNOWN'}") # Print host doang biar aman

# 5. BIKIN ENGINE
try:
    engine = create_async_engine(DB_URL, echo=True, pool_pre_ping=True)
except Exception as e:
    print(f"ERROR CREATING ENGINE. URL: {DB_URL}")
    raise e

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