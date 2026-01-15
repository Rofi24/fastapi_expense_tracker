from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, engine, Base

# PENTING: Import models di sini biar kebaca sama engine
from app.models import user, transaction
from app.routers import auth

# Ini fungsi yang jalan otomatis pas Server Start
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables in database...")
    async with engine.begin() as conn:
        # Perintah ajaib buat create table kalau belum ada
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created!")
    yield

app = FastAPI(title="Expense Tracker API", lifespan=lifespan)

app.include_router(auth.router, tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Server Expense Tracker is Running!"}

@app.get("/check-db")
async def check_db(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "Database Connected Successfully!"}
    except Exception as e:
        return {"status": "Database Connection Failed", "error": str(e)}