import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. AMBIL URL DARI ENV
DB_URL = os.getenv("DATABASE_URL")

# 2. CEK APAKAH URL ADA?
if not DB_URL:
    raise ValueError("❌ FATAL ERROR: DATABASE_URL tidak ditemukan! Cek Environment Variables di Vercel.")

# 3. BERSIHKAN URL
DB_URL = DB_URL.strip().strip("'").strip('"')

# 4. FIX PROTOCOL (Wajib buat Asyncpg)
if "postgresql+asyncpg://" not in DB_URL:
    if DB_URL.startswith("postgres://"):
        DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
    elif DB_URL.startswith("postgresql://"):
        DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# 5. --- JURUS ANTI-ERROR SSLMODE ---
# Asyncpg bakal crash kalau ada '?sslmode=' di URL. Kita buang bagian itu.
if "?" in DB_URL:
    DB_URL = DB_URL.split("?")[0]  # Ambil bagian depan tanda tanya aja

print(f"✅ CLEANED DB URL: {DB_URL}") # Debugging (aman, password gak ke-print full biasanya)

# 6. BIKIN ENGINE DENGAN SSL EXPLICIT
# Kita masukin settingan SSL lewat connect_args, bukan lewat URL
engine = create_async_engine(
    DB_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={"ssl": "require"}  # <-- INI KUNCINYA BIAR NEON MAU KONEK
)

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