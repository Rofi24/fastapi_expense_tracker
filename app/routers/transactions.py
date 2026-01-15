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

# 3. ENDPOINT DELETE
@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    # Pake await karena crud-nya async
    deleted_item = await crud_transaction.remove_transaction(
        db=db, 
        transaction_id=transaction_id, 
        user_id=current_user.id
    )
    
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
        
    return {"message": "Berhasil dihapus"}

# 4, ENDPOIT EDIT
@router.put("/{transaction_id}")
async def update_transaction(
    transaction_id: int, 
    transaction_data: TransactionCreate, # pake schema Create buat update
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    updated_item = await crud_transaction.update_transaction(
        db=db, 
        transaction_id=transaction_id, 
        transaction_data=transaction_data, 
        user_id=current_user.id
    )
    
    if not updated_item:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
        
    return updated_item