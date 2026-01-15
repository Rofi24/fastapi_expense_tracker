from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Bikin Engine (Mesin Koneksi)
# echo=True biar kita bisa liat SQL query-nya di terminal (bagus buat debug)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 2. Bikin Session Factory
# Ini pabrik yang bakal bikinin session database buat tiap request user
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# 3. Base Class buat Model
# Nanti semua tabel (User, Transaction) bakal inherit dari class ini
Base = declarative_base()

# 4. Dependency Injection
# Fungsi ini bakal dipake di setiap Route API buat dapet koneksi DB
async def get_db():
    async with SessionLocal() as session:
        yield session