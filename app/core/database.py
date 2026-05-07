import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. LOAD .env BIAR BISA BACA DATABASE_URL
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("❌ DATABASE_URL tidak ditemukan!")

DB_URL = DB_URL.strip().strip("'").strip('"')

# 2. LOGIKA SSL DINAMIS (Biar localhost gak crash)
konfigurasi_koneksi = {}
if "localhost" not in DB_URL and "127.0.0.1" not in DB_URL:
    konfigurasi_koneksi = {"ssl": "require"}
    print("🔒 Mode SSL Aktif")
else:
    print("🔓 Mode Non-SSL (Localhost)")

# 3. FIX PROTOCOL
if "postgresql+asyncpg://" not in DB_URL:
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)

if "?" in DB_URL:
    DB_URL = DB_URL.split("?")[0]

engine = create_async_engine(
    DB_URL,
    echo=True,
    connect_args=konfigurasi_koneksi 
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session