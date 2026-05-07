import datetime
from sqlalchemy import Column, DateTime, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Data dasar
    title = Column(String, index=True) 
    amount = Column(Float)          
    category = Column(String)          
    
    tanggal_tempo = Column(String, nullable=True)   
    tenor_berjalan = Column(Integer, nullable=True)  
    total_tenor = Column(Integer, nullable=True)
    platform = Column(String, nullable=True)        

    user = relationship("User", back_populates="transactions")
    last_paid_at = Column(DateTime, nullable=True)

class PaymentLog(Base):
    __tablename__ = "payment_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    title = Column(String)
    amount = Column(Float)
    paid_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))