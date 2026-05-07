from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Data dasar
    title = Column(String, index=True) # Misal: "Cicilan Rumah"
    amount = Column(Float)             # Nominal
    category = Column(String)          # Isinya: "Rutin" atau "Cicilan"
    
    # Data tambahan buat tracking cicilan (seperti di Excel lu)
    tanggal_tempo = Column(String, nullable=True)   # Misal: "11 mei, 11 jun"
    tenor_berjalan = Column(Integer, nullable=True)  # Cicilan ke-berapa (misal: 1)
    total_tenor = Column(Integer, nullable=True)     # Total tenor (misal: 3)
    platform = Column(String, nullable=True)         # Misal: "shopee", "tiktok", "adakami"

    user = relationship("User", back_populates="transactions")