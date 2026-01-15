from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate

# Logic Create Transaksi (Otomatis nempel ke user yg login)
async def create_transaction(db: AsyncSession, transaction: TransactionCreate, user_id: int):
    # Kita bongkar data dari schema, terus tambahin owner_id
    db_transaction = Transaction(**transaction.model_dump(), owner_id=user_id)
    
    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction

# Logic Get Transaksi (Cuma ambil punya user yg login)
async def get_transactions(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Transaction)
        .filter(Transaction.owner_id == user_id) # <--- Filter penting!
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# FUNGSI DELETE
async def remove_transaction(db: AsyncSession, transaction_id: int, user_id: int):
    # 1. Cari dulu barangnya pake select()
    result = await db.execute(
        select(Transaction).filter(Transaction.id == transaction_id, Transaction.owner_id == user_id)
    )
    trx = result.scalars().first()
    
    # 2. Kalau ketemu, HAPUS.
    if trx:
        await db.delete(trx)
        await db.commit()
    
    return trx