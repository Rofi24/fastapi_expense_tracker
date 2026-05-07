from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.transaction import PaymentLog, Transaction
from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.models.user import User
# Pastikan import get_current_user sesuai dengan lokasi file dependencies lu
from app.dependencies import get_current_user

router = APIRouter()

# Endpoint nambah transaksi/cicilan baru
@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pydantic schema di-unpack langsung ke model SQLAlchemy
    new_transaction = Transaction(
        **transaction.model_dump(),
        user_id=current_user.id
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

# Endpoint narik semua data transaksi user yang lagi login
@router.get("/", response_model=List[TransactionResponse])
async def read_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Transaction).where(Transaction.user_id == current_user.id)
    )
    transactions = result.scalars().all()
    return transactions

# Endpoint buat update data (Edit)
@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) :
    # 1. Cari datanya dulu
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    )
    db_transaction = result.scalar_one_or_none()
    
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Catatan tidak ditemukan")
    
    # 2. Update field yang dikirim dari frontend
    update_data = transaction_update.model_dump()
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
        
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

# Endpoint hapus transaksi
@router.delete("/{transaction_id}")
async def delete_transaction(
    transaction_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == current_user.id)
    )
    transaction = result.scalar_one_or_none()
    
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaksi tidak ditemukan")
        
    await db.delete(transaction)
    await db.commit()
    return {"message": "Transaksi berhasil dihapus"}

# Endpoint buat proses bayar
@router.post("/{transaction_id}/pay")
async def pay_transaction(transaction_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id, Transaction.user_id == current_user.id))
    trx = result.scalar_one_or_none()
    
    if not trx: raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    
    trx.last_paid_at = datetime.now() # Catat waktu bayar sekarang
    if trx.category == "Cicilan": trx.tenor_berjalan += 1 # Tenor otomatis naik
    
    new_log = PaymentLog(transaction_id=trx.id, title=trx.title, amount=trx.amount, user_id=current_user.id)
    db.add(new_log)
    await db.commit()
    return {"message": "Lunas bro!"}

# Endpoint buat tarik data riwayat
@router.get("/history/logs")
async def get_payment_logs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(PaymentLog).where(PaymentLog.user_id == current_user.id).order_by(PaymentLog.paid_at.desc()).limit(10))
    return result.scalars().all()