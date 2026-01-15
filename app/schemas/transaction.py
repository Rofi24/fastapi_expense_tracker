from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base Schema (Field dasar)
class TransactionBase(BaseModel):
    title: str
    amount: float
    category: str = "General"
    description: Optional[str] = None

# Schema buat Create (Input dari user)
class TransactionCreate(TransactionBase):
    pass

# Schema buat Response (Output ke user)
class TransactionResponse(TransactionBase):
    id: int
    date_posted: datetime
    owner_id: int

    class Config:
        from_attributes = True