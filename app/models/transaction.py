from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
# Import User biar bisa relasi
from app.models.user import User

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float, nullable=False)  # Bisa minus (pengeluaran) atau plus (pemasukan)
    category = Column(String, default="General")
    description = Column(String, nullable=True)
    date_posted = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Key: Link ke tabel users
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relasi biar gampang akses data owner dari transaksi
    owner = relationship("User", backref="transactions")