from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, engine, Base
from app.models import user, transaction
from app.routers import auth, transactions
from fastapi.middleware.cors import CORSMiddleware

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
app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Boleh diakses dari mana aja
    allow_credentials=True,
    allow_methods=["*"],  # Boleh method apa aja (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Boleh header apa aja
)


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