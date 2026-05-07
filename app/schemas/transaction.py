from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    title: str
    amount: float
    category: str
    tanggal_tempo: Optional[str] = None
    tenor_berjalan: Optional[int] = None
    total_tenor: Optional[int] = None
    platform: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    last_paid_at: Optional[datetime] = None
    user_id: int

    class Config:
        from_attributes = True