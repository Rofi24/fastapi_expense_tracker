from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship # <-- Tambahin ini
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Tambahin baris ini biar User kenal sama daftar transaksinya
    transactions = relationship("Transaction", back_populates="user")