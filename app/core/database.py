import os
import ssl
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("❌ DATABASE_URL tidak ditemukan!")

DB_URL = DB_URL.strip().strip("'").strip('"')

# Fix Protocol untuk Asyncpg
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql+asyncpg://", 1)
elif DB_URL.startswith("postgresql://") and "asyncpg" not in DB_URL:
    DB_URL = DB_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

# Bersihin URL dari parameter bawaan Neon biar asyncpg gak bingung
if "?" in DB_URL:
    DB_URL = DB_URL.split("?")[0]

# BIKIN SERTIFIKAT SSL ANTI-REWEL
konfigurasi_koneksi = {}
if "localhost" not in DB_URL and "127.0.0.1" not in DB_URL:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    konfigurasi_koneksi = {"ssl": ctx}
    print("🔒 Mode SSL Aktif (Production) via SSLContext")
else:
    print("🔓 Mode Non-SSL (Localhost)")

engine = create_async_engine(
    DB_URL,
    echo=False,
    connect_args=konfigurasi_koneksi
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autocommit=False, autoflush=False)
Base = declarative_base()

async def get_db():
    async with SessionLocal() as session:
        yield session