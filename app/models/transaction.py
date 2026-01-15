from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, default="General")
    description = Column(String, nullable=True)
    
    # func.now() biar otomatis ngisi tanggal saat ini pas data dibuat
    date_posted = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Key: Ini "tali" pengikat ke tabel users (users.id)
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relasi biar codingan enak: transaction.owner
    owner = relationship("User", backref="transactions")