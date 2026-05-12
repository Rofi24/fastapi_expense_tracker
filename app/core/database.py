import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. LOAD .env BIAR BISA BACA DATABASE_URL (Di local baca .env, di Render baca env server)
load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

if not DB_URL:
    raise ValueError("❌ DATABASE_URL tidak ditemukan! Pastikan sudah setting di .env atau Render.")

DB_URL = DB_URL.strip().strip("'").strip('"')

# 2. LOGIKA SSL DINAMIS (Biar localhost gak crash, tapi Neon aman)
konfigurasi_koneksi = {}
if "localhost" not in DB_URL and "127.0.0.1" not in DB_URL:
    konfigurasi_koneksi = {"ssl": "true"}
    print("🔒 Mode SSL Aktif (Production)")
else:
    print("🔓 Mode Non-SSL (Localhost)")

# 3. FIX PROTOCOL (Neon kasih postgresql://, asyncpg butuh postgresql+asyncpg://)
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DB_URL.startswith("postgresql://") and "asyncpg" not in DB_URL:
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Buang parameter ?sslmode=require bawaan Neon karena asyncpg maunya lewat connect_args (Logika lu udah bener banget!)
if "?" in DB_URL:
    DB_URL = DB_URL.split("?")[0]

engine = create_async_engine(
    DB_URL,
    echo=False, # Saran: Ubah jadi False biar log terminal di Render nggak terlalu penuh sama query SQL
    connect_args=konfigurasi_koneksi 
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session