from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.crud import crud_transaction
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

# 1. Endpoint buat CATAT Transaksi
@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- SI SATPAM
):
    # Kita ambil ID user dari token, terus kirim ke CRUD
    return await crud_transaction.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

# 2. Endpoint buat LIHAT History Transaksi
@router.get("/", response_model=List[TransactionResponse])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user) # <--- SI SATPAM
):
    # Cuma balikin data punya user yang lagi login
    return await crud_transaction.get_transactions(db=db, user_id=current_user.id, skip=skip, limit=limit)